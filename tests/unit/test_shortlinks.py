from __future__ import annotations

from pathlib import Path

import pytest

from nfl_book.errors import BookError, ValidationFailed
from nfl_book.pipeline import load, prepare_links
from nfl_book.project import Project
from nfl_book.shortlinks import ShortlinkCache
from nfl_book.shortlinks.providers import Shortener


class FakeShortener:
    name = "fake"

    def __init__(self) -> None:
        self.calls: list[str] = []

    def shorten(self, url: str) -> str:
        self.calls.append(url)
        return f"https://sho.rt/{len(self.calls)}"


def test_fake_satisfies_protocol() -> None:
    assert isinstance(FakeShortener(), Shortener)


def test_cache_round_trip_is_deterministic(tmp_path: Path) -> None:
    cache = ShortlinkCache(tmp_path / "shortlinks.yml")
    cache.add("https://b.example/x", "https://s/2")
    cache.add("https://a.example/y?q=1&r=2", "https://s/1")
    assert cache.save() is True
    assert cache.save() is False
    text = cache.path.read_text()
    assert text.index("a.example") < text.index("b.example")
    assert ShortlinkCache.load(cache.path).links == cache.links


def test_cache_never_replaces_an_entry(tmp_path: Path) -> None:
    cache = ShortlinkCache(tmp_path / "s.yml", {"https://a.example/": "https://s/1"})
    cache.add("https://a.example/", "https://s/1")  # idempotent
    with pytest.raises(BookError, match="refusing to replace"):
        cache.add("https://a.example/", "https://s/2")
    assert cache.get("https://a.example/") == "https://s/1"


def test_cache_rejects_bad_file(tmp_path: Path) -> None:
    path = tmp_path / "s.yml"
    path.write_text("links:\n  https://a.example/: 42\n")
    with pytest.raises(BookError, match=str(path)):
        ShortlinkCache.load(path)


def test_missing_cache_file_is_empty(tmp_path: Path) -> None:
    assert ShortlinkCache.load(tmp_path / "nope.yml").links == {}


def test_prepare_only_shortens_new_urls(fixture_book: Project) -> None:
    before = fixture_book.shortlinks_file.read_text()
    fake = FakeShortener()
    result = prepare_links(fixture_book, fake)
    assert fake.calls == []
    assert result.added == {} and result.cached == 3
    assert fixture_book.shortlinks_file.read_text() == before


def test_prepare_fills_cache_and_keeps_full_urls(fixture_book: Project) -> None:
    fixture_book.shortlinks_file.unlink()
    sliders = fixture_book.content_root / "recipes/afc/east/bills/test-buffalo-sliders.md"
    source_before = sliders.read_text()
    fake = FakeShortener()
    result = prepare_links(fixture_book, fake)
    # drafts are prepared too, so they are ready when published; fixtures have 3 sources
    assert len(fake.calls) == 3
    assert result.changed
    assert sliders.read_text() == source_before  # canonical full URL untouched
    links = ShortlinkCache.load(fixture_book.shortlinks_file).links
    assert "https://example.com/recipes/test-buffalo-sliders?ref=fixture&x=1" in links
    assert load(fixture_book).diagnostics.ok
    assert sorted(p.name for p in fixture_book.qr_dir.iterdir()) == [
        "component-test-blue-cheese-dip.png",
        "recipe-test-buffalo-sliders.png",
        "recipe-test-citrus-wings.png",
    ]


def test_prepare_refuses_invalid_content(fixture_book: Project) -> None:
    sliders = fixture_book.content_root / "recipes/afc/east/bills/test-buffalo-sliders.md"
    sliders.write_text(sliders.read_text().replace("course: appetizers", "course: brunch"))
    fake = FakeShortener()
    with pytest.raises(ValidationFailed):
        prepare_links(fixture_book, fake)
    assert fake.calls == []
