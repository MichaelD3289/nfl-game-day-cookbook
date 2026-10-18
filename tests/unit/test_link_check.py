"""``prepare-links --check``: dead and moved source URLs, with no real network.

Every :class:`LinkChecker` here gets an ``httpx.MockTransport`` client and a fake
clock, so nothing leaves the machine and nothing really sleeps.
"""

from __future__ import annotations

import socket
from collections.abc import Callable
from pathlib import Path

import httpx
import pytest

from nfl_book import pipeline
from nfl_book.errors import Severity, ValidationFailed
from nfl_book.project import Project
from nfl_book.shortlinks.check import (
    USER_AGENT,
    CheckResult,
    LinkChecker,
    LinkProblem,
    ProblemKind,
    check_sources,
    render_report,
)
from nfl_book.shortlinks.prepare import sources_to_check, urls_to_prepare

U1 = "https://example.com/components/test-blue-cheese-dip"
U2 = "https://example.com/recipes/test-buffalo-sliders?ref=fixture&x=1"
U3 = "https://example.com/recipes/test-citrus-wings"
SLIDERS = "recipes/afc/east/bills/test-buffalo-sliders.md"
WINGS = "recipes/afc/east/dolphins/test-citrus-wings.md"
DIP = "components/dips/test-blue-cheese-dip.md"
NACHOS = "recipes/afc/east/jets/test-draft-nachos.md"

Handler = Callable[[httpx.Request], httpx.Response]


class FakeTime:
    def __init__(self) -> None:
        self.now = 0.0
        self.sleeps: list[float] = []

    def clock(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.now += seconds


class Recorder:
    """A MockTransport handler that records every request it answers."""

    def __init__(self, handler: Handler) -> None:
        self.handler = handler
        self.requests: list[httpx.Request] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        return self.handler(request)

    def calls(self, method: str | None = None) -> list[str]:
        return [str(r.url) for r in self.requests if method is None or r.method == method]


def make_checker(
    handler: Handler, *, retries: int = 2, per_host_delay: float = 1.0
) -> tuple[LinkChecker, Recorder, FakeTime]:
    recorder = Recorder(handler)
    fake = FakeTime()
    client = httpx.Client(transport=httpx.MockTransport(recorder))
    checker = LinkChecker(
        client,
        retries=retries,
        per_host_delay=per_host_delay,
        sleep=fake.sleep,
        clock=fake.clock,
    )
    return checker, recorder, fake


def ok(_: httpx.Request) -> httpx.Response:
    return httpx.Response(200)


def edit(project: Project, relative: str, old: str, new: str) -> None:
    path = project.content_root / relative
    text = path.read_text(encoding="utf-8")
    assert old in text
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


# --- which URLs --------------------------------------------------------------


def test_sources_cover_every_non_retired_source(fixture_book: Project) -> None:
    content = pipeline.load(fixture_book, require_shortlinks=False).content
    sources = sources_to_check(content)
    assert set(sources) == {U1, U2, U3}
    assert sources[U2] == (fixture_book.content_root / SLIDERS,)
    assert urls_to_prepare(content) == list(sources)


def test_sources_dedupe_include_drafts_and_skip_retired(fixture_book: Project) -> None:
    # the draft nachos cite the wings page too; the sliders are retired
    edit(fixture_book, NACHOS, "yield: 1 tray\n", f"yield: 1 tray\nsource:\n  url: {U3}\n")
    edit(fixture_book, SLIDERS, "status: published", "status: retired")
    content = pipeline.load(fixture_book, require_shortlinks=False).content
    sources = sources_to_check(content)
    assert set(sources) == {U1, U3}
    root = fixture_book.content_root
    assert sources[U3] == tuple(sorted([root / NACHOS, root / WINGS]))
    assert urls_to_prepare(content) == list(sources)


# --- probing -----------------------------------------------------------------


def test_all_ok_uses_head_only(fixture_book: Project) -> None:
    checker, recorder, _ = make_checker(ok)
    content = pipeline.load(fixture_book, require_shortlinks=False).content
    with checker:
        result = check_sources(content, checker)
    assert result.ok and result.checked == 3
    assert result.problems == [] and len(result.diagnostics) == 0
    assert [r.method for r in recorder.requests] == ["HEAD"] * 3


@pytest.mark.parametrize("head_status", [405, 404])
def test_head_failure_falls_back_to_get(head_status: int) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(head_status if request.method == "HEAD" else 200)

    checker, recorder, _ = make_checker(handler)
    assert checker.check(U3).ok
    assert [r.method for r in recorder.requests] == ["HEAD", "GET"]


def test_404_is_broken_and_names_the_file(fixture_book: Project) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404 if str(request.url) == U3 else 200)

    checker, recorder, _ = make_checker(handler)
    content = pipeline.load(fixture_book, require_shortlinks=False).content
    result = check_sources(content, checker)
    assert not result.ok
    [problem] = result.problems
    assert problem.kind is ProblemKind.BROKEN
    assert problem.status == 404 and problem.detail == "HTTP 404"
    assert problem.files == (fixture_book.content_root / WINGS,)
    assert problem.wayback == f"https://web.archive.org/web/*/{U3}"
    [diag] = list(result.diagnostics)
    assert diag.code == "link-broken" and diag.severity is Severity.ERROR
    assert diag.path == fixture_book.content_root / WINGS
    assert U3 in diag.message
    assert recorder.calls("GET") == [U3]  # a 404 is not retried


