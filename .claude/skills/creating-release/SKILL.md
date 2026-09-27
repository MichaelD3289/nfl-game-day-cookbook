---
name: creating-release
description: Cut a new version of the NFL cookbook - pick the correct SemVer bump from CHANGELOG [Unreleased], bump with `uv version`, date the changelog, then commit for automatic tagging on main. Use when the user asks to release, cut, tag or bump a version.
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
  entries require which bump and ask before continuing. Never pick a smaller bump than
  the entries require.
- If an entry looks misfiled, for example a breaking change under `Fixed`, point it out
  before releasing.

## Steps

1. **Prepare the release for `main`.** Commit pending work first using the
   `logical-commits` skill. A release commit contains only version and changelog changes.
   It may be prepared on a review branch, but publication happens only after it reaches
   `main`. Never create or push tags manually; the workflow owns tagging.
2. **Preview the bump:**
   `uv version --bump <major|minor|patch> --dry-run`
   This prints `old => new` and writes nothing.
3. **Apply it:**
   `uv version --bump <major|minor|patch>`
   This updates `pyproject.toml` and re-locks `uv.lock`. Never edit the version by hand.
   Read the new version back with `uv version --short`.
4. **Date the changelog.** Rename `## [Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD`, using
   today's date in the maintainer's local time zone, not UTC. Agents and CI often run on
   UTC, which is already the next day in the maintainer's evening; if you cannot tell the
   local date, ask. Add a fresh, empty `## [Unreleased]` above it. If a remote exists, add
   or refresh the compare links at the bottom.
5. **Verify.** Run `make check`, `make pdf`, `make website` and `make epub`. All must pass,
   and `make pdf` must show no overflow warnings.
6. **Commit:**
   `git add pyproject.toml uv.lock CHANGELOG.md`
   `git commit -m "chore(release): X.Y.Z"`
   No AI attribution.
7. **Merge/push the release commit to `main`.** Do not run `git tag` or push tags.
   `.github/workflows/auto-tag.yml` reads the pushed commit's `pyproject.toml` and
   compares its stable `X.Y.Z` version numerically with all existing stable version tags.
   A higher version creates an annotated tag at that commit and directly calls
   `.github/workflows/release.yml`. Equal or lower versions do not create tags.
   Unsupported prerelease/development versions fail with a clear error.
8. **Verify publication.** The release workflow checks main ancestry and the package
   version, validates and builds PDF/HTML/EPUB, publishes all three, and deploys the newest
   stable release to Pages. Report the workflow result and release URL.
   Rerun a failed automatic workflow to reuse its tag at the same commit. For existing
   assets, the Release workflow also supports manual rebuilding with an existing tag
   (`gh workflow run release.yml --ref main -f tag=vX.Y.Z`); this never creates a tag.
   Never move an already pushed tag. If a fix changes code or workflows, prepare a new
   version using the bump rules above and merge it into `main`.

## Existing tags and merge behavior

The comparison uses the highest stable version number, not the newest tag by date.
Both a merged branch and a direct push to `main` follow these rules:

| State at the pushed `main` commit                                                       | Automatic result                                      |
| --------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| Package version is higher than every existing stable tag                                | Create the version tag at this commit and run Release |
| Package version equals the highest stable tag, and that tag points to this exact commit | Reuse the tag and run Release (safe retry)            |
| Same version tag points to a different commit                                           | Skip; never move the existing tag                     |
| Package version is lower than the highest stable tag                                    | Skip, even if an older tag points to this commit      |
| A tag is pushed without a push to `main`                                                | No automatic publication                              |

Tags only present locally are invisible to CI. Do not pre-tag feature branches.
Squash merges and merge commits change the commit identity; a pre-existing feature
branch tag will not be reused at the resulting main commit. A fast-forward preserves
identity, but tag reuse still requires the highest stable version and exact commit.
If an existing tag prevents publication, prepare a newer version; never retag it.
Manual rebuilding of an existing tag is separate from automatic tagging and still
requires that tag's commit to be in `main` history. The workflow cannot prohibit an
administrator from creating tags; these are project rules, not a GitHub tag ruleset.
