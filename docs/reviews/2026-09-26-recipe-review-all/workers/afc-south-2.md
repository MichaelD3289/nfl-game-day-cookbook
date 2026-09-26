# Worker batch: afc-south-2

Date checked: 2026-09-26. Assigned recipes: 5. Assigned shared components: none.

## sausage-kolaches-or-klobasneks

- Path: `recipes/afc/south/texans/sausage-kolaches-or-klobasneks.md` · status: published
- Source: https://www.kingarthurbaking.com/recipes/kolaches-sweet-savory-recipe
- Input hash: `e382cef483b59ad2b17bb75bc5aa105882e40285`

**City fit: pass.** Klobasnek/sausage-kolache is broadly a Central Texas Czech-belt
tradition (West, TX; Village Bakery, 1950s), but Houston has its own strong,
independently documented claim: Kolache Factory, one of the format's largest
commercial popularizers, was founded in Houston in 1982 (kolachefactory.com/about).
Regional adoption of a dish that originated elsewhere is valid per the brief;
Houston's association is civic/commercial, not the origin point, and the recipe
correctly does not claim otherwise.

**Authenticity: accepted variation, evidence-supported.** King Arthur's own page
presents both a sweet fruit/cheese kolache and a savory sausage-filled klobasnek
variant from the same base dough; our recipe follows the savory variant as
published. Classification: home/bakery-style adaptation of the tradition, not a
copycat of any specific restaurant. Some sources (e.g., Houston Chronicle "kolache
vs. klobasnek" explainers) distinguish klobasnek purists' use of a cased
kielbasa-style link from a milder breakfast-sausage link; King Arthur's own
ingredient list specifies "breakfast sausage links" too, so this is a source-match,
not a transcription error — flagged only as a specificity note below, not an
authenticity finding.

**Source fidelity: pass, close match.** Dough ingredients/quantities (sour cream,
sugar, salt, butter, yeast, water, eggs, flour), overnight refrigeration, 20-piece
division, ~1 hour final rise, 350°F/15–20 min bake all match the source. Minor,
non-substantive omissions versus source: source mentions greasing the rising
pan/lining with parchment; our recipe omits this prep detail without changing
technique or outcome (severity: minor, confidence: high).

**Specificity:**
- Finding (minor, confidence: medium): "20 small cooked breakfast sausage links"
  is a direct source match, but purist klobasnek versions commonly use a
  smoked, cased kielbasa-style link rather than a breakfast-sausage link. Proposed
  addition: a parenthetical noting "(or a small smoked kielbasa-style link for a
  more traditional klobasnek profile)". Rationale: gives readers the style choice
  without contradicting the cited source. URL: kingarthurbaking.com source page;
  corroborating regional distinction from Houston Chronicle klobasnek explainer
  (search-snippet corroboration only, not separately fetched).
- "Yellow mustard" and "shredded cheddar" are left generic and optional — appropriate,
  no brand needed for an optional to-taste filling.

