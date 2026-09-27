"""CLI wiring: exit codes, messages and that every command honours the path options."""

from __future__ import annotations

from collections.abc import Callable, Iterator
from pathlib import Path

import httpx
import pytest
from typer.testing import CliRunner

from nfl_book import cli, pipeline
from nfl_book.errors import BookError
from nfl_book.pipeline import load
from nfl_book.project import Project
from nfl_book.shortlinks import Shortener
from nfl_book.shortlinks.check import LinkChecker

runner = CliRunner()


@pytest.fixture(autouse=True)
def reset_state() -> Iterator[None]:
    cli.state = cli.State()
    yield
    cli.state = cli.State()


def invoke(project: Project, *args: str) -> tuple[int, str]:
    content = project.content_root
    result = runner.invoke(
        cli.app,
        [
            "--root",
            str(project.root),
            "--content",
            str(content),
            "--generated",
            str(content / "generated"),
            "--dist",
            str(content / "dist"),
            *args,
        ],
    )
    return result.exit_code, result.output


def test_validate_ok(fixture_book: Project) -> None:
    code, output = invoke(fixture_book, "validate")
    assert code == 0, output
    assert "OK" in output


def test_validate_failure_names_file(fixture_book: Project) -> None:
    path = fixture_book.content_root / "recipes/afc/east/bills/test-buffalo-sliders.md"
    path.write_text(path.read_text().replace("course:", "course_typo:"), encoding="utf-8")
    code, output = invoke(fixture_book, "validate")
    assert code == 1
    assert "test-buffalo-sliders.md" in output


def test_build_without_pdf(fixture_book: Project) -> None:
    code, output = invoke(fixture_book, "build", "--no-pdf")
    assert code == 0, output
    assert "QMD:" in output
    assert (fixture_book.content_root / "generated/book/book.qmd").is_file()


def test_preview_draft_recipe(fixture_book: Project) -> None:
    draft = fixture_book.content_root / "recipes/afc/east/jets/test-draft-nachos.md"
    code, output = invoke(fixture_book, "preview", str(draft), "--no-pdf")
    assert code == 0, output
    assert "QMD:" in output


def test_new_recipe_and_component(fixture_book: Project) -> None:
    code, output = invoke(fixture_book, "new", "recipe", "--team", "packers", "--slug", "brat-dip")
    assert code == 0, output
    assert (fixture_book.content_root / "recipes/nfc/north/packers/brat-dip.md").is_file()

    code, output = invoke(
        fixture_book, "new", "component", "--kind", "sauces", "--slug", "beer-cheese"
    )
    assert code == 0, output
    assert (fixture_book.content_root / "components/sauces/beer-cheese.md").is_file()

    code, output = invoke(fixture_book, "new", "recipe", "--team", "packers", "--slug", "brat-dip")
    assert code == 1


def test_clean(fixture_book: Project) -> None:
    assert invoke(fixture_book, "build", "--no-pdf")[0] == 0
    code, output = invoke(fixture_book, "clean")
    assert code == 0, output
    assert not (fixture_book.content_root / "generated").exists()


def test_production_skeleton_validates() -> None:
    """The committed (empty) production tree is always a valid book."""
    root = Path(__file__).resolve().parents[2]
    diags = load(Project.create(root)).diagnostics
    assert diags.ok, [d.message for d in diags.errors]


LinkHandler = Callable[[httpx.Request], httpx.Response]


@pytest.fixture
def offline_links(monkeypatch: pytest.MonkeyPatch) -> Callable[[LinkHandler], None]:
    """Answer --check requests with ``handler``; shortening would fail loudly."""

    def no_shortener(name: str) -> Shortener:
        raise BookError("--check must not shorten anything")

    monkeypatch.setattr(pipeline, "get_shortener", no_shortener)

    def use(handler: LinkHandler) -> None:
        client = httpx.Client(transport=httpx.MockTransport(handler))
        monkeypatch.setattr(
            pipeline,
            "default_link_checker",
            lambda: LinkChecker(client, sleep=lambda _: None, clock=lambda: 0.0),
        )

    return use


def test_prepare_links_check_reports_dead_link(
    fixture_book: Project, offline_links: Callable[[LinkHandler], None], tmp_path: Path
) -> None:
    dead = "https://example.com/recipes/test-citrus-wings"
    offline_links(lambda r: httpx.Response(404 if str(r.url) == dead else 200))
    report = tmp_path / "r.md"
    code, output = invoke(fixture_book, "prepare-links", "--check", "--report", str(report))
    assert code == 1, output
    assert "test-citrus-wings.md" in output
    assert "3 checked, 1 need attention" in output
    assert report.read_text(encoding="utf-8").startswith("# Source link check")


def test_prepare_links_check_all_ok(
    fixture_book: Project, offline_links: Callable[[LinkHandler], None], tmp_path: Path
) -> None:
    offline_links(lambda _: httpx.Response(200))
    report = tmp_path / "ok.md"
    code, output = invoke(fixture_book, "prepare-links", "--check", "--report", str(report))
    assert code == 0, output
    assert "All 3" in report.read_text(encoding="utf-8")


def test_prepare_alias_check(
    fixture_book: Project, offline_links: Callable[[LinkHandler], None]
) -> None:
    offline_links(lambda _: httpx.Response(200))
    code, output = invoke(fixture_book, "prepare", "--check")
    assert code == 0, output
    assert "3 checked, 0 need attention" in output


def test_report_needs_check(
    fixture_book: Project, offline_links: Callable[[LinkHandler], None], tmp_path: Path
) -> None:
    code, output = invoke(fixture_book, "prepare-links", "--report", str(tmp_path / "r.md"))
    assert code == 2, output
    assert not (tmp_path / "r.md").exists()
