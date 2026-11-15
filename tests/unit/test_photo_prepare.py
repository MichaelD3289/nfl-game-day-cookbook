"""Offline source-photo preparation, using synthetic images and recipes."""

from __future__ import annotations

import hashlib
import io
import os
import random
import stat
from pathlib import Path

import pytest
import yaml
from PIL import Image, ImageCms
from typer.testing import CliRunner

from nfl_book import photo_prepare
from nfl_book.cli import app
from nfl_book.photo_prepare import PhotoPreparationError, prepare_photos
from nfl_book.project import Project

RECIPE = Path("recipes/afc/east/dolphins/test-citrus-wings.md")


def jpeg_bytes(size: tuple[int, int], *, orientation: int = 1) -> bytes:
    image = Image.new("RGB", size, "red")
    exif = Image.Exif()
    exif[0x0112] = orientation
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=95, exif=exif)
    return buffer.getvalue()


def webp_bytes(size: tuple[int, int], *, quality: int = 85) -> bytes:
    image = Image.new("RGB", size, "purple")
    buffer = io.BytesIO()
    image.save(buffer, format="WEBP", quality=quality)
    return buffer.getvalue()


def recipe_with_photo(project: Project, name: str = "test-citrus-wings.jpg") -> tuple[Path, Path]:
    recipe = project.content_root / RECIPE
    text = recipe.read_text(encoding="utf-8")
    recipe.write_text(
        text.replace(
            "status: published\n",
            f"status: published\nimage: {name}\nphoto_credit: Synthetic credit\n",
        ),
        encoding="utf-8",
    )
    photo = recipe.parent / name
    photo.write_bytes(jpeg_bytes((1200, 800), orientation=6))
    return recipe, photo


def recipe_with_webp(project: Project, name: str = "test-citrus-wings.webp") -> tuple[Path, Path]:
    recipe = project.content_root / RECIPE
    text = recipe.read_text(encoding="utf-8")
    recipe.write_text(
        text.replace(
            "status: published\n",
            f"status: published\nimage: {name}\nphoto_credit: Synthetic credit\n",
        ),
        encoding="utf-8",
    )
    photo = recipe.parent / name
    photo.write_bytes(webp_bytes((1200, 800)))
    return recipe, photo


def test_prepare_converts_photo_and_updates_recipe_and_manifest(fixture_book: Project) -> None:
    recipe, source = recipe_with_photo(fixture_book)
    original = source.read_bytes()
    manifest = fixture_book.data_dir / "photo-manifest.yml"

    result = prepare_photos(fixture_book.content_root, manifest)

    target = source.with_suffix(".webp")
    assert result.converted == 1
    assert result.skipped == 0
    assert not source.exists()
    assert target.is_file()
    with Image.open(target) as image:
        assert image.format == "WEBP"
        assert image.size == (800, 1200)  # EXIF orientation is applied without cropping.
    text = recipe.read_text(encoding="utf-8")
    assert "image: test-citrus-wings.webp" in text
    assert "photo_credit: Synthetic credit" in text
    assert "## Ingredients" in text
    data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    key = source.with_suffix(".webp").relative_to(fixture_book.content_root).as_posix()
    assert data == {
        "photos": {key: {"sha256": hashlib.sha256(target.read_bytes()).hexdigest(), "policy": 1}}
    }
    assert original  # Test fixture was a real source image before conversion.


def test_prepare_is_idempotent(fixture_book: Project) -> None:
    _recipe, source = recipe_with_photo(fixture_book)
    manifest = fixture_book.data_dir / "photo-manifest.yml"
    first = prepare_photos(fixture_book.content_root, manifest)
    target = source.with_suffix(".webp")
    target_bytes = target.read_bytes()
    recipe_path = fixture_book.content_root / RECIPE
    recipe_bytes = recipe_path.read_bytes()
    manifest_bytes = manifest.read_bytes()

    second = prepare_photos(fixture_book.content_root, manifest)

    assert first.converted == 1
    assert second.converted == 0
    assert second.skipped == 1
    assert target.read_bytes() == target_bytes
    assert recipe_path.read_bytes() == recipe_bytes
    assert manifest.read_bytes() == manifest_bytes


