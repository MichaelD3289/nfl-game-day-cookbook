"""Assemble the Pages site from a fresh build plus synthetic release ZIPs."""

import hashlib
import json
import zipfile
from pathlib import Path

import pytest

from nfl_book.errors import Diagnostics
from nfl_book.publishing import RELEASES
from nfl_book.site_archive import MEDIA, VERSIONS_MARKER, WEBSITE_ZIP, assemble, main
from nfl_book.website_check import check_site

PDF = "test-booklet.pdf"


def _page(version: str, body: str = "") -> str:
    return (
        '<!DOCTYPE html>\n<html lang="en"><head>\n<meta charset="utf-8">\n'
        f'<title>{version}</title>\n</head>\n<body class="nav-sidebar">\n'
        f'<a href="{RELEASES}/latest/download/{PDF}">Download PDF</a>\n'
        f"<p>Edition {version}</p>{body}\n</body></html>\n"
    )


def _site(folder: Path, version: str, *, extra: tuple[str, ...] = ()) -> Path:
    folder.mkdir(parents=True)
    (folder / "index.html").write_text(_page(version))
    (folder / "recipe-test-citrus-wings.html").write_text(_page(version))
    (folder / "versions.html").write_text(_page(version, f"\n{VERSIONS_MARKER}"))
    for name in extra:
        (folder / name).write_text(_page(version))
    return folder


def _release(archive: Path, tag: str, *, date: str, assets: tuple[str, ...]) -> None:
    archive.mkdir(parents=True, exist_ok=True)
    data = {
        "tagName": tag,
        "publishedAt": f"{date}T12:00:00Z",
        "assets": [{"name": name} for name in assets],
    }
    (archive / f"{tag}.json").write_text(json.dumps(data))


def _zip(archive: Path, tag: str, site: Path) -> None:
    (archive / tag).mkdir(parents=True)
    with zipfile.ZipFile(archive / tag / WEBSITE_ZIP, "w") as bundle:
        for path in site.rglob("*"):
            bundle.write(path, path.relative_to(site).as_posix())


@pytest.fixture
def releases(tmp_path: Path) -> Path:
    """v0.4.0 predates the website; v0.5.0 has a ZIP with an extra retired page."""
    archive = tmp_path / "archive"
    _release(archive, "v0.4.0", date="2026-01-10", assets=(PDF,))
    _release(archive, "v0.5.0", date="2026-02-20", assets=(PDF, WEBSITE_ZIP))
    _zip(archive, "v0.5.0", _site(tmp_path / "old", "0.5.0", extra=("recipe-test-retired.html",)))
    _release(archive, "v0.6.0", date="2026-03-30", assets=(PDF, WEBSITE_ZIP))
    return archive


def test_newest_release_is_root_and_each_version_has_a_folder(
    tmp_path: Path, releases: Path
) -> None:
    site = _site(tmp_path / "fresh", "0.6.0")
    out = tmp_path / "pages"
    diags = Diagnostics()
    assert assemble("v0.6.0", site, releases, out, PDF, diags) == "v0.6.0"
    assert diags.ok and not diags.warnings, [d.format() for d in diags]

    assert "Edition 0.6.0" in (out / "index.html").read_text()
    assert "noindex" not in (out / "index.html").read_text()
    assert (out / "v0.6.0/recipe-test-citrus-wings.html").is_file()
    assert "Edition 0.5.0" in (out / "v0.5.0/recipe-test-citrus-wings.html").read_text()
    assert not (out / "v0.4.0").exists()
    # A copy of the latest release is not a separate edition: no banner, but noindex.
    latest_copy = (out / "v0.6.0/index.html").read_text()
    assert '<meta name="robots" content="noindex">' in latest_copy
    assert "archived-version" not in latest_copy

    check = Diagnostics()
    check_site(out, check)
    assert check.ok, [d.format() for d in check]


def test_archived_pages_get_banner_noindex_and_their_own_pdf(
    tmp_path: Path, releases: Path
) -> None:
    out = tmp_path / "pages"
    assemble("v0.6.0", _site(tmp_path / "fresh", "0.6.0"), releases, out, PDF, Diagnostics())
    wings = (out / "v0.5.0/recipe-test-citrus-wings.html").read_text()
    assert '<head>\n<meta name="robots" content="noindex">' in wings
    assert "You're viewing v0.5.0." in wings
    assert 'href="../recipe-test-citrus-wings.html">See the latest version' in wings
    assert f"{RELEASES}/download/v0.5.0/{PDF}" in wings
    assert "/latest/download/" not in wings
    # A page that no longer exists in the latest release falls back to its home page.
    retired = (out / "v0.5.0/recipe-test-retired.html").read_text()
    assert 'href="../index.html">See the latest version' in retired


