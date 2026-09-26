# Worker report — afc-north-2

Date checked: 2026-09-26. Scope: 4 recipes + 1 exclusive component (Baltimore
horseradish sauce). Access failures noted per recipe/component; none filled from memory.

## potato-and-cheese-pierogi

- Path: `recipes/afc/north/browns/potato-and-cheese-pierogi.md` · status: published
- Source: https://clevelandmagazine.com/articles/pierogi/ · hash: `e220bc915d54a8d21f24df826053be0f57a8877e`
- **City fit — pass.** Source is St. Andrew's Ukrainian Church (Parma, OH), a Cleveland
  metro suburb with a well-documented Slavic/Ukrainian population; `location: Cleveland, OH`
  is the valid metro-area framing per brief (suburb need not replace city identity).
- **Authenticity — pass.** Church-hall/community recipe, not a restaurant copycat;
  classic Cleveland-area Polish/Ukrainian pierogi (boiled, potato-cheese, butter finish).
  Defining traits (high-gluten dough, potato+Velveeta+American cheese filling, float-test
  doneness) all present.
- **Source fidelity — minor findings only.**
  - Finding (minor): source specifies "3 1/2 cups **Sapphire flour** (because of its high
    gluten percentage)"; our file drops the brand/rationale to plain "flour." Proposed:
    "3 1/2 cups high-gluten (bread) flour, such as Sapphire, or all-purpose in a pinch."
    Confidence: high (direct source quote).
  - Finding (minor): source assembly instruction reads "fold and pinch edges (**starting
    middle, working to edges**)"; our step drops that sealing technique. Proposed: append
    "starting at the center and working outward" to step 3. Confidence: high.
  - Finding (minor): source dough sequence is knead → rest 10 min → **divide** → roll;
    ours divides before the rest. Functionally minor, worth aligning order. Confidence: med.
  - Everything else (filling amounts, cheese amounts, salted-water float+3-min rule,
    melted-butter toss) matches verbatim. No access failure — full text was fetched.
- **Specificity.** "Idaho russet potatoes," Velveeta/American cheese blend, and white
  pepper are all appropriately concrete already; only the flour brand/type is under-specified
  (see above).
- **Components.** No existing component fits (this recipe *is* the from-scratch dish, no
  shared sub-recipe). No new component proposed — a pierogi dough/filling isn't reused
  elsewhere in the book.
- **Readability: A.** Ordered steps, measured amounts, observable endpoints (float, then
  3 more minutes; fork-tender potatoes). Kitchen Notes already flags batch/hand-shaping
  variance honestly.
- **Decision: keep**, with two small worded fixes (flour type/brand, sealing technique)
  the orchestrator can apply as a targeted fix if desired; neither is required for accuracy.
- No access failures.

## baltimore-crab-cakes

- Path: `recipes/afc/north/ravens/baltimore-crab-cakes.md` · status: published
- Source: https://www.mccormick.com/blogs/old-bay-recipes/chesapeake-old-bay-crab-cakes ·
  hash: `cd20e92ca1daeca0be2809c3f6b665fe05ed0760`
- **City fit — pass, regional-to-city.** Source frames the dish as Chesapeake/Maryland
  ("In Maryland, crab cakes are as familiar as bread and butter"), a state/regional
  identity Baltimore anchors most visibly: Faidley's Seafood at Lexington Market
  (est. 1886, jumbo-lump crab cakes since 1987 per Baltimore Magazine/Explore Baltimore
  Heritage) carries an official Baltimore historical marker ("It's a crab cake legacy,
  hon!"). Old Bay itself was created in Baltimore (1939, Gustav Brunn) — additional
  city-specific grounding beyond generic "Maryland." Worth citing Faidley's in a future
  city-fit note if the recipe is ever expanded.
- **Authenticity — pass.** Bread-binder + Old Bay + minimal filler, pan-fried, is the
  standard "Maryland-style" (light-binder, crab-forward) crab cake as opposed to
  breadcrumb-heavy "Boardwalk" style. No unsupported claims made.
- **Source fidelity — verified match, no findings.** Full source text fetched and
  compared line by line: bread/mayo/Old Bay/parsley/mustard/egg quantities, crab
  weight, oil amount, fry time (5 min/side), and mixing/shaping order all match exactly.
  One editorial addition beyond the source: "preferably Maryland blue crab" and "fresh"
  are not in the McCormick text (source just says "1 pound lump crabmeat"). This is
  reasonable regional specificity, not a fidelity error, but should be read as an
  editorial enhancement, not a source claim — flag severity minor. Source also offers a
  broiling alternative (10 min, turn once) that our recipe omits; not an error, just an
  unused option worth a one-line mention if space allows.
- **Specificity.** Old Bay, French's yellow mustard (with a fair generic-mustard
  alternative already included) are correctly specific. "Maryland blue crab" callout is
  accurate regional guidance (not claimed as brand-mandatory).
