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
  subtitles sit below the title; recipe page references align to the right. A card
  keeps the shared `\BookMenuCardHeight` and grows only when its content needs more
  room, so long content pushes the page instead of spilling past the card.
- Each game-day menu page and division page ends with a `\BookEnd` anchor inside its
  last card (`menu:<last-id>:end`, or `division:<key>:end`; after the teams when a
  division has no dish-offs). `nfl-book build --strict` fails when that anchor lands
  on a later page than the page's first anchor (`menu:<first-id>` or
  `division:<key>`).
- Division cards pair side by side with equal heights. Recipe lists precede their
  short description and preparation note.
- A kickoff timeline sits under the menu's Prep plan or the dish-off's Prep note (the
  heading shows when either is present) as compact rows: a fixed label column
  (`\BookTimelineLabelWidth`, for example "Day before" or "Kickoff") and the task,
  linked to its recipe when it names one. Timeline rows carry no page numbers.
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
recipe, game-day menu and division page's one-page span and run `make check`. Longer
menu content, such as a full kickoff timeline, must still be checked visually: a card
that grows past the shared height is allowed as long as the page fits.

Validated 2026-09-26: 152-page production build, no recipe overflow warnings,
no overfull LaTeX boxes, 100 tests passing, zero content-validation warnings.
