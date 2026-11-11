# Batch 4 review: grouping, duplicates, course

| recipe path | grouping | duplicate | course |
|---|---|---|---|
| recipes/nfc/east/eagles/roast-pork-sandwich.md | pass | none | ok |
| recipes/nfc/east/eagles/water-ice.md | pass | none | ok |
| recipes/nfc/east/giants/black-and-white-cookies.md | pass | none | ok |
| recipes/nfc/east/giants/new-york-style-pizza.md | finding (ungrouped toppings) | near-duplicate of afc/east/jets/new-york-style-cheese-pizza.md | ok |
| recipes/nfc/east/giants/pastrami-on-rye-giants.md | pass | exact pair with afc/east/jets/pastrami-on-rye-jets.md (validator) | ok |
| recipes/nfc/north/bears/chicago-style-hot-dogs.md | pass | none | ok |
| recipes/nfc/north/bears/deep-dish-pizza.md | finding (minor: unlisted pan oil, optional regroup) | none | ok |
| recipes/nfc/north/bears/italian-beef-sandwiches.md | pass | none | ok |
| recipes/nfc/north/bears/tavern-style-thin-crust-pizza.md | pass | none | ok |
| recipes/nfc/north/lions/detroit-coney-dogs.md | finding (two-part dish, no groups) | none (distinct from Cincinnati cheese coneys) | ok |
| recipes/nfc/north/lions/detroit-style-pizza.md | pass | none | ok |
| recipes/nfc/north/packers/beer-brats.md | pass | none | ok |
| recipes/nfc/north/packers/chicken-booyah.md | pass | none | ok |
| recipes/nfc/north/packers/fried-wisconsin-cheese-curds.md | pass | none | ok |
| recipes/nfc/north/vikings/jucy-lucy-cheese-stuffed-burgers.md | pass | none | ok |
| recipes/nfc/north/vikings/tater-tot-hotdish.md | pass | none | ok |
| recipes/nfc/south/buccaneers/deviled-crab.md | pass | none | ok |
| recipes/nfc/south/buccaneers/spanish-bean-soup.md | pass | none | ok |

Counts: grouping findings 3 (one minor), duplicate findings 2 pairs, course findings 0.

## recipes/nfc/east/giants/new-york-style-pizza.md

### Grouping

Current: four ungrouped lines come first, then `### Dough`, then `### Sauce`:

```
- All-purpose flour or cornmeal for dusting
- 2 tablespoons grated Parmesan
- 2 ounces fresh mozzarella, torn
- 1 heaping cup grated low-moisture mozzarella
### Dough ...
### Sauce ...
```

The lead lines are toppings and a dusting aid, not part of any group, and read as if they belong to nothing. Step 5 uses Parmesan and both mozzarellas on the pizza; step 4 uses the flour for stretching.

Proposed: put the dust line and the cheeses after Sauce under a new `### Assembly` (or `### Topping`) heading, with the order Dough, Sauce, Assembly:

- `### Dough`: unchanged.
- `### Sauce`: unchanged.
- `### Assembly`: all-purpose flour or cornmeal for dusting; 2 tablespoons grated Parmesan; 2 ounces fresh mozzarella, torn; 1 heaping cup grated low-moisture mozzarella.

Every ingredient is used and listed.

### Duplicate (near-duplicate)

Pair: nfc/east/giants/new-york-style-pizza.md and afc/east/jets/new-york-style-cheese-pizza.md. I read both.

- Same dish: a plain NY cheese pizza of bread flour dough, crushed or whole tomato sauce, low-moisture mozzarella and Parmesan, baked at 500°F on a stone or steel. Both split the dough into two balls and bake one or two.
- Different sources (Food Network vs King Arthur) and different details: the Jets version uses a 8-10 hour cold ferment and a broil finish; the Giants version uses a same-day dough, adds fresh mozzarella and a parchment bake. The validator misses this because the URLs differ.
- Both list location "New York City metro".

