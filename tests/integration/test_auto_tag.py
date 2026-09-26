"""Run the CI tagging script against disposable repositories, never GitHub."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / ".github/scripts/tag_release.py"


@pytest.mark.parametrize(
    ("version", "previous", "expected"),
    [
        ("0.1.0", None, "v0.1.0"),
        ("0.5.0", "v0.4.0", "v0.5.0"),
        ("0.10.0", "v0.9.0", "v0.10.0"),
        ("0.4.0", "v0.4.0", ""),
        ("0.3.0", "v0.4.0", ""),
    ],
)
def test_auto_tag_and_retry(
    tmp_path: Path, version: str, previous: str | None, expected: str
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    remote = tmp_path / "remote.git"

    def git(*args: str) -> str:
        return subprocess.check_output(["git", *args], cwd=repo, text=True).strip()

    git("init", "--bare", str(remote))
    git("init", "-b", "main")
    git("config", "user.email", "test@example.com")
    git("config", "user.name", "Test")
    git("commit", "--allow-empty", "-m", "initial")
    if previous:
        git("tag", "-a", previous, "-m", "previous")
    (repo / "pyproject.toml").write_text(f'[project]\nversion = "{version}"\n')
    (repo / "CHANGELOG.md").write_text(f"## [{version}] - 2026-09-26\n\n- Test release\n")
    git("add", "pyproject.toml", "CHANGELOG.md")
    git("commit", "-m", "version")
    git("remote", "add", "origin", str(remote))
    git("push", "--tags", "origin", "main")
    sha = git("rev-parse", "HEAD")
    output = tmp_path / "output"
    env = {
        **os.environ,
        "GITHUB_REF": "refs/heads/main",
        "GITHUB_SHA": sha,
        "GITHUB_OUTPUT": str(output),
    }

    def run() -> subprocess.CompletedProcess[str]:
        output.write_text("")
        return subprocess.run(
            [sys.executable, str(SCRIPT)], cwd=repo, env=env, capture_output=True, text=True
        )

    result = run()
    assert result.returncode == 0, result.stdout + result.stderr
    assert output.read_text().strip() == f"tag={expected}"
    if expected:
        assert git("rev-parse", f"{expected}^{{commit}}") == sha
        assert expected in git("ls-remote", "--tags", "origin")
        original = git("rev-parse", expected)
        # A failed downstream build can be retried without moving/recreating its tag.
        assert run().returncode == 0
        assert output.read_text().strip() == f"tag={expected}"
        assert git("rev-parse", expected) == original
    # A manual/feature execution must never tag or publish.
    env["GITHUB_REF"] = "refs/heads/feature"
    assert run().returncode != 0
    assert output.read_text() == ""
