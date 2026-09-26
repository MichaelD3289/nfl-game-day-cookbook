"""Independent HTML presentation of the resolved book; never mutates authored content."""

from __future__ import annotations

import html
import re
import shutil
import subprocess
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from nfl_book.errors import Diagnostics, ValidationFailed
from nfl_book.pipeline import build_media, load
from nfl_book.project import Project
from nfl_book.render.pages import Media, PageSpec, build_pages
from nfl_book.resolve import resolve

RELEASES = "https://github.com/MichaelD3289/nfl-game-day-cookbook/releases"


@dataclass(frozen=True)
class WebsiteResult:
    document: Path
    site: Path | None
    diagnostics: Diagnostics


def _filename(page: PageSpec) -> str:
    return "index.qmd" if page.slug == "cover" else f"{page.slug}.qmd"


def _anchor(label: str) -> str:
    return label.replace(":", "-")


def _markdown(text: str) -> str:
    """Escape plain titles used in Markdown (rich authored body text passes through)."""
    return re.sub(r"([\\`*_{}\[\]<>#|])", r"\\\1", text)


def _web_body(text: str) -> str:
    # Print cover annotations: preserve prose and provide the equivalent visible Q.
    text = text.replace(r"`\QMark{}\ `{=latex}", "[Q]{.q-mark}")
    return re.sub(r"```\{=latex\}\n.*?\n```", "", text, flags=re.DOTALL)


def _navigation(pages: list[PageSpec]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = [
        {"text": "Start here", "href": "index.qmd"},
        {"text": "All recipes", "href": "contents.qmd"},
    ]
    indexes = [
        {"text": p.context["title"], "href": _filename(p)}
        for p in pages
        if p.template == "index.qmd.j2"
    ]
    result.append({"section": "Find a recipe", "contents": indexes})
    for p in pages:
        if p.template == "division.qmd.j2":
            teams = [
                {"text": t["name"], "href": f"{_filename(p)}#{_anchor(t['label'])}"}
                for t in p.context["teams"]
                if t["recipes"]
            ]
            if teams:
                result.append(
                    {"section": p.context["name"], "href": _filename(p), "contents": teams}
                )
    result.extend(
        [
            {"text": "Game Day Menus", "href": "game-day-menus.qmd"},
            {"text": "Make It or Buy It", "href": "make-it-or-buy-it.qmd"},
        ]
    )
    return result


def _prepare(project: Project, build_dir: Path) -> tuple[list[PageSpec], Diagnostics]:
    loaded = load(project)
    if not loaded.diagnostics.ok:
        raise ValidationFailed(loaded.diagnostics)
    model = resolve(loaded.settings, loaded.content, loaded.shortlinks.links)
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir(parents=True)
    media = build_media(project, model, build_dir)
    assets = build_dir / "assets"
    assets.mkdir()
    maps = []
    for mapping in (media.qr, media.images):
        copied = {}
        for label, relative in mapping.items():
            source = (build_dir / relative).resolve()
            name = f"{_anchor(label)}{source.suffix}"
            if mapping is media.qr:
                name = f"qr-{name}"
            shutil.copyfile(source, assets / name)
            copied[label] = f"assets/{name}"
        maps.append(copied)
    pages = build_pages(model, Media(qr=maps[0], images=maps[1]))
    descriptions = {f"recipe:{r.id}": r.meta.description for r in model.recipes}
    menu_previews = {m["label"]: m for page in pages for m in page.context.get("menus", [])}
    for page in pages:
        page.context["recipe_descriptions"] = descriptions
        page.context["menu_previews"] = menu_previews
    return pages, loaded.diagnostics


def build_website(project: Project, *, render: bool = True) -> WebsiteResult:
    build_dir = project.generated_dir / "site"
    pages, diags = _prepare(project, build_dir)
    routes = {label: f"{_filename(p)}#{_anchor(label)}" for p in pages for label in p.anchors}
    for p in pages:
        for menu in p.context.get("dishoffs", []):
            routes[menu["label"]] = f"{_filename(p)}#{_anchor(menu['label'])}"
    env = Environment(
        loader=FileSystemLoader(project.templates_dir / "website"),
        undefined=StrictUndefined,
        autoescape=False,
        keep_trailing_newline=True,
    )
    env.filters.update(md=_markdown, web_body=_web_body, anchor=_anchor)
    env.globals.update(route=lambda label: routes[label])
    metadata = tomllib.loads((project.root / "pyproject.toml").read_text())
    version = metadata["project"]["version"]
    pdf = load(project).settings.book.output_filename
    download = f"{RELEASES}/latest/download/{pdf}"
    for page in pages:
        context = page.context
        title = context.get("title") or context.get("name") or context.get("type_title")
        title = title or {
            "contents": "All recipes",
            "game-day-menus": "Game Day Menus",
            "make-it-or-buy-it": "Make It or Buy It",
        }.get(page.slug, page.slug)
        front = yaml.safe_dump({"title": "", "pagetitle": title}, sort_keys=False)
        body = env.get_template(page.template).render(**context, version=version, download=download)
        body = re.sub(r"(?m)^(:{3,}[^\n]*)$", r"\n\1\n", body)
        (build_dir / _filename(page)).write_text(f"---\n{front}---\n\n{body}")
    config = {
        "project": {"type": "website", "output-dir": "_site", "resources": ["assets/**"]},
        "website": {
            "title": pages[0].context["title"],
            "search": {"location": "sidebar", "type": "textbox"},
            "sidebar": {"style": "docked", "collapse-level": 1, "contents": _navigation(pages)},
            "navbar": {
                "right": [
                    {"text": f"v{version}", "href": f"{RELEASES}/tag/v{version}"},
                    {"text": "Download PDF", "href": download},
                    {"text": "Earlier releases", "href": RELEASES},
                ]
            },
            "page-footer": {
                "left": "NFL Meals · A city-by-city game-day cookbook",
                "right": f"Edition {html.escape(version)}",
            },
        },
        "format": {
            "html": {
                "theme": "cosmo",
                "css": "website.css",
                "toc": False,
                "anchor-sections": False,
                "smooth-scroll": True,
                "lang": "en",
            }
        },
    }
    (build_dir / "_quarto.yml").write_text(yaml.safe_dump(config, sort_keys=False))
    shutil.copyfile(project.styles_dir / "website.css", build_dir / "website.css")
    if not render:
        return WebsiteResult(build_dir / "index.qmd", None, diags)
    quarto = shutil.which("quarto")
    if quarto is None:
        diags.error(
            "website",
            "Quarto is required; install it or use website --no-render.",
            build_dir / "_quarto.yml",
        )
        raise ValidationFailed(diags)
    compiled = subprocess.run(
        [quarto, "render", "--to", "html"],
        cwd=build_dir,
        capture_output=True,
        text=True,
        check=False,
    )
    staged = build_dir / "_site"
    if compiled.returncode or not (staged / "index.html").is_file():
        tail = "\n".join((compiled.stdout + compiled.stderr).splitlines()[-35:])
        diags.error("website", f"Quarto HTML build failed:\n{tail}", build_dir / "_quarto.yml")
        raise ValidationFailed(diags)
    from nfl_book.website_check import check_site

    check_site(staged, diags)
    if not diags.ok:
        raise ValidationFailed(diags)
    target = project.dist_dir / "site"
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(staged, target)
    return WebsiteResult(build_dir / "index.qmd", target, diags)