def test_503_is_retried_then_broken() -> None:
    checker, recorder, fake = make_checker(lambda _: httpx.Response(503), per_host_delay=0)
    outcome = checker.check(U3)
    assert outcome.kind is ProblemKind.BROKEN and outcome.detail == "HTTP 503"
    assert len(recorder.calls("GET")) == 3
    assert fake.sleeps == [2.0, 4.0]


def test_transient_timeout_recovers() -> None:
    attempts: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        attempts.append(request.method)
        if len(attempts) <= 2:  # the HEAD and the first GET
            raise httpx.ReadTimeout("timed out", request=request)
        return httpx.Response(200)

    checker, _, fake = make_checker(handler, per_host_delay=0)
    assert checker.check(U3).ok
    assert attempts == ["HEAD", "GET", "GET"]
    assert fake.sleeps == [2.0]


def test_dns_failure() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("[Errno -2] lookup failed", request=request) from (
            socket.gaierror(-2, "Name or service not known")
        )

    checker, _, _ = make_checker(handler)
    outcome = checker.check(U3)
    assert outcome.kind is ProblemKind.DNS
    assert "example.com" in outcome.detail


def test_timeout_is_unreachable() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectTimeout("connect timeout", request=request)

    checker, recorder, _ = make_checker(handler)
    outcome = checker.check(U3)
    assert outcome.kind is ProblemKind.UNREACHABLE
    assert "timed out" in outcome.detail
    assert len(recorder.calls("GET")) == 3


# --- redirects ---------------------------------------------------------------

NEW = "https://example.com/recipes/citrus-wings"


@pytest.mark.parametrize(
    "chain",
    [
        {U3: (301, NEW)},
        {U3: (308, "/recipes/citrus-wings")},
        {U3: (301, "https://example.com/step"), "https://example.com/step": (301, NEW)},
    ],
    ids=["301", "308-relative", "301-301"],
)
def test_permanent_redirect_is_moved(chain: dict[str, tuple[int, str]]) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if str(request.url) in chain:
            status, location = chain[str(request.url)]
            return httpx.Response(status, headers={"Location": location})
        return httpx.Response(200)

    checker, _, _ = make_checker(handler)
    outcome = checker.check(U3)
    assert outcome.kind is ProblemKind.MOVED
    assert outcome.location == NEW
    assert outcome.status == chain[U3][0]


