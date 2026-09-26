# Cookbook layout guide

The Reader Layout booklet is the visual reference. Styling belongs in shared
rules, not individual recipe files. Content edits must not be used to hide overflow.

## Cover

- Left-align the serif title and subtitle beside the gold vertical accent.
- Retain the slim blue top strip and muted tagline; avoid a duplicate statistics panel.
- Give the introductory paragraphs their own inset column and generous line spacing.
- Render the same Q badge used in recipes in the cover legend.
- Set timing/cost guidance in the smaller `CoverFinePrint` style.

## Cards

- Use the shared blue-gray background, rounded corners and no visible border.
- Use blue uppercase labels and dark serif titles for menu and division cards.
- Game-day pages carry a visible heading and two consistently sized cards. Matchup
  subtitles sit below the title; recipe page references align to the right.
- Division cards pair side by side with equal heights. Recipe lists precede their
  short description and preparation note.
- Recipe quick options always follow the two-column ingredients/instructions area,
  before Kitchen Notes. Their Q markers and page links continue to use component IDs.
- Component pages combine the purchased option and explanatory note in one panel,
  below the scratch instructions. Keep the used-in links outside that panel.
- Kitchen Notes use an unfilled, quiet treatment so they do not compete with Q cards.

## Ownership and checks

`styles/theme.tex` owns palette, typography and dimensions. `styles/book.tex`
owns semantic macros. Templates choose placement; they must preserve anchors,
source links and the `tex`/`tex_url` escaping filters.

Use the `BookCover*`, `BookCard*`, `BookMenu*` and `BookQ*` tokens to tune these
layouts. Do not copy literal measurements into templates or recipe content.

After changes, rebuild and visually inspect the cover, a division, a game-day menu,
a component, a dense recipe, a recipe without a photo, and an index. Check every
recipe's one-page span and run `make check`. Longer future menu content must be
checked visually against the shared card height.

Validated 2026-09-26: 152-page production build, no recipe overflow warnings,
no overfull LaTeX boxes, 100 tests passing, zero content-validation warnings.
