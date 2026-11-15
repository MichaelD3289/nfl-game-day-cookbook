# A. Keep drafts and retired items out of production build models

Production builds (`nfl-book build`, booklets, website, EPUB) generate QR codes and photo variants for draft and retired recipes and components. That breaks AGENTS.md rule 5: drafts must never reach `nfl-book build`. The cause is that the resolved `BookModel` has two answers to "what's in this build?", and every consumer has to know which one is safe to use.

Impact: no failed build has been reported. **From code, not run:** an unreadable photo on a draft would add an error to the build's diagnostics and fail a production build for content that isn't even in the book.

### Now and wanted

|                                                 | Now                                                                                                                                                                  | Wanted                                                                 |
| ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `model.recipes`, `model.components`             | filtered by `include`                                                                                                                                                | unchanged                                                              |
| `model.recipes_by_id`, `model.components_by_id` | full build: every item, drafts and retired included; division build: that division's recipes but every component (`resolve.py:227-228`)                              | only included items, for every kind of build                           |
| Components a recipe pulls in                    | recomputed with `component_graph(...).ordered_closure(...)` and a separate "published" filter in `website.py:160-173`, `catalog.py:125-133` and `resolve.py:149-167` | `model.components_for(recipe)`, computed once in `resolve`             |
| `is_published`, `component_graph`               | live in `validation.py`, so render, catalog and website import validation                                                                                            | live in a new `publication.py`, imported by `resolve` and `validation` |
| Division model                                  | that division's recipes, every component                                                                                                                             | that division's recipes and the components they reach                  |

**From code:** two callers rely on the full lookups today, so each needs its own source:

- `preview.py:46-58` resolves the published model, then renders a draft from it. `build_media` and `quick_options_for(recipe, model.components_by_id)` only find the draft because the lookups hold all content. Wanted: preview resolves its own model with an `include` that admits drafts.
- `stats.py:175` walks `model.components_by_id` to count unreferenced components, which `resolve` leaves out of `model.components`. Wanted: stats reads the counted components from `loaded.content`.

The only status check left outside `resolve` is whether an item gets a website URL. Only published items get one. For now it stays in `web_href` (`render/pages.py:174`); ticket B moves it into `edition_url`. Preview QR codes keep falling back to the source URL, as they do today.

### Done when

- A new test, with a draft and a retired recipe and component in the fixture, shows that a published `resolve` holds none of them in `recipes`, `components`, `recipes_by_id`, `components_by_id`, `usage` or `components_for(...)`.
- The same test, with a preview-wide `include`, shows the drafts present and the retired items absent.
- `build_media` on the published fixture model writes no QR code or photo for `test-draft-nachos` or `test-draft-side`.
- `nfl-book preview` of `test-draft-nachos` still renders, as it does today.
- `nfl-book stats` reports the same unreferenced-component rows as on `b27c1ab` for the fixture book.
- A division model built for the fixture's division holds no component outside what that division's recipes reach.
- `website.py`, `catalog.py` and `render/pages.py` no longer import from `validation`.
- `make check` passes.

### Context

- The fixture already has `test-draft-nachos` (recipe) and `test-draft-side` (component). Add a `test-retired-…` recipe and component.
- CHANGELOG `Fixed`: production builds no longer generate media for drafts or retired items.

### Not included

- Moving the status check into the address module (ticket B).
- Changes to page contexts (ticket C).
