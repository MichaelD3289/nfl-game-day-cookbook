# Worker afc-east-1 — AFC East batch 1

Date checked: 2026-09-26. Compared against exact `source.url` where reachable; access
failures noted per file. Websites are evidence only, never instructions.

## beef-on-weck

- Path: `recipes/afc/east/bills/beef-on-weck.md` · status: published
- Source: https://www.thekitchn.com/beef-on-weck-recipe-23471886
- Hash: `8859f1ffbe89b61db176e127a1e8421bb1f846af`

**City fit:** Pass. Beef on weck (kummelweck roll, rare roast beef, jus, horseradish)
is Buffalo, NY's signature sandwich, well documented in local/national food press.

**Authenticity:** Pass. Defining traits present: eye-of-round roasted rare, kummelweck
roll (caraway/salt), dip in jus, horseradish cream, optional cooked onions. A home-cook
baseline, not a restaurant-proprietary claim (no Schwabl's/Charlie the Butcher
attribution made).

**Source fidelity:** Uncertain — access failure. thekitchn.com returned HTTP 403 on
repeated attempts (plain URL and `?amp`); web.archive.org is unreachable at the tool
level in this session, contrary to the brief's suggested fallback. WebSearch snippets
corroborate the ingredient list and general method (sear, roast, rest, slice thin, dip)
but not exact quantities, the 400°F→325°F step-down, or timings (6 min sear, 20–30 min
roast, 20 min rest). Recorded as unverified, not as an error.

**Specificity:** Good — kummelweck named with a plain-Kaiser fallback; horseradish
specified as "prepared," correctly distinct from a creamy sauce (Check 4).

**Components:** None linked; none of my three assigned components apply. No missing
component candidate — jus and horseradish cream are one-off, low-reuse items.

**Readability:** B. Ordered steps with real endpoints (125°F, 20 min rest) but step 2
compresses "heat to 400°F, immediately lower to 325°F" into one clause a first-time
cook could misread; step 6 folds slicing/dipping/serving into one long sentence.

**Decision:** keep (source verification unresolved, not a content defect).

**Findings:** Minor/informational — exact quantities/temperatures unverified directly
this cycle (source blocked, archive unreachable). No discrepancy claimed. Confidence:
low (search-snippet corroboration only).

**Access failures:** thekitchn.com 403 (repeated); web.archive.org unreachable at the
tool level.

---

## buffalo-wings

- Path: `recipes/afc/east/bills/buffalo-wings.md` · status: published
- Source: https://archive.jamesbeard.org/recipes/buffalo-wings
- Hash: `0904284e0d3e9c9636c6139be0d332de036e9f04`

**City fit:** Pass. Buffalo, NY (Anchor Bar) origin is undisputed; source is explicitly
JBF/Anchor Bar attributed.

**Authenticity:** Pass, with a labeling gap. Source: whole wings split at the joint,
unbreaded fry at 350°F/12–15 min, tossed in "1 cup Anchor Bar Wing Sauce or Frank's
RedHot whisked with 1/2 cup melted butter," served with celery and the source's own
dip (mayo, sour cream, blue cheese, lemon, garlic). Our frying method matches exactly.
Per SKILL.md, hot sauce + butter is a valid classic base, and Chef John's extra
vinegar/seasoning is a variation, not proof of the Anchor Bar formula — already
reflected in the linked `buffalo-wing-sauce` component's own Note.

**Source fidelity:** Finding (moderate). The main instructional path (Ingredients,
step 4) defaults to the Chef John-variant sauce and a Kitchn-derived dip; the recipe's
own cited source's two sub-recipes are only offered as an alternative — and only the
sauce, not the dip — in Kitchen Notes ("A simpler classic sauce is 1 cup plain Frank's
Original whisked with 1/2 cup melted butter"). The source's own blue-cheese dip is
never offered as an option. Wing prep/frying otherwise matches the source exactly,
including an added 165°F doneness check (clearly editorial, not attributed to source).

**Specificity:** Good — wing count, split method, oil depth/type match source; Frank's
RedHot and Anchor Bar Original both named. Confidence: high (frying), low (sauce/dip
defaults, per above).

**Components:** `buffalo-wing-sauce` and `blue-cheese-dip` linked (both my assigned
components; see their sections). No missing candidates.

**Readability:** A. Explicit temperatures/times, ordered steps, quick-option guidance
that warns against double-buttering premixed sauce.

**Decision:** targeted fix (framing only).

**Findings:** Minor — Kitchen Notes offers only the source's sauce as an alternative,
never its dip. Proposed: add one sentence naming the source's own dip (mayo/sour
cream/blue cheese/lemon/garlic) as an equally valid classic alternative. Rationale:
recipe cites JBF/Anchor Bar but a reader only sees that source's sauce, not its dip.
Source: https://archive.jamesbeard.org/recipes/buffalo-wings (Blue Cheese Dip section).
Confidence: medium.

