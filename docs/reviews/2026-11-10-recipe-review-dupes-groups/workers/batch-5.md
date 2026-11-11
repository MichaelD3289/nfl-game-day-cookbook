# Batch 5 review

| recipe path | grouping | duplicate | course |
|---|---|---|---|
| recipes/nfc/south/buccaneers/tampa-cuban-sandwich-with-salami.md | pass | near-dup with afc/east/dolphins/cuban-sandwich | ok |
| recipes/nfc/south/falcons/lemon-pepper-wet-wings.md | pass | none | ok |
| recipes/nfc/south/falcons/peach-cobbler.md | finding (minor) | none | ok |
| recipes/nfc/south/panthers/livermush-sandwiches.md | pass | none | ok |
| recipes/nfc/south/panthers/pimento-cheese-sandwiches.md | pass | none | ok |
| recipes/nfc/south/saints/beignets.md | pass | none | ok |
| recipes/nfc/south/saints/jambalaya.md | pass | none | ok |
| recipes/nfc/south/saints/muffuletta-sandwich.md | finding | none | ok |
| recipes/nfc/south/saints/red-beans-and-rice.md | pass | none | ok |
| recipes/nfc/south/saints/shrimp-po-boy.md | finding | none | ok |
| recipes/nfc/west/49ers/cioppino.md | pass | none | ok |
| recipes/nfc/west/49ers/mission-style-burritos.md | finding | none | ok |
| recipes/nfc/west/cardinals/fry-bread-tacos.md | finding | none | ok |
| recipes/nfc/west/cardinals/sonoran-hot-dogs.md | finding | near-dup with rams/chargers LA street dogs (family resemblance) | ok |
| recipes/nfc/west/rams/bacon-wrapped-la-street-dogs-rams.md | pass | pair with afc/west/chargers/bacon-wrapped-la-street-dogs-chargers (confirmed) | ok |
| recipes/nfc/west/rams/french-dip-sandwiches-rams.md | pass | pair with afc/west/chargers/french-dip-sandwiches-chargers (confirmed) | ok |
| recipes/nfc/west/seahawks/seattle-dogs-with-cream-cheese-and-onions.md | pass | none | ok |
| recipes/nfc/west/seahawks/seattle-style-chicken-teriyaki.md | pass | none | ok |

Counts: grouping findings 6 (5 real, 1 minor); duplicate findings 4 pairs (2 exact confirmed, 2 near); course findings 0.

Note on markdown: a blank line does not end a `###` group, so loose lines placed after a group's last bullet still belong to that group. This is the cause of the Muffuletta, Mission burrito and Sonoran findings.

## muffuletta-sandwich (grouping)

Everything sits under `### Olive salad`, including the loaf, meats and provolone:

```
### Olive salad
- 1 1/4 cups coarsely chopped cauliflower florets ... - 2 tablespoons red wine vinegar
- Kosher salt and black pepper, to taste
- 1 round 8-10-inch Italian sesame-seed loaf ...
- 6 ounces thinly sliced deli ham / Genoa salami / mortadella / provolone
```

Proposed:
- `### Olive salad`: cauliflower, olive oil, oregano, thyme, carrots, celery, water, green olives, Kalamata, roasted red peppers, banana peppers, red wine vinegar, kosher salt and black pepper (step 2 salts the olive salad).
- `### Sandwich`: sesame loaf, ham, Genoa salami, mortadella, provolone.

All ingredients are used and listed.

## shrimp-po-boy (grouping)

One flat list for a three-part dish (seasoning, fried shrimp, dressed roll). Proposed groups:
- `### Seasoning blend`: kosher salt, cayenne, garlic powder, paprika, oregano, thyme, black pepper, onion powder (the "first eight dry seasonings"; this ordering is already the step 1 dependency).
- `### Fried shrimp`: vegetable oil, shrimp, buttermilk, flour, cornmeal.
- `### Sandwich`: French rolls, rémoulade component, lettuce, tomatoes, pickles, hot sauce.

Step 1 says "first eight dry seasonings", which breaks if anyone reorders the list; a group name fixes that. Nothing unused or unlisted.

## mission-style-burritos (grouping)

The loose lines after `### Pico` are filed under Pico:

```
### Pico
- 3-4 seeded, diced Roma tomatoes
- 1/4 red onion ... salt to taste
(blank)
- 3-4 very large flour tortillas
- Shredded Monterey Jack and cheddar
- 1 avocado, sliced
- Homemade roasted salsa verde ... {{component:roasted-salsa-verde}}
- Aluminum foil for the classic wrap
```

Proposed: keep `### Pico` to the two pico lines; add `### Assembly` with tortillas, cheese, avocado, salsa verde component, foil.

Smaller notes: `### Carne asada` holds one line (steak) and `### Marinade` the rest. Either merge into `### Carne asada and marinade` or leave as is. Pico lines pack several ingredients per bullet; that is style only. The marinade's orange, onion and jalapeño are discarded per step 5, which is fine.

