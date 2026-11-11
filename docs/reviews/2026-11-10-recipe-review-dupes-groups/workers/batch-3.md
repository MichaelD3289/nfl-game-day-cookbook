# Batch 3 review (18 recipes)

| recipe path | grouping | duplicate | course |
|---|---|---|---|
| recipes/afc/south/titans/nashville-hot-chicken.md | finding (regroup) | none | ok |
| recipes/afc/west/broncos/colorado-pork-green-chile.md | pass | none | ok |
| recipes/afc/west/broncos/denver-omelet.md | pass | none | ok |
| recipes/afc/west/broncos/green-chile-breakfast-burritos.md | pass | none | ok |
| recipes/afc/west/chargers/bacon-wrapped-la-street-dogs-chargers.md | finding (salt used, not listed) | exact pair with rams/bacon-wrapped-la-street-dogs-rams | ok |
| recipes/afc/west/chargers/french-dip-sandwiches-chargers.md | finding (regroup, stray "divided") | exact pair with rams/french-dip-sandwiches-rams | ok |
| recipes/afc/west/chiefs/barbecue-baked-beans.md | pass | near-dup (moderate) with patriots/boston-baked-beans | ok |
| recipes/afc/west/chiefs/kansas-city-burnt-ends.md | pass | none | ok |
| recipes/afc/west/chiefs/kansas-city-cheesy-corn.md | pass | none | ok |
| recipes/afc/west/chiefs/kansas-city-style-barbecue-chicken.md | pass | none | ok |
| recipes/afc/west/raiders/casino-style-prime-rib.md | pass | none | ok |
| recipes/afc/west/raiders/old-vegas-shrimp-cocktail.md | finding (minor: split sauce) | related, low, with colts/st-elmo-style-shrimp-cocktail | ok |
| recipes/nfc/east/commanders/chicken-wings-with-mumbo-sauce.md | pass | none | ok |
| recipes/nfc/east/commanders/half-smoke-chili-dogs.md | pass | near-dup (moderate) with lions/detroit-coney-dogs (and bengals/cheese-coneys, weaker) | ok |
| recipes/nfc/east/cowboys/tex-mex-cheese-enchiladas.md | pass | none | ok |
| recipes/nfc/east/cowboys/texas-red-chili.md | pass | none | ok |
| recipes/nfc/east/eagles/philadelphia-soft-pretzels.md | finding (topping misfiled at top) | none | ok |
| recipes/nfc/east/eagles/philly-cheesesteak.md | pass | none | ok |

Counts: grouping findings 5 (Nashville, Chargers dogs, Chargers French dip, shrimp cocktail, pretzels); duplicates 2 exact + 3 near; course 0.

## Grouping findings

### nashville-hot-chicken (recommended)
One ungrouped list (plus "For serving") holds four separate components in step order: seasoned chicken, egg-buttermilk dip, flour dredge, hot paste. The frying oil sits in the middle of the list and is used for both frying and the paste. Proposed:
- `### Chicken`: chickens; black pepper; 2 tablespoons plus 4 teaspoons Diamond Crystal salt (divided, so say which part goes where, or leave as is)
- `### Buttermilk dip`: eggs; buttermilk; 2 tablespoons hot sauce
- `### Flour dredge`: 4 cups flour (the remaining salt is the same salt line above; consider splitting it as "2 tablespoons for the chicken" / "4 teaspoons for the flour")
- `### Frying`: about 10 cups vegetable oil {{no-scale}}
- `### Hot paste`: cayenne; brown sugar; chili powder; garlic powder; paprika
- `### For serving`: unchanged.
Nothing is unused or unlisted.

### bacon-wrapped-la-street-dogs-chargers (unlisted ingredient; same issue in Rams copy)
Step 2: "sprinkle lightly with sea salt or seasoning salt", but no salt line exists. The changelog note says the source's finishing salt was added, but only to the steps. Proposed: add `- Sea salt or seasoning salt, to sprinkle on the bacon` to the list. Grouping otherwise fine for a single assembled dish; optional split into `### Dogs` and `### Toppings` (cilantro, ketchup, mustard, mayonnaise, grilled vegetables) is not needed.

