"""The Quarto runner is a dependency: every build target reports its failures through
Diagnostics naming the document, and the post-render checks run against a fake."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from pathlib import Path

import pytest
from pypdf import PdfWriter

from fake_quarto import FakeQuarto
from nfl_book import pipeline
from nfl_book.cards import build_cards
from nfl_book.epub import build_epub
from nfl_book.errors import ValidationFailed
from nfl_book.project import Project
from nfl_book.publishing import EPUB_FILENAME
from nfl_book.website import build_website

Build = Callable[[Project, FakeQuarto], object]


def _pdf(project: Project, quarto: FakeQuarto) -> object:
    return pipeline.build(project, quarto=quarto)


def _booklet(project: Project, quarto: FakeQuarto) -> object:
    return pipeline.build(project, division="afc/east", quarto=quarto)


def _cards(project: Project, quarto: FakeQuarto) -> object:
    return build_cards(project, quarto=quarto)


def _website(project: Project, quarto: FakeQuarto) -> object:
    return build_website(project, quarto=quarto)


def _epub(project: Project, quarto: FakeQuarto) -> object:
    return build_epub(project, quarto=quarto)


# (build, the document the error must name, relative to the project's generated dir)
TARGETS: dict[str, tuple[Build, str]] = {
    "pdf": (_pdf, "book/book.qmd"),
    "booklet": (_booklet, "booklets/afc-east/book/book.qmd"),
    "cards": (_cards, "cards/cards.qmd"),
    "website": (_website, "site/_quarto.yml"),
    "epub": (_epub, "epub/book.qmd"),
}


@pytest.mark.parametrize("target", TARGETS)
def test_missing_quarto_is_a_diagnostic_naming_the_document(
    fixture_book: Project, target: str
) -> None:
    build, document = TARGETS[target]
    quarto = FakeQuarto(installed=False)
    with pytest.raises(ValidationFailed) as raised:
        build(fixture_book, quarto)
    [error] = raised.value.diagnostics.errors
    assert error.path == fixture_book.generated_dir / document
    assert "Quarto" in error.message and "PATH" in error.message
    assert len(quarto.calls) == 1


@pytest.mark.parametrize("target", TARGETS)
def test_failed_render_names_the_document_and_ends_with_the_log(
    fixture_book: Project, target: str
) -> None:
    build, document = TARGETS[target]
    log = "\n".join(f"noise {n}" for n in range(200)) + "\nERROR: the very last line"
    with pytest.raises(ValidationFailed) as raised:
        build(fixture_book, FakeQuarto(returncode=1, log=log))
    [error] = raised.value.diagnostics.errors
    assert error.path == fixture_book.generated_dir / document
    assert "the very last line" in error.message
    assert "noise 0\n" not in error.message  # only the end of the log


def _write_site(cwd: Path, args: Sequence[str]) -> None:
    site = cwd / "_site"
    site.mkdir()
    (site / "index.html").write_text('<html><a href="gone.html">x</a></html>')


def test_website_runs_its_site_check_after_a_fake_render(fixture_book: Project) -> None:
    quarto = FakeQuarto(writes=_write_site)
    with pytest.raises(ValidationFailed) as raised:
        build_website(fixture_book, quarto=quarto)
    assert quarto.calls == [(fixture_book.generated_dir / "site", ("render", "--to", "html"))]
    [error] = raised.value.diagnostics.errors
    assert error.code == "website-link"
    assert error.path == fixture_book.generated_dir / "site/_site/index.html"
    assert not (fixture_book.dist_dir / "site").exists()


def test_website_is_published_after_a_fake_render_that_passes(fixture_book: Project) -> None:
    def clean(cwd: Path, args: Sequence[str]) -> None:
        (cwd / "_site").mkdir()
        (cwd / "_site/index.html").write_text("<html></html>")

    result = build_website(fixture_book, quarto=FakeQuarto(writes=clean))
    assert result.site == fixture_book.dist_dir / "site"
    assert (result.site / "index.html").is_file()


def test_epub_post_processing_runs_after_a_fake_render(fixture_book: Project) -> None:
    def broken(cwd: Path, args: Sequence[str]) -> None:
        (cwd / "book.epub").write_bytes(b"not an epub")

    quarto = FakeQuarto(writes=broken)
    with pytest.raises(ValidationFailed) as raised:
        build_epub(fixture_book, quarto=quarto)
    assert quarto.calls == [
        (fixture_book.generated_dir / "epub", ("render", "book.qmd", "--to", "epub"))
    ]
    [error] = raised.value.diagnostics.errors
    assert error.code == "epub-package"
    assert error.path == fixture_book.generated_dir / "epub/book.epub"
    assert not (fixture_book.dist_dir / EPUB_FILENAME).exists()


def test_pdf_manifest_checks_run_after_a_fake_render(fixture_book: Project) -> None:
    def blank_pdf(cwd: Path, args: Sequence[str]) -> None:
        writer = PdfWriter()
        writer.add_blank_page(width=72, height=72)
        with (cwd / "book.pdf").open("wb") as handle:
            writer.write(handle)

    quarto = FakeQuarto(writes=blank_pdf)
    with pytest.raises(ValidationFailed) as raised:
        pipeline.build(fixture_book, quarto=quarto)
    assert quarto.calls == [
        (fixture_book.generated_dir / "book", ("render", "book.qmd", "--to", "pdf"))
    ]
    errors = raised.value.diagnostics.errors
    assert errors and {e.code for e in errors} == {"anchor"}
    assert all(e.path is not None and e.path.parent.name == "pages" for e in errors)
    assert not fixture_book.dist_dir.exists()


def test_render_that_writes_no_output_is_reported(fixture_book: Project) -> None:
    with pytest.raises(ValidationFailed) as raised:
        build_epub(fixture_book, quarto=FakeQuarto())
    [error] = raised.value.diagnostics.errors
    assert error.path == fixture_book.generated_dir / "epub/book.qmd"
    assert "book.epub" in error.message
