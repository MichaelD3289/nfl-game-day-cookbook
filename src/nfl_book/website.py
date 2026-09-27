"""Independent HTML presentation of the resolved book; never mutates authored content."""

from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
import tomllib
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from nfl_book.digital import prepare_pages, site_name
from nfl_book.errors import Diagnostics, ValidationFailed
from nfl_book.images import PhotoStats
from nfl_book.pipeline import load
from nfl_book.project import Project
from nfl_book.publishing import EPUB_FILENAME, RELEASES, REPOSITORY
from nfl_book.quantities import Amount, find_yield_amounts
from nfl_book.references import html_id
from nfl_book.render.pages import ItemView, PageSpec
from nfl_book.resolve import BookModel

# Quick issue form per suggestion kind: (template, title prefix, field used in the title).
SUGGESTION_FORMS = {
    "edit": ("suggest-edit.yml", "Edit suggestion: ", "item"),
    "recipe": ("quick-recipe.yml", "Recipe idea: ", "dish"),
    "component": ("quick-component.yml", "Component idea: ", "name"),
    "menu": ("quick-menu.yml", "Menu idea: ", ""),
    "dish-off": ("quick-dish-off.yml", "Dish-off idea: ", ""),
}

# Recipe multipliers offered on scalable pages: (label, factor as "n" or "n/d").
MULTIPLIERS = (("½×", "1/2"), ("1×", "1"), ("1½×", "3/2"), ("2×", "2"), ("3×", "3"), ("4×", "4"))


@dataclass(frozen=True)
class WebsiteResult:
    document: Path
    site: Path | None
    diagnostics: Diagnostics
    photos: PhotoStats = field(default_factory=PhotoStats)


def _filename(page: PageSpec) -> str:
    return "index.qmd" if page.slug == "cover" else f"{page.slug}.qmd"


def _markdown(text: str) -> str:
    """Escape plain titles used in Markdown (rich authored body text passes through)."""
    return re.sub(r"([\\`*_{}\[\]<>#|])", r"\\\1", text)


def _web_body(text: str) -> str:
    # Print cover annotations: preserve prose and provide the equivalent visible Q.
    text = text.replace(r"`\QMark{}\ `{=latex}", "[Q]{.q-mark}")
    return re.sub(r"```\{=latex\}\n.*?\n```", "", text, flags=re.DOTALL)


def _marked(text: str, amounts: Iterable[Amount], plain: Callable[[str], str] = str) -> str:
    """``text`` with each scalable amount wrapped for website-scale.js; ``plain`` escapes
    the text between them."""
    parts = []
    position = 0
    for amount in amounts:
        attrs = {"data-q": str(amount.low)}
        if amount.high is not None:
            attrs["data-q2"] = str(amount.high)
        if amount.unit:
            attrs["data-unit"] = amount.unit
        if amount.adjective:
            attrs["data-adj"] = amount.adjective
        shown = " ".join(f'{k}="{html.escape(v)}"' for k, v in attrs.items())
        parts.append(plain(text[position : amount.start]))
        parts.append(f'<span class="qty" {shown}>{plain(text[amount.start : amount.end])}</span>')
        position = amount.end
    parts.append(plain(text[position:]))
    return "".join(parts)


def _scalable(item: ItemView) -> str:
    """Ingredient Markdown with each scalable amount wrapped for website-scale.js."""
    return _marked(item.text, item.amounts)


def _add_scaling(model: BookModel, pages: list[PageSpec]) -> None:
    """Scaling controls for recipe and component pages that have amounts to scale."""
    servings = {f"recipe:{r.id}": r.servings for r in model.recipes}
    yields: dict[str, str | None] = {f"recipe:{r.id}": r.meta.yield_ for r in model.recipes}
    yields.update({f"component:{c.id}": c.meta.yield_ for c in model.components})
    for page in pages:
        context = page.context
        if page.template not in ("recipe.qmd.j2", "component.qmd.j2"):
            continue
        context["scaler"] = None
        context["yield_html"] = ""
        context["yield_fixed"] = False
        if not any(item.amounts for group in context["groups"] for item in group.items):
            continue
        # The yield grows with the batch too; one it cannot scale says how many batches.
        text = yields.get(context["label"])
        if text:
            amounts = find_yield_amounts(text)
            context["yield_html"] = _marked(text, amounts, html.escape)
            context["yield_fixed"] = not amounts
        scaler: dict[str, Any] = {
            "multipliers": MULTIPLIERS,
            "servings": None,
            "servings_max": None,
            "serves": "",
        }
        people = servings.get(context["label"])
        if people:
            low, high = people
            scaler["servings"] = low
            scaler["servings_max"] = high
            scaler["serves"] = str(low) if low == high else f"{low}–{high}"
        context["scaler"] = scaler


def _suggestion(kind: str, lead: str, **fields: str) -> dict[str, str]:
    """A prefilled GitHub issue link plus the same fields for the anonymous form."""
    template, prefix, title_field = SUGGESTION_FORMS[kind]
    query = {"template": template, "title": prefix + fields.get(title_field, "")}
    query.update({k: v for k, v in fields.items() if v})
    return {
        "kind": kind,
        "lead": lead,
        "github": f"{REPOSITORY}/issues/new?{urlencode(query)}",
        "fields": json.dumps(fields, ensure_ascii=False),
    }


