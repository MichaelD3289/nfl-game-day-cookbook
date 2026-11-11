---
name: creating-release
description: "Release a new version of the NFL cookbook: SemVer bump from CHANGELOG [Unreleased], dated changelog, merged to main for automatic tagging. Use when asked to release or bump the version, tag a release, or rerun or republish a failed release."
---

# Creating a release

## Pick the bump from `[Unreleased]`

In this repo, the "public API" is:

- the content format (recipe and component front matter, and paths);
- `data/*.yml`;
- the `nfl-book` CLI and Make targets;
- the printed book.

Read every entry under `## [Unreleased]` and use the **highest** rule that matches:

| Found in `[Unreleased]`                                                                                                                                                                           | Bump      |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| Any `Removed` entry, or any **BREAKING:** entry. Examples: renamed or required front-matter field, moved content path, changed `data/*.yml` schema, removed or renamed CLI command or Make target | **major** |
| Any `Added` entry (new recipe, component, menu, index, command, target or skill), a `Deprecated` entry, or a `Changed` entry that alters the book or tooling behaviour                            | **minor** |
| Only `Fixed`, `Security`, or wording-only `Changed` entries                                                                                                                                       | **patch** |

**While the version is `0.x`,** use a minor bump where the table says major, so `0.2.0`
goes to `0.3.0`. Go to `1.0.0` only when the user asks for it.

**Enforce it:**

- If `[Unreleased]` is empty, stop. There is nothing to release.
- If the user asks for a specific version or bump that differs from the rule, say which
  entries require which bump and ask before continuing. The bump is at least what the
  entries require.
- If an entry looks misfiled, for example a breaking change under `Fixed`, point it out
  before releasing.

## Steps

Automation owns tags: your job ends when the release commit is merged into `main`.

1. **Start clean.** Commit pending work through `logical-commits` first. The **release
   commit** holds only `pyproject.toml`, `uv.lock` and `CHANGELOG.md`, on its own
   branch from current `main`.
2. **Preview the bump:** `uv version --bump <major|minor|patch> --dry-run` prints
   `old => new` and writes nothing.
3. **Apply it:** `uv version --bump <major|minor|patch>` updates `pyproject.toml` and
   re-locks `uv.lock`. Read the new version back with `uv version --short`.
4. **Date the changelog.** Rename `## [Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD`
   exactly; auto-tag rejects the release otherwise. Use today's date in the
   maintainer's local time zone, not UTC: agents and CI often run on UTC, which is
   already the next day in the maintainer's evening, so ask if you cannot tell the local
   date. Add a fresh, empty `## [Unreleased]` above it. At the bottom, point
   `[Unreleased]` at `compare/vX.Y.Z...HEAD` and add
   `[X.Y.Z]: .../compare/vPREV...vX.Y.Z`.
5. **Prove it green.** Run `make check`, `uv run nfl-book build --strict`,
   `uv run nfl-book cards --strict`, `make booklets`, `make website` and `make epub`.
   Each must exit 0. `make booklets` runs in no PR check, so a failure there would
   surface only after the tag exists.
6. **Commit.** Show the user the three files and the message `chore(release): X.Y.Z`,
   and commit on their approval. This skill owns the release commit; it needs no
   `logical-commits` plan.
7. **Open a PR and get it squash-merged into `main`.** Title it
   `chore(release): X.Y.Z`. The squash creates a new commit
   (`chore(release): X.Y.Z (#N)`), and auto-tag judges eligibility at that commit: a
   version higher than every stable tag gets an annotated tag there, and auto-tag calls
   `release.yml`.
8. **Verify publication.** Watch `gh run list --workflow auto-tag.yml --limit 1`, then
   `gh release view vX.Y.Z --json url`. The Release workflow re-checks main ancestry and
   the version, builds and publishes every asset in `release.yml`, and deploys Pages
   when this is the newest stable tag. Report the workflow result and the release URL.
   If publication failed or was skipped, read
   [references/tagging.md](references/tagging.md).
