---
name: add-recipe
description: Add a new recipe to the NFL game-day cookbook. Use when asked to add, create, import or write up a recipe for a team.
---

# Add a recipe

Every recipe is one Markdown file. Its team comes **only** from its path, so never
add a `team` or `teams` field.

## 1. Pick the location

- Look up the team's conference, division and slug in `data/nfl.yml`, for example
  `afc` / `east` / `bills`.
- Choose a kebab-case `id`. It must be unique across all recipes (check with
  `ls recipes/*/*/*/`).
- The path is `recipes/<conf>/<div>/<team>/<id>.md`, and the file name must equal
  `id`.

## 2. Scaffold (optional)

```sh
uv run nfl-book new recipe --team <team-slug> --slug <id>
```

This writes a `status: draft` file in the right place. You can also copy an
existing recipe from the same team.

## 3. Front matter

```yaml
---
id: <id>                        # == file name
title: Sentence-case title
status: draft                   # draft | testing | published | retired
course: meals                   # appetizers | sides | meals | desserts
location: Buffalo, NY           # optional, overrides the team's location
yield: 4 servings               # required, non-empty
servings: 4                     # optional: people fed (4 or 4-6) when yield is not "N servings"
prep: 20 minutes                # optional
cook: 45 minutes                # optional
image: <id>.jpg                 # optional, next to the .md; requires photo_credit; the build
                                #   makes square resized copies and never edits the original
photo_credit: Who took it
index:                          # one key per field index in data/indexes.yml (see add-index)
  main_ingredient: beef         # beef | pork-and-sausage | poultry | seafood | mixed-meat | meatless
  practical_time: 31-to-60-minutes  # up-to-30-minutes | 31-to-60-minutes | over-60-minutes | variable-or-make-ahead
  cost: moderate                # pantry-friendly | moderate | premium
source:
  url: https://full.canonical/url   # never a short link
quick_options:                  # optional: override a referenced component's quick_buy
  <component-id>: Store-bought suggestion
---
```

Unknown keys are errors (`extra="forbid"`).

## 4. Body

Only these sections are allowed, in this order:

```markdown
## Ingredients

- ungrouped items only before the first group
- 1 cup sauce {{component:<component-id>}}

### Group name

- item

## Instructions

1. Numbered steps.

## Kitchen Notes

Optional short paragraph.
```

- Put at most one `{{component:<id>}}` on an ingredient line, and use it only in
  `## Ingredients`. The component must exist under `components/`, and a published
  recipe may only reference published components. To create one, see the
  `add-component` skill.
- Start each ingredient line with its amount (`1 1/2 cups beef broth`, `3 garlic
  cloves`, `About ½ teaspoon salt`) and put a space before the unit (`500 g`, not
  `500g`), so the website can scale it. Lines without amounts (`Salt, to taste`) are
  fine. Add `{{no-scale}}` to a line whose amount should not grow with the batch, such
  as frying oil measured by pot depth. Validation reports amounts it cannot read.
- For a yield such as "4 sandwiches", add `servings:` so readers can scale by people.
- Don't write single-item `###` groups. Use an inline bullet such as
  `- Optional: ...` instead.
- Every recipe must fit on **one page**. As a rough budget, keep to 20 ingredient
  lines or fewer and 4–6 concise steps. Lists with more than 24 lines switch
  automatically to compact run-in groups.

## 5. Check it

```sh
uv run nfl-book validate recipes/<conf>/<div>/<team>/<id>.md
make preview FILE=recipes/<conf>/<div>/<team>/<id>.md    # drafts allowed
```

## 6. Publish

1. Set `status: published`.
2. Run `make links` (= `uv run nfl-book prepare-links`) (see the `source-links` skill). A published
   recipe whose source URL is not cached fails validation.
3. Optionally add it to a menu or dish-off (see `menus-and-dish-offs`).
4. Run `make pdf` and confirm there is **no** `overflows its page` warning for it.
   If there is one, tighten the wording; do not change the layout for one recipe.
5. Run `make check`.
6. Add a `CHANGELOG.md` entry under `[Unreleased]` → `Added`.

If the cover tagline counts recipes (`book/frontmatter/cover.md`), update it.
