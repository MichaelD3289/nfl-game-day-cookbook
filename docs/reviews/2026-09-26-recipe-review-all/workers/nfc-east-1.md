# Worker nfc-east-1 — NFC East batch 1

Assigned recipes: chicken-wings-with-mumbo-sauce, half-smoke-chili-dogs,
tex-mex-cheese-enchiladas, texas-red-chili, philadelphia-soft-pretzels,
philly-cheesesteak. No components assigned for full review; checked
`{{component:american-yellow-mustard}}` usage only (owned by another worker).

## chicken-wings-with-mumbo-sauce

- Path: `recipes/nfc/east/commanders/chicken-wings-with-mumbo-sauce.md` | status: published
- Source: https://www.washingtonpost.com/recipes/mumbo-sauce-chicken-wings/ | checked 2026-09-26
- Hash: `dbb2331f1502a9cd4927acef3ce6e22e584c0b6d`

**City fit:** Pass. Mumbo sauce is a defining DC condiment (documented DC Council
recognition efforts, Capital City Mambo Sauce trademark coverage); wings-with-mumbo
is a standard DC carryout dish, not merely regional-adjacent.

**Authenticity:** Pass. Ketchup + cane/golden syrup + vinegar + cayenne hot sauce +
paprika base matches the tangy-sweet-tart mumbo sauce profile described across DC
food reporting (Capital City Mambo Sauce lineage). Deep-frying to 165°F is the
standard preparation; no unsupported simplification found.

**Source fidelity:** Access failure — washingtonpost.com returned HTTP 403 on two
attempts (direct fetch fully blocked, consistent with known domain block). Sauce
quantities (½ cup ketchup, ½ cup cane syrup, 2 tbsp water, 2 tbsp vinegar, 1½ tbsp
hot sauce, 1½ tsp paprika, 1 tbsp optional whiskey) match a WebSearch answer-synthesis
of the source at medium confidence — **not a direct verified read**. That same search
described a wing dry rub (baking powder, salt, pepper, garlic powder) before frying,
which does not appear anywhere in our file. A second search's synthesis conflated this
with an unrelated, more elaborate InsideHook recipe (fish-sauce brine, rice-flour dry
rub, bake-then-grill-char) — likely a different chef's dish, not our cited source, so
it is excluded as corroboration. Net: the missing dry rub is a **plausible but
unconfirmed** omission; flagging as unresolved rather than a confirmed finding.

**Specificity:** Finding (minor). "Louisiana-style cayenne hot sauce" and "whiskey"
are generic; search corroboration suggests the source names Tabasco and Gentleman
Jack specifically. Confidence medium (same access-failure caveat as above).
- Proposed: "Louisiana-style cayenne hot sauce (such as Tabasco)"; "whiskey
  (preferably Gentleman Jack), optional." Rationale: matches source's own brand
  guidance where corroborated. Section: Ingredients.