## fry-bread-tacos (grouping)

Flat list holding three components. Proposed:
- `### Taco meat`: ground chuck/sirloin, beef seasoning line, refried beans.
- `### Fry bread`: flour, baking powder, salt, sugar, powdered milk, lard or margarine, warm water, oil for frying.
- `### Toppings`: optional toppings line, optional salsa verde component.

All ingredients are used and listed.

## sonoran-hot-dogs (grouping)

After `### Jalapeño sauce`, the hot dogs, bacon, beans, onions, rolls and toppings all fall under the sauce group:

```
### Jalapeño sauce
- 4 jalapeños ... - Kosher salt, to taste
(blank)
- 8 jumbo all-beef hot dogs
- 8 regular-cut bacon slices
- 1 (15.5-ounce) can pinto beans ... - Kosher salt and black pepper, to taste
```

Proposed:
- `### Jalapeño sauce`: jalapeños, garlic clove, 1/2 medium onion, 2 tablespoons vegetable oil, kosher salt.
- `### Hot dogs`: hot dogs, bacon, 8 bolillo rolls.
- `### Beans and onions`: pinto beans, 2 tablespoons vegetable oil for onions, 2 white onions (final "Kosher salt and black pepper" line, which seasons the beans per step 2).
- `### Toppings`: tomatoes, avocados, mayonnaise and yellow mustard.

Two different "2 tablespoons vegetable oil" lines exist (sauce and onions); groups remove the ambiguity.

## peach-cobbler (grouping, minor)

The optional serving line sits under `### Topping`:

```
- 1-2 tablespoons milk or melted butter, for brushing

- Optional: coarse sparkling sugar and vanilla ice cream for serving
```

Coarse sugar belongs to the biscuit topping (step 4); ice cream is for serving. Low-impact options: split the line into "Optional: coarse sparkling sugar, for sprinkling" (kept under Topping) and "Vanilla ice cream, for serving" (new `### To serve`, or just a plain trailing line). Reasonable to leave as is.

## Duplicates

### bacon-wrapped-la-street-dogs (rams vs chargers): exact (validator-confirmed)
Same source URL (latinasquecomen.com/mexican-hot-dogs); ingredients and method are the same apart from wording; the Chargers' version is more detailed, with a 5-step method.

### french-dip-sandwiches (rams vs chargers): exact (validator-confirmed)
Identical ingredients and same source URL; the Rams Kitchen Notes even call it "the shared Chargers/Rams version". The Rams and Chargers share SoFi Stadium.

Local claim (judgment, not verified): both dishes are Los Angeles dishes (French dip: Philippe's and Cole's, downtown LA; the bacon-wrapped street dog is an LA street-cart food). The Rams are the Los Angeles team and play in Inglewood; the Chargers also moved to LA in 2017 and share SoFi Stadium, so the claim is nominally equal today. Historically, the Rams are the safer home for both, while the Chargers' San Diego heritage points to other dishes (for example fish tacos or California burritos). The editor decides.

### tampa-cuban-sandwich-with-salami vs afc/east/dolphins/cuban-sandwich: near-duplicate, probably acceptable
Different sources (Columbia Restaurant vs Food Network). Both are pressed Cuban bread sandwiches with ham, pork, Swiss, pickle and mustard. Distinctions: Tampa adds Genoa salami and has no butter or foil bake; Dolphins uses homemade mojo pork and bakes under a weighted sheet. The salami is the genuine Tampa/Miami dividing line, so the pair reads as two regional variants, not one dish. Judgment: Tampa has the stronger claim for the salami version and Miami for the plain one. Flagging for the editor's call, probably keep both.

### sonoran-hot-dogs (cardinals) vs bacon-wrapped-la-street-dogs (rams/chargers): near-duplicate in family
Both are bacon-wrapped all-beef dogs in soft rolls with mayo and mustard. Toppings differ (Sonoran: pinto beans, tomatoes, avocado, jalapeño sauce, bolillo; LA: peppers, onions, jalapeños, cilantro, ketchup in a regular bun), and sources differ. The LA street dog is a descendant of the Sonoran dog, so they are distinct dishes. Judgment: Arizona has the stronger claim to the original (Tucson/Phoenix). Los Angeles has a strong local claim to the "danger dog" street version. Keep both.

No near-duplicates found for the other recipes. Checked against the index: jambalaya and red beans (only New Orleans rice dishes besides the Dolphins' Cuban beans), muffuletta, po-boy (St. Elmo and Vegas shrimp cocktails differ), cioppino, burrito (Denver breakfast burritos differ), Seattle dog (Chicago/Detroit/Commanders dogs differ), teriyaki, wings (Buffalo and mumbo wings differ), pimento cheese, livermush, beignets, peach cobbler.

## Course
No course findings. Beignets and peach cobbler as desserts, wings as appetizers, and the rest as meals all look right.