def test_prepare_normalizes_unregistered_webp_in_place(fixture_book: Project) -> None:
    _recipe, source = recipe_with_webp(fixture_book)
    original = source.read_bytes()
    manifest = fixture_book.data_dir / "photo-manifest.yml"

    result = prepare_photos(fixture_book.content_root, manifest)

    assert result.converted == 1
    assert result.skipped == 0
    assert source.is_file()
    data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    key = source.relative_to(fixture_book.content_root).as_posix()
    assert data["photos"][key] == {
        "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "policy": 1,
    }
    with Image.open(source) as output:
        assert output.format == "WEBP"
        assert max(output.size) <= 2048
    assert source.read_bytes() != b""
    assert original


def test_prepare_recovers_backup_after_interrupted_in_place_replace(fixture_book: Project) -> None:
    _recipe, source = recipe_with_webp(fixture_book)
    original = source.read_bytes()
    expected = photo_prepare._prepare_bytes(source, original)
    backup = source.with_name(f".{source.name}.prepare-photos.bak")
    backup.write_bytes(original)
    source.write_bytes(expected)  # Simulate termination after replace, before manifest write.

    result = prepare_photos(fixture_book.content_root, fixture_book.data_dir / "photo-manifest.yml")

    assert result.converted == 1
    assert source.read_bytes() == expected
    assert not backup.exists()
    data = yaml.safe_load((fixture_book.data_dir / "photo-manifest.yml").read_text())
    key = source.relative_to(fixture_book.content_root).as_posix()
    assert data["photos"][key]["sha256"] == hashlib.sha256(expected).hexdigest()


def test_prepare_preserves_manual_edit_when_recovery_backup_exists(fixture_book: Project) -> None:
    _recipe, source = recipe_with_webp(fixture_book)
    original = source.read_bytes()
    backup = source.with_name(f".{source.name}.prepare-photos.bak")
    backup.write_bytes(original)
    manual_edit = webp_bytes((700, 700), quality=45)
    source.write_bytes(manual_edit)

    with pytest.raises(PhotoPreparationError, match="preserving both files"):
        prepare_photos(fixture_book.content_root, fixture_book.data_dir / "photo-manifest.yml")

    assert source.read_bytes() == manual_edit
    assert backup.read_bytes() == original


def test_recovery_rechecks_webp_before_restoring_backup(
    fixture_book: Project, monkeypatch: pytest.MonkeyPatch
) -> None:
    _recipe, source = recipe_with_webp(fixture_book)
    original = webp_bytes((1200, 800), quality=40)
    source.write_bytes(original)
    backup = source.with_name(f".{source.name}.prepare-photos.bak")
    backup.write_bytes(original)
    expected = photo_prepare._prepare_bytes(source, original)
    source.write_bytes(expected)
    concurrent = webp_bytes((650, 650), quality=55)
    prepare = photo_prepare._prepare_bytes

    def edit_during_recovery(path: Path, data: bytes) -> bytes:
        output = prepare(path, data)
        source.write_bytes(concurrent)
        return output

    monkeypatch.setattr(photo_prepare, "_prepare_bytes", edit_during_recovery)
    with pytest.raises(PhotoPreparationError, match="changed during"):
        prepare_photos(fixture_book.content_root, fixture_book.data_dir / "photo-manifest.yml")

    assert source.read_bytes() == concurrent
    assert backup.read_bytes() == original


def test_recovery_rechecks_webp_before_removing_backup(
    fixture_book: Project, monkeypatch: pytest.MonkeyPatch
) -> None:
    _recipe, source = recipe_with_webp(fixture_book)
    original = source.read_bytes()
    backup = source.with_name(f".{source.name}.prepare-photos.bak")
    backup.write_bytes(original)
    concurrent = webp_bytes((650, 650), quality=55)
    assert_unchanged = photo_prepare._assert_unchanged

    def edit_before_backup_removal(path: Path, expected: bytes | None, label: str) -> None:
        if label == "image during backup recovery":
            source.write_bytes(concurrent)
        assert_unchanged(path, expected, label)

    monkeypatch.setattr(photo_prepare, "_assert_unchanged", edit_before_backup_removal)
    key = source.relative_to(fixture_book.content_root).as_posix()
    with pytest.raises(PhotoPreparationError, match="changed during"):
        photo_prepare._recover_in_place_backup(source, key, {})

    assert source.read_bytes() == concurrent
    assert backup.read_bytes() == original


