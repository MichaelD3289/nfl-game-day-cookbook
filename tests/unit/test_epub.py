import shutil
from pathlib import Path

import pytest
from typer.testing import CliRunner

from nfl_book.cli import app
from nfl_book.errors import ValidationFailed
from nfl_book.project import Project


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


def test_missing_quarto_preserves_existing_epub(
    fixture_book: Project, monkeypatch: pytest.MonkeyPatch
) -> None:
    from nfl_book.epub import build_epub

    fixture_book.dist_dir.mkdir(parents=True)
    target = fixture_book.dist_dir / "nfl-game-day-cookbook.epub"
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


@pytest.mark.skipif(shutil.which("quarto") is None, reason="Quarto not installed")
def test_fixture_epub_renders_with_valid_links(fixture_book: Project) -> None:
    from nfl_book.epub import build_epub

    result = build_epub(fixture_book)
    assert result.epub and result.epub.is_file()
    from zipfile import ZipFile

    with ZipFile(result.epub) as archive:
        nav = archive.read("EPUB/nav.xhtml").decode()
    assert "recipe-test-citrus-wings" in nav


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
    from zipfile import ZipFile

    from nfl_book.epub_check import check_epub
    from nfl_book.errors import Diagnostics

    path = tmp_path / "test.epub"
    with ZipFile(path, "w") as archive:
        archive.writestr("mimetype", "application/epub+zip")
        archive.writestr(
            "META-INF/container.xml",
            '<container><rootfiles><rootfile full-path="book.opf"/></rootfiles></container>',
        )
        archive.writestr(
            "book.opf",
            '<package><manifest><item id="nav" properties="nav" href="nav.xhtml"/></manifest>'
            '<spine><itemref idref="nav"/></spine></package>',
        )
        archive.writestr("nav.xhtml", f'<html><body><img src="{target}"/></body></html>')
    diags = Diagnostics()
    check_epub(path, diags)
    assert not diags.ok
    assert expected in diags.errors[0].message
    assert diags.errors[0].path == path
