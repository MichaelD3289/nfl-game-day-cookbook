# Worker report — afc-west-1

Date checked: 2026-09-26. Scope: 6 recipes (Broncos x3, Chargers x2, Chiefs x1), no
exclusive components (none of the six use a `{{component:...}}` marker). Two confirmed
access failures (highlandsranchfoodie.com, saveur.com — both 403, retried once each per
instructions); nothing filled from memory for either.

## colorado-pork-green-chile

- Path: `recipes/afc/west/broncos/colorado-pork-green-chile.md` · status: published
- Source: https://edibledenver.com/ed-recipe/colorado-style-pork-green-chile/ · hash:
  `65c01439b306b8eda10a542b6373ad1ce7ef87bc`
- **City fit — pass.** `location: Denver, CO`; source is Edible Denver, a Denver-based
  food publication. Green chile (pork, tomatillo/tomato base) is a defining Denver/Front
  Range dish; 5280 Magazine's green-chile feature and coverage of James Beard
  America's-Classics honoree El Taco de Mexico corroborate its centrality to Denver's
  food identity.
- **Authenticity — accepted variant, worth a note.** Local reporting (5280) associates
  the most "iconic" Denver/Pueblo-style green chile with Pueblo chiles and a flour/roux
  thickener, giving a thicker, reddish-brown "smothering" sauce. This recipe (and its
  source) instead use Anaheim or Big Jim chiles with a clear, non-roux tomatillo/tomato
  pork stew — a legitimate, commonly served Denver-area chile verde style, but a
  different sub-style than the roux-thickened "Pueblo" smother. Not an error (both
  styles are attested), but the distinction is worth naming if the book ever discusses
  regional sub-styles.
