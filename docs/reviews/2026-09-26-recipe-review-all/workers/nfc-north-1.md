# Worker batch: nfc-north-1

Date checked: 2026-09-26. Prior review `docs/reviews/2026-09-26-scratch-components.md`
used as leads only, re-verified independently below.

## chicago-style-hot-dogs

- Recipe ID: chicago-style-hot-dogs. Path: `recipes/nfc/north/bears/chicago-style-hot-dogs.md`.
  Status: published. Source: https://www.pbs.org/food/recipes/chicago-style-hot-dog
  (fetched in full, direct read). Date checked: 2026-09-26. Input hash:
  `18db3d3378a3bb2141cb75419904cc6299b77637`.
- City fit: strong. Chicago-style hot dog is unambiguously a Chicago dish; recipe is
  filed under Bears/Chicago and every topping matches the city's defining formula.
- Authenticity: defining traits present — all-beef natural-casing frank, poppy-seed
  bun, yellow mustard, neon-green relish, chopped onion, tomato, dill pickle spear,
  sport peppers, celery salt, and (critically) no ketchup. This is the canonical
  "dragged through the garden" build; no other regional variant is supported or
  implied. Classification: standard/canonical, well evidenced.
- Source fidelity: two minor discrepancies against the PBS source.
  1. Source specifies 2 whole sport peppers per hot dog; our ingredient line reads
     "4–8 pickled sport peppers (1–2 per dog)," which permits as few as 1 — softer
     than the source's fixed amount.
  2. Source does not give a relish quantity; our line "about 1 tablespoon per dog" is
     an editorial addition, not sourced, and isn't labeled as an estimate.
  One deliberate, quality-motivated adaptation: source says to boil the franks; our
  step 1 says to keep the water "below a hard boil so the casings do not split" —
  a reasonable technique upgrade, not an error, but worth flagging as a deviation.
  Positive fidelity evidence: topping order (mustard → relish → onion → tomato →
  pickle → peppers → celery salt) matches the source exactly, and the pickle ratio
  (1 pickle cut into 4 spears for 4 dogs = source's 1/4 pickle per dog) matches exactly.
- Specificity: Vienna Beef named for the frank (correct, market-leading brand for
  this dish); poppy-seed bun specified; mustard/relish both correctly pointed at
  components with brand quick-options (French's, Vienna Beef relish). Good
  confidence, no changes needed.
- Components: `{{component:american-yellow-mustard}}` and
  `{{component:chicago-sweet-green-relish}}` both checked, both used exactly once.
  Per assignment, only american-yellow-mustard's usage here (not a full review) was
  checked: amount is "for a line on each dog" (no fixed quantity, appropriate for a
  condiment applied to a finished item), the marker sits on the finished
  Ingredients line describing how it's applied to the dog (not a raw pantry
  ingredient), and instructions step 3 references the same single application with
  no second mustard line anywhere — no double-counting. Full review of
  american-yellow-mustard itself is out of scope (owned by another worker).
- Readability: A. Four clearly grouped ingredients, four short steps, standard
  American recipe phrasing throughout.
- Decision: targeted fix — tighten sport-pepper count to match source (or explicitly
  frame the range as "to taste"), and label the relish quantity as an editorial
  estimate.
- Findings:
  1. Minor. Current: "4–8 pickled sport peppers (1–2 per dog)." Proposed: "8 pickled
     sport peppers (2 per dog)," or keep the range but add "(source specifies 2)."
     Rationale: source is explicit at 2 per dog; our low end undershoots it.
     Source: PBS page above. Section: Ingredients. Confidence: high (direct read).
  2. Minor. Current: "...about 1 tablespoon per dog." Proposed: "...about 1
     tablespoon per dog (estimated; source does not specify an amount)." Rationale:
     avoid implying a source-specified quantity that doesn't exist. Source: PBS page
     above. Section: Ingredients. Confidence: high (direct read).
  3. Minor/informational. Current: "keep the water below a hard boil so the casings
     do not split." This deviates from the source's plain "boil," but is a
     deliberate, defensible technique note, not an error — no change required unless
     the team wants source-literal phrasing.
- Replacement candidates: not needed; source is a solid, well-matched fit.
- Access failures or unverified claims: none. Source read directly and in full.

## deep-dish-pizza

- Recipe ID: deep-dish-pizza. Path: `recipes/nfc/north/bears/deep-dish-pizza.md`.
  Status: published. Source:
  https://www.kingarthurbaking.com/recipes/chicago-style-deep-dish-pizza-recipe
  (fetched in full, direct read, twice — second pass targeted the pan-oil amount,
  rise/rest timings, bake temps/times, and tomato-draining step specifically).
  Date checked: 2026-09-26. Input hash: `8d4ff202a808591b9a676cc6e3c8e45ae5425ad5`.
- City fit: strong. Deep-dish is the definitive Chicago pizza style; filed correctly
  under Bears/Chicago.
- Authenticity: defining traits present and correctly ordered — oiled pan (fried,
  not baked, bottom crust), mozzarella laid directly on the dough (under the
  toppings and sauce, preventing a soggy crust), sauce on top, cheese/herb finish.
  This layering order is the single most important authenticity marker for deep-dish
  and it is correct here. Classification: standard, well evidenced.
- Source fidelity: no discrepancies found. Confirmed matches: pan oil "3 to 4
  tablespoons olive oil, tilting to cover the bottom and partway up the sides" (exact
  wording echoed); ~60-minute first rise; two 15-minute rests (after initial stretch,
  and after pushing dough up the sides); 425°F preheat; 10-minute crust-only bake;
  ~25-minute final bake; tomatoes drained and salted to taste as separate explicit
  steps. This is a high-fidelity, near-verbatim transcription.