def test_recovery_fsyncs_restored_file_before_removing_backup(
    fixture_book: Project, monkeypatch: pytest.MonkeyPatch
) -> None:
    _recipe, source = recipe_with_webp(fixture_book)
    original = webp_bytes((1200, 800), quality=40)
    source.write_bytes(original)
    expected = photo_prepare._prepare_bytes(source, original)
    source.write_bytes(expected)
    backup = source.with_name(f".{source.name}.prepare-photos.bak")
    backup.write_bytes(original)
    events: list[str] = []
    original_fsync = os.fsync
    original_replace = Path.replace
    original_unlink = Path.unlink

    def record_fsync(fd: int) -> None:
        if stat.S_ISDIR(os.fstat(fd).st_mode):
            events.append("directory-fsync")
        original_fsync(fd)

    def record_replace(path: Path, target: Path) -> Path:
        result = original_replace(path, target)
        if target == source:
            events.append("replace")
        return result

    def record_unlink(path: Path, missing_ok: bool = False) -> None:
        if path == backup:
            events.append("backup-unlink")
        original_unlink(path, missing_ok=missing_ok)

    monkeypatch.setattr(os, "fsync", record_fsync)
    monkeypatch.setattr(Path, "replace", record_replace)
    monkeypatch.setattr(Path, "unlink", record_unlink)

    key = source.relative_to(fixture_book.content_root).as_posix()
    photo_prepare._recover_in_place_backup(source, key, {})

    replace_index = events.index("replace")
    fsync_index = events.index("directory-fsync", replace_index + 1)
    assert replace_index < fsync_index < events.index("backup-unlink")
    assert source.read_bytes() == original
    assert not backup.exists()


def test_jpeg_target_and_source_directory_changes_are_fsynced_in_order(
    fixture_book: Project, monkeypatch: pytest.MonkeyPatch
) -> None:
    recipe, source = recipe_with_photo(fixture_book)
    manifest = fixture_book.data_dir / "photo-manifest.yml"
    target = source.with_suffix(".webp")
    events: list[str] = []
    fsync_directory = photo_prepare._fsync_directory
    original_link = os.link
    original_replace = Path.replace
    original_unlink = Path.unlink
    original_write_temp = photo_prepare._write_temp
    source_backups: list[Path] = []

    def capture_source_backup(path: Path, data: bytes) -> Path:
        temp = original_write_temp(path, data)
        if path == source:
            source_backups.append(temp)
        return temp

    def record_fsync(path: Path) -> None:
        if path == source.parent:
            events.append("directory-fsync")
        fsync_directory(path)

    def record_link(source_path: Path, target_path: Path) -> None:
        original_link(source_path, target_path)
        if target_path == target:
            events.append("target-link")

    def record_replace(path: Path, target_path: Path) -> Path:
        result = original_replace(path, target_path)
        if target_path == recipe:
            events.append("recipe-replace")
        elif target_path == manifest:
            events.append("manifest-replace")
        return result

    def record_unlink(path: Path, missing_ok: bool = False) -> None:
        if path == source:
            events.append("source-unlink")
        elif path in source_backups:
            events.append("source-backup-unlink")
        original_unlink(path, missing_ok=missing_ok)

    monkeypatch.setattr(photo_prepare, "_fsync_directory", record_fsync)
    monkeypatch.setattr(os, "link", record_link)
    monkeypatch.setattr(Path, "replace", record_replace)
    monkeypatch.setattr(Path, "unlink", record_unlink)
    monkeypatch.setattr(photo_prepare, "_write_temp", capture_source_backup)

    prepare_photos(fixture_book.content_root, manifest)

    link_index = events.index("target-link")
    target_sync_index = events.index("directory-fsync", link_index + 1)
    recipe_index = events.index("recipe-replace")
    manifest_index = events.index("manifest-replace")
    source_unlink_index = events.index("source-unlink")
    source_sync_index = events.index("directory-fsync", source_unlink_index + 1)
    source_backup_unlink_index = events.index("source-backup-unlink")
    assert (
        link_index
        < target_sync_index
        < recipe_index
        < manifest_index
        < source_unlink_index
        < source_sync_index
        < source_backup_unlink_index
    )


