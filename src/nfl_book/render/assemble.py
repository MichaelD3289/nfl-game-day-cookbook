"""Write page specs to QMD files plus a manifest of expected anchors."""

from __future__ import annotations

import json
import shutil
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment

from nfl_book.errors import Diagnostics, ValidationFailed
from nfl_book.render.pages import PageSpec
from nfl_book.render.views import CardView, view_fields

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


@dataclass(frozen=True)
class Layout:
    """What differs between print targets: file names, styles and front matter."""

    document: str = "book.qmd"
    styles: tuple[str, ...] = ("theme.tex", "book.tex")
    numbered: bool = True  # pages/NNN-slug.qmd, else pages/slug.qmd
    latex_auto_install: bool | None = None
    extra_styles: Mapping[str, str] = field(default_factory=dict)  # generated, name -> text


def copy_styles(
    styles_dir: Path, build_dir: Path, names: Sequence[str], diagnostics: Diagnostics
) -> list[str]:
    target = build_dir / "styles"
    target.mkdir(parents=True, exist_ok=True)
    includes = []
    for name in names:
        source = styles_dir / name
        try:
            text = source.read_text(encoding="utf-8")
        except OSError as exc:
            diagnostics.error("style", f"cannot read style file: {exc}", source)
            continue
        write_if_changed(target / name, text)
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
    diagnostics: Diagnostics,
    preamble: str = "",
    layout: Layout | None = None,
) -> Assembled:
    """Render every spec to ``pages/NNN-slug.qmd`` and the ``book.qmd`` that includes them."""
    layout = layout or Layout()
    pages_dir = build_dir / "pages"
    if pages_dir.exists():
        shutil.rmtree(pages_dir)  # stale pages must never leak into a build
    pages_dir.mkdir(parents=True)
    includes = copy_styles(styles_dir, build_dir, layout.styles, diagnostics)
    if not diagnostics.ok:
        raise ValidationFailed(diagnostics)
    for name, text in layout.extra_styles.items():
        write_if_changed(build_dir / "styles" / name, text)
        includes.append(f"styles/{name}")

    names = []
    for number, spec in enumerate(specs, start=1):
        name = (
            f"pages/{number:03d}-{spec.slug}.qmd" if layout.numbered else f"pages/{spec.slug}.qmd"
        )
        text = env.get_template(spec.template).render(**view_fields(spec.view))
        write_if_changed(build_dir / name, text)
        names.append(name)

    document = build_dir / layout.document
    write_if_changed(
        document,
        env.get_template("book.qmd.j2").render(
            front_matter=front_matter(
                title,
                paper,
                includes,
                preamble,
                latex_auto_install=layout.latex_auto_install,
            ),
            pages=names,
        ),
    )
    manifest = build_dir / MANIFEST
    write_if_changed(
        manifest,
        json.dumps(
            {
                "pages": [
                    {
                        "file": n,
                        **({"source": s.view.recipe_file} if isinstance(s.view, CardView) else {}),
                        # Labels LaTeX must define: the anchors, then where each span ends.
                        "anchors": [*s.anchors, *(end for _, end in s.spans)],
                        "spans": [list(p) for p in s.spans],
                    }
                    for n, s in zip(names, specs, strict=True)
                ]
            },
            indent=2,
        )
        + "\n",
    )
    return Assembled(build_dir, document, manifest)
