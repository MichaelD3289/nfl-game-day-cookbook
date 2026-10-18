"""Recipe photos become per-output variants; the authored originals are never touched."""

from __future__ import annotations

import io
from pathlib import Path

import pytest
from PIL import Image
from typer.testing import CliRunner

from nfl_book import pipeline
from nfl_book.cli import app
from nfl_book.config import load_settings
from nfl_book.errors import Diagnostics, ValidationFailed
from nfl_book.images import PhotoStats, build_photos, make_variant
from nfl_book.models.config import PhotoVariant
from nfl_book.project import Project
from nfl_book.website import build_website

WEB = PhotoVariant(format="webp", size=100, quality=80)
PRINT = PhotoVariant(format="jpeg", size=120, quality=82)
GPS = 0x8825
ORIENTATION = 0x0112


def photo_bytes(width: int, height: int, *, orientation: int = 1) -> bytes:
    """A synthetic JPEG: red left half, blue right half, with EXIF (GPS + orientation)."""
    image = Image.new("RGB", (width, height), "blue")
    image.paste("red", (0, 0, width // 2, height))
    exif = Image.Exif()
    exif[ORIENTATION] = orientation
    exif[GPS] = {1: "N", 2: (40.0, 26.0, 46.0)}
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=95, exif=exif)
    return buffer.getvalue()


def rgb(image: Image.Image, x: int, y: int) -> tuple[int, int, int]:
    pixel = image.convert("RGB").getpixel((x, y))
    assert isinstance(pixel, tuple)
    return (pixel[0], pixel[1], pixel[2])


def add_photo(project: Project, data: bytes, name: str = "test-wings.jpg") -> Path:
    recipe = next(project.recipes_dir.rglob("test-citrus-wings.md"))
    recipe.write_text(
        recipe.read_text().replace(
            "status: published",
            f"status: published\nimage: {name}\nphoto_credit: Synthetic fixture",
        )
    )
    photo = recipe.parent / name
    photo.write_bytes(data)
    return photo


def test_variant_is_square_resized_and_stripped(tmp_path: Path) -> None:
    source = tmp_path / "wide.jpg"
    source.write_bytes(photo_bytes(600, 300))
    for variant in (WEB, PRINT):
        photo, cached = make_variant(source, variant, tmp_path / "cache")
        assert not cached
        with Image.open(photo.path) as out:
            assert out.format == variant.format.upper()
            assert out.size == (variant.size, variant.size) == (photo.size, photo.size)
            assert not out.getexif()
            # Centre crop: both halves of the source remain visible.
            assert rgb(out, 5, variant.size // 2)[0] > 200
            assert rgb(out, variant.size - 5, variant.size // 2)[2] > 200


def test_variant_is_never_enlarged(tmp_path: Path) -> None:
    source = tmp_path / "small.jpg"
    source.write_bytes(photo_bytes(90, 60))
    photo, _ = make_variant(source, PRINT, tmp_path)
    assert photo.size == 60
    with Image.open(photo.path) as out:
        assert out.size == (60, 60)


def test_exif_rotation_is_applied_before_stripping(tmp_path: Path) -> None:
    source = tmp_path / "rotated.jpg"
    # Orientation 6: stored landscape (red left), displayed rotated 90° clockwise (red on top).
    source.write_bytes(photo_bytes(200, 200, orientation=6))
    photo, _ = make_variant(source, PRINT, tmp_path / "cache")
    with Image.open(photo.path) as out:
        assert not out.getexif()
        assert rgb(out, 60, 5)[0] > 200
        assert rgb(out, 60, 115)[2] > 200


def test_variants_are_cached_by_content_and_settings(tmp_path: Path) -> None:
    source = tmp_path / "wide.jpg"
    source.write_bytes(photo_bytes(600, 300))
    first, cached = make_variant(source, PRINT, tmp_path)
    assert not cached
    again, cached = make_variant(source, PRINT, tmp_path)
    assert cached and again == first
    other, cached = make_variant(source, PRINT.model_copy(update={"quality": 60}), tmp_path)
    assert not cached and other.path != first.path
    source.write_bytes(photo_bytes(600, 301))
    changed, cached = make_variant(source, PRINT, tmp_path)
    assert not cached and changed.path != first.path


def test_transparent_png_is_flattened_for_jpeg(tmp_path: Path) -> None:
    source = tmp_path / "clear.png"
    Image.new("RGBA", (80, 80), (0, 0, 0, 0)).save(source)
    photo, _ = make_variant(source, PRINT, tmp_path / "cache")
    with Image.open(photo.path) as out:
        assert out.mode == "RGB"
        assert rgb(out, 40, 40) == (255, 255, 255)


def test_corrupt_photo_is_a_diagnostic_naming_the_file(tmp_path: Path) -> None:
    source = tmp_path / "broken.jpg"
    source.write_bytes(b"not a jpeg")
    diags = Diagnostics()
    stats = PhotoStats()
    photos = build_photos({"recipe:x": source}, PRINT, tmp_path / "cache", diags, stats)
    assert photos == {}
    assert stats.count == 0
    assert [(d.code, d.path) for d in diags.errors] == [("image", source)]


def test_print_photos_must_be_jpeg(fixture_book: Project) -> None:
    book = fixture_book.data_dir / "book.yml"
    # Only the print photo format is JPEG, so this switches print to WebP.
    book.write_text(book.read_text().replace("format: jpeg", "format: webp"), encoding="utf-8")
    with pytest.raises(ValidationFailed) as failed:
        load_settings(fixture_book)
    assert [d.path for d in failed.value.diagnostics.errors] == [book]


def test_pdf_build_uses_resized_jpeg_and_keeps_source(fixture_book: Project) -> None:
    source = add_photo(fixture_book, photo_bytes(1600, 1200))
    before = (source.read_bytes(), source.stat().st_mtime_ns)
    result = pipeline.build(fixture_book, pdf=False)
    assert (source.read_bytes(), source.stat().st_mtime_ns) == before
    size = load_settings(fixture_book).book.photos.print.size
    photos = list(fixture_book.photo_cache_dir.glob("*.jpg"))
    assert len(photos) == 1
    with Image.open(photos[0]) as out:
        assert out.size == (size, size)
    page = next((fixture_book.book_build_dir / "pages").glob("*test-citrus-wings.qmd"))
    assert f"photos/{photos[0].name}" in page.read_text()
    assert result.photos.count == 1
    assert result.photos.source_bytes == len(before[0])
    assert result.photos.output_bytes == photos[0].stat().st_size


def test_website_uses_webp_with_dimensions(fixture_book: Project) -> None:
    source = add_photo(fixture_book, photo_bytes(1600, 1200))
    before = source.read_bytes()
    result = build_website(fixture_book, render=False)
    assert source.read_bytes() == before
    assets = fixture_book.generated_dir / "site" / "assets"
    photo = assets / "recipe-test-citrus-wings.webp"
    size = load_settings(fixture_book).book.photos.web.size
    with Image.open(photo) as out:
        assert out.format == "WEBP"
        assert out.size == (size, size)
    assert not [p for p in assets.iterdir() if p.suffix.lower() in (".jpg", ".jpeg")]
    wings = (fixture_book.generated_dir / "site" / "recipe-test-citrus-wings.qmd").read_text()
    assert (
        '(assets/recipe-test-citrus-wings.webp){fig-alt="Test Citrus Wings" '
        f'.dish-photo width="{size}" '
        f'height="{size}" loading="lazy" decoding="async"}}'
    ) in wings
    assert result.photos.count == 1


def test_corrupt_photo_fails_the_build_naming_the_file(fixture_book: Project) -> None:
    source = add_photo(fixture_book, b"\xff\xd8\xff not really a jpeg")
    with pytest.raises(ValidationFailed) as failed:
        pipeline.build(fixture_book, pdf=False)
    assert [(d.code, d.path) for d in failed.value.diagnostics.errors] == [("image", source)]
    with pytest.raises(ValidationFailed):
        build_website(fixture_book, render=False)


def test_cli_reports_photo_sizes(fixture_book: Project) -> None:
    add_photo(fixture_book, photo_bytes(800, 600))
    result = CliRunner().invoke(
        app,
        [
            "--root",
            str(fixture_book.root),
            "--content",
            str(fixture_book.content_root),
            "--generated",
            str(fixture_book.generated_dir),
            "--dist",
            str(fixture_book.dist_dir),
            "build",
            "--no-pdf",
        ],
    )
    assert result.exit_code == 0, result.output
    assert "Photos: 1 photo(s):" in result.output
