# Website layout

`templates/website/*.qmd.j2`, `styles/website.css` (with the Quarto theme
`styles/website.scss`) and the `styles/website-*.js` scripts are the separate HTML
presentation. `src/nfl_book/website.py` reuses the resolved book's page contexts, then
Quarto produces `dist/site/`. The print contract does not apply here: use responsive
columns and normal links instead of page numbers. Preserve the shared palette, Q cards
and source content, and keep the PDF templates and styles as they are for a
website-only change.

## Raw HTML and tests: Quarto rewrites your markup

Raw ` ```{=html} ` blocks in the web templates reach `dist/site/` only after Quarto
re-serializes them. The markup changes on the way. A bare `hidden` becomes `hidden=""`,
attribute order and quoting can change, and whitespace moves. The generated `.qmd`
(`nfl-book website --no-render`) keeps your exact text, so a test that passes there can
still fail in the release build, which renders with Quarto. This happened in 0.9.0 and
needed the 0.9.1 fix.

- Unit tests in `tests/unit/test_website.py` read the generated `.qmd` and may match
  exact strings.
- Tests of the **rendered** site (`tests/integration/test_website_build.py`) compare
  attributes, not markup. Use its `_elements(html, tag, css_class)` helper and assert on
  the returned dict, for example `assert "hidden" in bars[0]`.
- Those integration tests are skipped when Quarto is not installed, and `make check`
  still passes. A skip is not a pass: if you cannot run them, say so in the PR.
- Controls that need JavaScript ship with `hidden` and are revealed by their script, so
  readers without JavaScript see only working controls.

## Done when

`make website` passes its built-in check of local links, images and fragments, and
home, a dense recipe, a component and an index look right at desktop width and at
375px.