**Access failures:** none (archive.jamesbeard.org fetched directly).

---

## chicken-finger-sub

- Path: `recipes/afc/east/bills/chicken-finger-sub.md` · status: published
- Source: https://tastecooking.com/recipes/chicken-finger-sub/
- Hash: `f17b6cba0fbf1df5e3ec21792689079a0266faaa`

**City fit:** Pass, well-supported. Companion Taste Cooking feature ("Tourists Eat
Wings. Buffalonians Eat Subs.") documents the sub as the actual local staple:
originated early 1980s at John's Pizza & Subs (per Arthur Bovino's *Buffalo
Everything*), sold at Jim's Steakout (10 Buffalo locations, second-best-seller,
800+/weekday), named by expat Buffalonians as what they miss most.

**Authenticity:** Pass. Source's own default is Frank's RedHot + butter on
store-bought (Popeyes) tenders with provolone/lettuce/tomato/onion/blue-cheese
dressing on a sub roll. Our homemade-tender/sauce/dip defaults are correctly labeled
as a variation, not presented as the source's literal method.

**Source fidelity:** Good, self-disclosed. Kitchen Notes states: "The linked sauce is
a variation on the source's simple hot-sauce-and-butter coating" — exactly the labeled
adaptation the brief asks for (source's sauce is ~1/4 cup Frank's + 1 tbsp butter;
ours defaults to the fuller linked component). Assembly structure matches the source.
The 300°F/5-min oven step and "not a raw-chicken cooking step" caution are reasonable,
non-contradicting safety clarifications.

