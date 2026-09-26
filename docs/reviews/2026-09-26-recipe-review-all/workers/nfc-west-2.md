# Worker report — nfc-west-2

Date checked: 2026-09-26. Scope: 4 recipes (Rams x2, Seahawks x2), no exclusive
components. One recipe (`french-dip-sandwiches-rams`) is byte-identical to an
already-reviewed sibling; its source was not re-fetched, per instructions — findings
are reused from `workers/afc-west-1.md`. No access failures on the three sources I
fetched directly (latinasquecomen.com, applegate.com, feedthepudge.com).

## bacon-wrapped-la-street-dogs-rams

- Path: `recipes/nfc/west/rams/bacon-wrapped-la-street-dogs-rams.md` · status: published
- Source: https://www.latinasquecomen.com/mexican-hot-dogs/ · hash:
  `cf020dd703e71c17cda6a36fe96fd459e4b37b38`
- **City fit — pass, strong** (reused from afc-west-1's Chargers sibling review, same
  dish/city). Bacon-wrapped ("danger dog") hot dogs were made LA's official city hot
  dog by a 2010 LA City Council proclamation; street-cart ubiquity near sporting
  events/Venice Beach matches `location: Los Angeles, CA`.
- **Authenticity — pass.** Bacon-wrapped dog, grilled peppers/onions/jalapeños,
  ketchup/mustard/mayo trio matches the canonical street-cart build; source frames the
  dish as "a local LA street food."
- **Source fidelity — one major, independently-found defect, plus a shared minor
  omission.** Full source text fetched. `diff` against the Chargers sibling
  (`recipes/afc/west/chargers/bacon-wrapped-la-street-dogs-chargers.md`) shows this
  file has real content differences (not a copy), so it was audited independently.
  - **Major:** ingredients list "2 jalapeños, halved," but none of the 5 instruction
    steps ever cook or place them — step 3 reads "Cook the sliced pepper and onion
    over medium heat with about 2 teaspoons olive oil or rendered bacon fat," and no
    later step mentions jalapeños. Source text: "top with grilled onions, peppers,
    and jalapeños" — jalapeños are meant to be grilled alongside the other vegetables.
    The Chargers sibling correctly retains this ("add sliced bell pepper, onion and
    halved jalapeños"). Proposed: change step 3 to "Cook the sliced pepper, onion and
    halved jalapeños over medium heat with about 2 teaspoons olive oil or rendered
    bacon fat; avoid burning the vegetables." Confidence: high (direct source text +
    sibling-file comparison).
  - **Minor, shared with Chargers:** source includes "gently sprinkle with sea salt or
    favorite seasoning salt" as a finishing step; absent from both team files. Flagging
    for the orchestrator since a fix would apply to both. Confidence: high.