- **Components.** No purchased/scratch component applies; this is already the complete
  from-scratch preparation and nothing here is reused across other recipes.
- **Readability: A.** Four short, ordered steps with clear doneness cues (golden, cooked
  through) and a clear caution against oversaucing.
- **Decision: keep.** No corrections required; the one addition ("Maryland blue crab")
  is accurate and can stay, optionally re-labeled as recommended-not-sourced.
- No access failures — full source text fetched successfully.

## berger-cookies

- Path: `recipes/afc/north/ravens/berger-cookies.md` · status: published
- Source: https://sugarspunrun.com/copycat-berger-cookies-recipe/ ·
  hash: `ab6f8cb0713a8da07929f77be13ceb729ae0321b`
- **Access failure:** direct `WebFetch` of sugarspunrun.com returned HTTP 403 (twice,
  not a listed tool-level block but a page-level bot/403). Corroborated instead via two
  `WebSearch` passes that returned direct quoted snippets of the source's ingredient
  list and instructions (dampen-and-flatten technique, 350°F/10–12 min bake, double
  boiler frosting step, "about 1½ tablespoons" frosting on the flat side). This is
  search-snippet corroboration, not a full page read; residual risk is limited to
  wording/ordering outside the quoted snippets (e.g., exact prose between steps).