def test_versions_page_lists_each_kept_version(tmp_path: Path, releases: Path) -> None:
    out = tmp_path / "pages"
    assemble("v0.6.0", _site(tmp_path / "fresh", "0.6.0"), releases, out, PDF, Diagnostics())
    root = (out / "versions.html").read_text()
    assert VERSIONS_MARKER not in root
    assert root.index("v0.6.0") < root.index("v0.5.0")
    assert 'href="index.html">v0.6.0</a> (latest) · 2026-03-30' in root
    assert 'href="v0.5.0/index.html">v0.5.0</a> · 2026-02-20' in root
    assert f"{RELEASES}/download/v0.5.0/{PDF}" in root
    assert "v0.4.0" not in root
    nested = (out / "v0.6.0/versions.html").read_text()
    assert 'href="../v0.5.0/index.html">v0.5.0</a>' in nested
    assert 'href="../index.html">v0.6.0</a>' in nested


def test_rebuilding_an_older_tag_keeps_the_newest_root(tmp_path: Path, releases: Path) -> None:
    _zip(releases, "v0.6.0", _site(tmp_path / "newest", "0.6.0"))
    out = tmp_path / "pages"
    diags = Diagnostics()
    assert assemble("v0.5.0", _site(tmp_path / "fresh", "0.5.0"), releases, out, PDF, diags) == (
        "v0.6.0"
    )
    assert "Edition 0.6.0" in (out / "index.html").read_text()
    assert "Edition 0.5.0" in (out / "v0.5.0/index.html").read_text()
    assert "You're viewing v0.5.0." in (out / "v0.5.0/index.html").read_text()


def test_missing_newest_zip_leaves_an_older_root_for_the_caller_to_reject(
    tmp_path: Path, releases: Path
) -> None:
    out = tmp_path / "pages"
    diags = Diagnostics()
    root = assemble("v0.5.0", _site(tmp_path / "fresh", "0.5.0"), releases, out, PDF, diags)
    assert root == "v0.5.0"
    assert [d.path for d in diags.warnings] == [releases / "v0.6.0" / WEBSITE_ZIP]


def test_corrupt_or_unsafe_zips_are_skipped_with_a_warning(tmp_path: Path, releases: Path) -> None:
    (releases / "v0.5.0" / WEBSITE_ZIP).write_bytes(b"not a zip")
    _release(releases, "v0.5.1", date="2026-02-25", assets=(WEBSITE_ZIP,))
    (releases / "v0.5.1").mkdir()
    with zipfile.ZipFile(releases / "v0.5.1" / WEBSITE_ZIP, "w") as bundle:
        bundle.writestr("index.html", "<html></html>")
        bundle.writestr("../escape.html", "<html></html>")
    out = tmp_path / "pages"
    diags = Diagnostics()
    assert assemble("v0.6.0", _site(tmp_path / "fresh", "0.6.0"), releases, out, PDF, diags) == (
        "v0.6.0"
    )
    assert diags.ok
    assert {d.path for d in diags.warnings} == {
        releases / "v0.5.0" / WEBSITE_ZIP,
        releases / "v0.5.1" / WEBSITE_ZIP,
    }
    assert not (out / "v0.5.0").exists()
    assert not (out / "v0.5.1").exists()
    assert not (tmp_path / "escape.html").exists()
    assert "v0.5.0" not in (out / "versions.html").read_text()


def test_prerelease_build_is_not_published(tmp_path: Path, releases: Path) -> None:
    _zip(releases, "v0.6.0", _site(tmp_path / "newest", "0.6.0"))
    out = tmp_path / "pages"
    site = _site(tmp_path / "fresh", "0.7.0-rc.1")
    assert assemble("v0.7.0-rc.1", site, releases, out, PDF, Diagnostics()) == "v0.6.0"
    assert not (out / "v0.7.0-rc.1").exists()


def test_existing_output_is_an_error(tmp_path: Path, releases: Path) -> None:
    out = tmp_path / "pages"
    out.mkdir()
    diags = Diagnostics()
    assert assemble("v0.6.0", _site(tmp_path / "fresh", "0.6.0"), releases, out, PDF, diags) is None
    assert diags.errors[0].path == out


