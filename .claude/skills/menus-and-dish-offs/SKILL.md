---
name: menus-and-dish-offs
description: Create or edit game-day menus (menus/game-day/) and division dish-offs (menus/divisions/) in the NFL cookbook.
---

# Menus and dish-offs

Both are YAML files that list recipe **ids**. The book prints the page numbers
itself, so never write page numbers in them.

## Game-day menu

The path is `menus/game-day/<type>/<id>.yml`. `<type>` must be an id from
`data/menu-types.yml` (grudge-match-grub, shared-prep, across-the-league,
premium-day, fast-day, ...). To add a new type, add it to that file and create
its directory.

```yaml
id: pizza-playoffs          # == file name
title: Pizza Playoffs
subtitle: Bears + Lions + Jets   # optional
status: published
order: 2                    # optional sort key within the type
recipes:                    # at least one; must be published recipe ids
- tavern-style-thin-crust-pizza
- detroit-style-pizza
why_it_works: One sentence.
prep_plan: One sentence.
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
```

## Rules and checks

- Find recipe ids with `ls recipes/*/*/*/`. A dish-off should use recipes from
  its own division.
- Published menus may only reference published recipes.
- Keep text short: the cards share a page.
- Run `uv run nfl-book validate`, then `make pdf`. Look at the division pages and
  the Game Day Menus pages.
- Run `make check` and add a CHANGELOG entry.
