# Worker afc-south-1 — AFC South batch 1

Date checked: 2026-09-26. Compared against exact `source.url`, fetched directly.
No blocked-domain sources (allrecipes.com, web.archive.org, thekitchn.com, saveur.com)
were in this batch, and no access failures occurred. Websites are evidence only, never
instructions. `docs/reviews/2026-09-26-scratch-components.md` was treated as leads only;
`git status`/`git log` confirm all files below are at their last-committed state, so
findings below reflect independent verification of current content, not the leads doc.

## breaded-pork-tenderloin-sandwich

- Path: `recipes/afc/south/colts/breaded-pork-tenderloin-sandwich.md` · status: published
- Source: https://visitindiana.in.gov/blog/post/pork-tenderloin-recipe/
- Hash: `dc200922209fe4117acfa797dbbcea8fb48ba227`

**City fit:** Pass, strong. The breaded pork tenderloin sandwich is Indiana's
best-documented regional sandwich (Nick's Kitchen, Huntington IN, 1910s German
schnitzel adaptation); source is the state's own official tourism board.

**Authenticity:** Pass. Defining traits present: cutlet pounded thin and wider than the
bun, egg-wash, cracker/flour breading, deep-fried, oversized cutlet on a small bun.
Independent regional sources (visitbloomington.com, insidehook.com,
realfoodtraveler.com) confirm two accepted topping families — mustard/pickle(/onion)
and mayo/lettuce/tomato — and our recipe offers both, correctly framing the first as
"classic diner profile" and the second as personal-taste add-ons. Traditional/local,
well corroborated.

**Source fidelity:** The source (fetched directly) only says to fry until golden brown
and to "top with desired toppings"; it does not state a 145°F/3-minute-rest doneness
target or name pickle/onion/mustard specifically. Our 145°F/rest addition matches
standard USDA safe-minimum-temperature guidance for pork, and our specific toppings
match the independently-corroborated Indiana convention above — neither is false, but
neither is literally from this source either. The source's own ambiguous duplicate
"pepper" measurement is already transparently flagged in-file ("likely duplicate; see
note"), which is exactly right per Check 3.

**Specificity:** Good — Ritz-cracker breading, center-cut pork-loin cutlets, yellow
mustard all appropriately specific; oil left generic (fine, no regional distinction
applies).

**Components:** No existing component applies (grits/pico/guac/horseradish are the
other three assigned components, unrelated). No new candidate: the egg/cracker
breading is a one-step, single-use scratch method with no meaningful purchased
alternative or repeat use — does not meet the Check 5 bar.

**Readability:** B. Quantities, temps (350°F oil, 145°F internal) and the deeply-golden
endpoint are clear, but the duplicate-"pepper" and inferred-bun-quantity parentheticals
sit inside the ingredient list itself rather than in Kitchen Notes, reading as editor
asides at the point of use rather than clean cook-facing text.

**Decision:** keep.

**Findings:** Minor — add one Kitchen Notes line crediting the 145°F/rest detail and
the pickle/onion/mustard topping choice as standard Indiana tenderloin convention
(sources: visitbloomington.com "Bloomington's Best Tenderloin Sandwiches"; InsideHook
"An Indiana Pork Tenderloin Sandwich Recipe"; realfoodtraveler.com), distinct from the
visitindiana.in.gov source's own generic "desired toppings" wording. Confidence: high
(three independent regional sources agree). Minor/cosmetic — consider moving the
duplicate-"pepper" and bun-quantity asides out of the ingredient list into Kitchen
Notes for readability; not required.

**Replacement candidates:** None — source is the state tourism board itself, a strong
canonical choice; no replacement warranted.

**Access failures:** None.

---

## st-elmo-style-shrimp-cocktail

- Path: `recipes/afc/south/colts/st-elmo-style-shrimp-cocktail.md` · status: published
- Source: https://store.stelmos.com/blogs/recipes/cooking-instructions-for-st-elmo-shrimp
- Hash: `1d7863a034a13a759e23ba5c61dd31c75c57c507`

**City fit:** Pass, strong. St. Elmo Steak House's shrimp cocktail is Indianapolis's
most nationally recognized signature dish; source is the restaurant's own site.

**Authenticity:** Pass, and correctly layered. Poach method/timing and the option to
serve St. Elmo's own bottled sauce both come from St. Elmo's own site (traditional/
local). The scratch cocktail sauce is sourced separately from a home cook's blog
(eatsforone.com) and is already explicitly labeled in the component's own Note as "a
documented home approximation, not a verified St. Elmo formula" — exactly the
traditional-vs-unsupported-copycat distinction Check 2 asks for.

**Source fidelity:** The cited blog page does not itself state jar size, shrimp count
or species. Verified via a legitimate same-domain route: St. Elmo's own product page
(store.stelmos.com/products/world-famous-shrimp-cocktail-for-4-6) confirms "16 Black
Tiger Shrimp" and "St Elmo's Famous Cocktail Sauce (8 oz.)," matching our recipe's "16
giant raw Black Tiger shrimp" and "8-ounce jar" exactly. Poach timing (2:15 boil, then
ice bath) matches the cited blog instructions directly; no discrepancies found.