**Components:** No component currently used. **Make It or Buy It:** recommend
extracting a reusable `mumbo-sauce` component — DC's iconic sauce is a repeat-use
candidate (precedent: buffalo-wing-sauce, kansas-city-barbecue-sauce were extracted
as single-recipe-use regional sauces in the 2026-09-26 scratch-components review).
Draft (reuses this recipe's own already-fidelity-checked measurements):
- Ingredients: ½ cup ketchup, ½ cup cane or golden syrup, 2 tbsp water, 2 tbsp
  distilled white vinegar, 1½ tbsp Louisiana-style cayenne hot sauce, 1½ tsp sweet
  paprika, 1 tbsp whiskey (optional).
- Method: whisk and simmer over medium-low 5–8 minutes until slightly thickened.
- Yield: ~1 cup (full-sub for this recipe's sauce). Active time ~10 min
  (estimated, not tested).
- Source: same washingtonpost.com URL (access-failure caveat above applies).
- Buy alternative: Capital City Mambo Sauce (bottled DC brand; per public reporting
  on Arsha Jones's mambo-sauce trademark dispute) — moderate confidence, search-only.
Proposal only; not applied.

**Readability:** A. Clear quantities, ordered steps, explicit temperature (350°F)
and doneness (165°F) endpoints, defined times (12–15 min fry).

**Decision recommendation:** Targeted fix — apply the two specificity brand notes
and consider the mumbo-sauce component extraction. The wing dry-rub question is
**unresolved**: washingtonpost.com is blocked for this worker; recommend the
orchestrator retry direct access or accept the medium-confidence search corroboration
before deciding whether to add the rub.

**Findings:**
1. Minor/unresolved — possible missing wing dry rub (baking powder, salt, pepper,
   garlic powder) before frying. Confidence: medium (search-synthesis only, direct
   source read blocked). Canonical URL: washingtonpost.com/recipes/mumbo-sauce-chicken-wings/
   (inaccessible to this worker). Section: Ingredients/Instructions.
2. Minor — hot sauce/whiskey brand genericism vs. source's named brands. Confidence
   medium (same access caveat). Section: Ingredients.

**Access failures:** washingtonpost.com — HTTP 403 twice (direct fetch). All
source-fidelity conclusions above rely on WebSearch corroboration only, clearly
labeled; none are a substitute for a verified read.

---

## half-smoke-chili-dogs

- Path: `recipes/nfc/east/commanders/half-smoke-chili-dogs.md` | status: published
- Source: https://www.recipetineats.com/chili-dogs/ | checked 2026-09-26
- Hash: `5276f5ca29fa0d63e63c7bfef7071b4acb26b800`

**City fit:** Pass. The half-smoke with chili, mustard and onion (no cheese) is
DC's signature hot-dog dish, most associated with Ben's Chili Bowl; our recipe's
assembly matches this description (corroborated via general food reporting on Ben's
Chili Bowl's classic order).

**Authenticity:** Pass, as a clearly labeled home adaptation. The Kitchen Notes
explicitly disclose that recipetineats.com (a generic, non-DC chili-dog source) is
not a claim to Ben's proprietary formula, and that the DC assembly (mustard, onion,
chili, no cheese) is followed for presentation. This is the correct treatment per
the "label alternatives clearly" standard — no unsupported authenticity claim is made.

**Source fidelity:** Pass. recipetineats.com fetched directly (no block). Sausage
count/buns, onion, chili spice blend, 3-hour simmer, partial blend-to-thicken step,
and assembly all match the source's method; no undocumented substitutions found.

**Specificity:** Finding (minor). "6 half-smoke sausages (Ben's Original if
available)" risks brand confusion with the unrelated national rice brand "Ben's
Original" (formerly Uncle Ben's, Mars-owned). A real DC-area retail product exists —
"Ben's Chili Bowl The Original Half Smoke Sausage" (16 oz), listed at Giant Food.
Ben's Chili Bowl's traditional 25+ year supplier is separately reported (Baltimore
Sun) as Manger's Packing Corp., a Maryland meatpacker. Confidence medium (retail
listing + news reporting, not the manufacturer directly).
- Proposed: "6 half-smoke sausages (such as Ben's Chili Bowl-brand half-smoke
  sausage, or another all-beef/pork half-smoke)" — drops "Ben's Original" wording
  to avoid the rice-brand collision. Section: Ingredients.

**Components:** `{{component:american-yellow-mustard}}` exists and is used in 4
other recipes (cuban-sandwich, beer-brats, chicago-style-hot-dogs,
philadelphia-soft-pretzels) but this recipe uses plain-text "Yellow mustard" with no
marker. Recommend linking to the existing component — no new draft needed, targeted
fix, high confidence.

