# Batch 1 review (18 recipes)

Read-only review. Duplicate calls on "stronger claim" are my judgment, not verified.

| recipe path | grouping | duplicate | course |
|---|---|---|---|
| recipes/afc/east/bills/beef-on-weck.md | pass | none | ok |
| recipes/afc/east/bills/buffalo-wings.md | pass | none | ok |
| recipes/afc/east/bills/chicken-finger-sub.md | pass | none | ok |
| recipes/afc/east/bills/sponge-candy.md | pass | none | ok |
| recipes/afc/east/dolphins/cuban-black-beans-and-rice.md | pass | none | ok |
| recipes/afc/east/dolphins/cuban-frita-burger.md | finding (minor, optional) | none | ok |
| recipes/afc/east/dolphins/cuban-sandwich.md | pass | related to tampa-cuban-sandwich-with-salami (distinct variant, see below) | ok |
| recipes/afc/east/jets/new-york-bagels.md | pass | none | ok (judgment: "meals" is a stretch for a bagel, but no better course exists) |
| recipes/afc/east/jets/new-york-style-cheese-pizza.md | finding | near-duplicate of nfc/east/giants/new-york-style-pizza.md | ok |
| recipes/afc/east/jets/pastrami-on-rye-jets.md | pass | exact pair with nfc/east/giants/pastrami-on-rye-giants.md (confirmed) | ok |
| recipes/afc/east/patriots/boston-baked-beans.md | pass | none | ok |
| recipes/afc/east/patriots/boston-cream-pie.md | pass | none | ok |
| recipes/afc/east/patriots/lobster-rolls.md | finding (minor, optional) | none | ok |
| recipes/afc/east/patriots/new-england-clam-chowder.md | pass | none | ok |
| recipes/afc/north/bengals/cheese-coneys.md | finding | near-duplicate of afc/north/bengals/cincinnati-chili-over-spaghetti.md (same team); related to nfc/north/lions/detroit-coney-dogs.md | ok |
| recipes/afc/north/bengals/cincinnati-chili-over-spaghetti.md | finding (includes a missing ingredient) | near-duplicate of cheese-coneys (same chili) | ok |
| recipes/afc/north/bengals/goetta.md | pass | none | ok |
| recipes/afc/north/browns/polish-boy-sandwich.md | pass | none | ok |

Counts: grouping findings 5 (3 substantive, 2 minor/optional); duplicate findings 3 pairs (+2 related-but-distinct notes); course findings 0.

## Grouping findings

### recipes/afc/east/jets/new-york-style-cheese-pizza.md
Current: an untitled block at the top holds the toppings, then `### Dough` and `### Sauce`.
```
- Semolina or cornmeal for dusting
- 1 cup prepared sauce, divided
- 7 ounces shredded whole-milk, low-moisture mozzarella
- 1/4 cup grated Parmigiano-Reggiano
- Red pepper flakes and dried oregano, optional
```
Problems: "1 cup prepared sauce, divided" is a second listing of the sauce that `### Sauce` makes below it (the sauce yield is not stated, so the two do not visibly connect). The untitled block is really the assembly part.
Proposed:
- `### Dough`: the six dough lines (unchanged).
- `### Sauce`: the three sauce lines (unchanged). Drop the "1 cup prepared sauce, divided" line, or move it to Assembly as "1 cup sauce (from above), divided".
- `### Assembly` (for the toppings): semolina or cornmeal for dusting; the 1 cup sauce line if kept; 7 ounces mozzarella; 1/4 cup Parmigiano-Reggiano; red pepper flakes and oregano, optional.
Nothing is unused or unlisted. The giants pizza uses the same Dough / Sauce layout, so this also makes the two consistent.

### recipes/afc/north/bengals/cheese-coneys.md
Current: one flat list mixing chili ingredients with hot dogs, rolls, mustard and cheese. The method has two parts (step 1-2 chili; step 3-4 assembly). Nothing is unused or unlisted.
Proposed:
- `### Coney chili`: 1 tbsp olive oil; 1 cup chopped white onion, plus more for topping; 1 tbsp minced garlic; 1 pound 85%-lean ground beef; kosher salt; 1 tbsp cocoa; 1/2 tsp cinnamon; 1/2 tsp allspice; 1 can (8 oz) tomato sauce; 1 cup water; 1 tbsp cider vinegar; 1 tsp Worcestershire; 1 tbsp chili powder.
- `### Coneys`: 6 small all-beef hot dogs; 6 long potato rolls; yellow mustard for serving; 4 ounces finely shredded sharp cheddar. (The extra chopped onion for topping is referenced in the chili line; keep the note there or repeat "chopped onion, for topping" here.)

### recipes/afc/north/bengals/cincinnati-chili-over-spaghetti.md
Current: one flat list (oil, onions, beef, spices, then "1 pound spaghetti, cooked", the beans/cheddar topping line, oyster crackers).
- Unlisted: step 2 says "with 1 cup water" but no water is in the list. Add "1 cup water".
- Grouping: two parts (chili, and the spaghetti and toppings).
Proposed:
- `### Chili`: 4 tbsp olive oil; 2 sweet onions, finely chopped, plus more for topping; 2 pounds ground beef chuck; salt and pepper line; 4 cloves garlic; 1 can tomato sauce; 2 medium tomatoes; 1/4 cup cider vinegar; 1/4 cup chili powder; 2 tbsp paprika; 1 tbsp cinnamon; 2 tsp cumin; 1/2 tsp allspice; 1/4 tsp cloves; 1/4 tsp cayenne; 1 cup water (add).
- `### Spaghetti and toppings`: 1 pound spaghetti, cooked; the kidney beans and shredded cheddar line; oyster crackers, optional. (Move or repeat the "more onion for topping" so the 4-way/5-way onion is findable.)

