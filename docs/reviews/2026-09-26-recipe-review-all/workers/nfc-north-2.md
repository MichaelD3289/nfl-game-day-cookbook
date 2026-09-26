# Worker nfc-north-2

Batch: 5 recipes (Packers x3, Vikings x2) + 1 exclusively assigned component
(`hotdish-cream-sauce`) + a usage-only check of `american-yellow-mustard`
(reviewed elsewhere) inside `beer-brats`.

Two of five recipe sources could not be read directly: `beer-brats`
(culinaryhill.com returned HTTP 403 on two attempts) and `chicken-booyah`
(archive.jsonline.com is blocked at the tool level, like web.archive.org).
Both are reported honestly below with what independent corroboration could
and could not establish; nothing was filled from memory. The other three
recipe sources and the component's source were fetched and read in full.

## beer-brats

- Path: `recipes/nfc/north/packers/beer-brats.md` · status: published
- Source: https://www.culinaryhill.com/wisconsin-beer-brats/ · checked 2026-09-26
- Hash: `5197707317e4251b315f1bc7b4244ff747d27315`

**City fit:** pass. Location Green Bay, WI. Beer brats are a well-documented
Wisconsin tradition (bratwurst poached in beer, grilled, served in a bun);
not city-specific but correctly framed as statewide/Packers-adjacent, which
matches how the rest of the book treats other statewide Wisconsin dishes.

**Authenticity — supported beer style established before brand advice:**
pass. The cited source itself could not be fetched, but independent search
corroboration (multiple secondary write-ups plus a search-engine summary
attributed to the Culinary Hill recipe) converges on: mild American
lagers/pilsners are the traditional poaching beer; heavily hopped (IPA),
dark, or strongly flavored beers are discouraged because they turn bitter or
overpowering when reduced during simmering. This establishes a supported
beer style — mild American lager — before assessing brand advice. The
file's ingredient line, "4 (12-ounce) cans mild American lager (for example
Miller High Life, Pabst Blue Ribbon or Leinenkugel Original); another
low-bitterness lager works," fits squarely within that established style.
Confidence: medium (style corroborated by multiple independent sources and
one AI-search summary citing the source; not read directly from the source
itself).

