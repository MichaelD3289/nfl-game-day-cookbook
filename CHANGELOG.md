# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Queue Dependabot pull requests for squash auto-merge once human review and required validation pass, without automatically approving changes.

- MIT licensing for software/developer documentation and CC BY 4.0 for original cookbook content, with explicit third-party exclusions and contribution terms.

- Read-only PR validation, owner review routing, recipe, component, division dish-off, game-day menu, and PR templates, contributor guidance, conduct/security policies, and weekly GitHub Actions dependency updates.

### Changed

- Agent rules now ask for each task to run in a git worktree under `.worktrees/`, removed after its branch is merged; `.worktrees/` is git-ignored.

- Organize README links into a read/download table with the public cookbook website, PDF, and HTML archive, plus release assets and earlier versions.

### Fixed

- AFC recipes follow their sources more closely: Boston cream pie, clam chowder, Cuban frita and Cuban sandwich, cheese coneys, Cincinnati chili, Polish Boy, Nashville hot chicken, green chile burritos, both French dips (yield, onion and jus note), and LA street dogs (jalapeños cooked, finishing salt).

- NFC recipes follow their sources more closely: black-and-white cookies, New York pizza, Giants pastrami (Katz's warming method correctly credited), Chicago and Detroit dogs, beer brats, booyah, Jucy Lucy, deviled crab, Tampa Cuban, peach cobbler, beignets, jambalaya, muffuletta, red beans, Mission burritos, fry bread tacos, half-smokes, Philly cheesesteak, roast pork and water ice.

- Recipe adaptations and editorial estimates are now labeled as such, including the Buffalo wing dip note, New York bagel framing, Jets pastrami assembly, and the chicken-finger, guacamole, prime rib jus and hotdish sauce components.

- The Kansas City burnt ends rub is now labeled as a half batch of AmazingRibs' Big Bad Beef Rub.

## [0.5.0] - 2026-09-26

### Added

- Automatically tag newer package versions on pushes to `main` and call the release workflow; manual tagging is no longer part of publishing. Failed runs can reuse their existing tag without moving it.

### Fixed

- Authenticate Quarto's TinyTeX release lookup during CI setup to avoid anonymous GitHub API limits.
- Require release tags to point to commits on `main`, with tagging owned by the main-branch workflow. Agent rules, the release skill, and README document exact-commit retries and how existing tags interact with merges.

## [0.4.0] - 2026-09-26

### Added

- Short dish descriptions on website recipe lists, with editable descriptions added
  to all 90 recipe files. These summaries do not change the printed booklet.
- Compact game-day menu cards show the included dishes and link to each recipe
  and the full menu's prep plan.

- `make website` builds a searchable, mobile-friendly HTML cookbook from the same
  published sources, with matching recipe cards, indexes and scratch-component links.
- Version-tag releases include a downloadable website archive and deploy the newest
  stable version to GitHub Pages; older tags and prereleases cannot replace it.

- README download link that automatically follows the latest released cookbook PDF,
  with links to all assets for the latest release, release notes and earlier versions.

- `review-recipes` agent skill: research workers check a recipe, a list, a team or
  division, or the whole book for city fit, authenticity, source fidelity, ingredient
  specificity and Make It or Buy It coverage, and report proposed fixes by default.
- Optional `last_reviewed_at` and `last_reviewed_notes` recipe metadata for editorial
  reviews. They never print; existing recipes start with empty fields.

## [0.3.1] - 2026-09-26

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


[Unreleased]: https://github.com/MichaelD3289/nfl-game-day-cookbook/compare/v0.5.0...HEAD
[0.5.0]: https://github.com/MichaelD3289/nfl-game-day-cookbook/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/MichaelD3289/nfl-game-day-cookbook/compare/v0.3.1...v0.4.0
[0.3.1]: https://github.com/MichaelD3289/nfl-game-day-cookbook/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/MichaelD3289/nfl-game-day-cookbook/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/MichaelD3289/nfl-game-day-cookbook/compare/631ec41...v0.2.0
[0.1.0]: https://github.com/MichaelD3289/nfl-game-day-cookbook/commit/631ec41
