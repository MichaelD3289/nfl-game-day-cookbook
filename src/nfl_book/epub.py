"""Independent reflowable EPUB generation from the published book model."""

import re
import shutil
import subprocess
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from PIL import Image, ImageDraw, ImageFont

from nfl_book.digital import prepare_pages
from nfl_book.epub_check import check_epub
from nfl_book.errors import Diagnostics, ValidationFailed
from nfl_book.project import Project
from nfl_book.publishing import EPUB_FILENAME, EPUB_IDENTIFIER
from nfl_book.references import html_id
from nfl_book.render.pages import PageSpec, check_web_links
from nfl_book.resolve import BookModel

__all__ = ["EPUB_FILENAME", "EpubResult", "build_epub"]

# 1:1.6 is the portrait ratio e-book stores and reading apps expect for covers.
COVER_SIZE = (1600, 2560)
COVER_NAVY = (25, 79, 112)  # --book-navy in styles/website.css
COVER_PHOTOS = 9
RIGHTS = (
    "Software is MIT-licensed; original cookbook content is CC BY 4.0. Third-party "
    "text and images keep their own rights and credits."
)


@dataclass(frozen=True)
class EpubResult:
    document: Path
    epub: Path | None
    diagnostics: Diagnostics


def _md(value: str) -> str:
    """Escape plain text used in Markdown (rich authored body text passes through)."""
    return re.sub(r"([\\`*_{}\[\]<>#|])", r"\\\1", value)


def _prose(value: str) -> str:
    """Authored cover text without its print-only LaTeX."""
    value = value.replace(r"`\QMark{}\ `{=latex}", "**Q** ")
    return re.sub(r"```\{=latex\}\n.*?\n```", "", value, flags=re.DOTALL)


def _site_name(url: str) -> str:
    """``https://www.example.com/a/b`` -> ``example.com``: link text for an untitled source."""
    host = urlsplit(url).hostname or url
    return host.removeprefix("www.")


def _author(project: Project) -> str:
    metadata = tomllib.loads((project.root / "pyproject.toml").read_text())["project"]
    names = [a["name"] for a in metadata.get("authors", []) if a.get("name")]
    return " and ".join(names) or "NFL Game Day Cookbook contributors"