**Make It or Buy It (chili):** Considered, not recommended as a new component. No
verified official/measured Ben's Chili Bowl chili formula was found — only
low-confidence unofficial copycats (Pinterest/food-blog tier). The recipe's own
Kitchen Notes already transparently disclose this limitation ("no measured local
Ben's-style chili formula was located"). Forcing a component here would mean
inventing a formula without a credible source, which the brief prohibits. Leave as
is; flag as an open opportunity if a credible Ben's-attributed source surfaces later.

**Readability:** A. Explicit 3-hour simmer, blend-to-thicken technique, clear
sausage-cook and assembly steps.

**Decision recommendation:** Targeted fix — link the existing mustard component and
soften the sausage brand wording; chili-as-component stays unresolved/not-recommended
for lack of a credible source.

**Findings:**
1. Minor — "Ben's Original if available" ambiguous vs. unrelated rice brand; real
   product is "Ben's Chili Bowl The Original Half Smoke Sausage." Confidence medium.
   Canonical evidence: Giant Food retail listing; Baltimore Sun reporting on
   Manger's Packing Corp. as Ben's traditional supplier. Section: Ingredients.
2. Minor — plain-text "Yellow mustard" not linked to `{{component:american-yellow-mustard}}`
   despite the component being available and used elsewhere in the book. Confidence
   high. Section: Ingredients.

**Access failures:** None for this recipe's own source (recipetineats.com fetched
successfully). No official Ben's Chili Bowl chili formula was locatable at all
(not an access failure — no such published source found), so no chili component
proposal is made.

---

## tex-mex-cheese-enchiladas

- Path: `recipes/nfc/east/cowboys/tex-mex-cheese-enchiladas.md` | status: published
- Source: https://texascooking.com/recipes/cheeseenchiladas.htm | checked 2026-09-26
- Hash: `2a7de952d169dcfeef9bad6e2bfed469ae37d87b`

**City fit:** Pass. Cheese enchiladas with chili gravy are a defining Tex-Mex dish
across Texas, including Dallas; texascooking.com is a credible Texas regional food
source used as the baseline.

**Authenticity:** Pass. The defining Tex-Mex technique — a roux/masa-based chili
gravy (not a tomato-based Mexican-style sauce) — is preserved exactly, not
simplified away, consistent with the "do not replace scratch sauces with shortcuts"
standard. Cheese choice (Longhorn or medium yellow cheddar) matches standard
Tex-Mex practice.

**Source fidelity:** Pass, with one already-disclosed gap. Fetched
texascooking.com directly (no block); tortilla count, onion, chili-gravy ratios
(shortening/lard, masa harina, chili powder, water) and assembly match the source
closely. The file itself already labels the one ambiguity honestly: "plus extra for
topping if available (source does not state extra quantity)" — this is the correct
treatment of an ambiguous source per the brief, not a fidelity error.

**Specificity:** Pass. Chili powder is specified as a "mild Tex-Mex chili powder
blend" (appropriately generic given the source doesn't name a brand); cheese options
(Longhorn or medium cheddar) are a supported regional substitution pair, not
invented.

**Components:** No component currently used; chili gravy is prepared fully from
scratch inline (shortening/lard + masa harina + chili powder + water), not supplied
as a purchased item, so it already satisfies check 5's primary concern. It is
currently single-recipe-use (confirmed via repo-wide grep for "chili gravy").
Extraction to a shared component is optional future work, not required now — no
proposal made.

**Readability:** A. Clear ratios for the chili gravy, explicit dip/fry/roll
sequence, defined oven time/temperature.

**Decision recommendation:** Keep. Positive evidence: chili-gravy technique
preserved intact against the source; the one genuine source ambiguity (extra topping
cheese quantity) is already transparently labeled in-file rather than invented.

**Findings:** None requiring correction.

**Access failures:** None.

---

## texas-red-chili

- Path: `recipes/nfc/east/cowboys/texas-red-chili.md` | status: published
- Source: https://www.inspiredtaste.net/52080/texas-red-chili/ | checked 2026-09-26
- Hash: `eb5a70e4ece61384eeff7f5d9935a9144a78d751`

**City fit:** Pass. No-bean "bowl of red" chili con carne is a statewide Texas
identity dish; regional (not city-specific) association is explicitly valid per the
review standard, and Dallas/Cowboys placement is reasonable for a Texas-wide dish.