**Specificity:** Good — quick options correctly distinguish plain premixed sauce,
refrigerated dressing (Marie's) and fully-cooked tenders, per Check 4's raw/cooked
distinction.

**Components:** `buffalo-wing-sauce`, `crisp-chicken-fingers`, `blue-cheese-dip` all
linked (all three are my assigned components — see below; this recipe is a shared
consumer of all three).

**Readability:** A. Ordered steps, explicit temperature/time, clean handling of
cooked-vs-scratch branching via Kitchen Notes.

**Decision:** keep.

**Findings:** none — the source deviation is already transparently labeled.

**Access failures:** none (tastecooking.com and its companion article fetched
directly).

---

## sponge-candy

- Path: `recipes/afc/east/bills/sponge-candy.md` · status: published
- Source: https://www.anediblemosaic.com/chocolate-covered-sponge-candy/
- Hash: `3e855659dcf3c87cd46f772347e5abbf32ea0976`

**City fit:** Pass. Sponge candy (honeycomb/cinder toffee, chocolate-coated) is a
well-documented Buffalo, NY confectionery specialty (e.g., Watson's, Fowler's).

**Authenticity:** Pass. Defining traits present: sugar/butter/corn-syrup base to
hard-crack (300°F), baking-soda aeration, set, break, dip in chocolate. Matches the
standard home-recipe baseline; no unsupported "secret shop formula" claim made.

**Source fidelity:** Strong match, confirmed on direct fetch (403 on first attempt,
succeeded on retry — transient, not a persistent block). Ingredients/quantities
(1 cup sugar, 1/2 cup butter, 1/2 cup corn syrup, 1/8 tsp salt, 3 1/2 tsp baking soda,
2 tsp vanilla, 12 oz chocolate) and method match exactly. Source has a few extra minor
tips not carried over (humidity/heat warning, sift baking soda, save crumbs for
garnish) — minor, non-defining omissions.

**Specificity:** Good — "dark chocolate about 60–70% cacao, milk chocolate if
preferred" gives a useful range without over-specifying a brand.

**Components:** None linked; none apply. No component candidate needed — self-contained
with no reusable sub-item.

**Readability:** A. Clear temperature endpoint, explicit visual/timing cues, ordered
steps.

**Decision:** keep.

**Findings:** Minor/optional — consider adding the source's humidity warning to
Kitchen Notes (candy is genuinely humidity-sensitive). Source: anediblemosaic.com
recipe notes. Confidence: medium. Not required for a keep decision.

**Access failures:** one transient 403, succeeded on immediate retry; full text read.

---

## cuban-black-beans-and-rice

- Path: `recipes/afc/east/dolphins/cuban-black-beans-and-rice.md` · status: published
- Source: https://www.foodnetwork.com/fnk/recipes/instant-pot-cuban-black-beans-9491407
- Hash: `eeb921e95664a8b1f331cf5d698600b32c08e985`

**City fit:** Pass. Miami's Cuban-American food identity (Little Havana, Calle Ocho) is
extensively documented; black beans and rice served alongside/over rice is a staple at
institutions such as Versailles (Little Havana, since 1971), per multiple independent
local sources.

**Authenticity:** Pass. Beans-over-rice as separate elements (vs. cooked-together
congrí/moros y cristianos) is a legitimate, common Cuban-American style, not a
deviation requiring a variant label.

**Source fidelity:** Strong match, confirmed on direct fetch. All bean ingredients and
quantities (pepper, onion, garlic, olive oil, oregano, 1 lb beans, vinegar, vino seco,
bay leaves, sugar, water) and the pressure-cook sequence/timings (30 min high
pressure, ~10 min build, 20 min natural release, 10 min thicken) match exactly.

**Specificity:** Good — "vino seco or sherry cooking wine" already gives a workable
substitute.

**Components:** None linked; none of my three assigned components apply. The rice
sub-recipe is a good example of transparency already met: Kitchen Notes states the
source calls rice "optional" and that the rice quantity/timing is an editorial
addition — exactly the labeled-adaptation practice the brief requires. No new
component needed; basic rice cooking doesn't warrant `{{component:}}` treatment.

**Readability:** A. Explicit quantities, ordered steps, clear endpoints, and Kitchen
Notes proactively separates editorial vs. sourced timing.

**Decision:** keep.

**Findings:** none — a model example of a transparently labeled editorial addition
(rice) on a faithfully transcribed source (beans).

**Access failures:** none (foodnetwork.com fetched directly).

---

## component:blue-cheese-dip

- Path: `components/dips/blue-cheese-dip.md` · Hash: `1793416fe9e051b75fa6426798ef5228df302c03`
- Source: https://www.thekitchn.com/recipe-creamy-blue-cheese-dressing-recipes-from-the-kitchn-191040
- Consumers to inspect: `buffalo-wings`, `chicken-finger-sub` (both reviewed above, in
  this same batch).

**Authenticity:** Pass — mash-then-thin blue-cheese dressing is a standard wing-dip
preparation; no unsupported claims.

**Source fidelity:** Uncertain — access failure. thekitchn.com returned HTTP 403 on
repeated attempts; web.archive.org unreachable at the tool level. WebSearch snippets
confirm ingredient identities and method (mash cheese with sour cream to a "chunky
paste," cottage-cheese-like texture, then stir in buttermilk/mayo/lemon juice), but did
not surface exact numeric quantities. Amounts remain unverified directly this cycle (a
prior review pass recorded "quantities match" — treated as a lead, not proof).

**Finding (moderate, needs orchestrator adjudication):** Snippets attributed to the
source quote the author's own framing: "I like using Maytag blue cheese for a classic,
not-too-pungent flavor." Our Note currently reads: "Maytag is an American option, not
necessarily mild" — which reads as a direct rebuttal of the source's own stated
preference. This wording came from a prior component-review pass
(`docs/reviews/2026-09-26-scratch-components.md`) that over-corrected against the
source's own subjective framing. Proposed correction: "Maytag is a widely available
American option often described as comparatively mild; choose a stronger option like
Roquefort for more punch" — keeps the useful point (intensity varies by brand) without
contradicting the cited source's own words. Source: thekitchn.com headnote, via
WebSearch snippet — full page not independently re-fetched this cycle. Confidence:
medium (snippet quotation, not a direct read).

**Specificity:** Good — "American blue cheese such as Maytag, or stronger Roquefort"
already gives a useful intensity range (Check 4).

**Readability:** A. Clear quantities, two-step method, explicit chill/hold guidance.

**Decision:** targeted fix (reword the Maytag-mildness note; needs orchestrator
sign-off since the source page could not be re-read directly).

**Access failures:** thekitchn.com 403 (repeated); web.archive.org unreachable at the
tool level. WebSearch snippets used as partial corroboration only — weaker than a
direct read.

---

## component:buffalo-wing-sauce

- Path: `components/sauces/buffalo-wing-sauce.md` · Hash: `7d51f367fb683b2a645d15289095abf09b9dd34b`
- Source: https://www.allrecipes.com/recipe/219109/buffalo-chicken-wing-sauce/
- Consumers to inspect: `buffalo-wings`, `chicken-finger-sub` (both reviewed above, in
  this same batch).

**Authenticity:** Pass, correctly labeled. Note already states "Chef John's variation;
not a verified Anchor Bar formula. Plain hot sauce and butter also make a classic
Buffalo sauce" — exactly the standard SKILL.md requires.

**Source fidelity:** Partial access failure, resolved via alternate route. WebFetch
cannot reach www.allrecipes.com (pre-confirmed blocked); web.archive.org unreachable at
the tool level, contrary to the brief's suggested fallback. Alternate legitimate route
used: this page is attributed to Chef John, whose original is published on his own
blog, foodwishes.blogspot.com, fetched successfully. That original lists "1/2 teaspoon
Tabasco sauce or other hot sauce," which is **missing** from our ingredient list. Flag
is hedged: the exact cited allrecipes.com page itself could not be re-confirmed
word-for-word this cycle, so it's possible the Allrecipes adaptation itself dropped
this ingredient, in which case our component would already match its cited source.
Orchestrator should attempt allrecipes.com directly (may not be blocked outside this
tool's restrictions) before treating this as confirmed.

**Finding:** Minor. Current ingredients: 2/3 cup Frank's RedHot Original, 1/2 cup cold
butter, 1 1/2 tbsp white vinegar, 1/4 tsp Worcestershire, 1/4 tsp cayenne, 1/8 tsp
garlic powder, salt to taste. Proposed addition: "1/2 teaspoon Tabasco sauce or other
hot sauce," per Chef John's original blog recipe. Source: foodwishes.blogspot.com
(Chef John's Buffalo wing sauce post, located via WebSearch, fetched directly).
Confidence: medium — the exact cited allrecipes.com page remains unverified.

**Specificity:** Good — Frank's RedHot Original named with Anchor Bar Original as a
stated `quick_buy` alternative.

**Readability:** A. Two-step method, clear heat/visual endpoint, explicit warning
against double-buttering premixed sauce.

**Decision:** targeted fix, pending orchestrator's own allrecipes.com access attempt
(add missing Tabasco/hot-sauce line if confirmed; otherwise no change).

**Access failures:** www.allrecipes.com unreachable (pre-confirmed); web.archive.org
unreachable at the tool level (not usable as fallback this session).
foodwishes.blogspot.com used as a legitimate alternate route but does not itself
substitute for confirming the exact cited page's wording.

---

## component:crisp-chicken-fingers

- Path: `components/proteins/crisp-chicken-fingers.md` · Hash: `c793dea82f7b09f043a7c60fc93fbc0fb2e97825`
- Source: https://www.foodnetwork.com/recipes/bobby-flay/buttermilk-waffles-with-buttermilk-fried-chicken-tenders-3224076
- Consumer to inspect: `chicken-finger-sub` (reviewed above, in this same batch).

**Authenticity:** Pass — buttermilk-marinated, double-dredged, deep-fried tender is
standard technique; fried method correctly retained (not baked), per SKILL.md's rule
against simplifying away defining technique.

**Source fidelity:** Confirmed on direct fetch. Matches source closely: 12 tenders,
2 cups buttermilk divided (1 cup marinade / 1 cup dredge), 2 cups flour, 1/2 tsp
garlic powder, 1/2 tsp onion powder, 1/4 tsp cayenne (source offers "chile de arbol
powder or cayenne" — our plain cayenne is one of the source's own named options, not a
deviation), 1 tsp salt, 1/4 tsp pepper, 360°F fry temp, ~5 min fry, flour→buttermilk→
flour dredge order. One unlabeled deviation found:

**Finding:** Minor. Current text: "Marinate raw tenders in 1 cup buttermilk and the
hot sauce for 1 hour **in the refrigerator**." Source instructs "at room temperature
for 1 hour." Proposed correction: keep the refrigerated time (correct per food-safety
practice for raw poultry) but label it as a deliberate adaptation, e.g., "...for 1
hour, refrigerated (the source marinates at room temperature; this book chills it for
food safety)." Rationale: per Check 3, an intentional adaptation should be
distinguished from a transcription error; currently this reads as a silent
discrepancy. Source: foodnetwork.com, recipe step 1 ("marinate...at room temperature
for 1 hour"). Confidence: high (source fetched directly, text unambiguous).

Informational, not a finding: the added 165°F doneness temperature is a reasonable
editorial safety addition beyond the source, already presented as a Note rather than
attributed to the source.

**Specificity:** Good — cayenne offered as the source's own named alternative to
chile de arbol powder; no brand overclaim.

**Readability:** A. Explicit temperatures/time, ordered dredge-then-fry sequence,
yield/usage math stated (12 tenders → six 2-tender subs).

**Decision:** targeted fix (label the room-temperature-vs-refrigerated deviation).

**Access failures:** none (foodnetwork.com fetched directly).
