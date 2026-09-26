# Worker report — nfc-south-3

Scope: `recipes/nfc/south/saints/{jambalaya,muffuletta-sandwich,red-beans-and-rice,shrimp-po-boy}.md`
plus exclusively assigned components `cajun-seasoning` and `louisiana-remoulade`.

## jambalaya

- Recipe ID: `jambalaya` · Path: `recipes/nfc/south/saints/jambalaya.md` · Status: published
- Source URL: https://www.neworleans.com/restaurants/traditional-new-orleans-foods/jambalaya/
- Date checked: 2026-09-26 · Input content hash: `88bf6da84ec5e0609bd1aa87d53774d0043f5e80`

**City fit** — Pass. Source is the official New Orleans tourism site, recipe attributed to
Chef Isaac Toups, chef/owner of Toups Meatery (New Orleans) and a published cookbook author.
Jambalaya is a defining New Orleans/Louisiana dish; direct city attribution, not just regional.

**Authenticity** — Pass, labeled variant. This is Cajun-style "brown" jambalaya (dark roux,
no tomato) as opposed to Creole "red" jambalaya (tomato-based) — both are legitimate New
Orleans-area traditions; the recipe correctly stays in the brown/roux lane throughout
(dark-chocolate roux, beer deglaze, chicken + andouille, no tomato product appears). Fully
attributed to a named local chef, not an anonymous copycat.

**Source fidelity** — Fetched the source three times (ingredient list/steps, timing fields,
and beer/roux step wording) and it fully verified: every ingredient quantity (2 tbsp + 1/2 cup
oil, 1 lb chicken, 1 lb andouille, 8 cloves garlic, 2 tsp salt, 2 tsp pepper, 1 tsp cayenne,
1/2 cup flour, 1 cup amber beer, 6 cups stock, 2 cups rice, 3 tbsp butter, 1/4 cup green
onions) and sequence (sear chicken → brown roux to dark chocolate → add trinity/garlic 1 min →
add beer 30 sec → add stock, return meat, simmer 1 hour covered → add rice, bake 30 min at
350°F → butter + scallions) match the source exactly. Source confirms "Time to Prep (mm): 20
minutes" and "Time to Cook (mm): 1 hour" as separate header fields, distinct from the 30-minute
bake after rice is added — so the file's own Kitchen Notes claim ("Source header lists 1 hour
cook but method includes another 30 minutes after adding rice") is **confirmed accurate**.
One low-confidence gap: the source's numbered steps as summarized to me don't show a
separate "brown the andouille" step distinct from searing chicken; our recipe adds "Brown
sliced andouille in the same pot for about 3–5 minutes" as its own step. This may simply be
lost in summarization rather than an actual addition — flagged as **minor/uncertain**, not a
confirmed finding, since I did not get raw page text.

**Specificity** — Pass. "Amber lager or amber ale (for example Abita Amber)" is a supported,
non-mandatory regional brand call-out (Abita Brewing, Abita Springs, LA), correctly hedged
with "for example."

**Components** — Not applicable. Jambalaya seasons meat directly with salt/pepper/cayenne per
its own source; this is a different, simpler blend than the `cajun-seasoning` component and
should not be replaced by it (would silently add garlic powder, onion powder, paprika, herbs,
cumin, etc. not in the source). No shared component under- or over-used here.

**Readability: B.** Ingredient amounts, sequence, temperatures (350°F oven, dark-chocolate
roux color cue, 165°F chicken doneness) and endpoints are all present and clear. The one
defect: Instruction step 4 embeds the editorial annotation about Abita/tourism-recipe caveat
mid-sentence, producing a garbled, confusing run-on (quoted below). That drags an otherwise-A
recipe down to B.

**Decision recommendation: targeted fix.**

**Findings:**
- Severity: major (readability). Current text (Instructions, step 4): "Stir in 1 cup amber
  lager or amber ale (for example Abita Amber); this beer-roux version is a New Orleans
  tourism recipe, not universal jambalaya technique for 30 seconds, then slowly add 6 cups
  low-sodium chicken stock while stirring." The annotation clause is spliced into the middle
  of the sentence, so "technique for 30 seconds" reads as one broken phrase. Proposed
  correction: move the annotation out of the instruction sentence entirely (it's already
  present in the Ingredients line and/or belongs in Kitchen Notes) and restore a clean
  instruction: "Stir in 1 cup amber lager or amber ale for 30 seconds, then slowly add 6 cups
  low-sodium chicken stock while stirring." Rationale: instructions must read as ordered,
  unambiguous actions per Check 3; the caveat is already stated once in the ingredient line, so
  repeating it verbatim inside the instruction is redundant as well as garbled. Confidence:
  high (direct comparison of file text against itself; no source dispute involved).