- **City fit — pass, strong.** Berger Cookies trace to George/Henry Berger's Fells Point
  bakery (Baltimore, 1835 immigration/founding lineage per Wikipedia/Smithsonian/Atlas
  Obscura), now made by DeBaufre Bakeries of Baltimore. Unambiguously city-identified.
  `location: Baltimore, MD` is correct.
  - **Note the recipe title/source frame this honestly as a "copycat,"** i.e. a home
    approximation of a proprietary bakery item, not DeBaufre's actual recipe. That is
    the correct classification (home adaptation/copycat of a real, named product), not
    "unsupported copycat" — the source explains its choices (cake flour for the
    authentic cakey crumb; imitation vanilla for flavor match) rather than asserting it
    is the bakery's formula. No claim of an exact Berger's/DeBaufre formula should be
    made or implied; current file makes no such claim.
  - Corroborating detail: an actual Berger cookie is reported at ~1.25 oz total, with
    the fudge frosting alone weighing about 1 oz (roughly 4x the under-cookie's weight),
    i.e. a very thick, dominant frosting layer — consistent with our recipe's "spread
    thickly," "1 1/2 tablespoons," per-cookie instruction.
- **Source fidelity — verified match via corroborated snippets, no findings.** Every
  ingredient amount in both the cookie and frosting sections matches the search-quoted
  source text exactly (butter, sugar, egg, milk, imitation vanilla, cake flour, baking
  powder, salt; frosting butter, corn syrup, powdered sugar, natural + Dutch cocoa,
  cream, vanilla). Bake temp/time, "dampen fingertips," "double boiler," and "1 1/2
  tablespoons" frosting amount are all confirmed. No omissions or additions found.
- **Specificity.** Cake flour (vs. all-purpose) and imitation (not pure) vanilla are
  correctly called out as the two features that most affect authenticity; both are used
  as the source intends, not simplified away.
- **Components.** No existing/candidate component — the fudge frosting is specific to
  this single recipe and not proposed for reuse elsewhere in this batch.
- **Readability: A.** Ordered, measured, with concrete endpoints (edges "begin to
  color," frosting "warm... stirring smooth," "let set before stacking").
- **Decision: keep.** Accurate transcription of a clearly labeled copycat/home-approximation
  recipe of a real, city-specific bakery item; no corrections needed.

## pit-beef-sandwiches

- Path: `recipes/afc/north/ravens/pit-beef-sandwiches.md` · status: published
- Source: https://www.washingtonpost.com/recipes/baltimore-pit-beef/ ·
  hash: `c9beedd8c947285d04a55e73a39b39da4dca5c68`
- **Access failure:** direct `WebFetch` of washingtonpost.com returned HTTP 403 twice
  (likely paywall/bot-gate, not in the pre-listed tool-blocked set but effectively
  unreachable). Corroborated via `WebSearch`, which returned direct quotes/paraphrase
  of the ingredient list and a named attribution.
- **City fit — pass, strong, with named local sourcing.** WaPo's recipe (Smoke Signals
  columnist Jim Shahin) is built around **Michael Shores of "Beef Barons,"** whose
  family "has been cooking pit beef at the Baltimore Farmers' Market & Bazaar for some
  30 years." That is a direct, named Baltimore vendor as the recipe's authenticity
  anchor — stronger city-fit evidence than a generic regional claim. Independent
  regional history (Wikipedia/Chaps Pit Beef "History of Maryland BBQ") corroborates
  pit beef as a Baltimore-specific tradition, especially the Pulaski Highway
  roadside-stand lineage from the 1970s.
- **Authenticity — pass, with a labeled adaptation.** Independent regional evidence
  (Chaps Pit Beef; Wikipedia "Pit beef") describes the traditional restaurant method as
  meat cooked **entirely over direct high-heat charcoal (~400–500°F)** the whole time,
  no rub/sauce on the meat itself, classically a **bottom round** cut. Our recipe (and
  its WaPo source) uses a **dry spice rub** (salt/pepper/garlic/chili powder) and a
  **sear-then-finish-indirect** method on an **eye round** — this is WaPo's own
  home-grill adaptation (explicitly recommended by Shores for home cooks per the
  search-quoted text), not a transcription error. The book should treat this as a
  supported home adaptation of a real vendor's method, not the literal
  direct-heat-throughout restaurant technique — worth a one-line "home-grill adaptation"
  note if the book wants to be precise, but not a required fix.
- **Source fidelity — largely verified, one unresolved gap.**
  - Verified exact matches (via search-quoted source text): rub (1 tsp kosher salt, 1
    tsp cracked black pepper, 1/2 tsp garlic powder, 1/2 tsp chili powder), **3-pound
    eye round**, "8 kaiser rolls (or potato rolls or 16 slices... white sandwich
    bread)," **1/2 cup** horseradish sauce, 1 large sweet onion sliced thin, "at least 4
    hours or overnight" refrigeration, and 6–8 servings. All match our file exactly.
  - **Unresolved/unverified:** the exact grill temperature, direct-sear duration,
    indirect-cook duration, target internal temperature, and post-cook rest time as
    literally written by WaPo could not be confirmed — the source page is blocked and
    search snippets on these specific figures returned either silence or unattributed
    third-party paraphrases (e.g., a "10–20 min sear, 30–45 min indirect, rest 5 min"
    figure that a search summary explicitly could not confirm as WaPo's own wording).
    Our file's "2–3 minutes per side... 30–45 minutes... about 130°F internal... rest no
    more than 5 minutes" is plausible (matches the general medium-rare range 125–130°F
    independently reported by Meatwave, a non-source comparison recipe) but is **not
    independently verified against the exact source text**. Flag as unresolved pending
    a direct read of the WaPo page.
- **Specificity.** "Eye round" (home-friendly, WaPo/Shores-recommended vs. the
  restaurant-classic bottom round), "kaiser rolls or potato rolls," and "Vidalia in
  season" sweet onion are all reasonable, correctly labeled as optional/seasonal.
- **Components.** Uses `{{component:baltimore-horseradish-sauce}}` correctly, on the
  finished sauce line in `## Ingredients` (not a raw ingredient), with a `quick_options`
  override to Tulkoff Tiger Horseradish Sauce. Quantity check: recipe calls for 1/2 cup
  sauce for 8 sandwiches; the component's own guidance ("use about 1 tablespoon per
  sandwich") × 8 = 1/2 cup — consistent, no double-counting or scaling mismatch.
- **Readability: A.** Ordered, measured, with an internal-temp target and a Kitchen
  Notes callout for the long lead time.
- **Decision: keep**, with the grill-timing/temperature figures logged as **unresolved**
  (not disproven — a targeted fix would only be warranted if a direct read of the WaPo
  source later contradicts the numbers; no contradiction found so far).

