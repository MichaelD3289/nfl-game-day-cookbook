---
name: add-component
description: "Make It or Buy It components: add, rename or retire a shared sub-recipe with a store-bought shortcut, and link it from recipe ingredient lines with {{component:id}}."
---

# Components

A component is a shared sub-recipe with a store-bought shortcut. Recipes reference it
from an ingredient line, and the book shows a Q marker and a page reference.

## 1. Scaffold

```sh
uv run nfl-book new component --kind <kind> --slug <id>
```

`<kind>` is an id in `data/component-kinds.yml`. The file lands at
`components/<kind>/<id>.md` with every front-matter key and the sections
`## Ingredients`, `## From Scratch` and an optional `## Note`.

## 2. Fill it in

- `quick_buy` is required: the store-bought shortcut, brand or style.
- `description` is one plain sentence for the website's Make It or Buy It list.
- `source.url` is the full canonical URL of the original.
- `always_include: true` prints a component that no published recipe uses.
- Write its ingredient lines by the Ingredient lines section of
  [recipe-body.md](../add-recipe/references/recipe-body.md), so the website can scale
  the component page.

## 3. Reference it

Add a line to a recipe's `## Ingredients` by the Make It or Buy It lines section of
[recipe-body.md](../add-recipe/references/recipe-body.md). A recipe overrides the buy
text with `quick_options: {<id>: ...}`. Components can reference other components the
same way.

## 4. Finish

1. Reference it from at least one published recipe, or set `always_include: true`;
   validate otherwise warns `unused` and the build drops it.
2. Run `uv run nfl-book validate <path>` and `make preview FILE=<path>`. Done when
   there are no errors and no warnings for the files you touched.
3. Set `status: published` and run `make links` (see `source-links`).
4. Build per `build-pdf`. Done when the component page's "Used in:" line lists every
   published recipe that references it.

## Renaming or retiring a component

- **Rename:** `git mv` to `<new-id>.md`, update `id:`, then update every
  `{{component:<old-id>}}` marker and every `quick_options` key found by
  `rg -ln "<old-id>" recipes/ components/`.
- **Retire:** first rewrite each referencing line as a plain ingredient (keep the
  store-bought choice), then set `status: retired`. Validate errors while a published
  recipe still references it.
