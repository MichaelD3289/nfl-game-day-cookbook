---
name: build-pdf
description: Build, preview or troubleshoot the cookbook PDF (make pdf, nfl-book build/preview, Quarto/LaTeX errors, overflow warnings, missing anchors).
---

# Build the PDF

## Commands

| Goal | Command |
| --- | --- |
| Everything: short links (network), then the full book | `make book`, which runs `make links` then `make pdf` |
| Full book (published content only), offline | `make pdf`, which runs `uv run nfl-book build` |
| Treat warnings as errors | `uv run nfl-book build --strict` |
| Generate QMD only (no Quarto needed) | `uv run nfl-book build --no-pdf` |
| One recipe or component, drafts allowed | `make preview FILE=<path>` |
| Clean output | `make clean` |
| Lint, types, tests and validation | `make check` |

The output goes to `dist/nfl-game-day-recipe-booklet.pdf` (the name is set in
`data/book.yml`). Intermediate files go to `generated/book/`: `book.qmd`,
`pages/NNN-*.qmd`, `book.tex`, `book.log` and `manifest.json`. All of this is
git-ignored build output. Read it for debugging, but never edit or commit it.

## Requirements

- `uv sync`
- Quarto and TinyTeX (`quarto install tinytex`). **The user installs these.** Never
  install system software yourself; ask the user to.
- Everything except the final PDF works without them.

## Pipeline

1. discover + validate
2. resolve (published only)
3. Jinja2 (`templates/`) → QMD
4. Quarto + pdflatex, using `styles/theme.tex` and `styles/book.tex`
5. post-build: PDF named destinations → `generated/pagemap.json`, checked against
   `manifest.json`

## Reading the output

- `<file>: error ...` means validation failed. The message names the source file;
  fix that file.
- `recipe:<id> overflows its page (pages N-M)`: the content is too long for one
  page. See `update-recipe` → "Fixing an overflow", or `layout-changes` if many
  recipes overflow.
- Missing anchor or label errors mean a template or macro stopped emitting
  `\BookAnchor{...}` / `\BookEnd{...}`. Look at the most recent template or style
  change.
- LaTeX errors: search `generated/book/book.log` for `^!`, then map the failing
  page back to its `generated/book/pages/*.qmd` and from there to the source file
  or template.

## Viewing pages without a PDF viewer

Render a page to PNG for visual checks. The source PDF is 1-indexed; PyMuPDF's
page index is 0-based.

```sh
uv run --no-project --with pymupdf python -c "
import pymupdf; d=pymupdf.open('dist/nfl-game-day-recipe-booklet.pdf')
d[PAGE-1].get_pixmap(dpi=60).save('/path/to/scratch/page.png')"
```

Then read the PNG. Write scratch files outside the repo.

## Done when

- `make pdf` produces no overflow warnings and no errors.
- `make check` is green.
