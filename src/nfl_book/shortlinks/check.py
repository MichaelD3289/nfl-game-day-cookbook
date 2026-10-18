"""Find dead and moved source URLs (``nfl-book prepare-links --check``).

Part of the one network command. It only reads: it never shortens a URL,
writes ``data/shortlinks.yml`` or touches a source file. Requests are sequential,
identify the tool, and wait between requests to the same host.
"""

from __future__ import annotations

import socket
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from types import TracebackType

import httpx

from nfl_book import __version__
from nfl_book.errors import Diagnostics
from nfl_book.models.content import Content
from nfl_book.shortlinks.prepare import sources_to_check

USER_AGENT = (
    f"nfl-game-day-cookbook/{__version__} link check "
    "(+https://github.com/MichaelD3289/nfl-game-day-cookbook)"
)
ACCEPT = "text/html,*/*;q=0.8"
HEADERS = {"User-Agent": USER_AGENT, "Accept": ACCEPT}

REDIRECTS = frozenset({301, 302, 303, 307, 308})
PERMANENT = frozenset({301, 308})
RETRY_STATUSES = frozenset({429, 500, 502, 503, 504})
BLOCKED_STATUSES = frozenset({401, 403, 429})
MAX_RETRY_AFTER = 60.0
DNS_MESSAGES = ("Name or service not known", "nodename nor servname", "getaddrinfo")


class ProblemKind(StrEnum):
    BROKEN = "broken"
    DNS = "dns"
    UNREACHABLE = "unreachable"
    MOVED = "moved"
    BLOCKED = "blocked"


DEAD = frozenset({ProblemKind.BROKEN, ProblemKind.DNS, ProblemKind.UNREACHABLE})


@dataclass(frozen=True)
class Outcome:
    """What one URL did. ``kind`` is ``None`` when it responded OK."""

    url: str
    kind: ProblemKind | None = None
    detail: str = ""
    status: int | None = None
    location: str | None = None

    @property
    def ok(self) -> bool:
        return self.kind is None


@dataclass(frozen=True)
class LinkProblem:
    url: str
    kind: ProblemKind
    detail: str
    files: tuple[Path, ...]
    status: int | None = None
    location: str | None = None

    @property
    def wayback(self) -> str | None:
        """Wayback Machine listing for a dead page (built offline, never requested)."""
        return f"https://web.archive.org/web/*/{self.url}" if self.kind in DEAD else None

    @property
    def summary(self) -> str:
        if self.kind is ProblemKind.MOVED and self.location:
            return f"{self.detail} to {self.location}"
        if self.location:
            return f"{self.detail} after a redirect to {self.location}"
        return self.detail


@dataclass
class CheckResult:
    checked: int
    problems: list[LinkProblem] = field(default_factory=list)
    diagnostics: Diagnostics = field(default_factory=Diagnostics)

    @property
    def ok(self) -> bool:
        return not self.problems


@dataclass(frozen=True)
class _Hop:
    """The end of one redirect chain: a response status or a transport error."""

    url: str
    status: int | None = None
    error: httpx.TransportError | None = None
    first_status: int | None = None
    redirected: bool = False
    detail: str = ""


