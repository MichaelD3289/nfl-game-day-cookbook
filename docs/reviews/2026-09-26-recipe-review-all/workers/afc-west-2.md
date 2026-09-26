# Worker report — afc-west-2

Date checked: 2026-09-26. Scope: 5 recipes (Chiefs x3, Raiders x2) plus 2 exclusively
assigned components (`prime-rib-horseradish-cream`, `prime-rib-pan-jus`). Three access
failures on primary sources (amazingribs.com — 403, retried once; www.seriouseats.com —
hard tool-level block, not retryable; www.qvc.com — HTTP 418, retried once), partly
offset by WebSearch snippet corroboration as noted per recipe. Nothing filled from
memory for any blocked source.

## kansas-city-burnt-ends

- Path: `recipes/afc/west/chiefs/kansas-city-burnt-ends.md` · status: published
- Source: https://amazingribs.com/brisket-burnt-ends/ · hash:
  `81a738df581c42467f40a54cd63ce513eb392dd2`
- **City fit — pass.** `location: Kansas City, MO`; the source's own title calls this "A
  Ridiculously Delicious Kansas City Original." Burnt ends (cubed, twice-cooked, sauced
  brisket point) are the defining Kansas City barbecue dish, per the same page and wide
  independent food reporting.
- **Authenticity — traditional/local.** Two-stage cook (smoke to ~155°F bark, foil-braise
  to ~195°F, cube, then crisp and glaze in rendered fat with sauce) matches the
  Meathead/AmazingRibs method that popularized the modern "burnt ends as a dish"
  presentation, itself derived from Arthur Bryant's original point trimmings. No
  unsupported claims made.
- **Source fidelity — direct fetch blocked (403 twice); strongly corroborated via
  search.** WebFetch to the source URL returned 403 on first attempt and again on retry.
  WebSearch snippets from the live page corroborated: "155°F" bark target, "195°F"
  wrap-done target, "1-inch cubes," and the finishing glaze of "¼ cup of your favorite
  BBQ sauce and ¼ cup of the drippings" — all matching our recipe's step 2–5 numbers.
  The standalone "Big Bad Beef Rub" sub-recipe (a separate AmazingRibs page, also
  403-blocked directly) was corroborated via search snippet: full batch is 3 tbsp
  pepper, 2 tbsp salt, 1 tbsp sugar, 1 tbsp onion powder, 2 tsp each mustard/garlic/
  ancho-or-chili powder, 1 tsp chipotle/cayenne, with salt applied separately at "about
  1/2 teaspoon Morton Coarse Kosher Salt per pound." Our recipe's rub (1½ tbsp pepper,
  1½ tsp sugar, 1½ tsp onion powder, 1 tsp each mustard/garlic/ancho, ½ tsp
  chipotle/cayenne) is an exact half-batch of every one of the seven spice ingredients,
  with salt correctly moved to the separate dry-brine step at 3 teaspoons for 6 pounds
  — exactly the source's own ½ teaspoon-per-pound rate. No discrepancy found. Because
  this is snippet corroboration rather than a direct read of the live page, treat as
  strong (not absolute) confidence.
- **Specificity.** "USDA Choice or better," "brisket point" (not whole packer or flat),
  Morton coarse kosher salt (a specific, non-interchangeable-by-volume brand called out
  correctly since Morton coarse crystals differ from Diamond Crystal by volume), and
  named individual rub spices are all concrete and appropriately non-generic.
- **Components.** Checked `components/sauces/kansas-city-barbecue-sauce.md` (used here
  via `{{component:kansas-city-barbecue-sauce}}` as the ¼-cup finishing sauce/quick
  option) — owned by another worker, not re-reviewed. Usage note: the marker sits on a
  clearly finished sauce quantity ("¼ cup... barbecue sauce"), not a raw ingredient, and
  is not double-counted (the recipe's own sauce use is a single ¼-cup addition in step
  5). No existing or candidate component fits the "Big Bad Beef Rub" — it is a
  single-recipe spice blend fully printed in this file already, with no demonstrated
  reuse elsewhere in the batch; not proposing a new component for it.
