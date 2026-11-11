---
name: menus-and-dish-offs
description: "Game-day menus and division dish-offs: create or edit one, add a kickoff timeline, or add a menu type."
---

# Menus and dish-offs

Both are YAML files that list recipe **ids** (find them with `ls recipes/*/*/*/`).

## Game-day menu

The path is `menus/game-day/<type>/<id>.yml`, where `<type>` is an id from
`data/menu-types.yml`. A new type needs an entry there (`id`, `title`, `description`)
and its directory.

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

The path is `menus/divisions/<conf>/<div>/<id>.yml`, and its recipes come from this
division. Dish-offs print as cards on the division page (`nfl-book stats` flags
divisions with fewer than two).

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

- `at` counts back from kickoff in one spelling per time: `-1d`..`-7d`, `-1h`..`-23h`,
  `-1m`..`-59m`, `-1h30m`, `kickoff`, `halftime` (so `-90m` is `-1h30m`, and `-24h` is
  `-1d`). Validate rejects other spellings, out-of-order steps, more than 6 steps and
  tasks over 80 characters.
- `recipe` names one of this menu's `recipes`; leave it out for general tasks such as
  heating the oven.
- Derive each time from the `prep_plan`/`prep_note` or the recipes' own prep, cook and
  resting times.

## Check it

1. `uv run nfl-book validate` reports no errors and no warnings for your file.
2. `uv run nfl-book build --strict` exits 0, so no division or menu page overflows;
   keep text short, because the cards share a page.
3. In the PDF, each card shows its recipes and timeline.
