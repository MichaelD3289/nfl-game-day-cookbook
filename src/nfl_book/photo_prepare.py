"""Prepare recipe source photos as manifest-tracked WebP files, offline."""

from __future__ import annotations

import hashlib
import io
import os
import re
import tempfile
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from PIL import Image, ImageCms, ImageOps

from nfl_book.errors import BookError
from nfl_book.markdown import DocumentError, read_document

POLICY_VERSION = 1
MAX_EDGE = 2048
MIN_SHORT_EDGE = 500
MAX_BYTES = 1024 * 1024
QUALITY = 85
MANIFEST_KEY = "photos"
IMAGE_LINE = re.compile(r"(?m)^image:\s*[^\r\n]*$")


class PhotoPreparationError(BookError):
    """A source photo could not be prepared safely."""


@dataclass(frozen=True)
class PreparationResult:
    converted: int
    skipped: int


@dataclass(frozen=True)
class _ImagePlan:
    recipe: Path
    recipe_before: bytes
    recipe_after: bytes
    source: Path | None
    target: Path
    target_bytes: bytes | None
    manifest_key: str
    digest: str
    already_written: bool
    source_before: bytes | None = None


def parse_photo_manifest(raw: bytes | None, path: Path) -> dict[str, dict[str, Any]]:
    if raw is None:
        return {}
    try:
        data = yaml.safe_load(raw.decode("utf-8"))
    except (UnicodeDecodeError, yaml.YAMLError) as exc:
        raise PhotoPreparationError(f"{path}: cannot read photo manifest: {exc}") from exc
    if not isinstance(data, dict) or set(data) != {MANIFEST_KEY}:
        raise PhotoPreparationError(f"{path}: expected a mapping with only a '{MANIFEST_KEY}' key")
    photos = data[MANIFEST_KEY]
    if not isinstance(photos, dict):
        raise PhotoPreparationError(f"{path}: '{MANIFEST_KEY}' must be a mapping")
    result: dict[str, dict[str, Any]] = {}
    for key, value in photos.items():
        if (
            not isinstance(key, str)
            or not key
            or "\\" in key
            or Path(key).is_absolute()
            or ".." in Path(key).parts
            or not isinstance(value, dict)
            or set(value) != {"sha256", "policy"}
            or not isinstance(value.get("sha256"), str)
            or not re.fullmatch(r"[0-9a-f]{64}", value["sha256"])
            or type(value.get("policy")) is not int
        ):
            raise PhotoPreparationError(f"{path}: invalid manifest entry for {key!r}")
        result[key] = value
    return result


def _safe_image_path(recipe: Path, image_name: str, content_root: Path) -> Path:
    source = (recipe.parent / image_name).resolve()
    if content_root.resolve() not in source.parents:
        raise PhotoPreparationError(f"{recipe}: image path escapes the content root: {image_name}")
    return source


def _entry_key(path: Path, content_root: Path) -> str:
    return path.relative_to(content_root).as_posix()


def _is_manifested_webp(path: Path, key: str, entries: dict[str, dict[str, Any]]) -> str | None:
    entry = entries.get(key)
    if entry is None or entry.get("policy") != POLICY_VERSION:
        return None
    try:
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        if digest != entry["sha256"] or len(data) > MAX_BYTES:
            return None
        with Image.open(io.BytesIO(data)) as image:
            if image.format != "WEBP" or max(image.size) > MAX_EDGE:
                return None
            return digest
    except (OSError, ValueError, Image.DecompressionBombError):
        return None


def _dimensions(width: int, height: int, longest: int) -> tuple[int, int]:
    scale = min(1.0, longest / max(width, height))
    return max(1, round(width * scale)), max(1, round(height * scale))


