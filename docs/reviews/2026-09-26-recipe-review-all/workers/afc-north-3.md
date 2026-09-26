# Worker afc-north-3 — Steelers batch

Date checked: 2026-09-26. Mode: suggest (research only; no source files edited).
No shared components were assigned to this worker.

## chipped-ham-barbecue-sandwiches

- **Path:** `recipes/afc/north/steelers/chipped-ham-barbecue-sandwiches.md`
- **Status:** published · **Source:** https://hearthandvine.com/ham-barbecue-sandwiches/
- **Hash:** `e5452a58f115c087b3d13361765c6d44371fca32`

**City fit — pass.** Chipped chopped ham BBQ is a Pittsburgh-specific dish tied to Isaly's, a Mansfield, OH–founded chain that grew to ~100 Pittsburgh-area stores and is credited (via employee Claire Hatch, early 1930s) with inventing paper-thin "chipped chopped" ham. Independent corroboration: Pittsburgh Magazine ("The Savvy Yinzer's Guide to Chipped Chopped Ham"), Wikipedia (*Chipped chopped ham*, *Isaly's*), Tasting Table, Sandwich Tribunal. Regional scope extends into Western PA/WV/eastern OH but Pittsburgh is the recognized origin/identity city — consistent with the cookbook's Pittsburgh location tag.

