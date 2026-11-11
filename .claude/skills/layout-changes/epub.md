# EPUB layout

EPUB uses `templates/epub/`, `styles/epub.css` and `src/nfl_book/epub.py`. It reflows to
the reader's screen and font settings, so the print contract does not apply. Preserve
linked anchors and source/photo credits.

- **Headings decide the pages.** The EPUB starts a new file at every heading of level
  1–3 (`epub-chapter-level: 3`). Book sections are `#`; teams, division dish-offs, menu
  types and component kinds are `##`; each recipe, component and game-day menu is `###`.
  Everything inside a recipe or component (Ingredients, Method, Quick options, Kitchen
  notes) is `####`, so the recipe stays on one page. Group items inside a page
  (contents, index sections, Make It or Buy It lists) with bold labels.
- **Section openers come from `epub.py`:** team and component-kind headings are added
  between pages, and a menu type's heading is printed once (`continued`).
- **Labels (`{.eyebrow}`) go after their heading.**
- The EPUB links each recipe to its page in this edition of the website instead of a QR
  code, and shows full source URLs, not print short links.

## Done when

`nfl-book epub --no-render` and the tests in `tests/unit/test_epub.py` pass, and
`make epub` (needs Quarto) opens in a reader (Apple Books, Calibre) with a recipe, a
component, a division menu and an index reading correctly at a few text sizes. Run
EPUBCheck separately when changing packaging.
