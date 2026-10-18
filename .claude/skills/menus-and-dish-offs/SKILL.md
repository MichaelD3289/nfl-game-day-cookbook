---
name: menus-and-dish-offs
description: Create or edit game-day menus (menus/game-day/) and division dish-offs (menus/divisions/) in the NFL cookbook.
---

# Menus and dish-offs

> **Working from a GitHub issue?** Claim it first ([AGENTS.md](../../../AGENTS.md) rule
> 15). If the issue already has the `in-progress` label, stop and ask a human; do not
> work on it without their explicit permission. Otherwise add the label before you
> change anything.

Both are YAML files that list recipe **ids**. The book prints the page numbers
itself, so never write page numbers in them.

## Game-day menu

The path is `menus/game-day/<type>/<id>.yml`. `<type>` must be an id from
`data/menu-types.yml` (grudge-match-grub, shared-prep, across-the-league,
premium-day, fast-day, ...). To add a new type, add it to that file and create
its directory.

```yaml
id: pizza-playoffs # == file name
title: Pizza Playoffs
subtitle: Bears + Lions + Jets # optional
status: published
order: 2 # optional sort key within the type
recipes: # at least one; must be published recipe ids
  - tavern-style-thin-crust-pizza
  - detroit-style-pizza
why_it_works: One sentence.
prep_plan: One sentence.
timeline: # optional; see "Kickoff timeline" below
  - at: -1d
    recipe: detroit-style-pizza
    task: Make the dough.
  - at: -30m
    task: Heat the oven. # a general task needs no recipe
  - at: kickoff
    recipe: tavern-style-thin-crust-pizza
    task: Bake the first pizza.
```

## Division dish-off

The path is `menus/divisions/<conf>/<div>/<id>.yml`. The division's two dish-offs
are printed as cards on its division page.

```yaml
id: east-coast-kickoff
title: East Coast Kickoff
status: published
order: 1
recipes:
  - buffalo-wings
  - boston-cream-pie
description: One sentence.
prep_note: One sentence.
timeline: # optional; see "Kickoff timeline" below
  - at: -1h
    recipe: buffalo-wings
    task: Fry the wings.
  - at: halftime
    recipe: boston-cream-pie
    task: Slice the pie.
```

## Kickoff timeline

`timeline` is optional on both. Each step has `at`, `task` and an optional `recipe`.

- `at` is counted back from kickoff, in one lowercase spelling per time:
  `-1d` to `-7d` (a whole day before, no clock time), `-1h` to `-23h`, `-1m` to
  `-59m`, hours and minutes together such as `-1h30m`, then `kickoff` and
  `halftime`. So `-90m` must be written `-1h30m`, and `-24h` must be `-1d`; leading
  zeros, `-1h0m`, `+`, uppercase and mixed days and hours are rejected.
- List steps in time order (equal times are fine); validate does not sort them.
- `recipe` must be one of this menu's `recipes`. Leave it out for general tasks such
  as heating the oven.
- At most 6 steps, and each `task` is one short sentence of at most 80 characters.
- Do not invent times. Convert them from the `prep_plan`/`prep_note` prose or from the
  recipes' own prep, cook and resting times.

## Rules and checks

- Find recipe ids with `ls recipes/*/*/*/`. A dish-off should use recipes from
  its own division.
- Published menus may only reference published recipes.
- Timeline steps must be in time order and name only recipes on the same menu.
- Keep text short: the cards share a page.
- Run `uv run nfl-book validate`, then `make pdf`. Look at the division pages and
  the Game Day Menus pages.
- Run `make check` and add a CHANGELOG entry.