- **Readability: A.** Fully measured quantities, temperature-anchored endpoints (155°F,
  195°F), ordered numbered steps, and explicit visual/tactile doneness cues ("dark
  bark," "glaze clings," "cubes sizzle").
- **Decision: keep.** No corrections needed.
- Findings: none (minor note only, not an error) — the rub's absence of salt is
  intentional and matches the source's own stated separate-salting guidance; worth nothing
  further.
- Access failure: amazingribs.com main article and its linked rub sub-page both returned
  403 on direct WebFetch (retried once each); relied on WebSearch snippets as described
  above. Nothing taken from memory.

## kansas-city-cheesy-corn

- Path: `recipes/afc/west/chiefs/kansas-city-cheesy-corn.md` · status: published
- Source: https://www.seriouseats.com/kansas-style-cheesy-corn-recipe-8682405 · hash:
  `0798e321c3b897bf21fbc4c66b3f3fd6a5802f90`
- **City fit — pass, via independent regional evidence (not the source).** Cheesy corn
  is a well-documented Kansas City barbecue side, most closely associated with Fiorella's
  Jack Stack Barbecue's "Cheesy Corn Bake" (per Jack Stack's own site and its Wikipedia
  entry, plus independent write-ups on The Virtual Weber Bullet and House of Nash Eats
  explicitly framed as "Jack Stack Copycat"). America's Test Kitchen/Cook's Country also
  publish a "Kansas City-Style Cheesy Corn" recipe, confirming the dish name is an
  established regional genre, independent of our specific blocked source.
- **Authenticity — plausible accepted variant; genre confirmed independently, exact
  source unverified.** The defining traits reported across independent sources are corn
  + cream cheese + cheddar, cooked to a velvety (not gritty) consistency, with a smoked
  pork product (ATK's version uses both bacon and ham steak, off-heat then broiled). Our
  recipe (ham steak only, all-stovetop, corn-cob "milk" scraped for body, dual
  extra-sharp/smoked cheddar) is consistent with this genre and is a legitimate simpler
  variant, but I could not confirm this is what the cited Serious Eats article itself
  specifies.
- **Source fidelity — access failure, unverified.** WebFetch to www.seriouseats.com
  returned a hard tool-level block ("unable to fetch"), not a retryable HTTP error.
  Multiple WebSearch queries (direct title, ingredient-combination search, "corn milk"
  phrasing) did not surface the actual Serious Eats article text — results returned only
  other publishers' distinct recipes (Plain Chicken, Frugal Hausfrau, Taste of Home,
  America's Test Kitchen, etc.), none of which are the cited source and several of which
  materially differ (bacon instead of/alongside ham, broiler finish). A same-topic
  today.com page (attributed to chef Matt Abdoo) was also fetched; it returned only
  partial metadata (title/times/servings/chef notes) and its notes mention "salty bacon"
  and a broiler technique — contradicting our recipe's ham-only, no-broil method — so it
  was not used as corroboration; it appears to be an unrelated recipe, not a mirror.
  **Ingredient quantities, exact steps, and the specific corn-milk-scraping instruction
  as attributed to Serious Eats remain unverified against the literal source.**
- **Specificity.** "Smoked ham steak," "Diamond Crystal kosher salt (or ½ teaspoon table
  salt)" with an explicit conversion, "full-fat block cream cheese" (vs. spreadable tub),
  and two named cheddar treatments (extra-sharp plus a naturally smoked cheddar, with an
  explicit "avoid artificial smoke flavor" callout) are all concrete, non-generic, and
  usable at the grocery store without further guidance.
- **Components.** Searched `components/sides/`, `components/sauces/`,
  `components/dips/` — nothing fits; this recipe is itself the from-scratch dish, not a
  consumer of a reusable sub-recipe (same reasoning as other from-scratch mains/sides in
  this batch). No new component proposed. No existing `{{component:...}}` markers are
  used in this file.
