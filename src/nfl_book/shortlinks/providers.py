"""URL shortening providers. Only ``prepare-links`` ever calls these."""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol, runtime_checkable

import httpx

from nfl_book.errors import BookError


@runtime_checkable
class Shortener(Protocol):
    name: str

    def shorten(self, url: str) -> str:
        """Return a short URL that redirects to ``url``."""
        ...


class TinyUrlShortener:
    name = "tinyurl"
    endpoint = "https://tinyurl.com/api-create.php"

    def __init__(self, client: httpx.Client | None = None, timeout: float = 15.0) -> None:
        self._client = client or httpx.Client(timeout=timeout, follow_redirects=True)

    def shorten(self, url: str) -> str:
        try:
            response = self._client.get(self.endpoint, params={"url": url})
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise BookError(f"tinyurl: could not shorten {url}: {exc}") from exc
        short = response.text.strip()
        if not short.startswith("https://"):
            raise BookError(f"tinyurl: unexpected response for {url}: {short[:120]!r}")
        return short


PROVIDERS: dict[str, Callable[[], Shortener]] = {"tinyurl": TinyUrlShortener}


def get_shortener(name: str) -> Shortener:
    try:
        return PROVIDERS[name]()
    except KeyError:
        known = ", ".join(sorted(PROVIDERS))
        raise BookError(f"unknown shortlink provider {name!r} (known: {known})") from None
