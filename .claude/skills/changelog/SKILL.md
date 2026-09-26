---
name: changelog
description: Write CHANGELOG.md entries (Keep a Changelog) for changes to the NFL cookbook. Use whenever a change is user-visible; cutting a version is the creating-release skill.
---

# Changelog entries

`CHANGELOG.md` follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/).

Every user-visible change gets a bullet under `## [Unreleased]` in the same change that
makes it. Use only these subsections, in this order:

1. `Added`
2. `Changed`
3. `Deprecated`
4. `Removed`
5. `Fixed`
6. `Security`

Write for a reader of the book or repo, not a commit log. Examples:
- "Added Buffalo sliders (Bills)."
- "Recipe photos now sit beside the title."

Mark incompatible changes with **BREAKING:** at the start of the bullet, for example a
renamed front-matter field or a removed CLI command. `creating-release` uses these
markers to choose the version.

Never rename `[Unreleased]` yourself. That is the `creating-release` skill's job.