@pytest.mark.parametrize("status", [302, 303, 307])
def test_temporary_redirects_are_followed_silently(status: int) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if str(request.url) == U3:
            return httpx.Response(status, headers={"Location": NEW})
        return httpx.Response(200)

    checker, recorder, _ = make_checker(handler)
    assert checker.check(U3).ok
    assert recorder.calls() == [U3, NEW]


def test_redirect_to_dead_page_is_broken_with_location() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if str(request.url) == U3:
            return httpx.Response(301, headers={"Location": NEW})
        return httpx.Response(404)

    checker, _, _ = make_checker(handler)
    outcome = checker.check(U3)
    assert outcome.kind is ProblemKind.BROKEN
    assert outcome.detail == "HTTP 404" and outcome.location == NEW


def test_redirect_without_location_is_broken() -> None:
    checker, _, _ = make_checker(lambda _: httpx.Response(301))
    outcome = checker.check(U3)
    assert outcome.kind is ProblemKind.BROKEN
    assert "Location" in outcome.detail


def test_redirect_loop_is_unreachable() -> None:
    checker, _, _ = make_checker(lambda _: httpx.Response(302, headers={"Location": U3}))
    outcome = checker.check(U3)
    assert outcome.kind is ProblemKind.UNREACHABLE
    assert outcome.detail == "too many redirects"


# --- refusals ----------------------------------------------------------------


def test_429_honours_retry_after_then_blocked() -> None:
    checker, recorder, fake = make_checker(
        lambda _: httpx.Response(429, headers={"Retry-After": "7"})
    )
    outcome = checker.check(U3)
    assert outcome.kind is ProblemKind.BLOCKED and outcome.status == 429
    assert len(recorder.calls("GET")) == 3
    assert fake.sleeps.count(7.0) == 2
    assert 2.0 not in fake.sleeps and 4.0 not in fake.sleeps


def test_retry_after_is_capped() -> None:
    checker, _, fake = make_checker(
        lambda _: httpx.Response(429, headers={"Retry-After": "3600"}), retries=1
    )
    checker.check(U3)
    assert max(fake.sleeps) == 60.0


def test_403_is_blocked_without_retry() -> None:
    checker, recorder, _ = make_checker(lambda _: httpx.Response(403))
    outcome = checker.check(U3)
    assert outcome.kind is ProblemKind.BLOCKED and outcome.detail == "HTTP 403"
    assert len(recorder.calls("GET")) == 1


# --- politeness and headers ---------------------------------------------------


def test_per_host_delay(fixture_book: Project) -> None:
    content = pipeline.load(fixture_book, require_shortlinks=False).content
    checker, _, fake = make_checker(ok)
    check_sources(content, checker)
    assert fake.sleeps == [1.0, 1.0]

    edit(fixture_book, SLIDERS, "https://example.com/", "https://example.net/")
    content = pipeline.load(fixture_book, require_shortlinks=False).content
    checker, _, fake = make_checker(ok)
    check_sources(content, checker)
    assert fake.sleeps == [1.0]


def test_redirect_hops_count_for_politeness() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if str(request.url) == U3:
            return httpx.Response(302, headers={"Location": NEW})
        return httpx.Response(200)

    checker, _, fake = make_checker(handler)
    assert checker.check(U3).ok
    assert fake.sleeps == [1.0]


def test_sends_user_agent_and_never_auto_follows() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if str(request.url) == U3:
            return httpx.Response(302, headers={"Location": NEW})
        return httpx.Response(200)

    recorder = Recorder(handler)
    fake = FakeTime()
    client = httpx.Client(transport=httpx.MockTransport(recorder), follow_redirects=True)
    with LinkChecker(client, sleep=fake.sleep, clock=fake.clock) as checker:
        assert checker.check(U3).ok
    assert [r.method for r in recorder.requests] == ["HEAD", "HEAD"]
    for request in recorder.requests:
        assert request.headers["User-Agent"] == USER_AGENT
        assert request.headers["Accept"] == "text/html,*/*;q=0.8"
    assert USER_AGENT.startswith("nfl-game-day-cookbook/")
    assert "link check" in USER_AGENT


# --- report ------------------------------------------------------------------


