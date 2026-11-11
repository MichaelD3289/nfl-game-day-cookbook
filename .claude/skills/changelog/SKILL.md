---
name: changelog
description: Write CHANGELOG.md entries (Keep a Changelog) for user-visible changes to the NFL cookbook - content, layout, CLI, Make targets, config, hooks, agent rules or skills.
---

# Changelog entries

`CHANGELOG.md` follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/).
This skill is the single source for its format.

Every user-visible change gets a bullet under `## [Unreleased]` in the same change that
makes it. Use only these subsections, in this order, and add a missing one in its place:

1. `Added`
2. `Changed`
3. `Deprecated`
4. `Removed`
5. `Fixed`
6. `Security`

Each bullet describes the effect for a reader of the book or a user of the tooling in
one or two plain sentences, not the commit that made it. A real entry:

```markdown
### Fixed

- Recipe cards render Unicode fractions on fresh TeX installations without requiring
  the optional `newunicodechar` package or downloading it during builds.
```

Short ones work too: "Added Buffalo sliders (Bills)."

- If an existing `[Unreleased]` bullet already covers your change, extend that bullet.
- Start the bullet with **BREAKING:** for an incompatible change, for example a renamed
  front-matter field or a removed CLI command. `creating-release` picks the version from
  these markers and the section names.

Done when each user-visible effect of the change has exactly one bullet under
`[Unreleased]`, in the right section, and `[Unreleased]` keeps its name.
