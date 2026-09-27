"""Write page specs to QMD files plus a manifest of expected anchors."""

from __future__ import annotations

import json
import shutil
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment

from nfl_book.errors import BookError
from nfl_book.render.pages import PageSpec

MANIFEST = "manifest.json"


@dataclass(frozen=True)
class Assembled:
    build_dir: Path
    document: Path
    manifest: Path


def write_if_changed(path: Path, text: str) -> None:
    if path.is_file() and path.read_text(encoding="utf-8") == text:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def front_matter(
    title: str,
    paper: str,
    header_includes: Sequence[str],
    preamble: str,
    *,
    latex_auto_install: bool | None = None,
) -> str:
    """Quarto document options. Generated, never authored by hand.

    No ``title`` key: Quarto would emit ``\\maketitle``; the cover page is ours.
    """
    headers: list[Any] = [{"text": preamble}] if preamble else []
    headers.extend(header_includes)
    headers.append({"text": f"\\AtBeginDocument{{\\hypersetup{{pdftitle={{{title}}}}}}}"})
    data: dict[str, Any] = {
        "format": {
            "pdf": {
                "pdf-engine": "pdflatex",
                "documentclass": "article",
                "papersize": paper,
                "toc": False,
                "number-sections": False,
                "keep-tex": True,
                "latex-clean": False,
                "include-in-header": headers,
            }
        },
    }
    if latex_auto_install is not None:
        data["format"]["pdf"]["latex-auto-install"] = latex_auto_install
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=1000).strip()


def copy_styles(styles_dir: Path, build_dir: Path) -> list[str]:
    target = build_dir / "styles"
    target.mkdir(parents=True, exist_ok=True)
    includes = []
    for name in ("theme.tex", "book.tex"):
        source = styles_dir / name
        if not source.is_file():
            raise BookError(f"missing style file {source}")
        write_if_changed(target / name, source.read_text(encoding="utf-8"))
        includes.append(f"styles/{name}")
    return includes


def assemble(
    env: Environment,
    specs: Sequence[PageSpec],
    build_dir: Path,
    *,
    title: str,
    paper: str,
    styles_dir: Path,
    preamble: str = "",
) -> Assembled:
    """Render every spec to ``pages/NNN-slug.qmd`` and the ``book.qmd`` that includes them."""
    pages_dir = build_dir / "pages"
    if pages_dir.exists():
        shutil.rmtree(pages_dir)  # stale pages must never leak into a build
    pages_dir.mkdir(parents=True)
    includes = copy_styles(styles_dir, build_dir)

    names = []
    for number, spec in enumerate(specs, start=1):
        name = f"pages/{number:03d}-{spec.slug}.qmd"
        text = env.get_template(spec.template).render(**spec.context)
        write_if_changed(build_dir / name, text)
        names.append(name)

    document = build_dir / "book.qmd"
    write_if_changed(
        document,
        env.get_template("book.qmd.j2").render(
            front_matter=front_matter(title, paper, includes, preamble), pages=names
        ),
    )
    manifest = build_dir / MANIFEST
    write_if_changed(
        manifest,
        json.dumps(
            {
                "pages": [
                    {"file": n, "anchors": list(s.anchors), "spans": [list(p) for p in s.spans]}
                    for n, s in zip(names, specs, strict=True)
                ]
            },
            indent=2,
        )
        + "\n",
    )
    return Assembled(build_dir, document, manifest)
