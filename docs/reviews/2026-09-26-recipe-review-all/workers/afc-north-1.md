# Worker batch: afc-north-1

Date checked: 2026-09-26

## recipes/afc/north/bengals/cheese-coneys.md

- ID: `cheese-coneys`
- Path: `recipes/afc/north/bengals/cheese-coneys.md`
- Status: `published`
- Source: https://oryana.coop/recipe/the-best-cincinnati-cheese-coney-recipe/
- Date checked: 2026-09-26
- Hash: `289915c8ec926580a20455727205972b2735ab7a`

**City fit:** Pass. Cheese coneys (chili-topped hot dogs, Cincinnati-style chili, shredded mild cheddar) are a genuine, well-documented Cincinnati specialty (Skyline/Gold Star chili-parlor tradition), independently corroborated via search.

**Authenticity:** The dish concept is authentic. Independent research confirms Cincinnati chili parlors traditionally serve coneys on **steamed** buns with **steamed/boiled** hot dogs, not grilled — grilling is a home/backyard variation, not the parlor-standard method.

**Source fidelity:** The cited source's own method only grills the hot dogs (medium-high grill, rotate, 6–8 min) and toasts the buns on the grill; it never mentions boiling/steaming. Our recipe's instructions invert this: they present steaming in hot water as the primary/default method and characterize grilling as "the source's ... charred variation," which misattributes the source's only stated method as a secondary option. This is a fidelity/attribution error, not an authenticity error — the steamed method is real and traditional, it's just not what this source says.

**Specificity:** Two small specificity losses vs. source: source specifies "potato hot dog buns (such as Martin's)" — ours drops the brand/type example; source specifies "Dutch-process cocoa powder" — ours just says "cocoa powder." Source calls for "6 all-beef hot dogs" (no size qualifier) — ours adds "small," a minor unlabeled addition.

**Components:** No Make-It-or-Buy-It component currently covers Cincinnati-style hot dog chili; not assigned to me and out of scope for a new proposal here, but flagging for the orchestrator that neither `cheese-coneys` nor `cincinnati-chili-over-spaghetti` has a shared component, despite both making a very similar chili from scratch. No existing component in `components/` covers this (confirmed via directory listing). Not recommending one be forced into this batch — the two chilis differ in scale and a couple of spices — but the orchestrator may want to weigh a shared `cincinnati-chili-base` component across both recipes.

**Readability:** A. Ordered steps, clear endpoints ("until fragrant," "simmer 18–20 minutes"), quantities given throughout.

**Decision:** Targeted fix.