def _prepare_bytes(source: Path, source_data: bytes) -> bytes:
    try:
        with Image.open(io.BytesIO(source_data)) as opened:
            opened.load()
            image = ImageOps.exif_transpose(opened)
            width, height = image.size
            short_floor = min(MIN_SHORT_EDGE, width, height)
            icc = image.info.get("icc_profile")
            if image.mode not in ("RGB", "RGBA"):
                if "A" in image.getbands() or image.info.get("transparency") is not None:
                    image = image.convert("RGBA")
                elif icc:
                    try:
                        source_profile = ImageCms.ImageCmsProfile(io.BytesIO(icc))
                        target_profile = ImageCms.createProfile("sRGB")
                        source_image = image.convert("RGB") if image.mode == "P" else image
                        profiled = ImageCms.profileToProfile(
                            source_image, source_profile, target_profile, outputMode="RGB"
                        )
                        if profiled is None:
                            raise PhotoPreparationError(
                                f"{source}: ICC conversion returned no image"
                            )
                        image = profiled
                        icc = ImageCms.ImageCmsProfile(target_profile).tobytes()
                    except (OSError, ValueError, ImageCms.PyCMSError) as exc:
                        raise PhotoPreparationError(
                            f"{source}: cannot convert its ICC profile: {exc}"
                        ) from exc
                else:
                    image = image.convert("RGB")
                    icc = None

            longest = min(MAX_EDGE, max(width, height))
            while True:
                size = _dimensions(width, height, longest)
                if min(size) < short_floor:
                    raise PhotoPreparationError(
                        f"{source}: cannot meet the 500 px minimum short edge and "
                        "2048 px maximum long edge"
                    )
                candidate = (
                    image.resize(size, Image.Resampling.LANCZOS)
                    if size != image.size
                    else image.copy()
                )
                buffer = io.BytesIO()
                options: dict[str, Any] = {
                    "quality": QUALITY,
                    "method": 6,
                    "exact": True,
                }
                if icc:
                    options["icc_profile"] = icc
                if candidate.mode == "RGBA":
                    options["alpha_quality"] = 100
                candidate.save(buffer, format="WEBP", **options)
                data = buffer.getvalue()
                if len(data) <= MAX_BYTES:
                    return data
                next_longest = int(longest * 0.9)
                if next_longest >= longest:
                    next_longest = longest - 1
                if next_longest < 1:
                    raise PhotoPreparationError(f"{source}: cannot meet the 1024 KiB size limit")
                longest = next_longest
    except PhotoPreparationError:
        raise
    except (OSError, ValueError, Image.DecompressionBombError) as exc:
        raise PhotoPreparationError(f"{source}: cannot prepare image: {exc}") from exc


def _replace_image_reference(recipe_data: bytes, recipe: Path, new_name: str) -> bytes:
    try:
        text = recipe_data.decode("utf-8")
        doc = read_document(recipe)
    except (UnicodeDecodeError, DocumentError) as exc:
        raise PhotoPreparationError(f"{recipe}: cannot update image reference: {exc}") from exc
    if not isinstance(doc.meta.get("image"), str):
        raise PhotoPreparationError(f"{recipe}: image must be a string")
    updated, count = IMAGE_LINE.subn(lambda _match: f"image: {new_name}", text, count=1)
    if count != 1:
        raise PhotoPreparationError(f"{recipe}: could not locate its image front matter")
    return updated.encode("utf-8")


def _write_temp(path: Path, data: bytes) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temp = Path(name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        _fsync_directory(path.parent)
    except BaseException:
        temp.unlink(missing_ok=True)
        raise
    return temp


def _fsync_directory(path: Path) -> None:
    directory_fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)


def _atomic_replace(path: Path, data: bytes) -> None:
    temp = _write_temp(path, data)
    try:
        temp.replace(path)
        _fsync_directory(path.parent)
    finally:
        temp.unlink(missing_ok=True)


def _assert_unchanged(path: Path, expected: bytes | None, label: str) -> None:
    try:
        current = path.read_bytes() if path.exists() else None
    except OSError as exc:
        raise PhotoPreparationError(f"{path}: cannot recheck {label}: {exc}") from exc
    if current != expected:
        raise PhotoPreparationError(f"{path}: {label} changed during photo preparation")


def _manifest_bytes(entries: dict[str, dict[str, Any]]) -> bytes:
    content = {MANIFEST_KEY: dict(sorted(entries.items()))}
    return yaml.safe_dump(content, sort_keys=False, allow_unicode=True).encode("utf-8")


def _in_place_backup(path: Path) -> Path:
    return path.with_name(f".{path.name}.prepare-photos.bak")


def _recover_in_place_backup(path: Path, key: str, entries: dict[str, dict[str, Any]]) -> None:
    backup = _in_place_backup(path)
    if not backup.exists():
        return
    try:
        backup_data = backup.read_bytes()
        current = path.read_bytes() if path.exists() else None
    except OSError as exc:
        raise PhotoPreparationError(
            f"{path}: cannot recover interrupted WebP preparation: {exc}"
        ) from exc
    entry = entries.get(key)
    committed = (
        current is not None
        and entry is not None
        and entry.get("policy") == POLICY_VERSION
        and hashlib.sha256(current).hexdigest() == entry.get("sha256")
    )
    if committed or current == backup_data:
        _assert_unchanged(path, current, "image during backup recovery")
        _assert_unchanged(backup, backup_data, "recovery backup")
        backup.unlink()
        _fsync_directory(backup.parent)
    else:
        expected_output = _prepare_bytes(path, backup_data)
        if current is not None and current != expected_output:
            raise PhotoPreparationError(
                f"{path}: current WebP differs from both its recovery backup and manifest; "
                f"preserving both files"
            )
        _assert_unchanged(path, current, "image during backup recovery")
        _assert_unchanged(backup, backup_data, "recovery backup")
        _atomic_replace(path, backup_data)
        _assert_unchanged(path, backup_data, "restored image")
        _assert_unchanged(backup, backup_data, "recovery backup")
        backup.unlink()
        _fsync_directory(backup.parent)


