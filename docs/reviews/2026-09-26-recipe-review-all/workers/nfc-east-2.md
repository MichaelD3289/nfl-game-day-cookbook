# Worker batch: nfc-east-2

Date checked: 2026-09-26. No shared components assigned. `components/` searched
(21 components across dips/proteins/sauces/seasonings/sides/staples/toppings) —
none match roast pork, broccoli rabe, provolone, pastrami, pizza dough/sauce, or
cookie icing. Cross-repo grep confirms "roast pork" also appears in
`recipes/afc/east/dolphins/cuban-sandwich.md` and `components/proteins/cuban-mojo-pork.md`,
but that is a mojo-marinated Cuban roast pork (different cut prep, seasoning and
serving style) — not a viable shared component with Philly braised pork. Pastrami
and NY-style pizza each have a second recipe (Jets) reviewed independently in
`workers/afc-east-2.md` with different sources; no forced merge attempted here.

---

## roast-pork-sandwich

- Path: `recipes/nfc/east/eagles/roast-pork-sandwich.md` | status: published
- Source: https://www.seriouseats.com/philly-roast-pork-sandwich-recipe-8605326
- Hash: `93898c338f778fdd5cc9cbe2e10333e1225c4cc3`

**City fit — pass.** Philadelphia roast pork is a defining local sandwich
(John's Roast Pork, Tommy DiNic's/Reading Terminal Market, Tony Luke's), well
documented by independent food journalism (sandwichtribunal.com, Pat Willard's
food-history substack).

**Authenticity — pass, with a variant note.** Defining traits confirmed
independently: thin-sliced roast pork reheated in its own broth/jus, broccoli
rabe (Tony Luke's-style; John's original used spinach — both are recognized
variants, so our broccoli-rabe version is a supported variant, not a copycat
error), sharp provolone, optional long hot peppers, crusty Italian roll. Our
recipe matches this baseline (braise, chill, slice thin, reheat in jus, broccoli
rabe, long hots, provolone, Italian roll).

**Source fidelity — largely unresolved (source blocked).** WebFetch to
seriouseats.com is tool-blocked (same class as the pre-flagged allrecipes.com/
web.archive.org blocks). A WebSearch snippet gives a near-verbatim partial match
("1 1/4 pounds of broccoli rabe trimmed and cut into 1-inch pieces"), and the
recipe's internal timing math (15 min prep + 3h5m cook + 13h chill = 16h20m
total, stated in Kitchen Notes) is internally consistent. Cannot verify exact
quantities/steps line-by-line beyond this partial corroboration.

**Specificity — finding.** Independent regional sources (sandwichtribunal.com,
cookwell.com) consistently identify **sharp** provolone, not mild, as the
traditional cheese; our ingredient list just says "provolone cheese."

**Components — no new proposal.** Roast pork and broccoli rabe are single-use
in this cookbook and already scratch-cooked (not a purchased shortcut needing a
buy/make split); the only other "roast pork" hit (Cuban mojo pork) is a
different regional dish and technique, so merging would blur both.

**Readability — B.** Quantities, temperatures (325°F, 180°F, 400°F) and time
ranges are all present and ordered; the one gap is that prep/cook front-matter
fields omit the 13-hour chill (Kitchen Notes catches this, but a reader scanning
only the header could under-plan).

**Decision: targeted fix.**

Findings:
1. **Minor — specificity.** Current: "12 to 18 thin slices provolone cheese."
   Proposed: "12 to 18 thin slices sharp provolone cheese." Rationale: sharp
   provolone is the consistently cited traditional choice in independent Philly
   sandwich sources; mild provolone is not typically used. URL:
   https://www.sandwichtribunal.com/2024/12/skip-the-cheesesteak-philadelphias-roast-pork-sandwich/
   Section: Ingredients > Sandwiches. Confidence: medium-high (independent
   sources agree; not confirmed against the primary source itself).
2. **Minor — metadata consistency.** Current: `photo_credit: www.bonappetit.com`
   while `source.url` is seriouseats.com. Rationale: photo and recipe source
   are on different domains with no note explaining the split; may be
   intentional (separate photo credit) but should be confirmed, not assumed.
   Section: front matter. Confidence: low (could be legitimate).

Replacement candidates: none proposed — no material defect found, only a
specificity upgrade and an unresolved verification gap.

