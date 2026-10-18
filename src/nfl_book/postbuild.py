"""Read label -> page facts back out of the compiled PDF.

LaTeX decides every page number. This stage only *observes* the result:
it records the page map used by previews and checks that each expected
anchor exists and that single-page items did not overflow.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader

from nfl_book.errors import Diagnostics

LABEL_PREFIXES = ("recipe:", "component:", "division:", "menu:", "team:", "section:", "index:")


def read_pagemap(pdf: Path) -> dict[str, int]:
    """Named destinations for known labels -> physical 1-based page numbers."""
    reader = PdfReader(pdf)
    pagemap = {}
    for name, destination in reader.named_destinations.items():
        if name.startswith(LABEL_PREFIXES):
            page = reader.get_destination_page_number(destination)
            if page is not None and page >= 0:
                pagemap[name] = page + 1
    return dict(sorted(pagemap.items()))


def write_pagemap(pagemap: dict[str, int], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(pagemap, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_pagemap(path: Path) -> dict[str, int]:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return {k: int(v) for k, v in data.items()} if isinstance(data, dict) else {}


@dataclass(frozen=True)
class Overflow:
    start: str
    end: str
    first: int
    last: int


def check_manifest(
    manifest: Path, pagemap: dict[str, int], diags: Diagnostics, *, strict: bool, max_pages: int = 1
) -> list[Overflow]:
    """Check observed spans against the allowed physical sides per item."""
    data = json.loads(manifest.read_text(encoding="utf-8"))
    overflows = []
    for page in data["pages"]:
        source = Path(page["source"]) if "source" in page else manifest.parent / page["file"]
        for anchor in page["anchors"]:
            if anchor not in pagemap:
                diags.error("anchor", f"label {anchor!r} is missing from the compiled PDF", source)
        for start, end in page["spans"]:
            if (
                start in pagemap
                and end in pagemap
                and pagemap[end] - pagemap[start] + 1 > max_pages
            ):
                overflow = Overflow(start, end, pagemap[start], pagemap[end])
                overflows.append(overflow)
                limit = "page" if max_pages == 1 else f"{max_pages}-page limit"
                message = (
                    f"{start} overflows its {limit} "
                    f"(pages {overflow.first}-{overflow.last}); "
                    "shorten the content or split it"
                )
                if strict:
                    diags.error("overflow", message, source)
                else:
                    diags.warning("overflow", message, source)
    return overflows