**Findings:**
1. Severity: Moderate. Current text: instructions present steaming as the primary method and describe grilling as "the source's ... charred variation." Proposed fix: reverse the framing — present the source's method (grill 6–8 min, rotating; toast buns on the grill) as the primary/cited method, and add a brief separate note that steaming the dogs and buns is the traditional Cincinnati chili-parlor style (independently sourced, not from this URL). Rationale: avoids misattributing an untested claim to the cited source. URL: https://oryana.coop/recipe/the-best-cincinnati-cheese-coney-recipe/. Section: Instructions. Confidence: High.
2. Severity: Low. Current text: "soft hot dog buns." Proposed fix: "potato hot dog buns (such as Martin's)." Rationale: restores source specificity. URL: same. Section: Ingredients. Confidence: High.
3. Severity: Low. Current text: "cocoa powder." Proposed fix: "Dutch-process cocoa powder." Rationale: restores source specificity (Dutch-process affects chili's color/bitterness). URL: same. Section: Ingredients. Confidence: High.
4. Severity: Low. Current text: "mild yellow cheddar (sharp is a stronger alternative)." Source only calls for "shredded mild cheddar," no sharp alternative mentioned. Proposed fix: either remove the "sharp is a stronger alternative" aside or label it explicitly as our own substitution note, not sourced. Rationale: unlabeled addition not in source. URL: same. Section: Ingredients. Confidence: Medium.

**Replacement candidates:** None — source is reachable and mostly sound; targeted fixes are sufficient.

**Access failures / unverified claims:** None. Source fetched successfully. Note: an initial fetch of this URL returned an aside about the dish being "preferred in northern Michigan," which did not reappear in a follow-up literal/quoted re-fetch of the same page; I have treated the second, quote-anchored extraction as authoritative and did not use the unreproduced claim anywhere in this review.

---

## recipes/afc/north/bengals/cincinnati-chili-over-spaghetti.md

- ID: `cincinnati-chili-over-spaghetti`
- Path: `recipes/afc/north/bengals/cincinnati-chili-over-spaghetti.md`
- Status: `published`
- Source: https://www.foodnetwork.com/recipes/food-network-kitchen/cincinnati-chili-recipe-2043706
- Date checked: 2026-09-26
- Hash: `074046e9eda4b2e7bcc36a60e01db52bd9dd041d`

**City fit:** Pass. Cincinnati chili over spaghetti ("two-way") is the archetypal Cincinnati chili-parlor dish; strongly documented regionally.

**Authenticity:** Independent research confirms the traditional four-way/five-way topping bean is **red kidney beans**, not pinto — so our recipe's use of kidney beans, while it diverges from this cited source (which calls for pinto beans), is actually the more regionally authentic choice. This is a positive authenticity note but still an *unlabeled* deviation from the cited source.

**Source fidelity:** Two issues found by direct comparison against the fetched source (fetched twice to confirm):
1. The source gives **no quantity at all** for salt and pepper — it lists them as unquantified seasoning. Our recipe states "(recipe uses 1/2 teaspoon of each)," which is a fabricated, invented precise quantity attributed to the source. This is exactly the kind of silent invention the brief calls out as a fidelity violation.
2. Source calls for pinto beans; ours uses red kidney beans, unlabeled as a deviation (see Authenticity above — regionally justified, but should be disclosed as an intentional adaptation rather than presented as if sourced).

**Specificity:** Source specifies "1 large or 2 medium yellow onions, such as Vidalia, finely chopped" — ours drops the Vidalia example, generic "onion." Topping quantities ("about 2 cups warm kidney beans," "4 cups shredded cheddar") are not quantified per-serving in the source either, so this part is consistent with source vagueness, not a new fidelity problem.

**Components:** Same note as cheese-coneys — no shared chili component exists; not proposing one in this batch.

**Readability:** B. Mostly clear and ordered, but the fabricated salt/pepper parenthetical actively misleads a cook trying to follow the source, and topping-quantity vagueness ("add to preference") could use tighter guidance for a first-time cook.

**Decision:** Targeted fix.

**Findings:**
1. Severity: High. Current text: "Kosher salt and freshly ground black pepper (recipe uses 1/2 teaspoon of each)." Proposed fix: remove the parenthetical entirely, or replace with "Kosher salt and freshly ground black pepper, to taste" and drop the attribution to the source. Rationale: source specifies no quantity; the parenthetical fabricates and falsely attributes a precise figure. URL: https://www.foodnetwork.com/recipes/food-network-kitchen/cincinnati-chili-recipe-2043706. Section: Ingredients. Confidence: High.
2. Severity: Low. Current text: uses red kidney beans without comment. Proposed fix: add a brief note such as "(kidney beans, the traditional four-way topping — source uses pinto)." Rationale: discloses the deviation instead of presenting it silently; also documents that the substitution is regionally motivated. URL: same. Section: Ingredients or Kitchen Notes. Confidence: Medium.
3. Severity: Low. Current text: "onion, finely chopped." Proposed fix: "onion (such as Vidalia), finely chopped." Rationale: restores dropped source specificity. URL: same. Section: Ingredients. Confidence: High.

**Replacement candidates:** None — source is reachable and otherwise sound.

**Access failures / unverified claims:** None. Source fetched successfully twice.

---

## recipes/afc/north/bengals/goetta.md

- ID: `goetta`
- Path: `recipes/afc/north/bengals/goetta.md`
- Status: `published`
- Source: https://www.saveur.com/article/Recipes/Goetta/
- Date checked: 2026-09-26
- Hash: `4329ab85bc2ea45c420a5c37287418a7ec14ab31`

**City fit:** Pass. Goetta (beef/pork + steel-cut oat loaf, sliced and pan-fried) is a well-documented, distinctively Cincinnati dish tied to the city's German immigrant heritage; independently corroborated.

**Authenticity:** Confirmed authentic core recipe: beef+pork blend, steel-cut ("pinhead") oats (never rolled oats — using rolled oats is a recognized error that ruins the texture), onion, white pepper, formed into a loaf, chilled, sliced, and pan-fried until crisp. Our recipe matches this profile exactly, including the explicit "do not use rolled oats" caution.

**Source fidelity:** **Access failure** — saveur.com returned HTTP 403 Forbidden on two separate direct-fetch attempts; web.archive.org is blocked at the tool level and could not be used as a fallback. I used WebSearch to obtain search-result-snippet corroboration (not a verified direct read) of the source recipe. The snippet-level content strongly corroborates our recipe on: beef chuck and pork shoulder cuts and their approximate quantities (1.5 lb / 0.75 lb), beef stock, steel-cut oats and quantity (1 cup), dried onion flakes (1/4 cup), ground white pepper (1 1/4 tsp), method (simmer meat 1.5–2 hrs until tender, cook oats ~15 min, combine/puree, press into a loaf pan, refrigerate overnight, slice 1/2", pan-fry 4–5 min per side until crisp). I could **not** independently verify: the exact water quantities used for the meat simmer and for cooking the oats, and the frying medium ("canola oil" specifically) — the search snippets did not surface these details, and per the task's constraints I have not filled these gaps from memory. These remain unverified but are not contradicted by anything found.

**Specificity:** Good — steel-cut oats are explicitly required (with an explicit "not rolled oats" warning), white (not black) pepper is correctly specified, loaf pan size and slice thickness are given. No specificity issues found within what could be verified.

**Components:** Standalone recipe; goetta is not used in and does not use any other recipe/component in the book. No Make-It-or-Buy-It component is warranted (it is inherently a from-scratch, cure-like preparation, not a swappable side or sauce).

**Readability:** A. Clear ordered steps with concrete endpoints (simmer until fork-tender, oats until tender ~15 min, fry until crisp and browned 4–5 min/batch).

**Decision:** Keep — no discrepancy found between the recipe and the (partially verified) source; residual gaps are unverifiable due to a source access failure, not evidence of a problem.

**Findings:** None rising to a fix — no confirmed discrepancy found in the fields that could be checked.

**Replacement candidates:** None identified. (No alternate accessible mirror of this exact Saveur recipe was found via search; the snippets came from the same original URL's indexed text, not a mirror.)

**Access failures / unverified claims:**
- saveur.com/article/Recipes/Goetta/ — HTTP 403 Forbidden on two direct WebFetch attempts (persistent, not transient). web.archive.org unavailable (tool-level block).
- Mitigation: WebSearch snippet-level corroboration used for partial verification only, explicitly not equivalent to a direct source read.
- Unverified specifics: exact water quantities for the meat simmer (recipe states "4 cups water") and for cooking the oats (recipe states "3 1/3 cups water"), and the frying oil type ("canola oil," 1/4 cup). None of these were contradicted by available evidence; they simply could not be confirmed against the primary source.

---

## recipes/afc/north/browns/polish-boy-sandwich.md

- ID: `polish-boy-sandwich`
- Path: `recipes/afc/north/browns/polish-boy-sandwich.md`
- Status: `published`
- Source: https://www.reneeskitchenadventures.com/2016/04/polish-boy-sandwich.html
- Date checked: 2026-09-26
- Hash: `086bbc44073d4aef51d84afbe0099d3f52753a9c`

**City fit:** Pass. The Polish Boy (kielbasa + fries + BBQ sauce + coleslaw on a bun) is a well-documented Cleveland original (independently corroborated; commonly associated with Cleveland rib houses such as Freddie's Southern Style Rib House and the "Polish Boys" food-truck/street-cart tradition).

**Authenticity:** Core structure matches the authentic dish exactly: kielbasa, fries, tangy BBQ sauce, coleslaw, all stacked in a bun/hoagie roll.

**Source fidelity:** Source fetched successfully (an initial attempt returned a transient 403; a retry succeeded). Quantities match the source closely (2 rolls, 2 kielbasa links, half of a 32 oz fries package, 1/4 cup BBQ sauce, 1 cup coleslaw, oil for the skillet, assembly order of sauce-then-fries-then-slaw). One unlabeled deviation found: the source's original recipe uses **turkey kielbasa** ("I used turkey kielbasa..." per the source's own text); our recipe calls for "smoked pork kielbasa" without noting this as a deviation from the cited source. Independent research supports pork kielbasa as the traditionally authentic choice for this dish, so the substitution is regionally sound, but it should be disclosed as an intentional adaptation rather than left silent, per the brief's guidance on labeling adaptations.

**Specificity:** Front-matter `quick_options` for the barbecue-sauce component states: "Use KC Masterpiece Sweet Honey & Molasses or another Kansas City-style tomato-and-molasses sauce." Independent research on the Cleveland Polish Boy tradition describes the sauce as a generic "sweet, tangy" or "Southern rib-house style" sauce (associated with Freddie's Southern Style Rib House), not as specifically "Kansas City-style" — I found no regional source calling for Kansas City-style sauce on a Polish Boy. This over-specifies a regional identity ("Kansas City-style") that isn't supported for this Cleveland dish. The in-body ingredient line already hedges better ("tangy tomato-based barbecue sauce (or Cleveland-style hot sauce)"), so the fix is to align the front-matter language with that more neutral framing.

**Components:** All three of my assigned components are consumed here:
- `{{component:oven-fries}}` — used for the fries.
- `{{component:kansas-city-barbecue-sauce}}` — used for the sauce.
- `{{component:quick-creamy-coleslaw}}` — used for the slaw.

**Readability:** A. Short, clearly ordered steps with quantities and a clear endpoint ("cook kielbasa until heated through and browned").

**Decision:** Targeted fix.

**Findings:**
1. Severity: Low. Current text: "smoked pork kielbasa" with no note about the source's turkey kielbasa. Proposed fix: add a brief note, e.g., "(the cited source uses turkey kielbasa; pork is the more traditional Polish Boy choice)." Rationale: discloses an unlabeled deviation from the cited source, even though the deviation is regionally beneficial. URL: https://www.reneeskitchenadventures.com/2016/04/polish-boy-sandwich.html. Section: Ingredients or Kitchen Notes. Confidence: High.
2. Severity: Moderate. Current text (front matter `quick_options`): "Use KC Masterpiece Sweet Honey & Molasses or another Kansas City-style tomato-and-molasses sauce." Proposed fix: reframe as a generic recommendation, e.g., "Use a sweet, tangy barbecue or rib sauce (such as Sweet Baby Ray's Original, or a Kansas City-style tomato-and-molasses sauce) — Cleveland rib houses serve a similarly sweet-tangy style." Rationale: avoids asserting an unsupported "Kansas City-style" regional identity for a Cleveland dish; independent research found no source calling for that specific regional style here. URL: same. Section: front matter `quick_options`. Confidence: Medium.
3. Severity: Low. Current text: omits the source's serving suggestion not to overstuff the sandwich with all the fries (source suggests reserving some fries to serve on the side). Proposed fix: optionally add a Kitchen Note: "Save any extra fries to serve on the side rather than piling them all into the sandwich." Rationale: minor usability note present in source, dropped in transcription. URL: same. Section: Kitchen Notes. Confidence: Medium.

**Replacement candidates:** None — source is reachable and sound; targeted fixes are sufficient.

**Access failures / unverified claims:** reneeskitchenadventures.com returned a transient HTTP 403 on the first fetch attempt; a retry succeeded and returned the full recipe. Not treated as a persistent access failure.

---

## component:kansas-city-barbecue-sauce

- Path: `components/sauces/kansas-city-barbecue-sauce.md`
- Source: https://www.kshb.com/lifestyle/food/recipe-make-your-own-kc-style-sauce-in-honor-of-the-american-royal-world-series-of-barbecue
- Date checked: 2026-09-26
- Hash: `27151959733211d60e25f8f0976977aa98cff46a`

**Source fidelity:** Verified against the fetched source; matches exactly on every ingredient and quantity (Ardie Davis's regional KC-style formula: ketchup, molasses, brown sugar, vinegar, Worcestershire, mustard, spices in the stated proportions) and on method/timing. This is consistent with the prior scratch-components review's "Tune" note (molasses/time clarifications), which appears to have already been applied.

**Specificity:** Good — quantities, named ingredients, and simmer time are all present and match source.

**Readability:** A.

**Decision:** Keep. No discrepancies found.

**Findings:** None.

**Consumers** (via `grep -rl '{{component:kansas-city-barbecue-sauce}}' recipes components`):
- `recipes/afc/north/browns/polish-boy-sandwich.md` (reviewed above — flagged for the "Kansas City-style" regional-framing issue in that recipe's own front matter, not in this component file itself).
- `kansas-city-style-barbecue-chicken.md` — not reviewed by me; assigned to a different batch/worker. Flagging only that it exists as a consumer for the orchestrator's cross-batch awareness.
- `kansas-city-burnt-ends.md` — not reviewed by me; same note.

**Access failures / unverified claims:** None.

---

## component:oven-fries

- Path: `components/sides/oven-fries.md`
- Source: https://www.foodnetwork.com/recipes/tyler-florence/oven-fries-recipe-1946000
- Date checked: 2026-09-26
- Hash: `3dad5fa4ae712295fb3016a019147aa8947441ee`

**Source fidelity:** Verified against the fetched source; matches on oil, salt, and oven method/temperature/timing. The component text already explicitly labels its own adaptation: it omits the source's parsley/Parmesan finish, and separately notes it is a plain, homemade alternative to the frozen fries called for by the Polish Boy recipe — this is a well-labeled, transparent adaptation, consistent with the prior scratch-components review's "Tune" note.

**Specificity:** Good — oil type, salt, and baking time/temperature specified.

**Readability:** A.

**Decision:** Keep. No discrepancies found; adaptation is already properly disclosed.

**Findings:** None.

**Consumers** (via `grep -rl '{{component:oven-fries}}' recipes components`):
- `recipes/afc/north/browns/polish-boy-sandwich.md` (reviewed above) — only consumer found.

**Access failures / unverified claims:** None.

---

## component:quick-creamy-coleslaw

- Path: `components/sides/quick-creamy-coleslaw.md`
- Source: https://www.foodnetwork.com/recipes/food-network-kitchen/the-best-creamy-coleslaw-7447977
- Date checked: 2026-09-26
- Hash: `a7802b59d9e1acad4ef2a9aa5032516eeb4c4480`

**Source fidelity:** Verified against the fetched source; matches almost exactly on ingredients, quantities, and timing, including the source's active/chilling time note. Consistent with the prior scratch-components review's "Tune" note (add active/chilling time), which appears to have already been applied.

**Specificity:** Good.

**Readability:** A.

**Decision:** Keep. No discrepancies found.

**Findings:** None.

**Consumers** (via `grep -rl '{{component:quick-creamy-coleslaw}}' recipes components`):
- `recipes/afc/north/browns/polish-boy-sandwich.md` (reviewed above) — only consumer found.

**Access failures / unverified claims:** None.
