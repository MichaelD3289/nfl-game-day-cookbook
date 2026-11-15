# C. Build each page from typed data once, instead of patching it in website passes

Every recent website feature (#61 JSON-LD, #62 cook mode, #72 menu builder, #73 matchup) added another pass that edits page contexts after they're built. A website recipe page is now assembled in seven places. Those passes don't know which recipe a page is for, so they find recipe pages by comparing template file names and recover the recipe by parsing its label. This ticket builds each page's data once, from the item itself, so the next website feature is one field rather than one more pass.

Blocked by A (included-only model) and B (addresses).

### Now and wanted

**From code:**

- `PageSpec.context` is an untyped `dict` (`render/pages.py:48-54`).
- `digital.prepare_pages` (`digital.py:58-65`) and seven `_add_*` passes (`website.py:96-361`: scaling, structured data, print pages, suggestions, browse, menu builder, matchup) edit it afterwards.
- `catalog.recipe_catalog` reads `page.context["image"]`.
- There are 22 checks of template file names or slugs in `website.py` and 6 in `epub.py`.
- `website.py:168` and `epub.py:241` get the item back by parsing its label.

Wanted:

- `PageSpec` keeps `slug`, `template`, `anchors` and `spans`, and carries a typed page view (a frozen dataclass per page kind) instead of `context`.
- One base view per recipe and per component serves every format: print, cards, EPUB and website. A website view is built from it and adds scaling, JSON-LD, print pages and suggestions.
- Website page builders take `(item, model, media, catalog)` and compute every field once. The catalog is built first, from the model, as typed entries.
- `website._markdown`/`epub._md`, `_web_body`/`_prose` and the two `:::` fence regexes become one digital-text module.

### Done when

- `website.py` and `epub.py` contain no `page.template ==` or `page.slug ==` checks, and no `_add_*` pass edits a built page.
- Neither file parses a label to find an item.
- `test_website.py` checks view fields for its feature tests and keeps one rendered-QMD check per page kind.
- No test imports a private `_add_*` function.
- The fixture's generated website and EPUB QMD files are identical to `b27c1ab`'s, apart from ordering or whitespace explained in the PR. One way to check: diff `build_website(render=False)` output before and after.
- The print book and cards build from the same base views, with no template changes except attribute access where needed.
- `make check` passes.

### Context

Jinja's `x.y` works the same on dicts and dataclasses, so print templates barely change.

### Not included

- The JSON serializer, the `printPages` rename and the JS contract test (ticket E).
- Build orchestration and Quarto (ticket D).

### Watch out for

`cards.py` reuses `recipe_context` and adds a `"source"` key. That key moves onto the card view here, or in D if D lands first.