### recipes/afc/east/patriots/lobster-rolls.md (minor, optional)
Current: dressing ingredients, lobster, buns, lettuce and the butter for the buns are all in one list, followed by `### For serving`. Two distinct parts (lobster salad; toasted buttered rolls).
Proposed (optional):
- `### Lobster salad`: 1/4 cup mayonnaise; 2 celery stalks; chives; 1 tbsp lemon juice; 1/4 tsp kosher salt; 1 pound cooked lobster meat.
- `### Rolls`: 2 tbsp softened butter; 4 split-top buns; 4 Bibb lettuce leaves (optional).
- `### For serving`: lemon wedges (unchanged).
Note the butter currently comes first in the list but is used in step 3, so reordering also fixes the order.

### recipes/afc/east/dolphins/cuban-frita-burger.md (minor, optional)
Current: one flat list. Parts: seasoned patties (ground chuck, spices, hot sauce, diced onion), crisp potato topping (potatoes, oil), and buns.
Proposed (optional):
- `### Patties`: ground chuck; paprika; garlic powder; onion powder; cumin; hot sauce; diced onion.
- `### Crisp potatoes`: 2 russet potatoes; about 1 cup oil; salt, to taste.
- `### To assemble`: 5 rolls; ketchup, optional.
The salt line is shared (potatoes and patties), so keep "Salt, to taste" in the potatoes group and mention it in step 3, or leave the list flat. I would only do this if the book applies the same rule to other burgers; the dish is simple enough to pass.

## Duplicate findings

### Pastrami on rye: Jets vs Giants (confirmed exact duplicate)
- afc/east/jets/pastrami-on-rye-jets.md: source centralmarketnewyork.com; 1 pound pastrami, 8 rye slices, 4 tbsp spicy brown mustard, optional Swiss, sauerkraut, coleslaw, butter-toasted bread, broiled cheese.
- nfc/east/giants/pastrami-on-rye-giants.md: source labreabakery.com (instructions reference Katz's); 1 1/3 pounds pastrami, 8 rye slices, 4 tbsp mustard, pickles.
Same dish, same title, same core ingredients; the sources differ. Local claim (judgment): both are New York City deli food; the Giants recipe is closer to the classic (plain pastrami, mustard, rye, pickle, Katz's reference), while the Jets recipe is a grilled/Reuben-style variant with optional Swiss, kraut and coleslaw. Katz's and the Lower East Side delis are Manhattan, which is neutral between the two. Not a clear winner; I lean Giants for the classic version.

### New York style pizza: Jets vs Giants (near-duplicate, validator misses it)
- afc/east/jets/new-york-style-cheese-pizza.md (King Arthur, two 13-inch pizzas, 8-10 hour cold-rested dough, tomato sauce, low-moisture mozzarella, Parmigiano).
- nfc/east/giants/new-york-style-pizza.md (Food Network, one 12-13 inch pizza saved second dough ball, same sauce idea, low-moisture plus fresh mozzarella, Parmesan).
Different sources and quantities, but the same dish: a thin foldable New York cheese pizza with tomato sauce and mozzarella. Local claim (judgment): equal, as both teams play in New Jersey and represent the NYC metro, so neither is more local. Retain one, or differentiate (for example one a classic cheese slice and the other a different New York style such as a Grandma or Sicilian square). Decision for the owner.

### Cheese coneys vs Cincinnati chili over spaghetti (same team, near-duplicate)
- afc/north/bengals/cheese-coneys.md and afc/north/bengals/cincinnati-chili-over-spaghetti.md both make Cincinnati chili (beef, tomato sauce, cocoa/cinnamon/allspice, vinegar) and top it with mustard/onion/cheddar. The two differ only in vehicle (hot dog bun versus spaghetti). The two chilis are separate full recipes, not a shared component, so they can drift. This is the strongest candidate for extracting a `cincinnati-chili` component and referencing it in both recipes, which would keep both dishes, since "3-way" and "coney" are distinct local dishes (judgment). Not a dupe to delete.

### Related but distinct (no action suggested)
- afc/east/dolphins/cuban-sandwich.md vs nfc/south/buccaneers/tampa-cuban-sandwich-with-salami.md: both are pressed Cuban sandwiches. The Tampa one adds Genoa salami and uses no mojo pork, and the salami is the Tampa-versus-Miami point of the rivalry. Distinct and worth keeping both, with the contrast stated.
- afc/north/bengals/cheese-coneys.md vs nfc/north/lions/detroit-coney-dogs.md: Cincinnati coney (cocoa/cinnamon sauce, cheddar pile) versus Detroit coney (cumin/paprika, no cheese, mustard and onion). Different regional styles; local claims are clear (Cincinnati versus Detroit).

No other batch recipe duplicates an index entry: Buffalo wings differ from the Commanders mumbo wings and Falcons lemon-pepper wings; Boston baked beans differ from KC barbecue baked beans; the Cuban black beans do not overlap with the Spanish bean soup; the Polish Boy is not the Browns pierogi.

## Course findings
None. Mild judgment only: New York bagels as "meals" (there is no breakfast course).