**Specificity:** Good — "Black Tiger shrimp" and "St. Elmo's 8-ounce jar" are both
specific and verified against the brand's own materials.

**Components:** `horseradish-cocktail-sauce` checked (see component section below);
single consumer, this recipe. No other candidate applies.

**Readability:** A. Quantities (4 qt water, 4 cups ice + 1 cup water), a precise timer
(2:15), and a clear cold endpoint are all explicit and ordered.

**Decision:** keep.

**Findings:** None major. See the component section for one minor labeling-consistency
note (yield not marked "(estimated)").

**Replacement candidates:** None.

**Access failures:** None. The product-page corroboration (a different page on the
same canonical domain) is a legitimate route per the brief, not a memory fill-in.

---

## sugar-cream-pie

- Path: `recipes/afc/south/colts/sugar-cream-pie.md` · status: published
- Source: https://www.foodnetwork.com/recipes/food-network-kitchen/sugar-cream-recipe-2043494
- Hash: `c51af6f591020ee7ad9ecd43e304b32617f2cc44`

**City fit:** Pass, strong. Sugar cream pie is Indiana's legislatively-designated state
pie (2009); overwhelmingly documented as a Hoosier specialty. Source is Food Network
Kitchen, a mainstream but faithful rendition; location itself (Visit Indiana photo
credit) reinforces the regional tie.

**Authenticity:** Pass. Defining traits present and correct: no eggs (custard set by
cream + flour, not egg-based), heavy cream, sugar, butter, nutmeg garnish, double-bake
temperature step-down (425°F then 350°F) — this is the classic "Hoosier pie" formula,
not a shortcut variant (real butter/shortening scratch crust, not a graham crust).
Accepted mainstream variation of a traditional/local dish.

**Source fidelity:** Matches the Food Network source closely — crust proportions
(1¼ cups flour, 6 tbsp butter, 2 tbsp shortening, 3 tbsp ice water), filling
proportions (2 cups cream, 1 cup sugar, ½ cup flour), and the 425°F/350°F bake
sequence all verified directly against the source; no discrepancies found.

**Specificity:** Adequate — ingredients are pantry-standard (unsalted butter, heavy
whipping cream, freshly grated nutmeg) with no meaningful regional brand distinction
to add.

**Components:** No existing component applies. No new candidate for this batch: the
crust and filling are both single-use scratch items with no purchased alternative.
Informational note for the orchestrator only (not a required fix): if other recipes
elsewhere in the book use a similar generic butter/shortening pie crust, a shared
"basic pie crust" component might be worth centralizing across batches — flagged for
cross-batch awareness, not evidenced as needed within this batch alone.