def test_command_prints_root_tag(
    tmp_path: Path, releases: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    site = _site(tmp_path / "fresh", "0.6.0")
    args = ["--tag", "v0.6.0", "--site", str(site), "--archive", str(releases)]
    code = main([*args, "--out", str(tmp_path / "pages"), "--pdf", PDF])
    assert code == 0
    assert capsys.readouterr().out == "v0.6.0\n"


def _with_photo(site: Path, photo: bytes, *, page: str = "recipe-test-citrus-wings.html") -> Path:
    (site / "assets").mkdir(exist_ok=True)
    (site / "assets/recipe-test-citrus-wings.jpg").write_bytes(photo)
    (site / "assets/qr-recipe-test-citrus-wings.png").write_bytes(b"same QR")
    (site / "assets/unused.png").write_bytes(b"never linked " + photo)
    depth = "../" * page.count("/")
    body = (
        f'<img src="{depth}assets/recipe-test-citrus-wings.jpg" '
        f'srcset="{depth}assets/recipe-test-citrus-wings.jpg 2x">'
        f'<img src="{depth}assets/qr-recipe-test-citrus-wings.png">'
        f"<div style=\"background: url('{depth}assets/recipe-test-citrus-wings.jpg')\"></div>"
    )
    (site / page).parent.mkdir(parents=True, exist_ok=True)
    (site / page).write_text(_page("x", body))
    return site


def _media(data: bytes, suffix: str) -> str:
    return f"{MEDIA}/{hashlib.sha256(data).hexdigest()}{suffix}"


def test_identical_images_are_stored_once_across_versions(tmp_path: Path, releases: Path) -> None:
    _zip(releases, "v0.6.0", _with_photo(_site(tmp_path / "newest", "0.6.0"), b"photo"))
    old = _with_photo(_site(tmp_path / "older", "0.5.0"), b"photo", page="teams/wings.html")
    (releases / "v0.5.0" / WEBSITE_ZIP).unlink()
    (releases / "v0.5.0").rmdir()
    _zip(releases, "v0.5.0", old)
    out = tmp_path / "pages"
    fresh = _with_photo(_site(tmp_path / "fresh", "0.6.1"), b"photo")
    _release(releases, "v0.6.1", date="2026-04-01", assets=(WEBSITE_ZIP,))
    diags = Diagnostics()
    assert assemble("v0.6.1", fresh, releases, out, PDF, diags) == "v0.6.1"
    assert diags.ok, [d.format() for d in diags]

    photo, qr = _media(b"photo", ".jpg"), _media(b"same QR", ".png")
    assert sorted(p.name for p in (out / MEDIA).iterdir()) == sorted(
        Path(p).name for p in (photo, qr)
    )
    assert not list(out.rglob("assets"))
    root = (out / "recipe-test-citrus-wings.html").read_text()
    assert f'src="{photo}" srcset="{photo} 2x"' in root
    assert f"url('{photo}')" in root
    assert f'src="../{photo}"' in (out / "v0.6.0/recipe-test-citrus-wings.html").read_text()
    # Pages in subfolders link up one extra level.
    assert f'src="../../{qr}"' in (out / "v0.5.0/teams/wings.html").read_text()


def test_changed_photo_keeps_old_contents_on_old_version(tmp_path: Path, releases: Path) -> None:
    _zip(releases, "v0.6.0", _with_photo(_site(tmp_path / "newest", "0.6.0"), b"old photo"))
    fresh = _with_photo(_site(tmp_path / "fresh", "0.6.1"), b"new photo")
    _release(releases, "v0.6.1", date="2026-04-01", assets=(WEBSITE_ZIP,))
    out = tmp_path / "pages"
    assemble("v0.6.1", fresh, releases, out, PDF, Diagnostics())
    old, new = _media(b"old photo", ".jpg"), _media(b"new photo", ".jpg")
    assert (out / old).read_bytes() == b"old photo"
    assert f'src="../{old}"' in (out / "v0.6.0/recipe-test-citrus-wings.html").read_text()
    assert f'src="{new}"' in (out / "recipe-test-citrus-wings.html").read_text()
    assert f'src="../{new}"' in (out / "v0.6.1/recipe-test-citrus-wings.html").read_text()


def test_search_index_asset_paths_are_relinked(tmp_path: Path, releases: Path) -> None:
    site = _with_photo(_site(tmp_path / "fresh", "0.6.0"), b"photo")
    entries = [{"href": "recipe-test-citrus-wings.html", "img": "assets/unused.png"}]
    (site / "search.json").write_text(json.dumps(entries))
    out = tmp_path / "pages"
    assemble("v0.6.0", site, releases, out, PDF, Diagnostics())
    unused = _media(b"never linked photo", ".png")
    assert json.loads((out / "search.json").read_text())[0]["img"] == unused
    assert json.loads((out / "v0.6.0/search.json").read_text())[0]["img"] == f"../{unused}"
    assert (out / unused).is_file()


def test_release_zips_are_left_unchanged(tmp_path: Path, releases: Path) -> None:
    _zip(releases, "v0.6.0", _with_photo(_site(tmp_path / "newest", "0.6.0"), b"photo"))
    before = (releases / "v0.6.0" / WEBSITE_ZIP).read_bytes()
    assemble(
        "v0.5.0",
        _site(tmp_path / "fresh", "0.5.0"),
        releases,
        tmp_path / "pages",
        PDF,
        Diagnostics(),
    )
    assert (releases / "v0.6.0" / WEBSITE_ZIP).read_bytes() == before


def test_missed_reference_fails_the_assembly(tmp_path: Path, releases: Path) -> None:
    site = _site(tmp_path / "fresh", "0.6.0")
    (site / "index.html").write_text(_page("0.6.0", '<img src="assets/missing.png">'))
    diags = Diagnostics()
    assemble("v0.6.0", site, releases, tmp_path / "pages", PDF, diags)
    assert not diags.ok
    assert {d.code for d in diags.errors} == {"website-link"}
