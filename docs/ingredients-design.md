# Ingredient identity: design proposal

Status: **Proposal — awaiting maintainer decision.** Tracks issue #44. This document
changes no code or content. It compares three ways to record what each ingredient
line is, and recommends one.

## Problem

Ingredient lines are free Markdown. `src/nfl_book/quantities.py` finds the amounts
and units in a line so the website can scale them. Nothing records _what_ the
ingredient is. The build knows that `1 1/2 cups beef broth` holds "1 1/2 cups", but
not that it is beef broth.

That gap blocks several planned features:

- **Shopping lists** (#43) cannot merge `2 garlic cloves` from one recipe with
  `3 large garlic cloves` from another.
- **Aisle grouping** needs to know that broth is in the soup aisle and butter is in
  dairy.
- **Volume and weight conversion** needs a density per ingredient (a cup of flour
  is about 120 g, but a cup of sugar is about 200 g).
- **Dietary and allergen tags** (#51) need to know which lines contain milk, wheat,
  shellfish and so on.
- **Scaling** could be more reliable if a count such as `3 garlic cloves` were
  known to be counted in cloves.

## Goals

- Record a stable ingredient id for every non-component ingredient line in
  published content.
- Keep a single catalog of ingredients in `data/ingredients.yml`, with a name,
  aisle and optional conversion data.
- Leave the printed book and EPUB unchanged, word for word.
- Keep the source readable and diff-friendly. A reviewer should see the meaning of
  a line in the line itself.
- Validate everything offline, with `Diagnostics` that name the file and line.
- Make the backfill of 1,258 lines practical in batches.

## Non-goals

- Building shopping lists, aisle views, conversions or allergen indexes. Those are
  consumers (Phase 4) and have their own issues.
- Changing how amounts are parsed or scaled today.
- Nutrition data, prices or brand tracking.
- Any network lookup or external food database. AGENTS.md rule 6 allows the
  network only in `prepare-links`.

## Current state

### Parsing

- `references.parse_ingredients()` splits `## Ingredients` into bullet lines under
  optional `### Group` headings. Each line goes to `parse_ingredient()`.
- `parse_ingredient()` accepts exactly two marker kinds: `{{component:<id>}}`
  (`MARKER_RE`, at most one per line) and `{{no-scale}}` (`NO_SCALE_RE`, at most
  one). Any other `{{…}}` is an error: "malformed marker … use
  {{component:<component-id>}} or {{no-scale}}".
- It removes the markers to get the display text, then calls
  `quantities.find_amounts()` on that text.
- The result is `models.content.Ingredient(text, component, amounts)`. Problems are
  reported by `discovery.py` as `diags.error("ingredients", …, path)` with the
  line number in the message.
- `references.find_markers()` rejects `{{…}}` in free text such as Instructions.

### Rendering

- **PDF:** `templates/_macros.qmd.j2` prints `item.text`, plus a `\QMark` and
  `\ComponentRef` when the line references a component.
- **EPUB:** `templates/epub/_macros.qmd.j2` prints `item.text` and a Q link.
- **Website:** `templates/website/_macros.qmd.j2` prints `item|scalable`.
  `website._scalable()` wraps each amount in
  `<span class="qty" data-q="…" data-q2="…" data-unit="…" data-adj="…">`.
  `styles/website-scale.js` rescales those spans. Its `UNITS` table must match
  `UNITS` in `quantities.py`. `styles/website-print.js` prints the page as shown.
- `render/pages.ItemView(text, ref, amounts)` carries a line into all templates.

### Real lines

These are real lines. They show the range a design has to handle.

```markdown
- 1 medium yellow onion (about 8 ounces), halved and thinly sliced
- 2 tablespoons Diamond Crystal kosher salt (or 1 tablespoon table salt)
- 4 tablespoons canola or other neutral oil, divided
- 2 cups buttermilk (preferred for tang) or whole milk
- Kosher salt and freshly ground black pepper
- 4 Swiss cheese slices (optional)
- About 10 cups vegetable oil, or enough for 2 inches in a heavy pot {{no-scale}}
- 1 tablespoon homemade yellow mustard; or substitute the same amount of store-bought yellow mustard {{component:american-yellow-mustard}}
- Soft white sandwich bread and dill pickle slices
- 4 cups ice plus 1 cup water, for chilling
- 1/4 pound Velveeta, cubed
```

These come from `eagles/roast-pork-sandwich`, `bills/beef-on-weck`,
`titans/nashville-hot-chicken`, `jets/pastrami-on-rye-jets`,
`buccaneers/tampa-cuban-sandwich-with-salami`,
`colts/st-elmo-style-shrimp-cocktail` and `browns/potato-and-cheese-pierogi`.

### Size of the backfill

Counted from `## Ingredients` bullets on 2026-09-27. All content is `published`.

| Source     | Files | Lines | With `{{component:…}}` | With `{{no-scale}}` |
| ---------- | ----: | ----: | ---------------------: | ------------------: |
| Recipes    |    90 | 1,140 |                     32 |                   4 |
| Components |    21 |   151 |                      1 |                   0 |
| **Total**  |   111 | 1,291 |                     33 |                   4 |

That leaves **1,258 lines** to key. By division: AFC East 159, AFC North 134,
AFC South 167, AFC West 120, NFC East 143, NFC North 142, NFC South 158,
NFC West 117, components 151. Recipes have 4 to 42 lines, about 13 on average.

Approximate counts of lines that need a rule: 149 contain "or", 118 contain "and",
65 say "to taste", 51 say "optional", and 16 are salt-and-pepper pairs. A rough
text normalisation finds about 670 distinct item strings. Many are variants
("salt", "kosher salt", "table salt"), so we estimate a catalog of 250 to 350
entries.

## Catalog: `data/ingredients.yml`

All three options need the catalog. It is authored data, like
`data/component-kinds.yml`, and it is loaded by `config.load_settings()` through
`load_model()` into a strict Pydantic model.

### Schema draft

```yaml
# Ingredient catalog. Authored data.
#
# Each ingredient line in a recipe or component names one or more of these ids with
# {{ing:<id>}}. Ids are kebab-case and stable; names and aliases can change freely.
#
# aisle:         one of the aisle ids below (drives shopping-list grouping).
# grams_per_cup: optional density for volume <-> weight conversion.
# each:          optional weight of one counted item ({unit, grams}).
# shop:          false for things you do not buy (tap water). Default true.
# allergens:     reserved for #51; ids from the allergen list below.
aisles:
  - { id: produce, label: Produce }
  - { id: meat-seafood, label: Meat and Seafood }
  - { id: deli, label: Deli }
  - { id: dairy-eggs, label: Dairy and Eggs }
  - { id: bakery, label: Bakery }
  - { id: baking, label: Baking }
  - { id: spices, label: Spices and Seasonings }
  - { id: condiments, label: Condiments and Sauces }
  - { id: canned-jarred, label: Canned and Jarred }
  - { id: pantry, label: Pantry }
  - { id: oils-vinegars, label: Oils and Vinegars }
  - { id: frozen, label: Frozen }
  - { id: beverages, label: Beverages }
  - { id: none, label: Not Bought }

allergens: [milk, eggs, fish, shellfish, tree-nuts, peanuts, wheat, soy, sesame]

ingredients:
  - id: yellow-onion
    name: yellow onion
    aliases: [yellow onions, onion, onions]
    aisle: produce
    each: { unit: onion, grams: 225 } # medium

  - id: garlic
    name: garlic
    aliases: [garlic clove, garlic cloves]
    aisle: produce
    each: { unit: clove, grams: 5 }

  - id: kosher-salt
    name: kosher salt
    aliases: [diamond crystal kosher salt, morton kosher salt]
    aisle: spices
    # No density: Diamond Crystal and Morton differ by about 2x per cup.

  - id: black-pepper
    name: black pepper
    aliases: [freshly ground black pepper, ground black pepper]
    aisle: spices

  - id: all-purpose-flour
    name: all-purpose flour
    aliases: [flour]
    aisle: baking
    grams_per_cup: 120
    allergens: [wheat]

  - id: buttermilk
    name: buttermilk
    aisle: dairy-eggs
    grams_per_cup: 245
    allergens: [milk]

  - id: beef-broth
    name: beef broth
    aliases: [beef stock]
    aisle: canned-jarred
    grams_per_cup: 240

  - id: velveeta
    name: processed cheese (Velveeta)
    aliases: [velveeta]
    aisle: dairy-eggs
    allergens: [milk]

  - id: water
    name: water
    aisle: none
    shop: false
```

### Granularity

Key what a cook would pick off the shelf. Kosher salt and table salt are different
entries, because they measure differently. Yellow onion and white onion are
different entries, because the list should say which to buy. Brands are not
entries unless the recipe depends on the product, as with Velveeta. Preparation
("diced", "softened") and size ("large") stay in the line's prose.

### Catalog validation

All of these report through `Diagnostics` with `data/ingredients.yml` as the path:

- Ids match `SLUG_PATTERN` and are unique.
- Names are unique. Each alias is unique across all names and aliases, so the
  suggester never has two equal matches.
- `aisle` is one of `aisles`, and `allergens` entries are in `allergens`.
- `grams_per_cup` and `each.grams` are greater than zero, and `each.unit` is not
  empty.
- An entry that no content uses is a warning, like an unused component.

## Options

Each option is shown with real lines, mostly from
`recipes/nfc/east/eagles/roast-pork-sandwich.md`.

### Option a: inline key marker

The author adds `{{ing:<id>}}` at the end of the line, as with the existing
markers.

```markdown
- 3 medium garlic cloves, minced {{ing:garlic}}
- 2 tablespoons Diamond Crystal kosher salt (or 1 tablespoon table salt) {{ing:kosher-salt}}
- 1 medium yellow onion (about 8 ounces), halved and thinly sliced {{ing:yellow-onion}}
- Kosher salt and freshly ground black pepper {{ing:kosher-salt,black-pepper}}
- 2 cups pork stock, homemade chicken stock, or low-sodium chicken broth {{ing:pork-stock}}
```

- **Rendering:** the PDF and EPUB are unchanged, because the marker is removed from
  `Ingredient.text` like the others. The website wraps the line in a span with
  `data-ing`. No visible change.
- **Validation:** unknown id, malformed marker, duplicate id in a marker, and a key
  on a component line are errors. A missing key is a warning, then an error for
  published content (see Rollout).
- **Diff and readability:** one short token per line. Retagging a line is a one-line
  diff. The meaning is visible where the line is edited.
- **Parser:** small. One more regex beside `MARKER_RE` and `NO_SCALE_RE` in
  `parse_ingredient()`, and one more field on `Ingredient`.
- **Migration:** 1,258 lines, each touched once. Mechanical with a suggester.
  About 14 lines per file.
- **#43 merging:** exact. Merge by id, then by amount kind from `find_amounts()`.
- **#51 allergens:** exact, through the catalog's `allergens`.
- **Risks:** noise in the source. An author can choose a wrong key, but the choice
  is visible in review.

### Option b: structured front matter

Ingredients move to a YAML list, and the build writes the prose.

```yaml
ingredients:
  - group: Pork
    items:
      - { qty: 3, item: garlic, size: medium, unit: clove, prep: minced }
      - qty: 2
        unit: tbsp
        item: kosher-salt
        brand: Diamond Crystal
        note: or 1 tablespoon table salt
      - qty: 1
        size: medium
        item: yellow-onion
        note: about 8 ounces
        prep: halved and thinly sliced
  - group: Sandwiches
    items:
      - { item: [kosher-salt, black-pepper], note: to taste }
```

- **Rendering:** the build has to generate every line. The generated lines would
  differ from the current prose unless the generator can reproduce phrasing such
  as "About 1 cup homemade horseradish cocktail sauce; or substitute the same
  amount of store-bought St. Elmo sauce (one 8-ounce jar as written); serve 2
  tablespoons per portion". The PDF would change, and page fit would need
  checking again.
- **Validation:** strongest. Schema-checked amounts, units and ids.
- **Diff and readability:** poor. A 13-line list becomes 40 to 80 lines of YAML.
  Reviewers read fields, not the sentence a cook will see.
- **Parser:** the `find_amounts()` heuristics would be replaced by a prose
  generator, which is new code with many cases.
- **Migration:** every one of the 1,291 lines is rewritten by hand, including the
  component lines. The `add-recipe`, `update-recipe` and `add-component` skills and
  the scaffold all change. Source wording from imported recipes is lost.
- **#43 and #51:** exact.
- **Risks:** the largest authoring change in the project. Imported recipes lose
  fidelity to their sources, which `review-recipes` checks.

### Option c: inferred keys

Lines stay as they are. The build guesses the id from the text using the
catalog's names and aliases. Authors add a marker only where the guess fails.

```markdown
- 3 medium garlic cloves, minced
- 1/2 teaspoon red pepper flakes
- 1 1/4 pounds broccoli rabe, trimmed and cut into 1-inch pieces
- 2 cups pork stock, homemade chicken stock, or low-sodium chicken broth {{ing:pork-stock}}
```

- **Rendering:** same as a.
- **Validation:** weak. The build cannot tell a right guess from a wrong one.
- **Diff and readability:** cleanest source. But adding an alias to the catalog
  can silently change the meaning of lines that nobody touched.
- **Parser:** the largest and least predictable. It has to handle "garlic powder"
  versus "garlic cloves", "onion powder" versus "onion", "cayenne pepper" versus
  "black pepper", "4 cups ice plus 1 cup water" and "canola or other neutral oil".
- **Migration:** smallest up front. The cost moves to review of every guess, which
  is never recorded.
- **#43 and #51:** unreliable. A wrong guess on an allergen is a safety problem, and
  #51 must not rest on guesses.
- **Risks:** results are not reproducible across catalog edits, and wrong keys
  cannot be seen in the source.

## Comparison

| Criterion                     | a: inline marker   | b: front matter       | c: inferred      |
| ----------------------------- | ------------------ | --------------------- | ---------------- |
| PDF and EPUB unchanged        | Yes                | No, prose regenerated | Yes              |
| Meaning visible in the source | Yes                | Yes, as fields        | No               |
| Diff size per change          | One line           | Several YAML lines    | Catalog-wide     |
| Parser work                   | Small              | Large, new generator  | Large, heuristic |
| Validation strength           | Strong for ids     | Strongest             | Weak             |
| Backfill cost (1,258 lines)   | Medium, mechanical | High, manual rewrite  | Low up front     |
| Reproducible across edits     | Yes                | Yes                   | No               |
| Fit for #43 merging           | Good               | Best                  | Fair             |
| Fit for #51 allergens         | Good               | Best                  | Unsafe           |
| Change to author workflow     | Small              | Large                 | None             |

## Recommendation

Adopt **option a** as the source of truth. Use **option c only as an offline
helper**: a command that suggests keys, which the author confirms and commits. The
committed marker is the only thing the build trusts. Inference never runs during
`validate` or `build`.

This keeps the prose that the PDF prints, gives exact ids to #43 and #51, and
keeps every decision visible in a diff. Option b's precision is not worth rewriting
1,291 imported lines or regenerating the printed text.

### Rules for awkward lines

- **Several ingredients on one line.** List every id in one marker, in reading
  order: `Kosher salt and freshly ground black pepper {{ing:kosher-salt,black-pepper}}`.
  A shopping list shows those items without a merged amount, because one amount
  cannot be split between them.
- **"Or" alternatives.** Key the first choice only, which is the one the recipe
  prefers: `2 cups buttermilk (preferred for tang) or whole milk {{ing:buttermilk}}`.
  Alternatives stay in prose. Recording alternatives is left open (question 4).
- **Optional ingredients.** Key them like any other line. "Optional" stays in the
  prose. A later `optional` flag can be derived from the text if #43 needs it.
- **"To taste" and "for serving".** Key them. They merge as items without an amount.
- **Lines with `{{component:id}}`.** No `{{ing:…}}`. The component is the ingredient,
  and its own lines carry keys. A component line with an ing marker is an error.
  A merged list can expand the component's lines when the cook makes it from
  scratch.
- **Lines with `{{no-scale}}`.** Key them normally:
  `About 10 cups vegetable oil, or enough for 2 inches in a heavy pot {{ing:vegetable-oil}} {{no-scale}}`.
- **Things you do not buy** (tap water, ice for an ice bath). Key them to catalog
  entries with `shop: false`, so every line has a key and shopping lists can skip
  them.

## Marker syntax

- The form is `{{ing:<id>[,<id>…]}}`. Spaces are allowed around `:` and `,`, as
  `MARKER_RE` allows today. Each id must match `SLUG_PATTERN`.
- There is at most one ing marker per line, the same rule as the other markers.
  Several ids go in one marker.
- Put markers at the end of the line. The recommended order is `{{ing:…}}` then
  `{{no-scale}}`. A marker followed by more text is a warning ("move markers to the
  end of the line").
- Markers are illegal outside `## Ingredients`. `find_markers()` already reports
  them.
- **Parsing:** add `ING_RE` in `references.py`, count it in `parse_ingredient()`'s
  brace check, remove it from the display text with the other markers, and store
  the ids as `Ingredient.ingredients: tuple[str, ...] = ()`. Update the
  malformed-marker message to list all three forms.
- **PDF and EPUB:** nothing changes. Both templates print `item.text`, which no
  longer contains the marker.
- **Website:** add `ingredients` to `ItemView`. `website._scalable()` wraps the
  line in `<span class="ing" data-ing="kosher-salt black-pepper">…</span>`. The ids
  are space-separated, so CSS and JS can match `[data-ing~="garlic"]`. The line
  goes into a span because a Pandoc list item cannot take attributes, and
  `_scalable()` already writes raw spans. `website_check.py` should check that
  every `data-ing` id is in the catalog, as it does for the scaler attributes.
- **Conversions later:** `website-scale.js` should not copy the catalog. When
  conversions arrive, the build writes a generated `ingredients.json` with
  densities, and the unit tables in `quantities.py` and `website-scale.js` stay
  the only shared list.

## Suggester command

```sh
uv run nfl-book ingredients suggest [PATHS...] [--write]
```

- It is offline and deterministic, and it adds no new dependency (rule 9).
- `PATHS` are recipe or component files or directories. The default is all
  content.
- By default it prints proposals and changes nothing:

  ```text
  recipes/nfc/east/eagles/roast-pork-sandwich.md:31  exact     {{ing:garlic}}                     3 medium garlic cloves, minced
  recipes/nfc/east/eagles/roast-pork-sandwich.md:45  multiple  {{ing:kosher-salt,black-pepper}}   Kosher salt and freshly ground black pepper
  recipes/nfc/east/eagles/roast-pork-sandwich.md:44  none      —                                  1 1/4 pounds broccoli rabe, trimmed ...
  ```

- `--write` adds markers to the working tree for `exact` and `multiple` matches
  only. It never stages or commits and never replaces an existing marker. It
  skips component lines.
- `none` and `ambiguous` lines are left for the author, with the nearest catalog
  names shown. A summary lists unmatched strings, which are candidates for new
  catalog entries.
- **Matching:** remove markers and the spans found by `find_amounts()`, drop
  parentheticals and anything after the first comma or semicolon, drop size words
  (large, medium, small), then take the longest name or alias that matches on
  word boundaries. Split on "and" for several ids. On "or", take the first match
  and report the others.
- The author reviews the diff and commits through `logical-commits`.

## Rollout

The pattern follows the index rollout in the `add-index` skill: land the field
optional, backfill, then make it required.

**Phase 0: decide.** The maintainer answers the open questions below. No code.

**Phase 1: catalog, markers and validation.**

- Add the catalog model, `data/ingredients.yml` with a starter set of about 50
  common entries, `ING_RE` parsing, `Ingredient.ingredients`, website `data-ing`
  and catalog validation.
- An unknown id is an error. A missing key produces no diagnostic yet.
- Tests come first, under `tests/unit/test_references.py`,
  `test_validation.py` and `test_website.py`, using the fixture book.
- The fixture book gets its own `tests/fixtures/sample-book/data/ingredients.yml`
  with `test-` ids. The catalog is content, so it stays out of `CONFIG_FILES` in
  `tests/conftest.py`, and tests never read the production catalog (rule 8).
- Update the README marker section, the `add-recipe`, `update-recipe` and
  `add-component` skills, and the CHANGELOG.
- This phase must merge before any backfill, because the current parser rejects
  `{{ing:…}}`.

**Phase 2: suggester and backfill.**

- Add `nfl-book ingredients suggest`.
- Backfill in nine batches: components first (151 lines, because recipes build on
  them), then one division per pull request (117 to 167 lines each). Grow the
  catalog as each batch needs it.
- Once the first batch lands, a missing key on published content becomes a
  warning, so progress is visible in `nfl-book validate`.

**Phase 3: require.** A missing key on a non-component line of published content
becomes an error. Drafts still get warnings, so work in progress can build
previews. The new-recipe scaffold and the skills say keys are required.

**Phase 4: consumers.** These each have their own issue:

- #43: merged shopping lists grouped by aisle.
- #51: a dietary and allergen index computed from the catalog through the
  component graph.
- Volume and weight conversion from `grams_per_cup` and `each`.

## Open questions

Each question has a recommended answer.

1. **Adopt a with c as an offline helper?** Recommended: yes.
2. **One marker with commas, or several markers per line?** Recommended: one marker,
   `{{ing:a,b}}`. It matches the one-marker-per-kind rule, and lines stay shorter.
3. **Must the marker be at the end of the line?** Recommended: yes, but only as a
   warning, so the rule can be relaxed later.
4. **Record "or" alternatives?** Recommended: not now. Key the first choice. Revisit
   with #51, where an alternative can remove an allergen. A later syntax could be
   `{{ing:buttermilk|whole-milk}}`.
5. **Catalog granularity: shelf item or generic food?** Recommended: shelf item
   (kosher salt and table salt apart), with brands only where the recipe depends
   on them.
6. **Aisles in `data/ingredients.yml`, or a separate `data/aisles.yml`?**
   Recommended: the same file. There is one place to edit, and nothing else uses
   aisles.
7. **Accept `allergens` in Phase 1, or wait for #51?** Recommended: accept the
   optional field and its fixed list now, but do not require it. That avoids a
   second schema change.
8. **Keys on component lines?** Recommended: no. The component's own lines carry the
   keys. Store-bought mapping, if #43 needs it, goes in component front matter
   later.
9. **Key lines for things you do not buy, such as water?** Recommended: yes, with
   `shop: false`, so "every line has a key" stays a simple rule.
10. **When does a missing key become an error?** Recommended: after all nine
    backfill batches have landed, in one small pull request, as with
    `required: true` for indexes.
11. **Should the suggester be a CLI command or a script?** Recommended: a CLI command
    (`nfl-book ingredients suggest`) with tests, because authors and agents will use
    it for every new recipe.
