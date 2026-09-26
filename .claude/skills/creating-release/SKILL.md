---
name: creating-release
description: Cut a new version of the NFL cookbook - pick the correct SemVer bump from CHANGELOG [Unreleased], bump with `uv version`, date the changelog, then commit and tag. Use when the user asks to release, cut, tag or bump a version.
---

# Creating a release

## Semantic versioning in brief

Versions are `MAJOR.MINOR.PATCH` ([SemVer 2.0.0](https://semver.org/spec/v2.0.0.html)):

- **MAJOR:** an incompatible change. Existing content, config or commands stop working as
  they did.
- **MINOR:** new functionality or content that stays backwards compatible.
- **PATCH:** backwards-compatible fixes only.

A bump resets the parts to its right: `0.2.3` goes to `0.3.0` on a minor bump.

## Pick the bump from `[Unreleased]`

In this repo, the "public API" is:
- the content format (recipe and component front matter, and paths);
- `data/*.yml`;
- the `nfl-book` CLI and Make targets;
- the printed book.

Read every entry under `## [Unreleased]` and use the **highest** rule that matches:

| Found in `[Unreleased]` | Bump |
| --- | --- |
| Any `Removed` entry, or any **BREAKING:** entry. Examples: renamed or required front-matter field, moved content path, changed `data/*.yml` schema, removed or renamed CLI command or Make target | **major** |
| Any `Added` entry (new recipe, component, menu, index, command, target or skill), a `Deprecated` entry, or a `Changed` entry that alters the book or tooling behaviour | **minor** |
| Only `Fixed`, `Security`, or wording-only `Changed` entries | **patch** |

**While the version is `0.x`,** use a minor bump where the table says major, so `0.2.0`
goes to `0.3.0`. Go to `1.0.0` only when the user asks for it.

**Enforce it:**
- If `[Unreleased]` is empty, stop. There is nothing to release.
- If the user asks for a specific version or bump that differs from the rule, say which
  entries require which bump and ask before continuing. Never pick a smaller bump than
  the entries require.
- If an entry looks misfiled, for example a breaking change under `Fixed`, point it out
  before releasing.

## Steps

1. **Start from a clean tree.** Commit pending work first as its own commits with the
   `logical-commits` skill. The release commit contains only the release.
2. **Preview the bump:**
   `uv version --bump <major|minor|patch> --dry-run`
   This prints `old => new` and writes nothing.
3. **Apply it:**
   `uv version --bump <major|minor|patch>`
   This updates `pyproject.toml` and re-locks `uv.lock`. Never edit the version by hand.
   Read the new version back with `uv version --short`.
4. **Date the changelog.** Rename `## [Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD`, using
   today's date. Add a fresh, empty `## [Unreleased]` above it. If a remote exists, add
   or refresh the compare links at the bottom.
5. **Verify.** Run `make check` and `make pdf`. Both must pass with no overflow warnings.
6. **Commit:**
   `git add pyproject.toml uv.lock CHANGELOG.md`
   `git commit -m "chore(release): X.Y.Z"`
   No AI attribution.
7. **Tag:**
   `git tag -a vX.Y.Z -m "vX.Y.Z"`
8. **Report** the version, the bump and why, the commit and the tag. Tell the user to
   push with `git push --follow-tags`.