**Source fidelity:** partial/unconfirmed, honestly disclosed. Two direct
WebFetch attempts on culinaryhill.com both returned HTTP 403; this is a
genuine access failure, not a tool-level block. Corroboration via WebSearch
snippets independently matches this file's core structure and timing:
brats+onion+beer simmered "10 to 12 minutes" then grilled "about 5 minutes"
— both figures match this file's `cook: 10–12 min simmer + about 5 min
grill` exactly. One search summary explicitly states the Culinary Hill
recipe "keeps it simple" on toppings, in contrast with other Wisconsin
beer-brat recipes that serve the beer-braised onion itself as a bun topping
— this is consistent with our file's Step 3 (serves only ketchup, mustard,
sauerkraut; the poaching onion is not called back for serving), so the
apparent omission of onion-as-topping is not treated as a fidelity error,
only as a point I could not verify against the source's own text directly.
A separate AOL-published "Wisconsin-Style Beer Brats" article was checked
as a possible mirror of the same recipe but turned out to be a materially
different recipe (different ingredients, buns, mustard) — it was **not**
used as source verification, only as generic corroboration of the beer-style
guidance above.

**Specificity:** pass. Explicit can count (4), can size (12 oz), onion
prep, and named beer-brand examples are all appropriately specific.

**Ingredient specificity / components — `american-yellow-mustard` usage
check only** (component itself reviewed by another worker; not
re-reviewed here): the marker appears exactly once, correctly placed on the
"For serving" line — "Yellow or spicy brown mustard; ketchup only if
personally preferred `{{component:american-yellow-mustard}}`" — i.e. on the
finished/served condiment, not on a raw staple, with no double-counting
elsewhere in the file. No amount is given, which is correct for a
to-taste condiment. The `quick_options` entry ("Use French's Classic Yellow
or another plain American yellow mustard for the familiar ballpark
flavor.") is consistent with the component's own plain-yellow-mustard
content. No issues found with this recipe's usage of the component.

**Readability:** A. Quantities, order, and endpoints (160°F center on the
poach, "about 5 minutes" browned on the grill) are all clear and
unambiguous.

**Decision:** keep.

**Findings:** none requiring correction. No confirmed transcription errors
were found; the two items that could not be independently confirmed
(exact serving-step wording, and the Kitchen Note's claim that the source's
own recipe card lists a 30-minute total time) are listed below as
unverified rather than treated as errors.

**Replacement candidates:** none — no fidelity problem was found that would
justify replacing the source; the access failure is with reachability, not
with the source's suitability.

**Access failures / unverified claims:**
- culinaryhill.com/wisconsin-beer-brats/ returned HTTP 403 on two separate
  WebFetch attempts (initial + retry); **full source text was not read
  directly**. Assessment above relies on WebSearch snippet/summary
  corroboration only.
- The Kitchen Note "Source card says 30 minutes cook, allowing time for
  beer to boil and grill to heat" could not be confirmed or refuted against
  the actual source page; flagged as unverified, not as an error.
- Whether the source itself explicitly omits onion as a serving topping
  (versus this file's own editorial choice) is inferred only from a
  secondary AI-search summary, not from the source page itself; medium
  confidence at best.

## chicken-booyah

- Path: `recipes/nfc/north/packers/chicken-booyah.md` · status: published
- Source: https://archive.jsonline.com/features/recipes/115053789.html · checked 2026-09-26
- Hash: `6bfabd1ae5ddbdb555d7200a504c3ae6c5b0a8b2`

**City fit:** pass, strongly and independently corroborated. Booyah
(chicken booyah specifically) is a well-documented Green Bay/northeastern
Wisconsin stew tradition tracing to Walloon Belgian immigrants near Green
Bay/Brussels, WI (the "bouillon" → "booyah" transcription story from a 1906
Green Bay fundraiser recurs across multiple independent sources). Location
"Green Bay, WI" is an excellent city fit.

**Authenticity:** pass, independently corroborated. Multiple independent
recipes/histories converge on the same core: chicken and beef together (or
chicken alone for smaller batches), long two-stage simmer, and a vegetable
list of cabbage, celery, carrots, tomatoes, potatoes, corn, peas, and green
beans — this file's ingredient list matches that pattern closely. Several
independent sources also confirm that soy sauce and lemon juice, stirred in
near the end, are a real and traditional booyah flavoring, matching this
file's step 4.

**Source fidelity:** **unresolved — access failure.** WebFetch on
archive.jsonline.com returned an explicit tool-level block ("Claude Code is
unable to fetch from archive.jsonline.com"), analogous to the pre-known
web.archive.org block; this is not a 403, it cannot be retried around.
Follow-up attempts to find a mirror (a bigoven.com booyah recipe, and a
content.mpl.org digital-collection page) both returned unusable
navigation/placeholder content with no actual recipe text, so neither
could substitute for the source. **The cited source's exact text was never
read.** Everything above is independent corroboration of the dish in
general, not verification of this specific source's exact wording or
quantities.

**Specificity — one finding, moderate confidence:** several independent,
traditional booyah recipes/histories describe Worcestershire sauce added
alongside soy sauce and lemon juice near the end of cooking ("Just before
serving, lemon juice, soy sauce, and Worcestershire sauce are added...").
This file's step 4 adds lemon juice and soy sauce but no Worcestershire.
Because the actual cited source could not be read, I cannot tell whether
this is a real omission from the source or whether the source itself
simply doesn't call for Worcestershire (both are plausible — recipes for
this dish vary by family/publication). Flagged as a specificity finding
for the orchestrator to resolve if the source becomes reachable by another
route, not asserted as a confirmed error. The file's own honest
disclosures (bay leaves "as a practical starting point (source gives no
quantity...)") are good practice and not themselves findings.

**Components:** none. This recipe references no `{{component:}}` markers.

**Readability:** A. Quantities, order, and timing are clear throughout,
including explicit guidance on when to add quick-cooking vegetables (corn
and peas reserved for the final 20–30 minutes) and how to season
incrementally (salt in 1/4-teaspoon increments) at the end.

**Decision:** unresolved (access failure) for source fidelity; the dish's
authenticity and city fit are independently well supported and not in
question.

**Findings:**
1. Minor, moderate confidence — current: step 4 lists "lemon juice and soy
   sauce" near the end with no Worcestershire sauce — possible addition:
   Worcestershire sauce alongside the soy sauce and lemon juice, matching
   several independent booyah recipes/histories — rationale: multiple
   traditional sources pair all three; but the actual cited source was
   never read, so this cannot be confirmed as an omission rather than a
   legitimate source variation. Section: Instructions, step 4. Confidence:
   medium, contingent on someone reading the actual source.

**Replacement candidates:** if archive.jsonline.com remains permanently
unreachable by this tool, a credible alternative would be a Wisconsin
newspaper/food-history source that explicitly covers Green Bay chicken
booyah (e.g., a Green Bay Press-Gazette or Wisconsin Historical Society
piece), to restore direct source-fidelity checking. Not proposing this as
a required replacement — flagging it as an option for the orchestrator.

**Access failures / unverified claims:**
- archive.jsonline.com/features/recipes/115053789.html: tool-level block
  ("Claude Code is unable to fetch from archive.jsonline.com"). **Full
  source text was not read directly**, and could not be after two mirror
  attempts (bigoven.com, content.mpl.org) both returned unusable content.
- The Worcestershire-sauce question above is explicitly uncertain, not a
  confirmed omission.

## fried-wisconsin-cheese-curds

- Path: `recipes/nfc/north/packers/fried-wisconsin-cheese-curds.md` · status: published
- Source: https://www.foodnetwork.com/recipes/amanda-freitag/fried-cheese-curds-3168939 · checked 2026-09-26
- Hash: `c86c1906fca9faaf49c567124e5a03a6ff421bec`

**City fit:** pass. Green Bay, WI; fried Wisconsin cheddar cheese curds are
a definitive, well-documented Wisconsin bar/fair food, correctly framed.

**Authenticity:** pass. Batter-fried curds are the standard, authentic
preparation (versus breaded/deep-fried variants seen elsewhere); "fresh...
curds (white or yellow; cold, well drained)" correctly calls out that
fresh squeaky curds (not aged block cheddar) are required for the dish to
work.

**Source fidelity:** pass, verified against the full source text (fetched
directly). Batter (flour, baking powder, salt, club soda), curd quantity (1
pound), oil temperature (360°F), and fry time (about 1 minute, turning
halfway) all match the source closely. Kitchen Note's claim that the
source "explicitly lists 15 minutes active and total, including
setup/heating" was confirmed against the source's own listed timing.

**Specificity:** pass. Oil temperature, batter proportions, and curd
quantity are all explicit and specific; no vague terms.

**Components:** none linked; no shared component exists for the batter or
frying oil, and none is warranted (single-use, simple preparation).

**Readability:** A. Clear quantities, ordered steps, and explicit
temperature/time/visual endpoints (360°F, about 1 minute, golden, drain).

**Decision:** keep.

**Findings:** none requiring correction.

**Replacement candidates:** none — source is a strong, well-matched,
fully-verified authority for this dish.

**Access failures / unverified claims:** none. Full source text was read
directly.

## jucy-lucy-cheese-stuffed-burgers

- Path: `recipes/nfc/north/vikings/jucy-lucy-cheese-stuffed-burgers.md` · status: published
- Source: https://www.foodnetwork.com/recipes/food-network-kitchen/jucy-lucy-recipe-1973693 · checked 2026-09-26
- Hash: `1e3ae1865a60f91cb01bab9f017e082ab73dcc3b`

**City fit:** pass. Minneapolis, MN; the Jucy Lucy is a well-documented
Minneapolis bar-food specialty (Matt's Bar / the 5-8 Club origin dispute
notwithstanding, both are Minneapolis institutions), correctly located.

**Authenticity:** pass. Cheese sealed inside a double-patty with a crimped
edge, molten center, and the defining "let it stand/pierce with a
toothpick to release steam" caution are all present and correctly
represent the dish's signature technique — nothing about the defining
seal-and-melt technique was simplified away.

**Source fidelity:** pass, verified against the full source text (fetched
directly). Portioning (12 thin patties from 2 1/2 lb beef, folded cheese
square, crimped edges), onion browning (~10 minutes), and cook times (7–8
minutes then flip, pierce, ~7 more minutes) all match the source closely.
Two minor items, both editorial rather than transcription errors:
- The instruction to "let the burger stand a few minutes... because the
  cheese is very hot" (step 4) is repeated almost verbatim as "Rest the
  burgers a few minutes before eating because the cheese center is
  extremely hot" (step 5) — a redundant duplicate warning rather than a
  content error.
- Step 5's explicit "ground beef should reach 160°F" doneness check is not
  worded this way in the source; it reads as a reasonable food-safety
  addition consistent with USDA ground-beef guidance, not a literal
  transcription from the source. It should be understood as an editorial
  safety addition, not mis-attributed as sourced.

**Specificity:** pass. Beef fat percentage (80% lean chuck), cheese type
(American), pickle count (about three slices per bun), and bun type are
all appropriately specific.

**Components:** none linked; American cheese slices and pickles are
reasonably left as plain purchased items (no existing component matches,
and insufficient reuse elsewhere to justify one per check 5).

**Readability:** A. Quantities, order, and endpoints (7–8 min, flip,
~7 more min, 160°F) are all clear; the redundancy noted above is a
stylistic duplication, not an ambiguity that would confuse a cook.

**Decision:** targeted fix (minor, cosmetic).

**Findings:**
1. Minor — current: step 4 ends "...because the cheese is very hot" and
   step 5 restates "Rest the burgers a few minutes before eating because
   the cheese center is extremely hot" — proposed: remove the duplicate
   clause from one of the two steps (keep the food-safety/rest guidance
   once, e.g. fold it into step 5 only). Section: Instructions, steps 4–5.
   Confidence: high.
2. Minor — current: step 5's "160°F" doneness figure is stated as if
   directly sourced — proposed: no content change needed, but consider a
   brief Kitchen Note clarifying this is a standard food-safety addition
   rather than the source's own wording, for consistency with how other
   recipes in this batch label such additions. Section: Kitchen Notes
   (new). URL: https://www.foodnetwork.com/recipes/food-network-kitchen/jucy-lucy-recipe-1973693.
   Confidence: medium.

**Replacement candidates:** none — source is a strong, well-matched,
fully-verified authority for this dish.

**Access failures / unverified claims:** none. Full source text was read
directly.

## tater-tot-hotdish

- Path: `recipes/nfc/north/vikings/tater-tot-hotdish.md` · status: published
- Source: https://www.billstjohn.com/recipes/minnesota-tater-tot-hotdish · checked 2026-09-26
- Hash: `c7625257f4928199a6e51485ee5dfc298cb6361e`

**City fit:** pass. Minneapolis, MN; tater tot hotdish is Minnesota's
defining potluck/casserole dish, correctly located.

**Authenticity:** pass. Ground beef, condensed cream soup (or the linked
homemade cream sauce), mixed vegetables, cheddar, and a tater-tot topping
are exactly the traditional hotdish formula; nothing definitional was
simplified away.

**Source fidelity:** pass, with one clearly labeled and correctly-handled
deviation, verified against the full source text (fetched directly). Bake
temperature (375°F), bake time (45–50 minutes), and the overall
brown-meat/layer/top-with-tots structure all match the source. The source
itself splits the cheddar half-under and half-over the tots, while this
file places all of the cheddar beneath the tots; this is not an
unlabeled transcription error — the file's own Kitchen Notes explicitly
disclose and justify the change ("Keep cheese beneath the tots so the
frozen potato layer remains the exposed crisp topping"). Per the review
brief, a disclosed, in-file adaptation is correctly treated as an
intentional, labeled variation, not a fidelity finding.

**Specificity:** pass. Corn, peas, and cheddar amounts, tater tot count
range (60–70), and both the homemade-sauce and canned-soup paths are all
appropriately specific.

**Components:** one marker, correctly placed: `{{component:hotdish-cream-sauce}}`
appears once, inline with "1 batch homemade hotdish cream sauce (about 3
1/2 cups), or two 10–10.5-ounce cans condensed cream of mushroom soup,
undiluted" in `## Ingredients` — this is the finished sauce as used in the
dish, not a raw staple, and there is no double-counting (only one
occurrence). The `quick_options` entry matches the component's own
`quick_buy` text (both specify two 10–10.5 oz cans, undiluted). See the
`hotdish-cream-sauce` component section below for the component's own
review; a significant finding there (unsupported mushroom-variation and
yield claims) is a problem in the component file itself, not in how this
recipe consumes it — this recipe's own text ("about 3 1/2 cups") merely
echoes the component's stated yield and is consistent with it.

