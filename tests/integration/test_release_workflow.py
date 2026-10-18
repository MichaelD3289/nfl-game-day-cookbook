"""Exercise the workflow's release guard against a synthetic Git repository."""

import os
import shlex
import subprocess
from pathlib import Path

import pytest
import yaml

from nfl_book.config import load_settings
from nfl_book.project import Project

WORKFLOW = Path(__file__).resolve().parents[2] / ".github/workflows/release.yml"


@pytest.mark.parametrize(
    ("case", "allowed"),
    [
        ("main", True),
        ("older-main", True),
        ("feature", False),
        ("missing", False),
        ("wrong-checkout", False),
    ],
)
def test_release_requires_tag_on_main(tmp_path: Path, case: str, allowed: bool) -> None:
    def git(*args: str) -> str:
        return subprocess.check_output(["git", *args], cwd=tmp_path, text=True).strip()

    git("init", "-b", "main")
    git("config", "user.email", "test@example.com")
    git("config", "user.name", "Test")
    git("commit", "--allow-empty", "-m", "initial")
    git("tag", "-a", "v0.1.0", "-m", "test")
    git("commit", "--allow-empty", "-m", "main update")
    git("tag", "v0.2.0")
    git("update-ref", "refs/remotes/origin/main", "HEAD")
    if case == "feature":
        git("checkout", "-b", "feature")
        git("commit", "--allow-empty", "-m", "unmerged")
        git("tag", "v0.3.0")
    tag = {
        "main": "v0.2.0",
        "older-main": "v0.1.0",
        "feature": "v0.3.0",
        "missing": "main",
        "wrong-checkout": "v0.1.0",
    }[case]
    if case == "older-main":
        git("checkout", "--detach", tag)
    workflow = yaml.safe_load(WORKFLOW.read_text())
    guard = next(
        step["run"]
        for step in workflow["jobs"]["release"]["steps"]
        if step.get("name") == "Verify release tag is on main"
    )
    result = subprocess.run(
        ["bash", "-e", "-o", "pipefail", "-c", guard],
        cwd=tmp_path,
        env={**os.environ, "TAG": tag},
        capture_output=True,
        text=True,
    )
    assert (result.returncode == 0) is allowed, result.stdout + result.stderr


def test_release_builds_and_publishes_recipe_cards(fixture_book: Project) -> None:
    workflow = yaml.safe_load(WORKFLOW.read_text())
    release = workflow["jobs"]["release"]
    filename = load_settings(fixture_book).book.cards.output_filename
    assert release["env"]["CARDS"] == f"dist/{filename}"
    steps = release["steps"]
    assert any(step.get("run") == "make cards" for step in steps)
    publish = next(step["run"] for step in steps if step.get("name") == "Publish release")
    for action in ("upload", "create"):
        command = next(line for line in publish.splitlines() if f"gh release {action} " in line)
        assert "$CARDS" in shlex.split(command.rstrip(" \\")), action
