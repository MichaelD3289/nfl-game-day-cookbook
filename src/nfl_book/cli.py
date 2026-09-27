"""``nfl-book`` command line interface."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, NoReturn

import typer
from rich.console import Console

from nfl_book import pipeline, scaffold
from nfl_book.config import load_settings
from nfl_book.errors import BookError, Diagnostics, Severity, ValidationFailed
from nfl_book.preview import preview as run_preview
from nfl_book.project import Project

app = typer.Typer(no_args_is_help=True, help="Build the NFL Game Day Cookbook from source.")
new_app = typer.Typer(no_args_is_help=True, help="Create a new draft from a template.")
app.add_typer(new_app, name="new")

out = Console()
err = Console(stderr=True)


@dataclass
class State:
    root: Path | None = None
    content: Path | None = None
    generated: Path | None = None
    dist: Path | None = None

    def project(self) -> Project:
        base = Project.discover(self.root)
        if self.content is None and self.generated is None and self.dist is None:
            return base
        return Project.create(base.root, self.content, self.generated, self.dist)


state = State()


@app.callback()
def main(
    root: Annotated[
        Path | None, typer.Option(help="Project root (default: search upward).")
    ] = None,
    content: Annotated[
        Path | None, typer.Option(help="Content root holding recipes/, components/, menus/.")
    ] = None,
    generated: Annotated[Path | None, typer.Option(help="Generated build directory.")] = None,
    dist: Annotated[
        Path | None, typer.Option(help="Output directory for the PDF and website.")
    ] = None,
) -> None:
    state.root, state.content, state.generated, state.dist = root, content, generated, dist


def report(diags: Diagnostics, root: Path) -> None:
    for d in diags:
        style = "red" if d.severity is Severity.ERROR else "yellow"
        err.print(f"[{style}]{d.format(root)}[/{style}]", highlight=False, soft_wrap=True)


def fail(exc: BookError, root: Path | None) -> NoReturn:
    if isinstance(exc, ValidationFailed):
        report(exc.diagnostics, root or Path.cwd())
        err.print(f"[red]{len(exc.diagnostics.errors)} error(s)[/red]")
    else:
        err.print(f"[red]error:[/red] {exc}", highlight=False, soft_wrap=True)
    raise typer.Exit(1)


@app.command()
def validate(
    paths: Annotated[
        list[Path] | None, typer.Argument(help="Limit reports to these paths.")
    ] = None,
) -> None:
    """Validate all content (offline). Errors name the source file."""
    project = None
    try:
        project = state.project()
        diags = pipeline.validate(project, paths)
    except BookError as exc:
        fail(exc, project.root if project else None)
    report(diags, project.root)
    out.print(f"[green]OK[/green] ({len(diags.warnings)} warning(s))")


def _prepare() -> None:
    project = None
    try:
        project = state.project()
        result = pipeline.prepare_links(project)
    except BookError as exc:
        fail(exc, project.root if project else None)
    for full, short in result.added.items():
        out.print(f"added {short} <- {full}", highlight=False)
    out.print(f"{len(result.added)} added, {result.cached} already cached")


@app.command()
def prepare() -> None:
    """Alias of prepare-links."""
    _prepare()


@app.command("prepare-links")
def prepare_links() -> None:
    """The ONLY network stage: shorten new source URLs into data/shortlinks.yml, make QRs."""
    _prepare()


@app.command()
def preview(
    path: Annotated[Path, typer.Argument(help="A recipe or component Markdown file.")],
    no_pdf: Annotated[bool, typer.Option("--no-pdf", help="Generate QMD only.")] = False,
) -> None:
    """Render one recipe or component (drafts included)."""
    project = None
    try:
        project = state.project()
        result = run_preview(project, path, pdf=not no_pdf)
    except BookError as exc:
        fail(exc, project.root if project else None)
    report(result.diagnostics, project.root)
    out.print(f"QMD: {result.document}")
    if result.pdf:
        out.print(f"PDF: {result.pdf}")


@app.command()
def build(
    no_pdf: Annotated[bool, typer.Option("--no-pdf", help="Generate QMD only.")] = False,
    strict: Annotated[bool, typer.Option(help="Treat page overflows as errors.")] = False,
) -> None:
    """Validate, generate Quarto sources and compile the PDF (published content only)."""
    project = None
    try:
        project = state.project()
        result = pipeline.build(project, pdf=not no_pdf, strict=strict)
    except BookError as exc:
        fail(exc, project.root if project else None)
    report(result.diagnostics, project.root)
    out.print(f"QMD: {result.document}")
    out.print(f"Photos: {result.photos.summary()}")
    if result.pdf:
        out.print(f"PDF: {result.pdf}")


@app.command()
def website(
    no_render: Annotated[
        bool, typer.Option("--no-render", help="Generate website QMD without compiling HTML.")
    ] = False,
) -> None:
    """Build the static website in dist/site (offline, published content only)."""
    from nfl_book.website import build_website

    project = None
    try:
        project = state.project()
        result = build_website(project, render=not no_render)
    except BookError as exc:
        fail(exc, project.root if project else None)
    report(result.diagnostics, project.root)
    out.print(f"Website sources: {result.document.parent}")
    out.print(f"Photos: {result.photos.summary()}")
    if result.site:
        out.print(f"Website: {result.site}")


@app.command()
def epub(
    no_render: Annotated[
        bool, typer.Option("--no-render", help="Generate EPUB sources only.")
    ] = False,
) -> None:
    """Build the reflowable EPUB (offline, published content only)."""
    from nfl_book.epub import build_epub

    project = None
    try:
        project = state.project()
        result = build_epub(project, render=not no_render)
    except BookError as exc:
        fail(exc, project.root if project else None)
    report(result.diagnostics, project.root)
    out.print(f"EPUB sources: {result.document}")
    if result.epub:
        out.print(f"EPUB: {result.epub}")


@app.command()
def clean() -> None:
    """Remove generated/ and dist/."""
    try:
        removed = pipeline.clean(state.project())
    except BookError as exc:
        fail(exc, None)
    for path in removed:
        out.print(f"removed {path}")


@new_app.command("recipe")
def new_recipe(
    team: Annotated[str, typer.Option(help="Team slug, e.g. bills.")],
    slug: Annotated[str, typer.Option(help="Recipe id (kebab-case, unique).")],
) -> None:
    """Create a draft recipe in the team's directory."""
    try:
        project = state.project()
        path = scaffold.new_recipe(project, load_settings(project), team, slug)
    except BookError as exc:
        fail(exc, None)
    out.print(f"created {path}")


@new_app.command("component")
def new_component(
    kind: Annotated[str, typer.Option(help="Component kind, e.g. sauces.")],
    slug: Annotated[str, typer.Option(help="Component id (kebab-case, unique).")],
) -> None:
    """Create a draft shared component."""
    try:
        project = state.project()
        path = scaffold.new_component(project, load_settings(project), kind, slug)
    except BookError as exc:
        fail(exc, None)
    out.print(f"created {path}")