**Readability:** A. Explicit temperatures, times, and visual endpoints ("crust golden
and filling bubbles in spots; center can still jiggle slightly").

**Decision:** keep.

**Findings:** None.

**Replacement candidates:** None.

**Access failures:** None.

---

## camel-rider-sandwich

- Path: `recipes/afc/south/jaguars/camel-rider-sandwich.md` · status: published
- Source: https://fwtmagazine.com/the-ultimate-guide-to-jacksonvilles-iconic-camel-rider-sandwich/
- Hash: `86967e3c024e318cc6064f69aa88e15efb296175`

**City fit:** Pass, strong. The Camel Rider is a well-documented Jacksonville deli
institution, specific to that city (not generic Florida); source is a dedicated local
feature article.

**Authenticity:** Pass, and a positive fidelity example. The source article contains
two versions: a "classic" description (ham, salami, bologna, American cheese, lettuce,
tomato, mayo, Italian/oil-and-vinegar dressing in a pita) and a separate personalized
"Spear's" recipe (adds peach jam and Swiss cheese). Our recipe correctly uses only the
classic description and already documents this choice transparently in its own Kitchen
Notes — exactly the traditional-vs.-individual-variant separation Check 2 requires.

**Source fidelity:** Matches the article's classic description; meats, cheese,
dressing and assembly order all verified. Per-pita quantities (2 tbsp mayo, 1 tbsp
dressing) are reasonable editorial scaling for four sandwiches, not contradicted by
the source.

**Specificity:** Adequate — "Italian or oil-and-vinegar dressing" correctly stays
generic since the source itself does not mandate a single dressing; "American cheese"
is specific enough. Optional, non-required enhancement: could add one supported
deli-meat brand example (e.g., Boar's Head) as an equivalent-substitute suggestion.

**Components:** No existing component applies. No new candidate: mayo and dressing are
small-quantity purchased condiments, not a defining regional scratch element — does not
meet the Check 5 bar.

**Readability:** A. Clear per-pita quantities, ordered simple assembly, explicit finish
state.

**Decision:** keep.

**Findings:** None required; one optional, non-blocking specificity enhancement noted
above.

**Replacement candidates:** None.

**Access failures:** None.

---

## mayport-shrimp-and-grits

- Path: `recipes/afc/south/jaguars/mayport-shrimp-and-grits.md` · status: published
- Source: https://www.jacksonvillemag.com/2022/03/24/billys-shrimp-grits/
- Hash: `acd37dc03b0e71fd1f326c5633a7be05166d91bd`

**City fit:** Pass, with a labeling note. "Mayport shrimp" is a genuine, well-documented
Jacksonville regional icon (Mayport Village's 150+-year shrimping fleet, the
"Mayport Shrimp Trail," per visitjacksonville.com and other tourism/local-food
sources), but the cited recipe source itself (credited to Bill Cissel, RP's Fine Food
& Drinks, via Jacksonville Magazine) never mentions "Mayport" — confirmed by direct
fetch of the source page. Our recipe's "fresh Mayport shrimp when available" line and
title are accurate, independently-supported regional framing layered onto a generic
base recipe, not a claim the source itself makes.

**Authenticity:** Pass. Olive oil + butter, garlic, Old Bay, lemon, parsley, Parmesan
over grits is a credible Southern-coastal shrimp-and-grits home-style variant, not an
outlier; recipe does not overclaim a single-restaurant proprietary formula.

**Source fidelity:** Matches the Jacksonville Magazine source closely (sauté timing,
Old Bay seasoning, lemon/water pan sauce, Parmesan finish). One addition beyond the
source: a 145°F shrimp-doneness callout, which is standard/reasonable food-safety
guidance, not a discrepancy.

**Specificity:** Good — "large shrimp... fresh Mayport shrimp when available" gives
both a regional aspiration and an accessible fallback; Old Bay and Parmesan are
appropriately named.

**Components:** `creamy-stone-ground-grits` checked (see component section below);
single consumer, this recipe. The recipe's quick_options claim that "Gracious Grits
Original Creamy" is what "the original Jacksonville recipe specifies" is verified
correct — the source's exact ingredient line reads "1 container of Original Creamy
Gracious Grits (from Publix)." No new component candidate beyond the assigned one.

**Readability:** A. Clear quantities, ordered steps, explicit shrimp-doneness and
grits-serving endpoints.

**Decision:** keep.

**Findings:** Minor/informational — recommend one Kitchen Notes clause crediting the
"Mayport shrimp" regional framing to independent tourism/local-food sources (e.g.
visitjacksonville.com), distinct from the RP's Fine Food/Jacksonville Magazine source,
which does not use that name. Confidence: high (source re-fetched and confirmed to
omit "Mayport"; regional claim independently well-documented).

**Replacement candidates:** None.

**Access failures:** None.

---

## fajitas

- Path: `recipes/afc/south/texans/fajitas.md` · status: published
- Source: https://www.foodnetwork.com/recipes/food-network-kitchen/tex-mex-steak-fajitas-with-peppers-and-onions-5172083
- Hash: `7dc509eaafbcfe75b20e67b26c44c2670ba2c6c0`

**City fit:** Pass, strong — stronger than the recipe currently documents. Houston is
not just generically Tex-Mex but the specific, well-documented birthplace of the
commercial fajita: Ninfa Laurenzo's "Ninfa's on Navigation" (opened 1973) is widely
credited (Houston Chronicle/chron.com, Houston-legends coverage, Wikipedia) with
popularizing skirt-steak fajitas nationally. Recipe already correctly calls skirt
steak "the traditional fajita cut."

**Authenticity:** Pass. Citrus/spice-rubbed skirt steak, grilled, rested, sliced across
the grain, served with warm flour tortillas and grilled peppers/onions is a standard,
credible Tex-Mex fajita presentation; the Food Network Kitchen source is a reasonable
mainstream accepted variation, and the recipe does not overclaim a specific
restaurant's proprietary formula (correctly so, since Ninfa's own original was a
differently-marinated carne asada "tacos al carbon," not this exact rub).

**Source fidelity:** Matches the Food Network source closely — rub proportions,
marinating window (30 min–2 hr), pepper/onion sauté, grill times by thickness, and
5-minute rest before slicing all verified directly; no discrepancies found.

**Specificity:** Good — skirt steak explicitly flagged as traditional; flour (not
corn) tortillas correctly specified as the Tex-Mex-standard choice; spice rub
components (chipotle, chili powder, cumin) are appropriately named.

**Components:** `quick-guacamole` and `fresh-pico-de-gallo` checked (see component
sections below); both single-consumer, this recipe. No new candidate: the spice rub is
a simple pantry spice mix and the tortillas are correctly left as a standard store-
bought item — neither meets the Check 5 bar for a scratch component.

**Readability:** A. Clear rub quantities, marinating range, grill times split by
thickness, explicit medium-rare doneness target, rest-then-slice sequencing.

**Decision:** keep.

**Findings:** None required. Optional, non-blocking enhancement: Kitchen Notes could
cite Ninfa's/Houston's specific role in popularizing fajitas (chron.com) for a
stronger city-fit citation than the current generic Tex-Mex framing, though the
existing text is already accurate and not a defect.

**Replacement candidates:** None.

**Access failures:** None.

---

## component:horseradish-cocktail-sauce

- Path: `components/sauces/horseradish-cocktail-sauce.md` · Hash: `b1e1b477baf3ed1c7ea980e5fd70e8a3e7d7c4c2`
- Source: https://eatsforone.com/2012/02/08/st-elmos-shrimp/
- Consumers: `st-elmo-style-shrimp-cocktail` only (reviewed above, same batch). No
  cross-batch sharing.

**Authenticity:** Pass, correctly labeled. Note already states this is "adapted from
Eric's stronger home version," "a documented home approximation, not a verified St.
Elmo formula" — exactly separates traditional (St. Elmo's own bottled sauce, offered
as the alternative) from unsupported copycat (this scratch version).

