# Sunday Roadtrip UI Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans to implement this plan.

**Goal:** Implement the approved A design across the existing website.

**Architecture:** Keep the resolved recipe catalog, Quarto rendering, stable routes,
and existing feature scripts. Add web-only discovery context, reuse card markup,
and update the website theme and navigation without altering other formats.

**Tech Stack:** Python, Jinja, Markdown/YAML, Quarto, native CSS and JavaScript.

**Spec:** `docs/superpowers/specs/2026-11-10-sunday-roadtrip-ui-design.md`.

## Global Constraints

- City/state orange; full NFL team names medium-weight slate gray; titles dark green.
- Published content only; fixture tests only; no production content edits.
- Preserve all existing interactive scripts, routes, anchors, and offline behavior.
- No dependencies, version changes, staging, commits, or publishing.

## Review Focus

- Empty collections and missing photos must render without broken images or exceptions.
- Long locations, full team names, and navigation labels must wrap at phone widths.
- Menu selections, filter counts, scales, and exported content retain their DOM contracts.
- Cook mode and printed pages must remain usable under the new screen theme.
- Search, team browsing, suggestions, and edition downloads remain reachable.

## Tasks

### 1. Discovery context, homepage, cards, and navigation

Files: `src/nfl_book/website.py`, `templates/website/*.qmd.j2`,
`tests/unit/test_website.py`, `tests/unit/test_website_roadtrip.py`.

- [x] Add failing synthetic tests for published homepage cards, photo/empty fallbacks,
      full team and location labels, menu-builder shortcuts, and reachable navigation.
- [x] Generate web-only card context from the existing catalog; select a small,
      deterministic set of featured recipes with course and division variety.
- [x] Implement the homepage and shared card markup. Retain existing finder/menu
      selectors and data attributes. Keep full team labels separate from course metadata.
- [x] Move site navigation to the navbar, preserving all discovery/download links.
- [x] Run targeted tests; adapt only assertions intentionally superseded by the new UI.

### 2. Apply the approved theme across existing page types

Files: `styles/website.css`, `styles/website.scss`, `CHANGELOG.md`.

- [x] Apply approved palette, system typography, photo layouts, and card hierarchy.
- [x] Style navigation, filters, builder, menu cards, recipe tools, and responsive
      fallbacks; preserve feature states and isolate screen styling from print rules.
- [x] Add the user-visible changelog entry.

### 3. Validate the real generated site and review

- [x] Run `make check`, compile the actual website, and inspect home, browse, builder,
      menu, dense recipe, component, and index pages at desktop and phone widths.
- [x] Run existing browser audits where installed tooling permits; verify search,
      filtering, selection, scaling, cook mode, and print behavior.
- [x] Review the complete diff against the approved design and preserved features.
- [x] Report the worktree, checks, preview, and any remaining limitations.

## Validation record

- Worktree: `.worktrees/sunday-roadtrip-ui`, branch `feat/sunday-roadtrip-ui`, based on `c1ba979` from current `origin/main`. The older main checkout and its untracked files are untouched.
- `make check`: 577 passed, one opt-in browser test skipped; formatting, strict mypy, and validation passed. The existing 21 missing-review-date content warnings remain.
- Opt-in rendered synthetic browser and integration checks: two passed using installed Chrome and existing Playwright tools, without installing dependencies.
- Complete-site browser audit: desktop and phone checks across eight page types; no blocking findings or external requests after the summary foreground contrast correction. Eight existing Quarto mobile-toggle ARIA warnings remain, matching the previous site.
- Actual website build and local link/asset/fragment checks passed. Quarto now explicitly renders the page glob so the ignored worktree is supported. Query-string shortcuts use HTML routes because Quarto does not rewrite those QMD links.
- Visual inspection covered the real homepage, dense recipe, and menu cards. Native-browser search returned matching recipes; a curated menu shortcut opened the real builder with three dishes and its export controls.
- Independent read-only review found no consequential issues after print-photo and menu-summary-class corrections. Existing feature JavaScript and PDF/EPUB templates are unchanged.
- No staging, commits, version changes, merges, pushes, or publication.