- Severity: minor/uncertain. The andouille-browning sub-step (step 2) was not visible in my
  fetch summary of the source's numbered steps. Could not confirm whether this is an
  editorial addition or just summarizer compression. Recommend the orchestrator do one more
  direct read of the source's raw instruction list before deciding whether to label it.

**Access failures:** None. `https://www.neworleans.com/...` was fetched successfully on all
three attempts; its full text (as summarized by the fetch tool) was used directly, not
supplemented from memory.

---

## muffuletta-sandwich

- Recipe ID: `muffuletta-sandwich` · Path: `recipes/nfc/south/saints/muffuletta-sandwich.md` · Status: published
- Source URL: https://www.saveur.com/article/Recipes/Muffuletta-Sandwich/
- Date checked: 2026-09-26 · Input content hash: `7eae4688cf0837c838f82a61cddcce8e02ac6b55`

**City fit** — Pass. Muffuletta is the defining New Orleans sandwich, invented at Central
Grocery on Decatur Street; Saveur's own copy attributes it to that origin. Direct city
identity, not merely regional.

**Authenticity** — Pass, standard build. Round sesame-seed Italian loaf, halved and hollowed,
layered with ham/salami/mortadella/provolone, dressed both sides with a marinated olive-and-
pickled-vegetable salad, wrapped and rested so the oil/brine soak into the bread — this matches
the accepted New Orleans muffuletta format (not a shortcut or copycat invention).

**Source fidelity** — **WebFetch to saveur.com returned HTTP 403 on the initial attempt and
again on one retry (transient-403 retry exhausted); the source was never read directly.**
Used WebSearch instead. Three independent search queries returned snippets that verbatim-quote
the source page's full ingredient list (cauliflower, olive oil, oregano, thyme, carrots, celery,
water, olives, roasted red peppers, banana peppers, red wine vinegar — all matching our file
exactly) and, critically, all three snippets independently describe the green olives as
**"chopped pitted green niçoise olives,"** not the "Spanish or Calabrese" our file states. This
is partial corroboration via search snippets, not a direct page read, but three independently
worded queries converging on the same phrase gives it reasonably high confidence. The meat and
cheese quantities (6 oz each of ham/salami/mortadella/provolone in our file) could not be
confirmed from any snippet — one search surfaced only a different site's 4 oz quantities for a
similar but not identical recipe — so those amounts remain **unverified**, not confirmed wrong.

**Specificity** — Finding (see below): the current text actively mis-describes the olive
variety used, working against specificity/accuracy rather than helping it.

**Components** — Checked `components/` (toppings, sides, sauces, dips, staples, seasonings);
no existing olive-salad or muffuletta-adjacent component exists.
`components/toppings/chicago-oil-packed-giardiniera.md` exists but is an explicitly different
Chicago giardiniera product (per assignment, not re-reviewed here). **Yes, a new component is
justified** under the "regional fidelity" criterion in Check 5 — the olive salad is the
sandwich's defining, non-generic element, worth a shared, correctly-sourced draft even though
it currently has one consumer. Proposed complete draft:

  - Proposed id: `new-orleans-olive-salad` (kind: `toppings`)
  - Ingredients (matches the recipe file's own olive-salad section, with the olive variety
    corrected to match the verified source): 1 1/4 cups coarsely chopped cauliflower florets;
    1/2 cup extra-virgin olive oil; 1/2 tsp dried oregano; 1/2 tsp dried thyme; 2 small carrots,
    roughly chopped; 2 small celery ribs, thinly sliced; 3 tbsp water; 3/4 cup chopped pitted
    green niçoise olives; 1/2 cup chopped pitted Kalamata olives; 1/2 cup chopped roasted red
    peppers; 1/4 cup drained sliced pickled banana peppers; 2 tbsp red wine vinegar; kosher
    salt and black pepper to taste.
  - Instructions: (1) Bring cauliflower, oil, oregano, thyme, carrots, celery and water to a
    boil in a 2-quart saucepan over medium-high heat; cover, lower heat, and simmer 10–12
    minutes until vegetables soften. (2) Transfer to a bowl; stir in both olives, roasted
    peppers, banana peppers and vinegar; taste before salting (olives are already salty); cool
    completely before use.
  - Yield: about 3 cups (editorial estimate from ingredient volumes) — enough to dress one
    whole muffuletta loaf (4 sandwiches), used half on the bottom half and half on top.
  - Timing (estimated, not kitchen-tested): about 10 minutes active + 10–12 minutes cook, plus
    cooling to room temperature (~30 min) before assembly; best made ahead and refrigerated.
  - Usage per recipe: entire batch (~3 cups) for one 8–10" loaf / 4 sandwiches.
  - Source: https://www.saveur.com/article/Recipes/Muffuletta-Sandwich/ (same source already
    cited by the recipe).
  - Purchased alternative: jarred Central Grocery Olive Salad (the sandwich's originator,
    ships nationally) or Boscoli Family Italian/Kalamata Olive Salad; drain excess oil if using
    a very wet jar product.

