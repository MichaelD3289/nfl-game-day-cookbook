---
name: release
description: Record changes in CHANGELOG.md (Keep a Changelog) and cut a version of the NFL cookbook - bump pyproject version, commit, tag.
---

# Changelog and releases

`CHANGELOG.md` follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/),
and versions follow SemVer.

## Every change

Add a bullet under `## [Unreleased]` in the right subsection. Use only these,
in this order:

1. `Added`
2. `Changed`
3. `Deprecated`
4. `Removed`
5. `Fixed`
6. `Security`

Write for a reader of the book or repo, not a commit log. Examples:
- "Added Buffalo sliders (Bills)."
- "Recipe photos now sit beside the title."

## Cutting a release (only when the user asks)

1. Choose the version:
   - patch for content fixes
   - minor for new recipes, features or layout changes
   - major for incompatible content-format changes
2. Rename `[Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD` and add a fresh, empty
   `## [Unreleased]` above it.
3. Set `version = "X.Y.Z"` in `pyproject.toml`, then run `uv lock`.
4. Run `make check` and `make pdf`. Both must succeed with no overflow warnings.
5. Commit only when the user asks. The message should summarise the release notes.
   If on `main`, confirm that the user wants the commit there.
6. Tag (`git tag -a vX.Y.Z -m "vX.Y.Z"`) only if the user asks. Push only if asked.
7. If a remote exists, add the compare links at the bottom of the changelog.
