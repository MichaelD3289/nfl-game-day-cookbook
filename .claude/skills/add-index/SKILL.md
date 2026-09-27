---
name: add-index
description: Add, change or remove a search index in the NFL cookbook (e.g. "Index by Region", "Index by Cooking Method"), including new buckets and backfilling recipe front matter. Use for any edit to data/indexes.yml or src/nfl_book/indexes/.
---

# Add a search index

> **Working from a GitHub issue?** Claim it first ([AGENTS.md](../../../AGENTS.md) rule
> 15). If the issue already has the `in-progress` label, stop and ask a human; do not
> work on it without their explicit permission. Otherwise add the label before you
> change anything.

Indexes are configured, not hard-coded. Each entry in `data/indexes.yml` produces
one index page. That page lists recipe title, team and page reference, grouped
by bucket in the order the buckets are listed. The page number comes from
LaTeX, so no page numbers go anywhere.

Every index also becomes a filter on the website's **Browse recipes** page and a facet
in `recipes.json`, in `indexes.yml` order, with no code changes. The ids `conference`,
`division` and `team` are reserved for the league filters, so validation rejects them.

## Pieces

| File                            | Role                                                                                                     |
| ------------------------------- | -------------------------------------------------------------------------------------------------------- |
| `data/indexes.yml`              | Index definitions: `id`, `title`, `kind`, `field`, `required`, `multiple`, `intro`, `buckets`, `options` |
| `src/nfl_book/models/config.py` | `IndexConfig` / `Bucket` schema (strict; `course` index is mandatory)                                    |
| `src/nfl_book/indexes/field.py` | Built-in `field` kind, which reads front matter                                                          |
| `src/nfl_book/indexes/base.py`  | `IndexDefinition` and `@register_index_kind` for computed kinds                                          |
| `src/nfl_book/validation.py`    | Errors on unknown buckets, on missing required values, and on unknown `index.<key>` keys                 |
| `templates/index.qmd.j2`        | The index page. The contents page and scaffold pick up new indexes automatically.                        |

## Option A: a front-matter index (usual case, no Python)

1. Add an entry to `data/indexes.yml` where it should appear in the book:
   ```yaml
   - id: cooking-method # kebab-case, unique; becomes label index:<id>
     title: Index by Cooking Method
     kind: field
     field: index.cooking_method # snake_case key under the recipe's index: map
     required: true # published recipes must set it
     multiple: false # true = value may be a list of bucket ids
     buckets:
       - { id: grilled, label: Grilled }
       - { id: fried, label: Fried }
       - { id: baked, label: Baked }
       - { id: no-cook, label: No Cook }
   ```
   Make the buckets **exhaustive**. Every published recipe must fit at least one,
   so add a catch-all such as `other` or `variable` if needed.
2. **Backfill every recipe.** With `required: true`, every published recipe
   without the key fails validation. Any recipe with an unknown key also fails.
   - List the recipes: `ls recipes/*/*/*/*.md` (90+ files).
   - Add `cooking_method: <bucket>` under each recipe's `index:` mapping,
     after the existing keys.
   - Decide from the recipe's Ingredients and Instructions; don't guess from the
     title.
   - If a recipe is ambiguous, pick the dominant method and list those recipes
     for the user to review.
   - For a large backfill, you can stage it: land the index with
     `required: false`, backfill, then switch to `true`.
3. **Update the test fixtures.** `tests/conftest.py` copies the production
   `indexes.yml` into the synthetic book, so the fixture recipes under
   `tests/fixtures/sample-book/recipes/` also need the new key.
4. The `new recipe` scaffold adds the key automatically, because it reads
   `front_matter_keys()`. Update the field list in the `add-recipe` skill.

## Option B: a computed index (derived, not authored)

Use this when the bucket can be derived from existing data, for example
"Index by Conference", which comes from the path.

1. Add `src/nfl_book/indexes/<kind>.py`:
   ```python
   @register_index_kind("<kind>")
   class MyIndex(IndexDefinition):
       def buckets_for(self, recipe: Recipe) -> list[str]:
           ...  # return bucket ids; use self.config.options for settings
   ```
2. Import it in `src/nfl_book/indexes/__init__.py`, as is done for `field`.
3. Reference it from `data/indexes.yml` with `kind: <kind>`. Leave out `field`.
   Put any settings under `options:`.
4. `front_matter_keys()` stays empty, so no recipe changes are needed.
5. Write the unit tests **first**, under `tests/unit/`, using the fixture book:
   - bucket assignment
   - validation of unknown buckets

## Changing or removing an index

- **Renaming a bucket id:** update `indexes.yml` and then every recipe that uses
  it. Find them with `grep -rln "<old-id>" recipes tests/fixtures`. Labels
  (`display text`) can change freely.
- **Removing an index:** delete its entry, then remove its key from every
  recipe's `index:` map, because leftover keys become "unknown index key" errors.
- **The `course` index:** it cannot be removed, since recipe pages use its
  `short_label`.

## Verify

```sh
uv run nfl-book validate           # every missing or unknown value is reported with its file
make check
make pdf 2>&1 | grep -E "overflows|error"
```

- Check the new index page in the PDF, following the page-rendering steps in the
  `build-pdf` skill.
- Every published recipe should appear in the index. Empty buckets still print a
  heading, so drop or merge buckets nobody uses.
- Add a CHANGELOG `[Unreleased]` → `Added` entry, for example
  "Index by Cooking Method."
