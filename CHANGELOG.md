# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- Rebuilding an older tag with the release workflow no longer marks it as the latest
  release, so the latest-download link always serves the newest version.
- Buffalo wings keep their unbreaded deep-frying method, use the linked homemade
  sauce and dip, and explain the classic hot-sauce-and-butter option.
- Corrected sauce and dip references on Bills recipes and barbecue chicken so Q
  options replace finished components, not individual base ingredients.
- Updated affected recipe timing and the chicken-finger sub's practical-time index;
  clarified scratch preparation versus quick assembly.

## [0.3.0] - 2026-09-26

### Added

- `logical-commits` agent skill, and an `AGENTS.md` rule that every commit follows it:
  Conventional Commits, one green change per commit with its own changelog entry, and
  a plan approved before staging.
- `CLAUDE.md` imports `AGENTS.md`, so Claude Code sessions load the agent rules.
- `creating-release` agent skill: picks the SemVer bump from `[Unreleased]`, bumps with
  `uv version --bump`, dates the changelog, then commits and tags.
- GitHub Actions release workflow: pushing a `v*` tag builds the book and publishes
  the PDF to a GitHub Release, with that version's changelog section as the notes.
  It can also be run manually for any existing tag.

### Changed

- The `release` skill is now `changelog`, which covers writing entries only; releases
  moved to `creating-release`.

### Fixed

- Source QR codes now encode the full source URL instead of the short link; the
  printed link text still shows the short URL.

## [0.2.0] - 2026-09-26

### Added

- PyPI keywords and trove classifiers in `pyproject.toml`.
- Agent skills in `.claude/skills/` for adding and updating recipes, components,
  menus, search indexes and source links, building the PDF, layout changes and releases.
- `make links` target that runs `nfl-book prepare-links`.
- `make book` target that runs `make links` then `make pdf`.
- `docs/layout-guide.md`, the house rules for the cover, cards and recipe pages, and
  the scratch-component source review in `docs/reviews/`.

### Changed

- Cover now follows the reference booklet's left-aligned title, gold accent,
  generous paragraph spacing and illustrated Q-marker legend.
- Shared cards use the reference blue-gray palette, rounded borderless panels,
  larger menu titles and consistent spacing. Game-day menus have full page headings.
- Quick-option cards follow recipe instructions; component shortcuts and notes share
  one panel. The Q badge is blue and rounded throughout the book.
- `AGENTS.md` now points to the task skills; the "import not started" notice is
  removed.
- `AGENTS.md` requires every agent to record its changes under `[Unreleased]` in
  this changelog.
- Package author email is now the GitHub noreply address.

### Fixed

- Reviewed all 21 Make It or Buy It components against their sources; corrected
  missing ingredients, preparation details, yields, timing and shortcut wording.
- Buffalo sauce now includes Chef John's homemade version.
- Replaced mismatched source links for pico de gallo, grits, horseradish cream and
  cocktail sauce; cached five new short URLs without replacing existing links.

## [0.1.0] - 2026-09-26

### Added

- Book-as-code pipeline (`nfl_book`, managed with uv): Markdown/YAML content is
  validated with Pydantic, resolved into a book model, rendered to Quarto QMD with
  Jinja2 and compiled to a letter-size PDF with Quarto + LaTeX.
- LaTeX-resolved cross-references: every recipe, component, menu, division and index
  gets a stable label, and all page numbers come from LaTeX. The build warns when a
  recipe overflows its page.
- `nfl-book` CLI with `validate`, `prepare-links`, `preview`, `build`, `clean` and
  `new`, plus `make check`, `make preview` and `make pdf` targets.
- `prepare-links`, the only networked stage, caches short links in
  `data/shortlinks.yml` and generates source QR codes.
- Content imported from the "NFL Meals Game Day Recipe Booklet":
  - 90 recipes across all 32 teams and 8 divisions, with photos.
  - 21 "Make It or Buy It" components (dips, proteins, sauces, seasonings, sides,
    staples, toppings) with quick-buy options.
  - 32 game-day menus and 16 division dish-offs.
  - Cover copy and 104 cached source short links.
- Generated indexes by course, main ingredient, practical time and ingredient cost.
- One-page recipe layout matching the print booklet: a photo beside the title, two
  columns for ingredients and instructions, and compact Kitchen Notes. Recipes with
  more than 24 ingredient lines set each group as a run-in paragraph.
- Unit and integration tests against a synthetic sample book.


[Unreleased]: https://github.com/MichaelD3289/nfl-game-day-cookbook/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/MichaelD3289/nfl-game-day-cookbook/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/MichaelD3289/nfl-game-day-cookbook/compare/631ec41...v0.2.0
[0.1.0]: https://github.com/MichaelD3289/nfl-game-day-cookbook/commit/631ec41
