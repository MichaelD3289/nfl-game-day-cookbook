# E. Test the Python → JS website payloads against the real JS

The website's JS (browse, menu builder, matchup) reads JSON built by hand in Python, and the JS tests run on hand-written copies of that JSON. A renamed key would pass both test suites and break the live site. This adds a single contract between them.

Blocked by C, which makes the catalog entries typed.

### Now and wanted

**From code:**

- The payloads are built as dicts in `website.py:321-416` and `catalog.py:83-112`.
- Keys are snake_case except `printPages` (`website.py:397`).
- The JS tests (`tests/unit/test_website_matchup.py:26-80`, `test_website_menu.py:31-36`) run `styles/website-*.js` under `node` on hand-written data.

Wanted:

- The menu builder and matchup payloads become dataclasses, like C's catalog entries, with one shared serializer.
- All keys are snake_case, and `printPages` is renamed in both Python and JS.
- One integration test builds the fixture website with `render=False`, takes the payloads out of the generated pages, and runs the real JS parse functions on them under `node`.
- The hand-written JS tests stay, for edge cases.

### Done when

- In the contract test, renaming any payload field in Python fails the test.
- `rg -n 'printPages' src styles` finds nothing.
- The browse, menu builder and matchup pages work in a local website build. Check manually, or with the existing JS tests plus the contract test.
- `make check` passes.

### Not included

- Changing what the JS does.