- **Readability: A** (for the recipe's own clarity, independent of the unresolved
  source-fidelity question above). Fully measured quantities, ordered steps, and
  explicit visual endpoints ("small bubbles appear at the edge," "just melted and
  glossy," "do not boil after cheese goes in").
- **Decision: unresolved.** City fit and dish genre are independently well supported,
  but source fidelity to the specific cited Serious Eats URL could not be checked by any
  available route. Recommend the orchestrator either accept the recipe on genre grounds
  (with the caveat recorded) or attempt access to seriouseats.com through a channel this
  worker does not have (e.g., a cached/mirrored copy, or manual verification).
- Findings: none proposed pending source access, since no confirmed discrepancy exists —
  only an unverified attribution.
- Access failure: www.seriouseats.com is hard-blocked at the tool level; no working
  mirror or republish of this specific article was found despite multiple search
  attempts.

## kansas-city-style-barbecue-chicken

- Path: `recipes/afc/west/chiefs/kansas-city-style-barbecue-chicken.md` · status:
  published
- Source: https://www.qvc.com/recipes/kansas-city-style-smoked-chicken.html · hash:
  `f379d8c2502af6ed6d342b0acc7e45e9979f566d`
- **City fit — pass.** `location: Kansas City, MO`; smoked whole chicken finished with a
  sweet tomato-and-molasses sauce is a standard item at Kansas City barbecue joints and a
  natural companion dish to the region's beef/pork tradition; the sauce style itself
  (ketchup, molasses, cider vinegar, Worcestershire, liquid smoke) matches the
  Kansas-City "sweet, thick, tomato-based" archetype documented for the shared
  `kansas-city-barbecue-sauce` component (not re-reviewed here, per assignment).
- **Authenticity — accepted variant.** Whole smoked bird, dry-rubbed then sauced late in
  the cook to prevent burning the sugars, is standard barbecue technique and a
  reasonable, non-elaborated treatment; no unsupported "copycat of a named restaurant"
  claim is made.
- **Source fidelity — direct fetch blocked (HTTP 418, "I'm a Teapot," retried once,
  same result); corroborated on structure and process, not on every number.** WebSearch
  surfaced verbatim-matching process phrases from the live QVC page, including "Pour
  1/4 cup rub into a smaller bowl..." and a sauce-simmering instruction to "cook for
  5–10 minutes, stirring occasionally" — both consistent with our recipe's step 1–2
  wording and timing. Ingredient list and order (brown sugar, paprika, salt, pepper,
  garlic powder, onion powder, dry mustard, chili powder, cayenne for the rub; ketchup,
  brown sugar, molasses, cider vinegar, Worcestershire, liquid smoke, salt, cayenne for
  the sauce) match what search snippets returned. However, I could not pin every exact
  numeric quantity (¼ cup paprika, 2½ cups ketchup, etc.) to a single verbatim quote from
  the source, since the QVC page itself could not be directly read. Treat numeric
  fidelity as reasonably, not exhaustively, corroborated.
- **Specificity.** "Trussed" whole chicken with a butcher-truss instruction, "mild
  fruitwood or hickory" smoking wood, and a named liquid smoke ingredient are all
  concrete. The rub and sauce ingredient lists are fully generic pantry items
  appropriately left ungated by brand.
- **Components.** Uses `{{component:kansas-city-barbecue-sauce}}` as a whole-sauce
  alternative (marker correctly sits on "about 3 cups finished... sauce, replacing the
  entire sauce mixture above," a finished-item substitution, not a raw ingredient, and
  the recipe explicitly says to omit all eight scratch-sauce ingredients if using it — no
  double-counting). This component is owned by another worker and not re-reviewed here.
  Flag for the orchestrator: `kansas-city-barbecue-sauce` has three total consumers
  (`grep -rl '{{component:kansas-city-barbecue-sauce}}' recipes components`) — this
  recipe, `kansas-city-burnt-ends.md` (both in this batch), and
  `recipes/afc/north/browns/polish-boy-sandwich.md` (outside this batch, not reviewed by
  me). No existing or candidate component fits the poultry dry rub; it differs enough in
  profile from the burnt-ends' "Big Bad Beef Rub" (brown-sugar/paprika-forward vs.
  pepper/ancho-forward) that merging them into one shared rub component is not
  recommended.
- **Readability: A.** Measured rub/sauce quantities, ordered steps, and an explicit
  temperature endpoint (165°F in breast and thigh) rather than relying on smoking time
  alone.
- **Decision: keep**, with the numeric-fidelity caveat above recorded rather than
  silently passed.
- Findings: none confirmed; the only open item is the unpinned exact quantities noted
  above, which is an access limitation, not a known discrepancy.
- Access failure: www.qvc.com returned HTTP 418 on both the initial attempt and one
  retry; relied on WebSearch snippets for partial corroboration as described.

## casino-style-prime-rib

- Path: `recipes/afc/west/raiders/casino-style-prime-rib.md` · status: published
- Source: https://www.foodnetwork.com/recipes/food-network-kitchen/the-best-prime-rib-7422442
  · hash: `8ac1d6b716b3898402c9904364e5b02d67d1756f`
