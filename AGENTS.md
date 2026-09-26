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
11. **Log every change in the changelog.** Any change you make that a reader of the
    book or a user of the tooling would notice (content, layout, CLI, Make targets,
    config, agent rules and skills) gets an entry under `## [Unreleased]` in
    `CHANGELOG.md`, in the matching Keep a Changelog section (Added, Changed,
    Deprecated, Removed, Fixed, Security). Add it in the same change, not later.
    Describe the effect in one or two plain sentences, and do not repeat entries that
    already cover your change. Only the `creating-release` skill turns `[Unreleased]` into a
    version.
12. **Commit through the `logical-commits` skill.** Every commit is one coherent,
    Conventional Commit change that passes `make check` by itself, carries its own
    CHANGELOG entry and has no AI attribution. Present the commit plan and get approval
    before staging.

## Task skills

Step-by-step playbooks for common work live in `.claude/skills/*/SKILL.md`:

| Skill | Use it for |
| --- | --- |
| `add-recipe` | Adding a recipe for a team |
| `review-recipes` | Authenticity/source-quality audit of one recipe, a list, or all recipes |
| `update-recipe` | Editing, renaming, moving, retiring or shortening a recipe |
| `add-component` | "Make It or Buy It" components and `{{component:id}}` markers |
| `menus-and-dish-offs` | Game-day menus and division dish-offs |
| `add-index` | New or changed search indexes and recipe backfill |
| `source-links` | Source URLs, `data/shortlinks.yml`, QR codes |
| `build-pdf` | Building, previewing and debugging the PDF |
| `layout-changes` | Anything in `styles/` or `templates/` |
| `changelog` | Writing CHANGELOG entries |
| `creating-release` | Choosing the SemVer bump, versioning with uv, tagging |
| `logical-commits` | Planning and creating every commit |

Recipe content is imported. Adding or editing individual recipes is normal work;
follow the skill for it.