**Access failures:** `www.seriouseats.com` is tool-blocked (both direct
WebFetch attempts failed: "unable to fetch from www.seriouseats.com"); a
secondary attempt via punchfork.com's mirror also failed (socket hang up,
network-level, not a content block). Ingredient quantities/steps beyond the
one WebSearch snippet remain unverified against the primary source.

---

## water-ice

- Path: `recipes/nfc/east/eagles/water-ice.md` | status: published
- Source: https://soufflebombay.com/diy-philadelphia-style-lime-water-ice/
- Hash: `c5fcb2c3903224b08fc2eb305235867d906472c4`

**City fit — pass.** Philadelphia water ice ("wooder ice") is a defining local
treat (Rita's, John's Water Ice, Pop's), independently traced to southern
Italian immigrant granita traditions (patwillard.substack.com).

**Authenticity — pass, home-adaptation classification.** Source is a home
cook's blog reproduction of shop-style water ice, not an original historic shop
recipe — this is honestly reflected in the source's own title ("DIY ... Water
Ice") and should be treated as an accepted home adaptation of the shop style,
not a specific shop's proprietary formula. Lime is a standard, widely used
water-ice flavor; nothing contradicts it.

**Source fidelity — finding (minor).** Source fetched in full. Ingredient
quantities match exactly (4 1/2 cups water, 1 cup sugar, 1–2 tsp lime extract,
4–5 drops food coloring). Instructions match for syrup and churn steps, but our
step 3 compresses the source's three-part sequence (churn → transfer and
**freeze** → thaw/soften before serving) into "transfer to jars ... allow it to
soften ... before serving," dropping the explicit freeze step in between. A
reader could plausibly serve it straight from the churner without the
freeze/re-soften cycle the source describes.

**Specificity — minor finding.** Source recommends The Spice House brand for
the lime extract; our recipe generalizes to "concentrated lime extract" with no
brand mentioned. Not required, but a useful optional pointer.

**Components — no new proposal.** Single-use, fully scratch, no purchased
component to split out.

**Readability — B.** Clear quantities and an explicit doneness cue for the
syrup ("clear"), but the storage/freeze step is compressed enough to create
minor ambiguity about whether freezing is required before serving.

**Decision: targeted fix.**

Findings:
1. **Minor — omitted step.** Current: "Pour into a chilled ice-cream-maker
   bowl and churn until slushy, about 20–25 minutes. To store, transfer to
   jars or another container; allow it to soften to a slushy texture and stir
   before serving." Proposed: split into (a) churn 20–25 min until slushy;
   (b) transfer to jars and **freeze** (do not leave in the ice cream maker, it
   will harden); (c) before serving, let soften/thaw to a slushy texture and
   stir. Rationale: source explicitly separates freezing from the pre-serving
   thaw; as written, our step could be read as one continuous action. URL:
   https://soufflebombay.com/diy-philadelphia-style-lime-water-ice/ Section:
   Instructions, step 3. Confidence: high (source fetched in full).
2. **Minor — specificity.** Current: "concentrated lime extract." Proposed:
   optionally note "(The Spice House brand recommended by the source)" as an
   optional brand pointer. Section: Ingredients. Confidence: high.

Replacement candidates: none — source is fully accessible and sound; only
completeness/specificity gaps.

**Access failures:** none. Source fetched successfully in full.

---

## black-and-white-cookies

- Path: `recipes/nfc/east/giants/black-and-white-cookies.md` | status: published
- Source: https://www.kingarthurbaking.com/recipes/black-and-white-cookies-recipe
- Hash: `ef75e5d8e94f4f534efeea416296c5bdc4de4f14`

**City fit — pass.** Source's own headnote frames this as a NYC deli/corner-
bakery staple; independently corroborated (Ess-a-Bagel, William Greenberg
Desserts) as a defining NYC classic.

**Authenticity — pass.** King Arthur is a reputable test-kitchen source
reproducing the generic NYC deli cookie (soft, cake-like, half vanilla/half
chocolate fondant-style icing); it is not presented as a specific named
bakery's proprietary recipe, and neither is ours, so no overclaim exists.

**Source fidelity — finding (minor, internal inconsistency).** Ingredients
match the source exactly (butter, sugar, salt, baking powder, lemon oil/zest,
vanilla, eggs, flour, milk; both icings match quantities exactly). Instructions
match, including the source's own doneness guidance (10 min = moist, 12 min =
drier/"more authentic," 11 min = in between). However, front matter states
`cook: 11 to 12 minutes bake`, narrowing the range, while the recipe body
correctly says "Bake 10 to 12 minutes" — the two disagree with each other and
the front matter also disagrees with the source's actual 10–12 minute range.