- **City fit — pass, regional serving-style association (not an ingredient-origin
  claim).** `location: Las Vegas, NV`. Independent reporting (Tasting Table's history of
  Vegas buffet prime rib) confirms hand-carved prime-rib carving stations have been a
  defining, decades-long fixture of Las Vegas casino buffets since the 1940s–50s (The
  Last Frontier's table-side prime rib dinner), which is exactly the framing this recipe
  uses ("casino-style carving-station roast"). The roast formula itself is a generic
  standing-rib-roast method, not claimed as Vegas-specific, which is the correct,
  non-overclaimed framing.
- **Authenticity — pass, generic technique correctly labeled.** Low-and-slow roast to
  120°F, rest, then high-heat blast to crisp the fat cap, is a standard, well-supported
  method for a standing rib roast; no unsupported claim of a specific casino's proprietary
  method is made anywhere in the file.
- **Source fidelity — verified, full match.** Source fetched directly (200 OK). Roast
  size (7–8 lb, 3-rib), salt/pepper/garlic prep, 4-hour-to-overnight salting, 250°F roast
  to 120°F center (~4 hours), 1-hour rest with 10–14°F carryover, 500°F browning for
  10–15 minutes, and final 30-minute rest all match the source exactly. No discrepancies
  found.
- **Specificity.** "3-rib standing beef rib roast," coarsely ground black *or tricolor*
  peppercorns, and kosher salt are all concrete; photo credit (Certified Angus Beef) is
  an appropriate stock-photo attribution for a generic cut, not a false restaurant claim.
- **Components.** Uses `{{component:prime-rib-pan-jus}}` and
  `{{component:prime-rib-horseradish-cream}}`, both under "For serving," each marked
  "Optional" and each a genuine finished-item substitution (not present in the literal
  Food Network source, which the recipe honestly discloses: "au jus if desired (not
  included in source recipe)"). Both components are exclusively assigned to me; see their
  own sections below. `grep -rl` confirms this recipe is the *only* consumer of both
  components — no other recipe reaches them, so no cross-batch flag is needed. No
  double-counting: the pan jus is prepared once from the roast's own drippings, and the
  horseradish cream is prepared once and refrigerated ahead, exactly as the recipe's
  step 1 and step 4 describe.
- **Readability: A.** Precise temperatures throughout (120°F, 500°F, 10–14°F carryover),
  ordered numbered steps, and explicit timing for every stage.
- **Decision: keep.** No corrections needed.
- Findings: none.
- No access failures for this recipe.

## old-vegas-shrimp-cocktail

- Path: `recipes/afc/west/raiders/old-vegas-shrimp-cocktail.md` · status: published
- Source: https://www.lasdiscounts.com/post/bring-las-vegas-to-your-table-the-iconic-vegas-shrimp-cocktail-recipe
  · hash: `6b480b039e7e2de1f64279069cd835fe31a23a48`
- **City fit — pass, well-documented icon.** `location: Las Vegas, NV`. Independent
  reporting (Tasting Table, Golden Gate Hotel & Casino's own history page, Las Vegas Sun,
  KTNV) confirms the Golden Gate's 50-cent (later 99-cent) shrimp cocktail, introduced in
  1959 by Italo Ghelfi, is one of the most iconic, specifically Las Vegas food traditions,
  served in tulip/sundae glasses with a ketchup-based cocktail sauce and shredded cabbage
  — matching this recipe's glassware and sauce framing closely.
- **Authenticity — honestly labeled as an approximation, not an overclaim.** The
  original Golden Gate sauce is independently confirmed to be "a secret recipe... closely
  guarded for decades" (per the casino's own history page), and this recipe's own Kitchen
  Notes already state "the original Golden Gate sauce formula is undisclosed" — a
  correctly labeled home approximation rather than an unsupported copycat claim. This is
  good practice and needs no correction.
- **Source fidelity — verified, full match.** Source fetched directly (200 OK). Shrimp
  type/prep, sauce ingredients and proportions (ketchup, bottled chili sauce, prepared
  horseradish, lemon juice, Worcestershire, optional hot sauce), chilled-glass technique,
  and serving order all match the source exactly. No discrepancies found.
- **Specificity.** "Small cooked salad shrimp, peeled, deveined and tail-off" and named
  "Heinz Chili Sauce (not hot chile sauce)" — an important, correctly flagged distinction
  since "chili sauce" and "chile sauce/hot sauce" are commonly confused — are both
  concrete and well-chosen.
- **Components.** No `{{component:...}}` marker is used in this file; the cocktail sauce
  is fully inline. Note for the orchestrator to avoid batch-confusion: this recipe does
  *not* use `components/sauces/horseradish-cocktail-sauce.md` — that component's only
  consumer (confirmed via `grep -rl`) is
  `recipes/afc/south/colts/st-elmo-style-shrimp-cocktail.md`, a different (St. Elmo-style)
  shrimp cocktail recipe outside this batch. No new component proposed here: the sauce is
  a small, single-use whisked mixture with no demonstrated reuse elsewhere, so
  componentizing it would not add meaningful value per the coverage check.
- **Readability: A.** Fully measured quantities, ordered steps, explicit chill time (20
  minutes), and a clear serving endpoint.
- **Decision: keep.** No corrections needed.
- Findings: none.
- No access failures for this recipe. Note: I could not independently corroborate
  `lasdiscounts.com`'s general editorial credibility (no independent coverage of the site
  itself was found), but this does not bear on source fidelity, since the literal source
  page was read directly and matches our transcription word-for-word on every
  ingredient/step.

