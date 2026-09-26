# Worker nfc-west-1

Batch: 49ers (cioppino, mission-style-burritos), Cardinals (fry-bread-tacos,
sonoran-hot-dogs), plus exclusively-assigned component roasted-salsa-verde.
Date checked: 2026-09-26. `docs/reviews/2026-09-26-scratch-components.md` used only
as a lead, not proof.

## cioppino

- ID `cioppino`, path `recipes/nfc/west/49ers/cioppino.md`, status `published`,
  source `https://www.saveur.com/article/recipes/cioppino/`, checked 2026-09-26,
  hash `d187bf3f13012c236adc8e8a6a71b64093c9af4e`.
- **City fit**: Pass. Saveur's recipe is explicitly the Tadich Grill (San Francisco,
  est. 1849) cioppino, originally published in a 2001 "Big Soup" feature and updated
  in 2023 (confirmed via WebSearch snippets of the live page). Strong, direct match
  for a San Francisco Bay Area team.
- **Authenticity**: Baseline. Cioppino is the North Beach Italian-immigrant
  fisherman's stew (Genoese "ciuppin" etymology is the better-supported origin; the
  popular "chip in" folk etymology is disputed and should not be stated as fact).
  Our file follows the restaurant-attributed Tadich Grill/Saveur formula: soffritto
  → long tomato-broth simmer → dredge-and-sear firm seafood → crab warmed through →
  wine-deglazed clams folded in at the end. Dungeness crab, bay shrimp and sourdough
  are all correct, defining San Francisco Bay ingredients (also called out correctly
  in the file's own Kitchen Notes).
- **Source fidelity**: Primary source could not be read directly (see Access
  failures). Against a matching third-party transcription of the same Tadich
  Grill/Saveur recipe (cabcooks.wordpress.com), two possible discrepancies surfaced,
  both medium-confidence only:
  1. Garlic — our file's "2 garlic cloves, finely chopped" is used only in the
     seafood-searing step; the corroborating transcription divides garlic between
     the vegetable/broth base and the seafood sear.
  2. Wine — our file's "2 cups dry white wine" (used only to deglaze for the clams)
     vs. the transcription's "2 1/2 cups dry white wine, divided."
  Everything else (seafood list, quantities, yield of 8, method order) matches.
- **Specificity**: Good as-is — Dungeness crab and bay shrimp already carry regional
  labeling; "halibut or other firm white fish" is a reasonable substitution note.
  Optional polish: name a typical dry white (e.g., Sauvignon Blanc) for the wine;
  low priority.
- **Components**: None used or needed. Toasted sourdough is a simple optional side,
  not a componentization candidate. No shared consumers to flag.
- **Readability**: A — quantities, divisions (butter/oil "divided"), times and
  temperatures are all explicit; steps are ordered and end-pointed.
- **Decision**: Targeted fix — reorder/verify garlic split and wine quantity once
  the primary source is reachable; nothing else needs to change.
- **Findings**:
  1. Minor, confidence medium (secondary corroboration only). Current: "2 garlic
     cloves, finely chopped" used once, in the seafood sear. Proposed: confirm
     whether source splits garlic across the vegetable base and the sear, and
     divide accordingly if so. Rationale: aromatics in a long-simmered broth base
     usually benefit from garlic added early, not only in a quick sear. URL
     (secondary): https://cabcooks.wordpress.com/2011/01/09/cioppino-tadich-grill/.
     Section: Ingredients / Instructions steps 1 & 3.
  2. Minor, confidence medium (same caveat). Current: "2 cups dry white wine," used
     only in step 4. Proposed: verify against primary source whether total wine is
     2 1/2 cups and/or divided across two uses. Section: Ingredients / step 4.
  3. Informational, not a finding: `pekinthechef.com/tadichgrill/cioppino` was
     checked and rejected as corroboration — despite its URL it describes a
     materially different, simpler recipe (serves 6; no butter, scallops, crab,
     fennel or leek; mussels instead of Manila clams). Do not use it to support or
     contradict this file.
- **Replacement candidates**: Not applicable — source is sound; no replacement
  needed.
- **Access failures**: Primary source `https://www.saveur.com/article/recipes/cioppino/`
  returned HTTP 403 on the initial fetch and again on one retry — full text was
  **not** read directly. Mitigated with (a) WebSearch snippets confirming the
  Tadich Grill attribution, 2001/2023 publication history, and serves-8 yield, and
  (b) the cabcooks.wordpress.com transcription as labeled secondary corroboration.
  The garlic and wine findings above should be treated as leads pending direct
  confirmation, not confirmed errors.

## mission-style-burritos

- ID `mission-style-burritos`, path
  `recipes/nfc/west/49ers/mission-style-burritos.md`, status `published`, source
  `https://www.pantsinthekitchen.com/recipes/mission-burrito`, checked 2026-09-26,
  hash `4e9dcefd05833df5305a03b9520f4b480f110ac4`. Source fetched and read directly
  in full.
- **City fit**: Pass, strong. Source explicitly names "Taquería El Farolito - San
  Francisco, CA" as its inspiration. Mission-style burrito is definitionally a San
  Francisco Bay Area dish.
- **Authenticity**: Supported variant. The generic "classic" Mission burrito
  baseline (steamed oversized flour tortilla; rice, beans, grilled meat, cheese,
  salsa, foil wrap; commonly also sour cream and guacamole) is well established.
  This source — and our file, faithfully — includes rice, beans, carne asada,
  cheese, salsa verde and the foil wrap, but only plain sliced avocado and no sour
  cream. That is a source-level authenticity observation (the cited home-cook
  source is a leaner variant of the wider Mission-burrito category), not a
  transcription error: our file accurately reflects what its own source specifies.
- **Source fidelity**: Marinade, rice method/quantities, pico ingredients, steak
  searing method and tortilla-size guidance all match the source closely. Two real
  discrepancies:
  1. Beans salt — source specifies "2 tsp salt"; our file says "start with 1/2
     teaspoon kosher salt, then adjust after simmering," a 3/4 reduction that is
     not labeled as a deliberate adaptation (contrast with this same source's
     roasted-salsa-verde component, whose Note explicitly documents its own salt
     reduction).
  2. Assembly order — source layers cheese, meat, pico, **salsa verde**, rice,
     beans, avocado; our file adds salsa "to taste" after avocado instead of mid-
     stack. Minor, unlikely to affect the result.
  Also: source offers an optional pan-sear-to-seal finish as an alternative to
  foil-wrapping; our file presents foil-wrap only. This is a reasonable,
  source-supported simplification, not an error, but worth a mention since it
  drops one of two source-offered closing techniques.
- **Specificity**: Chili powder is already labeled "mild"; cheese is specified as
  Monterey Jack and cheddar; tortilla size given as "about 12-13 inches" (should be
  labeled as an editorial estimate — the source's exact-inch figure was not
  independently confirmed against the fetched text, only the general "large
  sandwich wrap" description). Optional: name a specific large-format tortilla
  example (e.g., a 12" burrito-size flour tortilla).
- **Components**: Uses `{{component:roasted-salsa-verde}}` correctly; verified
  match against its shared source (see component section below). Existing
  `fresh-pico-de-gallo` and `quick-guacamole` (reviewed by a different worker,
  front matter only peeked here) considered as reuse candidates:
  - `fresh-pico-de-gallo` (2 tomatoes ~12oz, 1/2 white onion, jalapeño/serrano,
    cilantro, 2 tbsp lime, ~1/2 tsp salt) is similar in spirit to but not identical
    to this recipe's own sourced pico (3-4 Roma tomatoes, 1/4 red onion, juice of 1
    lime, 1-2 tbsp cilantro, jalapeño/serrano, salt to taste — different onion type
    and ratios). Recommend the orchestrator weigh book-wide consistency (reuse)
    against preserving this recipe's own cited proportions; not flagging as an
    error either way.
  - `quick-guacamole` is not a good fit here: this recipe's own source calls for
    plain sliced avocado, not guacamole. Recommend leaving as-is rather than
    substituting, to preserve fidelity to the cited source.
  No new component candidates proposed; rice, beans and the carne asada marinade
  are recipe-specific and not observed reused elsewhere in this batch.
- **Readability**: B — clear, ordered, with explicit times/temperatures, but the
  unlabeled salt reduction and the "to taste" salsa placement (rather than a fixed
  layer position) are minor ambiguities.
- **Decision**: Targeted fix — label or restore the bean salt quantity; other items
  are optional polish.
- **Findings**:
  1. Moderate, confidence high (source read directly). Current: "start with 1/2
     teaspoon kosher salt, then adjust after simmering" (Beans). Source: "2 tsp
     salt." Proposed: raise the starting salt toward the source figure, or add an
     explicit adaptation note as done in roasted-salsa-verde.md's Note. Rationale:
     consistency with the cookbook's own established labeling practice; as written
     a cook has no signal the amount was cut by three-quarters. URL:
     https://www.pantsinthekitchen.com/recipes/mission-burrito. Section:
     Ingredients / Beans.
  2. Minor, confidence high. Current: assembly (step 6) adds salsa verde "to
     taste" after avocado; source layers salsa verde before rice/beans. Proposed:
     optional reorder, or note the simplification. Section: Instructions step 6.
  3. Minor, confidence high. Source's optional pan-sear-to-seal closing technique
     is not mentioned; only foil-wrap is presented. Proposed: optionally mention it
     as an alternative. Section: Instructions step 7.
- **Replacement candidates**: Not applicable — source is sound.
- **Access failures**: None. Source fetched and read directly in full.

## fry-bread-tacos

- ID `fry-bread-tacos`, path `recipes/nfc/west/cardinals/fry-bread-tacos.md`,
  status `published`, source
  `https://www.foodnetwork.com/recipes/indian-taco-recipe-1939718`, checked
  2026-09-26, hash `50f7ebdb62b000729542bbfb8de2f3de908e8075`. Source (Food
  Network, "Indian Taco," courtesy Roberta Kesselring) fetched and read directly in
  full.
- **City fit**: Pass at the state level, with a caveat. Fry bread tacos (Navajo/
  Indian tacos) were voted Arizona's official state dish in a 1995 Arizona Republic
  reader poll, supporting a statewide fit for the Phoenix-based Cardinals. The
  dish's actual origin, however, traces to Navajo Nation history — fry bread grew
  out of the U.S. government's forced 1864 "Long Walk" relocation to Bosque
  Redondo, New Mexico — not to Phoenix specifically. Recommend the book frame this
  as a dish of Native American origin that Arizona has statewide adopted, rather
  than implying a Phoenix-native invention.
- **Authenticity**: Baseline/traditional. Fry bread + seasoned beef + refried
  beans + standard taco toppings is the standard Indian taco construction; our
  recipe follows a real published home-cook source rather than an invented
  composite.
- **Source fidelity**: Dough ingredients/quantities (flour, baking powder, salt,
  sugar, powdered milk, lard, water) and the beef/beans base match the source
  almost exactly. Three real discrepancies:
  1. Source's frying instruction says to "puncture [each round] once or twice"
     before/during frying (a standard technique to stop uneven puffing). Our
     file's step 4 omits this entirely.
  2. Source's topping list includes "Chopped olives"; our optional-toppings list
     (cheese, tomato, onion, roasted green chiles, roasted salsa verde, sour
     cream) omits olives.
  3. Source's meat seasoning is just generic "Taco seasoning (to taste)"; our file
     substitutes a specific from-scratch blend ("Suggested starting beef
     seasoning: 1 tablespoon mild ground chile..."). This is clearly labeled as a
     suggestion and is a defensible editorial addition, not a fidelity violation —
     but it is not a verified traditional proportion and should be understood as
     editorial.
  Also, `photo_credit: Instant Pot` in the front matter looks like a mismatched/
  copy-paste value for what is a stovetop-fried dish; flagging for the
  orchestrator since front-matter edits are outside my remit.
- **Specificity**: Good — "mild ground chile" and "cheddar or Monterey Jack" are
  already style-labeled; lard vs. margarine is offered as a traditional-vs-
  convenient choice, which is appropriate.
- **Components**: Uses `{{component:roasted-salsa-verde}}` correctly as one topping
  option. No other component gaps; the 1 cup refried beans is a simple, likely
  canned ingredient and not a strong componentization candidate.
- **Readability**: D — unreliable/contradictory step order. Step 4 ends "Fry until
  golden on both sides and drain on paper," then step 5 opens "Let mixed fry-bread
  dough rest covered at least 15 minutes if time allows... this editorial rest
  makes shaping easier," i.e., an instruction to rest the dough before shaping
  appears after the dough has already been shaped and fried.
- **Decision**: Targeted fix — the step-order contradiction should be corrected
  first; the puncture step and olives are secondary polish.
- **Findings**:
  1. Major, confidence high. Current: Instructions steps 4-5 as quoted above.
     Proposed: move the resting instruction to immediately follow step 2 (dough
     mixed and refrigerated), before oil is heated and rounds are shaped/fried, or
     renumber so resting precedes shaping. Rationale: readability grade D per the
     rubric ("unreliable or contradictory"); structural fix only, not a content
     change. Section: Instructions steps 4-5.
  2. Minor, confidence high (source read directly). Current: step 4 has no
     puncture instruction. Proposed: add "piercing each round once or twice before
     frying" to step 4. Rationale: brief instructs not to simplify away defining
     technique. URL:
     https://www.foodnetwork.com/recipes/indian-taco-recipe-1939718. Section:
     Instructions step 4.
  3. Minor, confidence high. Current: optional toppings list omits olives.
     Proposed: add chopped/sliced olives as an optional topping, or note the
     omission is intentional. Section: Ingredients (optional toppings).
  4. Minor, confidence medium. `photo_credit: Instant Pot` appears mismatched for
     this stovetop-fried dish — flagged for the orchestrator to check.
- **Replacement candidates**: Not applicable — source is sound once the step order
  is fixed.
- **Access failures**: None. Source fetched and read directly in full.

## sonoran-hot-dogs

- ID `sonoran-hot-dogs`, path `recipes/nfc/west/cardinals/sonoran-hot-dogs.md`,
  status `published`, source `https://www.saveur.com/recipes/sonoran-dogs/`,
  checked 2026-09-26, hash `fab12522c218f05c6ba167149b2a04bb029653f8`. This
  saveur.com URL fetched and read directly in full on the first attempt (unlike
  the cioppino saveur.com URL, which failed) — full primary text was read
  directly.
- **City fit**: Pass, regional. Sonoran hot dogs originated in Hermosillo, Sonora,
  Mexico, and are most iconically associated with Tucson (El Güero Canelo, James
  Beard America's Classics recognition, extensive national coverage naming Tucson
  specifically). Phoenix also has a genuine, documented tradition of Sonoran-style
  vendors (e.g., "Nogales Hot Dogs," cited in coverage of the format). This
  supports an Arizona/Sonoran-borderland regional pass for the Phoenix-based
  Cardinals, with the explicit caveat that Tucson, not Phoenix, is the dish's more
  iconic city — consistent with the brief's allowance that regional adoption is
  valid without requiring the team's metro to hold an exclusive/originating claim.
  Note: a different, unrelated dish — bacon-wrapped Los Angeles-style street dogs
  — was reviewed separately in `workers/afc-west-1.md`; that is a distinct format
  and not a duplicate or conflict with this entry.
- **Authenticity**: Baseline. Saveur's own recipe closely matches the canonical
  Sonoran dog formula: bacon-wrapped dog, pinto beans, grilled onions, tomato,
  avocado, jalapeño-based sauce, mayonnaise and mustard, bolillo-style roll.
- **Source fidelity**: Matches almost exactly across every ingredient and
  instruction — jalapeño sauce method, bacon-wrap, beans, onions, roll-steaming,
  toppings and assembly all align with the source. No discrepancies found.
- **Specificity**: Already a strong example of this check done well. "8 jumbo
  all-beef hot dogs (beef is Tucson-style recommendation; source says jumbo dogs)"
  correctly distinguishes the source's plain spec from an added regional
  recommendation; rolls are specified as "bolillo-style Sonoran hot-dog rolls, or
  soft bolillos." No changes recommended.
- **Components**: None used. The jalapeño sauce is bespoke to this recipe; no
  other recipe in this batch references a similar sauce, so I see no reuse case
  forcing extraction into a shared component. Optional for the orchestrator to
  reconsider if a similar sauce turns up elsewhere in the book, but not required.
- **Readability**: A — clear quantities, ordered steps, explicit times/
  temperatures and endpoints throughout.
- **Decision**: Keep. Positive evidence: full primary source read directly and
  found to match this file on every ingredient, quantity and step; regional fit
  and authenticity both hold with the Tucson-vs-Phoenix caveat noted above.
- **Findings**: None.
- **Replacement candidates**: Not applicable.
- **Access failures**: None. Source fetched and read directly in full.

## component:roasted-salsa-verde

- ID `roasted-salsa-verde`, path `components/sauces/roasted-salsa-verde.md`,
  status `published`, source
  `https://www.pantsinthekitchen.com/recipes/mission-burrito` (same page as
  mission-style-burritos), checked 2026-09-26, hash
  `92c698dd1976461ee1c40d7e7e1b1445c549e474`. Source fetched and read directly in
  full.
- **Consumers**: `grep -rl '{{component:roasted-salsa-verde}}' recipes components`
  returns exactly two files, both inside my own assigned batch —
  `recipes/nfc/west/49ers/mission-style-burritos.md` and
  `recipes/nfc/west/cardinals/fry-bread-tacos.md`. No external consumers to flag.
- **Fidelity vs. source**: Tomatillos (1/2 lb), onion (1/4 cup chopped), garlic (1
  clove), serrano (1, stemmed/seeded), light oil coat, lime (1, half used) and the
  roast-then-blend method all match the source's roasted salsa verde formula. The
  file's own Note already labels its one deliberate deviation: starting salt cut
  from the source's ~1 teaspoon to 1/4 teaspoon, "to allow adjustment for the rest
  of the meal" — exactly the good labeling practice missing from
  mission-style-burritos' bean salt (see that section above).
- **Relation to prior lead**: `docs/reviews/2026-09-26-scratch-components.md`
  recorded this component's prior decision as "Tune" ("specify onion cut/oil
  quantity and label lower starting salt as adaptation"). The current file already
  specifies onion cut ("roughly chopped"), oil quantity ("1 teaspoon... or enough
  to lightly coat"), and labels the salt reduction — the prior Tune items appear
  already addressed.
- **Specificity**: Serrano is specified (regional heat level); could optionally
  suggest a substitute (e.g., jalapeño for milder heat) but this is minor.
- **Readability**: A — clear roast times/temperatures (450°F, 10 min + 5 min) and
  a clear blend-and-adjust endpoint.
- **Decision**: Keep. Positive evidence: source read directly and matches the
  component's ingredients and method; the one intentional deviation (salt) is
  already transparently labeled.
- **Findings**: None.
- **Replacement candidates**: Not applicable.
- **Access failures**: None. Source fetched and read directly in full.
