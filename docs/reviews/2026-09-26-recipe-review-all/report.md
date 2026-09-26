# Recipe review: all recipes (2026-09-26)

Mode: **suggest**. Recipe content, components, sources and menus were not changed. Completed, adjudicated recipes received `last_reviewed_at`/`last_reviewed_notes`; incomplete ones kept `null`.

Inventory and hashes: [ledger.md](ledger.md). Worker evidence: `workers/<batch>.md` (linked per recipe). The worker files are raw research notes from the first passes; where they disagree with this report, the report and its follow-up sections are final (for example, FeedMi, The Chopping Block and the original photo credits were later replaced). All prior review metadata was `null`, so nothing was replaced.

## Summary

- Recipes selected: **90** (all published; no drafts or retired recipes in scope)
- Complete and adjudicated: **86** — kept: 43, findings pending: 43
- Incomplete (metadata left null): **4** (all four completed in the follow-up below)
- Decisions: keep 50, replace source 2, targeted fix 38
- Readability grades: A 57, B 29, C 3, D 1
- Components reviewed: 21 — fixes proposed: 4
- Component proposals: 5; unresolved evidence items: 4

Follow-up (same day, apply mode on branch `fix/recipe-review-fixes`): the proposed fixes were applied, and the approved source replacements and resolved evidence are recorded in [Follow-up: approved replacements](#follow-up-approved-replacements). Rows below show final decisions.

Snapshot note: the ledger hashes predate a `description:` front-matter line added in commit 7a76d71; findings were checked against current text.

Second pass (same day): sources that blocked the first pass were re-fetched with a plain `curl` using a browser User-Agent; where that still failed, the nearest Internet Archive (Wayback Machine) capture was read and its timestamp is recorded in the recipe notes and state. Washington Post recipe pages are paywalled; the paywall was not bypassed, their text was not used as evidence, and open replacement sources are proposed for approval. No headless browser or new dependency was used.

## Recipes

| Recipe | Grade | Decision | State | Summary | Worker |
| --- | --- | --- | --- | --- | --- |
| [beef-on-weck](#beef-on-weck) | B | keep | complete | Buffalo fit strong; The Kitchn source (read live) matches. | [afc-east-1](workers/afc-east-1.md) |
| [buffalo-wings](#buffalo-wings) | A | targeted fix | complete | Deep-fried Anchor Bar/James Beard method kept; name the source's own dip so the linked dip reads as a variation. | [afc-east-1](workers/afc-east-1.md) |
| [chicken-finger-sub](#chicken-finger-sub) | A | keep | complete | Buffalo fit supported; Taste source matches; reachable sauce and dip components now verified. | [afc-east-1](workers/afc-east-1.md) |
| [sponge-candy](#sponge-candy) | A | keep | complete | Buffalo confection; source matches; clear endpoints. | [afc-east-1](workers/afc-east-1.md) |
| [cuban-black-beans-and-rice](#cuban-black-beans-and-rice) | A | keep | complete | Miami Cuban staple; Instant Pot source matches. | [afc-east-1](workers/afc-east-1.md) |
| [cuban-frita-burger](#cuban-frita-burger) | B | targeted fix | complete | Miami frita fit strong (Burger Beast); paprika wording over-specifies vs source. | [afc-east-2](workers/afc-east-2.md) |
| [cuban-sandwich](#cuban-sandwich) | B | targeted fix | complete | Cook time overstates the source; photo replaced with a verified CC BY-SA 2.0 image. | [afc-east-2](workers/afc-east-2.md) |
| [new-york-bagels](#new-york-bagels) | A | targeted fix | complete | Method matches King Arthur; source never calls itself New York style. | [afc-east-2](workers/afc-east-2.md) |
| [new-york-style-cheese-pizza](#new-york-style-cheese-pizza) | A | keep | complete | King Arthur NY-style pizza; matches. | [afc-east-2](workers/afc-east-2.md) |
| [pastrami-on-rye-jets](#pastrami-on-rye-jets) | B | targeted fix | complete | Optional cheese is listed but never melted. | [afc-east-2](workers/afc-east-2.md) |
| [boston-baked-beans](#boston-baked-beans) | A | keep | complete | Smithsonian source; faithful. Cider vinegar, rinse and 10-minute rest are editorial. | [afc-east-3](workers/afc-east-3.md) |
| [boston-cream-pie](#boston-cream-pie) | B | targeted fix | complete | Milk type, heating endpoint and doneness test drift from King Arthur. | [afc-east-3](workers/afc-east-3.md) |
| [lobster-rolls](#lobster-rolls) | A | keep | complete | New England fit strong; The Kitchn source (read live) matches. | [afc-east-3](workers/afc-east-3.md) |
| [new-england-clam-chowder](#new-england-clam-chowder) | A | targeted fix | complete | Faithful to Yankee; front matter labels total time as cook time. | [afc-east-3](workers/afc-east-3.md) |
| [cheese-coneys](#cheese-coneys) | A | targeted fix | complete | Source uses sharp cheddar, Martin's potato rolls, Dutch-process cocoa; ours generalizes. | [afc-north-1](workers/afc-north-1.md) |
| [cincinnati-chili-over-spaghetti](#cincinnati-chili-over-spaghetti) | B | targeted fix | complete | Salt is correct (worker's high-severity claim overturned); beans and onion type need disclosure. | [afc-north-1](workers/afc-north-1.md) |
| [goetta](#goetta) | A | keep | complete | Cincinnati fit strong; Saveur source (Keith Pandolfi, 2013) matches in every amount and step. | [afc-north-1](workers/afc-north-1.md) |
| [polish-boy-sandwich](#polish-boy-sandwich) | A | targeted fix | complete | Cleveland fit strong; source's turkey kielbasa undisclosed; quick option names one brand. | [afc-north-1](workers/afc-north-1.md) |
| [potato-and-cheese-pierogi](#potato-and-cheese-pierogi) | A | keep | complete | Cleveland Magazine source; faithful. | [afc-north-2](workers/afc-north-2.md) |
| [baltimore-crab-cakes](#baltimore-crab-cakes) | A | keep | complete | Old Bay/McCormick Chesapeake crab cakes; faithful. | [afc-north-2](workers/afc-north-2.md) |
| [berger-cookies](#berger-cookies) | A | keep | complete | Baltimore fit strong; Sugar Spun Run copycat matches in every amount and step. | [afc-north-2](workers/afc-north-2.md) |
| [pit-beef-sandwiches](#pit-beef-sandwiches) | A | replace source | complete | Baltimore fit strong; approved follow-up switched the paywalled Washington Post source to The Meatwave. | [afc-north-2](workers/afc-north-2.md) |
| [chipped-ham-barbecue-sandwiches](#chipped-ham-barbecue-sandwiches) | A | keep | complete | Pittsburgh chipped-ham fit strong; faithful. | [afc-north-3](workers/afc-north-3.md) |
| [haluski-cabbage-and-noodles](#haluski-cabbage-and-noodles) | B | keep | complete | Pittsburgh fit; faithful with minor wording gaps. | [afc-north-3](workers/afc-north-3.md) |
| [pierogi](#pierogi) | B | keep | complete | Food Network pierogi; faithful. | [afc-north-3](workers/afc-north-3.md) |
| [primanti-style-sandwiches](#primanti-style-sandwiches) | B | keep | complete | Primanti fit strong; source read via alternate copy. | [afc-north-3](workers/afc-north-3.md) |
| [breaded-pork-tenderloin-sandwich](#breaded-pork-tenderloin-sandwich) | B | keep | complete | Visit Indiana source; faithful, minor ambiguity. | [afc-south-1](workers/afc-south-1.md) |
| [st-elmo-style-shrimp-cocktail](#st-elmo-style-shrimp-cocktail) | A | keep | complete | St. Elmo's own instructions; faithful. | [afc-south-1](workers/afc-south-1.md) |
| [sugar-cream-pie](#sugar-cream-pie) | A | keep | complete | Indiana state pie; faithful. | [afc-south-1](workers/afc-south-1.md) |
| [camel-rider-sandwich](#camel-rider-sandwich) | A | keep | complete | Jacksonville fit strong; faithful. | [afc-south-1](workers/afc-south-1.md) |
| [mayport-shrimp-and-grits](#mayport-shrimp-and-grits) | A | keep | complete | Jacksonville fit; faithful. | [afc-south-1](workers/afc-south-1.md) |
| [fajitas](#fajitas) | A | keep | complete | Houston Tex-Mex; faithful. | [afc-south-1](workers/afc-south-1.md) |
| [sausage-kolaches-or-klobasneks](#sausage-kolaches-or-klobasneks) | A | keep | complete | Texas Czech bakery tradition; King Arthur faithful. | [afc-south-2](workers/afc-south-2.md) |
| [viet-cajun-crawfish](#viet-cajun-crawfish) | A | replace source | complete | Houston fit strong; follow-ups replaced the blocked Roadfood source, now with Edible Houston's lemongrass boil. | [afc-south-2](workers/afc-south-2.md) |
| [goo-goo-clusters](#goo-goo-clusters) | B | keep | complete | Nashville confection; copycat faithful. | [afc-south-2](workers/afc-south-2.md) |
| [meat-and-three-plate-with-meatloaf](#meat-and-three-plate-with-meatloaf) | A | keep | complete | Arnold's (Nashville) meatloaf; faithful. | [afc-south-2](workers/afc-south-2.md) |
| [nashville-hot-chicken](#nashville-hot-chicken) | B | targeted fix | complete | Nashville fit strong; Bon Appétit/Hattie B's source (read live) matches, but the salt split is vague. | [afc-south-2](workers/afc-south-2.md) |
| [colorado-pork-green-chile](#colorado-pork-green-chile) | A | keep | complete | Edible Denver source; faithful. | [afc-west-1](workers/afc-west-1.md) |
| [denver-omelet](#denver-omelet) | A | keep | complete | Western/Denver omelet; faithful. | [afc-west-1](workers/afc-west-1.md) |
| [green-chile-breakfast-burritos](#green-chile-breakfast-burritos) | B | targeted fix | complete | Denver fit; Highlands Ranch Foodie source matches in all amounts; the smothering chile swap is unlabeled. | [afc-west-1](workers/afc-west-1.md) |
| [bacon-wrapped-la-street-dogs-chargers](#bacon-wrapped-la-street-dogs-chargers) | B | keep | complete | LA street dog fit strong; minor gaps. | [afc-west-1](workers/afc-west-1.md) |
| [french-dip-sandwiches-chargers](#french-dip-sandwiches-chargers) | C | targeted fix | complete | Yield inconsistent with bread count; simplified jus unlabeled; onion omitted. | [afc-west-1](workers/afc-west-1.md) |
| [barbecue-baked-beans](#barbecue-baked-beans) | A | keep | complete | KC barbecue side; Saveur source (Paul Kirk's mother) matches in every amount and step. | [afc-west-1](workers/afc-west-1.md) |
| [kansas-city-burnt-ends](#kansas-city-burnt-ends) | A | keep | complete | KC fit strong; amazingribs method matches; rub verified as an exact half batch. | [afc-west-2](workers/afc-west-2.md) |
| [kansas-city-cheesy-corn](#kansas-city-cheesy-corn) | B | keep | complete | KC fit plausible; Serious Eats (Liz Cook) source matches in every amount. | [afc-west-2](workers/afc-west-2.md) |
| [kansas-city-style-barbecue-chicken](#kansas-city-style-barbecue-chicken) | B | keep | complete | KC fit; QVC source matches in rub, sauce and method. | [afc-west-2](workers/afc-west-2.md) |
| [casino-style-prime-rib](#casino-style-prime-rib) | A | keep | complete | Vegas buffet fit; faithful. | [afc-west-2](workers/afc-west-2.md) |
| [old-vegas-shrimp-cocktail](#old-vegas-shrimp-cocktail) | A | keep | complete | Golden Gate-style Vegas cocktail; faithful. | [afc-west-2](workers/afc-west-2.md) |
| [chicken-wings-with-mumbo-sauce](#chicken-wings-with-mumbo-sauce) | A | replace source | complete | DC fit strong; approved follow-up switched the paywalled Washington Post source to Anthony Thomas's TODAY recipe. | [nfc-east-1](workers/nfc-east-1.md) |
| [half-smoke-chili-dogs](#half-smoke-chili-dogs) | A | targeted fix | complete | DC fit strong; sausage brand misnamed. | [nfc-east-1](workers/nfc-east-1.md) |
| [tex-mex-cheese-enchiladas](#tex-mex-cheese-enchiladas) | A | keep | complete | Texas Tex-Mex; faithful. | [nfc-east-1](workers/nfc-east-1.md) |
| [texas-red-chili](#texas-red-chili) | A | keep | complete | Texas red; faithful. | [nfc-east-1](workers/nfc-east-1.md) |
| [philadelphia-soft-pretzels](#philadelphia-soft-pretzels) | A | keep | complete | Philly pretzel fit; King Arthur faithful. | [nfc-east-1](workers/nfc-east-1.md) |
| [philly-cheesesteak](#philly-cheesesteak) | A | targeted fix | complete | Philly fit strong; cheese-melt method adapted without label. | [nfc-east-1](workers/nfc-east-1.md) |
| [roast-pork-sandwich](#roast-pork-sandwich) | B | targeted fix | complete | Philly fit strong; Serious Eats (Leah Colins) source matches, but its headnote calls for sharp provolone. | [nfc-east-2](workers/nfc-east-2.md) |
| [water-ice](#water-ice) | B | targeted fix | complete | Faithful; churn and extract steps can be clearer. | [nfc-east-2](workers/nfc-east-2.md) |
| [black-and-white-cookies](#black-and-white-cookies) | B | targeted fix | complete | Bake time inconsistent between front matter and steps; spacing unstated. | [nfc-east-2](workers/nfc-east-2.md) |
| [new-york-style-pizza](#new-york-style-pizza) | B | targeted fix | complete | Faithful; dough storage, knead time and border underspecified. | [nfc-east-2](workers/nfc-east-2.md) |
| [pastrami-on-rye-giants](#pastrami-on-rye-giants) | B | targeted fix | complete | Warming step is misattributed to Katz's. | [nfc-east-2](workers/nfc-east-2.md) |
| [chicago-style-hot-dogs](#chicago-style-hot-dogs) | A | targeted fix | complete | PBS source faithful; pepper count and relish amount need alignment/labeling. | [nfc-north-1](workers/nfc-north-1.md) |
| [deep-dish-pizza](#deep-dish-pizza) | A | keep | complete | King Arthur Chicago deep dish; faithful. | [nfc-north-1](workers/nfc-north-1.md) |
| [italian-beef-sandwiches](#italian-beef-sandwiches) | A | keep | complete | Chicago fit strong; amazingribs source matches; giardiniera component now follows Lou Malnati's next-day recipe. | [nfc-north-1](workers/nfc-north-1.md) |
| [tavern-style-thin-crust-pizza](#tavern-style-thin-crust-pizza) | A | keep | complete | Chicago tavern cut; King Arthur (The Book of Pizza) source matches; giardiniera component now follows Lou Malnati's next-day recipe. | [nfc-north-1](workers/nfc-north-1.md) |
| [detroit-coney-dogs](#detroit-coney-dogs) | B | targeted fix | complete | Detroit fit strong; water omitted. | [nfc-north-1](workers/nfc-north-1.md) |
| [detroit-style-pizza](#detroit-style-pizza) | A | keep | complete | King Arthur Detroit pizza; faithful. | [nfc-north-1](workers/nfc-north-1.md) |
| [beer-brats](#beer-brats) | A | targeted fix | complete | Wisconsin fit strong; Culinary Hill amounts match; method changes are unlabeled. | [nfc-north-2](workers/nfc-north-2.md) |
| [chicken-booyah](#chicken-booyah) | B | targeted fix | complete | Green Bay fit strong; source (Judy Ullmer via The Flavor of Wisconsin) confirms lemon and soy, but most onion goes unused. | [nfc-north-2](workers/nfc-north-2.md) |
| [fried-wisconsin-cheese-curds](#fried-wisconsin-cheese-curds) | A | keep | complete | Wisconsin curds; faithful. | [nfc-north-2](workers/nfc-north-2.md) |
| [jucy-lucy-cheese-stuffed-burgers](#jucy-lucy-cheese-stuffed-burgers) | A | targeted fix | complete | Minneapolis fit strong; duplicated warning; 160°F is ours. | [nfc-north-2](workers/nfc-north-2.md) |
| [tater-tot-hotdish](#tater-tot-hotdish) | A | keep | complete | Minnesota fit strong; recipe faithful; component has findings. | [nfc-north-2](workers/nfc-north-2.md) |
| [deviled-crab](#deviled-crab) | B | targeted fix | complete | Tampa fit strong; dough test step out of order, chilling total unclear. | [nfc-south-1](workers/nfc-south-1.md) |
| [spanish-bean-soup](#spanish-bean-soup) | B | keep | complete | Columbia Restaurant soup; faithful. | [nfc-south-1](workers/nfc-south-1.md) |
| [tampa-cuban-sandwich-with-salami](#tampa-cuban-sandwich-with-salami) | A | targeted fix | complete | Columbia's own recipe; mustard and salami can be more specific. | [nfc-south-1](workers/nfc-south-1.md) |
| [lemon-pepper-wet-wings](#lemon-pepper-wet-wings) | A | keep | complete | Atlanta fit strong; faithful. | [nfc-south-1](workers/nfc-south-1.md) |
| [peach-cobbler](#peach-cobbler) | B | targeted fix | complete | King Arthur faithful except the topping method in step 4. | [nfc-south-2](workers/nfc-south-2.md) |
| [livermush-sandwiches](#livermush-sandwiches) | B | keep | complete | Carolinas livermush; faithful. | [nfc-south-2](workers/nfc-south-2.md) |
| [pimento-cheese-sandwiches](#pimento-cheese-sandwiches) | A | targeted fix | complete | Faithful; photo replaced with a verified CC BY 2.0 image. | [nfc-south-2](workers/nfc-south-2.md) |
| [beignets](#beignets) | A | targeted fix | complete | New Orleans fit strong; The Kitchn source matches, but the frying step omits basting the tops. | [nfc-south-2](workers/nfc-south-2.md) |
| [jambalaya](#jambalaya) | B | targeted fix | complete | Editorial note spliced into step 4 breaks the sentence. | [nfc-south-3](workers/nfc-south-3.md) |
| [muffuletta-sandwich](#muffuletta-sandwich) | A | targeted fix | complete | Olive type contradicts the Saveur (Central Grocery-style) source. | [nfc-south-3](workers/nfc-south-3.md) |
| [red-beans-and-rice](#red-beans-and-rice) | A | targeted fix | complete | Camellia source faithful; mashing step is ours. | [nfc-south-3](workers/nfc-south-3.md) |
| [shrimp-po-boy](#shrimp-po-boy) | A | keep | complete | New Orleans fit strong; Epicurious (Bon Appétit Test Kitchen) source matches in every amount and step. | [nfc-south-3](workers/nfc-south-3.md) |
| [cioppino](#cioppino) | A | keep | complete | SF fit strong; Saveur (Tadich Grill) source matches in every amount and step. | [nfc-west-1](workers/nfc-west-1.md) |
| [mission-style-burritos](#mission-style-burritos) | B | targeted fix | complete | SF fit strong; bean salt far below source. | [nfc-west-1](workers/nfc-west-1.md) |
| [fry-bread-tacos](#fry-bread-tacos) | D | targeted fix | complete | Steps 4–5 contradict (rest after shaping); piercing and olives missing; photo replaced with a verified CC0 image. | [nfc-west-1](workers/nfc-west-1.md) |
| [sonoran-hot-dogs](#sonoran-hot-dogs) | A | keep | complete | Phoenix/Tucson fit strong; faithful. | [nfc-west-1](workers/nfc-west-1.md) |
| [bacon-wrapped-la-street-dogs-rams](#bacon-wrapped-la-street-dogs-rams) | C | targeted fix | complete | Jalapeños listed but never cooked; finishing salt missing. | [nfc-west-2](workers/nfc-west-2.md) |
| [french-dip-sandwiches-rams](#french-dip-sandwiches-rams) | C | targeted fix | complete | Byte-identical to the Chargers version apart from id and image; same fixes apply. | [nfc-west-2](workers/nfc-west-2.md) |
| [seattle-dogs-with-cream-cheese-and-onions](#seattle-dogs-with-cream-cheese-and-onions) | A | keep | complete | Seattle fit strong; faithful. NYT origin claim unverified. | [nfc-west-2](workers/nfc-west-2.md) |
| [seattle-style-chicken-teriyaki](#seattle-style-chicken-teriyaki) | A | keep | complete | Seattle fit (snippets); faithful. | [nfc-west-2](workers/nfc-west-2.md) |

## beef-on-weck

- Path: `recipes/afc/east/bills/beef-on-weck.md`
- Source: <https://www.thekitchn.com/beef-on-weck-recipe-23471886>
- Readability: B. Decision: **keep**. State: complete (second pass: live, browser UA).
- Evidence: [workers/afc-east-1.md](workers/afc-east-1.md)
- Summary: Buffalo fit strong; The Kitchn source (read live) matches.
- Notes: Via: live page with browser User-Agent. Step 2 compresses the 400°F→325°F step-down into one clause (readability B). The source uses Kaiser rolls plus a caraway-salt topping; our store-bought kummelweck option could double that topping, so topping only plain rolls is worth saying.

## buffalo-wings

- Path: `recipes/afc/east/bills/buffalo-wings.md`
- Source: <https://archive.jamesbeard.org/recipes/buffalo-wings>
- Readability: A. Decision: **targeted fix**. State: complete (second pass: components verified live).
- Evidence: [workers/afc-east-1.md](workers/afc-east-1.md)
- Summary: Deep-fried Anchor Bar/James Beard method kept; name the source's own dip so the linked dip reads as a variation.
- Notes: Both reachable components now verified live (see Component findings). Batch sizes line up: the sauce makes about 1 1/4 cups and the dip about 1 1/2 cups, as stated.

**Correction 1**

- Current: Closing note: "The linked Chef John wing sauce and creamy blue-cheese dip are homemade variations with their own sources."
- Proposed: Add one sentence naming the James Beard source's own blue-cheese dressing, so readers see the linked dip is a substitute variation, not the source's.
- Reason: Source-fidelity framing; the dip is a labeled variation, but the source's own version is not named.
- Evidence: <https://archive.jamesbeard.org/recipes/buffalo-wings>
- Confidence: medium
- Affects: `recipes/afc/east/bills/buffalo-wings.md`

## chicken-finger-sub

- Path: `recipes/afc/east/bills/chicken-finger-sub.md`
- Source: <https://tastecooking.com/recipes/chicken-finger-sub/>
- Readability: A. Decision: **keep**. State: complete (second pass: components verified live).
- Evidence: [workers/afc-east-1.md](workers/afc-east-1.md)
- Summary: Buffalo fit supported; Taste source matches; reachable sauce and dip components now verified.
- Notes: `crisp-chicken-fingers` has a component finding (see Component findings), so this recipe is findings pending.

## sponge-candy

- Path: `recipes/afc/east/bills/sponge-candy.md`
- Source: <https://www.anediblemosaic.com/chocolate-covered-sponge-candy/>
- Readability: A. Decision: **keep**. State: complete.
- Evidence: [workers/afc-east-1.md](workers/afc-east-1.md)
- Summary: Buffalo confection; source matches; clear endpoints.

## cuban-black-beans-and-rice

- Path: `recipes/afc/east/dolphins/cuban-black-beans-and-rice.md`
- Source: <https://www.foodnetwork.com/fnk/recipes/instant-pot-cuban-black-beans-9491407>
- Readability: A. Decision: **keep**. State: complete.
- Evidence: [workers/afc-east-1.md](workers/afc-east-1.md)
- Summary: Miami Cuban staple; Instant Pot source matches.

## cuban-frita-burger

- Path: `recipes/afc/east/dolphins/cuban-frita-burger.md`
- Source: <https://burgerbeast.com/frita-cubana/>
- Readability: B. Decision: **targeted fix**. State: complete.
- Evidence: [workers/afc-east-2.md](workers/afc-east-2.md)
- Summary: Miami frita fit strong (Burger Beast); paprika wording over-specifies vs source.

**Correction 1**

- Current: 3 tablespoons sweet Spanish paprika (pimentón dulce)
- Proposed: 3 tablespoons Spanish paprika
- Reason: Source says Spanish paprika without specifying sweet/dulce; the added type is unsourced.
- Evidence: <https://burgerbeast.com/frita-cubana/>
- Confidence: medium
- Affects: `recipes/afc/east/dolphins/cuban-frita-burger.md`

## cuban-sandwich

- Path: `recipes/afc/east/dolphins/cuban-sandwich.md`
- Source: <https://www.foodnetwork.com/recipes/food-network-kitchen/cubano-9343989>
- Readability: B. Decision: **targeted fix**. State: complete.
- Evidence: [workers/afc-east-2.md](workers/afc-east-2.md)
- Summary: Cook time overstates the source; photo credit names a different publisher.
- Notes: Components `cuban-mojo-pork` and `american-yellow-mustard` kept (mustard source read directly).

**Correction 1**

- Current: cook: 35 minutes total
- Proposed: cook: about 20 minutes (press/griddle), per source card
- Reason: Source card timing is about 20 minutes; 35 is unsupported.
- Evidence: <https://www.foodnetwork.com/recipes/food-network-kitchen/cubano-9343989>
- Confidence: medium
- Affects: `recipes/afc/east/dolphins/cuban-sandwich.md`

**Correction 2**

- Current: photo_credit: King Arthur Baking
- Proposed: Credit matching the actual photo's origin (verify image provenance)
- Reason: Source is Food Network; King Arthur credit appears mismatched.
- Evidence: <https://www.foodnetwork.com/recipes/food-network-kitchen/cubano-9343989>
- Confidence: low
- Affects: `recipes/afc/east/dolphins/cuban-sandwich.md`

## new-york-bagels

- Path: `recipes/afc/east/jets/new-york-bagels.md`
- Source: <https://www.kingarthurbaking.com/recipes/bagels-recipe>
- Readability: A. Decision: **targeted fix**. State: complete.
- Evidence: [workers/afc-east-2.md](workers/afc-east-2.md)
- Summary: Method matches King Arthur; source never calls itself New York style.

**Correction 1**

- Current: title: New York bagels / location: New York City metro
- Proposed: Keep title, add a timing/source note that the King Arthur recipe is a general boiled-and-baked bagel used here to represent the New York style.
- Reason: Framing: the NY identity is the book's, not the source's.
- Evidence: <https://www.kingarthurbaking.com/recipes/bagels-recipe>
- Confidence: medium
- Affects: `recipes/afc/east/jets/new-york-bagels.md`

## new-york-style-cheese-pizza

- Path: `recipes/afc/east/jets/new-york-style-cheese-pizza.md`
- Source: <https://www.kingarthurbaking.com/recipes/new-york-style-pizza-recipe>
- Readability: A. Decision: **keep**. State: complete.
- Evidence: [workers/afc-east-2.md](workers/afc-east-2.md)
- Summary: King Arthur NY-style pizza; matches.

## pastrami-on-rye-jets

- Path: `recipes/afc/east/jets/pastrami-on-rye-jets.md`
- Source: <https://www.centralmarketnewyork.com/how-to-make-a-pastrami-sandwich-a-step-by-step-guide/>
- Readability: B. Decision: **targeted fix**. State: complete.
- Evidence: [workers/afc-east-2.md](workers/afc-east-2.md)
- Summary: Optional cheese is listed but never melted.
- Notes: Optional: link `{{component:quick-creamy-coleslaw}}` on the coleslaw line.

**Correction 1**

- Current: Step 4: "…add optional cheese, sauerkraut or coleslaw, and close sandwiches."
- Proposed: Add: broil about 60 seconds to melt the optional cheese before closing.
- Reason: Source melts the cheese; ours supplies cheese without the melting step.
- Evidence: <https://www.centralmarketnewyork.com/how-to-make-a-pastrami-sandwich-a-step-by-step-guide/>
- Confidence: medium
- Affects: `recipes/afc/east/jets/pastrami-on-rye-jets.md`

## boston-baked-beans

- Path: `recipes/afc/east/patriots/boston-baked-beans.md`
- Source: <https://americanhistory.si.edu/sites/default/files/file-uploader/CUH%20July%2013%202018%20Boston%20Baked%20Beans.pdf>
- Readability: A. Decision: **keep**. State: complete.
- Evidence: [workers/afc-east-3.md](workers/afc-east-3.md)
- Summary: Smithsonian source; faithful. Cider vinegar, rinse and 10-minute rest are editorial.
- Notes: Transparency polish: label cider vinegar, the rinse and the 10-minute rest as editorial additions.

## boston-cream-pie

- Path: `recipes/afc/east/patriots/boston-cream-pie.md`
- Source: <https://www.kingarthurbaking.com/recipes/boston-cream-pie-recipe>
- Readability: B. Decision: **targeted fix**. State: complete.
- Evidence: [workers/afc-east-3.md](workers/afc-east-3.md)
- Summary: Milk type, heating endpoint and doneness test drift from King Arthur.

**Correction 1**

- Current: Step 2: "Heat the 1 cup cake milk with 4 tablespoons butter until steaming"
- Proposed: "…just to a boil"
- Reason: Source heats milk and butter to a boil.
- Evidence: <https://www.kingarthurbaking.com/recipes/boston-cream-pie-recipe>
- Confidence: medium
- Affects: `recipes/afc/east/patriots/boston-cream-pie.md`

**Correction 2**

- Current: Step 3: "bake 30 to 35 minutes"
- Proposed: Add the source's toothpick test as the doneness endpoint.
- Reason: Endpoint missing.
- Evidence: <https://www.kingarthurbaking.com/recipes/boston-cream-pie-recipe>
- Confidence: high
- Affects: `recipes/afc/east/patriots/boston-cream-pie.md`

**Correction 3**

- Current: "1 cup milk" / "2 1/2 cups milk"
- Proposed: "1 cup whole milk" / "2 1/2 cups whole milk"
- Reason: Source specifies whole milk in cake and filling.
- Evidence: <https://www.kingarthurbaking.com/recipes/boston-cream-pie-recipe>
- Confidence: medium
- Affects: `recipes/afc/east/patriots/boston-cream-pie.md`

**Correction 4**

- Current: "1/3 cup chopped dark or semisweet chocolate"
- Proposed: Note the chocolate forms the source allows (chips or chopped).
- Reason: Specificity polish.
- Evidence: <https://www.kingarthurbaking.com/recipes/boston-cream-pie-recipe>
- Confidence: low
- Affects: `recipes/afc/east/patriots/boston-cream-pie.md`

## lobster-rolls

- Path: `recipes/afc/east/patriots/lobster-rolls.md`
- Source: <https://www.thekitchn.com/lobster-roll-recipe-23733104>
- Readability: A. Decision: **keep**. State: complete (second pass: live, browser UA).
- Evidence: [workers/afc-east-3.md](workers/afc-east-3.md)
- Summary: New England fit strong; The Kitchn source (read live) matches.
- Notes: Via: live page with browser User-Agent. Only difference: the source's black pepper to taste is omitted.

## new-england-clam-chowder

- Path: `recipes/afc/east/patriots/new-england-clam-chowder.md`
- Source: <https://newengland.com/food/fish-seafood/massachusetts-new-england-clam-chowder/>
- Readability: A. Decision: **targeted fix**. State: complete.
- Evidence: [workers/afc-east-3.md](workers/afc-east-3.md)
- Summary: Faithful to Yankee; front matter labels total time as cook time.

**Correction 1**

- Current: cook: 1 hour 15 minutes total
- Proposed: cook: time excluding prep (source's 1 hr 15 min is total time)
- Reason: Source's 1 hr 15 min is Total Time; with 45 minutes prep listed separately it double-counts.
- Evidence: <https://newengland.com/food/fish-seafood/massachusetts-new-england-clam-chowder/>
- Confidence: medium
- Affects: `recipes/afc/east/patriots/new-england-clam-chowder.md`

## cheese-coneys

- Path: `recipes/afc/north/bengals/cheese-coneys.md`
- Source: <https://oryana.coop/recipe/the-best-cincinnati-cheese-coney-recipe/>
- Readability: A. Decision: **targeted fix**. State: complete.
- Evidence: [workers/afc-north-1.md](workers/afc-north-1.md)
- Summary: Source uses sharp cheddar, Martin's potato rolls, Dutch-process cocoa; ours generalizes.
- Notes: Worker's proposal to reverse the grill/boil framing is downgraded: the source allows either. Optional: note the source toasts the buns.

**Correction 1**

- Current: "4 ounces finely shredded mild yellow cheddar (sharp is a stronger alternative), about 2 cups"
- Proposed: "4 ounces finely shredded sharp cheddar (about 2 cups)"
- Reason: Oryana source specifies sharp cheddar (orchestrator read; worker's 'mild' claim overturned).
- Evidence: <https://oryana.coop/recipe/the-best-cincinnati-cheese-coney-recipe/>
- Confidence: high
- Affects: `recipes/afc/north/bengals/cheese-coneys.md`

**Correction 2**

- Current: "6 soft hot dog buns (steam for a parlor-style coney)"
- Proposed: "6 long potato rolls, such as Martin's" (steaming remains an option)
- Reason: Source names potato rolls.
- Evidence: <https://oryana.coop/recipe/the-best-cincinnati-cheese-coney-recipe/>
- Confidence: high
- Affects: `recipes/afc/north/bengals/cheese-coneys.md`

**Correction 3**

- Current: "1 tablespoon unsweetened cocoa powder"
- Proposed: "1 tablespoon unsweetened Dutch-process cocoa powder"
- Reason: Source specifies Dutch-process.
- Evidence: <https://oryana.coop/recipe/the-best-cincinnati-cheese-coney-recipe/>
- Confidence: high
- Affects: `recipes/afc/north/bengals/cheese-coneys.md`

## cincinnati-chili-over-spaghetti

- Path: `recipes/afc/north/bengals/cincinnati-chili-over-spaghetti.md`
- Source: <https://www.foodnetwork.com/recipes/food-network-kitchen/cincinnati-chili-recipe-2043706>
- Readability: B. Decision: **targeted fix**. State: complete.
- Evidence: [workers/afc-north-1.md](workers/afc-north-1.md)
- Summary: Salt is correct (worker's high-severity claim overturned); beans and onion type need disclosure.
- Notes: Orchestrator verified the source says to sprinkle the beef with 1/2 teaspoon each salt and pepper; the current text is correct.

**Correction 1**

- Current: "about 2 cups warm red kidney beans (optional four-way style)"
- Proposed: Keep, but note the source uses pinto beans.
- Reason: Undisclosed substitution.
- Evidence: <https://www.foodnetwork.com/recipes/food-network-kitchen/cincinnati-chili-recipe-2043706>
- Confidence: medium
- Affects: `recipes/afc/north/bengals/cincinnati-chili-over-spaghetti.md`

**Correction 2**

- Current: "2 sweet onions, finely chopped"
- Proposed: "2 sweet onions (such as Vidalia), finely chopped"
- Reason: Restores the source's example.
- Evidence: <https://www.foodnetwork.com/recipes/food-network-kitchen/cincinnati-chili-recipe-2043706>
- Confidence: low
- Affects: `recipes/afc/north/bengals/cincinnati-chili-over-spaghetti.md`

## goetta

- Path: `recipes/afc/north/bengals/goetta.md`
- Source: <https://www.saveur.com/article/Recipes/Goetta/>
- Readability: A. Decision: **keep**. State: complete (second pass: live).
- Evidence: [workers/afc-north-1.md](workers/afc-north-1.md)
- Summary: Cincinnati fit strong; Saveur source (Keith Pandolfi, 2013) matches in every amount and step.
- Notes: Via: live page text. Checked 1 1/2 lb chuck, 3/4 lb pork, stock and water, 1 1/2–2 hr simmer, 3 1/3 cups water to 1 cup steel-cut oats, onion flakes, white pepper, 1/2-inch slices fried in canola.

## polish-boy-sandwich

- Path: `recipes/afc/north/browns/polish-boy-sandwich.md`
- Source: <https://www.reneeskitchenadventures.com/2016/04/polish-boy-sandwich.html>
- Readability: A. Decision: **targeted fix**. State: complete.
- Evidence: [workers/afc-north-1.md](workers/afc-north-1.md)
- Summary: Cleveland fit strong; source's turkey kielbasa undisclosed; quick option names one brand.
- Notes: Components `kansas-city-barbecue-sauce`, `oven-fries`, `quick-creamy-coleslaw` kept.

**Correction 1**

- Current: "2 links fully cooked smoked pork kielbasa"
- Proposed: Keep pork, add note: the source uses turkey kielbasa.
- Reason: Undisclosed substitution.
- Evidence: <https://www.reneeskitchenadventures.com/2016/04/polish-boy-sandwich.html>
- Confidence: medium
- Affects: `recipes/afc/north/browns/polish-boy-sandwich.md`

**Correction 2**

- Current: quick_options: "Use KC Masterpiece Sweet Honey & Molasses or another Kansas City-style…"
- Proposed: "Use a Kansas City-style tomato-and-molasses sauce, such as KC Masterpiece."
- Reason: Brand should be an example, not the lead instruction.
- Evidence: <https://www.reneeskitchenadventures.com/2016/04/polish-boy-sandwich.html>
- Confidence: low
- Affects: `recipes/afc/north/browns/polish-boy-sandwich.md`

## potato-and-cheese-pierogi

- Path: `recipes/afc/north/browns/potato-and-cheese-pierogi.md`
- Source: <https://clevelandmagazine.com/articles/pierogi/>
- Readability: A. Decision: **keep**. State: complete.
- Evidence: [workers/afc-north-2.md](workers/afc-north-2.md)
- Summary: Cleveland Magazine source; faithful.
- Notes: Minor polish: name the flour type; add 'starting at the center and working outward' when sealing.

## baltimore-crab-cakes

- Path: `recipes/afc/north/ravens/baltimore-crab-cakes.md`
- Source: <https://www.mccormick.com/blogs/old-bay-recipes/chesapeake-old-bay-crab-cakes>
- Readability: A. Decision: **keep**. State: complete.
- Evidence: [workers/afc-north-2.md](workers/afc-north-2.md)
- Summary: Old Bay/McCormick Chesapeake crab cakes; faithful.

## berger-cookies

- Path: `recipes/afc/north/ravens/berger-cookies.md`
- Source: <https://sugarspunrun.com/copycat-berger-cookies-recipe/>
- Readability: A. Decision: **keep**. State: complete (second pass: Wayback 20260519010950).
- Evidence: [workers/afc-north-2.md](workers/afc-north-2.md)
- Summary: Baltimore fit strong; Sugar Spun Run copycat matches in every amount and step.
- Notes: Via: Wayback snapshot 20260519010950 (live page blocked). Yield 30 cookies matches.

## pit-beef-sandwiches

- Path: `recipes/afc/north/ravens/pit-beef-sandwiches.md`
- Source: <https://www.washingtonpost.com/recipes/baltimore-pit-beef/>
- Readability: A. Decision: **replace source**. State: complete (second pass: paywalled, not bypassed; replacement proposed).
- Evidence: [workers/afc-north-2.md](workers/afc-north-2.md)
- Summary: Baltimore fit strong; Washington Post source is paywalled for readers, so propose an open source.
- Notes: Awaiting the user's approval before any change. Component `baltimore-horseradish-sauce` kept (optionally drop 'full-fat'). The WaPo text was not read and is not used as evidence.

**Correction 1**

- Current: source.url: https://www.washingtonpost.com/recipes/baltimore-pit-beef/
- Proposed: https://carnediem.blog/2023/baltimore-pit-beef-maryland-style-roast-beef/ (alternate: https://meatwave.com/recipes/baltimore-pit-beef-recipe)
- Reason: The paywalled source cannot be checked by readers or by this review (not bypassed). Carne Diem is open and complete. Adopting it changes the recipe: a heavier rub (paprika, oregano, rosemary, cayenne instead of chili powder), no 4-hour chill, 400°F instead of 450°F, pull at 120°F for rare instead of 130°F, a 10-minute rest instead of 5 minutes or less, tiger sauce at 1/4 cup mayo to 1 tbsp horseradish, and white onion instead of Vidalia. Neither candidate is Baltimore-local; ATK (paywalled), amazingribs, Chef Bolek and Pasatiempo were considered and rejected.
- Evidence: <https://carnediem.blog/2023/baltimore-pit-beef-maryland-style-roast-beef/>
- Confidence: medium
- Affects: `recipes/afc/north/ravens/pit-beef-sandwiches.md`

## chipped-ham-barbecue-sandwiches

- Path: `recipes/afc/north/steelers/chipped-ham-barbecue-sandwiches.md`
- Source: <https://hearthandvine.com/ham-barbecue-sandwiches/>
- Readability: A. Decision: **keep**. State: complete.
- Evidence: [workers/afc-north-3.md](workers/afc-north-3.md)
- Summary: Pittsburgh chipped-ham fit strong; faithful.
- Notes: Optional: name Heinz ketchup as the source does; offer Virginia ham as the substitute.

## haluski-cabbage-and-noodles

- Path: `recipes/afc/north/steelers/haluski-cabbage-and-noodles.md`
- Source: <https://www.thekitchenwhisperer.net/2024/02/09/the-best-pittsburgh-haluski-fried-cabbage-and-noodles-in-butter/>
- Readability: B. Decision: **keep**. State: complete.
- Evidence: [workers/afc-north-3.md](workers/afc-north-3.md)
- Summary: Pittsburgh fit; faithful with minor wording gaps.
- Notes: Clarify the cabbage-thirds wording; 'wide' noodles is ours.

## pierogi

- Path: `recipes/afc/north/steelers/pierogi.md`
- Source: <https://www.foodnetwork.com/recipes/food-network-kitchen/the-best-potato-and-cheese-pierogi-19951953>
- Readability: B. Decision: **keep**. State: complete.
- Evidence: [workers/afc-north-3.md](workers/afc-north-3.md)
- Summary: Food Network pierogi; faithful.
- Notes: Add 'Roll half the dough into a thin 15-inch square' for a clearer rolling endpoint.

## primanti-style-sandwiches

- Path: `recipes/afc/north/steelers/primanti-style-sandwiches.md`
- Source: <https://www.epicurious.com/recipes/food/views/primantis-sandwich-369031>
- Readability: B. Decision: **keep**. State: complete (source via alternate copy).
- Evidence: [workers/afc-north-3.md](workers/afc-north-3.md)
- Summary: Primanti fit strong; source read via alternate copy.
- Notes: Polish: cut fries 1/4–1/2 inch; 'turning occasionally'.

## breaded-pork-tenderloin-sandwich

- Path: `recipes/afc/south/colts/breaded-pork-tenderloin-sandwich.md`
- Source: <https://visitindiana.in.gov/blog/post/pork-tenderloin-recipe/>
- Readability: B. Decision: **keep**. State: complete.
- Evidence: [workers/afc-south-1.md](workers/afc-south-1.md)
- Summary: Visit Indiana source; faithful, minor ambiguity.

## st-elmo-style-shrimp-cocktail

- Path: `recipes/afc/south/colts/st-elmo-style-shrimp-cocktail.md`
- Source: <https://store.stelmos.com/blogs/recipes/cooking-instructions-for-st-elmo-shrimp>
- Readability: A. Decision: **keep**. State: complete.
- Evidence: [workers/afc-south-1.md](workers/afc-south-1.md)
- Summary: St. Elmo's own instructions; faithful.
- Notes: Component `horseradish-cocktail-sauce` kept.

## sugar-cream-pie

- Path: `recipes/afc/south/colts/sugar-cream-pie.md`
- Source: <https://www.foodnetwork.com/recipes/food-network-kitchen/sugar-cream-recipe-2043494>
- Readability: A. Decision: **keep**. State: complete.
- Evidence: [workers/afc-south-1.md](workers/afc-south-1.md)
- Summary: Indiana state pie; faithful.

## camel-rider-sandwich

- Path: `recipes/afc/south/jaguars/camel-rider-sandwich.md`
- Source: <https://fwtmagazine.com/the-ultimate-guide-to-jacksonvilles-iconic-camel-rider-sandwich/>
- Readability: A. Decision: **keep**. State: complete.
- Evidence: [workers/afc-south-1.md](workers/afc-south-1.md)
- Summary: Jacksonville fit strong; faithful.

## mayport-shrimp-and-grits

- Path: `recipes/afc/south/jaguars/mayport-shrimp-and-grits.md`
- Source: <https://www.jacksonvillemag.com/2022/03/24/billys-shrimp-grits/>
- Readability: A. Decision: **keep**. State: complete.
- Evidence: [workers/afc-south-1.md](workers/afc-south-1.md)
- Summary: Jacksonville fit; faithful.
- Notes: Component `creamy-stone-ground-grits` kept.

## fajitas

- Path: `recipes/afc/south/texans/fajitas.md`
- Source: <https://www.foodnetwork.com/recipes/food-network-kitchen/tex-mex-steak-fajitas-with-peppers-and-onions-5172083>
- Readability: A. Decision: **keep**. State: complete.
- Evidence: [workers/afc-south-1.md](workers/afc-south-1.md)
- Summary: Houston Tex-Mex; faithful.
- Notes: Components: `fresh-pico-de-gallo` yield already labeled estimated on re-check; `quick-guacamole` yield should be labeled estimated (see Component findings).

## sausage-kolaches-or-klobasneks

- Path: `recipes/afc/south/texans/sausage-kolaches-or-klobasneks.md`
- Source: <https://www.kingarthurbaking.com/recipes/kolaches-sweet-savory-recipe>
- Readability: A. Decision: **keep**. State: complete.
- Evidence: [workers/afc-south-2.md](workers/afc-south-2.md)
- Summary: Texas Czech bakery tradition; King Arthur faithful.

## viet-cajun-crawfish

- Path: `recipes/afc/south/texans/viet-cajun-crawfish.md`
- Source: <https://roadfood.com/recipes/viet-cajun-crawfish-recipe-houston-tx/>
- Readability: A. Decision: **replace source**. State: complete (Roadfood still blocked; replaced in the follow-up, see below).
- Evidence: [workers/afc-south-2.md](workers/afc-south-2.md)
- Summary: Houston fit strong; seasoning line ranks one option over the other.
- Notes: Incomplete: source not read in full directly.

**Correction 1**

- Current: "1 cup Zatarain's Crawfish, Shrimp & Crab Boil seasoning (or Old Bay for a milder, celery-salt-forward profile)"
- Proposed: Present Zatarain's and Old Bay as equal either/or options.
- Reason: Source offers both without preference.
- Evidence: <https://roadfood.com/recipes/viet-cajun-crawfish-recipe-houston-tx/>
- Confidence: medium
- Affects: `recipes/afc/south/texans/viet-cajun-crawfish.md`

## goo-goo-clusters

- Path: `recipes/afc/south/titans/goo-goo-clusters.md`
- Source: <https://globalbakes.com/goo-goo-clusters/>
- Readability: B. Decision: **keep**. State: complete.
- Evidence: [workers/afc-south-2.md](workers/afc-south-2.md)
- Summary: Nashville confection; copycat faithful.
- Notes: Add the source's kneading step.

## meat-and-three-plate-with-meatloaf

- Path: `recipes/afc/south/titans/meat-and-three-plate-with-meatloaf.md`
- Source: <https://thelocalpalate.com/recipes/arnolds-meatloaf-with-tomato-creole-sauce/>
- Readability: A. Decision: **keep**. State: complete.
- Evidence: [workers/afc-south-2.md](workers/afc-south-2.md)
- Summary: Arnold's (Nashville) meatloaf; faithful.
- Notes: Heinz brand dropped from ketchup; acceptable generic.

## nashville-hot-chicken

- Path: `recipes/afc/south/titans/nashville-hot-chicken.md`
- Source: <https://www.bonappetit.com/recipe/nashville-style-hot-chicken>
- Readability: B. Decision: **targeted fix**. State: complete (second pass: live, browser UA).
- Evidence: [workers/afc-south-2.md](workers/afc-south-2.md)
- Summary: Nashville fit strong; Bon Appétit/Hattie B's source (read live) matches, but the salt split is vague.
- Notes: Via: live page with browser User-Agent. Accepted editorial differences: 165°F for all pieces (source: 160°F white, 165°F dark; ours is safe); Crystal or Frank's where the source names Tabasco or Texas Pete; the source fries in 4 batches and lets the oil cool slightly before making the paste.

**Correction 1**

- Current: Step 1: "Season chicken all over with black pepper and the larger portion of salt."
- Proposed: "Season chicken all over with black pepper and 2 tablespoons Diamond Crystal (1 tablespoon Morton) kosher salt."
- Reason: The source gives the exact amount; 'the larger portion' makes the reader work out the divided salt.
- Evidence: <https://www.bonappetit.com/recipe/nashville-style-hot-chicken>
- Confidence: high
- Affects: `recipes/afc/south/titans/nashville-hot-chicken.md`

## colorado-pork-green-chile

- Path: `recipes/afc/west/broncos/colorado-pork-green-chile.md`
- Source: <https://edibledenver.com/ed-recipe/colorado-style-pork-green-chile/>
- Readability: A. Decision: **keep**. State: complete.
- Evidence: [workers/afc-west-1.md](workers/afc-west-1.md)
- Summary: Edible Denver source; faithful.

## denver-omelet

- Path: `recipes/afc/west/broncos/denver-omelet.md`
- Source: <https://www.foodnetwork.com/recipes/food-network-kitchen/western-omelette-recipe-2011477>
- Readability: A. Decision: **keep**. State: complete.
- Evidence: [workers/afc-west-1.md](workers/afc-west-1.md)
- Summary: Western/Denver omelet; faithful.

## green-chile-breakfast-burritos

- Path: `recipes/afc/west/broncos/green-chile-breakfast-burritos.md`
- Source: <https://highlandsranchfoodie.com/breakfast-burrito-with-green-chile-sauce/>
- Readability: B. Decision: **targeted fix**. State: complete (second pass: Wayback 20260412125705).
- Evidence: [workers/afc-west-1.md](workers/afc-west-1.md)
- Summary: Denver fit; Highlands Ranch Foodie source matches in all amounts; the smothering chile swap is unlabeled.
- Notes: Via: Wayback snapshot 20260412125705. The first-pass note to drop the 'Southwest spice blend' was wrong: the blend is in the source.

**Correction 1**

- Current: Ingredient: "3–4 cups prepared Colorado-style pork green chile, warmed (use the booklet’s Colorado pork green chile recipe)"
- Proposed: Add: "(The source smothers with its own Hatch pork green chili; ours is a Denver-style swap.)"
- Reason: Label the regional adaptation so it is not read as the source's.
- Evidence: <https://highlandsranchfoodie.com/breakfast-burrito-with-green-chile-sauce/>
- Confidence: medium
- Affects: `recipes/afc/west/broncos/green-chile-breakfast-burritos.md`

## bacon-wrapped-la-street-dogs-chargers

- Path: `recipes/afc/west/chargers/bacon-wrapped-la-street-dogs-chargers.md`
- Source: <https://www.latinasquecomen.com/mexican-hot-dogs/>
- Readability: B. Decision: **keep**. State: complete.
- Evidence: [workers/afc-west-1.md](workers/afc-west-1.md)
- Summary: LA street dog fit strong; minor gaps.
- Notes: Label olive oil as ours; step 3 already includes jalapeños. Shared item: source finishes with a sprinkle of sea salt or seasoning salt; ours omits it.

## french-dip-sandwiches-chargers

- Path: `recipes/afc/west/chargers/french-dip-sandwiches-chargers.md`
- Source: <https://discovercaliforniawines.com/recipes/french-dip-sandwich-an-l-a-classic/>
- Readability: C. Decision: **targeted fix**. State: complete.
- Evidence: [workers/afc-west-1.md](workers/afc-west-1.md)
- Summary: Yield inconsistent with bread count; simplified jus unlabeled; onion omitted.
- Notes: Optional: name a wine style (Zinfandel or Syrah). A `french-dip-au-jus` component is proposed.

**Correction 1**

- Current: yield: 6 sandwiches with "4 French rolls, split (or 2 baguettes cut into six 6-inch lengths)"
- Proposed: yield: 4 sandwiches (source serves 4), or 6 rolls with the scaling labeled editorial
- Reason: Source serves 4 from 4 rolls / 2 baguettes and a 2½ lb tri-tip.
- Evidence: <https://discovercaliforniawines.com/recipes/french-dip-sandwich-an-l-a-classic/>
- Confidence: high
- Affects: `recipes/afc/west/chargers/french-dip-sandwiches-chargers.md; recipes/nfc/west/rams/french-dip-sandwiches-rams.md`

**Correction 2**

- Current: Step 3 jus (wine reduction + stock)
- Proposed: Label as simplified from the source's jus.
- Reason: Unlabeled simplification.
- Evidence: <https://discovercaliforniawines.com/recipes/french-dip-sandwich-an-l-a-classic/>
- Confidence: medium
- Affects: `same two paths`

**Correction 3**

- Current: Rub: salt, garlic, pepper, oil
- Proposed: Restore 1 teaspoon granulated onion.
- Reason: Source ingredient omitted.
- Evidence: <https://discovercaliforniawines.com/recipes/french-dip-sandwich-an-l-a-classic/>
- Confidence: high
- Affects: `same two paths`

## barbecue-baked-beans

- Path: `recipes/afc/west/chiefs/barbecue-baked-beans.md`
- Source: <https://www.saveur.com/article/Recipes/Baked-Beans/>
- Readability: A. Decision: **keep**. State: complete (second pass: live).
- Evidence: [workers/afc-west-1.md](workers/afc-west-1.md)
- Summary: KC barbecue side; Saveur source (Paul Kirk's mother) matches in every amount and step.
- Notes: Via: live page. 275°F for 5–6 hours; serves 8.

## kansas-city-burnt-ends

- Path: `recipes/afc/west/chiefs/kansas-city-burnt-ends.md`
- Source: <https://amazingribs.com/brisket-burnt-ends/>
- Readability: A. Decision: **keep**. State: complete (method via Wayback 20260310130835; rub verified in the follow-up, see below).
- Evidence: [workers/afc-west-2.md](workers/afc-west-2.md)
- Summary: KC fit strong; amazingribs method matches; rub verified as an exact half batch in the follow-up.
- Notes: Via: Wayback snapshot 20260310130835. Matches the 6-lb point, 3 tsp Morton, 235°F then 225°F, wrap at 155°F, 195°F finish, 4 + 4 oz wood, 1/4 cup broth, 1/4 cup sauce + 1/4 cup drippings, 1/4 tbsp brown sugar. Still incomplete: the Big Bad Beef Rub sub-recipe page returned 403 live, 404 on Wayback and has no CDX captures, so our rub amounts are unverified.

## kansas-city-cheesy-corn

- Path: `recipes/afc/west/chiefs/kansas-city-cheesy-corn.md`
- Source: <https://www.seriouseats.com/kansas-style-cheesy-corn-recipe-8682405>
- Readability: B. Decision: **keep**. State: complete (second pass: live).
- Evidence: [workers/afc-west-2.md](workers/afc-west-2.md)
- Summary: KC fit plausible; Serious Eats (Liz Cook) source matches in every amount.
- Notes: Via: live page. Minor readability: we omit the source's cook-time cues (ham about 4 min, cream cheese about 10 min, cheese about 1 min, 'as thick as nacho cheese').

## kansas-city-style-barbecue-chicken

- Path: `recipes/afc/west/chiefs/kansas-city-style-barbecue-chicken.md`
- Source: <https://www.qvc.com/recipes/kansas-city-style-smoked-chicken.html>
- Readability: B. Decision: **keep**. State: complete (second pass: live).
- Evidence: [workers/afc-west-2.md](workers/afc-west-2.md)
- Summary: KC fit; QVC source matches in rub, sauce and method.
- Notes: Via: live page. Additions (fruitwood or hickory, rubbing the cavity, checking every 10–15 min) are minor editorial. Source quality is weak: a retailer page with no named author. A stronger KC source would help a future review.

## casino-style-prime-rib

- Path: `recipes/afc/west/raiders/casino-style-prime-rib.md`
- Source: <https://www.foodnetwork.com/recipes/food-network-kitchen/the-best-prime-rib-7422442>
- Readability: A. Decision: **keep**. State: complete.
- Evidence: [workers/afc-west-2.md](workers/afc-west-2.md)
- Summary: Vegas buffet fit; faithful.
- Notes: Components: `prime-rib-horseradish-cream` kept; `prime-rib-pan-jus` has a fix (see Component findings).

## old-vegas-shrimp-cocktail

- Path: `recipes/afc/west/raiders/old-vegas-shrimp-cocktail.md`
- Source: <https://www.lasdiscounts.com/post/bring-las-vegas-to-your-table-the-iconic-vegas-shrimp-cocktail-recipe>
- Readability: A. Decision: **keep**. State: complete.
- Evidence: [workers/afc-west-2.md](workers/afc-west-2.md)
- Summary: Golden Gate-style Vegas cocktail; faithful.

## chicken-wings-with-mumbo-sauce

- Path: `recipes/nfc/east/commanders/chicken-wings-with-mumbo-sauce.md`
- Source: <https://www.washingtonpost.com/recipes/mumbo-sauce-chicken-wings/>
- Readability: A. Decision: **replace source**. State: complete (second pass: paywalled, not bypassed; replacement proposed).
- Evidence: [workers/nfc-east-1.md](workers/nfc-east-1.md)
- Summary: DC fit strong; Washington Post source is paywalled, so propose an open, attributed DC source.
- Notes: Awaiting the user's approval. The first-pass Tabasco correction is withdrawn: it rested on unread WaPo text. `mumbo-sauce` component still proposed.

**Correction 1**

- Current: source.url: https://www.washingtonpost.com/recipes/mumbo-sauce-chicken-wings/
- Proposed: https://www.today.com/recipes/mambo-chicken-wings-t300767 (Chef Anthony Thomas); corroboration: https://www.blackfoodie.co/recipe/dc-mumbo-sauce/ and https://boundarystones.weta.org/2023/07/07/mumbo-sauce-it-really-quintessential-dc
- Reason: The paywalled source cannot be checked (not bypassed). Adopting the Today recipe changes the dish: buttermilk marinade and flour dredge, fry at 350°F for 8–10 min, a sauce of pineapple juice, two vinegars, sugar, honey, Worcestershire, soy, mustard and tomato paste (ours uses cane syrup, water and whiskey), drizzled rather than tossed.
- Evidence: <https://www.today.com/recipes/mambo-chicken-wings-t300767>
- Confidence: medium
- Affects: `recipes/nfc/east/commanders/chicken-wings-with-mumbo-sauce.md`

**Correction 2**

- Current: photo_credit: The Washington Post
- Proposed: New photo and credit to match the new source.
- Reason: The photo is tied to the replaced source.
- Evidence: <https://www.today.com/recipes/mambo-chicken-wings-t300767>
- Confidence: medium
- Affects: `recipes/nfc/east/commanders/chicken-wings-with-mumbo-sauce.md`

## half-smoke-chili-dogs

- Path: `recipes/nfc/east/commanders/half-smoke-chili-dogs.md`
- Source: <https://www.recipetineats.com/chili-dogs/>
- Readability: A. Decision: **targeted fix**. State: complete.
- Evidence: [workers/nfc-east-1.md](workers/nfc-east-1.md)
- Summary: DC fit strong; sausage brand misnamed.

**Correction 1**

- Current: "6 smoked beef-and-pork half-smoke sausages (Ben's Original if available)"
- Proposed: "…(such as the half-smokes sold by Ben's Chili Bowl, if available)"
- Reason: 'Ben's Original' is an unrelated rice brand.
- Evidence: <https://www.recipetineats.com/chili-dogs/>
- Confidence: high
- Affects: `recipes/nfc/east/commanders/half-smoke-chili-dogs.md`

**Correction 2**

- Current: "- Yellow mustard"
- Proposed: "- Yellow mustard {{component:american-yellow-mustard}}"
- Reason: Existing component covers it.
- Evidence: <https://www.recipetineats.com/chili-dogs/>
- Confidence: medium
- Affects: `recipes/nfc/east/commanders/half-smoke-chili-dogs.md`

## tex-mex-cheese-enchiladas

- Path: `recipes/nfc/east/cowboys/tex-mex-cheese-enchiladas.md`
- Source: <https://texascooking.com/recipes/cheeseenchiladas.htm>
- Readability: A. Decision: **keep**. State: complete.
- Evidence: [workers/nfc-east-1.md](workers/nfc-east-1.md)
- Summary: Texas Tex-Mex; faithful.

## texas-red-chili

- Path: `recipes/nfc/east/cowboys/texas-red-chili.md`
- Source: <https://www.inspiredtaste.net/52080/texas-red-chili/>
- Readability: A. Decision: **keep**. State: complete.
- Evidence: [workers/nfc-east-1.md](workers/nfc-east-1.md)
- Summary: Texas red; faithful.

## philadelphia-soft-pretzels

- Path: `recipes/nfc/east/eagles/philadelphia-soft-pretzels.md`
- Source: <https://www.kingarthurbaking.com/recipes/classic-pretzels-recipe>
- Readability: A. Decision: **keep**. State: complete.
- Evidence: [workers/nfc-east-1.md](workers/nfc-east-1.md)
- Summary: Philly pretzel fit; King Arthur faithful.

## philly-cheesesteak

- Path: `recipes/nfc/east/eagles/philly-cheesesteak.md`
- Source: <https://www.foodnetwork.com/recipes/food-network-kitchen/philly-cheesesteak-9343357>
- Readability: A. Decision: **targeted fix**. State: complete.
- Evidence: [workers/nfc-east-1.md](workers/nfc-east-1.md)
- Summary: Philly fit strong; cheese-melt method adapted without label.
- Notes: Optional: name Amoroso's as an example roll.

**Correction 1**

- Current: Step 3: "Cover each portion of beef with American cheese and let it melt directly over the meat."
- Proposed: Label the skillet melt as an adaptation; the source melts under the broiler.
- Reason: Unlabeled method change.
- Evidence: <https://www.foodnetwork.com/recipes/food-network-kitchen/philly-cheesesteak-9343357>
- Confidence: medium
- Affects: `recipes/nfc/east/eagles/philly-cheesesteak.md`

## roast-pork-sandwich

- Path: `recipes/nfc/east/eagles/roast-pork-sandwich.md`
- Source: <https://www.seriouseats.com/philly-roast-pork-sandwich-recipe-8605326>
- Readability: B. Decision: **targeted fix**. State: complete (second pass: live).
- Evidence: [workers/nfc-east-2.md](workers/nfc-east-2.md)
- Summary: Philly fit strong; Serious Eats (Leah Colins) source matches, but its headnote calls for sharp provolone.
- Notes: Via: live page. Every other amount and step matches.

**Correction 1**

- Current: "12 to 18 thin slices provolone cheese"
- Proposed: "12 to 18 thin slices sharp provolone (provolone piccante)"
- Reason: The ingredient list says provolone, but the source headnote says sharp provolone is the only cheese allowed.
- Evidence: <https://www.seriouseats.com/philly-roast-pork-sandwich-recipe-8605326>
- Confidence: high
- Affects: `recipes/nfc/east/eagles/roast-pork-sandwich.md`

**Correction 2**

- Current: photo_credit: www.bonappetit.com
- Proposed: Verify; source is Serious Eats.
- Reason: Possible mismatch.
- Evidence: <https://www.seriouseats.com/philly-roast-pork-sandwich-recipe-8605326>
- Confidence: low
- Affects: `recipes/nfc/east/eagles/roast-pork-sandwich.md`

## water-ice

- Path: `recipes/nfc/east/eagles/water-ice.md`
- Source: <https://soufflebombay.com/diy-philadelphia-style-lime-water-ice/>
- Readability: B. Decision: **targeted fix**. State: complete.
- Evidence: [workers/nfc-east-2.md](workers/nfc-east-2.md)
- Summary: Faithful; churn and extract steps can be clearer.

**Correction 1**

- Current: Step 3 combines churning and storage
- Proposed: Split churning (20–25 minutes) into its own step.
- Reason: Readability.
- Evidence: <https://soufflebombay.com/diy-philadelphia-style-lime-water-ice/>
- Confidence: medium
- Affects: `recipes/nfc/east/eagles/water-ice.md`

**Correction 2**

- Current: "1–2 teaspoons concentrated lime extract"
- Proposed: Specify the lime extract as the source does.
- Reason: Specificity.
- Evidence: <https://soufflebombay.com/diy-philadelphia-style-lime-water-ice/>
- Confidence: low
- Affects: `recipes/nfc/east/eagles/water-ice.md`

## black-and-white-cookies

- Path: `recipes/nfc/east/giants/black-and-white-cookies.md`
- Source: <https://www.kingarthurbaking.com/recipes/black-and-white-cookies-recipe>
- Readability: B. Decision: **targeted fix**. State: complete.
- Evidence: [workers/nfc-east-2.md](workers/nfc-east-2.md)
- Summary: Bake time inconsistent between front matter and steps; spacing unstated.

**Correction 1**

- Current: cook: "11 to 12 minutes bake" vs step 3 "Bake 10 to 12 minutes"
- Proposed: Make both match the source.
- Reason: Internal contradiction.
- Evidence: <https://www.kingarthurbaking.com/recipes/black-and-white-cookies-recipe>
- Confidence: high
- Affects: `recipes/nfc/east/giants/black-and-white-cookies.md`

**Correction 2**

- Current: Step 2: "leaving space between"
- Proposed: State the source's spacing.
- Reason: Missing measure.
- Evidence: <https://www.kingarthurbaking.com/recipes/black-and-white-cookies-recipe>
- Confidence: medium
- Affects: `recipes/nfc/east/giants/black-and-white-cookies.md`

## new-york-style-pizza

- Path: `recipes/nfc/east/giants/new-york-style-pizza.md`
- Source: <https://www.foodnetwork.com/recipes/food-network-kitchen/new-yorkstyle-cheese-pizza-10066512>
- Readability: B. Decision: **targeted fix**. State: complete.
- Evidence: [workers/nfc-east-2.md](workers/nfc-east-2.md)
- Summary: Faithful; dough storage, knead time and border underspecified.
- Notes: Worker declined a shared NY pizza-sauce component.

**Correction 1**

- Current: Step 6: "Refrigerate or freeze the unused dough ball."
- Proposed: Give the source's storage method/duration.
- Reason: Missing detail.
- Evidence: <https://www.foodnetwork.com/recipes/food-network-kitchen/new-yorkstyle-cheese-pizza-10066512>
- Confidence: medium
- Affects: `recipes/nfc/east/giants/new-york-style-pizza.md`

**Correction 2**

- Current: Step 1: "Knead 3 to 5 minutes"
- Proposed: Match the source's knead time.
- Reason: Fidelity.
- Evidence: <https://www.foodnetwork.com/recipes/food-network-kitchen/new-yorkstyle-cheese-pizza-10066512>
- Confidence: medium
- Affects: `recipes/nfc/east/giants/new-york-style-pizza.md`

**Correction 3**

- Current: Step 5: "leaving a border"
- Proposed: "leaving a 3/4-inch border"
- Reason: Missing measure.
- Evidence: <https://www.foodnetwork.com/recipes/food-network-kitchen/new-yorkstyle-cheese-pizza-10066512>
- Confidence: medium
- Affects: `recipes/nfc/east/giants/new-york-style-pizza.md`

## pastrami-on-rye-giants

- Path: `recipes/nfc/east/giants/pastrami-on-rye-giants.md`
- Source: <https://www.labreabakery.com/recipes/ny-deli-pastrami-rye>
- Readability: B. Decision: **targeted fix**. State: complete.
- Evidence: [workers/nfc-east-2.md](workers/nfc-east-2.md)
- Summary: Warming step is misattributed to Katz's.
- Notes: Supersedes the worker's claim that Katz's method is industrial-only.

**Correction 1**

- Current: Step 1: "…place portions in a covered skillet with 1–2 tablespoons water over medium-low heat for about 5 minutes… This warming step follows Katz's deli guidance…"
- Proposed: Either cite Katz's actual method (sealed package in boiling water, covered on low about 5 minutes, or microwave under a damp paper towel) or remove the attribution and label the skillet method editorial.
- Reason: La Brea source has no warming step; Katz's page describes a different method (orchestrator verified).
- Evidence: <https://katzsdelicatessen.com/cooking-instructions>
- Confidence: high
- Affects: `recipes/nfc/east/giants/pastrami-on-rye-giants.md`

## chicago-style-hot-dogs

- Path: `recipes/nfc/north/bears/chicago-style-hot-dogs.md`
- Source: <https://www.pbs.org/food/recipes/chicago-style-hot-dog>
- Readability: A. Decision: **targeted fix**. State: complete (relish source read by orchestrator).
- Evidence: [workers/nfc-north-1.md](workers/nfc-north-1.md)
- Summary: PBS source faithful; pepper count and relish amount need alignment/labeling.
- Notes: Below-a-boil note is defensible. Component `chicago-sweet-green-relish` verified by orchestrator (adamwitt.co) and kept.

**Correction 1**

- Current: "4–8 pickled sport peppers (1–2 per dog)"
- Proposed: "8 pickled sport peppers (2 per dog)"
- Reason: Source uses two per dog.
- Evidence: <https://www.pbs.org/food/recipes/chicago-style-hot-dog>
- Confidence: high
- Affects: `recipes/nfc/north/bears/chicago-style-hot-dogs.md`

**Correction 2**

- Current: "about 1 tablespoon per dog"
- Proposed: "about 1 tablespoon per dog (estimated; source does not specify)"
- Reason: Editorial quantity unlabeled.
- Evidence: <https://www.pbs.org/food/recipes/chicago-style-hot-dog>
- Confidence: high
- Affects: `recipes/nfc/north/bears/chicago-style-hot-dogs.md`

## deep-dish-pizza

- Path: `recipes/nfc/north/bears/deep-dish-pizza.md`
- Source: <https://www.kingarthurbaking.com/recipes/chicago-style-deep-dish-pizza-recipe>
- Readability: A. Decision: **keep**. State: complete.
- Evidence: [workers/nfc-north-1.md](workers/nfc-north-1.md)
- Summary: King Arthur Chicago deep dish; faithful.

## italian-beef-sandwiches

- Path: `recipes/nfc/north/bears/italian-beef-sandwiches.md`
- Source: <https://amazingribs.com/tested-recipes/beef-and-bison-recipes/chicago-italian-beef-sandwich-recipe/>
- Readability: A. Decision: **keep**. State: complete (source via Wayback 20260508110538; giardiniera component rebuilt in the follow-up; was: component source blocked).
- Evidence: [workers/nfc-north-1.md](workers/nfc-north-1.md)
- Summary: Chicago fit strong; amazingribs source matches; giardiniera component source still blocked.
- Notes: Via: Wayback snapshot 20260508110538. The source names Gonnella, Turano and D'Amato rolls and makes giardiniera optional ('if you wish'). Still incomplete by reach: `chicago-oil-packed-giardiniera` source returned 403 live, archive.ph 429, and has no Wayback captures.

## tavern-style-thin-crust-pizza

- Path: `recipes/nfc/north/bears/tavern-style-thin-crust-pizza.md`
- Source: <https://www.kingarthurbaking.com/videos/tavern-style-pizza>
- Readability: A. Decision: **keep**. State: complete (source live; giardiniera component rebuilt in the follow-up).
- Evidence: [workers/nfc-north-1.md](workers/nfc-north-1.md)
- Summary: Chicago tavern cut; King Arthur (The Book of Pizza) source matches.
- Notes: Via: live page text. Dough, sauce, toppings, 475°F for 7–10 min, oregano after baking and square cut match; source yields two 12-inch pizzas. Still incomplete by reach: giardiniera component source blocked.

## detroit-coney-dogs

- Path: `recipes/nfc/north/lions/detroit-coney-dogs.md`
- Source: <https://www.simplyscratch.com/detroit-style-coney-dogs/>
- Readability: B. Decision: **targeted fix**. State: complete.
- Evidence: [workers/nfc-north-1.md](workers/nfc-north-1.md)
- Summary: Detroit fit strong; water omitted.

**Correction 1**

- Current: Step 2: "…stir in the spices, sugar, tomato puree, and mustard. Cover and simmer…"
- Proposed: Add "1/4 cup water" to Ingredients and to step 2.
- Reason: Source ingredient omitted.
- Evidence: <https://www.simplyscratch.com/detroit-style-coney-dogs/>
- Confidence: high
- Affects: `recipes/nfc/north/lions/detroit-coney-dogs.md`

## detroit-style-pizza

- Path: `recipes/nfc/north/lions/detroit-style-pizza.md`
- Source: <https://www.kingarthurbaking.com/recipes/weeknight-detroit-pizza-recipe>
- Readability: A. Decision: **keep**. State: complete.
- Evidence: [workers/nfc-north-1.md](workers/nfc-north-1.md)
- Summary: King Arthur Detroit pizza; faithful.

## beer-brats

- Path: `recipes/nfc/north/packers/beer-brats.md`
- Source: <https://www.culinaryhill.com/wisconsin-beer-brats/>
- Readability: A. Decision: **targeted fix**. State: complete (second pass: live).
- Evidence: [workers/nfc-north-2.md](workers/nfc-north-2.md)
- Summary: Wisconsin fit strong; Culinary Hill amounts match; method changes are unlabeled.
- Notes: Via: live page. Also editorial: beer brand suggestions (the source says pilsners and lagers are traditional, but IPAs, porters and stouts work) and de-emphasized ketchup.

**Correction 1**

- Current: Step 1: "Bring the beer just to a simmer, then lower heat and gently poach raw brats about 10–12 minutes, until the centers reach 160°F."
- Proposed: Keep, but label the gentle simmer and 160°F endpoint as this book's method (the source brings the beer to a boil and cooks through).
- Reason: Unlabeled deviation from the source method.
- Evidence: <https://www.culinaryhill.com/wisconsin-beer-brats/>
- Confidence: medium
- Affects: `recipes/nfc/north/packers/beer-brats.md`

## chicken-booyah

- Path: `recipes/nfc/north/packers/chicken-booyah.md`
- Source: <https://archive.jsonline.com/features/recipes/115053789.html>
- Readability: B. Decision: **targeted fix**. State: complete (second pass: live).
- Evidence: [workers/nfc-north-2.md](workers/nfc-north-2.md)
- Summary: Green Bay fit strong; source (Judy Ullmer via The Flavor of Wisconsin) confirms lemon and soy, but most onion goes unused.
- Notes: Via: live page. Lemon juice and soy sauce are in the source (first-pass doubt resolved). Salt and bay starting amounts are already labeled estimates. Serves 10–12.

**Correction 1**

- Current: Step 3: "Add cabbage, celery, carrots, tomatoes, and potatoes first..."
- Proposed: Add the remaining onion with the vegetables.
- Reason: Step 1 uses only 'some of the onion'; nothing uses the rest of the 2 pounds. The source adds the remaining onion with the vegetables.
- Evidence: <https://archive.jsonline.com/features/recipes/115053789.html>
- Confidence: high
- Affects: `recipes/nfc/north/packers/chicken-booyah.md`

**Correction 2**

- Current: Step 3: "reserve quick-cooking corn and peas for roughly the final 20–30 minutes"
- Proposed: Label as this book's adjustment (the source adds all vegetables before the 2+ hour simmer).
- Reason: Unlabeled deviation.
- Evidence: <https://archive.jsonline.com/features/recipes/115053789.html>
- Confidence: medium
- Affects: `recipes/nfc/north/packers/chicken-booyah.md`

## fried-wisconsin-cheese-curds

- Path: `recipes/nfc/north/packers/fried-wisconsin-cheese-curds.md`
- Source: <https://www.foodnetwork.com/recipes/amanda-freitag/fried-cheese-curds-3168939>
- Readability: A. Decision: **keep**. State: complete.
- Evidence: [workers/nfc-north-2.md](workers/nfc-north-2.md)
- Summary: Wisconsin curds; faithful.

## jucy-lucy-cheese-stuffed-burgers

- Path: `recipes/nfc/north/vikings/jucy-lucy-cheese-stuffed-burgers.md`
- Source: <https://www.foodnetwork.com/recipes/food-network-kitchen/jucy-lucy-recipe-1973693>
- Readability: A. Decision: **targeted fix**. State: complete.
- Evidence: [workers/nfc-north-2.md](workers/nfc-north-2.md)
- Summary: Minneapolis fit strong; duplicated warning; 160°F is ours.

**Correction 1**

- Current: Steps 4 and 5 both warn about the hot cheese
- Proposed: Keep one warning.
- Reason: Duplication.
- Evidence: <https://www.foodnetwork.com/recipes/food-network-kitchen/jucy-lucy-recipe-1973693>
- Confidence: high
- Affects: `recipes/nfc/north/vikings/jucy-lucy-cheese-stuffed-burgers.md`

**Correction 2**

- Current: "ground beef should reach 160°F"
- Proposed: Label as food-safety guidance added by this book.
- Reason: Not in source.
- Evidence: <https://www.foodnetwork.com/recipes/food-network-kitchen/jucy-lucy-recipe-1973693>
- Confidence: medium
- Affects: `recipes/nfc/north/vikings/jucy-lucy-cheese-stuffed-burgers.md`

## tater-tot-hotdish

- Path: `recipes/nfc/north/vikings/tater-tot-hotdish.md`
- Source: <https://www.billstjohn.com/recipes/minnesota-tater-tot-hotdish>
- Readability: A. Decision: **keep**. State: complete.
- Evidence: [workers/nfc-north-2.md](workers/nfc-north-2.md)
- Summary: Minnesota fit strong; recipe faithful; component has findings.
- Notes: Findings pending on `hotdish-cream-sauce` (see Component findings).

## deviled-crab

- Path: `recipes/nfc/south/buccaneers/deviled-crab.md`
- Source: <https://recipesfoodandcooking.com/2018/12/12/deviled-crab-croquettes/>
- Readability: B. Decision: **targeted fix**. State: complete.
- Evidence: [workers/nfc-south-1.md](workers/nfc-south-1.md)
- Summary: Tampa fit strong; dough test step out of order, chilling total unclear.

**Correction 1**

- Current: Step 6 (dough test) after shaping steps 4–5
- Proposed: Move the dough test before step 4.
- Reason: Sequence error.
- Evidence: <https://recipesfoodandcooking.com/2018/12/12/deviled-crab-croquettes/>
- Confidence: high
- Affects: `recipes/nfc/south/buccaneers/deviled-crab.md`

**Correction 2**

- Current: prep: "about 4 hours chilling" with three 2-hour chills
- Proposed: "about 4–6 hours chilling (dough and filling chill in parallel)"
- Reason: Timing clarity.
- Evidence: <https://recipesfoodandcooking.com/2018/12/12/deviled-crab-croquettes/>
- Confidence: medium
- Affects: `recipes/nfc/south/buccaneers/deviled-crab.md`

## spanish-bean-soup

- Path: `recipes/nfc/south/buccaneers/spanish-bean-soup.md`
- Source: <https://www.cltampa.com/food-drink/cls-yborhood-guide-the-columbia-restaurants-spanish-bean-soup-recipe-12306207/>
- Readability: B. Decision: **keep**. State: complete.
- Evidence: [workers/nfc-south-1.md](workers/nfc-south-1.md)
- Summary: Columbia Restaurant soup; faithful.
- Notes: Label steps 2 and 5 as editorial.

## tampa-cuban-sandwich-with-salami

- Path: `recipes/nfc/south/buccaneers/tampa-cuban-sandwich-with-salami.md`
- Source: <https://www.columbiarestaurant.com/the-original-cuban-sandwich>
- Readability: A. Decision: **targeted fix**. State: complete.
- Evidence: [workers/nfc-south-1.md](workers/nfc-south-1.md)
- Summary: Columbia's own recipe; mustard and salami can be more specific.
- Notes: Pork component question unresolved (`tampa-roast-pork` proposed vs reuse `cuban-mojo-pork` vs keep purchased).

**Correction 1**

- Current: "1 tablespoon yellow mustard"
- Proposed: "1 tablespoon yellow mustard {{component:american-yellow-mustard}}"
- Reason: Existing component.
- Evidence: <https://www.columbiarestaurant.com/the-original-cuban-sandwich>
- Confidence: medium
- Affects: `recipes/nfc/south/buccaneers/tampa-cuban-sandwich-with-salami.md`

**Correction 2**

- Current: "1 ounce thinly sliced salami"
- Proposed: "1 ounce thinly sliced Genoa salami"
- Reason: Tampa standard per CBS-reported Columbia version.
- Evidence: <https://www.columbiarestaurant.com/the-original-cuban-sandwich>
- Confidence: medium
- Affects: `recipes/nfc/south/buccaneers/tampa-cuban-sandwich-with-salami.md`

## lemon-pepper-wet-wings

- Path: `recipes/nfc/south/falcons/lemon-pepper-wet-wings.md`
- Source: <https://www.sweetteaandthyme.com/lemon-pepper-wings-with-wing-sauce/>
- Readability: A. Decision: **keep**. State: complete.
- Evidence: [workers/nfc-south-1.md](workers/nfc-south-1.md)
- Summary: Atlanta fit strong; faithful.

## peach-cobbler

- Path: `recipes/nfc/south/falcons/peach-cobbler.md`
- Source: <https://www.kingarthurbaking.com/recipes/classic-peach-cobbler-recipe>
- Readability: B. Decision: **targeted fix**. State: complete.
- Evidence: [workers/nfc-south-2.md](workers/nfc-south-2.md)
- Summary: King Arthur faithful except the topping method in step 4.
- Notes: Sugar and cornstarch lines are correct; optionally combine them into one labeled line.

**Correction 1**

- Current: Step 4: "Pat dough about 3/4 inch thick and cut small biscuit rounds, or divide into evenly spaced rustic mounds over peaches so steam can escape."
- Proposed: Follow the source: pat the dough into a second greased 9-inch pan, cut 2-inch biscuits, invert and arrange over the peaches.
- Reason: 3/4-inch thickness and mound option are unsourced.
- Evidence: <https://www.kingarthurbaking.com/recipes/classic-peach-cobbler-recipe>
- Confidence: high
- Affects: `recipes/nfc/south/falcons/peach-cobbler.md`

## livermush-sandwiches

- Path: `recipes/nfc/south/panthers/livermush-sandwiches.md`
- Source: <https://www.ajc.com/food-and-dining/the-livermush-legacy-lives-on-at-this-north-carolina-restaurant/F7JRB6QXGBB4ZEKQ76COG6NFEM/>
- Readability: B. Decision: **keep**. State: complete.
- Evidence: [workers/nfc-south-2.md](workers/nfc-south-2.md)
- Summary: Carolinas livermush; faithful.
- Notes: Clarify the sourdough bread line.

## pimento-cheese-sandwiches

- Path: `recipes/nfc/south/panthers/pimento-cheese-sandwiches.md`
- Source: <https://www.foodnetwork.com/recipes/food-network-kitchen/pimiento-cheese-sandwich-9343947>
- Readability: A. Decision: **targeted fix**. State: complete.
- Evidence: [workers/nfc-south-2.md](workers/nfc-south-2.md)
- Summary: Faithful; photo credit mismatched.

**Correction 1**

- Current: photo_credit: Food.com
- Proposed: Credit matching the actual image; source is Food Network.
- Reason: Metadata mismatch.
- Evidence: <https://www.foodnetwork.com/recipes/food-network-kitchen/pimiento-cheese-sandwich-9343947>
- Confidence: medium
- Affects: `recipes/nfc/south/panthers/pimento-cheese-sandwiches.md`

## beignets

- Path: `recipes/nfc/south/saints/beignets.md`
- Source: <https://www.thekitchn.com/beignets-268400>
- Readability: A. Decision: **targeted fix**. State: complete (second pass: live, browser UA).
- Evidence: [workers/nfc-south-2.md](workers/nfc-south-2.md)
- Summary: New Orleans fit strong; The Kitchn source matches, but the frying step omits basting the tops.
- Notes: Via: live page with browser User-Agent. All amounts match (yield about 22). Our step 5 yeast and oil-temperature cautions are editorial additions. The source also lets refrigerated dough sit 20–25 min before rolling; ours omits it.

**Correction 1**

- Current: Step 6: "Fry 3 to 4 pieces at a time until golden, 1 to 2 minutes per side."
- Proposed: Add: "Immediately spoon hot oil over the tops so they puff."
- Reason: The source ladles hot oil over each batch as soon as it goes in.
- Evidence: <https://www.thekitchn.com/beignets-268400>
- Confidence: high
- Affects: `recipes/nfc/south/saints/beignets.md`

## jambalaya

- Path: `recipes/nfc/south/saints/jambalaya.md`
- Source: <https://www.neworleans.com/restaurants/traditional-new-orleans-foods/jambalaya/>
- Readability: B. Decision: **targeted fix**. State: complete.
- Evidence: [workers/nfc-south-3.md](workers/nfc-south-3.md)
- Summary: Editorial note spliced into step 4 breaks the sentence.
- Notes: Andouille-browning step uncertain.

**Correction 1**

- Current: Step 4: "Stir in 1 cup amber lager or amber ale (for example Abita Amber); this beer-roux version is a New Orleans tourism recipe, not universal jambalaya technique for 30 seconds, then…"
- Proposed: "Stir in 1 cup amber lager or amber ale for 30 seconds, then slowly add 6 cups low-sodium chicken stock while stirring." (keep the note on the ingredient line only)
- Reason: Transcription splice.
- Evidence: <https://www.neworleans.com/restaurants/traditional-new-orleans-foods/jambalaya/>
- Confidence: high
- Affects: `recipes/nfc/south/saints/jambalaya.md`

## muffuletta-sandwich

- Path: `recipes/nfc/south/saints/muffuletta-sandwich.md`
- Source: <https://www.saveur.com/article/Recipes/Muffuletta-Sandwich/>
- Readability: A. Decision: **targeted fix**. State: complete (second pass: live).
- Evidence: [workers/nfc-south-3.md](workers/nfc-south-3.md)
- Summary: Olive type contradicts the Saveur (Central Grocery-style) source.
- Notes: Via: live page text. Every other amount and step matches (serves 4). The source hollows out the loaf where ours pulls 'a little' bread (minor). `new-orleans-olive-salad` component proposed.

**Correction 1**

- Current: "3/4 cup chopped pitted briny green olives (such as Spanish or Calabrese; not specifically Niçoise)"
- Proposed: "3/4 cup chopped pitted green niçoise olives (or another briny green olive)"
- Reason: Saveur's ingredient list specifies green niçoise olives; our note says the opposite.
- Evidence: <https://www.saveur.com/article/Recipes/Muffuletta-Sandwich/>
- Confidence: high
- Affects: `recipes/nfc/south/saints/muffuletta-sandwich.md`

## red-beans-and-rice

- Path: `recipes/nfc/south/saints/red-beans-and-rice.md`
- Source: <https://www.camelliabrand.com/recipes/camellias-famous-new-orleans-style-red-beans/>
- Readability: A. Decision: **targeted fix**. State: complete.
- Evidence: [workers/nfc-south-3.md](workers/nfc-south-3.md)
- Summary: Camellia source faithful; mashing step is ours.
- Notes: Component `cajun-seasoning` kept.

**Correction 1**

- Current: Step 4: "Mash a spoonful of beans against the pot wall to make the liquid creamy."
- Proposed: Label as an editorial tip.
- Reason: Not in source.
- Evidence: <https://www.camelliabrand.com/recipes/camellias-famous-new-orleans-style-red-beans/>
- Confidence: medium
- Affects: `recipes/nfc/south/saints/red-beans-and-rice.md`

## shrimp-po-boy

- Path: `recipes/nfc/south/saints/shrimp-po-boy.md`
- Source: <https://www.epicurious.com/recipes/food/views/shrimp-poboy-365820>
- Readability: A. Decision: **keep**. State: complete (second pass: live).
- Evidence: [workers/nfc-south-3.md](workers/nfc-south-3.md)
- Summary: New Orleans fit strong; Epicurious (Bon Appétit Test Kitchen) source matches in every amount and step.
- Notes: Via: live page. New Orleans-style rolls, the rémoulade component and the timing estimate are labeled additions. Component `louisiana-remoulade` kept; Zatarain's/Crystal brands are our suggestions.

## cioppino

- Path: `recipes/nfc/west/49ers/cioppino.md`
- Source: <https://www.saveur.com/article/recipes/cioppino/>
- Readability: A. Decision: **keep**. State: complete (second pass: live).
- Evidence: [workers/nfc-west-1.md](workers/nfc-west-1.md)
- Summary: SF fit strong; Saveur (Tadich Grill) source matches in every amount and step.
- Notes: Via: live page text. First-pass concern withdrawn: the source uses all the garlic in the skillet and all the wine to steam the clams, exactly as ours does.

## mission-style-burritos

- Path: `recipes/nfc/west/49ers/mission-style-burritos.md`
- Source: <https://www.pantsinthekitchen.com/recipes/mission-burrito>
- Readability: B. Decision: **targeted fix**. State: complete.
- Evidence: [workers/nfc-west-1.md](workers/nfc-west-1.md)
- Summary: SF fit strong; bean salt far below source.
- Notes: Optional: reorder the salsa verde; mention the pan-sear. Component `roasted-salsa-verde` kept.

**Correction 1**

- Current: "start with 1/2 teaspoon kosher salt, then adjust after simmering"
- Proposed: Raise to the source's 2 teaspoons, or label the reduction.
- Reason: Undisclosed change.
- Evidence: <https://www.pantsinthekitchen.com/recipes/mission-burrito>
- Confidence: medium
- Affects: `recipes/nfc/west/49ers/mission-style-burritos.md`

## fry-bread-tacos

- Path: `recipes/nfc/west/cardinals/fry-bread-tacos.md`
- Source: <https://www.foodnetwork.com/recipes/indian-taco-recipe-1939718>
- Readability: D. Decision: **targeted fix**. State: complete.
- Evidence: [workers/nfc-west-1.md](workers/nfc-west-1.md)
- Summary: Steps 4–5 contradict (rest after shaping); piercing and olives missing; photo credit mismatched.

**Correction 1**

- Current: Step 5: "Let mixed fry-bread dough rest covered at least 15 minutes…" (after frying in step 4)
- Proposed: Move the rest before shaping.
- Reason: Contradictory order.
- Evidence: <https://www.foodnetwork.com/recipes/indian-taco-recipe-1939718>
- Confidence: high
- Affects: `recipes/nfc/west/cardinals/fry-bread-tacos.md`

**Correction 2**

- Current: Step 4 shaping
- Proposed: Add the source's piercing step before frying.
- Reason: Omitted technique.
- Evidence: <https://www.foodnetwork.com/recipes/indian-taco-recipe-1939718>
- Confidence: high
- Affects: `recipes/nfc/west/cardinals/fry-bread-tacos.md`

**Correction 3**

- Current: Toppings
- Proposed: Add olives.
- Reason: Source topping omitted.
- Evidence: <https://www.foodnetwork.com/recipes/indian-taco-recipe-1939718>
- Confidence: medium
- Affects: `recipes/nfc/west/cardinals/fry-bread-tacos.md`

**Correction 4**

- Current: photo_credit: Instant Pot
- Proposed: Credit matching the actual image.
- Reason: Metadata mismatch.
- Evidence: <https://www.foodnetwork.com/recipes/indian-taco-recipe-1939718>
- Confidence: medium
- Affects: `recipes/nfc/west/cardinals/fry-bread-tacos.md`

## sonoran-hot-dogs

- Path: `recipes/nfc/west/cardinals/sonoran-hot-dogs.md`
- Source: <https://www.saveur.com/recipes/sonoran-dogs/>
- Readability: A. Decision: **keep**. State: complete.
- Evidence: [workers/nfc-west-1.md](workers/nfc-west-1.md)
- Summary: Phoenix/Tucson fit strong; faithful.

## bacon-wrapped-la-street-dogs-rams

- Path: `recipes/nfc/west/rams/bacon-wrapped-la-street-dogs-rams.md`
- Source: <https://www.latinasquecomen.com/mexican-hot-dogs/>
- Readability: C. Decision: **targeted fix**. State: complete.
- Evidence: [workers/nfc-west-2.md](workers/nfc-west-2.md)
- Summary: Jalapeños listed but never cooked; finishing salt missing.
- Notes: Shared with Chargers: add the source's finishing sprinkle of sea salt or seasoning salt.

**Correction 1**

- Current: Step 3: "Cook the sliced pepper and onion over medium heat with about 2 teaspoons olive oil or rendered bacon fat…"
- Proposed: "Cook the sliced pepper, onion and halved jalapeños…"
- Reason: Ingredient unused.
- Evidence: <https://www.latinasquecomen.com/mexican-hot-dogs/>
- Confidence: high
- Affects: `recipes/nfc/west/rams/bacon-wrapped-la-street-dogs-rams.md`

## french-dip-sandwiches-rams

- Path: `recipes/nfc/west/rams/french-dip-sandwiches-rams.md`
- Source: <https://discovercaliforniawines.com/recipes/french-dip-sandwich-an-l-a-classic/>
- Readability: C. Decision: **targeted fix**. State: complete.
- Evidence: [workers/nfc-west-2.md](workers/nfc-west-2.md)
- Summary: Byte-identical to the Chargers version apart from id and image; same fixes apply.
- Notes: See [french-dip-sandwiches-chargers](#french-dip-sandwiches-chargers) for yield, jus label and granulated onion.

## seattle-dogs-with-cream-cheese-and-onions

- Path: `recipes/nfc/west/seahawks/seattle-dogs-with-cream-cheese-and-onions.md`
- Source: <https://www.applegate.com/recipes/seattle-dog>
- Readability: A. Decision: **keep**. State: complete.
- Evidence: [workers/nfc-west-2.md](workers/nfc-west-2.md)
- Summary: Seattle fit strong; faithful. NYT origin claim unverified.

## seattle-style-chicken-teriyaki

- Path: `recipes/nfc/west/seahawks/seattle-style-chicken-teriyaki.md`
- Source: <https://feedthepudge.com/seattle-chicken-teriyaki/>
- Readability: A. Decision: **keep**. State: complete.
- Evidence: [workers/nfc-west-2.md](workers/nfc-west-2.md)
- Summary: Seattle fit (snippets); faithful.
- Notes: Minor: skin-side-down note.

## Component findings

Component findings are recorded here only; components carry no review metadata.

| Component | Decision | Finding | Used by |
| --- | --- | --- | --- |
| `blue-cheese-dip` | keep | The Kitchn source read live (browser User-Agent): amounts and method match; the 1-tablespoon lemon option follows the source's own note for a thicker dip. Maytag wording already fine. | buffalo-wings, chicken-finger-sub |
| `buffalo-wing-sauce` | keep | Allrecipes 219109 (Chef John) read live: all amounts and the method match; the recipe card has no Tabasco, so the first-pass doubt is resolved. | buffalo-wings, chicken-finger-sub |
| `crisp-chicken-fingers` | targeted fix | Step 1 marinates in the refrigerator; source marinates at room temperature. Label the deviation as a food-safety adaptation. Confidence high. Path: components/proteins/crisp-chicken-fingers.md. | chicken-finger-sub |
| `cuban-mojo-pork` | keep | Food Network source matches. | cuban-sandwich |
| `american-yellow-mustard` | keep | adamwitt.co source read directly. | cuban-sandwich, philadelphia-soft-pretzels, chicago-style-hot-dogs, beer-brats |
| `kansas-city-barbecue-sauce` | keep | KSHB source matches. | polish-boy-sandwich, kansas-city-burnt-ends, kansas-city-style-barbecue-chicken |
| `oven-fries` | keep | Tyler Florence source matches. | polish-boy-sandwich |
| `quick-creamy-coleslaw` | keep | Food Network source matches. | polish-boy-sandwich |
| `baltimore-horseradish-sauce` | keep | Optional: drop 'full-fat'. | pit-beef-sandwiches |
| `horseradish-cocktail-sauce` | keep | Matches. | st-elmo-style-shrimp-cocktail |
| `creamy-stone-ground-grits` | keep | Paula Deen source matches. | mayport-shrimp-and-grits |
| `fresh-pico-de-gallo` | keep (already satisfied) | Yield fix already present: 'about 2 cups (estimated…)'. | fajitas |
| `quick-guacamole` | targeted fix | `yield: About 1½ cups` → label as estimated (the Rick Bayless source gives no volume). Confidence medium. Path: components/dips/quick-guacamole.md. | fajitas |
| `prime-rib-horseradish-cream` | keep | Alton Brown source matches. | casino-style-prime-rib |
| `prime-rib-pan-jus` | targeted fix | Step 3 'reduced by about one-third to one-half' → 'reduced by about half' per the Bobby Flay source. Readability B. Confidence medium. Path: components/sauces/prime-rib-pan-jus.md. | casino-style-prime-rib |
| `chicago-sweet-green-relish` | keep | Orchestrator read adamwitt.co directly: ingredients match; 1 tsp salt already labeled as this book's starting point (source unspecified). Minor: source minces in a food processor and boils 10 minutes where ours says simmer. | chicago-style-hot-dogs |
| `chicago-oil-packed-giardiniera` | replace source (follow-up) | Timing fix already present (refrigerate 12 hours; at least 2 days). Source still unverified: chilipeppermadness returned 403 to curl and a browser User-Agent, archive.ph returned 429, and Wayback has no captures. | italian-beef-sandwiches, tavern-style-thin-crust-pizza |
| `hotdish-cream-sauce` | targeted fix (major) | The cremini-mushroom variation is ours: label or remove. `yield: About 3 1/2 cups` → label estimated. 'low-sodium' broth is unlabeled. Source: modernfarmhouseeats. Confidence high. Path: components/sauces/hotdish-cream-sauce.md. | tater-tot-hotdish |
| `cajun-seasoning` | keep | Louisiana Cookin' source matches. | red-beans-and-rice, shrimp-po-boy |
| `louisiana-remoulade` | keep | Orchestrator verified; Zatarain's/Crystal brands are our suggestions (low severity). | shrimp-po-boy |
| `roasted-salsa-verde` | keep | Matches. | mission-style-burritos, fry-bread-tacos |

## Component proposals

- `french-dip-au-jus` — used by french-dip-sandwiches-chargers, french-dip-sandwiches-rams. Shared scratch jus; draft in workers/afc-west-1.md and workers/nfc-west-2.md.
- `mumbo-sauce` — used by chicken-wings-with-mumbo-sauce. DC's defining condiment; purchased bottles exist. Draft in workers/nfc-east-1.md. Follow-up: not added; the recipe now makes Anthony Thomas's sauce inline.
- `tampa-roast-pork` — used by tampa-cuban-sandwich-with-salami. Decide: new component, reuse cuban-mojo-pork, or keep purchased pork.
- `new-orleans-olive-salad` — used by muffuletta-sandwich. Olive salad is a standalone jarred product (e.g. Central Grocery); good make-or-buy fit.
- `cincinnati-chili (optional)` — used by cheese-coneys, cincinnati-chili-over-spaghetti. Shared chili base; the two recipes use different sources, so reconcile first.

## Unresolved evidence

All five items below were resolved in the approved follow-up. See [Follow-up: approved replacements](#follow-up-approved-replacements).

- `chicago-oil-packed-giardiniera`: chilipeppermadness 403, archive.ph 429, no Wayback captures. **Resolved:** the source was replaced.
- `kansas-city-burnt-ends`: the Big Bad Beef Rub page was blocked. **Resolved:** a saved copy of the rub recipe card was read.
- `viet-cajun-crawfish`: Roadfood is still blocked (403). **Resolved:** the source was replaced.
- `pit-beef-sandwiches`, `chicken-wings-with-mumbo-sauce`: the Washington Post paywall was not bypassed. **Resolved:** both sources were replaced after approval.

## Follow-up: approved replacements

These changes were applied on branch `fix/recipe-review-fixes` after the owner approved them. Websites were read as evidence only. No paywall was bypassed.

### pit-beef-sandwiches

- **New source:** <https://meatwave.com/recipes/baltimore-pit-beef-recipe> (Joshua Bousel).
- **Why this source:** Baltimore stands cook seasoned top or bottom round over hot charcoal, keep it rare to medium-rare, shave it thin, and serve it on a kaiser roll with raw onion and horseradish sauce. Sources: the Chaps history and Baltimore Banner reporting. Meatwave follows all of that: bottom round, a paprika and onion-powder rub, rest from 1 hour to overnight, charcoal, and 120°F for rare or 125–130°F for medium-rare.
- **Other candidate:** Carne Diem, which was a less close match to stand practice.
- **Changes:**
  - Rub, cook and doneness now follow Meatwave.
  - Yield is 10–12 servings on 10 rolls.
  - Tiger sauce stays as the `baltimore-horseradish-sauce` component, at 1 cup (about 1 1/2 tablespoons per sandwich). The component text was updated to match.
- **Photo:** the Pellets and Pits photo is kept.

### chicken-wings-with-mumbo-sauce

- **New source:** <https://www.today.com/recipes/mambo-chicken-wings-t300767> (D.C. chef Anthony Thomas, who calls mumbo "simply a DC staple").
- **Corroboration:**
  - Black Foodie: D.C. mumbo sauce.
  - Food Republic: a ketchup-vinegar base with a sweetener and hot sauce.
  - WETA Boundary Stones: a D.C. carryout staple since the 1960s, thinner than Chicago's.
- **Changes:**
  - Wings marinate in buttermilk, get a seasoned flour dredge, and fry at 350°F for 8–10 minutes.
  - The sauce is simmered for 8–10 minutes.
  - Timing and the practical-time bucket were updated.
  - The Mumbo Meets Tex-Mex prep plan now marinates the wings ahead.
- **Open question:** the photo is still credited to The Washington Post and shows unbreaded wings. Confirm or replace it.

### chicago-oil-packed-giardiniera (component)

- **New source:** <https://www.thechoppingblock.com/blog/the-recipe-for-real-chicago-style-giardiniera>. This is the Chicago cooking school's serrano-based recipe.
- **Changes:**
  - Scaled to a quarter of the 10-pint batch.
  - Salted overnight and marinated at least 1 week.
- **Storage:** kept refrigerated. The source's water-bath canning is not used, because oil-packed vegetables have no tested home-canning process.
- **Consumers:** italian-beef-sandwiches and tavern-style-thin-crust-pizza are now complete keeps. Their amounts did not change.

### kansas-city-burnt-ends

- **Evidence:** a saved copy of the AmazingRibs Big Bad Beef Rub recipe card, which the burnt-ends source links to.
- **Full batch:** 3 tablespoons pepper, 1 tablespoon each sugar and onion powder, 2 teaspoons each mustard, garlic and chili powder, 1 teaspoon chipotle or cayenne.
- **Finding:** the recipe's rub is exactly half of that, about 1/4 cup, which matches its "apply about 1/4 cup".
- **Change:** the rub heading is now labeled as a half batch. Decision: keep.

### viet-cajun-crawfish

- **New source:** <https://www.feedmi.org/how-to-make-the-best-viet-cajun-crawfish/>. This is Mimi's family recipe. She is a Vietnam-born cook living in Austin, TX, and recommends Houston's Crawfish Cafe.
- **Corroboration:** Houstonia (<https://www.houstoniamag.com/eat-and-drink/2022/04/viet-cajun-crawfish-houston>) describes the Houston style as a generous garlic and butter toss after the boil, with Cajun seasoning and sometimes lemongrass or ginger.
- **Why not Roadfood:** it still returns 403.
- **Rejected alternatives:**
  - Houston Hotspots: a very long 20-minute boil, and the recipe is modeled on LA's Boiling Crab.
  - The Food Dictator: a self-described personal version.
- **Changes:**
  - The full source batch is used: 15 lb, 5 servings.
  - Orange and orange-juice boil with sausage, peanuts, corn and potatoes.
  - 5-minute boil plus a 10-minute soak.
  - Cajun garlic-butter toss.
  - This makes the earlier Zatarain's/Old Bay correction unnecessary.
- **Note:** the source has no lemongrass. The Kitchen Notes cite Houstonia for that common restaurant addition.

## Second follow-up: photos, giardiniera and crawfish

Requested after the first follow-up. Photos with unverifiable or mismatched credits were replaced with openly licensed images. Each license was checked on the creator's Flickr page or on Wikimedia Commons. Credits print as "Photo: <credit>".

### Photo replacements

| Recipe | Previous credit | New photo | Creator | License | Verified at | Changes |
| --- | --- | --- | --- | --- | --- | --- |
| cuban-sandwich | King Arthur Baking | "Versailles, Calle Ocho, Miami - Cuban Sandwich" (Versailles, Little Havana, 2019-08-15) | Todd Van Hoosear | [CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0/) | <https://commons.wikimedia.org/w/index.php?curid=106640592>, <https://www.flickr.com/photos/vanhoosear/49397507642/> | Resized to 1600 px; credit says "(resized)" |
| roast-pork-sandwich | www.bonappetit.com | "tommy dinic's roast pork sandwich" (pork and broccoli rabe, 2009-05-30) | Krista (scaredykat) | [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/) | <https://www.flickr.com/photos/49215102@N00/3588153350> | None |
| pimento-cheese-sandwiches | Food.com | "Kitsch'n 155: Pimento Cheese Sandwich" (cold, on wheat, with a Cheerwine) | AVID Vines | [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/) | <https://www.flickr.com/photos/75921150@N00/6079613684> | None |
| fry-bread-tacos | Instant Pot | "Navajo tacos" (Arizona, 2016-08-11) | Gregg Montesi | [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) | <https://commons.wikimedia.org/w/index.php?curid=93933494>, <https://www.flickr.com/photos/14068186@N02/29129312806/> | Resized to 1600 px |
| chicken-wings-with-mumbo-sauce | The Washington Post | "Chicken wings and mumbo sauce" (carryout box with a cup of mumbo) | tanyaboza | [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/) | <https://commons.wikimedia.org/wiki/File:Chicken_wings_and_mumbo_sauce.jpg>, <https://www.flickr.com/photos/42007902@N04/11040683703/> | None |

- **Pimento caveat:** the photo was taken at a diner in Decatur, GA, not in Charlotte. It was the only openly licensed image found of a cold, classic pimento cheese sandwich. Rejected candidates were grilled, fried, on crackers, party trays or a tub of spread.
- **Mumbo:** the TODAY photo that goes with the new source is copyrighted, so it was not used.
- **Not replaced:** viet-cajun-crawfish keeps its Houston Chronicle photo (credited to Chron). It still shows garlic-butter crawfish with no corn or sausage, so it matches the new recipe. It was not among the flagged credits, and its license was not checked.

### chicago-oil-packed-giardiniera (component), second change

- **Reason:** the user asked for a version that doesn't need a week in the fridge.
- **New source:** <https://www.insidehook.com/food/giardiniera-chicago-pizzeria-italian-beef-pizza-recipe>. This is Lou Malnati's (Chicago pizzeria) hot giardiniera, published by InsideHook. I read the live page.
- **Method:** a 12–24 hour cold salt brine, then a rinse, then the vegetables are dressed with chili flakes, black pepper, garlic, white wine vinegar and olive oil. It chills overnight and is "ready to enjoy the next day", about 2 days in total.
- **Caveats:**
  - The heat comes from chili flakes, not fresh serranos or sport peppers.
  - It has no bell pepper or oregano.
  - InsideHook's Chicago giardiniera taste-test history piece (<https://www.insidehook.com/chicago/chicago-style-giardiniera-taste-test-history>) treats olives as a legitimate variant.
  - An optional sliced-serrano addition is labeled as this book's variation.
  - The source gives no yield. "About 2 quarts" is this book's estimate.
- **Replaced:** The Chopping Block's serrano recipe (1 week or more of marinating) is no longer the component's source.
- **Consumers:** italian-beef-sandwiches (1 cup) and tavern-style-thin-crust-pizza (1/4 cup) are unchanged in amount. Confidence: medium-high.

### viet-cajun-crawfish, second change

- **Reason:** the user asked for a recipe that includes lemongrass, if lemongrass is authentic.
- **Evidence on lemongrass:** Houstonia calls lemongrass (and ginger) a common, legitimate Houston addition to the Cajun boil, but not a defining one. The defining traits are the Cajun spice boil and the garlic-butter toss afterwards.
- **New source:** <https://ediblehouston.ediblecommunities.com/recipe/recipes-edible-houston-s-signature-vietnamese-crawfish-boil/>, Susan L. Ebert for Edible Houston. I read the live page.
- **What the source uses:**
  - A 30-lb sack in a 30-quart pot.
  - A boil with vinegar, celery, lemongrass, garlic, ginger, galangal, Thai basil, citrus leaves, jalapeños and squeezed oranges, lemons and limes.
  - Vegetables cooked for 10 minutes plus 2–3 minutes, then removed.
  - Crawfish in 10-lb batches: brought to a bubble, heat off, covered steep for about 10 minutes until they sink.
  - A garlic butter spiced with boil spice, with lime wedges.
- **Changes:**
  - Every amount is halved to 15 lb, which matches the previous yield, and cooked in two batches. The scaling is labeled as this book's.
  - The rinse step is labeled as standard practice.
  - The source's method omits where the lemongrass, galangal and citrus leaves go. This book adds them with the other aromatics and says so. Readability B.
- **Removed with FeedMi:** the orange juice, sausage, peanuts and corn.
- **Photo and index:** the photo still fits. The index buckets are unchanged (seafood, over 60 minutes, premium).
- **Caveat:** only one outlet was found for this exact recipe. Confidence: medium.
