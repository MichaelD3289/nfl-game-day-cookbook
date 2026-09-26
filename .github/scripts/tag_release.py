"""CI-only tag creation; uses the checkout credentials and no extra dependencies."""

import os
import re
import subprocess
import tomllib
from pathlib import Path

STABLE = re.compile(r"v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)")


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True).strip()


def main() -> None:
    if os.environ.get("GITHUB_REF") != "refs/heads/main":
        raise SystemExit("Automatic tagging only runs on pushes to main.")
    sha = os.environ["GITHUB_SHA"]
    if git("rev-parse", "HEAD") != sha:
        raise SystemExit("Checkout does not match the pushed commit.")
    git("fetch", "origin", "main:refs/remotes/origin/main", "--tags")
    subprocess.run(["git", "merge-base", "--is-ancestor", sha, "origin/main"], check=True)
    version = tomllib.loads(Path("pyproject.toml").read_text())["project"]["version"]
    tag = f"v{version}"
    match = STABLE.fullmatch(tag)
    if match is None:
        raise SystemExit("pyproject.toml: automatic releases require a stable X.Y.Z version.")
    candidate = tuple(map(int, match.groups()))
    tags = git("tag", "--list").splitlines()
    versions = [tuple(map(int, m.groups())) for t in tags if (m := STABLE.fullmatch(t))]
    highest = max(versions, default=(-1, -1, -1))
    output = ""
    if candidate > highest:
        notes = Path("CHANGELOG.md").read_text()
        if not re.search(rf"^## \[{re.escape(version)}\] - \d{{4}}-\d{{2}}-\d{{2}}$", notes, re.M):
            raise SystemExit(f"CHANGELOG.md: missing dated release section for {version}.")
        git(
            "-c",
            "user.name=github-actions[bot]",
            "-c",
            "user.email=41898282+github-actions[bot]@users.noreply.github.com",
            "tag",
            "-a",
            tag,
            sha,
            "-m",
            tag,
        )
        git("push", "origin", f"refs/tags/{tag}")
        output = tag
        print(f"Created {tag} at {sha}.")
    elif candidate == highest and tag in tags and git("rev-parse", f"{tag}^{{commit}}") == sha:
        # Rerunning a failed build reuses the original tag; it never moves a tag.
        output = tag
        print(f"Reusing {tag} at the same commit for a release retry.")
    else:
        print(f"Version {version} is not newer than the highest release tag; skipping.")
    with Path(os.environ["GITHUB_OUTPUT"]).open("a") as stream:
        stream.write(f"tag={output}\n")


if __name__ == "__main__":
    main()
