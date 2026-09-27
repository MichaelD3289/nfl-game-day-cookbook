"""Check local HTML links, fragment targets and assets without using the network."""

from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from nfl_book.catalog import CATALOG_FILE
from nfl_book.errors import Diagnostics

PRINT_PAGE_ATTRIBUTES = ("data-print-pages", "data-print-components")


class _Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if data.get("id"):
            self.ids.add(str(data["id"]))
        for attribute in ("href", "src"):
            if data.get(attribute):
                self.links.append(str(data[attribute]))
        # Pages print.js fetches to print with a recipe or menu are links too.
        for attribute in PRINT_PAGE_ATTRIBUTES:
            self.links.extend((data.get(attribute) or "").split())


def check_site(root: Path, diags: Diagnostics) -> None:
    root = root.resolve()
    pages = {}
    for page in root.rglob("*.html"):
        parsed = _Links()
        parsed.feed(page.read_text(encoding="utf-8"))
        pages[page] = parsed
    for page, parsed in pages.items():
        for href in set(parsed.links):
            url = urlsplit(href)
            if url.scheme or url.netloc:
                continue
            if url.path.startswith("/"):
                diags.error(
                    "website-link", f"Root-relative link breaks project hosting: {href}", page
                )
                continue
            target = (page.parent / unquote(url.path)).resolve() if url.path else page
            if target.is_dir():
                target /= "index.html"
            if not target.is_relative_to(root) or not target.is_file():
                diags.error("website-link", f"Missing local target: {href}", page)
            elif (
                url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids
            ):
                diags.error("website-link", f"Missing fragment: {href}", page)
    _check_catalog(root, diags)


def _check_catalog(root: Path, diags: Diagnostics) -> None:
    """Every recipe page and photo named in ``recipes.json`` must ship with the site."""
    path = root / CATALOG_FILE
    if not path.is_file():
        return
    try:
        catalog = json.loads(path.read_text(encoding="utf-8"))
        recipes = catalog["recipes"]
        targets = [r["url"] for r in recipes] + [r["photo"] for r in recipes if r.get("photo")]
    except (ValueError, KeyError, TypeError) as error:
        diags.error("website-link", f"Invalid recipe catalog: {error}", path)
        return
    for target in targets:
        file = (root / unquote(str(target))).resolve()
        if not file.is_relative_to(root) or not file.is_file():
            diags.error("website-link", f"Missing catalog target: {target}", path)
