# Worker report: afc-east-3 (Patriots)

Batch: boston-baked-beans, boston-cream-pie, lobster-rolls, new-england-clam-chowder.
No shared components assigned. Date checked: 2026-09-26.

## boston-baked-beans

- Path: `recipes/afc/east/patriots/boston-baked-beans.md` · status: published
- Source: https://americanhistory.si.edu/sites/default/files/file-uploader/CUH%20July%2013%202018%20Boston%20Baked%20Beans.pdf (Smithsonian NMAH, "Cooking Up History," Chef Brian Patterson demo, 2018-07-13)
- Input hash: `7f0c07bc5e1de0f32668d3eb71ce51363f86b603`

**City fit:** Pass. Source explicitly frames the dish as Boston's ("Bean Town") signature side, alongside hot dogs and lobster rolls. Strong direct-city evidence, not just regional.

**Authenticity:** Pass. Defining traits — dried white/navy beans, unsulfured molasses, salt pork, long slow bake, salt added only at the end, final uncovered stage to caramelize — all present and match the Smithsonian formula, a credible institutional source (National Museum of American History demo recipe) rather than a lifestyle-blog copycat.

**Source fidelity:** High. Verified against the full PDF text (fetched via WebFetch, which could not parse it as text; re-read the saved PDF with the Read tool to get the actual page content). Ingredient amounts, oven temp (300°F), bake time (~6 hr, checked every 45 min, uncovered final 50–60 min), and the "salt at the end" method all match verbatim. Minor, non-conflicting editorial additions found:
  - Ingredients "Optional: splash of cider vinegar" — source just says "a splash of vinegar," not cider vinegar specifically. Minor/severity minor, confidence medium; labeled as optional so low risk, but the varietal is the recipe's own addition, not sourced.
  - Instruction step 1 adds "Drain and rinse" — source says only "Drain in a colander and remove any debris." Rinsing after an overnight soak is standard practice but not stated by the source. Minor, confidence medium.
  - Instruction step 5 adds "Rest 10 minutes before serving" — source states the sauce thickens as it cools but gives no rest duration; this matches the recipe's own front-matter "(plus 10 minutes resting)," which is already labeled as an editorial addition in Kitchen Notes-adjacent metadata. Minor, confidence medium, should be understood as an estimate, not a sourced time.
  - Source also offers an optional aside (adding hot dogs/sausage to the pot during the uncovered stage) that the recipe reasonably omits as not core to the dish.

**Specificity:** Adequate. Beans (dried white/navy), unsulfured molasses, dry mustard, dark brown sugar, salt pork/bacon are all specific enough; no brand claims made or needed. Optional enhancement: could name an example unsulfured molasses brand (e.g., Grandma's Original or Crosby's) as a purchase pointer, but this is not required — generic term is already adequate per the skill's guidance.

**Components:** Checked existing `components/` (dips, proteins, sauces, seasonings, sides, staples, toppings) — none apply to a scratch bean bake. No component proposal; this dish is a from-scratch single unit with no purchased-shortcut ingredient worth converting.

**Readability:** A. Clear quantities, explicit oven temp, ordered steps, and endpoints (tender beans, thickened glaze, caramelized surface) all stated.

**Decision: keep.** Excellent, near-verbatim fidelity to a credible institutional source; only trivial, low-risk editorial additions (rinse step, cider vinegar type, 10-min rest) that don't contradict or undermine the source method.

**Findings (informational, no correction required):**
1. Minor — current "a splash of cider vinegar to finish" vs. source "a splash of vinegar to finish." No proposed change (harmless, optional garnish); flagged for transparency only. Confidence: medium. Source: PDF above, final paragraph.
2. Minor — "Drain and rinse" (step 1) vs. source's "Drain in a colander and remove any debris" only. No correction proposed (standard practice). Confidence: medium.

**Access failures:** WebFetch's HTML-conversion path failed to parse the PDF as text (returned only "encoded font and structural data"); recovered by re-reading the same downloaded PDF binary directly with the Read tool, which extracted the full two-page recipe text successfully. No unresolved access failure.

---

## boston-cream-pie

- Path: `recipes/afc/east/patriots/boston-cream-pie.md` · status: published
- Source: https://www.kingarthurbaking.com/recipes/boston-cream-pie-recipe
- Input hash: `64f29f86641da8d6836fca8bb7471991423ebe97`

