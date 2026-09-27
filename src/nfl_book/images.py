"""Per-output photo variants: square, resized, recompressed and metadata-free.

Source photos under ``recipes/`` are only ever read. Each variant is written to a
content-addressed cache (source bytes + settings) so rebuilds reuse earlier work.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageOps

from nfl_book.errors import Diagnostics
from nfl_book.models.config import PhotoVariant

# Bump when the processing below changes so cached variants are regenerated.
PIPELINE_VERSION = 1
SUFFIX = {"jpeg": ".jpg", "webp": ".webp"}


@dataclass(frozen=True)
class Photo:
    path: Path
    size: int  # square side in pixels


@dataclass
class PhotoStats:
    """Total bytes of the source photos and of the variants built from them."""

    count: int = 0
    source_bytes: int = 0
    output_bytes: int = 0

    def summary(self) -> str:
        def mb(n: int) -> str:
            return f"{n / 1_000_000:.1f} MB"

        return f"{self.count} photo(s): {mb(self.source_bytes)} -> {mb(self.output_bytes)}"


def _cache_name(source: Path, data: bytes, variant: PhotoVariant) -> str:
    key = f"{PIPELINE_VERSION}:{variant.model_dump_json()}".encode()
    digest = hashlib.sha256(key + data).hexdigest()[:16]
    return f"{source.stem}-{digest}{SUFFIX[variant.format]}"


def _flatten(image: Image.Image, keep_alpha: bool) -> Image.Image:
    if image.mode in ("RGB", "RGBA" if keep_alpha else "RGB"):
        return image
    if "A" in image.getbands() or image.info.get("transparency") is not None:
        image = image.convert("RGBA")
        if keep_alpha:
            return image
        background = Image.new("RGB", image.size, "white")
        background.paste(image, mask=image.getchannel("A"))
        return background
    return image.convert("RGB")


def make_variant(source: Path, variant: PhotoVariant, cache_dir: Path) -> tuple[Photo, bool]:
    """Write (or reuse) the variant of ``source``; returns it and whether it was cached.

    Raises ``OSError`` (or a Pillow error) when the source cannot be decoded.
    """
    data = source.read_bytes()
    target = cache_dir / _cache_name(source, data, variant)
    with Image.open(source) as opened:
        width, height = opened.size
        # EXIF orientation 5-8 swaps the axes; the square side is the same either way.
        side = min(variant.size, width, height)
        if target.is_file():
            return Photo(target, side), True
        opened.load()
        image = ImageOps.exif_transpose(opened)
    # Only an RGB profile still describes the pixels after conversion.
    icc = image.info.get("icc_profile") if image.mode in ("RGB", "RGBA") else None
    image = _flatten(image, keep_alpha=variant.format == "webp")
    square = ImageOps.fit(image, (side, side), Image.Resampling.LANCZOS)
    square.info = {}
    cache_dir.mkdir(parents=True, exist_ok=True)
    partial = target.with_name(f".{target.name}.tmp")
    # Cleared info drops EXIF (incl. location) and XMP; the ICC profile keeps colours true.
    options: dict[str, object] = {"quality": variant.quality}
    if icc:
        options["icc_profile"] = icc
    if variant.format == "jpeg":
        options.update(optimize=True, progressive=True)
    else:
        options.update(method=6)
    square.save(partial, format=variant.format.upper(), **options)
    partial.replace(target)
    return Photo(target, side), False


def build_photos(
    sources: dict[str, Path],
    variant: PhotoVariant,
    cache_dir: Path,
    diagnostics: Diagnostics,
    stats: PhotoStats,
) -> dict[str, Photo]:
    """Variants for ``{media key: source}``; unreadable photos become diagnostics."""
    photos = {}
    for key, source in sources.items():
        try:
            photo, _ = make_variant(source, variant, cache_dir)
        except (OSError, SyntaxError, ValueError, Image.DecompressionBombError) as exc:
            diagnostics.error("image", f"cannot read image {source.name}: {exc}", source)
            continue
        photos[key] = photo
        stats.count += 1
        stats.source_bytes += source.stat().st_size
        stats.output_bytes += photo.path.stat().st_size
    return photos