## component:prime-rib-horseradish-cream

- Path: `components/toppings/prime-rib-horseradish-cream.md` · status: published
- Source: https://altonbrown.com/recipes/horseradish-cream-sauce/ · date checked:
  2026-09-26 · hash: `9ec444f05bdb46f64f439637f13e0003ce5ec865`
- **Source fidelity — verified, full exact match.** Source fetched directly (200 OK).
  All six ingredients (sour cream, fresh horseradish root, Dijon mustard, white wine
  vinegar, kosher salt, black pepper) and both instruction steps (whisk together; cover
  and refrigerate at least 4 hours) match the source exactly, including the choice of
  fresh grated horseradish root over jarred prepared horseradish.
- **Specificity.** "Finely grated fresh horseradish root" (vs. jarred prepared) and
  named Dijon mustard are concrete and correctly distinguish a cream sauce built on fresh
  root from a simpler jarred-horseradish approach; the component's own Note correctly
  flags this distinction for a home substitution ("use well-drained plain prepared
  horseradish and adjust vinegar after tasting").
- **Consumers:** `grep -rl '{{component:prime-rib-horseradish-cream}}' recipes
  components` returns only `recipes/afc/west/raiders/casino-style-prime-rib.md`. Single
  consumer, already reviewed above in this same report; no cross-batch flag needed.
- **Readability: A.** Precise quantities, two ordered steps, explicit 4-hour chill
  endpoint.
- **Decision: keep.** No corrections needed. This is a faithful, correctly attributed
  scratch component with an appropriate, clearly labeled purchased alternative
  (`quick_buy`: refrigerated creamy horseradish, e.g. St. Elmo Creamy Horseradish).
- Findings: none.
- No access failures.

## component:prime-rib-pan-jus

- Path: `components/sauces/prime-rib-pan-jus.md` · status: published
- Source: https://www.foodnetwork.com/recipes/bobby-flay/roast-prime-rib-with-thyme-au-jus-recipe-1944997
  · date checked: 2026-09-26 · hash: `9802373d51b44804b313df2f8a3a0dbe990bbb00`
- **Source fidelity — verified as an accurately proportioned half-batch, with one minor
  wording deviation.** Source fetched directly (200 OK). The source's full-batch formula
  (2 cups red wine, 4 cups beef stock, 1 tablespoon/3 teaspoons chopped thyme) is halved
  exactly in our component (1 cup wine, 2 cups stock, 1½ teaspoons thyme) — confirmed
  correct on every quantity. Method (defat pan, keep browned bits, reduce wine by half,
  add stock, reduce further, add thyme, season) matches in sequence.
  - **Minor finding:** current text (step 3) reads "simmer until reduced by about
    one-third to one-half," but the source specifies a single target, reduced "by half."
    Proposed correction: "Add beef stock and simmer until reduced by about half," matching
    the source's one stated endpoint. Rationale: the added range is an unlabeled editorial
    hedge not present in the source; stopping at a one-third reduction (the low end of our
    current range) would yield a thinner, less concentrated jus than the source intends.
    Severity: minor. Confidence: high (source text directly confirmed by direct fetch in
    this session). Supporting URL: the source URL above; relevant section: `## From
    Scratch`, step 3.
- **Specificity.** "Dry red wine, such as Cabernet Sauvignon or Merlot (not sweet cooking
  wine)" is a well-chosen, correctly-scoped style recommendation with a helpful negative
  example; "low-sodium beef stock" appropriately anticipates the salt note in `## Note`.
- **Consumers:** `grep -rl '{{component:prime-rib-pan-jus}}' recipes components` returns
  only `recipes/afc/west/raiders/casino-style-prime-rib.md`. Single consumer, already
  reviewed above; no cross-batch flag needed.
- **Readability: B.** Otherwise fully measured and ordered, but the reduction-range
  wording in step 3 is a minor ambiguity about the actual doneness endpoint (per the
  grading rubric's "minor ambiguity" tier), addressed in the finding above.
- **Decision: targeted fix.** Tighten the step-3 reduction wording to match the source's
  single stated target; no other change needed. The `quick_buy` purchased alternative
  (prepared beef au jus) remains appropriate and correctly labeled as a jus rather than a
  gravy.
- No access failures.
