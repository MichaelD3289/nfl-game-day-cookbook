"""Render synthetic content to an EPUB with the same Quarto compiler used by releases."""

import re
import shutil
from zipfile import ZipFile

import pytest

from nfl_book.epub import build_epub
from nfl_book.project import Project


@pytest.mark.skipif(shutil.which("quarto") is None, reason="Quarto not installed")
def test_fixture_epub_renders_with_valid_links_and_navigation(fixture_book: Project) -> None:
    result = build_epub(fixture_book)  # also runs the package, anchor and link checks
    assert result.epub and result.epub.is_file()
    with ZipFile(result.epub) as archive:
        names = archive.namelist()
        nav = archive.read(next(n for n in names if n.endswith("nav.xhtml"))).decode()
        opf = archive.read(next(n for n in names if n.endswith(".opf"))).decode()
    assert "recipe-test-citrus-wings" in nav
    entries = re.findall(r"<a [^>]*>([^<]+)</a>", nav)
    assert len(entries) == len(set(entries)), "repeated contents entries"
    assert "cover" in opf.lower()
    assert not any("qr-" in n for n in names)
