import re
from pathlib import Path
from zipfile import ZIP_STORED, ZipFile

import pytest
import yaml
from PIL import Image
from typer.testing import CliRunner

from nfl_book.cli import app
from nfl_book.epub_check import check_epub
from nfl_book.errors import Diagnostics, ValidationFailed
from nfl_book.project import Project
from nfl_book.publishing import EPUB_FILENAME, EPUB_IDENTIFIER, RELEASES

REPO_ROOT = Path(__file__).resolve().parents[2]


def _source(project: Project) -> tuple[dict[str, object], str]:
    from nfl_book.epub import build_epub

    text = build_epub(project, render=False).document.read_text()
    _, front, body = text.split("---\n", 2)
    return yaml.safe_load(front), body


def _headings(body: str, level: int) -> list[str]:
    return re.findall(rf"(?m)^{'#' * level} (.+)$", body)


def test_epub_sources_are_independent_and_published_only(fixture_book: Project) -> None:
    from nfl_book.epub import build_epub

    before = {p: p.read_bytes() for p in fixture_book.content_root.rglob("*.md")}
    site = fixture_book.generated_dir / "site"
    site.mkdir(parents=True)
    (site / "sentinel").write_text("keep")
    result = build_epub(fixture_book, render=False)
    text = result.document.read_text()
    assert "test-citrus-wings" in text
    assert "#component-test-wing-sauce" in text
    assert "Test AFC East Dish-Off" in text
    assert "test-draft-nachos" not in text
    assert "last_reviewed" not in text
    assert "{=latex}" not in text
    assert ".qmd" not in text
    assert (site / "sentinel").read_text() == "keep"
    assert all(p.read_bytes() == data for p, data in before.items())
    assert result.epub is None


def test_each_section_opens_once_and_components_stay_on_one_page(fixture_book: Project) -> None:
    # Three fast-day menus fill two print pages; the EPUB still opens the type once.
    folder = fixture_book.content_root / "menus/game-day/fast-day"
    original = (folder / "test-quick-kickoff.yml").read_text()
    for n in (2, 3):
        (folder / f"test-quick-kickoff-{n}.yml").write_text(
            original.replace("test-quick-kickoff", f"test-quick-kickoff-{n}").replace(
                "Test Quick Kickoff", f"Test Quick Kickoff {n}"
            )
        )
    _, body = _source(fixture_book)
    top = _headings(body, 1)
    assert len(top) == len(set(top)), top
    # Menu types nest under Game Day Menus, and their menus under them.
    assert _headings(body, 2).count("Fast Day") == 1
    fast_day = body.index("## Fast Day")
    assert fast_day < body.index("### Test Quick Kickoff {#menu-test-quick-kickoff}")
    assert "## Test AFC East Dish-Off" in body
    # Sections inside a recipe or component are below the level the EPUB splits files at.
    for section in ("Ingredients", "Instructions", "Method", "Buy it", "Kitchen notes", "Used in"):
        assert not re.search(rf"(?m)^#{{1,3}} {section}\b", body), section
    assert re.search(r"(?m)^#### Method$", body)
    # Components follow their kind's heading, not the last kind listed.
    sauces = body.index("## Sauces {#kind-sauces}")
    dips = body.index("## Dips {#kind-dips}")
    assert sauces < body.index("{#component-test-wing-sauce}") < dips
    assert dips < body.index("{#component-test-blue-cheese-dip}")
    # The contents page and indexes read as one page each: no headings below their title.
    contents = body[body.index("# All recipes") : body.index("\n# ", body.index("# All recipes"))]
    assert not re.search(r"(?m)^#{2,} ", contents)
    # Each label comes right after its heading, so none is left at the bottom of the
    # previous page.
    lines = [line for line in body.splitlines() if line.strip()]
    for n, line in enumerate(lines):
        if line.endswith("{.eyebrow}"):
            assert lines[n - 1].startswith("#"), line


def test_indexes_come_after_the_recipes_and_components(fixture_book: Project) -> None:
    _, body = _source(fixture_book)
    make_buy = body.index("# Make It or Buy It")
    last_component = body.rindex("{#component-")
    first_index = body.index("{#index-")
    assert make_buy < last_component < first_index
    assert body.index("# All recipes") < body.index("{#recipe-")


def test_recipe_page_content(fixture_book: Project) -> None:
    recipe = next(fixture_book.recipes_dir.rglob("test-citrus-wings.md"))
    recipe.write_text(
        recipe.read_text().replace(
            "status: published",
            'status: published\ndescription: "Bright, sticky wings."\n'
            "image: fixture.png\nphoto_credit: Synthetic fixture",
        )
    )
    Image.new("RGB", (600, 600), "orange").save(recipe.parent / "fixture.png")
    _, body = _source(fixture_book)
    wings = body[body.index("{#recipe-test-citrus-wings}") :]
    wings = wings[: wings.index("\n### ")] if "\n### " in wings else wings
    assert "[Bright, sticky wings.]{.headnote}" in wings
    # The photo keeps its alt text but is not a captioned figure repeating the title.
    assert re.search(r"!\[Photo of Test Citrus Wings\]\([^)]+\)\{\.dish-photo\}&nbsp;", wings)
    # Yield, prep and cook are separate lines, not "|"-separated.
    assert "   |   " not in wings
    # Q goes to this recipe's Quick options card, which exists, with a readable label.
    assert "[Q](#recipe-test-citrus-wings-quick)" in wings
    assert 'aria-label="Quick option: see the store-bought suggestion"' in wings
    assert "Quick options {#recipe-test-citrus-wings-quick}" in wings
    # The source is the full URL, not the print short link.
    assert "(https://example.com/recipes/test-citrus-wings)" in wings
    assert "example.org/s/wings" not in wings
    # The page links to this edition of the website instead of carrying a QR code.
    assert "[View this page online](" in wings
    assert "/recipe-test-citrus-wings.html)" in wings
    assert not list((fixture_book.generated_dir / "epub/assets").glob("qr-*"))


