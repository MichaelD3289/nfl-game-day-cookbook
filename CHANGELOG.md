# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