- Specificity: sausage described generically as "Italian sweet or hot," which is
  reasonable; no brand call-out needed for this ingredient. Cheese and crust
  quantities match source amounts and units. Good confidence.
- Components: none referenced; none warranted (crust, sauce, and filling are
  single-use, recipe-specific quantities, not appropriate as shared components).
- Readability: A. Ingredients grouped by role (crust/filling), five sequential
  steps, doneness cues included ("until bubbling and golden").
- Decision: keep. Positive evidence supplied above for all five checks; strong,
  verified match with no corrective action needed.
- Findings: none.
- Replacement candidates: not needed.
- Access failures or unverified claims: none. Source read directly and in full.

## italian-beef-sandwiches

- Recipe ID: italian-beef-sandwiches. Path:
  `recipes/nfc/north/bears/italian-beef-sandwiches.md`. Status: published. Source:
  https://amazingribs.com/tested-recipes/beef-and-bison-recipes/chicago-italian-beef-sandwich-recipe/.
  Date checked: 2026-09-26. Input hash: `d35cb4c3383fa38b5ff58923b62eeadac94e97b9`.
- **Access failure**: WebFetch returned HTTP 403 on two attempts (initial + retry per
  guidance that transient 403s sometimes clear). The source's full text was **not**
  read directly. Fallback: multiple targeted WebSearch queries returned specific,
  numeric snippet corroboration that is a strong indirect match — rub "1 tablespoon
  ground black pepper, 2 teaspoons garlic powder, 1 teaspoon onion powder, 1 teaspoon
  dried oregano, 1 teaspoon dried basil, 1/2 teaspoon crushed red pepper"; juice "6
  cups hot water and 4 cubes beef bouillon"; roast at 225°F to an internal 130–140°F
  for medium-rare, about 3 hours. All of these exactly match our recipe's numbers.
  However, this is snippet-level corroboration, not a verbatim page read, and the
  pepper/roll assembly section (3 green bell peppers, 2 tbsp olive oil, ~15 min
  sauté) was not independently corroborated at all — that portion remains unverified
  against the actual source.
- City fit: strong. Italian beef is a Chicago-defining sandwich; filed correctly.
- Authenticity: defining traits present — thin-sliced beef held/served in its own
  jus ("wet" option offered), giardiniera and sautéed sweet peppers as toppings, soft
  Italian roll. No competing regional variant implied. Classification: standard,
  moderately evidenced (limited by the access failure above).
