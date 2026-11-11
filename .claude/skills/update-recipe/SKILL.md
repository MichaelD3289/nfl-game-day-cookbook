---
name: update-recipe
description: "Change an existing recipe in the NFL cookbook: edit, rename or move teams, retire, resolve a duplicate dish, or shorten an overflowing page."
---

# Update a recipe

## Common edits

- **Wording, quantities or steps:** edit the body and keep it within the page budget
  (see "Fixing an overflow").
- **Ingredient lines, component lines and groups:** follow
  [recipe-body.md](../add-recipe/references/recipe-body.md). Done for groups when every
  instruction step uses only its part's group.
- **Index values:** change `course` or the `index.*` fields to bucket ids from
  `data/indexes.yml`.
- **Source URL:** set the full canonical URL, then follow `source-links`.
- **Photo:** replace `<id>.jpg` next to the `.md`, and keep `photo_credit` accurate.

## Retiring or unpublishing

1. Set `status: retired` or `draft`.
2. Find menus and dish-offs that list it (`rg -n "<id>" menus/`) and remove the id from
   each published one.
3. When it was published, update the recipe count in `book/frontmatter/cover.md`
   (tagline and intro) to the output of `rg -l '^status: published' recipes | wc -l`.

## Resolving a duplicate dish

Validate warns "same title as" or "same source as" when two published recipes share a
dish. Each dish belongs to one team.

1. Choose the copy to keep: the one with the stronger regional tie to its team and the
   better source. When both are defensible, present the choice to the user and wait.
2. Retire the other copy (see "Retiring or unpublishing").
3. When the kept id carries a team suffix (`-rams`, `-jets`), rename it (see below).
4. Add a different local dish for the other team through `add-recipe`.

Done when validate reports no "same title" or "same source" warning for either file.

## Renaming the id or moving teams

1. Rename with `git mv` so `<new-id>.md` matches the `id:` field. Rename the image too
   and update `image:`.
2. For a team change, move the file into `recipes/<conf>/<div>/<new-team>/`.
3. Find references with `rg -ln "<old-id>" menus/ components/ recipes/` and update each
   one in menus and component lines. `last_reviewed_notes` report links keep the old
   id, because they point into a dated report.

## Fixing an overflow

The build warns `recipe:<id> overflows its page (pages N-M)`.

1. Remove content-level bloat:
   - editorial notes inside ingredient lines, such as "(source gives no quantity)"
   - repeated information
   - Kitchen Notes that only restate the timing
2. Merge short steps.
3. Reach for the global layout (`layout-changes`) only when many recipes overflow.

## Check it

```sh
uv run nfl-book validate <path>
make preview FILE=<path>
```

Done when validate reports no errors and no warnings for the files you touched, and,
for a published recipe, the build per `build-pdf` has no overflow for it. The CHANGELOG
entry is usually `Changed`, `Fixed` or `Removed`.
