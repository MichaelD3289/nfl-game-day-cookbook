# B. Give every labelled item one address from `references.py`

An item's LaTeX label, page slug, page file, HTML id and website URL are built with separate f-strings in seven modules. Nothing in the code keeps them in step, so `check_web_links` exists only to catch at build time when a slug and a link target disagree. This gives each item a single address, so that kind of drift can't happen.

Impact: no broken link has been reported. This is maintenance cost and a trap for future changes.

### Now and wanted

**From code:**

- Labels: `references.py:26-67`, and a second list in `postbuild.py:19` (`LABEL_PREFIXES`).
- Slugs and files: `render/pages.py:176` (`f"{kind}-{id}.html"`), `181` and `501` (`f"recipe-{id}"`), `website.py:55-56` (`_filename`), `catalog.py:89`.
- EPUB makes up `kind:<id>` labels for component-kind sections (`epub.py:203-206`), and `references.py` doesn't know them.
- Dish-off labels are rendered but missing from `PageSpec.anchors`. The website and EPUB route tables patch them in afterwards (`website.py:497-499`, `epub.py:122`).
- Website routes link to `.qmd` (Quarto rewrites them), while print pages and the catalog link to `.html`. Both forms are correct, but nothing says which to use where.

Wanted: `references.address(item)` returns label, end label, slug, `page_source` (`.qmd`, for cross-links inside Quarto), `page_url` (`.html`, for JS, QR codes and the catalog), HTML id and `edition_url`. `edition_url` is `None` for anything not published. It covers every labelled kind: recipe, component, division, menu, dish-off, team, section, index and component-kind section. `PageSpec.anchors` lists every anchor a page renders, and the route tables are built only from `anchors`.

### Done when

- An address test shows, for one item of each kind, that the slug, `page_source`, `page_url` and HTML id are consistent and that the label carries the prefix LaTeX expects.
- `edition_url` is `None` for the draft fixture recipe and set for a published one.
- `check_web_links` and its fake-`WebView` test are deleted, and `website_check` still passes on the built fixture site.
- `rg -n 'f"(recipe|component)[-:]' src/nfl_book` finds matches only in `references.py`.
- `postbuild.py` reads its prefixes from `references.py`.
- The website and EPUB route tables have no patching after `anchors`.
- `make check` passes.

### Context

AGENTS.md rule 2: cross-references are LaTeX labels. This keeps them all in one module.

### Not included

- Typed page views (ticket C). The address module only takes items, so it doesn't need them.