- Source fidelity: rub, juice, and roast-temperature figures corroborate exactly
  with independent WebSearch results (see access-failure note); pepper-sauté and
  bread-assembly steps could not be checked against source text. No contradictions
  found in what could be checked.
- Specificity: giardiniera correctly linked to the shared component with a clear
  quick-buy note (J.P. Graziano/Ditka's/Marconi); peppers specified as green bell
  (correct, standard); rolls described generically as "soft, fluffy... or Italian
  bread loaf," reasonable without over-specifying a brand.
- Components: `{{component:chicago-oil-packed-giardiniera}}` used once, on the
  finished sandwich-assembly line ("1 cup spicy hot giardiniera... use the linked
  Chicago oil-packed giardiniera component"), correctly placed as a finished
  topping, not a raw pantry item; no double-counting.
- Readability: A. Ingredients grouped by role (beef/rub/juice/sandwiches), six clear
  sequential steps, doneness temperature given, a Kitchen Notes section correctly
  flags that the source's total time excludes the several-hour chill.
- Decision: keep, with an access-failure caveat — the specific numbers that could be
  checked all corroborate exactly, but the source could not be read directly and one
  full section (peppers/assembly) is unverified.
- Findings: none identified in the portion that could be checked; no corrective
  edits proposed given the strength of the indirect corroboration.
- Replacement candidates: not needed; recommend a future retry of the direct fetch
  rather than switching sources, since available indirect evidence supports the
  current source strongly.
- Access failures or unverified claims: amazingribs.com blocked (403 twice); full
  text not read directly; pepper-sauté/assembly section unverified against source.

## tavern-style-thin-crust-pizza

- Recipe ID: tavern-style-thin-crust-pizza. Path:
  `recipes/nfc/north/bears/tavern-style-thin-crust-pizza.md`. Status: published.
  Source: https://www.kingarthurbaking.com/videos/tavern-style-pizza (fetched in
  full, direct read). Date checked: 2026-09-26. Input hash:
  `38367f02538caf655abd6569c577dd20ac07b803`.
- City fit: strong. Tavern-style ("party-cut") thin crust is a Chicago-area staple
  distinct from deep-dish; filed correctly under Bears/Chicago.
- Authenticity: defining traits present — cracker-thin, cornmeal-textured dough,
  cut into small squares (not wedges), sauce blended smooth, cheese to the edge.
  Giardiniera as an optional topping is a known Chicago tavern-pizza variant, offered
  here via quick-option rather than forced into the base recipe. Classification:
  standard, well evidenced.
- Source fidelity: no discrepancies found. Dough (103 g water, 6 g sugar, 6 g salt,
  scant 1/4 tsp yeast, 160 g flour, 28 g cornmeal, 28 g butter), sauce (794 g
  tomatoes, 12 g sugar, 10 g vinegar, 170 g paste, 25 g oil, garlic powder, salt,
  Italian seasoning), and per-pizza topping amounts (124 g sauce, 113 g mozzarella,
  114 g sausage, 50 g giardiniera, 14 g Parmigiano, oregano, optional fennel) all
  match the source's figures. Bake at 475°F on a preheated stone/steel for 7–10
  minutes matches. The only omission is the source's alternative "Outdoor Pizza Oven
  Method" — not included in our recipe, but this is not a fidelity problem since the
  home-oven method we do include matches the source's home-oven instructions
  exactly; no defining technique was simplified away.
- Specificity: giardiniera correctly linked to the shared component with the same
  quick-buy brands as italian-beef-sandwiches; sausage specified as "sweet Italian";
  cheese specified as "low-moisture whole-milk mozzarella." Good confidence.
- Components: `{{component:chicago-oil-packed-giardiniera}}` used once, on the
  finished per-pizza topping line ("Chicago-style giardiniera, drained, patted dry,
  and chopped"), correctly on the finished item, not a raw ingredient; no
  double-counting.
- Readability: A. Ingredients grouped by dough/sauce/per-pizza, five sequential
  steps, an explicit Kitchen Notes timing summary.
- Decision: keep. Positive evidence supplied above for all five checks.
- Findings: none.
- Replacement candidates: not needed.
- Access failures or unverified claims: none. Source read directly and in full.

## detroit-coney-dogs

- Recipe ID: detroit-coney-dogs. Path: `recipes/nfc/north/lions/detroit-coney-dogs.md`.
  Status: published. Source: https://www.simplyscratch.com/detroit-style-coney-dogs/
  (fetched in full, direct read). Date checked: 2026-09-26. Input hash:
  `83134a365973525adaa246ea1969579167b3121b`. Note: this is a distinct dish from
  cheese-coneys (Cincinnati), reviewed separately in `workers/afc-north-1.md`;
  reviewed here strictly against its own Detroit-style source.
- City fit: strong. Detroit Coney dogs (National Coney Island / American Coney
  Island lineage) are Detroit-specific; filed correctly under Lions/Detroit, and the
  ingredient line explicitly calls for "National Coney Island style if available."
- Authenticity: defining traits present — natural-casing all-beef frank, loose
  beef-based Coney sauce (not a bean chili), yellow mustard and diced onion as the
  standard finish, no cheese (correctly distinguishing it from the Cincinnati
  cheese-coney variant). Classification: standard, well evidenced.
- Source fidelity: one discrepancy found. The source's Coney sauce ingredient list
  includes 1/4 cup water (used during the simmer, alongside the tomato puree); our
  recipe's ingredient list has no water at all, and step 2 does not add any water
  either — the sauce goes straight from browned beef into spices, sugar, tomato
  puree, and mustard, covered and simmered 30 minutes then uncovered 10 more to
  thicken. Omitting the water could make the sauce simmer drier/thicker than
  intended and increases scorching risk over the 40-minute total simmer. All other
  checked spice quantities (chili powder, cumin, paprika, smoked paprika, onion
  powder, garlic powder, black pepper, cayenne, sugar) match the source.
- Specificity: franks specified as natural-casing all-beef with a Detroit-brand
  callout (National Coney Island style); mustard is plain "prepared yellow mustard,"
  used twice — once cooked into the sauce, once as a table garnish — which matches
  standard Coney-dog assembly and is not a double-counting error (this recipe does
  not reference any mustard component; it's a plain ingredient listed for two
  distinct uses).
- Components: no shared component referenced. Considered per check 5 whether a
  Coney-sauce component is warranted: a repo-wide search
  (`grep -ril coney recipes components`) found only this recipe and cheese-coneys.md
  use the word "coney," and cheese-coneys is a different, Cincinnati-style sauce
  reviewed separately. With no second consumer of this specific Detroit beef-sauce
  formulation, it does not meet the brief's bar ("propose... for meaningful
  regional fidelity or repeated use; do not add components for every... staple").
  Recommendation: keep the sauce scratch-only, inline in this recipe; do not extract
  a new component at this time.
- Readability: B. Steps are clear and short, but the missing water ingredient means
  a cook following the ingredient list literally cannot match the instructions'
  described simmer consistency without guessing.
- Decision: targeted fix — add the missing 1/4 cup water.
- Findings:
  1. Minor/moderate. Current: ingredient list ends at "8 hot dog buns" with no water
     listed; step 2 has no water addition. Proposed: add "1/4 cup water" to the
     ingredient list and "...stir in the spices, sugar, tomato puree, mustard, and
     1/4 cup water" to step 2. Rationale: source's Coney sauce simmers with added
     water; omitting it risks a drier, scorch-prone sauce over the 40-minute total
     simmer. Source: simplyscratch.com page above. Section: Ingredients/Instructions
     step 2. Confidence: high (direct read).
- Replacement candidates: not needed; source is a good match apart from the one
  omission above.
- Access failures or unverified claims: none for the recipe text itself; source read
  directly and in full.

## detroit-style-pizza

- Recipe ID: detroit-style-pizza. Path:
  `recipes/nfc/north/lions/detroit-style-pizza.md`. Status: published. Source:
  https://www.kingarthurbaking.com/recipes/weeknight-detroit-pizza-recipe (fetched
  in full, direct read). Date checked: 2026-09-26. Input hash:
  `ee378e1f709797efd15d6b965ade5e3d3e117fc8`.
- City fit: strong. Detroit-style (Buddy's Pizza lineage) is Detroit-specific; filed
  correctly under Lions/Detroit.
- Authenticity: defining traits present and correctly ordered — rectangular steel
  pan, brick cheese run edge-to-edge to caramelize against the pan sides, sauce
  applied in stripes on top of the cheese after baking the crust (not underneath),
  crust freed with a spatula while the pan is still warm to preserve the crisp,
  caramelized cheese edge. This is the single most important authenticity marker for
  Detroit-style and it is correct here. Classification: standard, well evidenced.
- Source fidelity: no discrepancies found. Confirmed matches: dough hydration and
  rest schedule (two 15-minute folds, then 1–1.5 hour bulk rise), sauce (2 tbsp oil,
  4 garlic cloves, 28 oz crushed tomatoes, 17 g sugar, salt, simmered ~20 minutes to
  about 3 cups), pan oil quantity, 500°F preheat with steel/stone, 10–12 minute
  crust-only bake, cheese-border technique, ~1 1/3 cups sauce in diagonal stripes,
  12–14 minute final bake, and the pan-release/Pecorino finish. Brick cheese given
  with a clearly labeled mozzarella+cheddar substitution.
- Specificity: cheese specified as brick with a workable substitute blend; Pecorino
  Romano named for the finish (correct, standard); pepperoni marked optional
  (correct — not universal on Detroit pizza). Good confidence.
- Components: none referenced; none warranted (sauce and dough are recipe-specific
  quantities without evidence of reuse elsewhere).
- Readability: A. Ingredients grouped by dough/sauce/assembly, six sequential steps
  including a dedicated pan-release step with rationale.
- Decision: keep. Positive evidence supplied above for all five checks.
- Findings: none.
- Replacement candidates: not needed.
- Access failures or unverified claims: none. Source read directly and in full.

## component:chicago-sweet-green-relish

- Component ID: chicago-sweet-green-relish. Path:
  `components/toppings/chicago-sweet-green-relish.md`. Status: published. Source:
  the adamwitt.co Chicago-style hot dog page (Adam Witt). Date checked: 2026-09-26.
  Input hash: `607932e50da789c4181e460802973027232e4d9e`. Consumers (via
  `grep -rl '{{component:chicago-sweet-green-relish}}' recipes components`):
  `recipes/nfc/north/bears/chicago-style-hot-dogs.md` (sole consumer).
- **Access failure**: WebFetch on the adamwitt.co source URL was denied outright by
  the tool's own auto-mode classifier (a tool-level policy denial, not a network
  403); per the denial's own instructions, no attempt was made to reach the same
  page through another tool, encoding, or host. Fallback: multiple WebSearch queries
  returned consistent paraphrased snippets of the page's actual content — page
  titled "Chicago-style Hot Dog (Homemade) — Adam Witt"; relish method built from a
  mustard-seed/celery-salt/turmeric/sugar/vinegar/water dressing over
  food-processor-chopped vegetables, an overnight salt-drain step, a ~10-minute
  boil, and optional green food coloring. This corroborates the component's method
  at a paraphrase level only — no verbatim page text was read, and exact
  vinegar/sugar/vegetable quantities were not independently confirmed.
- Authenticity/fidelity vs. source (as corroborated): method matches — overnight
  drain, mustard-seed/turmeric/celery-salt dressing, and optional green coloring for
  the traditional neon look are all present in our component. Consistent with the
  prior review's lead ("Witt recipe matches; identify measured salt as editorial
  estimate; retain overnight drain").
- Specificity: quick_buy correctly names Vienna Beef Chicago Style Relish, the
  market-standard bottled product; good confidence.
- Readability: B. Instructions are clear and complete, but confidence in exact
  quantities is capped by the access failure above (paraphrase-level corroboration
  only).
- Decision: targeted fix — in the salt/brine step, label the measured salt amount
  as an editorial estimate rather than a value taken verbatim from source (per the
  prior review's lead), and keep the overnight drain step as-is.
- Findings:
  1. Minor. Current: measured salt quantity presented as a plain instruction step.
     Proposed: add a brief note that the amount is an estimate calibrated for
     texture/drainage, not a literal source figure. Rationale: the source's exact
     salt amount could not be independently confirmed (access failure above), so it
     should not read as a verbatim source value. Source: adamwitt.co page (title
     confirmed via WebSearch only). Section: component method. Confidence: medium
     (based on paraphrase-level corroboration, not a direct read).
- Replacement candidates: not needed; recommend a future retry of the direct fetch
  (the denial was a tool-level classifier decision, which may not recur).
- Access failures or unverified claims: adamwitt.co blocked by the WebFetch tool's
  auto-mode classifier; full text not read directly; only WebSearch paraphrase-level
  corroboration obtained. Exact vinegar/sugar/vegetable quantities remain
  unverified against the source.

## component:chicago-oil-packed-giardiniera

- Component ID: chicago-oil-packed-giardiniera. Path:
  `components/toppings/chicago-oil-packed-giardiniera.md`. Status: published.
  Source: https://www.chilipeppermadness.com/recipes/giardiniera/. Date checked:
  2026-09-26. Input hash: `15de0335af8bfa6aef4ace7674e268d757eb3ee6`. Consumers (via
  `grep -rl '{{component:chicago-oil-packed-giardiniera}}' recipes components`):
  `recipes/nfc/north/bears/italian-beef-sandwiches.md` and
  `recipes/nfc/north/bears/tavern-style-thin-crust-pizza.md`.
- **Access failure**: WebFetch returned HTTP 403 on two attempts (initial + retry).
  Source's full text was **not** read directly. Fallback: WebSearch returned
  snippets suggesting the same site publishes at least two distinct giardiniera
  recipes — a general "Italian Giardiniera" (dried basil, different pepper counts)
  and a separately mentioned "Chicago-Style" version using "5 jalapeno peppers and 5
  sport peppers or serrano peppers," described as having "comparable brine and
  finishing processes." This partially corroborates our component's pepper approach
  but does not confirm the exact oil/vinegar/oregano/celery-seed/olive-oil
  quantities in our component, and it's not certain the search surfaced the exact
  same page our component cites (the URL path matches, but the snippet content
  could not be matched word-for-word).
- Authenticity/fidelity vs. source (as corroborated): partially supported — the
  oil-packed, hot-and-sweet-pepper Chicago format is directionally consistent with
  the snippet evidence, consistent with the prior review's lead ("Oil/vinegar
  Chicago home formula supported; spell out 12-hour brine plus two-day
  maturation").
- Specificity: quick_buy correctly names J.P. Graziano, Ditka's, and Marconi — all
  genuine, recognizable Chicago giardiniera brands; good confidence independent of
  the source-text access failure.
- Readability: B. Method is clear (brine, pack, rest), but exact source quantities
  remain unconfirmed, and the brine/maturation timing called out in the prior
  review is not yet spelled out explicitly in the component text.
- Decision: targeted fix — per the prior review's lead, spell out the 12-hour brine
  and two-day maturation period explicitly in the instructions (currently implicit
  or under-specified), since this materially affects usability (a cook needs to
  know to start this 2+ days ahead of game day).
- Findings:
  1. Minor. Current: brine/rest timing not spelled out as a discrete, explicit
     duration in the component's method. Proposed: state "brine 12 hours, then let
     mature at least 2 days before use" explicitly in the instructions. Rationale:
     matches the prior review's lead and gives cooks an accurate planning
     timeline; without it, a reader could underestimate lead time needed before
     game day. Source: chilipeppermadness.com (not independently re-confirmed this
     round due to 403; carried from prior lead). Section: component method.
     Confidence: medium (based on prior lead plus partial WebSearch corroboration,
     not a fresh direct read).
- Replacement candidates: not needed; recommend a future retry of the direct fetch.
- Access failures or unverified claims: chilipeppermadness.com blocked (403 twice);
  full text not read directly this round; WebSearch corroboration is
  directionally supportive but not a confirmed word-for-word match, and it's
  possible the snippets describe a different recipe on the same site than the one
  cited.