def test_in_place_webp_replace_is_fsynced_before_manifest_commit(
    fixture_book: Project, monkeypatch: pytest.MonkeyPatch
) -> None:
    _recipe, source = recipe_with_webp(fixture_book)
    original = webp_bytes((1200, 800), quality=40)
    source.write_bytes(original)
    manifest = fixture_book.data_dir / "photo-manifest.yml"
    events: list[str] = []
    fsync_directory = photo_prepare._fsync_directory
    original_replace = Path.replace

    def record_fsync(path: Path) -> None:
        if path == source.parent:
            events.append("directory-fsync")
        fsync_directory(path)

    def record_replace(path: Path, target_path: Path) -> Path:
        result = original_replace(path, target_path)
        if target_path == source:
            events.append("webp-replace")
        elif target_path == manifest:
            events.append("manifest-replace")
        return result

    monkeypatch.setattr(photo_prepare, "_fsync_directory", record_fsync)
    monkeypatch.setattr(Path, "replace", record_replace)

    prepare_photos(fixture_book.content_root, manifest)

    replace_index = events.index("webp-replace")
    fsync_index = events.index("directory-fsync", replace_index + 1)
    assert replace_index < fsync_index < events.index("manifest-replace")


def test_prepare_cleans_backup_when_conversion_never_replaced_source(fixture_book: Project) -> None:
    _recipe, source = recipe_with_webp(fixture_book)
    original = source.read_bytes()
    backup = source.with_name(f".{source.name}.prepare-photos.bak")
    backup.write_bytes(original)

    result = prepare_photos(fixture_book.content_root, fixture_book.data_dir / "photo-manifest.yml")

    assert result.converted == 1
    assert not backup.exists()
    assert source.is_file()
    assert source.read_bytes() == original


def test_prepare_cleans_leftover_backup_after_manifest_commit(fixture_book: Project) -> None:
    _recipe, source = recipe_with_webp(fixture_book)
    manifest = fixture_book.data_dir / "photo-manifest.yml"
    prepare_photos(fixture_book.content_root, manifest)
    prepared = source.read_bytes()
    backup = source.with_name(f".{source.name}.prepare-photos.bak")
    backup.write_bytes(webp_bytes((400, 400), quality=85))

    result = prepare_photos(fixture_book.content_root, manifest)

    assert result.converted == 0
    assert result.skipped == 1
    assert source.read_bytes() == prepared
    assert not backup.exists()