- **Cross-file comparison with Chargers (neither version is uniformly better):**
  Rams' plain "mustard" and "onion" wording is more literally faithful to the source's
  unqualified terms than Chargers' added "yellow mustard"/"white or yellow onion."
  Rams also correctly retains the source's optional-guacamole line ("guacamole is an
  optional topping"), which the Chargers file drops entirely. Conversely, Chargers
  correctly includes jalapeños in its sauté step (Rams' major defect above), and
  afc-west-1 flagged Chargers' unlabeled conditional-olive-oil wording as a separate
  minor issue not present in this file. Net: each file needs its own fix; neither is
  the cleaner baseline overall.
- **Specificity.** "All-beef hot dogs (other franks work by preference)" avoids
  over-claiming a brand; "soft hot dog buns, warmed" is adequate. No further gaps
  beyond the jalapeño-usage defect above.
- **Components.** Checked `components/` — no hot-dog-specific component exists.
  `components/dips/quick-guacamole.md` exists (Rick Bayless recipe) and could
  optionally be linked as `{{component:quick-guacamole}}` for the "guacamole is an
  optional topping" line; not required, minor enhancement only. Condiments
  (ketchup/mustard/mayo) are correctly left inline, not componentized.
- **Readability: C.** Ordered steps with time endpoints (7 min, 5 min per side), but
  a listed ingredient (jalapeños) is never actioned in any step — a concrete
  missing-actionable-detail defect.
- **Decision: targeted fix.** Add jalapeños to step 3's sauté instruction. Optionally
  also add a light seasoning line (shared issue, orchestrator's call on scope).
- **Findings:**
  1. Major — see source fidelity above. Section: Instructions step 3. Confidence:
     high.
  2. Minor (shared) — sea salt finishing step omitted. Section: Instructions
     step 4/5. Confidence: high.
- **Replacement candidates:** none — source is a legitimate, on-topic regional recipe;
  targeted fix suffices.
- **Access failures:** none. latinasquecomen.com/mexican-hot-dogs/ was fetched and
  read in full via WebFetch.

## french-dip-sandwiches-rams

- Path: `recipes/nfc/west/rams/french-dip-sandwiches-rams.md` · status: published
- Source: https://discovercaliforniawines.com/recipes/french-dip-sandwich-an-l-a-classic/
  · hash: `23ca7256810e49fc73a21bed05afd38e744d00a7`
- **Diff-confirmed duplicate.** `diff` against
  `recipes/afc/west/chargers/french-dip-sandwiches-chargers.md` (hash
  `d7f3a422d2aa2017f289f7b9243641f505c244fc` per afc-west-1) shows the only
  differences are the `id:` line and the `image:` filename; front matter body,
  Ingredients, Instructions and Kitchen Notes are byte-identical. Per task
  instructions this reuses afc-west-1's findings rather than re-deriving them; I did
  not independently re-fetch discovercaliforniawines.com.
- **City fit — pass**, reused: source frames the dish as "An L.A. Classic"; French
  dip's contested Philippe's/Cole's origin is centered on Los Angeles, matching
  `location: Los Angeles, CA`. Rams-specific note: the Rams carry LA's longest-running
  NFL identity (1946–1994, returned 2016), an equally or more natural fit for an
  "LA Classic" than the more recently LA-based Chargers — both team files legitimately
  share the same city framing.
- **Authenticity — pass, with labeled omissions** (reused): Kitchen Notes document
  cheese, pickled onion and mustard as omitted from the default, and wine as optional,
  matching the source's own optional/garnish items.
- **Source fidelity — reused verbatim from afc-west-1** (applies identically, text is
  byte-identical):
  1. Moderate — "4 French rolls, split" is a stale 4-serving figure that cannot yield
     the recipe's own stated 6-sandwich yield (the parenthetical baguette alternative
     is already correctly scaled to six segments). Fix: "6 French rolls, split."
  2. Minor — jus method is simplified from source's butter-browned, longer two-stage
     reduction (~10 min wine reduction + ~15 min stock reduction) to an un-buttered
     ~5-minute simmer, not labeled as an intentional adaptation.
  3. Minor — source's 1 tsp granulated onion (alongside granulated garlic in the rub)
     is dropped without a Kitchen Notes label.
  4. Minor/specificity — source specifies wine style "Zinfandel or Syrah" (fits its
     California-wine publisher); ours generalizes to "dry red wine." Restoring the
     wine style would improve fit and specificity.
- **Components.** Reused: `components/sauces/prime-rib-pan-jus.md` checked, distinct
  thyme/wine/drippings jus for a different roast, not a substitute. afc-west-1
  proposes a new shared component **`french-dip-au-jus`** (full measured draft,
  sourced to discovercaliforniawines.com): 2 tbsp butter; ½ cup dry red wine such as
  Zinfandel or Syrah (optional; substitute ½ cup beef stock for alcohol-free); 2 cups
  low-sodium beef stock; salt and pepper to taste. Method: melt butter until
  golden-brown and nutty; add wine, boil, simmer ~10 min until reduced by half (skip
  if alcohol-free); add stock, boil, simmer ~15 min until reduced by about
  one-third; season to taste. Yield: roughly 1½–2 cups (editorial estimate — source
  states no finished yield). Quick-buy alternative: prepared beef au jus concentrate
  or reduced beef bone broth, warmed separately. **Shared consumers to inspect:**
  both `recipes/afc/west/chargers/french-dip-sandwiches-chargers.md` and this file —
  a fix needs to land in (or replace inline text in) both.
- **Rams-specific note:** `french-dip-sandwiches-rams.jpg` is the same file size
  (142,364 bytes) as `french-dip-sandwiches-chargers.jpg`, both credited
  "discovercaliforniawines.com" — consistent, appears to be the same source photo
  reused for both team pages; no mismatch.
- **Readability: C** (reused) — the roll-count/yield mismatch is a concrete
  shopping/prep confusion point; otherwise ordered steps with clear endpoints (125°F
  internal, rest 15 min, slice thin).
- **Decision: targeted fix** (mirrors afc-west-1's Chargers recommendation exactly,
  since body text is identical): (1) "4 French rolls" → "6 French rolls" (affects both
  team files); (2) restore or label the jus butter/reduction-time method; (3) restore
  or label the granulated onion; (4) restore wine-style specificity; (5) consider the
  shared `french-dip-au-jus` component to eliminate duplication between the two files.
- **Access failures:** none for this file specifically. discovercaliforniawines.com
  was not independently re-fetched by me — by design, since the file is byte-identical
  to the already-audited Chargers file — so these findings are inherited from
  afc-west-1's direct fetch, not from memory.

## seattle-dogs-with-cream-cheese-and-onions

- Path: `recipes/nfc/west/seahawks/seattle-dogs-with-cream-cheese-and-onions.md` ·
  status: published
- Source: https://www.applegate.com/recipes/seattle-dog · hash:
  `e31a044e1cc608a755411d8c20cdf64864cdf0d8`
- **City fit — pass, strong, directly evidenced.** `location: Seattle, WA`.
  Wikipedia's "Seattle-style hot dog" article (fetched directly, not just a search
  snippet): "In Seattle, the dogs are sold from food carts, especially outside
  stadiums on game day and as a late-night meal outside the city's music venues" —
  direct support for both the city identity and the game-day framing. Origin:
  invented by Hadley Long, a Pioneer Square bagel-cart vendor, dated 1989 by Wikipedia
  and 1988 by SEAtoday (https://seatoday.6amcity.com/culture/seattle-dog-history-cream-cheese)
  — a minor date discrepancy between two secondary sources, not relevant to the
  recipe content.
- **Authenticity — pass, labeled accepted variant.** Wikipedia (direct fetch): "A hot
  dog served in a bun slathered with cream cheese and topped with caramelized onions
  and sometimes jalapeños" — matches our recipe's cream cheese + onions core and
  directly corroborates the jalapeño addition as a documented regional variant, not a
  fabrication. Classification: baseline (Applegate) recipe plus one independently
  corroborated variant addition.
- **Source fidelity — strong match, one addition beyond the cited source.** Applegate
  source (fetched in full): 2 tbsp extra-virgin olive oil, 1 large onion thinly
  sliced, 1 package (~8) Applegate uncured beef hot dogs, 1 package hot dog buns
  toasted, 8 tbsp cream cheese, yellow mustard; method: cook onion 8–10 min until
  soft/golden, grill/pan-sear hot dogs, toast buns and spread 1 tbsp cream cheese each,
  top with onions and mustard — matches our file one-to-one (hot dog brand correctly
  generalized: "Applegate is the source brand, but any quality beef frank works").
  No unlabeled discrepancies. The one addition — "optional sliced pickled jalapeños
  for a common Seattle street-cart variation" — is not in the Applegate source, but is
  independently corroborated by the Wikipedia quote above and correctly labeled
  "optional"/a variation rather than presented as the cited source's own text. Treated
  as pass, not a fidelity defect.
- **Specificity.** Yellow mustard is appropriately concrete and matches the source; a
  quality-beef-frank alternative to the named brand is a transparent, reasonable
  generalization. No gaps.
- **Components.** Checked `components/` — no existing onion-sauté or hot-dog-topping
  component fits; this recipe's steps are simple enough that componentizing isn't
  warranted (correctly left inline). No new component proposed.
- **Readability: A.** Ordered steps, explicit time endpoint (8–10 min for onions,
  "browned and hot" for dogs), precise per-bun quantities.
- **Decision: keep.** Positive evidence: quantities/method verified nearly one-to-one
  against the directly-fetched source; the one addition is explicitly optional,
  labeled as a regional variation, and independently corroborated by a primary-fetched
  Wikipedia citation. City fit is strong and directly evidenced.
- **Findings:** none rising to a defect. Observational only: SEAtoday/Wikipedia
  disagree on the invention year (1988 vs. 1989); irrelevant to recipe content.
- **Replacement candidates:** none needed.
- **Access failures/unverified claims:** none for the cited source (fetched in full).
  One unverified claim surfaced by WebSearch, not independently confirmed: a
  king5.com headline states the New York Times named the Seattle Dog "the best hot
  dog in the country." I did not fetch a primary NYT source for this, so it is
  flagged as an interesting but unverified claim — recommend the orchestrator not
  cite it as confirmed without checking the NYT source directly.

## seattle-style-chicken-teriyaki

- Path: `recipes/nfc/west/seahawks/seattle-style-chicken-teriyaki.md` · status:
  published
- Source: https://feedthepudge.com/seattle-chicken-teriyaki/ · hash:
  `c6cdbbc06d704059c9129dc37fe710c8584213ed`
- **City fit — pass, strong, directly evidenced.** `location: Seattle, WA`. The
  source's own text credits Toshihiro "Toshi" Kasahara's Toshi's Teriyaki Restaurant
  (opened March 2, 1976, Lower Queen Anne, Seattle) as the origin of Seattle-style
  teriyaki, with hundreds of teriyaki shops later spreading across the city/state.
  Independently corroborated via WebSearch (snippet-level, not full-text fetches)
  across Tasting Table, HistoryLink.org (Washington State's official history
  encyclopedia), KUOW, The Seattle Times, Seattle Weekly, Seattle Refined and Toshi's
  Teriyaki Grill's own site — all describing the same 1976 Kasahara/Toshi's origin,
  including the detail that a positive Seattle Times review (critic John
  Hinterberger) tripled or quadrupled early business. Consistent across all snippets;
  treated as reliable corroboration, but note this is search-snippet-level, not
  full-text-read corroboration, for each of those seven-plus outlets.
- **Authenticity — pass.** Defining traits: skin-on chicken thighs; soy/sugar/
  mirin/sake marinade with a reserved-sauce reduction; grilled or air-fried; served
  over rice — matches the source's own recipe and the broader documented Seattle-style
  teriyaki genre described in the corroborating articles.
- **Source fidelity — essentially exact match, fetched and compared in full.**
  Ingredients (2 lb boneless skin-on chicken thighs; 1 cup low-sodium soy sauce; ½ cup
  sugar; 1 tbsp each mirin/sake/minced garlic/grated ginger; sesame seeds) match
  one-to-one. Method matches: debone/flatten thighs; combine sauce, marinate half over
  chicken at least 30 min up to overnight, reserve rest; simmer reserved sauce to
  reduce, optional cornstarch slurry for thickness; grill to 165°F, rest 5 min, slice,
  serve over rice with a small iceberg salad (source's own classic side, correctly
  attributed as such); air-fryer alternative (375°F 14 min flipping halfway, drop to
  350°F if sugars brown too fast after 7 min, cook to 165°F) matches closely.
  - **Minor:** step 4's "Grill skin-side down first for char, then turn..." is a
    technique detail not present in my extraction of the source text (which specifies
    only grilling to 165°F, no explicit sequence). This is a standard, safe technique
    for skin-on poultry and not contradicted by the source, but it is an unlabeled
    addition beyond the literal source text. Confidence: medium (based on an
    extraction summary, not a verbatim reproduction of every source clause). No
    correction required; optionally credit in Kitchen Notes.
- **Specificity.** Mirin correctly distinguished from rice vinegar; sake flagged as
  omittable by preference. Cornstarch slurry amount is explicitly labeled as an
  editorial estimate ("source gives no amount; begin with 1 teaspoon cornstarch mixed
  into 1 teaspoon cold water") since the source itself gives no quantity — matches the
  brief's guidance to label estimates as estimates, not as tested facts.
- **Components.** Checked `components/` — no existing teriyaki-sauce/marinade
  component; this recipe's sauce (7 ingredients, one bowl) is simple enough that
  componentizing isn't warranted, and no other recipe in the book currently reuses it.
  No new component proposed.
- **Readability: A.** Ordered numbered steps, explicit temperatures/times (165°F,
  5 min rest, 375°F/14 min with a 350°F fallback), quantities specified throughout,
  the one genuine estimate clearly flagged as such.
- **Decision: keep.** Positive evidence: full source text fetched and compared
  line-by-line with only one minor, safe, unlabeled technique addition and no
  quantity or ingredient discrepancies; city fit is strong and multiply corroborated
  beyond the cited source itself.
- **Findings:** minor — see skin-side-down technique note above. Confidence: medium.
  No other findings.
- **Replacement candidates:** none needed.
- **Access failures:** none. feedthepudge.com/seattle-chicken-teriyaki/ was fetched
  and read in full via WebFetch. The Toshi's/Kasahara regional-history corroboration
  used WebSearch snippets across multiple outlets rather than full-text fetches of
  each — consistent findings, but stated explicitly per instructions.
