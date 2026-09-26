"""Filesystem layout of a book project.

Two roots are distinguished:

* ``root``: the repository (templates/, styles/, generated/, dist/).
* ``content_root``: authored content + data (recipes/, components/, menus/,
  data/, book/). It defaults to ``root``; tests point it at a fixture tree so
  fixtures are never discovered by the production book.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from nfl_book.errors import BookError

MARKER = Path("data") / "nfl.yml"


@dataclass(frozen=True)
class Project:
    root: Path
    content_root: Path
    generated_dir: Path
    dist_dir: Path

    @classmethod
    def create(
        cls,
        root: Path,
        content_root: Path | None = None,
        generated_dir: Path | None = None,
        dist_dir: Path | None = None,
    ) -> Project:
        root = root.resolve()
        return cls(
            root=root,
            content_root=(content_root or root).resolve(),
            generated_dir=(generated_dir or root / "generated").resolve(),
            dist_dir=(dist_dir or root / "dist").resolve(),
        )

    @classmethod
    def discover(cls, start: Path | None = None) -> Project:
        here = (start or Path.cwd()).resolve()
        for candidate in (here, *here.parents):
            if (candidate / MARKER).is_file() and (candidate / "templates").is_dir():
                return cls.create(candidate)
        raise BookError(f"No book project found at or above {here} (looked for {MARKER}).")

    # Authored content ------------------------------------------------------
    @property
    def recipes_dir(self) -> Path:
        return self.content_root / "recipes"

    @property
    def components_dir(self) -> Path:
        return self.content_root / "components"

    @property
    def game_day_dir(self) -> Path:
        return self.content_root / "menus" / "game-day"

    @property
    def dishoffs_dir(self) -> Path:
        return self.content_root / "menus" / "divisions"

    @property
    def data_dir(self) -> Path:
        return self.content_root / "data"

    @property
    def frontmatter_dir(self) -> Path:
        return self.content_root / "book" / "frontmatter"

    @property
    def shortlinks_file(self) -> Path:
        return self.data_dir / "shortlinks.yml"

    # Presentation ------------------------------------------------------------
    @property
    def templates_dir(self) -> Path:
        return self.root / "templates"

    @property
    def styles_dir(self) -> Path:
        return self.root / "styles"

    # Disposable output ---------------------------------------------------------
    @property
    def book_build_dir(self) -> Path:
        return self.generated_dir / "book"

    @property
    def preview_build_dir(self) -> Path:
        return self.generated_dir / "preview"

    @property
    def qr_dir(self) -> Path:
        return self.generated_dir / "qr"

    @property
    def pagemap_file(self) -> Path:
        return self.generated_dir / "pagemap.json"