**Specificity — pass.** Ingredient specificity already mirrors the source
closely (lemon oil or zest, optional espresso powder, semisweet/bittersweet
chips); no unsupported brand claims present.

**Components — no new proposal.** Vanilla/chocolate icing is single-use in
this cookbook (grep confirms no other recipe references "chocolate icing" or
"vanilla icing"); not a repeated-use candidate.

**Readability — B.** Instructions themselves are clear and ordered with
explicit endpoints ("until set," "~30 minutes to set"), but the front-matter/
body cook-time conflict is a metadata contradiction that could mislead time
planning.

**Decision: targeted fix.**

Findings:
1. **Minor — internal inconsistency.** Current front matter: `cook: 11 to 12
   minutes bake; about 1 hour 11 minutes total`. Body: "Bake 10 to 12 minutes
   until set." Proposed: align front matter to "10 to 12 minutes bake" (matching
   both the body and the source's stated range) and recompute total time
   accordingly. Rationale: source states 10–12 min with explicit meaning at
   each end (10 = moist, 12 = drier); narrowing to "11 to 12" in front matter
   isn't supported and contradicts the recipe's own instructions. URL:
   https://www.kingarthurbaking.com/recipes/black-and-white-cookies-recipe
   Section: front matter `cook`. Confidence: high.
2. **Minor — dropped detail.** Current: "flatten to about 3 inches, leaving
   space between." Source specifies flattened rounds spaced 2–2.5 inches apart.
   Proposed: state the spacing explicitly. Section: Instructions, step 2.
   Confidence: high.

Replacement candidates: none — source is sound and fully accessible.

**Access failures:** none. Source fetched successfully in full.

---

## new-york-style-pizza

- Path: `recipes/nfc/east/giants/new-york-style-pizza.md` | status: published
- Source: https://www.foodnetwork.com/recipes/food-network-kitchen/new-yorkstyle-cheese-pizza-10066512
- Hash: `6fea7d9045a8cc64c1c13a53c86191716cc24935`

**City fit — pass.** NY-style pizza (thin, foldable, high-heat baked) is a
defining NYC food; independently well documented.

**Authenticity — pass, variant classification noted.** Source's own headnote
frames this as evoking "the classic slice joint pie," cooked hot on a stone/
steel for a crispy, chewy crust — a home-style approximation, not a claim to
replicate coal/gas deck-oven pizzeria technique. The dough uses a single ~1.5-
hour room-temperature rise with no cold fermentation, unlike some artisan NY
approaches (including the Jets' King Arthur-sourced recipe, which does use a
long cold ferment per `workers/afc-east-2.md`). This is a legitimate, source-
faithful quick/home variant, not a fidelity error — our recipe doesn't overclaim
pizzeria-grade authenticity either, so no correction is needed, only this
classification note for the record.

**Source fidelity — finding (minor, multiple small omissions).** Source
fetched in full. Dough, sauce and topping ingredient quantities all match
exactly. Instructions match in sequence and bake times (5 min + 5–10 min = the
stated 10–15 min), but several specific actionable details from the source are
generalized away:
- Source: refrigerate the reserved dough ball "up to 2 days or freeze up to 3
  months." Ours: "Refrigerate or freeze the unused dough ball" (no durations).
- Source: knead until "very smooth and elastic but still slightly tacky."
  Ours: "Knead 3 to 5 minutes until smooth" (drops the tacky-texture endpoint).
- Source: spread sauce "leaving a 3/4-inch border." Ours: "leaving a border"
  (no measurement).

**Specificity — pass.** Cheese/flour choices already match the source
(low-moisture mozzarella, fresh mozzarella, bread flour + AP flour blend); no
unsupported brand claims.

**Components — no new proposal in this batch.** No pizza-dough or pizza-sauce
component exists in `components/`. The Jets' `new-york-style-cheese-pizza`
recipe also makes NY dough/sauce from a different source (King Arthur). A
shared `ny-pizza-dough`/`ny-pizza-sauce` component could reduce duplication
across NFC/AFC East, but unifying two different sourced techniques (same-day
rise vs. cold ferment) is a cross-batch call outside this worker's assignment —
flagging for the orchestrator rather than proposing a merged component
unilaterally.

**Readability — B.** Clear quantities, temperatures and bake-time ranges;
minor ambiguity from the dropped storage durations, kneading endpoint and
border measurement above.

**Decision: targeted fix.**