**Readability:** A. Quantities, order, and endpoints (375°F, 45–50
minutes, "bubbling at the sides," "tots are browned") are all clear.

**Decision:** keep.

**Findings:** none requiring correction in this recipe file itself (see
component section below for the one finding that applies to the linked
component).

**Replacement candidates:** none — source is a strong, well-matched,
fully-verified authority for this dish.

**Access failures / unverified claims:** none. Full source text was read
directly (two targeted fetches: one for the base recipe/method, one
specifically to check for a mushroom variation and stated yield, used for
the component review below).

## component:hotdish-cream-sauce

- Path: `components/sauces/hotdish-cream-sauce.md` · Source: https://www.modernfarmhouseeats.com/homemade-tater-tot-hotdish/ · checked 2026-09-26
- Hash: `0f2a0d76fc19103779276f22761b81012d934130`
- Consumers (via `grep -rl '{{component:hotdish-cream-sauce}}' recipes components`):
  `recipes/nfc/north/vikings/tater-tot-hotdish.md` only (reviewed above, in
  this batch).

**Assessment:** the base sauce (milk, flour, low-sodium chicken broth, soy
sauce, Worcestershire, salt, pepper, garlic/onion powder; whisk-then-thicken
method) was verified against the full source text (fetched directly, two
separate targeted fetches) and matches almost exactly. The source states
Worcestershire as "1/2 tablespoon," which is mathematically equivalent to
this component's "1 1/2 teaspoons" — not a discrepancy, just a different
unit. The "low-sodium" qualifier on the chicken broth is a minor,
unlabeled specificity addition not explicit in the source, but it is a
reasonable, non-substantive cook's clarification (a specific broth type
rather than a fabricated ingredient), so it is a low-severity note rather
than a finding requiring correction.