### french-dip-sandwiches-chargers (minor, same in Rams copy)
Single group holds three parts. Current lines 1-10 are all under one list. Proposed:
- `### Tri-tip`: tri-tip; 1½ tsp kosher salt; granulated garlic; granulated onion; black pepper; olive oil
- `### Jus`: 2 cups beef stock; ½ cup red wine; salt and pepper, to taste
- `### Sandwiches`: French rolls
Also "2 cups low-sodium beef stock, divided" has nothing to divide in the steps (step 3 uses 2 cups, or 2½ with the wine swap). Drop "divided".

### old-vegas-shrimp-cocktail (minor, optional)
Shrimp plus a six-item cocktail sauce in one list. Proposed `### Shrimp` (shrimp) and `### Cocktail sauce` (ketchup, chili sauce, horseradish, lemon juice, Worcestershire, optional hot sauce); keep `### For serving` (lemon wedges). Low value; fine to skip.

### philadelphia-soft-pretzels
Current top-of-list ungrouped lines:
- Pretzel or kosher salt for topping
- Optional: homemade American yellow mustard ... {{component:american-yellow-mustard}}
They sit before `### Dough` and `### Bath`, so they read as part of nothing. Proposed: move both to a final `### Topping and serving` group (salt, mustard), after Dough and Bath. Nothing unused or unlisted. (Unrelated: step 5 repeats step 3's drain/bake guidance; not a grouping issue.)

## Duplicate findings

Confirmed exact (diffed bodies; only id/image/report note differ, and Rams dog text differs slightly in wording):
- chargers/bacon-wrapped-la-street-dogs-chargers vs rams/bacon-wrapped-la-street-dogs-rams: same source URL and same preparation. Local claim (judgment): Rams/LA. The Chargers were in LA only 2017-2023 and San Diego before that, so a Los Angeles dish fits the Rams better; though a Chargers claim is plausible for the current LA market. Not for me to decide.
- chargers/french-dip-sandwiches-chargers vs rams/french-dip-sandwiches-rams: identical text and source. Local claim (judgment): Rams/LA (Philippe's and Cole's both claim the original, both downtown LA). Same Chargers caveat.

Near-duplicates (validator would miss):
- afc/west/chiefs/barbecue-baked-beans vs afc/east/patriots/boston-baked-beans (moderate): both are slow-baked navy/white beans with brown sugar, a molasses-type sweetener (sorghum vs molasses), onion, dry mustard and cured/smoked pork or beef, baked 5-6 hours in a pot at 275-300F. Differences: sorghum, soy, Worcestershire and brisket burnt ends vs molasses and salt pork. Different sources. Claim (judgment): Boston is the origin of the dish and has the stronger claim to "baked beans"; KC's version is a defensible barbecue-side variant, distinct mainly by burnt ends. Keep both is reasonable.
- nfc/east/commanders/half-smoke-chili-dogs vs nfc/north/lions/detroit-coney-dogs (moderate): both are beef chili over a dog in a bun with yellow mustard and chopped white onion, no cheese, no beans, and both use a spiced tomato-based beef chili. Differences: DC uses a half-smoke sausage and 3-hour chili with bell pepper; Detroit uses natural-casing franks and a 40-minute chili. Weaker overlap with afc/north/bengals/cheese-coneys (cocoa-cinnamon Cincinnati chili, cheddar). Claim (judgment): each city has its own named sausage/chili style; the half-smoke is distinctly DC, so Commanders hold a strong claim; the overlap is the topping template, not a true duplicate.
- afc/west/raiders/old-vegas-shrimp-cocktail vs afc/south/colts/st-elmo-style-shrimp-cocktail (low): both are chilled shrimp with a ketchup/horseradish cocktail sauce. Vegas: small cooked shrimp in glasses with ketchup-chili sauce; St. Elmo: poached jumbo raw shrimp with a horseradish-heavy sauce. Different shrimp, method and sauce; both have legitimate local identity (Golden Gate / St. Elmo). Not recommending action.

Considered and not flagged: bacon-wrapped LA street dogs vs nfc/west/cardinals/sonoran-hot-dogs (both bacon-wrapped dogs, but Sonoran adds beans, tomato, avocado, jalapeño sauce and a bolillo; distinct enough).

## Course
No findings. Baked beans and cheesy corn as sides, shrimp cocktail, mumbo wings and pretzels as appetizers all fit.