---

## component:baltimore-horseradish-sauce

- Path: `components/sauces/baltimore-horseradish-sauce.md` · status: published
- Source: https://barbecuebible.com/recipe/pit-beef-horseradish-sauce/ ·
  hash: `c3155ad82337abfa2553cdfe1823b0d8ab396e70`
- Consumers (via `grep -rl '{{component:baltimore-horseradish-sauce}}' recipes components`):
  only `recipes/afc/north/ravens/pit-beef-sandwiches.md` (reviewed above in this same
  batch; no other recipe or component reaches it).
- **Source fidelity — verified match, no findings.** Full source text fetched
  successfully (barbecuebible.com was not blocked). Source: "1 cup mayonnaise
  (preferably Hellmann's)," "½ cup freshly grated horseradish (or prepared)," "½
  teaspoon freshly grated lemon zest," "1 tablespoon fresh lemon juice," salt/pepper to
  taste; "Combine... and whisk to mix. Correct the seasoning..."; yield "1½ cups." This
  is Barbecue Bible / Project Fire (Steven Raichlen), explicitly captioned as "the basic
  horseradish sauce served at Baltimore's pit beef parlors" — a credible regional
  attribution, though the source itself doesn't cite a specific named stand (unlike the
  pit-beef recipe's Shores/Beef Barons attribution).
  - Finding (minor): our file adds "full-fat" to the mayonnaise line ("1 cup full-fat
    mayonnaise, preferably Hellmann's as recommended by the source"). The source says
    only "preferably Hellmann's," not "full-fat" — Hellmann's regular is full-fat by
    default, so this isn't contradicted, but it's an unsupported addition dressed as
    sourced fact ("as recommended by the source" applies to the brand, not the
    full-fat descriptor). Proposed: drop "full-fat" or rephrase as "1 cup mayonnaise,
    preferably Hellmann's (full-fat, as the source uses)" to avoid implying the source
    itself said "full-fat." Confidence: high. Severity: minor.
  - Finding (minor): "use about 1 tablespoon per sandwich" in the From Scratch step is
    not in the source (source gives no per-sandwich guidance) — it's a reasonable
    editorial derivation from the stated 1½-cup yield and the pit-beef recipe's 8-roll,
    1/2-cup usage, but should be understood as an editorial estimate, not a sourced
    amount. Already implicitly labeled by context; no change required, but the
    orchestrator may want an explicit "(estimated)" tag for consistency with the
    component's own "5 minutes active preparation (estimated)" labeling elsewhere.
  - Everything else — proportions, whisk-until-smooth method, "correct seasoning to
    taste" — matches verbatim.
- **Specificity — pass.** Component correctly distinguishes plain
  grated/prepared horseradish from creamy bottled horseradish sauce (a check-4
  requirement), and offers Tulkoff Tiger Horseradish Sauce as a named, regionally
  appropriate (Baltimore-made) purchased alternative.
- **Readability: A.** Two ordered steps, measured amounts, clear yield and per-use
  guidance.
- **Decision: keep**, with the two minor wording notes above available as an optional
  targeted fix (drop/rephrase "full-fat"; optionally label the per-sandwich amount as
  estimated). Neither is a source-fidelity error requiring replacement.
- No access failures for this file — full source text fetched successfully.

## Summary of access failures

- sugarspunrun.com (berger-cookies): HTTP 403 on direct fetch, twice. Worked around
  with WebSearch snippet corroboration covering the full ingredient list and the key
  technique steps (bake temp/time, dampen-and-flatten, double-boiler frosting, 1½ Tbsp
  application). No contradictions found; residual risk limited to unquoted prose.
- washingtonpost.com (pit-beef-sandwiches): HTTP 403 on direct fetch, twice. Worked
  around with WebSearch, which confirmed rub, cut/weight, rolls, onion, sauce quantity,
  refrigeration time, servings, and the Michael Shores/Beef Barons attribution
  word-for-word. **Unresolved:** the literal WaPo wording for direct-sear duration,
  indirect-cook duration, target internal temperature, and post-cook rest time was not
  independently confirmed; our file's figures are plausible and consistent with
  independent (non-source) comparison recipes but remain unverified against the exact
  source text.
- clevelandmagazine.com, mccormick.com, barbecuebible.com: fetched successfully in full;
  no access failures.
