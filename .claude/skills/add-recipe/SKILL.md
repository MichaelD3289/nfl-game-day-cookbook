---
name: add-recipe
description: Add a new recipe for a team to the NFL cookbook, written fresh or imported from a source.
---

# Add a recipe

## 1. Pick the team and the dish

- Look up the team's conference, division and slug in `data/nfl.yml`, for example
  `afc` / `east` / `bills`.
- Check the dish is new to the book. Search titles and sources
  (`rg -n -i '^title:.*<dish>|url:.*<source-domain>' recipes`), and look hardest at
  teams that share the `location` in `data/nfl.yml` (the Jets and Giants share New York;
  the Chargers and Rams share Los Angeles). Each dish belongs to one team, so when
  another team has it, pick a different local dish for this team. A distinct regional
  version with its own source (Tampa's Cuban with salami, Miami's Cuban) is a different
  dish. Done when no recipe covers this dish. Validate catches only published
  duplicates, so while the recipe is a draft this search is the check.
- Choose a kebab-case `id`.

## 2. Scaffold

```sh
uv run nfl-book new recipe --team <team-slug> --slug <id>
```

It writes a `status: draft` file at `recipes/<conf>/<div>/<team>/<id>.md` with every
front-matter key, including one `index:` key per field index in `data/indexes.yml`,
and refuses an id that is already used.

## 3. Front matter

Fill every `TODO` and `null` the scaffold left. The conventions it does not show:

- `yield` is required and non-empty.
- `description` is one plain sentence for the website card.
- `source.url` is the full canonical URL of the original, never a short link.
- `location: City, ST` overrides the team's location when the dish comes from
  elsewhere.
- A photo is `image: <id>.jpg` next to the `.md`, with `photo_credit:` naming who took
  it.
- `quick_options: {<component-id>: Store-bought suggestion}` overrides a referenced
  component's `quick_buy`.
- Index values are bucket ids from `data/indexes.yml`, decided from the ingredients and
  instructions.

## 4. Body

Only these sections, in this order:

```markdown
## Ingredients

- ungrouped lines, before the first group

### Part name

- 1 cup homemade sauce; or substitute the same amount of store-bought sauce {{component:<component-id>}}

## Instructions

1. Numbered steps.

## Kitchen Notes

Optional short paragraph.
```

Write the ingredient list by [recipe-body.md](references/recipe-body.md): ingredient
lines, Make It or Buy It lines, groups by **part**, and the page budget. A component
referenced from a published recipe must be published; create one with `add-component`.

## 5. Check it

```sh
uv run nfl-book validate recipes/<conf>/<div>/<team>/<id>.md
make preview FILE=recipes/<conf>/<div>/<team>/<id>.md    # drafts allowed
```

Done when validate reports no errors and no warnings for the file, and the preview
shows each group beside the steps that use it.

## 6. Publish

1. Set `status: published`.
2. Run `make links` to cache the short URL (see `source-links`). A published recipe
   without one fails validation.
3. Optionally add it to a menu or dish-off (`menus-and-dish-offs`).
4. Update the recipe count in `book/frontmatter/cover.md` (tagline and intro) to the
   output of `rg -l '^status: published' recipes | wc -l`.
5. Build per `build-pdf`. Done when the build has no `overflows its page` warning for
   this recipe; for one, tighten the wording per "Fixing an overflow" in
   `update-recipe`.
6. Add the CHANGELOG entry under `Added`.
