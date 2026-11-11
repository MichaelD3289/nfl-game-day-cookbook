# Batch 2 review: ingredient groups, duplicates, course

Reviewed 18 recipes (read-only). Group findings are marked severity: **clear** (wrong or missing groups, or listed/used mismatch) or **optional** (would read better, not wrong).

| recipe path | grouping | duplicate | course |
|---|---|---|---|
| recipes/afc/north/browns/potato-and-cheese-pierogi.md | pass | pair with steelers/pierogi | ok |
| recipes/afc/north/ravens/baltimore-crab-cakes.md | pass (lemon in step 4 not listed; trivial) | none | ok |
| recipes/afc/north/ravens/berger-cookies.md | pass | none | ok |
| recipes/afc/north/ravens/pit-beef-sandwiches.md | finding (optional) | none | ok |
| recipes/afc/north/steelers/chipped-ham-barbecue-sandwiches.md | finding (optional) | none | ok |
| recipes/afc/north/steelers/haluski-cabbage-and-noodles.md | finding (minor: green onions) | none | finding (borderline: sides?) |
| recipes/afc/north/steelers/pierogi.md | pass | pair with browns/potato-and-cheese-pierogi | ok |
| recipes/afc/north/steelers/primanti-style-sandwiches.md | finding (clear) | none | ok |
| recipes/afc/south/colts/breaded-pork-tenderloin-sandwich.md | finding (optional) | none | ok |
| recipes/afc/south/colts/st-elmo-style-shrimp-cocktail.md | pass | none (see note on Raiders shrimp cocktail) | ok |
| recipes/afc/south/colts/sugar-cream-pie.md | pass | none | ok |
| recipes/afc/south/jaguars/camel-rider-sandwich.md | pass | none | ok |
| recipes/afc/south/jaguars/mayport-shrimp-and-grits.md | finding (optional) | none | ok |
| recipes/afc/south/texans/fajitas.md | finding (clear) | none | ok |
| recipes/afc/south/texans/sausage-kolaches-or-klobasneks.md | pass | none | ok |
| recipes/afc/south/texans/viet-cajun-crawfish.md | finding (clear) | none | ok |
| recipes/afc/south/titans/goo-goo-clusters.md | finding (clear: cornstarch unlisted, peanuts placement) | none | ok |
| recipes/afc/south/titans/meat-and-three-plate-with-meatloaf.md | pass | none | ok |

Counts: grouping findings 8 (5 clear/minor-with-substance, 3 optional), duplicate pairs 1, course findings 1 (borderline).

## Duplicates

### Pierogi: browns/potato-and-cheese-pierogi vs steelers/pierogi (near-duplicate)

Both files read. Same dish (potato-and-cheese dumpling, boiled, finished in butter), different sources (Cleveland Magazine vs Food Network Kitchen) and small differences: Browns uses Velveeta + American cheese, a 5 lb potato batch (3-4 dozen), butter-only finish. Steelers uses white cheddar, caramelized onions folded into the filling and the finishing butter, sour cream in dough and to serve (about 2 1/2 dozen). A reader gets two pierogi recipes in one book; the validator would miss it (different ids, URLs, text).

Claim (judgment, not verified): both cities have a genuine Polish/Slovak pierogi culture. Pittsburgh's claim is probably the stronger and more widely recognised nationally (the Pirates pierogi race, church-sale pierogi, and the Steelers already carry haluski, which is traditionally eaten alongside). Cleveland has strong ties too (Parma and the Slavic Village area, plus the Polish Boy already filed under the Browns, which brings the Polish theme to Cleveland without repeating pierogi). If one must go, Cleveland's pierogi is the more replaceable. Decision left to the owner.

### Considered, not flagged

- st-elmo-style-shrimp-cocktail (Colts) vs raiders/old-vegas-shrimp-cocktail: both shrimp cocktail, but the preparations differ (poached jumbo raw shrimp and a horseradish-forward sauce vs cooked salad shrimp in a ketchup/chili-sauce cocktail served in chilled glasses) and each is a named local icon (St. Elmo vs the Golden Gate/Vegas cocktail). Related, not a duplicate; mentioned only so the owner knows two shrimp cocktails exist.
- primanti-style-sandwiches vs browns/polish-boy-sandwich: both pile fries and slaw on a sandwich, but the proteins, bread and sauces differ; distinct dishes.
- pit-beef-sandwiches vs beef-on-weck (Bills): both thin-sliced roast beef with horseradish, but roll, seasoning, cooking method and place differ; distinct.

