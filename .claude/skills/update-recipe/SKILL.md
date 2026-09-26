---
name: update-recipe
description: Edit, fix, rename, move, retire or shorten an existing recipe in the NFL game-day cookbook. Use for any change to a file under recipes/.
---

# Update a recipe

Edit only the source `.md` file under `recipes/`. Never edit `generated/` or `dist/`.

## Common edits

- **Wording, quantities or steps:** edit the body. Keep the page budget; see
  "Fixing an overflow" below.
- **Index values:** change `course` or the `index.*` fields. Allowed values are the
  bucket ids in `data/indexes.yml`.
- **Retiring or unpublishing:** set `status: retired` or `draft`. Then run
  `grep -rn "<id>" menus/` and remove the id from any published menu or dish-off,
  because published content may only reference published content.
- **Source URL:** replace it with the full canonical URL, then run
  `uv run nfl-book prepare-links`. That command never overwrites existing cache
  entries; stale ones are harmless.
- **Photo:** replace `<id>.jpg` next to the `.md`, and keep `photo_credit` accurate.

## Renaming the id or moving teams

The id is referenced by the file name, the image name and the menus.

1. Rename the file with `git mv` so `<new-id>.md` matches the `id:` field.
   Rename the image too and update `image:`.
2. For a team change, move the file into `recipes/<conf>/<div>/<new-team>/`.
   Don't add a team field.
3. Run `grep -rln "<old-id>" menus/ components/ recipes/` and update every hit.
4. Never hard-code page numbers anywhere; LaTeX resolves them from labels.

## Fixing an overflow

The build warns `recipe:<id> overflows its page (pages N-M)`.

1. First remove content-level bloat:
   - editorial notes inside ingredient lines, such as "(source gives no quantity)"
   - repeated information
   - Kitchen Notes that only restate the timing
2. Then merge short steps.
3. Change the global layout only if many recipes overflow; see `layout-changes`.

## Verify

```sh
uv run nfl-book validate <path>
make preview FILE=<path>
make pdf 2>&1 | grep overflows    # expect no output
make check
```

Record user-visible changes in `CHANGELOG.md` under `[Unreleased]`, using
`Changed`, `Fixed` or `Removed`.