**Readability: A.** Quantities, ordered actions and clear endpoints (simmer 10–12 min until
vegetables soften; refrigerate 8 hours or overnight; cut into four wedges) are all present.
The olive-variety error is a fidelity/specificity problem, not a structural readability one.

**Decision recommendation: targeted fix.**

**Findings:**
- Severity: major. Current text (Ingredients): "3/4 cup chopped pitted briny green olives
  (such as Spanish or Calabrese; not specifically Niçoise)." Three independent WebSearch
  snippets of the cited source page state the ingredient as "chopped pitted green niçoise
  olives" — i.e., the source specifies niçoise and our file asserts the opposite. Proposed
  correction: "3/4 cup chopped pitted green niçoise olives." Rationale: this is a direct,
  repeated contradiction of the source's own stated ingredient, not a labeled adaptation.
  Canonical URL: https://www.saveur.com/article/Recipes/Muffuletta-Sandwich/. Recipe section:
  Ingredients > Olive salad. Confidence: medium-high (three independently worded search
  queries converged on identical wording; full page text still unread directly — see access
  failure below).
- Severity: minor/unverified. The 6 oz per-meat/cheese quantities could not be confirmed
  against the source from any available snippet. Not contradicted either. Flag as an open
  item for the orchestrator if a direct read becomes possible.

**Access failures:** `https://www.saveur.com/article/Recipes/Muffuletta-Sandwich/` returned
HTTP 403 on first attempt and on one retry — **the source's full text was never read
directly.** All source-fidelity conclusions above rely on WebSearch snippets as partial
corroboration only, per the explicit instruction not to treat inaccessible text as if read.

---

## red-beans-and-rice

- Recipe ID: `red-beans-and-rice` · Path: `recipes/nfc/south/saints/red-beans-and-rice.md` · Status: published
- Source URL: https://www.camelliabrand.com/recipes/camellias-famous-new-orleans-style-red-beans/
- Date checked: 2026-09-26 · Input content hash: `821ca5aaac9120a8e85f86157885adec956a5b2b`

**City fit** — Pass. Red beans and rice (traditionally a Monday dish) is a defining New
Orleans/Louisiana staple; Camellia Brand is itself a New Orleans-based red-bean company and a
widely cited authority for this exact dish.

**Authenticity** — Pass. Smoked sausage, trinity, garlic, bay leaf, long simmer to creamy
tenderness, served over white rice — matches the standard New Orleans preparation; no
shortcut or unsupported variant introduced.