## Findings by recipe

### recipes/afc/north/ravens/pit-beef-sandwiches.md (optional)

Single flat list with two clear parts: a seasoned roast and the sandwich assembly. The 7-line rub sits above the beef, then rolls/sauce/onion.

Proposed:

```
### Beef and rub
- 2 tablespoons kosher salt
- 1 tablespoon coarsely ground black pepper
- 1 teaspoon each dried oregano, garlic powder, onion powder, paprika and chili powder
- 1 (4-pound) bottom round roast (top round also works)

### Sandwiches
- 10 kaiser rolls
- 1 cup homemade tiger sauce ... {{component:baltimore-horseradish-sauce}}
- 1 sweet white onion, thinly sliced
```

### recipes/afc/north/steelers/chipped-ham-barbecue-sandwiches.md (optional)

Seven sauce ingredients (brown sugar, ketchup, vinegar, Worcestershire, mustard, salt and pepper, onion powder) are mixed with the ham list; step 1 makes "the sauce" as a distinct part.

Proposed:

```
### Barbecue sauce
- 1/4 cup brown sugar
- 1 1/2 cups ketchup
- 1/4 cup apple cider vinegar
- 1 tablespoon Worcestershire sauce
- 1 tablespoon yellow mustard
- 1 tablespoon onion powder
- Salt and pepper, to taste

### Sandwiches
- 1 pound Isaly's chipped chopped ham ...
- 4 soft hamburger or Kaiser buns ...
```

### recipes/afc/north/steelers/haluski-cabbage-and-noodles.md

Grouping (minor): "2 green onions, chopped" is in the main list but step 3 uses it only to serve ("Serve with green onions"). A `### For serving` group already exists with only sour cream.

```
### For serving
- 2 green onions, chopped
- Sour cream, optional
```

Course (borderline, judgment): haluski is traditionally a side dish in Pittsburgh (served with pierogi, kielbasa or at church dinners). Here the kielbasa is optional and the recipe yields 8 servings from 8 oz of noodles and 1.5 lb of cabbage, which reads as a side. `course: sides` may be more accurate, unless the owner wants it as a meatless main. Left to the owner.

### recipes/afc/north/steelers/primanti-style-sandwiches.md (clear)

No groups, but the dish has three separate preparations in the steps: slaw (step 1), fries (step 2), sandwich assembly (steps 3 and 4). Current lines are one flat list of 12.

Proposed:

```
### Slaw
- 3 cups finely shredded Savoy cabbage
- 1 tablespoon cider vinegar
- 2 teaspoons extra-virgin olive oil
- 1/4 teaspoon crushed celery seed
- 1/4 teaspoon kosher salt, plus more to season
- 1/4 teaspoon sugar

### Fries
- 2 small russet potatoes
- Vegetable oil, for frying

### Sandwiches
- 4 ounces sliced capicola (hot or sweet, to preference)
- 4 ounces sliced provolone
- 4 thick slices thick-cut, soft Italian sandwich bread, ...
- 1 ripe tomato, sliced
```

Note: "plus more to season" salt is for the fries; the Fries group could carry "Kosher salt, to season" instead.

### recipes/afc/south/colts/breaded-pork-tenderloin-sandwich.md (optional)

Cutlet, breading and oil are fine as one list, but the buns and toppings are assembly items filed with the breading and oil. A two-group split makes the sandwich assembly obvious:

```
### Breaded pork tenderloin
- 4 center-cut pork-loin cutlets, 5 ounces each
- 2 cups all-purpose flour
- 2 sleeves Ritz crackers, finely crushed
- 2 tablespoons garlic powder
- 1 tablespoon black pepper, ...
- 2 tablespoons salt
- 4 eggs
- 1 cup milk
- 40 ounces vegetable oil for deep frying ... {{no-scale}}

### Sandwiches
- 4 soft hamburger buns ...
- Classic toppings to taste: ...
```

Separate wording issue, not grouping: the pepper line says "see note" but the recipe has no Kitchen Notes; the duplicate-pepper explanation is only in step 2. Either add a note or drop "see note".

### recipes/afc/south/jaguars/mayport-shrimp-and-grits.md (optional)

Two dish parts (shrimp, grits) in one flat list that is not in method order: grits is the 10th line, Parmesan (a finish, step 4) is 5th, between parsley and Old Bay.

Proposed:

