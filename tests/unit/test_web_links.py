import re
from dataclasses import replace
from pathlib import Path

import pytest
from pydantic import ValidationError

from nfl_book import __version__
from nfl_book.errors import Diagnostics
from nfl_book.models.config import BookConfig
from nfl_book.models.content import Component, Recipe
from nfl_book.pipeline import build, build_media, load
from nfl_book.project import Project
from nfl_book.qr import qr_png
from nfl_book.render.pages import PageSpec, WebView, build_pages, check_web_links
from nfl_book.resolve import BookModel, resolve
from nfl_book.validation import is_published

BASE = "https://michaeld3289.github.io/nfl-game-day-cookbook"
EDITION = f"{BASE}/v{__version__}"


def _unset_website_url(project: Project) -> None:
    book = project.content_root / "data/book.yml"
    book.write_text(re.sub(r"(?m)^website_url:.*$", "", book.read_text()))


def _pages(project: Project) -> tuple[BookModel, list[PageSpec]]:
    loaded = load(project)
    model = resolve(loaded.settings, loaded.content, loaded.shortlinks.links)
    media, _ = build_media(
        project, model, project.book_build_dir, Diagnostics(), loaded.settings.book.photos.print
    )
    return model, build_pages(model, media)


def _web(pages: list[PageSpec]) -> dict[str, WebView]:
    return {p.slug: p.context["web"] for p in pages if p.context.get("web") is not None}


def test_published_pages_link_to_their_website_page(fixture_book: Project) -> None:
    _, pages = _pages(fixture_book)
    web = _web(pages)
    wings = web["recipe-test-citrus-wings"]
    assert wings.href == f"{EDITION}/recipe-test-citrus-wings.html"
    assert wings.edition == __version__
    assert web["component-test-wing-sauce"].href == f"{EDITION}/component-test-wing-sauce.html"


def test_link_targets_are_published_website_pages(fixture_book: Project) -> None:
    model, pages = _pages(fixture_book)
    slugs = {p.slug for p in pages}
    items: dict[str, Recipe | Component] = {
        f"recipe-{r.id}": r for r in model.recipes_by_id.values()
    }
    items.update({f"component-{c.id}": c for c in model.components_by_id.values()})
    web = _web(pages)
    assert web
    for view in web.values():
        assert view.target in slugs
        assert is_published(items[view.target].meta.status)
    assert not any("draft" in target for target in web)


def test_draft_previews_are_never_linked(fixture_book: Project) -> None:
    from nfl_book.preview import preview

    drafts = [*fixture_book.content_root.rglob("test-draft-*.md")]
    assert len(drafts) == 2
    for path in drafts:
        document = preview(fixture_book, path, pdf=False).document.read_text()
        assert "github.io" not in document


def test_missing_link_target_names_the_source_file(fixture_book: Project) -> None:
    model, pages = _pages(fixture_book)
    orphan = [p for p in pages if p.slug != "component-test-wing-sauce"]
    diags = Diagnostics()
    check_web_links(model, orphan, diags)
    assert [d.code for d in diags] == []  # the component page itself is gone with its link
    broken = replace(
        next(p for p in pages if p.slug == "recipe-test-citrus-wings"),
        context={
            **next(p for p in pages if p.slug == "recipe-test-citrus-wings").context,
            "web": WebView("recipe-test-missing", f"{BASE}/x.html", __version__),
        },
    )
    check_web_links(model, [*orphan, broken], diags)
    [error] = list(diags)
    assert error.code == "web-link"
    assert error.path == model.recipes_by_id["test-citrus-wings"].path


def test_no_links_without_website_url(fixture_book: Project) -> None:
    _unset_website_url(fixture_book)
    _, pages = _pages(fixture_book)
    assert not _web(pages)
    assert all(p.context.get("website") is None for p in pages)


def _qr(project: Project, name: str) -> bytes:
    return (project.qr_dir / f"{name}.png").read_bytes()


def test_qr_codes_open_the_edition_page(fixture_book: Project) -> None:
    _, pages = _pages(fixture_book)
    assert _qr(fixture_book, "recipe-test-citrus-wings") == qr_png(
        f"{EDITION}/recipe-test-citrus-wings.html"
    )
    # Items without a source still get a QR code for their website page.
    wing_sauce = next(p for p in pages if p.slug == "component-test-wing-sauce")
    assert wing_sauce.context["qr"]
    assert _qr(fixture_book, "component-test-wing-sauce") == qr_png(
        f"{EDITION}/component-test-wing-sauce.html"
    )


def test_qr_codes_fall_back_to_the_source_without_website_url(fixture_book: Project) -> None:
    _unset_website_url(fixture_book)
    _, pages = _pages(fixture_book)
    assert _qr(fixture_book, "recipe-test-citrus-wings") == qr_png(
        "https://example.com/recipes/test-citrus-wings"
    )
    wing_sauce = next(p for p in pages if p.slug == "component-test-wing-sauce")
    assert wing_sauce.context["qr"] == ""


def test_drafts_get_no_website_qr_code(fixture_book: Project) -> None:
    loaded = load(fixture_book)
    model = resolve(loaded.settings, loaded.content, loaded.shortlinks.links)
    media, _ = build_media(
        fixture_book,
        model,
        fixture_book.book_build_dir,
        Diagnostics(),
        loaded.settings.book.photos.print,
    )
    assert "recipe:test-draft-nachos" not in media.qr
    assert "component:test-draft-side" not in media.qr


def test_website_url_must_be_https() -> None:
    with pytest.raises(ValidationError):
        BookConfig.model_validate({"title": "T", "website_url": "http://example.com/"})


def test_book_prints_links_and_edition_note(fixture_book: Project) -> None:
    document: Path = build(fixture_book, pdf=False).document
    text = "".join(p.read_text() for p in document.parent.rglob("*.qmd"))
    assert f"{{{EDITION}/recipe-test-citrus-wings.html}}" in text
    assert f"{{{EDITION}/component-test-wing-sauce.html}}" in text
    assert f"\\CoverOnline{{{EDITION}/}}" in text
    assert f"{{{__version__}}}" in text
    # The page link is a short label in the PDF, so its long URL is never printed.
    assert "{" + EDITION.removeprefix("https://") + "/recipe-" not in text
    assert "test-draft-nachos.html" not in text