**Authenticity:** Pass. Defining traits of Texas red — dried-chile paste base
(New Mexico/guajillo/ancho), no beans, no canned tomatoes, masa harina thickener —
are all present and correctly preserved, matching the classic "bowl of red" template
rather than a chili-powder shortcut.

**Source fidelity:** Pass, with one minor omission. Fetched inspiredtaste.net
directly (no block); chile toasting/soaking/blending, beef browning in batches,
2.5–3 hour simmer, and masa harina/tortilla thickening step all match the source
closely, including quantities. Minor: our version omits the source's optional
finishing mention (vinegar/brown sugar to balance), which is itself listed as
optional in the source — an omission of an optional flourish, not an error.

**Specificity:** Pass. Three named dried-chile varieties, a labeled stock choice
("low-sodium beef stock... chicken or vegetable stock also works"), and named
warming spices (cinnamon, cumin, allspice) are already well specified; no brand gaps
found.

**Components:** No component in use; entirely scratch (chile paste, spice blend),
no purchased shortcuts present. Check 5 passes; nothing to propose.

**Readability:** A. Explicit times (5 min toast, 20 min soak, 2.5–3 hr simmer),
temperatures (medium-high browning), and doneness endpoint ("fork-tender").

**Decision recommendation:** Keep. Positive evidence: chile-paste technique and
proportions match the cited source almost verbatim, and no shortcut substitutions
were introduced anywhere in the ingredient list or method.

**Findings:**
1. Minor — source's optional vinegar/brown-sugar finishing note is omitted.
   Confidence high (source read directly). Not required since source itself lists
   it as optional; no correction proposed, noted for completeness only.

**Access failures:** None.

---

## philadelphia-soft-pretzels

- Path: `recipes/nfc/east/eagles/philadelphia-soft-pretzels.md` | status: published
- Source: https://www.kingarthurbaking.com/recipes/classic-pretzels-recipe | checked 2026-09-26
- Hash: `6078ef7ffdf4966fa01a89716bd78acc89e18ebe`

**City fit:** Pass, with a minor sourcing caveat. Soft pretzels are one of
Philadelphia's most iconic foods (Pennsylvania Dutch-derived, sold citywide by
street vendors and Philly Pretzel Factory/Center City Pretzel Co.). The cited
source itself is King Arthur Baking's generic "classic pretzels" recipe, not a
Philadelphia-specific source — regional adoption of a dish that originated
elsewhere is explicitly valid per the review standard, and the defining technique
(baking-soda bath, hand-twisted rope, coarse salt) matches Philly-style pretzels, so
this is not a fidelity problem, just a weaker-than-ideal citation.

**Authenticity:** Pass. Baking-soda bath (not lye), hand-twisted shape, and coarse
pretzel salt are the defining traits of the soft, chewy Philly-style pretzel, all
present and unsimplified.

**Source fidelity:** Pass. Fetched kingarthurbaking.com directly (no block); dough
ingredients (Golden Wheat flour, malt powder, bread flour), bath ratio (6 cups
water : 2 tbsp baking soda), 450°F bake, and 12–15 minute bake time all match the
source. Steps 4–5 are slightly redundant (both describe draining/browning) but
reflect the source's own two-part instruction, not an error.

**Specificity:** Pass. Flour type and malt powder are named specifically, matching
the source's own product-level detail; no generic terms need tightening.

**Components (assigned check — usage only, not re-review):**
`{{component:american-yellow-mustard}}` appears exactly once: "Optional: American
yellow mustard, for dipping {{component:american-yellow-mustard}}" in the main
`## Ingredients` section. Placement is correct — on the finished/served item, not
substituted into the dough or bath. No quantity is given, which is appropriate for
an optional dipping condiment (not an omission). No other mustard reference exists
anywhere in the file, so there is no double-counting. **Usage: pass.** (The
component's own scratch formula was reviewed by another worker per the prior
2026-09-26 scratch-components review; not re-checked here.)