def _cover(path: Path, context: dict[str, Any], photos: list[Path]) -> None:
    """A text-and-photo cover: the title block above a grid of dish photos."""
    width, height = COVER_SIZE
    image = Image.new("RGB", COVER_SIZE, COVER_NAVY)
    draw = ImageDraw.Draw(image)
    y: float = 190
    for text, size in (
        (context["title"], 190),
        (context["subtitle"], 84),
        (context["tagline"], 58),
    ):
        if not text:
            continue
        font = ImageFont.load_default(size=size)
        left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
        while right - left > width - 200 and size > 30:  # shrink long lines to fit
            size -= 6
            font = ImageFont.load_default(size=size)
            left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
        draw.text(((width - (right - left)) / 2 - left, y - top), text, fill="white", font=font)
        y += bottom - top + size // 2
    grid = photos[:COVER_PHOTOS]
    if grid:
        gap, margin = 24, 120
        cell = (width - 2 * margin - 2 * gap) // 3
        top_edge = int(max(y + 120, height - margin - 3 * cell - 2 * gap))
        for n, photo in enumerate(grid):
            with Image.open(photo) as source:
                tile = source.convert("RGB").resize((cell, cell))
            image.paste(tile, (margin + (n % 3) * (cell + gap), top_edge + (n // 3) * (cell + gap)))
    image.save(path, "JPEG", quality=85, progressive=True)


def _order(pages: list[PageSpec]) -> list[PageSpec]:
    """Book order for reading on a screen: the browsing indexes go at the back."""
    indexes = [p for p in pages if p.template == "index.qmd.j2"]
    return [p for p in pages if p.template != "index.qmd.j2"] + indexes


def build_epub(project: Project, *, render: bool = True) -> EpubResult:
    directory = project.generated_dir / "epub"
    pages, diags, _photos, model = prepare_pages(project, directory, qr=False)
    check_web_links(model, pages, diags)
    if not diags.ok:
        raise ValidationFailed(diags)
    pages = _order(pages)
    env = Environment(
        loader=FileSystemLoader(project.templates_dir / "epub"),
        undefined=StrictUndefined,
        comment_start_string="<#",
        comment_end_string="#>",
        keep_trailing_newline=True,
        # Drop the newline after each block tag, so loops produce tight lists.
        trim_blocks=True,
        lstrip_blocks=True,
    )
    labels = {
        label for page in pages for label in page.anchors if label != page.context.get("end_label")
    }
    labels.difference_update(
        t["label"] for p in pages for t in p.context.get("teams", []) if not t["recipes"]
    )
    labels.update(m["label"] for page in pages for m in page.context.get("dishoffs", []))
    kinds = _component_kinds(model)
    labels.update(kinds.values())
    paths = {f"recipe:{r.id}": r.path for r in model.recipes_by_id.values()}
    paths.update({f"component:{c.id}": c.path for c in model.components_by_id.values()})

    def route(label: str, source: str = "") -> str:
        if label not in labels:
            diags.error(
                "epub-reference",
                f"links to {label}, which the EPUB does not include",
                paths.get(source) or project.templates_dir / "epub",
            )
            raise ValidationFailed(diags)
        return "#" + html_id(label)

    env.filters.update(md=_md, anchor=html_id, web_body=_prose, site_name=_site_name)
    env.globals["route"] = route
    metadata = tomllib.loads((project.root / "pyproject.toml").read_text())
    version = metadata["project"]["version"]
    parts = _render(env, pages, model, kinds, version)

    cover = pages[0].context
    photos = [directory / p.context["image"] for p in pages if p.context.get("image")]
    _cover(directory / "cover.jpg", cover, photos)
    header = {
        "title": cover["title"],
        "subtitle": cover["subtitle"],
        "author": _author(project),
        "lang": "en",
        "identifier": EPUB_IDENTIFIER,
        "description": _description(cover["body"]) or cover["subtitle"] or cover["title"],
        "rights": RIGHTS,
        "cover-image": "cover.jpg",
        "format": {
            "epub": {
                "toc": True,
                "toc-depth": 3,
                "number-sections": False,
                "css": "epub.css",
                # Each recipe, component, menu and section divider opens on a new page.
                "epub-chapter-level": 3,
            }
        },
    }
    document = directory / "book.qmd"
    body = "\n\n".join(parts)
    body = re.sub(r"(?m)^(:{3,}[^\n]*)$", r"\n\1\n", body)
    document.write_text("---\n" + yaml.safe_dump(header, sort_keys=False) + "---\n\n" + body)
    shutil.copy2(project.styles_dir / "epub.css", directory / "epub.css")
    if not render:
        return EpubResult(document, None, diags)
    quarto = shutil.which("quarto")
    if not quarto:
        diags.error("epub", "Quarto is required; install it or use epub --no-render.", document)
        raise ValidationFailed(diags)
    result = subprocess.run(
        [quarto, "render", "book.qmd", "--to", "epub"],
        cwd=directory,
        capture_output=True,
        text=True,
        check=False,
    )
    staged = directory / "book.epub"
    if result.returncode or not staged.is_file():
        diags.error(
            "epub",
            "Quarto EPUB build failed:\n"
            + "\n".join((result.stdout + result.stderr).splitlines()[-35:]),
            document,
        )
        raise ValidationFailed(diags)
    check_epub(staged, diags, {html_id(label) for label in labels})
    if not diags.ok:
        raise ValidationFailed(diags)
    project.dist_dir.mkdir(parents=True, exist_ok=True)
    target = project.dist_dir / EPUB_FILENAME
    shutil.copy2(staged, target)
    return EpubResult(document, target, diags)


def _component_kinds(model: BookModel) -> dict[str, str]:
    """Section label (``kind:<id>``) of each component kind that has published components."""
    used = {c.kind.id for c in model.components}
    return {k.id: f"kind:{k.id}" for k in model.settings.component_kinds if k.id in used}


def _description(body: str) -> str:
    """The cover's first paragraph as plain text, for the reading app's book details."""
    for paragraph in _prose(body).split("\n\n"):
        text = " ".join(paragraph.split())
        if text and not text.startswith(("#", "<", "`")):
            return re.sub(r"[*_`]", "", text)
    return ""


def _render(
    env: Environment, pages: list[PageSpec], model: BookModel, kinds: dict[str, str], version: str
) -> list[str]:
    """Render every page, adding the team and component-kind section openers.

    The print book repeats a menu type's title on each page of menus; the EPUB
    prints it once, before the first menu of that type.
    """
    teams = {t["name"]: t for p in pages for t in p.context.get("teams", [])}
    kind_titles = {k.id: k.label for k in model.settings.component_kinds}
    parts: list[str] = []
    last_team = last_kind = last_menu_type = None
    for page in pages:
        context = page.context
        extra: dict[str, Any] = {}
        if page.template == "recipe.qmd.j2" and context["team"] != last_team:
            last_team = context["team"]
            team = teams[last_team]
            parts.append(
                f"## {_md(team['name'])} {{#{html_id(team['label'])}}}\n\n"
                f"[{_md(team['location'])}]{{.eyebrow}}\n"
            )
        if page.template == "component.qmd.j2":
            kind = model.components_by_id[context["label"].split(":", 1)[1]].kind.id
            if kind != last_kind:
                last_kind = kind
                parts.append(f"## {_md(kind_titles[kind])} {{#{html_id(kinds[kind])}}}\n")
        if page.template == "game-day-menu.qmd.j2":
            extra["continued"] = context["type_title"] == last_menu_type
            last_menu_type = context["type_title"]
        if page.template == "make-buy-index.qmd.j2":
            extra["kind_links"] = {kind_titles[k]: label for k, label in kinds.items()}
        parts.append(env.get_template(page.template).render(**context, **extra, version=version))
    return parts