def test_book_details_are_stable_and_complete(fixture_book: Project) -> None:
    front, body = _source(fixture_book)
    assert front["identifier"] == EPUB_IDENTIFIER
    assert "urn:uuid:" in EPUB_IDENTIFIER
    assert front["author"] == "Michael Drummond"
    assert front["description"]
    assert "CC BY 4.0" in str(front["rights"])
    cover = fixture_book.generated_dir / "epub" / str(front["cover-image"])
    with Image.open(cover) as image:
        assert image.size == (1600, 2560)
    # The cover page explains the edition-specific website links once.
    welcome = body[: body.index("\n# ", 1)]
    assert "this edition" in welcome and "of the website at" in welcome


def test_missing_quarto_preserves_existing_epub(
    fixture_book: Project, monkeypatch: pytest.MonkeyPatch
) -> None:
    from nfl_book.epub import build_epub

    fixture_book.dist_dir.mkdir(parents=True)
    target = fixture_book.dist_dir / EPUB_FILENAME
    target.write_bytes(b"previous")
    monkeypatch.setattr("nfl_book.epub.shutil.which", lambda _: None)
    with pytest.raises(ValidationFailed):
        build_epub(fixture_book)
    assert target.read_bytes() == b"previous"


def test_epub_cli(fixture_book: Project) -> None:
    result = CliRunner().invoke(
        app,
        [
            "--root",
            str(fixture_book.root),
            "--content",
            str(fixture_book.content_root),
            "--generated",
            str(fixture_book.generated_dir),
            "epub",
            "--no-render",
        ],
    )
    assert result.exit_code == 0, result.output


def test_release_workflow_and_website_use_the_one_epub_name(fixture_book: Project) -> None:
    from nfl_book.website import build_website

    workflow = (REPO_ROOT / ".github/workflows/release.yml").read_text()
    assert f"EPUB: dist/{EPUB_FILENAME}\n" in workflow
    site = build_website(fixture_book, render=False).document.parent
    navbar = yaml.safe_load((site / "_quarto.yml").read_text())["website"]["navbar"]["right"]
    links = {item["text"]: item["href"] for item in navbar}
    assert links["Download EPUB"].startswith(f"{RELEASES}/download/v")
    assert links["Download EPUB"].endswith(f"/{EPUB_FILENAME}")


def _package(path: Path, body: str, *, stored: bool = True) -> None:
    with ZipFile(path, "w") as archive:
        archive.writestr("mimetype", "application/epub+zip", compress_type=ZIP_STORED)
        archive.writestr(
            "META-INF/container.xml",
            '<container><rootfiles><rootfile full-path="EPUB/book.opf"/></rootfiles></container>',
        )
        archive.writestr(
            "EPUB/book.opf",
            '<package><manifest><item id="nav" properties="nav" href="nav.xhtml"/>'
            '<item id="photo" href="photo.jpg"/></manifest>'
            '<spine><itemref idref="nav"/></spine></package>',
        )
        archive.writestr("EPUB/photo.jpg", b"jpg")
        archive.writestr("EPUB/nav.xhtml", f"<html><body>{body}</body></html>")


def test_package_check_accepts_a_valid_package(tmp_path: Path) -> None:
    path = tmp_path / "ok.epub"
    _package(
        path,
        '<p id="recipe-x">Recipe</p><a href="#recipe-x">x</a><img src="photo.jpg"/>'
        '<a href="https://example.com/source">source</a>',
    )
    diags = Diagnostics()
    check_epub(path, diags, {"recipe-x"})
    assert diags.ok, [d.message for d in diags.errors]


@pytest.mark.parametrize(
    "target,expected",
    [
        ("#missing", "missing link target"),
        ("absent.jpg", "missing resource"),
        ("https://example.com/photo.jpg", "Non-embedded resource"),
    ],
)
def test_package_rejects_broken_or_remote_resources(
    tmp_path: Path, target: str, expected: str
) -> None:
    path = tmp_path / "test.epub"
    _package(path, f'<img src="{target}"/>')
    diags = Diagnostics()
    check_epub(path, diags)
    assert not diags.ok
    assert expected in diags.errors[0].message
    assert diags.errors[0].path == path


def test_package_check_reports_missing_anchors(tmp_path: Path) -> None:
    path = tmp_path / "test.epub"
    _package(path, '<p id="recipe-x">Recipe</p>')
    diags = Diagnostics()
    check_epub(path, diags, {"recipe-x", "recipe-y"})
    assert "recipe-y" in diags.errors[0].message


def test_make_buy_lists_component_descriptions(fixture_book: Project) -> None:
    path = fixture_book.content_root / "components/sauces/test-wing-sauce.md"
    path.write_text(
        path.read_text().replace(
            "status: published", "status: published\ndescription: Hot and tangy.", 1
        )
    )
    _, body = _source(fixture_book)
    assert "[Test Wing Sauce](#component-test-wing-sauce) · Hot and tangy." in body