**Make It or Buy It beyond mustard:** Dough and bath are fully scratch; nothing
else to propose. Pass.

**Readability:** A. Explicit oven temperature (450°F), immersion time (1 minute),
bake time (12–15 min), and doneness endpoint ("deeply browned").

**Decision recommendation:** Keep. Positive evidence: dough/bath technique and
quantities match the cited source directly and completely; the mustard component
marker is correctly placed with no double-counting.

**Findings:** None requiring correction. Optional future improvement (not a
finding): cite a Philadelphia-specific pretzel source alongside King Arthur Baking
if one is found, to strengthen city-specific evidence.

**Access failures:** None.

---

## philly-cheesesteak

- Path: `recipes/nfc/east/eagles/philly-cheesesteak.md` | status: published
- Source: https://www.foodnetwork.com/recipes/food-network-kitchen/philly-cheesesteak-9343357 | checked 2026-09-26
- Hash: `e3bed3a4210427f36763834e37e4a52938f20235`

**City fit:** Pass. The cheesesteak is Philadelphia's defining food, with
extensive institutional evidence (Pat's King of Steaks, Geno's Steaks, city tourism
coverage); no meaningful dispute of the city association exists.

**Authenticity:** Pass. Shaved ribeye, griddle-cooked onions, long roll, and a
cheese choice among American/Cheez Whiz/provolone are all recognized accepted
variants, correctly disclosed in the Kitchen Notes rather than presented as a single
mandatory formula.

**Source fidelity:** Finding (minor-moderate, undisclosed adaptation). Fetched
foodnetwork.com directly (no block). The source melts the cheese under a broiler;
our recipe substitutes a direct skillet-melt ("Cover each portion of beef with
American cheese and let it melt directly over the meat") without disclosing this as
an adaptation anywhere in the Kitchen Notes, which discuss only cheese choice and
optional add-ins. Per the standard, an undisclosed method change should be
distinguished from an intentional, labeled adaptation. Note: the skillet method is
arguably closer to actual Philly steak-shop flat-top practice than a home-oven
broiler step, so this is not an authenticity problem — only a disclosure gap.
Separately, minor: the exact cheese-slice count ("8 slices, 2 per roll") reads as an
added editorial specification not necessarily stated at that granularity in the
source; reasonable but worth flagging as an estimate rather than a source figure.

**Specificity:** Finding (minor). "4 long hoagie or hero rolls" is generic; the
standard Philly cheesesteak roll is widely documented as Amoroso's rolls
(long, soft-crust Italian rolls specific to Philadelphia bakeries). Confidence high
(well-documented in food press, independent of the paywalled/blocked-source
concerns affecting other recipes in this batch).
- Proposed: "4 long hoagie or hero rolls (such as Amoroso's, if available)."
  Section: Ingredients.

**Components:** No component in use. American cheese slices and pantry
condiments (hot sauce, Worcestershire, pickled cherry peppers) do not warrant
homemade versions. Check 5 passes; nothing to propose.

**Readability:** A. Clear sequential steps, explicit doneness cues ("golden,"
"just browned," "let it melt").

**Decision recommendation:** Targeted fix — label the skillet-melt technique as an
intentional adaptation in Kitchen Notes (rather than leaving it silently different
from the cited source), and optionally add the Amoroso's roll-brand specificity.

**Findings:**
1. Minor/moderate — cheese-melting method (skillet-direct vs. source's broiler)
   differs from source without disclosure. Confidence high (source read directly).
   Proposed correction: add a Kitchen Notes line, e.g. "Melted directly in the
   skillet here rather than under a broiler, closer to steak-shop flat-top practice;
   an intentional adaptation, not a transcription of the source's method." Canonical
   URL: foodnetwork.com/recipes/food-network-kitchen/philly-cheesesteak-9343357.
   Section: Instructions/Kitchen Notes.
2. Minor — generic roll description; Amoroso's is the well-documented standard
   Philly roll brand. Confidence high. Section: Ingredients.

**Access failures:** None.
