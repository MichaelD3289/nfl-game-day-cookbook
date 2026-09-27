"""Independent reflowable EPUB generation from the published book model."""

import re
import shutil
import subprocess
import tomllib
from dataclasses import dataclass
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from nfl_book.digital import prepare_pages
from nfl_book.epub_check import check_epub
from nfl_book.errors import Diagnostics, ValidationFailed
from nfl_book.project import Project

EPUB_FILENAME = "nfl-game-day-cookbook.epub"


@dataclass(frozen=True)
class EpubResult:
    document: Path
    epub: Path | None
    diagnostics: Diagnostics


def build_epub(project: Project, *, render: bool = True) -> EpubResult:
    directory = project.generated_dir / "epub"
    pages, diags, _photos, _model = prepare_pages(project, directory)
    env = Environment(
        loader=FileSystemLoader(project.templates_dir / "epub"),
        undefined=StrictUndefined,
        comment_start_string="<#",
        comment_end_string="#>",
        keep_trailing_newline=True,
    )

    def anchor(value: str) -> str:
        return value.replace(":", "-")

    def md(value: str) -> str:
        return re.sub(r"([\\`*_{}\[\]<>#|])", r"\\\1", value)

    def prose(value: str) -> str:
        value = value.replace(r"`\QMark{}\ `{=latex}", "**Q** ")
        return re.sub(r"```\{=latex\}\n.*?\n```", "", value, flags=re.DOTALL)

    labels = {
        label for page in pages for label in page.anchors if label != page.context.get("end_label")
    }
    labels.difference_update(
        t["label"] for p in pages for t in p.context.get("teams", []) if not t["recipes"]
    )
    labels.update(m["label"] for page in pages for m in page.context.get("dishoffs", []))

    def route(label: str) -> str:
        if label not in labels:
            diags.error(
                "epub-reference", f"Unknown EPUB reference: {label}", project.templates_dir / "epub"
            )
            raise ValidationFailed(diags)
        return "#" + anchor(label)

    env.filters.update(md=md, anchor=anchor, web_body=prose)
    env.globals["route"] = route
    metadata = tomllib.loads((project.root / "pyproject.toml").read_text())
    version = metadata["project"]["version"]
    teams = {t["name"]: t["label"] for p in pages for t in p.context.get("teams", [])}
    parts = []
    last_team = None
    for page in pages:
        if page.template == "recipe.qmd.j2" and page.context["team"] != last_team:
            last_team = page.context["team"]
            parts.append(f"## {md(last_team)} {{#{anchor(teams[last_team])}}}\n")
        parts.append(env.get_template(page.template).render(**page.context, version=version))
    header = {
        "title": pages[0].context["title"],
        "subtitle": pages[0].context["subtitle"],
        "author": "Michael Drummond and contributors",
        "lang": "en",
        "identifier": f"urn:nfl-game-day-cookbook:{version}",
        "format": {
            "epub": {
                "toc": True,
                "toc-depth": 3,
                "number-sections": False,
                "css": "epub.css",
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
    check_epub(staged, diags, {anchor(label) for label in labels})
    if not diags.ok:
        raise ValidationFailed(diags)
    project.dist_dir.mkdir(parents=True, exist_ok=True)
    target = project.dist_dir / EPUB_FILENAME
    shutil.copy2(staged, target)
    return EpubResult(document, target, diags)
