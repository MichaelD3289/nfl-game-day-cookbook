---
name: add-component
description: Add or edit a "Make It or Buy It" component (shared sauce, dip, seasoning, side, staple, topping or protein) and reference it from recipes with {{component:id}}.
---

# Components

A component is a shared sub-recipe with a store-bought shortcut. Recipes reference
it from an ingredient line, and the book shows a Q marker and a page reference.

## File

The path is `components/<kind>/<id>.md`, where `<kind>` is one of the ids in
`data/component-kinds.yml`: sauces, dips, toppings, seasonings, sides, staples,
proteins.

Scaffold one with:

```sh
uv run nfl-book new component --kind <kind> --slug <id>
```

```markdown
---
id: <id> # == file name
title: Sentence-case title
status: draft
yield: about 1 cup # optional
quick_buy: Brand or store-bought suggestion. # required
always_include: false # true = print even if no published recipe uses it
source:
  url: https://full.canonical/url
---

## Ingredients

- item

## From Scratch

1. Step.

## Note

Optional.
```

## Referencing it

- Add it in a recipe's `## Ingredients`:
  `- 1/2 cup sauce {{component:<id>}}`
- Put at most one reference per line. It can share the line with `{{no-scale}}`.
- Write ingredient amounts as for recipes (amount first, space before the unit) so
  the component page can be scaled on the website.
- Components may reference other components, but cycles are errors.
- A recipe can override the buy text with `quick_options: {<id>: ...}`.
- A component that no published recipe reaches is dropped from the book unless
  `always_include: true`.

## Finish

1. Set `status: published`.
2. Run `make links` (= `uv run nfl-book prepare-links`).
3. Run `make pdf` and confirm the component page and the "Used in" list look
   right.
4. Run `make check`.
5. Add a CHANGELOG entry.
