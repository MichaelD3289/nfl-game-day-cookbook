"""Shared fixtures.

Tests never touch production content: the synthetic book under
``tests/fixtures/sample-book`` is copied to a temporary directory together
with the production configuration files (league, indexes, kinds, ...), and a
:class:`Project` is pointed at that copy.
"""

from __future__ import annotations

import shutil
from collections.abc import Callable
from pathlib import Path

import pytest

from nfl_book.config import Settings, load_settings
from nfl_book.errors import Diagnostics
from nfl_book.project import Project

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURE_BOOK = REPO_ROOT / "tests" / "fixtures" / "sample-book"
CONFIG_FILES = ("book.yml", "nfl.yml", "indexes.yml", "menu-types.yml", "component-kinds.yml")


def make_project(content: Path) -> Project:
    return Project.create(
        REPO_ROOT,
        content_root=content,
        generated_dir=content / "generated",
        dist_dir=content / "dist",
    )


def copy_config(target: Path) -> None:
    (target / "data").mkdir(parents=True, exist_ok=True)
    for name in CONFIG_FILES:
        shutil.copy2(REPO_ROOT / "data" / name, target / "data" / name)


@pytest.fixture
def fixture_book(tmp_path: Path) -> Project:
    """A writable copy of the synthetic sample book."""
    content = tmp_path / "book"
    shutil.copytree(FIXTURE_BOOK, content)
    copy_config(content)
    return make_project(content)


@pytest.fixture
def empty_book(tmp_path: Path) -> Project:
    """Production configuration with no content at all."""
    content = tmp_path / "empty"
    copy_config(content)
    return make_project(content)


@pytest.fixture
def settings(empty_book: Project) -> Settings:
    return load_settings(empty_book)


@pytest.fixture
def write(fixture_book: Project) -> Callable[[str, str], Path]:
    """Write a file relative to the fixture book's content root."""

    def _write(relative: str, text: str) -> Path:
        path = fixture_book.content_root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    return _write


@pytest.fixture
def diags() -> Diagnostics:
    return Diagnostics()