**Source fidelity** — Fetched the source directly, twice, with targeted prompts. Findings:
the file's parenthetical "(source calls this '1 toe')" is **confirmed exactly correct** — the
source's ingredient line reads "1 toe garlic, chopped" verbatim (a regional dialect term for a
garlic clove). The file's cook-time note "(source lists 3 hours)" is **confirmed** — source
lists Prep 2 hours / Cook 3 hours / Total 5 hours (the 2-hour prep figure appears to bundle an
optional soak). The file's claim that "the source also permits unsoaked beans" is **confirmed**
— source states "(Optional: Soak beans using your preferred method.)," i.e., soaking is
explicitly optional, not required. The seasoning step wording ("Add Cajun seasoning plus salt
and pepper to taste," appearing after the 1–2 hour simmer) matches our step 5. One unconfirmed
addition: our step 4 instructs to "Mash a spoonful of beans against the pot wall to make the
liquid creamy" — my direct fetch of the source's instructions did not surface any mashing
step. This is a very common, near-universal red-beans-and-rice technique, but it is not
confirmed as coming from *this* cited source, so it should be labeled as an added technique
rather than left implying it is verbatim from the source.

**Specificity** — Pass. "Camellia red beans if available" and "smoked andouille sausage or
mild smoked pork sausage" both give a regional-style-first, generic-substitute structure
consistent with Check 4. The `quick_options` override for `cajun-seasoning` (Tony Chachere's /
Slap Ya Mama) is a supported, well-known bottled Louisiana-blend pairing.

**Components** — `{{component:cajun-seasoning}}` is used correctly on a finished-blend line
("Cajun seasoning, to taste... {{component:cajun-seasoning}}"), not on a raw spice, satisfying
Check 5's placement rule. No double-counting of seasoning or butter observed elsewhere in the
recipe.

**Readability: A.** Quantities, ordered steps, explicit timing (30 min boil, 1–2 hr simmer),
and an observable doneness/thickening endpoint (mash test) are all present and clear.

**Decision recommendation: targeted fix (minor).**

**Findings:**
- Severity: minor. Current text (Instructions, step 4): "Mash a spoonful of beans against the
  pot wall to make the liquid creamy." Proposed correction: label it explicitly, e.g. "Mash a
  spoonful of beans against the pot wall to make the liquid creamy (a common regional
  technique not spelled out in this source)." Rationale: Check 3 requires distinguishing an
  intentional/labeled adaptation from an unlabeled addition; this step is good practice but its
  attribution should not be left implicitly sourced. Canonical URL:
  https://www.camelliabrand.com/recipes/camellias-famous-new-orleans-style-red-beans/. Recipe
  section: Instructions, step 4. Confidence: medium (based on a summarized fetch, not raw HTML;
  the step could exist further down the page than my prompt captured).

**Access failures:** None. The source was fetched directly twice and its text (as summarized
by the fetch tool) was used for all conclusions above; nothing was filled from memory.

---

## shrimp-po-boy

- Recipe ID: `shrimp-po-boy` · Path: `recipes/nfc/south/saints/shrimp-po-boy.md` · Status: published
- Source URL: https://www.epicurious.com/recipes/food/views/shrimp-poboy-365820
- Date checked: 2026-09-26 · Input content hash: `2c1d22b24eab5cbdf746227f6963c6b197868180`

**City fit** — Pass. The po'boy is a defining New Orleans sandwich, per independent regional
food-history evidence (Martin Brothers' 1929 streetcar-strike origin story, New Orleans French
bread bakeries such as Leidenheimer Baking Company and the historical John Gendusa Bakery).
This is a direct city association, not a broader regional stretch.

**Authenticity** — Pass, accepted variant. Cornmeal/flour-dredged fried shrimp on New
Orleans-style French bread, "dressed" with shredded lettuce, tomato, and pickles, is the
standard po'boy build per independent regional food-history sources (which also describe
"dressed" specifically as lettuce/tomato/pickle/mayonnaise, commonly Blue Plate mayonnaise
locally). The recipe offers rémoulade as an alternative to plain mayonnaise and labels mayo as
"traditional too" — correctly presenting rémoulade as an accepted dressing variant rather than
overriding the classic.

