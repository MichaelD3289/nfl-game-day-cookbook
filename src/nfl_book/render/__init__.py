"""Rendering: resolved model -> page specs -> QMD -> (Quarto) -> PDF."""

from nfl_book.render.assemble import Assembled, assemble
from nfl_book.render.env import make_env
from nfl_book.render.pages import Media, PageSpec, build_pages, component_page, recipe_page

__all__ = [
    "Assembled",
    "Media",
    "PageSpec",
    "assemble",
    "build_pages",
    "component_page",
    "make_env",
    "recipe_page",
]