**City fit:** Pass, and stronger than the recipe's own sourcing shows. Boston Cream Pie was created at Boston's Parker House hotel (Omni Parker House) in 1856, originally "Parker House Chocolate Cream Pie," and is Massachusetts's official state dessert. (Corroborated via WebSearch: Omni/Historic Hotels of America, Tasting Table, Fifty Plus Advocate — consistent independent accounts, though sources differ on whether chef Sanzian or Anezin gets original credit.) This is direct city-of-origin evidence, not just regional adoption.

**Authenticity:** Pass. Defining traits — two-layer sponge/butter cake, pastry cream filling, chocolate glaze (not frosting) — all present, matching the accepted modern formula for the dish (the original 1856 version reportedly had no glaze at all; today's chocolate-glazed version, as used here, is the long-established standard, not an invented variant).

**Source fidelity:** Good, with a few minor gaps against the exact King Arthur text (fetched directly; also re-fetched for verbatim quotes on ambiguous steps):
- **Finding (minor):** Step 2 says "Heat the 1 cup cake milk with 4 tablespoons butter **until steaming**." Source: "In a saucepan set over medium heat, bring the butter and milk **just to a boil**." Steaming implies a lower endpoint than a full boil. Proposed correction: "until it just comes to a boil." Confidence: high (verbatim source quote). Section: Instructions step 2.
- **Finding (minor):** Step 3 gives only a time range, "bake 30 to 35 minutes," and omits the source's doneness test. Source: "Bake the cakes for 30 to 35 minutes, **until a toothpick inserted into the center comes out clean**." Proposed correction: append the toothpick test. Confidence: high. Section: Instructions step 3.
- **Finding (minor):** Both the cake and filling ingredient lists say "milk"; source specifies "**whole milk**" in both places (cake: 1 cup whole milk; filling: 2 1/2 cups whole milk). Proposed correction: specify "whole milk" in both lists (fat content affects pastry-cream body). Confidence: high. Section: Ingredients (Cake, Filling).
- **Finding (minor, specificity not fidelity):** Glaze ingredient reads "1/3 cup chopped dark or semisweet chocolate." Source offers three interchangeable forms: "dark chocolate, chocolate chips, or semisweet chocolate wafers, chopped." Proposed addition: note that chocolate chips work as a pantry-friendly substitute, e.g. "dark or semisweet chocolate (bar, wafers, or chips), chopped." Confidence: high.
- Everything else checked cleanly against source: all quantities (sugar, eggs, oil, flour, salt, baking powder, butter, vanilla in all three components; cornstarch, egg yolks/whole egg; heavy cream), pan size/prep, cooling times, tempering method, "cook 2 minutes" for pastry cream, and total time (5 hr 10 min, already correctly noted as source-listed in Kitchen Notes).

**Specificity:** Adequate; ingredients are already generic-appropriate (granulated sugar, AP flour, vanilla extract, dark/semisweet chocolate). No misleading brand claims present.

**Components:** Checked `components/` — no existing pastry-cream, cake, or ganache/glaze component exists, and none of the sub-recipes here (cake, pastry cream, chocolate glaze) are reused by any other recipe in this batch or visible elsewhere in `components/`, so no proposal; each remains a recipe-specific scratch sub-preparation as intended.

**Readability:** B. Quantities and sequence are clear and mostly complete, but the missing doneness test (toothpick) and the softened "steaming" vs. sourced "just to a boil" step both leave small actionable gaps a home cook would otherwise have to guess at.

**Decision: targeted fix.** Apply the four minor corrections above (boil endpoint, doneness test, whole milk, chocolate-chip alternative); nothing here rises to a replace-source or authenticity problem.

**Access failures:** None; both the original fetch and a follow-up verbatim-quote fetch of kingarthurbaking.com succeeded.

---

## lobster-rolls

- Path: `recipes/afc/east/patriots/lobster-rolls.md` · status: published
- Source: https://www.thekitchn.com/lobster-roll-recipe-23733104
- Input hash: `bc6873ce47c6dc423bb742e77a7cba655e769fff`

**City fit:** Pass (broader New England regional dish, well-established in Boston specifically, not just claimed). Lobster rolls originated with early-20th-century New England fishermen/roadside stands (strongest historical roots in Maine/Connecticut), but Boston has a long-standing, well-documented lobster-roll identity of its own: Boston chef Jasper White is widely credited with popularizing dressed-up lobster rolls in the 1980s at his Boston waterfront restaurant, and long-running Boston institutions (Union Oyster House, Neptune Oyster, James Hook & Co.) are frequently cited "best lobster roll in Boston" destinations. (WebSearch corroboration: Bites of Boston Food Tours, Meg Anstalk-style local guides, National Geographic Boston travel piece.) The recipe's own photo credit, Boston.com, is itself a Boston-local outlet. This is a supported broader-regional dish with genuine local Boston presence, per AGENTS.md's allowance that stadium-suburb identity doesn't override the book's established city.

**Authenticity:** Pass. The style used — cold lobster meat, lightly dressed with mayonnaise (not drawn butter), on a buttered, griddle-toasted split-top New England hot dog bun — is the classic "Maine-style"/New England cold lobster roll, the dominant and most widely recognized version (as opposed to the warm-butter-only Connecticut style). The Kitchn's own recipe title is "Lobster Roll Recipe (Maine Style!)" per search indexing, consistent with the technique used here.

**Source fidelity: partially verified — access failure on the primary source.** Direct WebFetch of thekitchn.com returned **HTTP 403 Forbidden**. Per the web-notes instruction, tried a legitimate alternative: a web.archive.org snapshot of the exact URL. That request was refused at the tool level ("Claude Code is unable to fetch from web.archive.org") rather than returning page content, so no archived HTML could be retrieved either. As a fallback I used WebSearch (two independent queries) to recover a search-engine synthesis of the page's content — this is corroborating evidence, not a verbatim page read, and is recorded as such:
- Confirmed matching (via WebSearch synthesis, consistent across two separate queries): dressing = 1/4 cup mayonnaise + 2 finely chopped medium celery stalks + 2 tbsp finely chopped fresh chives + 1 tbsp lemon juice + 1/4 tsp kosher salt; 1 pound fresh-or-thawed lobster meat, patted dry, cut into bite-size pieces; 4 split-top hot dog buns spread with 2 tbsp room-temperature unsalted butter, toasted in a skillet ~3 minutes per side until golden-brown; one Bibb lettuce leaf per bun, described as "optional but recommended" (matches the recipe's own "optional" labeling).
- **Unresolved/unverified (flag, do not silently correct):** whether the source itself marks chives as "optional" (our recipe does; search synthesis did not confirm or deny this), whether the source specifies "Maine" lobster meat by name (our recipe says "Maine lobster meat," search synthesis just said "lobster meat"), and whether lemon wedges are a sourced serving suggestion or an added garnish. None of these are contradicted by what could be recovered — they're simply short of full verification. Recommend the orchestrator attempt an authenticated/browser-based fetch of the exact URL before treating these as settled.

**Specificity:** Good. "Maine lobster meat" and "New England split-top hot dog buns" are both regionally specific already. Optional, non-mandatory enhancement: could name a widely available split-top bun brand (e.g., Martin's Famous Potato Rolls "Sandwich Potato Rolls" or a regional New England-style hot dog roll) as a purchase pointer for cooks outside New England, but the current generic description is already adequate.

**Components:** Checked `components/` (dips, sauces, toppings, etc.) — no existing mayo-based seafood dressing component, and this dressing isn't reused elsewhere in the cookbook, so no proposal. Per the skill's guidance, the raw mayonnaise itself is not a component candidate.

**Readability:** A. Quantities, order, and endpoints (golden-brown, ~3 min per side) are all clear and complete.

**Decision: keep, with one unresolved item.** Everything independently confirmable matches the source; the chives-optional/"-Maine"-naming/lemon-wedge details are unverified due to the access failure above rather than known to be wrong, so no fix is proposed — flagging as unresolved rather than either a pass or a correction.

**Access failures:** thekitchn.com direct fetch = 403 Forbidden (both initial and retry). web.archive.org fetch of the same URL was blocked at the tool level, not merely unavailable. Used WebSearch synthesis as a partial substitute; treated its content as evidence only where corroborated across independent queries, per instructions never to fill gaps from memory.

---

## new-england-clam-chowder

- Path: `recipes/afc/east/patriots/new-england-clam-chowder.md` · status: published
- Source: https://newengland.com/food/fish-seafood/massachusetts-new-england-clam-chowder/ (Yankee Magazine / New England.com)
- Input hash: `92c7408119547bcc3045213094e5d6ef5efbfe69`

**City fit:** Pass. Source's own URL slug and framing is "Massachusetts New England Clam Chowder," published by Yankee/New England.com, a regional publication with direct Massachusetts/Boston-area authority. Direct city/state-level evidence, not merely regional inference.

**Authenticity:** Pass. Defining traits present and correct: cream-based (not tomato-based Manhattan-style) chowder, salt-pork/bacon-rendered fat base, roux (flour) thickener, potatoes, hard-shell clams (quahogs), light cream finished gently off strong heat to avoid breaking. This is the standard, widely credible New England style, not an elaborated or simplified copycat.

**Source fidelity:** Excellent — essentially a faithful, near line-by-line transcription of the source (fetched directly, full success). All ingredient quantities match exactly: 3 strips thick-cut bacon; 1/4 cup unsalted butter; 1 large onion; 1 celery rib (optional); 1 tsp fresh thyme (optional); 2 bay leaves (optional); 2 medium white potatoes; 1/2 cup AP flour; 4 cups bottled clam juice; 1 pound clam meat with juices; kosher salt to taste; 3 cups light cream; 1 tsp white pepper. All step timings match: bacon 10–12 min, onion/celery 6–8 min, potatoes boiled separately 5–8 min, flour cooked 3 min, clams/potatoes simmered ~5 min. One minor labeling note (not a content error):
- **Finding (minor, metadata only):** Front matter lists `prep: 45 minutes hands-on` and `cook: 1 hour 15 minutes total`. The source page shows these as **"Hands-on Time: 45 minutes"** and **"Total Time: 1 hour 15 minutes"** — i.e., the source's "Total Time" already *includes* the 45 minutes of hands-on work; it is not an additional cook-only duration on top of prep. Labeling the 1h15m figure as "cook" beside a separate 45-min "prep" reads as if the whole recipe takes ~2 hours, roughly double the source's actual total. Proposed correction: relabel front matter, e.g. `prep: 45 minutes hands-on` / `cook: 1 hour 15 minutes total (source's overall total, not additional to prep)`, or simply present total time as 1h15m without implying additive stacking. Confidence: high (verified via direct re-fetch of the source's time fields). Section: front matter `prep`/`cook`.

**Specificity:** Good, and already better than the bare source in one respect: recipe specifies "hard-shell clam meat, such as quahogs" where the source just says "chopped fresh clam meat" — an accurate, non-fabricated regional clarification (quahogs are the standard New England chowder clam). Recipe also adds "(18–20% milk fat; half-and-half is a lighter substitute)" for light cream — a generically accurate culinary definition, not sourced verbatim from the page, but not contradicted by it either; worth understanding as an editorial clarification rather than a source-verified fact. No brand claims made.

**Components:** Checked `components/` — no bacon/chowder-base component exists or is warranted; this is a single self-contained main dish with no purchased-shortcut ingredient worth converting to a reusable scratch component.

**Readability:** A. Clear quantities, explicit temperatures/heat levels, ordered steps, and doneness endpoints (crisp, translucent, tender, clams tender) throughout.

**Decision: targeted fix (metadata only).** Content/method fidelity is excellent and needs no recipe-body change; only the prep/cook time-labeling ambiguity above should be corrected so the printed time doesn't overstate total duration.

**Access failures:** None; source fetched directly and successfully on both the initial full-recipe fetch and a follow-up fetch to confirm the exact time-field wording.

---

## Summary

| Recipe | Decision | Readability | Notes |
|---|---|---|---|
| boston-baked-beans | keep | A | Near-verbatim to Smithsonian source; only trivial, low-risk editorial adds |
| boston-cream-pie | targeted fix | B | 4 minor corrections: boil endpoint, toothpick test, whole milk, chocolate-chip alternative |
| lobster-rolls | keep (1 unresolved) | A | thekitchn.com 403; archive.org blocked at tool level; WebSearch synthesis corroborates core recipe but leaves chives-optional/"Maine"-naming/lemon-wedge details unverified |
| new-england-clam-chowder | targeted fix (metadata only) | A | Content matches source exactly; prep/cook time labels overstate total vs. source's inclusive "Total Time" |

No component proposals from this batch. No recipe, component, metadata, or other project file was edited.
