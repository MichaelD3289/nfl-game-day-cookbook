---
name: layout-changes
description: Change how the cookbook looks - fonts, colours, margins, recipe page layout, photo size, columns, recipe cards, website or EPUB styling, templates or LaTeX macros. Use for any edit to styles/ or templates/.
---

# Layout changes

Website-only change (`templates/website/`, `styles/website*`): read
[website.md](website.md). EPUB change (`templates/epub/`, `styles/epub.css`): read
[epub.md](epub.md). Everything below is the print layout.

## Where things live

| File                                   | Owns                                                                                                                                          |
| -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `styles/theme.tex`                     | All colours, fonts, sizes and dimensions (`\Book*` lengths and font commands, geometry), shared by the book and the cards                     |
| `styles/book.tex`                      | Semantic macros for the book (`\RecipePage`, `RecipeIngredients`, `KitchenNotes`, `\RecipeSource`, tcolorbox cards, index and contents pages) |
| `styles/cards.tex`, `templates/cards/` | The recipe-card PDF (`make cards`)                                                                                                            |
| `templates/*.qmd.j2`                   | Jinja2 (`<< >>` expressions, `<% %>` blocks) → QMD that calls those macros. `recipe.qmd.j2` and `_macros.qmd.j2` render recipe pages.         |
| `src/nfl_book/render/pages.py`         | Builds the template context (for example `compact_ingredients` for long lists)                                                                |
| `photos:` in `data/book.yml`           | Photo pixel size, format and quality for each output (the book and site crop every photo to a centred square)                                 |

## Rules

1. Add every new colour, font and dimension as a named token in `theme.tex`, and refer
   to it by name from `book.tex`, `cards.tex` and templates. `book.tex` still has older
   literal spacing; tokenise any of it you touch. The printed photo box size is a
   `theme.tex` token.
2. **The print contract:** every recipe stays on one page, matching the print booklet:
   - a photo at the top right beside the title
   - two columns for ingredients and instructions
   - compact Kitchen Notes
   - source text and QR code at the bottom
3. Cross-references use `\BookAnchor` with `\BookPageRef` / `\ComponentRef`.
4. Keep every `\BookAnchor{<label>}` and `\BookEnd{<end_label>}` in place. The
   post-build checks and the overflow check depend on them.
5. Before removing or renaming a macro, find its uses with
   `rg -n '\\MacroName' templates styles`.
6. Pass values through the `|tex` filter in templates (and `|tex_url` for URLs).
7. A layout problem is fixed in the layout, and one long recipe is fixed in its content
   (`update-recipe` → "Fixing an overflow").

## Workflow

1. Take a baseline: build the book and the cards per `build-pdf` without `--strict`,
   and count the overflow warnings of each.
2. Make the change.
3. Rebuild both. Done when neither overflow count is above its baseline and there are
   no errors.
4. Render pages to PNG per `build-pdf` and check a dense page (for example
   meat-and-three, mission-style burritos or muffuletta), a recipe without a photo, a
   component page, an index page and a recipe card. Done when each one holds the print
   contract. For reference, the original booklet uses letter paper, about 0.67in
   margins, 9.4pt body text and a 120pt square photo at the top right.
5. If `pages.py` changed, add or adjust a test in `tests/unit/test_pages.py`.

Done when `build-pdf`'s done-criteria hold. The CHANGELOG entry goes under `Changed`.