**Components:** checked `components/toppings/american-yellow-mustard.md` (existing
scratch yellow-mustard recipe with a French's Classic Yellow quick-buy note). It is
a plausible match for the recipe's optional "yellow mustard" filling, but that
ingredient is optional and used to taste as a raw condiment, not a defining,
repeated element — Finding (minor, confidence: high): could reference
`{{component:american-yellow-mustard}}` in place of the raw "yellow mustard" line
if the orchestrator wants full Make-It-or-Buy-It coverage on optional condiments;
not required for this recipe to pass. No other existing component matches the
dough or sausage filling (checked `components/` breads/proteins categories — none
present for a kolache/klobasnek dough or breakfast sausage link). Not proposing a
new shared component: this dough is single-recipe-specific in this batch, and no
other consumer was found.

**Readability: A.** Clear quantities (weights and volumes given together), ordered
steps, clear visual/time endpoints (golden, 15–20 min; puffy after ~1 hr rise).

**Decision: keep.** No material fidelity problems; only optional specificity/
component suggestions above.

**Findings:** see specificity and components items above (both minor, optional).

**Replacement candidates:** none proposed.

**Access failures or unverified claims:** none. kingarthurbaking.com fetched
successfully.

---

## viet-cajun-crawfish

- Path: `recipes/afc/south/texans/viet-cajun-crawfish.md` · status: published
- Source: https://roadfood.com/recipes/viet-cajun-crawfish-recipe-houston-tx/
- Input hash: `7b97e8dd4fac717e1099b0171a9c1e60b4a669b0`

**City fit: pass, strong.** Viet-Cajun crawfish is a well-documented,
Houston-specific fusion style that emerged from the city's post-Katrina/post-1975
Vietnamese-American community (Crawfish & Noodles, Cajun Kitchen), reported by
Houston Chronicle, Houstonia Magazine and Texas Monthly. This is a defining
Houston dish, not merely a regionally adopted one.

**Authenticity: accepted regional variant matching the cited source.** The
garlic-lemongrass butter finish over a Cajun-seasoned boil matches the widely
reported Viet-Cajun template. Some independently found Viet-Cajun recipes add fish
sauce and/or MSG to the butter sauce; our recipe (and its cited Roadfood source, per
available evidence) omits these, representing one legitimate published variant
among several, not a fabricated one. No claim is made to any single restaurant's
proprietary formula.

**Source fidelity: targeted-fix findings, moderate confidence overall (see access
failure below).**
- Finding (minor–moderate, confidence: medium): current text lists "Zatarain's ...
  (or Old Bay for a milder, celery-salt-forward profile)," presenting Zatarain's as
  primary and Old Bay as the alternative. Search-snippet evidence of the source page
  indicates it lists the two as an either/or pair with Old Bay named first ("Old Bay
  or Zatarain's..."). Proposed correction: present both as equivalent either/or
  options rather than implying Zatarain's is the default, or confirm via a
  successful direct fetch before changing. Rationale: avoid reversing the source's
  framing without confirmation. URL: roadfood.com source (fetch blocked, see below).
  Section: Ingredients.
- Finding (minor, confidence: low-medium): "2½ gallons water" has no confirmed match
  in the visible source snippet (which did not show an explicit water quantity in
  the portion retrievable via search). This may be an editorial estimate scaled to
  the stated 4 lb crawfish/1.5 lb potatoes/3 ears corn, which is plausible, but it
  should be labeled as an editorial estimate rather than presented as sourced.
  Section: Ingredients.
- Matches confirmed at high confidence via search-snippet corroboration: butter
  sauce (2 tablespoons minced lemongrass, 6 garlic cloves, 2 tablespoons lemon
  juice, 1 teaspoon cayenne, 1 cup/2 sticks butter), 4 lb crawfish, 1.5 lb quartered
  red potatoes, 3 halved ears of corn, divided salt in two ¼-cup portions, ~8 minute
  crawfish boil time.

**Specificity:** Old Bay described as "milder, celery-salt-forward" and Zatarain's
implied more assertive — this flavor characterization is accurate to each product's
actual profile (independently well known), the issue is only the ordering/emphasis
noted above, not the description itself.

**Components:** checked `components/seasonings/cajun-seasoning.md` — this is a dry
all-purpose Cajun/Creole seasoning blend (garlic powder, onion powder, paprika,
thyme, oregano, cumin, etc.), a different product from a specialty wet crab/crawfish
boil seasoning (Zatarain's/Old Bay boil blend, which includes mustard seed, bay,
allspice, whole spices for boiling). Not a match; ruled out. No existing component
matches the garlic-lemongrass butter sauce; not proposing a new shared component
since no other recipe in this batch or found via grep uses it.

**Readability: A.** Clear quantities, ordered two-stage boil sequence, clear visual
endpoint (crawfish bright red, cooked through, ~8 min).

**Decision: targeted fix.** Reframe the Zatarain's/Old Bay either-or language to
match the source's framing (or confirm current framing via a successful direct
fetch), and label the water quantity as an editorial estimate.

**Replacement candidates:** none proposed; the source is appropriate and
well-matched to the dish, the issues found are transcription-emphasis/labeling, not
grounds for replacement.

**Access failures:** `roadfood.com` returned HTTP 403 on two attempts (including one
retry); could not be fetched directly. Findings above rely on WebSearch
result-snippet corroboration only, which is partial: high confidence on the butter
sauce and produce/protein quantities, lower confidence on the exact wording/ordering
of the boil-seasoning options and no confirmation at all of an explicit water
quantity in the source. Recommend the orchestrator retry the direct fetch later or
locate a mirror.

**Other note (not one of the five checks, flagging for orchestrator):** `photo_credit`
is "Houston Chronicle / Chron" while `source.url` is roadfood.com — a chocolatey
photo-credit/source mismatch worth a quick check, not a content-fidelity issue.

---

## goo-goo-clusters

- Path: `recipes/afc/south/titans/goo-goo-clusters.md` · status: published
- Source: https://globalbakes.com/goo-goo-clusters/
- Input hash: `934642c1af306ff25903c0eb6ad31340fd36cd1a`

**City fit: pass, strong.** Goo Goo Clusters originated at Standard Candy Company,
Nashville, in 1912, widely credited as the first combination candy bar
(corroborated via multiple independent regional/food-history sources).

**Authenticity: openly labeled scratch interpretation, well executed.** The
recipe's Kitchen Notes explicitly disclose that this is "a fully from-scratch
interpretation," that the source's honey nougat is firmer than the commercial
marshmallow nougat, and that the milk-chocolate coating matches the original
candy. Independent evidence confirms the original Goo Goo Cluster composition is
marshmallow nougat + caramel + peanuts + milk chocolate, so the milk-chocolate
choice is an accurate, correctly-labeled restoration of the original character even
though it's a documented swap from the cited source's own recommendation. This is
a model of a disclosed adaptation, not a fidelity error.

**Source fidelity: targeted-fix finding (minor).**
- Finding (minor, confidence: high): source instructs kneading the nougat several
  turns on a cornstarch-dusted surface before spreading/cutting (helps even out
  temperature and texture); our Instructions step 2 only says "Spread on a
  cornstarch-dusted surface," omitting the kneading step. Proposed correction: add
  "knead briefly" before spreading. Rationale: minor technique omission that could
  affect nougat texture consistency for readers following the recipe closely. URL:
  globalbakes.com/goo-goo-clusters/. Section: Instructions, step 2.
- All other quantities (egg whites, sugars, honey, corn syrup, water for nougat;
  condensed milk, butter, sugar, corn syrup, salt, vanilla, peanuts for caramel;
  syrup temperatures 310°F→320°F→300°F; caramel to 250°F; tempering curve
  113°F→81°F→84–86°F) match the source, with the chocolate-type swap already
  disclosed above. Yield (12) matches.

**Specificity:** Finding (minor, optional, confidence: n/a — suggestion only):
"good-quality milk chocolate" is generic; since the tempering instructions already
cite Callebaut guidance, naming a specific milk-chocolate product (e.g., Callebaut
or Ghirardelli milk chocolate) would be consistent and useful for sourcing, without
claiming it's the only acceptable option.

**Components:** checked `components/` sauces/staples/toppings — no existing nougat
or caramel component. Not proposing new shared components: both are single-recipe,
technique-specific preparations with no other consumer found in this batch. Buy-it
alternative (a purchased Original Goo Goo bar) is already given in Kitchen Notes —
good coverage.

**Readability: B.** Instructions are clear, ordered and give concrete temperatures
for the technique-sensitive stages, but "cool several hours" and "let set 2–4
hours" are vague windows for a candy-making process, and the missing kneading step
(above) removes a small amount of actionable detail a home cook would need for
consistent texture.

**Decision: keep.** Well-labeled interpretation with strong evidence support;
minor targeted fix optional (kneading step, chocolate brand example).

**Replacement candidates:** none; source is appropriate and well-matched.

**Access failures or unverified claims:** none. globalbakes.com fetched
successfully.

---

## meat-and-three-plate-with-meatloaf

- Path: `recipes/afc/south/titans/meat-and-three-plate-with-meatloaf.md` · status: published
- Source: https://thelocalpalate.com/recipes/arnolds-meatloaf-with-tomato-creole-sauce/
- Input hash: `e0b67374d1c0a6f4e8eccfcae7e92815e5886ce9`

**City fit: pass, strong.** Nashville's "meat-and-three" tradition is well
documented, and Arnold's Country Kitchen is a nationally recognized Nashville
meat-and-three institution (James Beard America's Classic award, 2009). Current
chef/owner Kahlil Arnold, son of founders Jack and Rose Arnold, is accurately
attributed (corroborated via Southern Foodways Alliance and local press coverage).

**Authenticity: restaurant-sourced recipe for the entrée/sauce; disclosed homestyle
sides.** The meatloaf and Tomato Creole sauce are Arnold's own published recipe via
The Local Palate, a credible regional food magazine — this is the strongest
sourcing tier (a restaurant's own recipe). The three sides (turnip greens, mac and
cheese, green beans) are honestly labeled in Kitchen Notes as "homestyle pairings,
not represented as Arnold's exact daily side recipes" — correctly disclosed, not a
false attribution, and consistent with the genre (meat-and-three sides rotate daily
and are not a fixed printed "recipe" at this or most such restaurants).

**Source fidelity: pass, with one minor specificity-level finding (see below).**
Meatloaf ingredients (onion, celery, garlic, salt, pepper, granulated garlic, beef
broth, Worcestershire, eggs, bread crumbs, 2½ lb 80%-lean ground chuck), 350°F/~50
min bake to 165°F, 10-minute rest, and sauce ingredients (olive oil, onion, celery,
garlic, 4 cups ketchup, horseradish, basil, oregano, tomato, pepper/salt/granulated
garlic, sugar, Worcestershire) all match the source. The recipe correctly notes the
4-cup ketchup quantity "yields extra," consistent with the source as printed
(editorial honesty about scale, not a silent change).

**Specificity:**
- Finding (minor, confidence: high): source specifies "Heinz" ketchup; our recipe
  generalizes to "ketchup" (brand dropped). Proposed correction: "4 cups ketchup
  (such as Heinz, per source)". Rationale: minor brand specificity per the
  source-fidelity guidance to name brands the source itself calls for. URL:
  thelocalpalate.com source. Section: Ingredients, Tomato Creole sauce. Severity is
  low since generic ketchup is otherwise adequate.

**Components:** checked `components/sauces/`, `components/sides/`, `components/staples/`
— no existing component for tomato-Creole sauce, turnip greens, baked mac and
cheese, or Southern green beans. Not proposing new shared components in this batch:
no other recipe consumer was identified via grep for these side names. Flagging for
the orchestrator: if other Southern-division recipes in later batches use turnip
greens, mac and cheese or green beans as sides, it may be worth extracting one or
more as shared components rather than duplicating across recipes.

**Readability: A.** Each of the four sub-recipes (meatloaf, sauce, greens, mac and
cheese, green beans) has clear quantities, ordered steps and explicit endpoints
(165°F center, 35–45 min "until set," tenderness times for the vegetable sides).

**Decision: keep.** Strong, well-attributed source with only a trivial optional
brand-naming fix.

**Replacement candidates:** none; source is a strong, credible restaurant-sourced
recipe.

**Access failures or unverified claims:** none. thelocalpalate.com fetched
successfully.

---

## nashville-hot-chicken

- Path: `recipes/afc/south/titans/nashville-hot-chicken.md` · status: published
- Source: https://www.bonappetit.com/recipe/nashville-style-hot-chicken
- Input hash: `86eb3046f0b2451eabcf8985ed0c785878da2125`

**City fit: pass, strong.** Nashville hot chicken is the city's defining dish,
originating at Prince's Hot Chicken Shack; this is well documented across
independent food-history sources and not disputed.

**Authenticity: media-recipe adaptation of an established local style, not a
proprietary restaurant formula (and no claim to one is made).** The recipe's
defining traits — buttermilk/egg-hot-sauce dredge, seasoned flour, deep-fry, then a
cayenne-forward hot-oil paste brushed on, served on white bread with pickle slices
— match the widely reported Nashville hot chicken template. Classification: credible
national-media rendition of the local style. Good, accurate framing; nothing here
overclaims restaurant-specific authenticity.

**Source fidelity: mostly corroborated via search snippets; direct fetch blocked
(see access failure below), so confidence is capped at "corroborated," not
"confirmed."**
- Matches found via WebSearch-snippet corroboration (confidence: medium-high, not
  a direct read): 2 chickens (3½–4 lb each) cut into 10 pieces; 4 eggs; 2 cups
  buttermilk or whole milk; 2 tablespoons vinegar-style hot sauce; 4 cups flour; 1
  tablespoon black pepper; 6 tablespoons cayenne (with a milder 2-tablespoon option);
  2 tablespoons dark brown sugar; 1 teaspoon each chili powder/garlic powder/paprika;
  dredge sequence (egg-buttermilk-hot sauce wash, seasoned flour, twice); ~2 inches
  oil at 325°F in a Dutch oven; spice paste loosened with hot frying oil; salt
  dry-cure refrigerated at least 3 hours.
- Unverified (no search corroboration located for these specific details, confidence:
  low): the divided dual-brand salt amounts ("2 tablespoons plus 4 teaspoons Diamond
  Crystal kosher salt, divided... or 1 tablespoon plus 2 teaspoons Morton kosher
  salt"), the exact "about 10 cups" oil volume, and the 165°F doneness callout as
  phrased. These are plausible (Diamond Crystal/Morton dual-listing is a standard
  Bon Appétit convention) but remain unconfirmed against the primary text.
- One item flagged and deliberately NOT reported as fact: a WebSearch result
  characterized the Bon Appétit recipe as "based on... Hattie B's," but no reliable
  source corroborated this claim, so it is not included as an established
  attribution and should not be added to the recipe or its Kitchen Notes without
  independent confirmation.

**Specificity:** Hot sauce brand alternatives (Crystal, Frank's RedHot) with an
"adjust brand to preference" disclaimer — good practice, avoids over-claiming a
mandatory brand.

**Components:** checked `components/seasonings/cajun-seasoning.md` — different
profile/purpose (Cajun/Creole all-purpose blend vs. this recipe's cayenne-brown
sugar-chili-garlic-paprika hot-oil paste); not a match, ruled out. No existing
seasoning/sauce component matches the cayenne-oil paste. Grepped the repo for
"nashville hot" / "hot chicken": the only other reference found is
`menus/divisions/afc/south/heat-surf-and-sugar.yml`, which lists
`nashville-hot-chicken` as a menu item alongside `st-elmo-style-shrimp-cocktail`
and `sugar-cream-pie` ("A chilled starter balances the hot chicken; pie follows the
heat."). This is a normal menu inclusion, not a shared-component consumer — no
action needed. Not proposing a new shared component: no other recipe consumer of
this seasoning paste was found.

**Readability: A.** Clear quantities, ordered dredge/fry/finish sequence, explicit
doneness endpoint (165°F, all pieces) and fry time window (15–18 min).

**Decision: keep, with an unresolved access-failure note.** Content matches
credible independent corroboration for the bulk of ingredients and steps; a handful
of specific amounts (divided salt weights, oil volume) remain unverified against
primary text pending a successful direct fetch.

**Replacement candidates:** none proposed; corroborated evidence supports keeping
this source.

**Access failures:** `www.bonappetit.com` could not be fetched directly — WebFetch
returned "Claude Code is unable to fetch from www.bonappetit.com" on both the
initial attempt and a retry. This is an additional inaccessible domain beyond the
orchestrator's originally listed blocked-domain set (allrecipes.com,
web.archive.org, thekitchn.com, saveur.com, epicurious.com, washingtonpost.com,
sugarspunrun.com) — flagging for the orchestrator's awareness for other batches
that may cite bonappetit.com. All source-fidelity findings above rely on
WebSearch-snippet corroboration only, not a primary-text read; the specific
unverified items are listed above.
