# NFL Game Day Cookbook

**[Download the latest cookbook (PDF)](https://github.com/MichaelD3289/nfl-game-day-cookbook/releases/latest/download/nfl-game-day-recipe-booklet.pdf)**

This link follows the latest published release automatically.

[View all assets for the latest release](https://github.com/MichaelD3289/nfl-game-day-cookbook/releases/latest) ·
[View release notes and earlier versions](https://github.com/MichaelD3289/nfl-game-day-cookbook/releases).

A "book as code" pipeline. Recipes are authored as Markdown with YAML front matter.
The pipeline validates them, resolves them into a book model, renders that model to
Quarto QMD through Jinja2 templates, and compiles a PDF with Quarto + LaTeX. LaTeX
resolves every page number from labels. Python never computes one.

```
Markdown/YAML ──discover──▶ Pydantic models ──validate──▶ resolve (published only)
      ──▶ Jinja2 ─▶ generated/book/*.qmd + manifest.json ──quarto/LaTeX──▶ dist/*.pdf
      ──▶ post-build: PDF named destinations ─▶ pagemap.json ─▶ manifest checks
```

## Requirements

- [uv](https://docs.astral.sh/uv/). Python and every Python dependency are managed with
  `uv sync`.
- For PDFs only: [Quarto](https://quarto.org) and TinyTeX (`quarto install tinytex`).
  Everything else, including validation, QMD generation and the tests, works without
  them.

## Layout

| Path | What |
| --- | --- |
| `data/book.yml` | Book title, paper and output settings |
| `data/nfl.yml` | Conferences, divisions and 32 teams (drives the directory layout) |
| `data/indexes.yml` | Search-index definitions (course, main ingredient, ...) |
| `data/menu-types.yml`, `data/component-kinds.yml` | Menu groups and "Make It or Buy It" kinds |
| `data/shortlinks.yml` | Cached source URL → short URL (written only by `prepare-links`) |
| `recipes/<conf>/<div>/<team>/<id>.md` | One recipe. Its team comes from the path |
| `components/<kind>/<id>.md` | Shared sauces, dips, seasonings, ... |
| `menus/game-day/<type>/<id>.yml` | Game-day menus |
| `menus/divisions/<conf>/<div>/<id>.yml` | Division dish-offs |
| `book/frontmatter/cover.md` | Cover copy |
| `templates/`, `styles/` | Jinja2 QMD templates and LaTeX styles |
| `generated/`, `dist/` | Build output (git-ignored, never edited) |
| `tests/fixtures/sample-book/` | Synthetic content used by the tests |

## Content format

```markdown
---
id: buffalo-sliders            # must match the file name
title: Buffalo Chicken Sliders
status: draft                  # draft | testing | published | retired
course: appetizers             # a bucket of the `course` index
yield: 12 sliders
index:                         # one value per index in data/indexes.yml
  main_ingredient: poultry
  practical_time: under-30-minutes
  cost: pantry-friendly
quick_options:                 # optional per-recipe override of a component's quick_buy
  wing-sauce: Frank's RedHot Wings Sauce
source:
  url: https://example.com/full/original/url
---

## Ingredients

- 1 cup wing sauce {{component:wing-sauce}}

## Instructions

...
```

Components use the sections `## Ingredients`, `## From Scratch` and an optional
`## Note`, plus the front-matter fields `quick_buy` and `always_include`. A component
that no published recipe reaches (directly or through other components) is left out of
the book unless it sets `always_include: true`.

## Commands

```sh
uv sync                                   # install
make book                                 # everything: make links, then make pdf
uv run nfl-book validate [PATHS...]       # validate everything (optionally report only PATHS)
uv run nfl-book prepare-links             # the ONLY network step (or `make links`): fill data/shortlinks.yml
uv run nfl-book preview PATH [--no-pdf]   # render one recipe/component (drafts allowed)
uv run nfl-book build [--no-pdf] [--strict]   # published-only book -> dist/
uv run nfl-book clean                     # remove generated/ and dist/
uv run nfl-book new recipe --team bills --slug buffalo-sliders
uv run nfl-book new component --kind sauces --slug wing-sauce
```

Global options `--root`, `--content`, `--generated` and `--dist` point the CLI at
another content tree. For example, to build the fixture book:

```sh
D=$(mktemp -d); cp -R tests/fixtures/sample-book/. "$D"; cp data/{book,nfl,indexes,menu-types,component-kinds}.yml "$D/data/"
uv run nfl-book --content "$D" --generated "$D/generated" --dist "$D/dist" build --no-pdf
```

Make targets: `make check` (lint, tests, validate), `make test`, `make lint`,
`make preview FILE=...`, `make pdf` and `make clean`.

## How page numbers work

Every page places LaTeX labels (`recipe:<id>`, `recipe:<id>:end`, `component:<id>`,
`division:<key>`, `menu:<id>`, `index:<id>`, ...). Indexes, contents and "used in" lists
print `\pageref`-style references to those labels. After compiling, the build reads the
PDF's named destinations into `generated/pagemap.json`, then checks them against
`generated/book/manifest.json`. Every expected anchor must exist, and a recipe should
start and end on the same page. Overflows are warnings, or errors with `--strict`.

## Shortlinks and QR codes

Source URLs in front matter are always full, canonical URLs. `prepare-links` shortens
any uncached URL of published content and appends the result to `data/shortlinks.yml`.
It never rewrites existing entries or source files. Builds read that cache offline, so
a published recipe whose URL is missing from it fails validation. QR codes are generated
deterministically from the full source URL; the printed link text uses the short URL.

See `AGENTS.md` for the rules contributors (human or AI) follow.

## Recipe quality reviews

Use the project Claude skill: `/review-recipes buffalo-wings`,
`/review-recipes buffalo-wings, beer-brats`, `/review-recipes afc/east/bills`, or
`/review-recipes all`.
It coordinates research workers and an editorial orchestrator across city fit,
authenticity, source fidelity, ingredient specificity and Make It or Buy It coverage.
Default mode recommends corrections and records completed-review metadata;
`--apply` also applies adjudicated fixes, while `--read-only` preserves metadata.
Reports go under `docs/reviews/`. See `.claude/skills/review-recipes/SKILL.md`.

Recipes support optional, non-printing metadata:

```yaml
last_reviewed_at: null  # or YYYY-MM-DD after a completed review
last_reviewed_notes: null  # outcome, outstanding findings and report path
```

A review date does not mean a recipe passed. Incomplete reviews do not replace
prior completed-review metadata. Existing recipes begin with empty fields; no
historical review dates are inferred. These fields do not affect booklet content.
