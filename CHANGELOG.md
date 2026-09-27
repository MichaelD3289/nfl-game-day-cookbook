# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.12.1] - 2026-09-26

### Changed

- Every recipe with a quick component now lists the homemade choice followed by an explicit store-bought substitution, with the component link kept at the end of the ingredient line. Batch quantities, measured portions and special substitution amounts are retained, and preparation instructions accommodate either choice.
- Recipe and component skills now document the shared homemade-or-store-bought wording, quantity and scaling conventions for future edits.
- The `creating-release` skill now dates a release by the maintainer's local day instead of UTC, so evening releases are no longer dated the following day.

## [0.12.0] - 2026-09-26

### Added

- Add `make epub` with the full reflowable cookbook, linked indexes and homemade components, embedded optimized photos, and package checks. Releases and download links include EPUB ([#19](https://github.com/MichaelD3289/nfl-game-day-cookbook/issues/19)).
- The EPUB opens each recipe, component, menu and section on its own page, with the indexes at the back. Each recipe shows its short description, lists yield and times on separate lines, and links to its page in this edition of the website. A **Q** beside an ingredient opens the recipe's Quick options card, and sources link to their full address.
- The EPUB has a cover, a description and rights details, and keeps the same identifier across editions, so reading apps treat a new edition as an update of the same book.
- The website's **All versions** page links each edition's EPUB next to its PDF.
- PR checks now render the website and EPUB with Quarto, so a rendering problem fails the pull request instead of the release.
- Formatting rules and pre-commit hooks: Ruff formats and lints Python, and Prettier formats Markdown, YAML, JSON, JavaScript and CSS with its default style. Run `make hooks` once so staged files are fixed at every commit, and `make format` to fix every file.

### Changed

- The `creating-release` skill now builds the website and EPUB before a release, and the `layout-changes` skill explains how headings decide EPUB pages.
- `make check`, and so the PR checks, now fail when any file is not formatted, not just Python in `src/` and `tests/`. The existing Markdown, YAML, JavaScript and CSS files were reformatted once to match; recipe content is unchanged.

## [0.11.0] - 2026-09-26

### Added

- Each recipe and component page in the PDF now links to its page in the same edition of the website (under `/vX.Y.Z/`), so the link matches the printing; newer editions are linked from there, and the cover explains this once. Set the site root with `website_url` in `data/book.yml`.

### Changed

- The QR code on each recipe and component page, in the PDF and on the website, now opens that page in this edition of the website instead of the recipe source, and pages without a source get one too. The PDF shows a short "View this page online" link instead of the full address, and the source stays a clickable link.

## [0.10.0] - 2026-09-26

### Added

- Recipe, component, game-day menu and division (dish-off) pages on the website have a **Print** button that prints just the page, without the site navigation, search or suggestion prompts. Most recipes fit on one Letter or A4 page; a scaled recipe prints its scaled amounts with a "Scaled 2× · serves 12" note, and every printout ends with the page's web address. The PDF is unchanged.

### Changed

- The `layout-changes` skill now explains that Quarto rewrites raw HTML in website pages (a bare `hidden` becomes `hidden=""`), so tests of the rendered site must compare attributes rather than exact markup.

## [0.9.1] - 2026-09-26

### Fixed

- The release build's rendered-website check no longer fails on the recipe scaling controls, which Quarto writes with `hidden=""` instead of a bare `hidden`. This unblocks publishing the 0.9 recipe scaling to the website.

## [0.9.0] - 2026-09-26

### Added

- Recipe and component pages on the website can be scaled from ½× to 4×, or by the number of people when the recipe has servings. Amounts switch to the most readable unit (tripling 4 teaspoons reads ¼ cup), counts stay whole, and the scale is kept in the page link and carried to linked components. The PDF is unchanged.
- Recipes accept an optional `servings` field (a number or a range such as `6-8`), and yields such as "6–8 servings" or "serves 6–10" are read automatically. Ingredient lines can be marked `{{no-scale}}` to keep their amount fixed, and validation reports amounts it cannot read, such as `500g`.
- Sandwich, burger, burrito, omelet and roll recipes list their servings, and deep-frying oil measured by pot depth is marked so it does not scale.

## [0.8.0] - 2026-09-26

### Added

- Every released website version stays online at `/vX.Y.Z/`, while the site root keeps serving the latest release. Older versions show a banner linking to the latest version, and a new **All versions** page lists each version with its date and PDF.

- The published website stores each image once across all versions, so a new release adds only its new or changed photos. Older versions keep the photos they were released with.

## [0.7.0] - 2026-09-26

### Added

- Project Claude Code settings (`.claude/settings.json`), shared by local and cloud sessions: no AI attribution in commits or pull requests, pre-approved routine checks (`make check`, tests, lint, read-only git), and blocks on reading `.env` files, editing `generated/` or `dist/`, and creating or pushing tags.

### Changed

- Creative Commons photo credits now say the photo was cropped and resized, and photo credits that were bare web addresses now name the publication or brand.
- Recipe photos are now cropped to a centred square and resized for each output: the website serves lazy-loaded WebP images of about 400px, and the PDF embeds small progressive JPEGs of about 500px with location and other metadata removed. Original photos in `recipes/` are never modified, and `nfl-book build` and `nfl-book website` report total photo size before and after.
- Photo size, format and quality for the website and PDF are set under `photos:` in `data/book.yml`. An unreadable photo now fails the build with an error that names the file.
- The Chicago tavern-style pizza recipe is shorter so it stays on one page with its full-size square photo.
- Agent rules now also forbid AI attribution in pull request titles and descriptions.

## [0.6.1] - 2026-09-26

### Changed

- Agent rules now ask for each task to run in a git worktree under `.worktrees/`, removed after its branch is merged; `.worktrees/` is git-ignored.

### Fixed

- AFC recipes follow their sources more closely: Boston cream pie, clam chowder, Cuban frita and Cuban sandwich, cheese coneys, Cincinnati chili, Polish Boy, Nashville hot chicken, green chile burritos, both French dips (yield, onion and jus note), and LA street dogs (jalapeños cooked, finishing salt).

- NFC recipes follow their sources more closely: black-and-white cookies, New York pizza, Giants pastrami (Katz's warming method correctly credited), Chicago and Detroit dogs, beer brats, booyah, Jucy Lucy, deviled crab, Tampa Cuban, peach cobbler, beignets, jambalaya, muffuletta, red beans, Mission burritos, fry bread tacos, half-smokes, Philly cheesesteak, roast pork and water ice.

- Recipe adaptations and editorial estimates are now labeled as such, including the Buffalo wing dip note, New York bagel framing, Jets pastrami assembly, and the chicken-finger, guacamole, prime rib jus and hotdish sauce components.

- Recipes that relied on paywalled or blocked sources now follow open, regionally attributed ones. Pit beef uses The Meatwave's charcoal-grilled bottom round, with a per-sandwich tiger sauce amount. Mumbo sauce wings use D.C. chef Anthony Thomas's recipe, and the Mumbo Meets Tex-Mex prep plan now marinates them ahead. Chicago giardiniera follows Lou Malnati's hot giardiniera, ready the next day instead of after a week. Viet-Cajun crawfish follows Edible Houston's lemongrass, ginger and citrus boil with garlic butter.

- The Kansas City burnt ends rub is now labeled as a half batch of AmazingRibs' Big Bad Beef Rub.

- The Cuban sandwich, roast pork, pimento cheese, fry bread tacos and mumbo sauce wings have new openly licensed photos, credited to their photographers and licenses.

## [0.6.0] - 2026-09-26

### Added

- Website pages have Suggest buttons for recipe and component edits, new recipes for a team, components, game-day menus, and division dish-offs. Each opens a prefilled GitHub issue form, and an optional form sends suggestions without a GitHub account.

- Quick issue templates for edits and for recipe, component, menu, and dish-off ideas, where one or two fields are enough; they are labelled `needs-research`.

- `suggestion_form_url` in `data/book.yml` turns on the no-account form. Its issues are labelled `anonymous-suggestion` and show who sent them. Setup and the Apps Script are in `docs/website-suggestions.md`.

- Queue Dependabot pull requests for squash auto-merge once human review and required validation pass, without automatically approving changes.

- MIT licensing for software/developer documentation and CC BY 4.0 for original cookbook content, with explicit third-party exclusions and contribution terms.

- Read-only PR validation, owner review routing, recipe, component, division dish-off, game-day menu, and PR templates, contributor guidance, conduct/security policies, and weekly GitHub Actions dependency updates.

### Changed

- Organize README links into a read/download table with the public cookbook website, PDF, and HTML archive, plus release assets and earlier versions.

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

[Unreleased]: https://github.com/MichaelD3289/nfl-game-day-cookbook/compare/v0.12.1...HEAD
[0.12.1]: https://github.com/MichaelD3289/nfl-game-day-cookbook/compare/v0.12.0...v0.12.1
[0.12.0]: https://github.com/MichaelD3289/nfl-game-day-cookbook/compare/v0.11.0...v0.12.0
[0.11.0]: https://github.com/MichaelD3289/nfl-game-day-cookbook/compare/v0.10.0...v0.11.0
[0.10.0]: https://github.com/MichaelD3289/nfl-game-day-cookbook/compare/v0.9.1...v0.10.0
[0.9.1]: https://github.com/MichaelD3289/nfl-game-day-cookbook/compare/v0.9.0...v0.9.1
[0.9.0]: https://github.com/MichaelD3289/nfl-game-day-cookbook/compare/v0.8.0...v0.9.0
[0.8.0]: https://github.com/MichaelD3289/nfl-game-day-cookbook/compare/v0.7.0...v0.8.0
[0.7.0]: https://github.com/MichaelD3289/nfl-game-day-cookbook/compare/v0.6.1...v0.7.0
[0.6.1]: https://github.com/MichaelD3289/nfl-game-day-cookbook/compare/v0.6.0...v0.6.1
[0.6.0]: https://github.com/MichaelD3289/nfl-game-day-cookbook/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/MichaelD3289/nfl-game-day-cookbook/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/MichaelD3289/nfl-game-day-cookbook/compare/v0.3.1...v0.4.0
[0.3.1]: https://github.com/MichaelD3289/nfl-game-day-cookbook/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/MichaelD3289/nfl-game-day-cookbook/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/MichaelD3289/nfl-game-day-cookbook/compare/631ec41...v0.2.0
[0.1.0]: https://github.com/MichaelD3289/nfl-game-day-cookbook/commit/631ec41
