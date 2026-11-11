# Sunday Roadtrip website design

Implement the approved A mockup: a warm, playful NFL cookbook that invites people
to discover regional food and assemble a Sunday spread. The approved follow-up
sets city/state in orange, full NFL team names in medium-weight slate gray, and
recipe titles in bold dark green. Keep the NFL connection explicit throughout.

Use the existing offline Quarto/Jinja website and authored photographs. Replace
the directory-style shell with primary navigation for browsing recipes, curated
menus, building a menu, and matchups. Keep team/division browsing, indexes,
Make It or Buy It, downloads, edition history, and full-text search accessible.

The homepage has a two-photo introduction, course shortcuts, regional recipe cards,
and a menu invitation. Select published content from the resolved catalog, with
graceful fallbacks for small collections and missing photos. Recipe cards and menu
listings retain the associated full team name. Apply the same visual language to
recipes, components, indexes, curated menus, the builder, and matchup pages.

Preserve route names, anchors, multi-select filters and counts, URL state, browser
storage, scaling and yields, cooking checklists and wake locks, print options,
shopping exports, kickoff timelines, source credits, QR codes, and suggestions.
The preview's single-select filters and memory-only menu are not the implementation.
Keep the production feature scripts and their DOM contracts. Preserve progressive
enhancement and print behavior. Do not change recipe content, PDF/EPUB presentation,
dependencies, or release versions.

Approaches considered: Sunday Roadtrip (selected for regional discovery and NFL
personality), Tailgate Club (stronger sports styling), and The Regional Table
(quieter culinary editorial styling). The implementation is authorized in a new
worktree; staging, commits, release preparation, and publication are outside scope.
