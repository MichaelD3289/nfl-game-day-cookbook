# Worker afc-east-2

Batch: 5 recipes (Dolphins x2, Jets x3) + 2 exclusively assigned components.
All sources fetched successfully; no access failures.

## cuban-frita-burger

- Path: `recipes/afc/east/dolphins/cuban-frita-burger.md` · status: published
- Source: https://burgerbeast.com/frita-cubana/ · checked 2026-09-26
- Hash: `cdc5e5a6b626a3dfed508cf832ec059a9c8fa802`

**City fit:** pass. Location Miami, FL. Frita Cubana is a well-documented Miami-Cuban street food (originated Havana, adopted/popularized in Miami's Cuban exile community); burgerbeast.com is a Miami-focused food blog, a credible local source.

**Authenticity:** finding. Source and broader Frita tradition use a beef+pork blend with BOTH sweet and smoked paprika; our recipe (matching its own cited source's ingredient list) uses pure ground chuck and a single paprika. This is a valid, source-supported simplified variant, not "the" authentic formula — should be labeled as a home/simplified variant rather than presented as definitive. Shoestring-potato-as-topping (the dish's defining trait) is present. Crystal Louisiana hot sauce and russet potatoes both match source exactly.

**Source fidelity:** finding (minor, internal source conflict). Ingredient list says "sweet Spanish paprika (pimentón dulce)" but the source's own ingredient list says plain "Spanish paprika," while the source's instructions say "smoked Spanish paprika." "Sweet" is unsupported by either part of the source. Potato frying temp/time is unspecified in the source too (already flagged honestly in our Kitchen Notes). USDA 160°F patty doneness is a reasonable food-safety addition not in source, correctly implicit rather than mis-attributed.

**Specificity:** pass. Crystal hot sauce named with a fair substitute; russet potato called out; chuck fat content not specified by source either (not a gap unique to us).

**Components:** none linked. Shoestring potatoes and the beef seasoning mix are single-use in this cookbook (no existing component matches); not proposing new components — insufficient reuse to justify per check 5.

**Readability:** B. Quantities, order and a doneness endpoint (160°F) are all clear; the only ambiguity is potato frying time/temp, which the recipe itself already flags as a gap rather than inventing one.

**Decision:** targeted fix.

**Findings:**
1. Minor — current text: "3 tablespoons sweet Spanish paprika (pimentón dulce)" — proposed: "3 tablespoons Spanish paprika" (or "smoked Spanish paprika" to match the source's own instructions) — rationale: source ingredient list has no "sweet"; source instructions say "smoked" — internal source inconsistency, but "sweet" appears nowhere in the source. Section: Ingredients. URL: https://burgerbeast.com/frita-cubana/. Confidence: high.
2. Minor — add one clause to Kitchen Notes or Authenticity framing noting that the fuller Frita tradition blends beef and pork with two paprikas, and this version (per its cited source) is a simplified all-beef, single-paprika variant. Section: Kitchen Notes. Confidence: medium (regional-variation framing, not a transcription error).

**Replacement candidates:** none — source is a legitimate, well-matched local food-blog recipe; no material reason to replace.

**Access failures / unverified claims:** none.

## cuban-sandwich

- Path: `recipes/afc/east/dolphins/cuban-sandwich.md` · status: published
- Source: https://www.foodnetwork.com/recipes/food-network-kitchen/cubano-9343989 · checked 2026-09-26
- Hash: `7c60aa8865da593c045f7fb28c9985461647ebd5`

**City fit:** pass. Miami, FL location. Recipe correctly omits salami/lettuce/tomato, matching Miami-style (versus Tampa's Cuban sandwich, which traditionally adds salami) — positive, independently-verified city-fit evidence.

**Authenticity:** pass, with one specificity note. "Mojo roast pork" and "sweet ham" both go beyond the source's plainer generic terms but are independently well-supported: mojo roast pork matches our own `cuban-mojo-pork` component; "sweet ham" corresponds to the traditional jamón dulce/bolo ham used in genuine Cubanos (confirmed via independent web search), not a fabrication. Pressed, buttered, foil-wrapped baking method matches source structure.

**Source fidelity:** finding (minor, metadata). Front matter states `cook: 35 minutes total`, but the source's and this recipe's own instructions describe roughly a 20-minute bake (step 3: "Bake about 20 minutes"). This reads as a timing double-count or stale estimate in the front matter rather than the instructions themselves, which are accurate.

**Specificity:** pass. "Sweet ham," "dill pickle slices" (6–8), and Swiss cheese are all reasonable, well-supported specificity beyond the source's generic terms. Photo credit lists "King Arthur Baking" while `source.url` is Food Network — this is a likely photo-credit/attribution mismatch worth flagging for the orchestrator to confirm and correct (image provenance, not a recipe-content error).

**Components:** two markers present and correctly placed in `## Ingredients`: `{{component:american-yellow-mustard}}` and `{{component:cuban-mojo-pork}}` (both reviewed below, both consistent). `quick_options` entries match each component's own `quick_buy` text. No missing component candidates — ham, cheese, pickles are reasonably left as plain purchased items.

**Readability:** B. Instructions are clear and ordered with a real temperature/time/visual endpoint (425°F, ~20 min, "hot and cheese melts"), but the front-matter `cook: 35 minutes total` conflicts with the ~20-minute bake actually described, which could mislead a reader's time planning.

**Decision:** targeted fix.

**Findings:**
1. Minor — current: `cook: 35 minutes total` — proposed: reconcile with the ~20-minute bake in step 3 (e.g., `cook: about 20 minutes`, or fold press/rest time explicitly if that's the intended source of the extra ~15 minutes) — rationale: apparent mismatch between front matter and instructions. Section: front matter. URL: https://www.foodnetwork.com/recipes/food-network-kitchen/cubano-9343989. Confidence: medium (could be intentional but is unexplained as written).
2. Minor — current: `photo_credit: King Arthur Baking` with a Food Network `source.url` — proposed: verify and correct photo attribution to match the actual image's origin. Section: front matter. Confidence: medium (flagging mismatch; did not independently trace the image file).

**Replacement candidates:** none — source is appropriate and well-matched.

**Access failures / unverified claims:** none.

## new-york-bagels

- Path: `recipes/afc/east/jets/new-york-bagels.md` · status: published
- Source: https://www.kingarthurbaking.com/recipes/bagels-recipe · checked 2026-09-26
- Hash: `1f59b67df8a23978dc0b0b886af834dcb6508dbf`

**City fit:** finding. The cited source page is a generic King Arthur bagel recipe that never mentions "New York," "NY-style," or any regional name anywhere on the page (confirmed by full-page targeted search). The recipe's "New York bagels" title/framing is not established by its own citation. Independent research (multiple bagel-technique sources plus general baking references) confirms the underlying technique — high-gluten/bread flour, malt in dough and water bath, boil-then-bake — genuinely matches authentic NY-style bagel-making, so the regional claim is defensible on independent grounds, but the citation itself has a sourcing gap.

**Authenticity:** pass (on independent grounds, not the source itself). Boil-then-bake with a malted water bath is the defining NY bagel technique and is faithfully present.

**Source fidelity:** pass. Transcription is highly faithful: dough ingredients, hole-widening to 1 1/2–2 inches, boiling in batches without crowding, boil timing (2 min first side/1 min after flip), bake time and mid-bake flip all match the source closely.

**Specificity:** pass. Bread flour, malt (with dark brown sugar substitute noted), and optional sesame/poppy topping are all appropriately specific.

**Components:** none applicable; this recipe is itself a from-scratch bready base item, not a consumer of shared components.

**Readability:** A. Clear quantities, ordered steps, explicit times and a visual doneness endpoint ("deeply browned").

**Decision:** targeted fix (citation/framing gap, not a content correction).

**Findings:**
1. Minor — current: recipe titled/framed as "New York bagels" citing a King Arthur page that never uses that regional term — proposed: either find/cite a source that explicitly discusses NY-style bagels, or add a short note in Kitchen Notes explaining that the technique (not the cited source's own framing) is what establishes the NY-style association. Section: front matter / Kitchen Notes. URL: https://www.kingarthurbaking.com/recipes/bagels-recipe. Confidence: high (confirmed absence via full-page search).

**Replacement candidates:** a source that explicitly discusses NY-style bagel history/technique (e.g., a NY bagel-shop-attributed recipe or a credible food-history piece) would close the citation gap without changing the recipe content, since the technique itself already checks out.

**Access failures / unverified claims:** none.

## new-york-style-cheese-pizza

- Path: `recipes/afc/east/jets/new-york-style-cheese-pizza.md` · status: published
- Source: https://www.kingarthurbaking.com/recipes/new-york-style-pizza-recipe · checked 2026-09-26
- Hash: `4f91cf7d60818203e14b29ca1d163837114cb709`

**City fit:** pass. Source headnote explicitly describes genuine NY-style characteristics (well-fermented dough, thin foldable slice) — direct, strong support, unlike the bagel recipe above.

**Authenticity:** pass. Long cold ferment (8–10 hr dough rest), high-heat steel/stone bake, and broil finish are all consistent with NY-style pizzeria technique as described by the source.

**Source fidelity:** pass. Dough, sauce and topping amounts all match source closely. Step 5's "5 to 7 minutes" bake compresses the source's fixed "5 minutes, +1–2 minutes if the bottom lacks color" into a range — arithmetically consistent (5 + up to 2 = up to 7), not a discrepancy.

**Specificity:** pass. Whole-milk low-moisture mozzarella and plum tomatoes are appropriately specific; bread flour and instant yeast amounts match source.

**Components:** none linked; sauce and dough are simple, single-use preparations. Not proposing a shared sauce component — only one current consumer, and check 5 says not to add components without meaningful reuse.

**Readability:** A. Clear quantities, times, temperatures and visual endpoints ("bottom colors," "spotted and browned") throughout.

**Decision:** keep.

**Findings:** none requiring correction.

**Replacement candidates:** none — source is a strong, well-matched authority for this dish.

**Access failures / unverified claims:** none.

## pastrami-on-rye-jets

- Path: `recipes/afc/east/jets/pastrami-on-rye-jets.md` · status: published
- Source: https://www.centralmarketnewyork.com/how-to-make-a-pastrami-sandwich-a-step-by-step-guide/ · checked 2026-09-26
- Hash: `3ff59375d028c5e40a4c0713fe0aa7bedddbf0c8`

**City fit:** pass. Central Market New York is a genuine Grand Central Terminal deli/market; a credible NYC-metro source for this dish.

**Authenticity:** pass. Independent cross-check (Katz's Deli practice, Wikipedia) confirms plain mustard + pickles is the traditional base, with cheese/sauerkraut/coleslaw as optional embellishments — matches our recipe's explicit "(optional)" labeling of those three items, which is accurate rather than watered-down.

**Source fidelity:** finding (minor, missing step). Source includes an explicit step to broil the assembled sandwich for about 60 seconds to melt the optional cheese; our recipe adds optional cheese in step 4 but never instructs melting it — the cheese-melt step is missing.

**Specificity:** minor opportunity, not an error. Source recommends French's/Gulden's for the mustard; our recipe says only "spicy brown deli mustard" (Katz's itself uses a housemade spicy brown mustard, so ours is not wrong — a brand example could be added but isn't required). Our recipe leads with "Jewish-style seeded rye" (marble rye as alternative) while the source leads with marble rye (classic rye as alternative) — an editorial emphasis reversal, not an error, since Katz's actually serves on seedless rye and "seeded" is a legitimate but non-universal regional variant; worth a light note, not a hard finding.

**Components:** `quick-creamy-coleslaw` (`components/sides/quick-creamy-coleslaw.md`) already exists in the cookbook and is currently used only by `recipes/afc/north/browns/polish-boy-sandwich.md`. This recipe's "1 cup coleslaw (optional)" is plain purchased/inline text with no component marker. Since coleslaw here is already labeled optional and is itself a non-traditional embellishment on pastrami-on-rye (per the authenticity check above), linking `{{component:quick-creamy-coleslaw}}` is a nice-to-have consistency improvement, not a required fix.

**Readability:** B. Times and order are clear (steam 5–8 min, toast 2–3 min, with a Kitchen Note acknowledging steps can overlap), but the missing cheese-melt instruction leaves the optional-cheese path incomplete.

**Decision:** targeted fix.

**Findings:**
1. Minor — current: step 4 adds optional cheese with no melting step — proposed: add "If using cheese, broil assembled sandwiches about 60 seconds until melted" (matching source) before serving. Section: Instructions, step 4. URL: https://www.centralmarketnewyork.com/how-to-make-a-pastrami-sandwich-a-step-by-step-guide/. Confidence: high.
2. Minor (optional) — current: "1 cup coleslaw (optional)" as plain text — proposed: consider `{{component:quick-creamy-coleslaw}}` for consistency with the cookbook's existing Make-It-or-Buy-It pattern. Section: Ingredients. Confidence: low/optional (coleslaw is already a non-traditional add-on here either way).

**Replacement candidates:** none — source is a legitimate NYC deli with clear, usable instructions.

**Access failures / unverified claims:** none.

## component:cuban-mojo-pork

- Path: `components/proteins/cuban-mojo-pork.md` · Source: https://www.foodnetwork.com/fnk/recipes/instant-pot-cuban-mojo-pork-9574117 · checked 2026-09-26
- Hash: `7bfed4aef714a9a861caf545af87925891fd7d46`
- Consumers (via `grep -rl '{{component:cuban-mojo-pork}}' recipes components`): `recipes/afc/east/dolphins/cuban-sandwich.md` only (reviewed above, in this batch).

**Assessment:** matches source closely, including the four-piece pork cut, reserved-marinade technique, and natural-release/reduce-and-shred sequence — the prior "Tune" pass (restoring the four-piece cut and cooked-yield estimate) holds up under independent re-verification. Minor, non-substantive omissions versus source: doesn't state "about 5 minutes per side" browning time, "8 to 10 minutes to come to pressure," or "reduced by half" as the liquid-reduction endpoint. None of these are contradictions, just slightly less complete than the source. Yield is explicitly and correctly labeled an estimate (source gives no cooked weight) — good practice. Correctly frames pressure-cooking as a home adaptation of traditional roast mojo pork (lechón), and orange+lime as a stand-in for sour orange — accurate, appropriately labeled.

**Decision:** keep. No corrections needed; two very minor completeness additions optional (per-side browning time, "reduced by half" endpoint) but not required.

## component:american-yellow-mustard

- Path: `components/toppings/american-yellow-mustard.md` · Source: https://www.adamwitt.co/allrecipes/4cknmn4gzlfd3se-6f73p-bzjk2-n8prs-bah54-4ew2f-h9l8y-n9hwn-awa68-bwbdj-52fx6-t44mc-z9mhb-gx2gd-29h9j · checked 2026-09-26
- Hash: `59309fc081a04d10c9c3b1fcfedde029c2159930`
- Consumers (via `grep -rl '{{component:american-yellow-mustard}}' recipes components`): `recipes/afc/east/dolphins/cuban-sandwich.md` (reviewed above, in this batch); also `recipes/nfc/north/packers/beer-brats.md`, `recipes/nfc/north/bears/chicago-style-hot-dogs.md`, and `recipes/nfc/east/eagles/philadelphia-soft-pretzels.md` — these three are outside my assigned batch; flagging for the orchestrator/other workers to inspect if not already covered elsewhere.

**Assessment:** ingredients and method match the source exactly (water, mustard powder, turmeric, garlic powder, paprika, salt, vinegar; same cook time/thickening method). The source's explicit mellowing note ("wait a few days... at first it will be strong") matches our component's chilling note. No unsupported storage-duration claim remains — the prior review's removal of an unsupported "one month" storage assertion holds up; current text makes no shelf-life claim beyond the mellowing period.

**Access note (not a hard failure):** the source domain is `adamwitt.co`, a page whose URL path (`/allrecipes/...`) and content (a bundle of five recipes) suggest it may be a personal mirror/archive of Allrecipes-style content rather than an original personal recipe; it fetched successfully and content matches our component, so this is flagged only as a provenance-confidence note for the orchestrator, not an access failure.

**Decision:** keep. No corrections needed.