- **Source fidelity — verified match, no findings.** Full source text fetched and
  compared: chile weight/type, pork/tomatillo/tomato quantities, chicken stock, potato
  addition timing (last 45 min), and 4-step method all match. Only trivial wording
  differences (our "husked" vs. source's "peeled" tomatillos) — not a fidelity error.
- **Specificity.** Chile type (Anaheim/Big Jim), Mexican oregano (correctly
  distinguished from Mediterranean oregano), kosher salt, and russet potatoes are all
  concrete. Optional enhancement (not required): a "quick-buy" note that thawed frozen
  roasted Hatch/Pueblo green chile (e.g., Bueno brand, widely sold in Colorado grocery
  stores each fall) can substitute for the fresh-roast step — would strengthen the
  Make-It-or-Buy-It angle without changing the from-scratch default.
- **Components.** No existing component fits — this recipe *is* the from-scratch dish.
  `components/sauces/roasted-salsa-verde.md` was checked and is a distinct raw
  tomatillo/serrano salsa, not a substitute. No new component proposed. Note for the
  orchestrator: `recipes/afc/west/broncos/green-chile-breakfast-burritos.md` (also in
  this batch) reuses this recipe by cross-reference, not as a component — correct design
  per AGENTS.md (component markers are for sub-recipes, not whole dishes).
- **Readability: A.** Ordered steps, precise quantities, clear endpoints (chiles
  blistered/steamed/peeled; pork browned; simmer 1–2 hr; potatoes tender).
- **Decision: keep.** No corrections needed; optional frozen-chile buy-it note only.
- No access failures.

## denver-omelet

- Path: `recipes/afc/west/broncos/denver-omelet.md` · status: published
- Source: https://www.foodnetwork.com/recipes/food-network-kitchen/western-omelette-recipe-2011477
  · hash: `e4d1f4e4dcf35b704bff6f5c31a05fa723cb573e`
- **City fit — pass, with a documented dispute noted.** Origin is contested: the
  American Historical Association's "The Muddled History of the Denver Omelet" and
  Atlas Obscura's entry on Denver's own commemorative Denver Omelet plaque both confirm
  the dish is inseparably tied to Denver in name and lore even though its true origin
  (possibly a Basque or Chinese-railroad-cook "egg foo yong" adaptation) is unresolved.
  This is a naming/lore association, not a manufactured claim, and is appropriate for
  `location: Denver, CO`.
- **Authenticity — pass, labeled adaptation.** Source calls this a "Western
  omelette... also known as a Denver omelette," built on ham, bell pepper, onion
  (scallions in source), and optional cheese (source notes cheese as non-traditional).
  Our recipe substitutes "1/2 cup chopped white onion" for the source's 4 scallions and
  explicitly documents this in its own Kitchen Notes as "editor's classic Denver
  substitution for scallions" — a labeled, intentional adaptation, not a silent error.
- **Source fidelity — verified, one labeled deviation only.** Full source text fetched
  and compared; ham/pepper/onion-type/egg technique/cheese-optionality all match once the
  labeled scallion→onion swap is accounted for. No unlabeled discrepancies found.
- **Specificity.** "Boiled ham (in one piece)," named cheese options (Monterey Jack,
  cheddar, Gouda), and unsalted butter are all concrete. No gaps.
- **Components.** No component applies (single-dish preparation, no reusable
  sub-recipe). None proposed.
- **Readability: A.** Precise quantities, ordered technique, clear visual endpoints
  (set edges, 30-second fold, melted cheese).
- **Decision: keep.** The onion-for-scallion swap is a documented, labeled variant, not
  a fidelity error — no correction needed.
- No access failures.

## green-chile-breakfast-burritos

- Path: `recipes/afc/west/broncos/green-chile-breakfast-burritos.md` · status: published
- Source: https://highlandsranchfoodie.com/breakfast-burrito-with-green-chile-sauce/ ·
  hash: `284609e6c087216c46c69d2f57ccf37fdb4fdd30`
- **City fit — pass.** `location: Denver, CO`. Green-chile-smothered breakfast burritos
  are a defining metro-Denver breakfast dish; the recipe correctly reuses this batch's
  own `colorado-pork-green-chile` as its smothering sauce rather than inventing a new
  one — a Denver-wide dish, not narrowly tied to the source blog's Highlands Ranch
  location (a suburb; per brief, suburb sourcing doesn't override the book's Denver
  framing for a metro-wide dish).
- **Authenticity — pass.** Standard construction (potato/egg/bacon/cheese filling,
  flour tortilla, smothered in green chile) matches the genre; cross-referencing this
  book's own pork green chile recipe for the sauce (rather than a shortcut jarred sauce)
  is a reasonable, well-integrated design choice.
- **Source fidelity — ACCESS FAILURE, partially corroborated only.** `WebFetch` to the
  cited URL returned HTTP 403 on first attempt and on a deliberate retry (not
  transient). Fallback `WebSearch` located the same post (titled "Hatch Green Chili
  Breakfast Burrito With Potatoes," blog "Cooking on the Ranch" /
  highlandsranchfoodie.com) and confirmed only the qualitative ingredient set matches:
  8–10" flour tortillas, red-skinned or Yukon Gold potatoes, yellow/sweet/white onion,
  green chile sauce, eggs, chopped cooked bacon, and cheddar/Monterey Jack/Pepper
  Jack/Muenster as alternates. Search snippets did **not** surface exact quantities, so
  the specific amounts in our file (8 oz bacon, 1½ lb potatoes, 6 eggs, tortilla count,
  cheese amount, etc.) remain unverified against the source's literal text. Nothing here
  was filled from memory — this is recorded as unresolved.
- **Specificity.** "Southwest spice blend or New Mexico red chile powder" is vague — no
  named product backs "Southwest spice blend." Proposed correction: drop the
  undefined blend name and specify "1 teaspoon ground New Mexico red chile powder (or
  a store Southwest/taco seasoning blend, checked for salt content)," or simply cite chile
  powder alone. Severity: minor (readability/specificity, not a factual error).
  Confidence: medium (a reasonable simplification, not sourced to the blocked page).
  Freshly grated cheddar is already appropriately specific.
- **Components.** No new component needed; this recipe's smothering sauce is already
  handled by cross-referencing `colorado-pork-green-chile` (see that section) rather
  than a shortcut component — correct design.
- **Readability: B.** Ordered steps with visible endpoints (browned edges, softly set
  eggs, melted cheese), but the cross-reference "3–4 cups prepared Colorado-style pork
  green chile" doesn't tell the cook how that maps to the other recipe's total yield —
  a home cook can't easily tell if a full batch of the other recipe is enough. Minor
  usability gap, not required for this review to fix.