Findings:
1. **Minor.** Current: "Refrigerate or freeze the unused dough ball." Proposed:
   "Refrigerate the unused dough ball up to 2 days, or freeze up to 3 months."
   URL: https://www.foodnetwork.com/recipes/food-network-kitchen/new-yorkstyle-cheese-pizza-10066512
   Section: Instructions, step 6. Confidence: high.
2. **Minor.** Current: "Knead 3 to 5 minutes until smooth." Proposed: "Knead 3
   to 5 minutes until very smooth and elastic but still slightly tacky."
   Section: Instructions, step 1. Confidence: high.
3. **Minor.** Current: "Spread 1/2 cup sauce on dough, leaving a border."
   Proposed: "...leaving a 3/4-inch border." Section: Instructions, step 5.
   Confidence: high.

Replacement candidates: none — source is sound and fully accessible.

**Access failures:** none. Source fetched successfully in full, including
headnote text.

---

## pastrami-on-rye-giants

- Path: `recipes/nfc/east/giants/pastrami-on-rye-giants.md` | status: published
- Source: https://www.labreabakery.com/recipes/ny-deli-pastrami-rye
- Hash: `10e5a7cdd9463a697bb8528dfb5bae9ad047be1d`

**City fit — pass.** Pastrami on rye is a defining NYC deli classic
(Katz's, 2nd Ave Deli); independently well established.

**Authenticity — pass for the sandwich itself; see fidelity finding below for
the added warming claim.** Sliced deli pastrami, rye bread, deli mustard and a
dill pickle is the standard defining assembly; nothing here is an unsupported
copycat.

**Source fidelity — major finding.** Source (La Brea Bakery) is a minimal
1-serving recipe: 1/3 lb pastrami, 2 slices rye, 1 tbsp mustard, pickle to
serve, with an explicit **0-minute cook time and no warming/steaming
instructions of any kind, and no mention of Katz's anywhere on the page**
(confirmed via two separate full-page fetches). Our recipe's step 1 adds a
skillet-steaming procedure and states "This warming step follows Katz's deli
guidance" — this attribution is not supported by the cited source. Independent
research confirms Katz's does reheat pastrami with steam, but via industrial
steam tables/kettles, not a home skillet-with-water method, so the specific
attribution and method are both unsupported as written (not necessarily wrong
as general kitchen advice, but not sourced from either citation given).
Ingredient quantities are otherwise scaled correctly from the source (1
serving × 4 matches our 4-serving quantities exactly for pastrami, rye and
mustard).

**Specificity — pass.** "Jewish-style rye bread" and "spicy brown deli
mustard" are reasonable, non-overclaiming specificity additions beyond the
source's plainer wording; not contradicted by it.

**Components — no new proposal.** Single recipe use; the Jets' separate
`pastrami-on-rye-jets` recipe (different source, centralmarketnewyork.com, per
`workers/afc-east-2.md`) is not a duplicate — different sourced instructions,
no forced merge.

**Readability — B.** Assembly steps are clear and ordered, but the warming
step's unsupported attribution undermines trust in that one instruction.

**Decision: targeted fix.**

Findings:
1. **Major — unsupported attribution / content not in cited source.** Current:
   "If pastrami is chilled, warm it just before serving: place portions in a
   covered skillet with 1–2 tablespoons water over medium-low heat for about 5
   minutes, until steaming. This warming step follows Katz's deli guidance;
   purchased ready-hot pastrami needs no reheating." Proposed: remove the
   "Katz's deli guidance" attribution since it appears nowhere in the cited
   source; either reword as an unattributed general deli tip (e.g., "a common
   deli method for warming sliced pastrami is...") or find and cite an actual
   Katz's-published source before keeping the attribution. Rationale: the cited
   source (La Brea Bakery) has zero cook time and no warming instructions;
   Katz's own reheating method is industrial steam-table/kettle, not a home
   skillet-and-water technique, so the specific claim is unsupported either
   way. URL: https://www.labreabakery.com/recipes/ny-deli-pastrami-rye Section:
   Instructions, step 1. Confidence: high (source fetched twice in full,
   confirmed no warming content or Katz's mention).

Replacement candidates: none proposed — the base sandwich and quantities are
sound; only the added instructional claim needs correction, not a source swap.

**Access failures:** none for the primary source (fetched successfully twice,
including a literal full-page-text request to confirm the absence of warming/
Katz's content). Katz's own published reheating instructions were not located
as a citable source in this session.