**Authenticity — pass, traditional/local.** Defining traits: paper-thin ("chipped") chopped ham loaf, warmed in a sweet-tangy ketchup/brown-sugar/vinegar BBQ sauce, served on a soft roll — all present. This is the standard home/community-cookbook preparation (not a single restaurant's proprietary formula); the source itself frames it as a classic Pittsburgh home dish. No conflicting authoritative version found.

**Source fidelity — pass.** Re-fetched source ingredient list and steps match the recipe file line for line: brown sugar 1/4 cup, ketchup 1.5 cups, cider vinegar 1/4 cup, Worcestershire 1 Tbsp, mustard 1 Tbsp, onion powder 1 Tbsp, salt/pepper to taste, 1 lb ham, combine sauce → stir in ham → warm 15–20 min → serve on Kaiser rolls. No omissions, additions, or scaling errors found. The bun-count aside ("use up to 6 smaller buns if preferred") is a harmless, clearly-labeled serving-size accommodation, not a source claim.

**Specificity — two optional upgrades, medium confidence:**
- Source names **Heinz** ketchup specifically, and Heinz originates in Pittsburgh — a well-supported regional match, not just a preference call.
- Source's own substitution note for non-Isaly's ham says "ask a deli to shave **Virginia ham** razor-thin"; the recipe's fallback ("other ham shaved paper-thin at deli") is vaguer than the source.

**Components — none used, none needed.** No existing `components/` sauce matches this ketchup/vinegar BBQ sauce (checked all 8 files in `components/sauces/`); it is recipe-specific and fully specified in-line already, so no Make-It-or-Buy-It gap. No shared consumers to flag.

**Readability: A.** Two short numbered steps, explicit quantities, a clear doneness/time endpoint (15–20 min warmed through), and an unambiguous serving instruction.

**Decision: keep.**

**Findings**
1. *Minor, specificity.* Current: `1 1/2 cups ketchup`. Proposed: `1 1/2 cups ketchup (Heinz, if available, for a Pittsburgh-made match)`. Rationale: source explicitly calls for Heinz; Heinz is a Pittsburgh-founded brand, so this is a defensible regional callout, not a mandatory-brand claim. Section: Ingredients. Source: https://hearthandvine.com/ham-barbecue-sandwiches/. Confidence: medium.
2. *Minor, specificity.* Current: `...or other ham shaved paper-thin at deli`. Proposed: `...or Virginia ham shaved paper-thin at deli`. Rationale: matches the source's own named substitute rather than a generic "other ham." Section: Ingredients. Source: same URL. Confidence: medium.

**Access failures:** none.

---

## haluski-cabbage-and-noodles

- **Path:** `recipes/afc/north/steelers/haluski-cabbage-and-noodles.md`
- **Status:** published · **Source:** https://www.thekitchenwhisperer.net/2024/02/09/the-best-pittsburgh-haluski-fried-cabbage-and-noodles-in-butter/
- **Hash:** `5364106def0902f74c2336becc57de3410b3816e`

**City fit — pass (regional, city-adopted).** Haluski (butter-fried cabbage and noodles) is documented as a Western Pennsylvania/Pittsburgh staple brought by Slovak/Polish/Ukrainian immigrants, especially associated with Pittsburgh's Polish Hill and Lenten meals. Corroborated independently by WVIA public radio ("Recipes of the Region"), America's Test Kitchen ("Pittsburgh-style haluski"), and multiple food-history write-ups. It is a broader Coal Region/Western PA dish adopted into Pittsburgh identity rather than a Pittsburgh invention — the recipe's Pittsburgh location tag is defensible as city-adopted regional food, consistent with check #1's allowance for regional adoption.

**Authenticity — pass, traditional/accepted variation.** Defining traits: cabbage and egg noodles pan-fried in a generous amount of butter, onion, optional kielbasa, traditionally meatless for Lent — all present and correctly balanced (butter is the dominant fat, not oil). This matches the accepted "Pittsburgh-style haluski" pattern rather than a diluted or Americanized shortcut.

**Source fidelity — pass, one minor condensation.** Re-fetched source matches the recipe's ingredients exactly (8 Tbsp butter divided as 3+2+3, 1 large onion, 1.5 lb cabbage, 1–1.5 tsp each salt/pepper divided, 8 oz egg noodles, optional 14 oz kielbasa, green onion, optional sour cream) and the cook times (cabbage 15–23 min covered; noodles cooked 1 minute under package time; final combine 5–6 min) are unchanged. One condensation: the source stages cabbage in three additions with butter interleaved (1/3 cabbage → 2 Tbsp butter → 1/3 cabbage → final 1/3 cabbage), while the recipe compresses this to "Add cabbage in thirds ... add 2 more tablespoons butter as cabbage is added" — total butter and cabbage quantities are unchanged, but exactly when the mid-stage butter goes in is less precise than the source.

**Specificity — one low-priority note.** The recipe adds "wide" to "egg noodles," which the source does not specify (source just says "egg noodles"). Wide egg noodles are the common choice in most published haluski recipes, so this isn't a fidelity error, but it is an editorial addition beyond the literal source text and should be understood as such if anyone traces it back. Kielbasa could optionally be specified as Polish-style smoked kielbasa for regional clarity, but the current generic term is already adequate (not flagged as a required fix).

**Components — none used, none needed.** This dish's home-made character (butter-fried cabbage/noodles) is the whole point; there is no purchased shortcut to flag, and no existing `components/` entry overlaps it.

**Readability: B.** Quantities and endpoints are clear, but the condensed cabbage/butter staging in step 1 (see fidelity note) requires the cook to infer timing the source states explicitly.

**Decision: keep.**

**Findings**
1. *Minor, source fidelity/readability.* Current: `Add cabbage in thirds, seasoning with 1 teaspoon each salt and pepper; add 2 more tablespoons butter as cabbage is added.` Proposed: `Add the first third of cabbage with 1 teaspoon each salt and pepper, stir in the second third with 2 more tablespoons butter, then add the final third.` Rationale: restores the source's specific staging order without changing any quantity. Section: Instructions step 1. Source: https://www.thekitchenwhisperer.net/2024/02/09/the-best-pittsburgh-haluski-fried-cabbage-and-noodles-in-butter/. Confidence: medium (clarity improvement, not a correctness error).
2. *Minor, specificity (informational).* Current: `8 ounces wide egg noodles`. Note: "wide" is an editorial addition not present in the cited source; harmless and conventional, but flagged for transparency rather than proposed as a required change. Confidence: low priority.

**Access failures:** none — thekitchenwhisperer.net fetched successfully (not one of the domains the brief flagged as blocked).

---

## pierogi

- **Path:** `recipes/afc/north/steelers/pierogi.md`
- **Status:** published · **Source:** https://www.foodnetwork.com/recipes/food-network-kitchen/the-best-potato-and-cheese-pierogi-19951953
- **Hash:** `a5ee4dc5cfa902b2f1556793cda35cb37464b641`

**City fit — pass.** Pittsburgh has one of the largest Polish-American populations of any U.S. city (Polish Hill neighborhood; ~200,000 Poles in Pittsburgh by 1920 per historical counts), and pierogi are deeply embedded in local food culture — bars/restaurants city-wide serve them, the Pittsburgh Pirates' "Great Pierogy Race" (started 1999) is a civic institution, and Mrs. T's (a major national pierogi brand) is Pennsylvania-rooted. Corroborated via paeats.org, Chowhound, Wikipedia (*Great Pierogy Race*), and MLB.com. Regional/city association is well supported.

**Authenticity — pass, traditional/local variant.** Potato-and-cheddar is specifically the standard Pittsburgh Polish-deli filling — confirmed via S&D Polish Deli (Strip District, a long-standing Pittsburgh Polish institution), which sells "Pierogi Potato & Cheddar Cheese" as one of its traditional offerings. This distinguishes it from the more strictly "old-country" Polish farmer's-cheese (twaróg) filling; both are legitimate, but cheddar is the documented Pittsburgh-area norm, so this is a supported local variant rather than an unsupported Americanization.

**Source fidelity — pass, one minor omission.** Re-fetched Food Network recipe matches the file's ingredients and quantities exactly: dough (2 cups flour, 1 tsp salt, 1/2 cup sour cream, 2 Tbsp oil, 2 Tbsp cold water, 1 egg), filling (10 Tbsp butter total split 4+4+2, 2 onions, 1 lb russet potatoes, 1 cup white cheddar, 1/4 cup sour cream, salt divided 1/2 + 1 tsp), yield "About 2 1/2 dozen," and the same step sequence (dough rest 30 min; onions 15–20 min; potatoes boiled 15–18 min; assembly with 3 1/2-inch rounds; boil until they float + 3–4 more minutes; finish in the reserved onion-butter skillet). One detail dropped: the source specifies rolling dough into a "thin 15-inch square" before cutting rounds; the file only says "Roll half the dough very thin," losing the source's concrete size/thinness reference.

**Specificity — adequate, no changes required.** White cheddar (~4 oz) and russet potatoes are both correctly specific already; sour cream and butter are generic staples that don't need a brand callout. No further recommendation.

**Components — none used, none needed.** Checked all `components/` — no existing scratch dough, mash, or caramelized-onion component overlaps this recipe, and there's no purchased-item shortcut here to convert (the dish is inherently from-scratch). No candidate proposed.

**Readability: B.** Steps are well-ordered with clear endpoints (float + 3–4 min; 15–20 min deep-golden onions), but "roll very thin" is subjective without the source's 15-inch-square reference, risking inconsistent dough thickness for a first-time cook.

**Decision: keep.**

**Findings**
1. *Minor, readability.* Current: `Roll half the dough very thin. Cut 3 1/2-inch rounds.` Proposed: `Roll half the dough into a thin 15-inch square. Cut 3 1/2-inch rounds.` Rationale: restores the source's concrete sizing cue that "very thin" alone omits. Section: Instructions step 4. Source: https://www.foodnetwork.com/recipes/food-network-kitchen/the-best-potato-and-cheese-pierogi-19951953. Confidence: medium.

**Access failures:** none — Food Network page fetched successfully.

---

## primanti-style-sandwiches

- **Path:** `recipes/afc/north/steelers/primanti-style-sandwiches.md`
- **Status:** published · **Source:** https://www.epicurious.com/recipes/food/views/primantis-sandwich-369031
- **Hash:** `0c58291c42043ecbb4883f3354d1d8db679c8566`

**Access failure:** WebFetch could not reach `www.epicurious.com` or `epicurious.com` (tool-level block, same class of failure as the allrecipes.com/archive.org blocks called out in the brief). I did not read the canonical page directly. To compensate, I corroborated via: (a) WebSearch snippets that quote the Epicurious page's ingredient list and slaw/fries instructions near-verbatim, and (b) a full fetch of https://lidiasitaly.com/recipes/primantis-sandwich/, which is explicitly the same recipe from the cookbook *Lidia's Italy in America* (the Epicurious page is Condé Nast's republication of that same cookbook recipe — matching "Serves 2" and identical ingredient quantities). I'm treating the Lidia's Italy fetch plus the search snippets as strong corroboration of the Epicurious text, not as a substitute canonical source; the exact Epicurious page itself remains unverified by direct read.

**City fit — pass.** Primanti Bros. is Pittsburgh's most iconic sandwich, founded 1933 in the Strip District. Corroborated independently via Wikipedia, PA Center for the Book ("The Steel City's Signature Sandwich"), and Saveur's history piece. Saveur's piece ("How Pittsburgh's Famous Sandwich Became its Most Beloved Fake News") notes the popular "fed steelworkers/eaten one-handed by truck drivers on shift" origin story is embellished folklore layered onto a real 1933 Strip District sandwich cart — worth knowing, but doesn't undermine the dish's genuine Pittsburgh identity, only some of its oral-history embellishments.

**Authenticity — pass, with an explicit classification caveat.** Defining traits present and correct: French fries **and** oil-and-vinegar-based coleslaw stacked inside the sandwich (not a mayo slaw — confirmed as "a very important distinction" per goodfoodstories.com), sliced meat + provolone, tomato, thick soft Italian bread. Primanti Bros.' actual in-restaurant recipe is proprietary and unpublished, so this Lidia Bastianich recipe is a credible **chef-attributed home adaptation/copycat** that reproduces the dish's defining structure — not a verified transcript of the restaurant's own formula. The recipe file doesn't overclaim authenticity beyond its title ("Primanti **style**"), which is appropriate framing.

**Source fidelity — pass (via corroboration described above).** Every ingredient and quantity in the file matches both the Lidia's Italy fetch and the WebSearch-quoted Epicurious text exactly: 3 cups Savoy cabbage, 1 Tbsp cider vinegar, 2 tsp EVOO, 1/4 tsp celery seed, 1/4 tsp salt + more to season, 1/4 tsp sugar, 2 small russet potatoes, vegetable oil for frying, 4 oz capicola, 4 oz provolone, 4 slices Italian bread (~6x4 in, not too crusty), 1 tomato. Steps also match (slaw rests while fries cook; capicola seared ~1 min/side then provolone melted on top; fries 8–10 min in ~1 inch oil). Two small procedural details present in both corroborating sources are missing from the file: potatoes should be cut into "1/4- to 1/2-inch sticks" (file just says "into fries"), and the fries should be turned "occasionally" while frying (file omits this).

**Specificity — adequate; one optional note.** Capicola/provolone/Savoy cabbage/russet potatoes are all correctly specific already. "Hot or sweet, to preference" for capicola is a fair, clearly-labeled optional call, not an overreach.

**Components — none used, none needed, one caution for the orchestrator.** This recipe's coleslaw is oil-and-vinegar based and structurally different from the existing `components/sides/quick-creamy-coleslaw.md` (mayonnaise/sour-cream based, built for the Browns' Polish Boy sandwich) — **do not** treat that component as a substitute here; swapping in a creamy slaw would erase a defining trait of the Primanti's sandwich. Likewise, the existing `components/sides/oven-fries.md` uses a different (oven) method than this dish's defining hot-oil fry, so it is not a good match either. No new component is proposed — the fries and slaw are simple enough, and specific enough to this one sandwich, that in-line scratch instructions remain appropriate.

**Readability: B.** Steps are ordered with reasonable endpoints, but two source details that aid consistent results are missing (potato stick size, "turning occasionally" while frying), and the Kitchen Notes total-time estimate is explicitly labeled as an editorial estimate (good practice, no issue there).

**Decision: keep.**

**Findings**
1. *Minor, readability.* Current: `Cut unpeeled potatoes into fries.` Proposed: `Cut unpeeled potatoes into 1/4- to 1/2-inch sticks.` Rationale: source specifies a cut size the file omits. Section: Instructions step 2. Source: https://lidiasitaly.com/recipes/primantis-sandwich/ (corroborating the inaccessible Epicurious canonical URL). Confidence: medium.
2. *Minor, readability.* Current: `Fry in about 1 inch of vegetable oil over medium heat 8–10 minutes until cooked and crisp; drain and season with salt.` Proposed: add "turning occasionally" to the frying step. Rationale: source instructs turning for even browning; omission risks uneven fries. Section: Instructions step 2. Source: same. Confidence: medium.

**Access failures:** Epicurious canonical URL blocked for WebFetch (tool-level block); compensated with lidiasitaly.com (same cookbook recipe) and WebSearch snippets as described above. No claim in this section rests on unfetched Epicurious text alone.

---

## Summary

All four recipes: **keep**. No major findings; all proposed corrections are minor readability/specificity polish, none change ingredient identity or quantities. Readability: chipped-ham A; haluski B; pierogi B; primanti-style B. One access failure (Epicurious, tool-blocked), compensated via an identical cookbook-source republication (Lidia's Italy in America) and WebSearch snippets — flagged so the orchestrator can decide whether that corroboration is sufficient or a further attempt is warranted.