def test_prepare_repairs_stale_webp_manifest_hash(fixture_book: Project) -> None:
    _recipe, source = recipe_with_webp(fixture_book)
    manifest = fixture_book.data_dir / "photo-manifest.yml"
    prepare_photos(fixture_book.content_root, manifest)
    previous_bytes = source.read_bytes()
    source.write_bytes(webp_bytes((1000, 700), quality=60))
    stale_bytes = source.read_bytes()
    assert stale_bytes != previous_bytes

    result = prepare_photos(fixture_book.content_root, manifest)

    data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    key = source.relative_to(fixture_book.content_root).as_posix()
    assert result.converted == 1
    assert source.read_bytes() != stale_bytes
    assert data["photos"][key]["sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()


def test_in_place_webp_failure_restores_original_and_manifest(
    fixture_book: Project, monkeypatch: pytest.MonkeyPatch
) -> None:
    _recipe, source = recipe_with_webp(fixture_book)
    original = source.read_bytes()
    manifest = fixture_book.data_dir / "photo-manifest.yml"
    atomic_replace = photo_prepare._atomic_replace

    def fail_for_manifest(path: Path, data: bytes) -> None:
        if path == manifest:
            raise OSError("synthetic manifest write failure")
        atomic_replace(path, data)

    monkeypatch.setattr(photo_prepare, "_atomic_replace", fail_for_manifest)
    with pytest.raises(OSError, match="synthetic manifest write failure"):
        prepare_photos(fixture_book.content_root, manifest)

    assert source.read_bytes() == original
    assert not manifest.exists()


def test_existing_manifested_target_is_not_assumed_to_match_jpeg(fixture_book: Project) -> None:
    recipe, source = recipe_with_photo(fixture_book)
    original_source = source.read_bytes()
    manifest = fixture_book.data_dir / "photo-manifest.yml"
    prepare_photos(fixture_book.content_root, manifest)
    target = source.with_suffix(".webp")
    recipe.write_text(
        recipe.read_text(encoding="utf-8").replace(
            "image: test-citrus-wings.webp", "image: test-citrus-wings.jpg"
        ),
        encoding="utf-8",
    )
    source.write_bytes(original_source)
    recipe_before = recipe.read_bytes()
    target_before = target.read_bytes()

    with pytest.raises(PhotoPreparationError, match="already exists"):
        prepare_photos(fixture_book.content_root, manifest)

    assert recipe.read_bytes() == recipe_before
    assert source.read_bytes() == original_source
    assert target.read_bytes() == target_before


@pytest.mark.parametrize("changed_file", ["recipe", "manifest", "source"])
def test_concurrent_edits_before_commit_are_not_overwritten(
    fixture_book: Project, monkeypatch: pytest.MonkeyPatch, changed_file: str
) -> None:
    recipe, source = recipe_with_photo(fixture_book)
    recipe_before = recipe.read_bytes()
    source_before = source.read_bytes()
    manifest = fixture_book.data_dir / "photo-manifest.yml"
    manifest_before = b"photos: {}\n"
    manifest.write_bytes(manifest_before)
    write_temp = photo_prepare._write_temp
    changed_bytes = {
        "recipe": recipe_before + b"\n# concurrent recipe edit\n",
        "manifest": b"# concurrent manifest edit\nphotos: {}\n",
        "source": jpeg_bytes((900, 600)),
    }[changed_file]

    def edit_after_staging(path: Path, data: bytes) -> Path:
        temp = write_temp(path, data)
        if path == source.with_suffix(".webp"):
            destination = {
                "recipe": recipe,
                "manifest": manifest,
                "source": source,
            }[changed_file]
            destination.write_bytes(changed_bytes)
        return temp

    monkeypatch.setattr(photo_prepare, "_write_temp", edit_after_staging)
    with pytest.raises(PhotoPreparationError, match="changed during"):
        prepare_photos(fixture_book.content_root, manifest)

    if changed_file == "recipe":
        assert recipe.read_bytes() == changed_bytes
        assert source.read_bytes() == source_before
    elif changed_file == "manifest":
        assert manifest.read_bytes() == changed_bytes
        assert recipe.read_bytes() == recipe_before
        assert source.read_bytes() == source_before
    else:
        assert source.read_bytes() == changed_bytes
        assert recipe.read_bytes() == recipe_before
    assert not source.with_suffix(".webp").exists()


def test_source_changed_before_removal_is_preserved_and_metadata_rolls_back(
    fixture_book: Project, monkeypatch: pytest.MonkeyPatch
) -> None:
    recipe, source = recipe_with_photo(fixture_book)
    recipe_before = recipe.read_bytes()
    manifest = fixture_book.data_dir / "photo-manifest.yml"
    concurrent_source = jpeg_bytes((1000, 700))
    atomic_replace = photo_prepare._atomic_replace

    def edit_source_after_manifest(path: Path, data: bytes) -> None:
        atomic_replace(path, data)
        if path == manifest:
            source.write_bytes(concurrent_source)

    monkeypatch.setattr(photo_prepare, "_atomic_replace", edit_source_after_manifest)
    with pytest.raises(PhotoPreparationError, match="source photo before removal changed"):
        prepare_photos(fixture_book.content_root, manifest)

    assert source.read_bytes() == concurrent_source
    assert recipe.read_bytes() == recipe_before
    assert not manifest.exists()
    assert not source.with_suffix(".webp").exists()


def test_partial_source_removal_failure_restores_every_original(
    fixture_book: Project, monkeypatch: pytest.MonkeyPatch
) -> None:
    recipe_one, source_one = recipe_with_photo(fixture_book)
    original_one = source_one.read_bytes()
    recipe_two = recipe_one.with_name("zz-test-citrus-wings-second.md")
    recipe_two_before = recipe_one.read_bytes().replace(
        b"image: test-citrus-wings.jpg", b"image: second.jpg"
    )
    recipe_two.write_bytes(recipe_two_before)
    source_two = source_one.with_name("second.jpg")
    original_two = jpeg_bytes((1100, 750))
    source_two.write_bytes(original_two)
    recipe_one_before = recipe_one.read_bytes()
    manifest = fixture_book.data_dir / "photo-manifest.yml"
    original_unlink = Path.unlink

    def fail_second_source_unlink(path: Path, missing_ok: bool = False) -> None:
        if path == source_two:
            raise OSError("synthetic second source removal failure")
        original_unlink(path, missing_ok=missing_ok)

    monkeypatch.setattr(Path, "unlink", fail_second_source_unlink)
    with pytest.raises(OSError, match="second source removal failure"):
        prepare_photos(fixture_book.content_root, manifest)

    assert source_one.read_bytes() == original_one
    assert source_two.read_bytes() == original_two
    assert recipe_one.read_bytes() == recipe_one_before
    assert recipe_two.read_bytes() == recipe_two_before
    assert not manifest.exists()
    assert not source_one.with_suffix(".webp").exists()
    assert not source_two.with_suffix(".webp").exists()
    assert not list(source_one.parent.glob(".*.tmp"))


def test_failed_original_restore_reports_and_keeps_backup(
    fixture_book: Project, monkeypatch: pytest.MonkeyPatch
) -> None:
    recipe_one, source_one = recipe_with_photo(fixture_book)
    original_one = source_one.read_bytes()
    recipe_two = recipe_one.with_name("zz-test-citrus-wings-second.md")
    recipe_two.write_bytes(
        recipe_one.read_bytes().replace(b"image: test-citrus-wings.jpg", b"image: second.jpg")
    )
    source_two = source_one.with_name("second.jpg")
    source_two.write_bytes(jpeg_bytes((1100, 750)))
    original_unlink = Path.unlink
    original_link = os.link
    original_write_temp = photo_prepare._write_temp
    source_backup: list[Path] = []

    def capture_temp(path: Path, data: bytes) -> Path:
        temp = original_write_temp(path, data)
        if path == source_one and data == original_one:
            source_backup.append(temp)
        return temp

    def fail_unlink(path: Path, missing_ok: bool = False) -> None:
        if path == source_two:
            raise OSError("synthetic second source removal failure")
        original_unlink(path, missing_ok=missing_ok)

    def fail_restore(source: Path, target: Path) -> None:
        if target == source_one:
            raise OSError("synthetic original restore failure")
        original_link(source, target)

    monkeypatch.setattr(photo_prepare, "_write_temp", capture_temp)
    monkeypatch.setattr(Path, "unlink", fail_unlink)
    monkeypatch.setattr(os, "link", fail_restore)

    with pytest.raises(PhotoPreparationError, match="backup at") as error:
        prepare_photos(fixture_book.content_root, fixture_book.data_dir / "photo-manifest.yml")

    assert len(source_backup) == 1
    assert str(source_backup[0]) in str(error.value)
    assert source_backup[0].read_bytes() == original_one


def test_rollback_does_not_overwrite_concurrent_recipe_edit(
    fixture_book: Project, monkeypatch: pytest.MonkeyPatch
) -> None:
    recipe, source = recipe_with_photo(fixture_book)
    manifest = fixture_book.data_dir / "photo-manifest.yml"
    atomic_replace = photo_prepare._atomic_replace
    concurrent_recipe = b"concurrent editor owns this content\n"

    def edit_then_fail_manifest(path: Path, data: bytes) -> None:
        if path == manifest:
            recipe.write_bytes(concurrent_recipe)
            raise OSError("synthetic manifest failure")
        atomic_replace(path, data)

    monkeypatch.setattr(photo_prepare, "_atomic_replace", edit_then_fail_manifest)
    with pytest.raises(OSError, match="synthetic manifest failure"):
        prepare_photos(fixture_book.content_root, manifest)

    assert recipe.read_bytes() == concurrent_recipe
    assert source.exists()
    assert not source.with_suffix(".webp").exists()


def test_rollback_does_not_overwrite_concurrent_manifest_edit(
    fixture_book: Project, monkeypatch: pytest.MonkeyPatch
) -> None:
    recipe, source = recipe_with_photo(fixture_book)
    recipe_before = recipe.read_bytes()
    manifest = fixture_book.data_dir / "photo-manifest.yml"
    atomic_replace = photo_prepare._atomic_replace
    concurrent_manifest = b"# concurrent editor owns this manifest\nphotos: {}\n"

    def edit_after_manifest_write(path: Path, data: bytes) -> None:
        if path == manifest:
            atomic_replace(path, data)
            manifest.write_bytes(concurrent_manifest)
            raise OSError("synthetic post-write failure")
        atomic_replace(path, data)

    monkeypatch.setattr(photo_prepare, "_atomic_replace", edit_after_manifest_write)
    with pytest.raises(OSError, match="synthetic post-write failure"):
        prepare_photos(fixture_book.content_root, manifest)

    assert manifest.read_bytes() == concurrent_manifest
    assert recipe.read_bytes() == recipe_before
    assert source.exists()
    assert not source.with_suffix(".webp").exists()


def test_recipe_subdirectory_reference_is_preserved(fixture_book: Project) -> None:
    recipe = fixture_book.content_root / RECIPE
    recipe.parent.joinpath("assets").mkdir()
    recipe.write_text(
        recipe.read_text(encoding="utf-8").replace(
            "status: published\n",
            "status: published\nimage: assets/wings.jpg\nphoto_credit: Synthetic credit\n",
        ),
        encoding="utf-8",
    )
    source = recipe.parent / "assets" / "wings.jpg"
    source.write_bytes(jpeg_bytes((900, 600)))

    prepare_photos(fixture_book.content_root, fixture_book.data_dir / "photo-manifest.yml")

    assert "image: assets/wings.webp" in recipe.read_text(encoding="utf-8")
    assert (recipe.parent / "assets" / "wings.webp").is_file()
    assert not source.exists()


def test_prepare_preserves_alpha_and_respects_size_limits(fixture_book: Project) -> None:
    recipe = fixture_book.content_root / RECIPE
    recipe.write_text(
        recipe.read_text(encoding="utf-8").replace(
            "status: published\n",
            "status: published\nimage: alpha.png\nphoto_credit: Synthetic credit\n",
        ),
        encoding="utf-8",
    )
    source = recipe.parent / "alpha.png"
    image = Image.new("RGBA", (2400, 1200), (20, 80, 120, 0))
    image.paste((255, 0, 0, 255), (10, 10, 110, 110))
    image.save(source, format="PNG")

    prepare_photos(fixture_book.content_root, fixture_book.data_dir / "photo-manifest.yml")

    target = source.with_suffix(".webp")
    with Image.open(target) as output:
        assert output.mode == "RGBA"
        assert max(output.size) <= 2048
        assert min(output.size) >= 500
        transparent = output.getpixel((0, 0))
        opaque = output.getpixel((50, 50))
        assert isinstance(transparent, tuple) and transparent[3] == 0
        assert isinstance(opaque, tuple) and opaque[3] > 240
        assert target.stat().st_size <= 1024 * 1024


def test_prepare_preserves_rgb_icc_profile(fixture_book: Project) -> None:
    recipe = fixture_book.content_root / RECIPE
    recipe.write_text(
        recipe.read_text(encoding="utf-8").replace(
            "status: published\n",
            "status: published\nimage: profiled.png\nphoto_credit: Synthetic credit\n",
        ),
        encoding="utf-8",
    )
    source = recipe.parent / "profiled.png"
    profile = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    Image.new("RGB", (800, 600), "green").save(source, format="PNG", icc_profile=profile)

    prepare_photos(fixture_book.content_root, fixture_book.data_dir / "photo-manifest.yml")

    with Image.open(source.with_suffix(".webp")) as output:
        assert output.info["icc_profile"] == profile


def test_prepare_shrinks_detailed_photo_to_size_limit(fixture_book: Project) -> None:
    recipe = fixture_book.content_root / RECIPE
    recipe.write_text(
        recipe.read_text(encoding="utf-8").replace(
            "status: published\n",
            "status: published\nimage: detailed.png\nphoto_credit: Synthetic credit\n",
        ),
        encoding="utf-8",
    )
    source = recipe.parent / "detailed.png"
    generator = random.Random(3)
    image = Image.frombytes(
        "RGB", (2048, 1024), bytes(generator.randrange(256) for _ in range(2048 * 1024 * 3))
    )
    image.save(source, format="PNG")

    prepare_photos(fixture_book.content_root, fixture_book.data_dir / "photo-manifest.yml")

    with Image.open(source.with_suffix(".webp")) as output:
        assert max(output.size) <= 2048
        assert min(output.size) >= 500
        target = source.with_suffix(".webp")
        assert target.stat().st_size <= 1024 * 1024


@pytest.mark.parametrize("bad_data", [b"not an image", jpeg_bytes((600, 400))[:12]])
def test_corrupt_source_fails_without_changing_recipe_or_losing_source(
    fixture_book: Project, bad_data: bytes
) -> None:
    recipe, source = recipe_with_photo(fixture_book)
    source.write_bytes(bad_data)
    recipe_before = recipe.read_bytes()

    with pytest.raises(PhotoPreparationError, match=r"test-citrus-wings\.jpg"):
        prepare_photos(fixture_book.content_root, fixture_book.data_dir / "photo-manifest.yml")

    assert source.read_bytes() == bad_data
    assert recipe.read_bytes() == recipe_before
    assert not source.with_suffix(".webp").exists()


def test_existing_untracked_destination_is_never_overwritten(fixture_book: Project) -> None:
    _recipe, source = recipe_with_photo(fixture_book)
    destination = source.with_suffix(".webp")
    destination.write_bytes(b"unrelated file")

    with pytest.raises(PhotoPreparationError, match="already exists"):
        prepare_photos(fixture_book.content_root, fixture_book.data_dir / "photo-manifest.yml")

    assert source.exists()
    assert destination.read_bytes() == b"unrelated file"


def test_missing_referenced_source_fails_without_changing_recipe(fixture_book: Project) -> None:
    recipe = fixture_book.content_root / RECIPE
    recipe.write_text(
        recipe.read_text(encoding="utf-8").replace(
            "status: published\n",
            "status: published\nimage: missing.jpg\nphoto_credit: Synthetic credit\n",
        ),
        encoding="utf-8",
    )
    recipe_before = recipe.read_bytes()

    with pytest.raises(PhotoPreparationError, match=r"missing\.jpg"):
        prepare_photos(fixture_book.content_root, fixture_book.data_dir / "photo-manifest.yml")

    assert recipe.read_bytes() == recipe_before


def test_manifest_write_failure_rolls_back_and_keeps_original(
    fixture_book: Project, monkeypatch: pytest.MonkeyPatch
) -> None:
    recipe, source = recipe_with_photo(fixture_book)
    recipe_before = recipe.read_bytes()
    manifest = fixture_book.data_dir / "photo-manifest.yml"
    atomic_replace = photo_prepare._atomic_replace

    def fail_for_manifest(path: Path, data: bytes) -> None:
        if path == manifest:
            raise OSError("synthetic manifest write failure")
        atomic_replace(path, data)

    monkeypatch.setattr(photo_prepare, "_atomic_replace", fail_for_manifest)
    with pytest.raises(OSError, match="synthetic manifest write failure"):
        prepare_photos(fixture_book.content_root, manifest)

    assert source.is_file()
    assert recipe.read_bytes() == recipe_before
    assert not source.with_suffix(".webp").exists()
    assert not manifest.exists()


def test_failed_recipe_rollback_reports_and_keeps_recovery_backup(
    fixture_book: Project, monkeypatch: pytest.MonkeyPatch
) -> None:
    recipe, source = recipe_with_photo(fixture_book)
    recipe_before = recipe.read_bytes()
    manifest = fixture_book.data_dir / "photo-manifest.yml"
    atomic_replace = photo_prepare._atomic_replace
    write_temp = photo_prepare._write_temp
    recipe_backup: list[Path] = []

    def capture_recipe_backup(path: Path, data: bytes) -> Path:
        temp = write_temp(path, data)
        if path == recipe and data == recipe_before:
            recipe_backup.append(temp)
        return temp

    def fail_manifest_and_rollback(path: Path, data: bytes) -> None:
        if path == manifest:
            raise OSError("synthetic manifest write failure")
        if path == recipe and data == recipe_before:
            raise OSError("synthetic recipe rollback failure")
        atomic_replace(path, data)

    monkeypatch.setattr(photo_prepare, "_write_temp", capture_recipe_backup)
    monkeypatch.setattr(photo_prepare, "_atomic_replace", fail_manifest_and_rollback)

    with pytest.raises(PhotoPreparationError, match="recovery backup") as error:
        prepare_photos(fixture_book.content_root, manifest)

    assert len(recipe_backup) == 1
    assert str(recipe_backup[0]) in str(error.value)
    assert recipe_backup[0].read_bytes() == recipe_before
    assert source.is_file()


def test_cli_prepare_photos_uses_project_paths(fixture_book: Project) -> None:
    _recipe, source = recipe_with_photo(fixture_book)
    result = CliRunner().invoke(
        app,
        [
            "--root",
            str(fixture_book.root),
            "--content",
            str(fixture_book.content_root),
            "prepare-photos",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "1 prepared" in result.output
    assert source.with_suffix(".webp").is_file()