**Source fidelity — ACCESS FAILURE, unresolved.** `https://www.epicurious.com/recipes/food/
views/shrimp-poboy-365820` is hard-blocked at the tool level ("unable to fetch from
www.epicurious.com"); no retry is possible. Two targeted WebSearch queries for this exact
recipe or a matching snippet returned no usable corroboration (no snippet quoting this specific
Epicurious page's ingredient list or steps was found). **The source's full text was not read,
directly or via corroborating snippet, at any point.** No ingredient, quantity, or step in this
file could be independently verified against its cited source. Nothing below is filled from
memory; the check is simply incomplete.

**Specificity** — Pass (on internal evidence, not source-verified). "4 eight-inch New
Orleans-style French rolls, light and crisp (ordinary soft French rolls if unavailable)"
correctly distinguishes the thin-crust/airy-crumb New Orleans French bread from generic French
bread, consistent with the independent bakery-history evidence above. "Hot pepper sauce,
optional, preferably Crystal" is a well-supported, non-mandatory regional brand call-out.

**Components** — `{{component:louisiana-remoulade}}` is used correctly on the finished
condiment line, with a sensible `quick_options` override (prepared Louisiana Fish Fry
Remoulade, or plain mayonnaise labeled as the traditional dressed-po'boy option). No new
component need identified; existing shared component already covers this well.

**Readability: A** (of this file's own text, independent of source verification). Quantities
are measured, steps are ordered (350°F oil, ~4 min per batch, "golden and cooked through" as a
doneness cue, then dress/assemble), and the alternative dressing is clearly labeled. This grade
describes internal clarity only — it does not imply the content was confirmed to match the
source, which it could not be.

**Decision recommendation: unresolved.** Checks 1, 2, 4 and 5 pass on strong independent
evidence; Check 3 (source fidelity) is a complete access failure with no possible substitute
verification found. Per the reviewer brief, this must not be treated as a pass by default.

**Findings:** None proposed — no discrepancy could be identified or ruled out, since the
source was never accessible in any form.

**Access failures:** `https://www.epicurious.com/recipes/food/views/shrimp-poboy-365820` — hard
tool-level block (pre-briefed domain), not a transient error, so no retry was attempted beyond
the initial failure. Two WebSearch queries for corroborating snippets returned no match. The
source's full text was **not** read directly and **no** corroboration was found — this is
recorded as an outright access failure, not a partial one.

---

## component:cajun-seasoning

- Path: `components/seasonings/cajun-seasoning.md` · Status: published
- Source URL: https://louisianacookin.com/cajun-spices-three-ways/
- Date checked: 2026-09-26 · Input content hash: `301a3fe9e4598b30f19b6ef5a97b7c2f5c89a24e`
- Consumers (via `grep -rl '{{component:cajun-seasoning}}' recipes components`):
  `recipes/nfc/south/saints/red-beans-and-rice.md`, `components/sauces/louisiana-remoulade.md`

Ingredients (garlic powder, onion powder, fine salt, Hungarian sweet paprika, black pepper,
oregano, thyme, cumin, dry mustard, celery seed, chipotle chile) match the cited source's
basic Cajun blend. The stated yield "about 2/3 cup (estimated from ingredient volumes)" is
independently verified by unit-conversion arithmetic: summing all listed teaspoon/tablespoon
volumes gives ≈30.5 tsp ≈ 0.635 cup, matching "about 2/3 cup" (positive evidence, not just
absence of error). The `## Note` correctly states this is Louisiana Cookin's basic blend and
that Cajun/Creole formulas vary regionally, avoiding an overclaim of a single "authentic"
formula. Usage guidance in `## From Scratch` (start at 1 tsp per pot of red beans, taste,
adjust in 1/2-tsp increments, account for sausage salt) is practical and consistent with how
`red-beans-and-rice.md` actually uses it.

**Decision recommendation: keep.**

**Access failures:** None; https://louisianacookin.com/cajun-spices-three-ways/ was fetched
directly and used for the ingredient-match conclusion above.

---

## component:louisiana-remoulade

- Path: `components/sauces/louisiana-remoulade.md` · Status: published
- Source URL: https://louisianacookin.com/fried-shrimp-mini-po-boys-with-lemon-remoulade/
- Date checked: 2026-09-26 · Input content hash: `112e167d992243bd5d85e6d7b2971ac1e9fdafe2`
- Consumers (via `grep -rl '{{component:louisiana-remoulade}}' recipes components`):
  `recipes/nfc/south/saints/shrimp-po-boy.md`

Ingredients (mayonnaise, Creole mustard "such as Zatarain's," lemon zest, lemon juice,
Louisiana cayenne hot sauce "preferably Crystal," and `{{component:cajun-seasoning}}") match
the cited lemon-rémoulade source, including the specific brand call-outs. The `## Note`
already explicitly discloses that "the linked Cajun blend is a home substitution for the
source's Creole seasoning" — this is the correctly labeled adaptation the prior review
(`docs/reviews/2026-09-26-scratch-components.md`) called for ("Cajun-for-Creole substitution
explicit"), and it is present and accurate in the current file. Yield "about 1 1/2 cups;
enough for four po'boys" is internally consistent with the recipe's stated 2–3 tbsp per roll
usage (4 rolls × ~2.5 tbsp ≈ 10 tbsp ≈ 0.6 cup used from a 1.5 cup batch, leaving reasonable
extra — plausible, not overstated). Refrigeration/use-within-3-days guidance is a sensible,
clearly labeled editorial addition for a mayonnaise-based sauce, not attributed to the source.

**Decision recommendation: keep.**

**Access failures:** None; the cited source was fetched directly for the prior review's
underlying research and the current file content is consistent with it; no new contradiction
found on this pass.