def test_report_text(fixture_book: Project) -> None:
    root = fixture_book.content_root

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        if url == U3:
            return httpx.Response(404)
        if url == U2:
            return httpx.Response(
                301, headers={"Location": "https://example.com/recipes/buffalo-sliders"}
            )
        return httpx.Response(200)

    content = pipeline.load(fixture_book, require_shortlinks=False).content
    checker, _, _ = make_checker(handler)
    result = check_sources(content, checker)
    assert {d.code: d.severity for d in result.diagnostics} == {
        "link-broken": Severity.ERROR,
        "link-moved": Severity.WARNING,
    }
    assert render_report(result, root) == (
        "# Source link check\n"
        "\n"
        "Checked 3 source URLs from recipes and components that are not retired. "
        "2 need attention.\n"
        "\n"
        "This report changes nothing. Fix `source.url` by hand in the files listed. "
        "Never replace a short URL in `data/shortlinks.yml` automatically "
        "(see the `source-links` skill).\n"
        "\n"
        "## Dead (1)\n"
        "\n"
        "- https://example.com/recipes/test-citrus-wings: HTTP 404\n"
        "  - `recipes/afc/east/dolphins/test-citrus-wings.md`\n"
        "  - Archived copies: "
        "https://web.archive.org/web/*/https://example.com/recipes/test-citrus-wings\n"
        "\n"
        "## Moved permanently (1)\n"
        "\n"
        "- https://example.com/recipes/test-buffalo-sliders?ref=fixture&x=1: "
        "HTTP 301 to https://example.com/recipes/buffalo-sliders\n"
        "  - `recipes/afc/east/bills/test-buffalo-sliders.md`\n"
    )


def test_report_sections_order_and_blocked(tmp_path: Path) -> None:
    files = (tmp_path / "a.md",)
    result = CheckResult(
        checked=4,
        problems=[
            LinkProblem("https://b.example/", ProblemKind.BLOCKED, "HTTP 403", files, 403),
            LinkProblem("https://z.example/", ProblemKind.DNS, "DNS lookup failed", files),
            LinkProblem("https://a.example/", ProblemKind.UNREACHABLE, "timed out", files),
        ],
    )
    text = render_report(result, tmp_path)
    assert text.index("## Dead (2)") < text.index("## Could not verify (1)")
    assert "## Moved" not in text
    assert text.index("https://a.example/") < text.index("https://z.example/")
    assert "https://web.archive.org/web/*/https://b.example/" not in text
    assert LinkProblem("u", ProblemKind.MOVED, "HTTP 301", files).wayback is None


def test_all_ok_report(fixture_book: Project) -> None:
    content = pipeline.load(fixture_book, require_shortlinks=False).content
    checker, _, _ = make_checker(ok)
    result = check_sources(content, checker)
    assert render_report(result, fixture_book.content_root) == (
        "# Source link check\n\n"
        "All 3 source URLs from recipes and components that are not retired responded OK.\n"
    )


# --- pipeline ----------------------------------------------------------------


def test_check_links_changes_nothing(fixture_book: Project) -> None:
    shortlinks = fixture_book.shortlinks_file.read_bytes()
    sources = {p: p.read_bytes() for p in fixture_book.content_root.rglob("*.md")}
    checker, recorder, _ = make_checker(lambda _: httpx.Response(404))
    result = pipeline.check_links(fixture_book, checker)
    assert result.checked == 3 and len(result.problems) == 3
    assert recorder.requests
    assert fixture_book.shortlinks_file.read_bytes() == shortlinks
    assert {p: p.read_bytes() for p in sources} == sources
    assert not fixture_book.qr_dir.exists()


def test_check_links_refuses_invalid_content(fixture_book: Project) -> None:
    edit(fixture_book, SLIDERS, "course: appetizers", "course: brunch")
    checker, recorder, _ = make_checker(ok)
    with pytest.raises(ValidationFailed):
        pipeline.check_links(fixture_book, checker)
    assert recorder.requests == []
