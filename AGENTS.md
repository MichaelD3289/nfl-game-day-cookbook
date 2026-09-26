# Agent rules

Rules for any human or AI agent editing this repository.

1. **Source is Markdown and YAML.** Recipes, components, menus and `data/*.yml` are the
   source of truth. Never edit `generated/` or `dist/`, and never treat generated QMD,
   LaTeX or PDF files as content. Regenerate them instead.
2. **No page numbers in source or Python.** Cross-references are LaTeX labels
   (`recipe:<id>`, `component:<id>`, ...), and LaTeX resolves them. Do not compute,
   hard-code or cache page numbers anywhere except the post-build `pagemap.json`, which
   is used for checks only.
3. **A recipe belongs to exactly one team, and its path decides which one.** It lives at
   `recipes/<conf>/<division>/<team>/<id>.md`, and the file name must equal `id`. Never
   add a `team`/`teams` field.
4. **Components are referenced only as `{{component:<id>}}` inside `## Ingredients`.**
   Components may reference other components. Cycles are errors.
5. **Production builds contain published content only.** Drafts can be previewed
   (`nfl-book preview`) but must never reach `nfl-book build`. Published content may
   reference only published content.
6. **The network is used in one place only.** `nfl-book prepare-links` fills
   `data/shortlinks.yml`. Commit the result. Every other command runs offline. Never
   replace an existing short URL automatically.
7. **Every error names its source file.** New checks must report through `Diagnostics`
   with the offending path, and must not raise bare exceptions.
8. **Test first, with synthetic fixtures.** New behaviour gets a test under `tests/`
   that uses `tests/fixtures/sample-book` (ids prefixed `test-`). Tests never read or
   write production content.
9. **Do not add dependencies or install system software silently.** Justify any new
   package in the PR. Quarto and TinyTeX are installed by the user, not by scripts.
10. **Keep it green.** Before finishing, run `make check` (ruff format and lint, strict
    mypy, pytest, `nfl-book validate`).

Recipe import is a separate, not-yet-started phase. Do not bulk-create, scrape or
migrate recipes, and do not use the `new` scaffold commands to fill production content
until that phase is explicitly opened.
