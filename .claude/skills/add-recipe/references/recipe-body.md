# Recipe body rules

The single source for how a recipe's `## Ingredients` list is written. The
`add-recipe`, `update-recipe`, `add-component` and `review-recipes` skills point here.
Component files follow the Ingredient lines section too.

## Ingredient lines

- Start each line with its amount (`1 1/2 cups beef broth`, `3 garlic cloves`,
  `About ½ teaspoon salt`) and put a space before the unit (`500 g`), so the website can
  scale it. Lines without amounts (`Salt, to taste`) are fine.
- Add `{{no-scale}}` to a line whose amount must stay fixed as the batch grows, such as
  frying oil measured by pot depth. Fix an amount validate cannot read by rewording it.
- When `yield` is not a plain "N servings" (`4 sandwiches`), set `servings:` (`4` or
  `4-6`) so readers can scale by people.

## Make It or Buy It lines

A line that uses a component names the homemade choice first, then `; or substitute`
and the store-bought choice, and ends with the component marker:

```markdown
- 1 batch homemade Buffalo wing sauce (about 1 1/4 cups); or substitute the same amount of store-bought Buffalo wing sauce {{component:buffalo-wing-sauce}}
- 1/4 cup homemade Buffalo wing sauce; or substitute the same amount of store-bought Buffalo wing sauce {{component:buffalo-wing-sauce}}
- Homemade yellow mustard, for spreading; or substitute store-bought yellow mustard {{component:american-yellow-mustard}}
```

- One `{{component:<id>}}` per line, only in `## Ingredients`. It is the last token on
  the line, after both choices and their preparation notes, and may share the line with
  `{{no-scale}}`.
- Name the substitute with the word "store-bought". Keep brand suggestions in the
  component's `quick_buy` or the recipe's `quick_options` unless a brand is needed to
  identify the substitute.
- Keep the source's batch quantities with their approximate yields, and keep a measured
  portion as that portion (`1/4 cup`), never "1 batch". Keep optional, to-taste and
  per-serving qualifiers as written.
- Use "the same amount" for equal volume or weight and "the same number" for counts.
  State special substitutions explicitly: hotdish uses two 10–10.5-ounce cans of
  undiluted soup **per homemade batch**.
- The website scales the leading amount and measured equivalents in parentheses, not
  spelled-out counts or a second count later in the line. Write a fixed package
  conversion as "... per homemade batch" so the batch count controls it.
- Give the component its own bullet when a mixed toppings line would make the link or
  substitution unclear.
- In the instructions, homemade preparation is conditional, and the store-bought choice
  follows its package directions when it needs preparing.

## Groups

Each `###` group is one **part** of the dish the cook makes or assembles: the protein, a
sauce, a salad, the bread, toppings, "For serving". Name the group after its part.

- Group by part, following the instructions rather than the source's layout. Done when
  every instruction step that makes a part uses only that part's group: the steps that
  season and roast the beef use `### Beef`, and the steps that mix the dressing use
  `### Dressing`.
- A group runs to the next `###` heading. Ungrouped lines come before the first heading.
  When the source lists a sauce or salad before the main ingredients, give the main
  ingredients their own group (`### Sandwich`, `### Hot dogs`), so they do not land in
  the sauce.
- A one-part recipe is a flat list with no headings. A part with a single line stays a
  bullet in the nearest group (`- Optional: ...`).
- Validate warns when one group holds every ingredient.

## Page budget

Every recipe fits on one page: about 20 ingredient lines or fewer and 4–6 concise steps.
When a page overflows, follow "Fixing an overflow" in the `update-recipe` skill.