class LinkChecker:
    """Probe URLs politely: HEAD first, then GET (headers only) when HEAD is not OK."""

    def __init__(
        self,
        client: httpx.Client | None = None,
        *,
        timeout: float = 15.0,
        retries: int = 2,
        backoff: float = 2.0,
        per_host_delay: float = 1.0,
        max_redirects: int = 10,
        sleep: Callable[[float], None] = time.sleep,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._owned = client is None
        self._client = client or httpx.Client(timeout=timeout, follow_redirects=False)
        self.retries = retries
        self.backoff = backoff
        self.per_host_delay = per_host_delay
        self.max_redirects = max_redirects
        self._sleep = sleep
        self._clock = clock
        self._last: dict[str, float] = {}

    def __enter__(self) -> LinkChecker:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close()

    def close(self) -> None:
        if self._owned:
            self._client.close()

    def check(self, url: str) -> Outcome:
        head = self._chain("HEAD", url)
        if head.status is not None and 200 <= head.status < 300:
            return self._classify(url, head)
        return self._classify(url, self._chain("GET", url))

    # --- requests -------------------------------------------------------------

    def _wait_for_host(self, url: str) -> None:
        host = httpx.URL(url).host
        last = self._last.get(host)
        if last is not None:
            wait = last + self.per_host_delay - self._clock()
            if wait > 0:
                self._sleep(wait)

    @contextmanager
    def _request(self, method: str, url: str) -> Iterator[httpx.Response]:
        self._wait_for_host(url)
        try:
            with self._client.stream(
                method, url, headers=HEADERS, follow_redirects=False
            ) as response:
                yield response  # the body is never read
        finally:
            self._last[httpx.URL(url).host] = self._clock()

    def _once(self, method: str, url: str) -> tuple[int, str | None, float | None]:
        with self._request(method, url) as response:
            return (
                response.status_code,
                response.headers.get("Location"),
                _retry_after(response),
            )

    def _attempt(
        self, method: str, url: str
    ) -> tuple[int | None, str | None, httpx.TransportError | None]:
        """One request (HEAD) or one request with retries (GET)."""
        retries = self.retries if method == "GET" else 0
        for attempt in range(retries + 1):
            try:
                status, location, retry_after = self._once(method, url)
            except httpx.TransportError as exc:
                if attempt == retries:
                    return None, None, exc
                self._sleep(self.backoff * 2**attempt)
                continue
            if status not in RETRY_STATUSES or attempt == retries:
                return status, location, None
            delay = self.backoff * 2**attempt
            if status == 429 and retry_after is not None:
                delay = retry_after
            self._sleep(delay)
        raise AssertionError("unreachable")  # pragma: no cover

    def _chain(self, method: str, url: str) -> _Hop:
        current = url
        first_status: int | None = None
        for hop in range(self.max_redirects + 1):
            status, location, error = self._attempt(method, current)
            if first_status is None:
                first_status = status
            redirected = hop > 0
            if error is not None or status is None:
                return _Hop(current, None, error, first_status, redirected)
            if status not in REDIRECTS:
                return _Hop(current, status, None, first_status, redirected)
            if not location:
                return _Hop(
                    current,
                    status,
                    None,
                    first_status,
                    redirected,
                    f"HTTP {status} without Location",
                )
            current = str(httpx.URL(current).join(location))
        return _Hop(current, None, None, first_status, True, "too many redirects")

    # --- classification -------------------------------------------------------

    def _classify(self, url: str, end: _Hop) -> Outcome:
        location = end.url if end.redirected else None
        if end.error is not None:
            if _is_dns(end.error):
                host = httpx.URL(url).host
                return Outcome(url, ProblemKind.DNS, f"DNS lookup failed for {host}")
            return Outcome(url, ProblemKind.UNREACHABLE, _describe(end.error), None, location)
        if end.status is None:
            return Outcome(url, ProblemKind.UNREACHABLE, end.detail, None, location)
        status = end.status
        if end.detail:
            return Outcome(url, ProblemKind.BROKEN, end.detail, status, location)
        if 200 <= status < 300:
            if end.redirected and end.first_status in PERMANENT:
                return Outcome(
                    url, ProblemKind.MOVED, f"HTTP {end.first_status}", end.first_status, location
                )
            return Outcome(url)
        if status in BLOCKED_STATUSES:
            return Outcome(url, ProblemKind.BLOCKED, f"HTTP {status}", status, location)
        return Outcome(url, ProblemKind.BROKEN, f"HTTP {status}", status, location)


def _retry_after(response: httpx.Response) -> float | None:
    value = response.headers.get("Retry-After", "").strip()
    if not value.isdigit():
        return None
    return min(float(value), MAX_RETRY_AFTER)


def _is_dns(error: BaseException) -> bool:
    if not isinstance(error, httpx.ConnectError):
        return False
    seen: set[int] = set()
    cause: BaseException | None = error
    while cause is not None and id(cause) not in seen:
        if isinstance(cause, socket.gaierror):
            return True
        seen.add(id(cause))
        cause = cause.__cause__ or cause.__context__
    return any(message in str(error) for message in DNS_MESSAGES)


def _describe(error: httpx.TransportError) -> str:
    if isinstance(error, httpx.TimeoutException):
        return "timed out"
    text = str(error).strip()
    return f"{type(error).__name__}: {text}" if text else type(error).__name__


# --- sources and report --------------------------------------------------------

_CODES = {
    ProblemKind.BROKEN: "link-broken",
    ProblemKind.DNS: "link-dns",
    ProblemKind.UNREACHABLE: "link-unreachable",
    ProblemKind.MOVED: "link-moved",
    ProblemKind.BLOCKED: "link-blocked",
}

_MESSAGES = {
    ProblemKind.BROKEN: "source URL {url} is dead: {summary}",
    ProblemKind.DNS: "source URL {url} is dead: {summary}",
    ProblemKind.UNREACHABLE: "source URL {url} is unreachable: {summary}",
    ProblemKind.MOVED: "source URL {url} moved permanently: {summary}",
    ProblemKind.BLOCKED: "source URL {url} could not be verified (the site refused): {summary}",
}


def check_sources(content: Content, checker: LinkChecker) -> CheckResult:
    """Check every non-retired source URL once; one diagnostic per citing file."""
    sources = sources_to_check(content)
    result = CheckResult(checked=len(sources))
    for url, files in sources.items():
        outcome = checker.check(url)
        if outcome.kind is None:
            continue
        problem = LinkProblem(
            url, outcome.kind, outcome.detail, files, outcome.status, outcome.location
        )
        result.problems.append(problem)
        message = _MESSAGES[problem.kind].format(url=url, summary=problem.summary)
        report = result.diagnostics.error if problem.kind in DEAD else result.diagnostics.warning
        for path in files:
            report(_CODES[problem.kind], message, path)
    return result


def _plural(count: int, singular: str, plural: str) -> str:
    return f"{count} {singular if count == 1 else plural}"


def _shown(path: Path, base: Path) -> str:
    try:
        return path.resolve().relative_to(base.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


_SECTIONS: tuple[tuple[str, frozenset[ProblemKind]], ...] = (
    ("Dead", DEAD),
    ("Moved permanently", frozenset({ProblemKind.MOVED})),
    ("Could not verify", frozenset({ProblemKind.BLOCKED})),
)

_SCOPE = "from recipes and components that are not retired"


def render_report(result: CheckResult, base: Path) -> str:
    """The problems as Markdown, paths relative to ``base``, and no dates."""
    urls = "source URL" if result.checked == 1 else "source URLs"
    if result.ok:
        return f"# Source link check\n\nAll {result.checked} {urls} {_SCOPE} responded OK.\n"
    attention = _plural(len(result.problems), "needs", "need")
    lines = [
        "# Source link check",
        "",
        f"Checked {result.checked} {urls} {_SCOPE}. {attention} attention.",
        "",
        "This report changes nothing. Fix `source.url` by hand in the files listed. "
        "Never replace a short URL in `data/shortlinks.yml` automatically "
        "(see the `source-links` skill).",
    ]
    for title, kinds in _SECTIONS:
        problems = sorted((p for p in result.problems if p.kind in kinds), key=lambda p: p.url)
        if not problems:
            continue
        lines += ["", f"## {title} ({len(problems)})", ""]
        for problem in problems:
            lines.append(f"- {problem.url}: {problem.summary}")
            lines += [f"  - `{_shown(path, base)}`" for path in problem.files]
            if problem.wayback:
                lines.append(f"  - Archived copies: {problem.wayback}")
    return "\n".join(lines) + "\n"