Claim (judgment, not verified): neither team has a clear local edge, since both play in New Jersey and the dish is shared city-wide. The Giants have the longer New York identity (the Jets arrived as the Titans in 1960 and the Giants have been New York's NFL team since 1925). The Jets recipe is the more technically distinctive (cold ferment, broil), so it would be the one to keep if only one stays. The decision is yours.

## recipes/nfc/east/giants/pastrami-on-rye-giants.md

Duplicate pair (confirmed): afc/east/jets/pastrami-on-rye-jets.md. Same sandwich: deli pastrami, rye, spicy brown mustard, dill pickle. The Jets version is the more elaborate one (optional Swiss, sauerkraut, coleslaw, butter). The Giants version is the leaner one, sourced from La Brea Bakery.

Claim (judgment): the sandwich is a Manhattan Lower East Side deli icon (Katz's), so neither team has a stronger claim than the other; both teams share the same market. If one stays, the Giants version is the cleaner "classic" and its method is tested against the Katz's reheating note. The decision is yours.

Grouping passes: the pickle sits under "For serving" and the rest are the sandwich.

## recipes/nfc/north/bears/deep-dish-pizza.md

Grouping (minor):

1. Used but not listed: step 2 oils the pan with "3-4 tablespoons additional olive oil" and step 4 salts the tomatoes "to taste". Neither appears in `### Filling` or `### Crust`. Propose adding `- 3 to 4 tablespoons olive oil, for the pan` and `- Salt, to taste` (the second is optional since it is a seasoning).
2. Optional regroup: `### Filling` holds three distinct parts (the cheese and sausage, the tomato layer, the topping). The layering order in step 4 is cheese, sausage, then tomato mixture, then Parmesan and drizzle. Propose:
   - `### Crust`: unchanged, plus the pan oil line.
   - `### Filling`: 3/4 pound sliced mozzarella; 1 pound cooked and sliced Italian sweet or hot sausage, or about 3 cups sautéed vegetables.
   - `### Tomato layer`: 1 (28-ounce) can plum tomatoes, lightly crushed; 2-4 garlic cloves, minced, optional; 1 tablespoon granulated sugar, optional; 1-2 teaspoons pizza seasoning or dried Italian herbs; salt.
   - `### Topping`: 1 cup freshly grated Parmesan or Asiago; 2 tablespoons olive oil.

The regroup is a judgment call; the unlisted pan oil is a real gap.

## recipes/nfc/north/lions/detroit-coney-dogs.md

Current: one ungrouped list, then `### For serving`. The dish has two distinct parts, the Coney chili and the dogs and buns:

```
- 1 pound ground beef
... (chili ingredients down to)
- 1/4 cup water
- 8 natural-casing all-beef hot dogs ...
- 8 hot dog buns
### For serving
- Yellow mustard and finely diced white onion
```

Proposed:

- `### Coney sauce`: 1 pound ground beef; 1 cup diced white onion; 2 garlic cloves, minced; 1 1/2 tablespoons chili powder; 1 1/2 teaspoons kosher salt; 1 teaspoon ground cumin; 3/4 teaspoon paprika; 1/2 teaspoon smoked paprika; 1/2 teaspoon onion powder; 1/2 teaspoon garlic powder; 1/2 teaspoon black pepper; 1 pinch cayenne; 2 small pinches sugar; 1 (15-ounce) can tomato puree; 3-4 tablespoons prepared yellow mustard; 1/4 cup water.
- `### Hot dogs`: 8 natural-casing all-beef hot dogs; 8 hot dog buns.
- `### For serving`: unchanged (yellow mustard and diced white onion).

Everything listed is used in the steps; nothing is missing.

### Duplicate check

Not a duplicate of afc/north/bengals/cheese-coneys.md (Cincinnati coney: cocoa, cinnamon and allspice chili, finely shredded cheddar; different dish) or nfc/east/commanders/half-smoke-chili-dogs.md (smoked half-smoke sausage, long-cooked beef chili, no cheese). Detroit's Coney is a beanless spiced beef chili on a plain frank with mustard and onion, which is a distinct regional style.

## Notes with no finding

- chicken-booyah.md: one-pot soup, no groups needed. The ingredient list has stray blank lines between the seasoning, water and optional base lines; cosmetic, not grouping.
- jucy-lucy-cheese-stuffed-burgers.md: buns, onion and pickles are all assembly items; splitting would add little.
- tater-tot-hotdish.md: single casserole with a component cream sauce, nothing misfiled.
- deviled-crab.md: Croquette dough, Filling and Coating line up with the steps; the salt and pepper in the coating belong to the egg wash (step 6). Course "appetizers" is reasonable for croquettes.
