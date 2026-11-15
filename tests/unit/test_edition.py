"""One entry point builds the edition every target renders from."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

import pytest
from PIL import Image

from fake_quarto import FakeQuarto
from nfl_book import pipeline
from nfl_book.edition import Edition, published_edition
from nfl_book.epub import build_epub
from nfl_book.errors import ValidationFailed
from nfl_book.models.common import Status
from nfl_book.project import Project
from nfl_book.website import build_website

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC = REPO_ROOT / "src" / "nfl_book"


def test_edition_holds_the_published_book_and_its_media(
    fixture_book: Project, tmp_path: Path
) -> None:
    edition = published_edition(fixture_book, tmp_path / "build")
    assert isinstance(edition, Edition)
    assert edition.diagnostics.ok
    assert edition.settings.book.title
    assert edition.version == fixture_book.version
    ids = {r.id for r in edition.model.recipes}
    assert "test-buffalo-sliders" in ids
    assert not any("draft" in i or "retired" in i for i in ids)
    assert "recipe:test-buffalo-sliders" in edition.media.qr


def test_edition_can_admit_drafts(fixture_book: Project, tmp_path: Path) -> None:
    edition = published_edition(
        fixture_book,
        tmp_path / "build",
        include=lambda status: status is not Status.RETIRED,
    )
    ids = {r.id for r in edition.model.recipes}
    assert "test-draft-nachos" in ids
    assert "test-retired-nachos" not in ids


def test_edition_for_a_division_keeps_media_under_the_root_generated(
    fixture_book: Project,
) -> None:
    build_dir = fixture_book.generated_dir / "booklets/afc-east/book"
    edition = published_edition(fixture_book, build_dir, "afc/east")
    assert edition.model.division is not None
    assert edition.model.division.key == "afc-east"
    qr = [(build_dir / relative).resolve() for relative in edition.media.qr.values()]
    assert qr and all(p.parent == fixture_book.qr_dir for p in qr)
    assert fixture_book.qr_dir == fixture_book.generated_dir / "qr"


def test_edition_rejects_an_unknown_division_before_writing(
    fixture_book: Project, tmp_path: Path
) -> None:
    with pytest.raises(ValidationFailed) as raised:
        published_edition(fixture_book, tmp_path / "build", "afc/nowhere")
    assert "Unknown division" in raised.value.diagnostics.errors[0].message
    assert not fixture_book.qr_dir.exists()


def _book_with_version(project: Project, tmp_path: Path, version: str) -> Project:
    """The fixture book under a root whose version differs from the installed package."""
    root = tmp_path / "root"
    root.mkdir()
    (root / "pyproject.toml").write_text(
        f'[project]\nname = "nfl-game-day-cookbook"\nversion = "{version}"\n'
        'authors = [{ name = "Test Author" }]\n'
    )
    for name in ("templates", "styles"):
        shutil.copytree(REPO_ROOT / name, root / name)
    return Project.create(
        root,
        content_root=project.content_root,
        generated_dir=project.generated_dir,
        dist_dir=project.dist_dir,
    )


def test_every_target_takes_the_version_from_the_project_file(
    fixture_book: Project, tmp_path: Path
) -> None:
    project = _book_with_version(fixture_book, tmp_path, "9.8.7")
    assert project.version == "9.8.7"
    book = pipeline.build(project, pdf=False).document.parent
    text = "".join(p.read_text() for p in book.rglob("*.qmd"))
    assert "/v9.8.7/" in text
    assert not re.search(r"/v(?!9\.8\.7)\d+\.\d+\.\d+/", text)
    site = build_website(project, render=False).document.parent
    pages = "".join(p.read_text() for p in site.glob("*.qmd"))
    assert "/v9.8.7/" in pages
    assert "Edition 9.8.7" in (site / "_quarto.yml").read_text()
    assert not re.search(r"/v(?!9\.8\.7)\d+\.\d+\.\d+/", pages)
    epub = build_epub(project, render=False).document.read_text()
    assert "Test Author" in epub


def test_the_project_file_is_read_in_one_place() -> None:
    readers = [
        p.relative_to(SRC).as_posix()
        for p in SRC.rglob("*.py")
        if "pyproject.toml" in p.read_text()
    ]
    assert readers == ["project.py"]
    assert not [p for p in (SRC / "render").glob("*.py") if "__version__" in p.read_text()]


def _book_with_matching_dish(project: Project, name: str) -> None:
    """Give a bills recipe and a ravens recipe the same photo."""
    root = project.content_root
    source = root / "recipes/afc/east/bills/test-buffalo-sliders.md"
    ravens = root / "recipes/afc/north/ravens"
    ravens.mkdir(parents=True)
    Image.new("RGB", (40, 30), "red").save(ravens / f"{name}.jpg")
    Image.new("RGB", (40, 30), "red").save(source.parent / f"{name}.jpg")
    photo = f"image: {name}.jpg\nphoto_credit: Test\n"
    source.write_text(source.read_text().replace("\n---\n", f"\n{photo}---\n", 1))
    twin = source.read_text().replace("id: test-buffalo-sliders", "id: test-ravens-sliders")
    (ravens / "test-ravens-sliders.md").write_text(twin)


def test_booklets_share_one_photo_cache(fixture_book: Project) -> None:
    _book_with_matching_dish(fixture_book, "dish")
    first = pipeline.build(fixture_book, pdf=False, division="afc/east")
    second = pipeline.build(fixture_book, pdf=False, division="afc/north")
    assert first.photos.count == 1 and first.photos.cached == 0
    assert second.photos.count == 1 and second.photos.cached == 1
    assert list((fixture_book.generated_dir / "photos").glob("dish-*"))
    booklets = fixture_book.generated_dir / "booklets"
    assert not list(booklets.rglob("qr")) and not list(booklets.rglob("photos"))
    text = "".join(p.read_text() for p in second.document.parent.rglob("*.qmd"))
    assert "../../../qr/" in text


def test_a_fake_runner_is_the_only_seam_between_a_build_and_quarto(
    fixture_book: Project,
) -> None:
    quarto = FakeQuarto(installed=False)
    with pytest.raises(ValidationFailed):
        pipeline.build(fixture_book, quarto=quarto)
    assert quarto.calls


def test_a_new_asset_table_entry_is_listed_copied_and_loaded(
    fixture_book: Project, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import yaml

    from nfl_book import site_config

    project = _book_with_version(fixture_book, tmp_path, "1.0.0")
    (project.styles_dir / "website-extra.js").write_text("// extra\n")
    extra = site_config.SiteAsset("extra.js", "website-extra.js", script=True)
    monkeypatch.setattr(site_config, "ASSETS", (*site_config.ASSETS, extra))
    site = build_website(project, render=False).document.parent
    config = yaml.safe_load((site / "_quarto.yml").read_text())
    assert "extra.js" in config["project"]["resources"]
    assert (site / "extra.js").read_text() == "// extra\n"
    assert (
        '<script src="extra.js"></script>' in config["format"]["html"]["include-after-body"]["text"]
    )