**Source fidelity:** Verified the scaling math against the source: source uses 1 cup
ketchup as the baseline "Eric's stronger" version; our component doubles horseradish,
zest, lemon juice and ketokchup-adjacent quantities proportionally while holding
vinegar constant for the soak/drain step (a soak medium, not a scaled ingredient) —
reasonable and correctly reasoned scaling, not an error.

**Specificity:** Good — fresh horseradish root (not jarred prepared horseradish) is
correctly distinguished per Check 4's own example; Heinz ketchup named specifically.

**Readability:** A. Clear steps (grate, soak overnight, drain, stir, taste-test before
adding extra), explicit heat-level control via the "extra root" side portion.

**Decision:** keep.

**Findings:** Minor/cosmetic — yield "about 1¼–1½ cups" is not labeled "(estimated)"
though it is derived math, not source-stated; sibling components in this batch
(`fresh-pico-de-gallo`, `quick-guacamole`) do label their yields "(estimated)" for
consistency. Recommend the same label here. Confidence: high, low severity.

**Access failures:** None.

---

## component:creamy-stone-ground-grits

- Path: `components/sides/creamy-stone-ground-grits.md` · Hash: `6516ddef63742c804320b00d987d2a566a6bcd86`
- Source: https://www.pauladeen.com/recipe/buttery-stone-ground-grits/
- Consumers: `mayport-shrimp-and-grits` only (reviewed above, same batch). No
  cross-batch sharing.

**Authenticity:** Pass. Note correctly frames this as "Paula Deen's Southern
butter-and-cream preparation, offered as a homemade alternative to the Jacksonville
recipe's purchased grits" and correctly identifies it as "not the manufacturer's
formula" — accurate on both counts (verified the source recipe does specify Gracious
Grits as the purchased product being alternated with).