**Major finding — unsupported content presented as fact, not labeled as
estimated:** a targeted, direct fetch of the source page specifically
asking about a mushroom variation and the sauce's yield confirmed that
**neither exists in the source**. The only mushroom-related content
anywhere on the source page is an unrelated reader comment about leftover
mushroom *gravy* — there are no measured quantities for cremini mushrooms
or butter, and no mushroom variation of the cream sauce at all in the
source's own recipe or notes. Despite this, the component's "## Note"
section states as fact: "For mushroom flavor, sauté 8 ounces finely
chopped cremini mushrooms in 1 tablespoon butter until their liquid
evaporates; fold into the sauce. That variation adds about 10 minutes."
This reads as fabricated/invented content attributed to the source, and
unlike the adjacent, correctly-labeled "Allow about 10 minutes
(estimated)" base-timing note, the mushroom variation carries no
"(estimated)" or similar hedge at all.

Separately, the source gives **no yield figure** for the cream sauce
anywhere on the page, yet the component's front matter states `yield:
About 3 1/2 cups` as if it were a supported figure, again with no
"(estimated)" label. (The prior lead-only review in
`docs/reviews/2026-09-26-scratch-components.md` treated this yield as
already established/acceptable; that review's own brief says to treat
prior findings as leads only, not proof, and this closer read did not
corroborate the yield against the source.)

Both problems affect the same recipe consumer (tater-tot-hotdish), whose
own text ("1 batch homemade hotdish cream sauce (about 3 1/2 cups)")
merely echoes this unverified yield — so fixing the yield here is the
correct place to resolve it, not in the consuming recipe.

**Decision:** targeted fix.

**Findings:**
1. Major — current: "## Note" section states the cremini-mushroom/butter
   variation as unqualified fact — proposed: either remove the mushroom
   variation entirely (it is not in the source), or explicitly relabel it
   as an editorial/estimated addition not from the source (e.g., "As an
   unsourced variation, you can..."), matching how the base timing is
   already labeled "(estimated)." Section: Note. URL:
   https://www.modernfarmhouseeats.com/homemade-tater-tot-hotdish/.
   Confidence: high (confirmed via direct, targeted re-fetch of the full
   source page; only mushroom mention found was an unrelated reader
   comment about mushroom gravy).
2. Moderate — current: front matter `yield: About 3 1/2 cups` stated as
   fact — proposed: label explicitly as an editorial estimate (e.g.,
   "About 3 1/2 cups (estimated)"), since the source gives no yield figure
   at all. Section: front matter. URL: same as above. Confidence: high
   (confirmed absence via direct fetch).
3. Low — current: "2 cups low-sodium chicken broth" — the "low-sodium"
   qualifier is not explicit in the source. Not proposing a change (a
   reasonable, disclosed-by-nature cook's clarification, not a fabrication)
   — noted for completeness only. Section: Ingredients. Confidence: medium.

**Replacement candidates:** none — the source is otherwise a strong,
well-matched authority for the base sauce itself; only the Note's mushroom
addition and the yield claim need correction/labeling, not a source
replacement.

**Access failures / unverified claims:** none — full source text was read
directly across two separate targeted fetches (one for the base recipe,
one specifically targeting the mushroom-variation and yield questions).