def _write_durable_backup(path: Path, data: bytes) -> Path:
    backup = _in_place_backup(path)
    try:
        fd = os.open(backup, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as exc:
        raise PhotoPreparationError(f"{backup}: recovery backup already exists") from exc
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        _fsync_directory(backup.parent)
    except BaseException:
        backup.unlink(missing_ok=True)
        raise
    return backup


def prepare_photos(content_root: Path, manifest_path: Path) -> PreparationResult:
    """Convert referenced recipe photos to WebP without network access.

    Originals are retained until every new image, recipe reference and manifest
    entry has been written successfully. Unrecognized target files are never
    overwritten.
    """
    content_root = content_root.resolve()
    try:
        old_manifest = manifest_path.read_bytes() if manifest_path.exists() else None
    except OSError as exc:
        raise PhotoPreparationError(f"{manifest_path}: cannot read photo manifest: {exc}") from exc
    entries = parse_photo_manifest(old_manifest, manifest_path)
    plans: list[_ImagePlan] = []
    output_entries: dict[str, dict[str, Any]] = {}
    image_refs: set[str] = set()

    recipes_root = content_root / "recipes"
    for recipe in sorted(recipes_root.rglob("*.md")):
        if any(part.startswith((".", "_")) for part in recipe.relative_to(recipes_root).parts):
            continue
        try:
            doc = read_document(recipe)
        except DocumentError as exc:
            raise PhotoPreparationError(
                f"{recipe}: cannot read recipe front matter: {exc}"
            ) from exc
        image_name = doc.meta.get("image")
        if image_name is None:
            continue
        if not isinstance(image_name, str) or not image_name:
            raise PhotoPreparationError(f"{recipe}: image must be a non-empty string")
        source = _safe_image_path(recipe, image_name, content_root)
        key = _entry_key(source, content_root)
        if key in image_refs:
            raise PhotoPreparationError(
                f"{recipe}: multiple recipes refer to the same image {source}"
            )
        image_refs.add(key)
        if source.suffix.lower() == ".webp":
            _recover_in_place_backup(source, key, entries)
        try:
            recipe_before = recipe.read_bytes()
        except OSError as exc:
            raise PhotoPreparationError(f"{recipe}: cannot read recipe: {exc}") from exc

        if source.suffix.lower() == ".webp":
            if not source.is_file():
                raise PhotoPreparationError(
                    f"{recipe}: referenced source photo is missing: {source}"
                )
            try:
                source_before = source.read_bytes()
            except OSError as exc:
                raise PhotoPreparationError(
                    f"{recipe}: cannot read source photo {source}: {exc}"
                ) from exc
            digest = _is_manifested_webp(source, key, entries)
            if digest == hashlib.sha256(source_before).hexdigest():
                output_entries[key] = {"sha256": digest, "policy": POLICY_VERSION}
                plans.append(
                    _ImagePlan(
                        recipe,
                        recipe_before,
                        recipe_before,
                        source,
                        source,
                        None,
                        key,
                        digest,
                        True,
                        source_before,
                    )
                )
                continue
            target_bytes = _prepare_bytes(source, source_before)
            digest = hashlib.sha256(target_bytes).hexdigest()
            output_entries[key] = {"sha256": digest, "policy": POLICY_VERSION}
            plans.append(
                _ImagePlan(
                    recipe,
                    recipe_before,
                    recipe_before,
                    source,
                    source,
                    target_bytes,
                    key,
                    digest,
                    False,
                    source_before,
                )
            )
            continue

        if source.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
            raise PhotoPreparationError(
                f"{recipe}: unsupported source image type: {source.suffix or '(none)'}"
            )
        if not source.is_file():
            raise PhotoPreparationError(f"{recipe}: referenced source photo is missing: {source}")
        try:
            source_before = source.read_bytes()
        except OSError as exc:
            raise PhotoPreparationError(
                f"{recipe}: cannot read source photo {source}: {exc}"
            ) from exc
        target = source.with_suffix(".webp")
        target_key = _entry_key(target, content_root)
        if target.exists():
            raise PhotoPreparationError(
                f"{recipe}: destination already exists; cannot verify it came from the current "
                f"source: {target}"
            )
        if target_key in image_refs or target_key in output_entries:
            raise PhotoPreparationError(
                f"{recipe}: multiple recipes would use the same image target {target}"
            )
        relative_target = Path(os.path.relpath(target, recipe.parent)).as_posix()
        recipe_after = _replace_image_reference(recipe_before, recipe, relative_target)
        target_bytes = _prepare_bytes(source, source_before)
        digest = hashlib.sha256(target_bytes).hexdigest()
        output_entries[target_key] = {"sha256": digest, "policy": POLICY_VERSION}
        plans.append(
            _ImagePlan(
                recipe,
                recipe_before,
                recipe_after,
                source,
                target,
                target_bytes,
                target_key,
                digest,
                False,
                source_before,
            )
        )

    skipped = sum(plan.already_written for plan in plans)
    changed = [plan for plan in plans if not plan.already_written]
    manifest_new = _manifest_bytes(output_entries)
    if not changed and old_manifest == manifest_new:
        return PreparationResult(converted=0, skipped=skipped)

    target_temps: list[tuple[_ImagePlan, Path]] = []
    created_targets: dict[Path, bytes] = {}
    in_place_outputs: dict[Path, tuple[bytes, bytes]] = {}
    changed_recipes: list[_ImagePlan] = []
    source_backups: dict[Path, Path] = {}
    metadata_backups: dict[Path, Path] = {}
    manifest_written = False
    committed = False
    try:
        for plan in changed:
            assert plan.target_bytes is not None
            target_temps.append((plan, _write_temp(plan.target, plan.target_bytes)))

        _assert_unchanged(manifest_path, old_manifest, "photo manifest")
        for plan in changed:
            _assert_unchanged(plan.recipe, plan.recipe_before, "recipe")
            if plan.source is not None:
                _assert_unchanged(plan.source, plan.source_before, "source photo")
            if plan.source != plan.target:
                _assert_unchanged(plan.target, None, "destination")

        for plan in changed:
            if plan.recipe_before != plan.recipe_after:
                metadata_backups[plan.recipe] = _write_temp(plan.recipe, plan.recipe_before)
        if old_manifest != manifest_new:
            metadata_backups[manifest_path] = _write_temp(
                manifest_path, old_manifest if old_manifest is not None else b""
            )

        for plan, temp in target_temps:
            if plan.source == plan.target:
                assert plan.source_before is not None and plan.target_bytes is not None
                _assert_unchanged(plan.target, plan.source_before, "source WebP")
                in_place_outputs[plan.target] = (plan.source_before, plan.target_bytes)
                source_backups[plan.target] = _write_durable_backup(plan.target, plan.source_before)
                _assert_unchanged(plan.target, plan.source_before, "source WebP")
                temp.replace(plan.target)
                _fsync_directory(plan.target.parent)
            else:
                assert plan.target_bytes is not None
                try:
                    os.link(temp, plan.target)
                    created_targets[plan.target] = plan.target_bytes
                    _fsync_directory(plan.target.parent)
                except FileExistsError as exc:
                    raise PhotoPreparationError(
                        f"{plan.target}: destination appeared during preparation"
                    ) from exc

        for plan in changed:
            if plan.recipe_before != plan.recipe_after:
                _assert_unchanged(plan.recipe, plan.recipe_before, "recipe")
                changed_recipes.append(plan)
                _atomic_replace(plan.recipe, plan.recipe_after)
        if old_manifest != manifest_new:
            _assert_unchanged(manifest_path, old_manifest, "photo manifest")
            manifest_written = True
            _atomic_replace(manifest_path, manifest_new)

        # Check every old source before any of them are removed.
        for plan in changed:
            if plan.source is not None and plan.source != plan.target:
                _assert_unchanged(plan.source, plan.source_before, "source photo before removal")
                assert plan.source_before is not None
                source_backups[plan.source] = _write_temp(plan.source, plan.source_before)
        for plan in changed:
            if plan.source is not None and plan.source != plan.target:
                _assert_unchanged(plan.source, plan.source_before, "source photo before removal")
                plan.source.unlink()
                _fsync_directory(plan.source.parent)
        committed = True
    except BaseException as cause:
        rollback_errors: list[str] = []
        for source, backup in source_backups.items():
            if source in in_place_outputs:
                continue
            try:
                original = backup.read_bytes()
                if not source.exists():
                    os.link(backup, source)
                _fsync_directory(source.parent)
                if source.read_bytes() != original:
                    raise OSError("restored source does not match its backup")
            except OSError as exc:
                rollback_errors.append(
                    f"{source}: could not restore original: {exc}; backup at {backup}"
                )
        for plan in reversed(changed_recipes):
            recipe_backup = metadata_backups.get(plan.recipe)
            try:
                current_recipe = plan.recipe.read_bytes()
                if current_recipe == plan.recipe_after:
                    original = (
                        recipe_backup.read_bytes()
                        if recipe_backup is not None
                        else plan.recipe_before
                    )
                    _atomic_replace(plan.recipe, original)
                    if plan.recipe.read_bytes() != plan.recipe_before:
                        raise OSError("recipe does not match its original contents")
            except OSError as exc:
                backup_note = (
                    f"; recovery backup at {recipe_backup}" if recipe_backup is not None else ""
                )
                rollback_errors.append(
                    f"{plan.recipe}: could not restore recipe: {exc}{backup_note}"
                )
        if manifest_written:
            manifest_backup = metadata_backups.get(manifest_path)
            try:
                current_manifest = manifest_path.read_bytes() if manifest_path.exists() else None
                if current_manifest == manifest_new:
                    if old_manifest is None:
                        manifest_path.unlink(missing_ok=True)
                        _fsync_directory(manifest_path.parent)
                    else:
                        original = (
                            manifest_backup.read_bytes()
                            if manifest_backup is not None
                            else old_manifest
                        )
                        _atomic_replace(manifest_path, original)
                current_manifest = manifest_path.read_bytes() if manifest_path.exists() else None
                if current_manifest == manifest_new:
                    raise OSError("manifest does not match its original contents")
            except OSError as exc:
                backup_note = (
                    f"; recovery backup at {manifest_backup}" if manifest_backup is not None else ""
                )
                rollback_errors.append(
                    f"{manifest_path}: could not restore manifest: {exc}{backup_note}"
                )
        for path, (original, expected) in in_place_outputs.items():
            webp_backup = source_backups.get(path)
            try:
                if path.read_bytes() == expected:
                    original = webp_backup.read_bytes() if webp_backup is not None else original
                    _atomic_replace(path, original)
                if webp_backup is not None and path.read_bytes() != webp_backup.read_bytes():
                    raise OSError("restored WebP does not match its recovery backup")
            except OSError as exc:
                backup_note = (
                    f"; recovery backup at {webp_backup}" if webp_backup is not None else ""
                )
                rollback_errors.append(f"{path}: could not restore WebP: {exc}{backup_note}")
        for path, expected in created_targets.items():
            try:
                if path.read_bytes() == expected:
                    path.unlink(missing_ok=True)
                    _fsync_directory(path.parent)
                if path.exists():
                    raise OSError("prepared destination remains after rollback")
            except OSError as exc:
                rollback_errors.append(f"{path}: could not remove prepared destination: {exc}")

        for path, backup in source_backups.items():
            if path in in_place_outputs:
                try:
                    restored = path.exists() and path.read_bytes() == backup.read_bytes()
                except OSError:
                    restored = False
            else:
                try:
                    restored = path.exists() and path.read_bytes() == backup.read_bytes()
                except OSError:
                    restored = False
            if restored:
                try:
                    backup.unlink()
                    _fsync_directory(backup.parent)
                except OSError as exc:
                    rollback_errors.append(f"{backup}: could not remove verified backup: {exc}")
        for path, backup in metadata_backups.items():
            try:
                current = path.read_bytes() if path.exists() else None
                backup_contents = (
                    None if path == manifest_path and old_manifest is None else backup.read_bytes()
                )
                expected = (
                    manifest_new
                    if path == manifest_path
                    else next(plan.recipe_after for plan in changed_recipes if plan.recipe == path)
                )
                restored = current == backup_contents or current != expected
            except OSError:
                restored = False
            if restored:
                try:
                    backup.unlink()
                    _fsync_directory(backup.parent)
                except OSError as exc:
                    rollback_errors.append(f"{backup}: could not remove verified backup: {exc}")
        if rollback_errors:
            details = "\n".join(f"- {error}" for error in rollback_errors)
            raise PhotoPreparationError(f"{cause}\nRollback incomplete:\n{details}") from cause
        raise
    finally:
        for _plan, temp in target_temps:
            temp.unlink(missing_ok=True)
        for _source, backup in source_backups.items():
            if committed:
                with suppress(OSError):
                    backup.unlink(missing_ok=True)
                    _fsync_directory(backup.parent)
        if committed:
            for backup in metadata_backups.values():
                with suppress(OSError):
                    backup.unlink(missing_ok=True)
                    _fsync_directory(backup.parent)
    return PreparationResult(converted=len(changed), skipped=skipped)
