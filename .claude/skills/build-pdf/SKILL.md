---
name: build-pdf
description: Build, preview or troubleshoot the cookbook PDFs (book, recipe cards, division booklets): make pdf/cards, nfl-book build/preview, Quarto/LaTeX errors, overflow warnings, missing anchors.
---

# Build the PDFs

## Commands

| Goal                                                  | Command                                     |
| ----------------------------------------------------- | ------------------------------------------- |
| Short links (network), then the full book             | `make book` (`make links`, then `make pdf`) |
| Full book, failing on page overflows (PR check)       | `uv run nfl-book build --strict`            |
| Recipe-card PDF, failing on card overflows (PR check) | `uv run nfl-book cards --strict`            |
| QMD only, no Quarto needed                            | `uv run nfl-book build --no-pdf`            |
| One recipe or component, drafts allowed               | `make preview FILE=<path>`                  |

Other targets (`make booklets`, `make website`, `make epub`, `build --division afc/east`)
are in the `Makefile` and `uv run nfl-book --help`.

The book goes to `dist/` under `output_filename` in `data/book.yml`. Intermediate files
go to `generated/book/`: `book.qmd`, `pages/NNN-*.qmd`, `book.tex`, `book.log` and
`manifest.json`. Read them for debugging; regenerate them to change them.

## Requirements

- `uv sync`, plus Quarto and TinyTeX (`quarto install tinytex`), installed by the user.
- `validate`, `--no-pdf` and `make check` work without Quarto (Quarto-marked tests
  skip). The book, cards, booklets, website and EPUB all need it.
- Without Quarto, open the PR: its **Build PDF** check runs `pytest -m pdf`,
  `nfl-book build --strict` and `nfl-book cards --strict` once the PR is ready for
  review (not while it is a draft).

## Reading the output

- `<file>: error [code] ...` means validation failed. The message names the source
  file; fix that file.
- `recipe:<id> overflows its page (pages N-M)`: the content is too long for one page.
  See `update-recipe` → "Fixing an overflow", or `layout-changes` if many recipes
  overflow.
- `recipe:<id> overflows its 2-page limit (pages N-M)`, from `cards`: the recipe runs
  past its card limit. Shorten it the same way.
- `menu:<id> overflows its page (pages N-M)`: a game-day menu page runs onto another
  page. The label is the page's first menu; the content that grew may be in either
  card. Shorten the menu's text (see `menus-and-dish-offs`).
- `division:<key> overflows its page (pages N-M)`: the division page (team recipe lists
  plus dish-off cards) runs onto another page. Shorten the dish-off text, or see
  `layout-changes` if the recipe lists alone no longer fit.
- Missing anchor or label errors mean a template or macro stopped emitting
  `\BookAnchor{...}` / `\BookEnd{...}`, so the post-build page map no longer matches
  `manifest.json`. Look at the most recent template or style change.
- LaTeX errors: search `generated/book/book.log` for `^!`, then map the failing page
  back to its `generated/book/pages/*.qmd` and from there to the source file or
  template.

## Viewing pages without a PDF viewer

Render a page to PNG for visual checks. The source PDF is 1-indexed; PyMuPDF's page
index is 0-based. PyMuPDF is not a project dependency: `uv run --no-project --with`
loads it into a throwaway environment and adds nothing to the lockfile.

```sh
uv run --no-project --with pymupdf python -c "
import pymupdf; d=pymupdf.open('dist/nfl-game-day-recipe-booklet.pdf')
d[PAGE-1].get_pixmap(dpi=60).save('/path/to/scratch/page.png')"
```

Then read the PNG. Write scratch files outside the repo.

## Done when

`uv run nfl-book build --strict` and `uv run nfl-book cards --strict` both exit 0, and
`make check` is green. These are the commands the PR's Build PDF check runs.