```
### Shrimp
- 1 pound large shrimp, ...
- 1 tablespoon extra-virgin olive oil
- 1 tablespoon butter
- 2 garlic cloves, thinly sliced
- 1 teaspoon Old Bay seasoning
- Juice of 1 large lemon
- 1/4 cup water
- 1 tablespoon chopped fresh parsley
- Kosher salt and freshly ground black pepper, to taste

### Grits and finish
- 4 servings homemade creamy stone-ground grits ... {{component:creamy-stone-ground-grits}}
- 1/2 cup grated Parmesan cheese
```

### recipes/afc/south/texans/fajitas.md (clear)

Uses inline pseudo-labels ("Rub:", "Vegetables:") inside a single flat list instead of `###` groups; the labels only appear on the first line of each part, so the rest of each part is unlabelled ("1 teaspoon kosher salt, for rub" etc.). Also, step 4 mentions sour cream, which is not listed anywhere.

Current lines (examples): `- Rub: 1 tablespoon paprika`, `- Vegetables: 2 red and 2 yellow bell peppers, cut into 1-inch strips`.

Proposed:

```
### Steak and rub
- 1 tablespoon paprika
- 2 teaspoons light brown sugar
- 1 1/2 teaspoons chili powder
- 1 teaspoon ground cumin
- 1/2 teaspoon chipotle chile powder
- 1/2 teaspoon garlic powder
- 1 teaspoon kosher salt
- 1 1/2 pounds skirt steak
- 1 tablespoon olive oil and juice of 1 lime
- Canola or other neutral oil, for grill grates

### Peppers and onions
- 2 red and 2 yellow bell peppers, cut into 1-inch strips
- 2 large red onions, thickly sliced
- 3 tablespoons olive oil and juice of 2 limes
- 1 teaspoon kosher salt

### For serving
- Warm flour tortillas, number to appetite
- Optional: homemade guacamole ... {{component:quick-guacamole}}
- Optional: homemade fresh pico de gallo ... {{component:fresh-pico-de-gallo}}
- Optional toppings: pickled jalapeños, lime wedges, chopped scallions, shredded cheddar, sour cream
```

Add sour cream to the optional toppings (listed in step 4 only). Lime wedges are optional topping; step 4 doesn't mention them, fine.

### recipes/afc/south/texans/viet-cajun-crawfish.md (clear)

The ungrouped list at the top holds 17 lines covering three jobs: the boil seasoning/aromatics, the vegetables added later (step 3), and the crawfish itself, followed by a single `### Garlic butter sauce` group. Mixing an unnamed block with a named group is inconsistent. Also `3 limes, cut into wedges` is filed under the garlic butter sauce but is tossed with the crawfish (step 5), not cooked into the sauce.

Proposed:

```
### Crawfish and boil
- 15 pounds live crawfish
- 1/2 to 1 1/2 cups powdered crawfish boil spice, ...
- 1/2 cup unfiltered apple cider vinegar
- 1/2 bunch celery, halved
- 3 stalks lemongrass, coarsely chopped
- 3 heads garlic, halved
- 1/2 large knob each ginger and galangal, chopped
- 1/2 bunch Thai basil
- 2 citrus (makrut lime) leaves
- 3 jalapeños, halved
- 4 oranges, 1 lemon and 3 limes, halved

### Vegetables
- 1 pound small new potatoes
- 1/2 pound carrots
- 12 boiling onions
- 1/2 pound long beans
- 1 pound snow or sugar snap peas
- 1/2 pound shiitake or oyster mushrooms

### Garlic butter sauce
- 1/2 pound (2 sticks) butter
- 4-6 cloves garlic, minced
- Crawfish boil spice, to taste

### For tossing
- 3 limes, cut into wedges
```

### recipes/afc/south/titans/goo-goo-clusters.md (clear)

Two issues.

1. Used but not listed: step 2 says "Spread on a cornstarch-dusted surface", and cornstarch is not in any group. Add it (for example `- Cornstarch, for dusting` under Nougat).
2. `- 3/4 cup salted roasted peanuts, chopped` is under `### Caramel`, but step 3 only spoons the caramel over the nougat and then "add[s] chopped salted roasted peanuts"; they are not cooked into the caramel. Move to an assembly group, or to Coating.

Proposed: keep Nougat (plus cornstarch), Caramel (condensed milk, butter, sugar, syrup, salt, vanilla), and add `### Assembly` (peanuts) before `### Coating` (milk chocolate); or combine as `### Topping and coating` (peanuts, chocolate).