- **Decision: keep, with an unresolved fidelity item.** Exact-quantity verification
  against the source is blocked; qualitative ingredient composition is corroborated.
  Recommend a further retry by the orchestrator at a later date, or accepting the
  current text as the best available.
- **Access failure:** highlandsranchfoodie.com/breakfast-burrito-with-green-chile-sauce/
  — HTTP 403, confirmed on retry. Partial corroboration via WebSearch snippets only
  (ingredient list, not exact quantities).

## bacon-wrapped-la-street-dogs-chargers

- Path: `recipes/afc/west/chargers/bacon-wrapped-la-street-dogs-chargers.md` ·
  status: published
- Source: https://www.latinasquecomen.com/mexican-hot-dogs/ · hash:
  `582d10ea8d8a8e44a069d0a900ba1c20b0e7ede4`
- **City fit — pass, strong corroboration.** The bacon-wrapped ("danger dog"/"dirty
  dog"/"LA street dog") hot dog was made LA's official city hot dog by a 2010 Los
  Angeles City Council proclamation; its Sonoran-hot-dog lineage and street-cart
  ubiquity near sporting events, concerts, and Venice Beach are well documented and
  match `location: Los Angeles, CA` (SoFi Stadium's Inglewood/Carson-area location is
  correctly generalized to the established LA city identity, per brief).
- **Authenticity — pass.** Bacon-wrapped dog, grilled peppers/onions/jalapeños,
  condiment trio (ketchup/mustard/mayo) matches the canonical street-cart build; source
  itself frames the dish as "a local LA street food."
- **Source fidelity — one minor unlabeled adaptation.** Full source text fetched:
  4 hot dogs/buns/bacon, red bell pepper, ½ onion, 2 jalapeños, 10 cilantro sprigs,
  2 tsp ketchup, 2 tsp mustard, 1 tsp mayo, 2 tsp olive oil (added unconditionally at the
  5-minute mark), sea salt to taste; prep 5 min / cook 22 min. Our recipe makes the
  olive oil **conditional** ("up to 2 teaspoons olive oil if bacon does not render
  enough fat") rather than the source's unconditional addition. This is a minor,
  practical, but **unlabeled** adaptation (not called out in Kitchen Notes). Severity:
  minor. Proposed correction: either add the oil unconditionally per source, or note in
  Kitchen Notes that it's conditional by design. Confidence: high (direct source text).
- **Specificity.** "All-beef hot dogs (brand is personal preference)" and "soft white
  hot dog buns" are appropriately concrete without over-claiming a brand; regular-cut
  bacon is specific. No further gaps.
- **Components.** Condiments (ketchup/mustard/mayo) and grilled vegetables are
  correctly left as plain ingredients/inline steps, not componentized — matches brief
  guidance that component markers belong on reusable finished sub-recipes, not raw
  condiments. No new component proposed.
- **Readability: B.** Ordered steps with time endpoints, but the condiment-application
  step ("dividing the source amounts across four dogs") reads like an editorial note
  rather than a plain per-dog measurement (e.g., "½ tsp each ketchup and mustard, ¼ tsp
  mayo per dog" would be clearer). Minor readability nit, not a factual error.
- **Decision: keep**, with a small labeling/consistency fix recommended for the olive
  oil step (make conditional-by-design explicit in Kitchen Notes, or restore the
  source's unconditional wording).
- No access failures.

## french-dip-sandwiches-chargers

- Path: `recipes/afc/west/chargers/french-dip-sandwiches-chargers.md` · status:
  published
- Source: https://discovercaliforniawines.com/recipes/french-dip-sandwich-an-l-a-classic/
  · hash: `d7f3a422d2aa2017f289f7b9243641f505c244fc`
- **City fit — pass.** Source itself frames the dish as "An L.A. Classic"; French dip's
  contested Philippe's/Cole's origin story is centered on Los Angeles, matching
  `location: Los Angeles, CA` for both this Chargers file and its byte-identical
  counterpart at `recipes/nfc/west/rams/french-dip-sandwiches-rams.md` (noted for
  context only — outside this batch, not reviewed here, but any correction below
  applies to both files).
- **Authenticity — pass, with labeled omissions.** Kitchen Notes explicitly document
  that cheese, pickled onion, and mustard are omitted from the default and that wine is
  optional — matching the source's own optional/garnish items. This labeling is
  correct practice.
- **Source fidelity — one concrete unlabeled defect, plus minor simplifications.**
  Full source text fetched (a 4-serving recipe; our file scales to 6 sandwiches):
  - **Finding (moderate/concrete): roll-count inconsistency.** Our ingredient list
    reads "**4 French rolls, split** (or 2 baguettes cut into six 6-inch lengths)" —
    the parenthetical baguette alternative was correctly scaled to six segments, but the
    primary "4 French rolls" figure is a stale leftover from the source's 4-serving
    recipe and cannot yield 6 sandwiches as the recipe's own stated yield requires.
    Proposed correction: change to "6 French rolls, split." Severity: moderate
    (concrete usability defect — a cook following the primary ingredient exactly comes
    up two rolls short). Confidence: high (direct comparison to source, which is
    explicitly a 4-serving recipe with "4 French rolls or 2 baguettes cut into six
    6-inch segments").
  - **Finding (minor): jus method simplified/shortened versus source.** Source method:
    melt butter until browned/nutty, add wine, reduce by half (~10 min), add stock,
    reduce by one-third (~15 min) — a longer, butter-based reduction. Our recipe uses an
    un-buttered, ~5-minute simmer. This is a flavor-concentration simplification, not
    labeled as an adaptation in Kitchen Notes. Severity: minor. Proposed: either restore
    the butter step and longer reduction, or add a Kitchen Notes line documenting the
    faster method as an intentional simplification. Confidence: high.
  - **Finding (minor): granulated onion dropped.** Source rub includes 1 tsp granulated
    onion alongside granulated garlic; ours omits it without a Kitchen Notes label.
    Severity: minor. Confidence: high.
  - "2 cups low-sodium beef stock, divided" + optional "½ cup dry red wine (replace
    with ½ cup beef stock)" reconciles correctly with the alcohol-free instruction's
    "2½ cups stock" — re-checked and is **not** an error, just slightly indirect
    wording; downgraded from a possible finding to a readability nit only.
  - Provolone cheese, pickled red onions, and spicy mustard are all labeled-omitted in
    Kitchen Notes already (source has all three) — correctly handled, no finding.
- **Specificity.** Source specifies wine style ("Zinfandel or Syrah") consistent with
  its California-wine-focused publisher; our recipe drops this to generic "dry red
  wine." Given the source's own branding is wine-pairing-focused, restoring "such as
  Zinfandel or Syrah" would improve specificity and fit. Severity: minor. Confidence:
  high (direct source wording).
- **Components.** No existing component matches — `components/sauces/prime-rib-pan-jus.md`
  was checked and is a distinct thyme/wine/pan-drippings jus tied to a different roast,
  not a substitute. **Proposal: extract a new shared component** for this jus, since the
  identical inline method is duplicated verbatim in both the Chargers and Rams French
  dip files (shared consumers the orchestrator should inspect: both paths above).
  Complete measured draft, sourced to discovercaliforniawines.com:
  - `french-dip-au-jus` (working id) — 2 tablespoons butter; ½ cup dry red wine, such as
    Zinfandel or Syrah (optional; substitute ½ cup beef stock for alcohol-free); 2 cups
    low-sodium beef stock; salt and pepper to taste. Method: melt butter over medium
    heat until golden-brown and nutty-smelling; add wine, bring to a boil, then simmer
    ~10 minutes until reduced by half (skip if using the alcohol-free substitution);
    add stock, bring to a boil, simmer ~15 minutes until reduced by about one-third;
    season to taste. Yield: roughly 1½–2 cups (editorial estimate — source doesn't
    state a finished yield). Quick-buy alternative: a prepared beef au jus concentrate
    or beef bone broth reduced to taste, warmed separately (pattern matches
    `prime-rib-pan-jus`'s existing quick-buy phrasing).
- **Readability: C.** The roll-count/yield mismatch is a concrete point of confusion a
  cook would hit while shopping/prepping; otherwise steps are ordered with clear
  endpoints (125°F internal, rest 15 min, slice thin).
- **Decision: targeted fix.** Recommend: (1) correct "4 French rolls" to "6 French
  rolls" (affects both Chargers and Rams files), (2) restore or label the jus
  butter/reduction-time method, (3) restore or label the granulated onion, (4) restore
  wine-style specificity ("Zinfandel or Syrah"), (5) consider the new shared
  `french-dip-au-jus` component to eliminate the duplication between the two team files.
- No access failures.

## barbecue-baked-beans

- Path: `recipes/afc/west/chiefs/barbecue-baked-beans.md` · status: published
- Source: https://www.saveur.com/article/Recipes/Baked-Beans/ · hash:
  `044842f8f3c8869949946cf4124d8597d080fc4b`
- **City fit — pass, strong.** `location: Kansas City, MO`; photo credit
  kcmasterpiece.com (a KC company). Baked beans built on smoked burnt ends and sorghum
  are squarely Kansas City barbecue tradition.
- **Authenticity — pass.** WebSearch corroboration (see below) attributes the Saveur
  recipe to barbecue pitmaster Paul Kirk's mother — Kirk being a well-documented Kansas
  City barbecue figure ("Baron of Barbecue") — consistent with a genuine KC-tradition
  provenance, not a generic copycat.
- **Source fidelity — ACCESS FAILURE, strongly corroborated via search snippets.**
  `WebFetch` to the cited saveur.com URL returned HTTP 403 on first attempt and on a
  deliberate retry (pre-flagged as a known-blocked domain; not transient). Fallback
  `WebSearch` surfaced a search-engine summary quoting quantities that match our recipe
  closely: 1 lb navy beans, ⅓ cup sorghum syrup, ¼ lb burnt ends, ½ cup dark brown
  sugar, 1 small yellow onion, soy sauce/Worcestershire/dry mustard, simmer 1–1.5 hr,
  bake at 275°F for 5–6 hr — all matching our file. A related but explicitly distinct
  Food Network page ("The Baron's Mother's (Mrs. Mary Kirk's) From-Scratch Baked Beans,"
  attributed to Lolis Eric Elie) was fetched successfully and used only for broader
  Kirk-family/KC regional corroboration — it is a different variant (bacon square/hog
  jowls instead of burnt ends, requires an overnight soak, bakes 5–8 hr) and was **not**
  used as a stand-in fidelity check for the actual blocked page. One quantity in our
  file — "about 3 cups water to start, plus up to 2 cups more as needed" — could not be
  confirmed against the source's exact wording via search snippets; flagged as an
  editorial estimate, not a verified fact.
- **Specificity.** Sorghum syrup (correctly distinguished from molasses), dry mustard,
  and "smoked beef brisket burnt ends or other barbecue meat scraps" are all
  appropriately concrete; the "or other barbecue meat scraps" fallback is a transparent,
  reasonable flexibility addition, not a hidden fidelity problem.
- **Components.** No new component proposed. This book already has a full recipe,
  `recipes/afc/west/chiefs/kansas-city-burnt-ends.md`, that is the natural "make it"
  source for the burnt ends called for here — recommend the orchestrator add a
  cross-reference note (similar to how `green-chile-breakfast-burritos` cross-references
  `colorado-pork-green-chile`) rather than creating a shared component, since burnt ends
  is already a full standalone recipe, not a sub-component. `components/sauces/kansas-city-barbecue-sauce.md`
  was checked and does not apply (not consumed directly in this recipe).
- **Readability: A.** Ordered steps, explicit oven temp/time (275°F, 5–6 hr, "cover if
  top browns too quickly"), and clear stage endpoints (beans simmered until tender,
  liquid levels maintained "just covered").
- **Decision: keep, with a noted access failure.** Strong quantity-level corroboration
  via search snippets; the one uncorroborated figure (starting water volume) is noted
  as an editorial estimate rather than a confirmed source fact.
- **Access failure:** saveur.com/article/Recipes/Baked-Beans/ — HTTP 403, confirmed on
  retry (pre-flagged blocked domain). Corroborated via WebSearch snippet quoting
  matching quantities plus a Paul Kirk's-mother attribution; the source page's exact
  instructional wording (and the starting-water-volume figure specifically) remain
  unverified.
