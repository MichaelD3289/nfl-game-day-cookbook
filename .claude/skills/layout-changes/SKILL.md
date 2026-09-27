---
name: layout-changes
description: Change how the cookbook looks - fonts, colours, margins, recipe page layout, photo size, columns, cards, templates or LaTeX macros. Use for any edit to styles/ or templates/.
---

# Layout changes

> **Working from a GitHub issue?** Claim it first ([AGENTS.md](../../../AGENTS.md) rule
> 15). If the issue already has the `in-progress` label, stop and ask a human; do not
> work on it without their explicit permission. Otherwise add the label before you
> change anything.

## Where things live

| File                           | Owns                                                                                                                                                                                             |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `styles/theme.tex`             | **All** colours, fonts, sizes and dimensions (for example `\BookPhotoWidth`, `\BookPhotoHeight`, `\BookIngredientsWidth`, `\BookInstructionsWidth`, `\BookBodySize`, `\BookNoteSize`, geometry)  |
| `styles/book.tex`              | Semantic macros (`\RecipePage`, `RecipeIngredients`, `KitchenNotes`, `\RecipeSource`, cards, index and contents pages). It contains no literal colours or sizes and refers only to theme tokens. |
| `templates/*.qmd.j2`           | Jinja2 (`<< >>` expressions, `<% %>` blocks) → QMD that calls those macros. `recipe.qmd.j2` and `_macros.qmd.j2` render recipe pages.                                                            |
| `src/nfl_book/render/pages.py` | Builds the template context (for example `compact_ingredients`, and `COMPACT_INGREDIENTS_OVER = 24`).                                                                                            |

## Rules

1. To restyle, edit the tokens in `theme.tex`. Never hard-code a colour or size in
   `book.tex` or in a template.
2. Every recipe must stay **one page**, matching the print booklet:
   - a photo at the top right beside the title
   - two columns for ingredients and instructions
   - compact Kitchen Notes
   - source text and QR code at the bottom
     Photo pixel size, format and quality for each output live under `photos:` in
     `data/book.yml` (the book and site crop every photo to a centred square). The
     printed size of the photo box is set in `theme.tex`.
3. Never compute or print page numbers from Python. Use `\BookAnchor` together with
   `\BookPageRef` / `\ComponentRef`.
4. Keep every `\BookAnchor{<label>}` and `\BookEnd{<end_label>}` in place. The
   post-build checks and the overflow check depend on them.
5. `\RecipeMeta` is still used by `component.qmd.j2`. Before removing or renaming
   a macro, run `grep -rn "\\MacroName" templates styles`.
6. Pass values through the `|tex` filter in templates (and `|tex_url` for URLs).
7. Don't change recipe content to fix a layout problem, and don't change the
   layout to fix one long recipe.

## Workflow

1. Take a baseline:
   ```sh
   make pdf 2>&1 | grep -c overflows
   ```
2. Make the change.
3. Rebuild:
   ```sh
   make pdf 2>&1 | grep -E "overflows|error"
   ```
4. Visually check a dense page (for example meat-and-three, mission-style
   burritos or muffuletta), a recipe without a photo, a component page and an
   index page. Render pages to PNG as described in the `build-pdf` skill.
   - For reference, the original booklet uses letter paper, about 0.67in margins,
     9.4pt body text and a 120pt square photo at the top right.
5. If `pages.py` changed, add or adjust a test in `tests/unit/test_pages.py`.
6. Run `make check`.
7. Add a `CHANGELOG.md` entry under `[Unreleased]` → `Changed`.

## Website layout

`templates/website/*.qmd.j2` and `styles/website.css` are the separate HTML
presentation. `src/nfl_book/website.py` reuses the resolved book's page contexts,
then Quarto produces `dist/site/`. The print-only rules above (one page, TeX tokens,
page anchors and LaTeX filters) apply to PDF templates, not these web templates.
Preserve the shared palette, Q cards, and source content; use responsive columns
and normal links instead of page numbers. Never change recipes to fit the screen.

Run `make website` and inspect home, a dense recipe, a component, and an index at
desktop and phone widths. The build checks local links, images and fragments.
Keep published-only and private-metadata tests green with `make check`. Do not
edit the PDF templates or styles when making a website-only layout change.

### Raw HTML and tests: Quarto rewrites your markup

Raw ` ```{=html} ` blocks in the web templates reach `dist/site/` only after
Quarto re-serializes them. The markup changes on the way. A bare `hidden` becomes
`hidden=""`, attribute order and quoting can change, and whitespace moves. The
generated `.qmd` (`nfl-book website --no-render`) keeps your exact text, so a test
that passes there can still fail in the release build, which renders with Quarto.
This happened in 0.9.0 and needed the 0.9.1 fix.

- Unit tests in `tests/unit/test_website.py` read the generated `.qmd` and may match
  exact strings.
- Tests of the **rendered** site (`tests/integration/test_website_build.py`) must
  compare attributes, not markup. Use its `_elements(html, tag, css_class)` helper and
  assert on the returned dict, for example `assert "hidden" in bars[0]`. Never assert
  `'<div class="x" hidden>' in page`.
- Those integration tests are skipped when Quarto is not installed, and `make check`
  still passes. If you cannot run them, say so in the PR. Do not treat a skip as a pass.
- Controls that need JavaScript (the scaler, the Print button, the no-account suggest
  button) ship with `hidden` and are revealed by their script. Keep that pattern so
  readers without JavaScript never see a button that does nothing.

## EPUB layout

EPUB uses `templates/epub/`, `styles/epub.css` and `src/nfl_book/epub.py`. It reflows
to the reader's screen and font settings; the PDF one-page, two-column, and
printed-page-number rules above apply only to print. Preserve linked anchors and
source/photo credits.

- **Headings decide the pages.** The EPUB starts a new file at every heading of level
  1–3 (`epub-chapter-level: 3`). Book sections are `#`; teams, division dish-offs,
  menu types and component kinds are `##`; each recipe, component and game-day menu
  is `###`. Anything inside a
  recipe or component (Ingredients, Method, Quick options, Kitchen notes) must be
  `####` or it splits the recipe across pages. Use bold labels, not headings, for
  groupings inside a page (contents, index sections, Make It or Buy It lists).
- **Section openers come from `epub.py`:** team and component-kind headings are added
  between pages, and a menu type's heading is printed once (`continued`).
- **Labels (`{.eyebrow}`) go after their heading**, never before it.
- The EPUB links each recipe to its page in this edition of the website instead of a
  QR code, and shows full source URLs, not print short links.
- Check the structure with `nfl-book epub --no-render` and the tests in
  `tests/unit/test_epub.py`. Run `make epub` (needs Quarto) and look at a recipe, a
  component, a division menu and an index in a reader (Apple Books, Calibre) at a few
  text sizes. Run EPUBCheck separately when changing packaging.