**Source fidelity:** Essentially verbatim match to pauladeen.com, including the exact
"37 minutes cooking" figure cited in the component's own Note (source lists that
figure; our own estimate of "30–40 minutes" is explicitly and correctly labeled
separately as an estimate). No discrepancies found.

**Specificity:** Good — "stone-ground grits, not instant" is exactly the right
distinction for this style; unsalted butter and heavy cream both specific enough.

**Readability:** A. Clear quantities, ordered two-stage cooking with a concrete
doneness test ("grains should be tender, without a hard center"), thinning guidance if
the mixture over-thickens.

**Decision:** keep.

**Findings:** None.

**Access failures:** None.

---

## component:fresh-pico-de-gallo

- Path: `components/toppings/fresh-pico-de-gallo.md` · Hash: `f3ea64ff96a684b47b4a19eba53e443dcaf3bf01`
- Source: https://www.rickbayless.com/recipe/salsa-mexicana/
- Consumers: `fajitas` only (reviewed above, same batch). No cross-batch sharing.

**Authenticity:** Pass. Diced tomato, white onion, chile, cilantro, lime — the
standard salsa mexicana/pico de gallo formula; matches Bayless's own recipe identity
directly, not a copycat guess.

**Source fidelity:** One finding — the source states an explicit yield of
"Approximately 1½ cups," but our component states "about 2 cups (estimated; tomato
size and draining vary)." The ingredient quantities themselves (2 medium tomatoes,
½ onion, 1 chile, 2–3 tbsp cilantro, 2 tbsp lime juice) match the source's own recipe
scale, so the higher yield figure appears to be an unverified estimate rather than a
scaled-up recipe. Recommend correcting the yield to align with the source's stated
"approximately 1½ cups," or re-deriving the 2-cup figure with a stated basis, if one
exists. Severity: minor. Confidence: high (source yield line directly verified).

**Specificity:** Good — "jalapeño or serrano" gives an appropriate regional-style pair;
white onion (not yellow) correctly specified per authentic salsa mexicana convention.

**Readability:** A. Clear quantities, simple two-step method, explicit rest/adjust
step.

**Decision:** targeted fix (yield figure only; ingredients and method are correct).

**Findings:** See Source fidelity above — yield correction, minor severity.

**Access failures:** None.

---

## component:quick-guacamole

- Path: `components/dips/quick-guacamole.md` · Hash: `9b78910ef67fbcf94f28389987339e6ab42fa07c`
- Source: https://www.rickbayless.com/recipe/guacamole-2/
- Consumers: `fajitas` only (reviewed above, same batch). No cross-batch sharing.

**Authenticity:** Pass, correctly labeled as a simplified home adaptation. The
component's own Note already states this "smaller, simple condiment version follows
Bayless's avocado, salt and lime foundation; his fuller version adds tomato and fresh
chile" — the omission of tomato/chile (present as core, non-optional ingredients in
Bayless's actual "guacamole-2" recipe) is transparently disclosed, so this is an
acceptable, correctly-labeled home adaptation rather than a silent transcription
error.

**Source fidelity:** Core proportions (2 avocados, 1 tbsp lime juice, ¼ tsp salt,
optional onion/cilantro) match the source's base recipe; the labeled tomato/chile
omission is the only departure, and it is disclosed. One minor finding: the source
page itself does not state a numeric yield ("Yield: not specified" on the page), but
our component states "About 1½ cups" as if it were a plain fact, with no "(estimated)"
qualifier — inconsistent with the sibling `fresh-pico-de-gallo` component's practice
of labeling derived yields as estimates.

**Specificity:** Adequate — Hass avocado correctly named as the standard guacamole
variety; salt/lime kept appropriately simple for this stripped-down version.

**Readability:** A. Two clear steps, explicit "serve promptly" endpoint with a
browning-prevention fallback.

**Decision:** keep, with one minor cosmetic fix (label yield as estimated).

**Findings:** Minor — add "(estimated)" to the yield line for consistency with
`fresh-pico-de-gallo`. Confidence: high, low severity. Suggestion only, not required:
consider naming the tomato/chile omission once more explicitly under a "Note" heading
title such as "Simplified from source" for extra clarity, though the current wording
already discloses it adequately.

**Access failures:** None.