def _add_suggestions(project: Project, model: BookModel, pages: list[PageSpec]) -> None:
    def source(path: Path) -> str:
        return path.relative_to(project.content_root).as_posix()

    items = {f"recipe:{r.id}": (r.path, f"{r.title} ({r.team.name})") for r in model.recipes}
    items.update({f"component:{c.id}": (c.path, c.title) for c in model.components})
    for page in pages:
        context = page.context
        if page.template in ("recipe.qmd.j2", "component.qmd.j2"):
            path, name = items[context["label"]]
            noun = "recipe" if page.template == "recipe.qmd.j2" else "component"
            context["suggest"] = _suggestion(
                "edit",
                f"Spot something to fix in this {noun}?",
                item=f"{name} [{context['label']}]",
                page=source(path),
            )
        elif page.template == "division.qmd.j2":
            for team in context["teams"]:
                team["suggest"] = _suggestion(
                    "recipe",
                    f"Know another {team['name']} dish?",
                    team=f"{team['name']} ({team['location']})",
                )
            context["suggest"] = _suggestion(
                "recipe", f"Missing a dish from a {context['name']} team?", team=""
            )
            context["suggest_dishoff"] = _suggestion(
                "dish-off",
                f"Have an idea for a {context['name']} dish-off?",
                division=context["name"],
            )
        elif page.slug == "game-day-menus":
            context["suggest"] = _suggestion("menu", "Have an idea for a game-day menu?")
        elif page.slug == "make-it-or-buy-it":
            context["suggest"] = _suggestion(
                "component", "Know a sauce, dip, or side we should add?"
            )


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
                {"text": t["name"], "href": f"{_filename(p)}#{html_id(t['label'])}"}
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


def _prepare(project: Project, build_dir: Path) -> tuple[list[PageSpec], Diagnostics, PhotoStats]:
    pages, diags, photos, model = prepare_pages(project, build_dir, web=True)
    _add_suggestions(project, model, pages)
    _add_scaling(model, pages)
    return pages, diags, photos


def build_website(project: Project, *, render: bool = True, preview: str = "") -> WebsiteResult:
    """Build the site; ``preview`` labels an unreleased build (a branch and commit) on
    every page, so it cannot pass for the published edition."""
    build_dir = project.generated_dir / "site"
    pages, diags, photos = _prepare(project, build_dir)
    routes = {label: f"{_filename(p)}#{html_id(label)}" for p in pages for label in p.anchors}
    for p in pages:
        for menu in p.context.get("dishoffs", []):
            routes[menu["label"]] = f"{_filename(p)}#{html_id(menu['label'])}"
    env = Environment(
        loader=FileSystemLoader(project.templates_dir / "website"),
        undefined=StrictUndefined,
        autoescape=False,
        keep_trailing_newline=True,
    )
    env.filters.update(
        md=_markdown, web_body=_web_body, anchor=html_id, scalable=_scalable, site_name=site_name
    )
    book = load(project).settings.book
    env.globals.update(
        route=lambda label: routes[label], suggestion_form_url=book.suggestion_form_url
    )
    metadata = tomllib.loads((project.root / "pyproject.toml").read_text())
    version = metadata["project"]["version"]
    pdf = book.output_filename
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
    # The release workflow lists every published website version at the marker.
    (build_dir / "versions.qmd").write_text(
        '---\ntitle: ""\npagetitle: All versions\n---\n\n# All versions\n\n'
        "Each release of this cookbook stays online at its own address. Every edition's "
        f"PDF and downloadable website are also on [GitHub releases]({RELEASES}).\n\n"
        "```{=html}\n<!-- site-versions -->\n```\n"
    )
    resources = ["assets/**", "scale.js", "print.js", "cook.js"]
    shutil.copyfile(project.styles_dir / "website-scale.js", build_dir / "scale.js")
    shutil.copyfile(project.styles_dir / "website-print.js", build_dir / "print.js")
    shutil.copyfile(project.styles_dir / "website-cook.js", build_dir / "cook.js")
    scripts = ["print.js", "cook.js"]
    html_format: dict[str, Any] = {
        "theme": "cosmo",
        "css": "website.css",
        "toc": False,
        "anchor-sections": False,
        "smooth-scroll": True,
        "lang": "en",
    }
    if book.suggestion_form_url:
        resources.append("suggest.js")
        scripts.append("suggest.js")
        shutil.copyfile(project.styles_dir / "website-suggest.js", build_dir / "suggest.js")
    if preview:
        html_format["include-before-body"] = {
            "text": '<div class="preview-banner" role="note"><strong>Preview</strong> '
            f"{html.escape(preview)}. Not a published edition: the version and download "
            "links point to the latest release.</div>"
        }
    html_format["include-after-body"] = {
        "text": "\n".join(f'<script src="{name}"></script>' for name in scripts)
    }
    config = {
        "project": {"type": "website", "output-dir": "_site", "resources": resources},
        "website": {
            "title": pages[0].context["title"],
            "search": {"location": "sidebar", "type": "textbox"},
            "sidebar": {"style": "docked", "collapse-level": 1, "contents": _navigation(pages)},
            "navbar": {
                "right": [
                    {"text": f"v{version}", "href": f"{RELEASES}/tag/v{version}"},
                    {"text": "Download PDF", "href": download},
                    {
                        "text": "Download EPUB",
                        "href": f"{RELEASES}/download/v{version}/{EPUB_FILENAME}",
                    },
                    {"text": "All versions", "href": "versions.qmd"},
                    {"text": "Earlier releases", "href": RELEASES},
                ]
            },
            "page-footer": {
                "left": "NFL Meals · A city-by-city game-day cookbook",
                "right": f"Preview {html.escape(preview)}"
                if preview
                else f"Edition {html.escape(version)}",
            },
        },
        "format": {"html": html_format},
    }
    (build_dir / "_quarto.yml").write_text(yaml.safe_dump(config, sort_keys=False))
    shutil.copyfile(project.styles_dir / "website.css", build_dir / "website.css")
    if not render:
        return WebsiteResult(build_dir / "index.qmd", None, diags, photos)
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
    return WebsiteResult(build_dir / "index.qmd", target, diags, photos)
