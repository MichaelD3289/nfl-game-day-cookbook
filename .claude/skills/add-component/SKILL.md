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
  `- 1/2 cup homemade sauce; or substitute the same amount of store-bought sauce {{component:<id>}}`
- Put at most one reference per line. It can share the line with `{{no-scale}}`.
- Write ingredient amounts as for recipes (amount first, space before the unit) so
  the component page can be scaled on the website.
- Components may reference other components, but cycles are errors.
- A recipe can override the buy text with `quick_options: {<id>: ...}`.
- A component that no published recipe reaches is dropped from the book unless
  `always_include: true`.

## Ingredient wording: homemade or store-bought

Use this pattern on every recipe ingredient that references a component:

```markdown
- 1 batch homemade Buffalo wing sauce (about 1 1/4 cups); or substitute the same amount of store-bought Buffalo wing sauce {{component:buffalo-wing-sauce}}
- 1/4 cup homemade Buffalo wing sauce; or substitute the same amount of store-bought Buffalo wing sauce {{component:buffalo-wing-sauce}}
- Homemade yellow mustard, for spreading; or substitute store-bought yellow mustard {{component:american-yellow-mustard}}
```

- Put the homemade choice first, then `; or substitute` and an explicitly named
  **store-bought** choice. Keep the component marker at the **end of the complete
  ingredient line**, after both choices and their preparation notes. Do not move
  it next to the homemade choice. Do not use only "prepared" or "refrigerated"
  to mean store-bought.
- Preserve existing batch quantities and their approximate yields. Keep measured
  portions as portions; do not turn a small serving into a whole component batch.
  Retain optional, to-taste and per-serving qualifiers without inventing amounts.
- Use "the same amount" for equal-volume or equal-weight substitutions and "the
  same number" for counts. Keep special substitutions explicit: hotdish uses two
  10–10.5-ounce cans of undiluted soup **per homemade batch**, not an equal volume
  of soup. Keep cooking, draining and chilling requirements for either choice.
- Give a component its own ingredient bullet when a mixed toppings line would
  make the link or substitution ambiguous. Keep brand suggestions in `quick_buy`
  or recipe `quick_options` unless needed to identify the substitute.
- Check instructions as well as ingredients: homemade preparation is conditional;
  a store-bought option follows its package preparation when needed.

### Scaling checks

Keep the leading amount numeric and before the ingredient, with a space before
its unit. The website scales a leading batch/count and measured equivalents in
parentheses. It does not scale spelled-out counts or a second count later in the
line. Express a fixed package conversion as "two ... cans per homemade batch",
so the leading batch count controls it, rather than leaving an apparently fixed
purchase count alongside a scaled homemade amount. Package sizes and per-serving
amounts stay fixed. Do not use `{{no-scale}}` to hide a quantity-parsing problem.

For wording changes, verify the parser and browser scaler on synthetic examples
at ½× and 2×, covering batches plus equivalent volumes, measured portions, and any
package or per-serving exceptions used. Tests must use synthetic fixtures, never
production recipes. Component links carry the page multiplier; they do not infer
what fraction of a component batch a measured portion needs. Do not claim that
portion-to-batch conversion happens automatically.

## Finish

1. Set `status: published`.
2. Run `make links` (= `uv run nfl-book prepare-links`).
3. Run `make pdf` and confirm the component page and the "Used in" list look
   right.
4. Run `make check`.
5. Add a CHANGELOG entry.
