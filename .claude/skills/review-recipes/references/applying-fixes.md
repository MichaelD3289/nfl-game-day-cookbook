# Applying accepted fixes (apply mode)

The orchestrator applies adjudicated fixes through `update-recipe` and `add-component`,
and owns every write to shared components, indexes, config and the changelog. Each file
has one writer at a time. The ledger hash is the snapshot: re-read a file whose current
`git hash-object` differs before writing to it, and preserve unrelated edits.

## Check every consumer

For every changed recipe or component, inspect all its consumers and check:

- Yield, scaling, scratch versus quick prep/cook/wait time and cost assumptions.
- Practical-time, course, main-ingredient and cost buckets, using existing bucket ids. A
  recipe moves to a fast bucket only when its scratch path is fast.
- Q ingredient labels, quick-option overrides, whole-component substitution amounts,
  component dependency cycles, used-in relationships and all affected recipes.
- Canonical source URL and any source title, representative photo and accurate photo
  credit. Keep an existing photo only if it still represents the selected dish.
- Menu descriptions, pairings, prep plans and claims about quick/shared preparation.
- A component is retired only when no recipe or other component still reaches it; one
  recipe dropping it is not enough.
- New canonical URLs: follow `source-links` and run `make links` once after all edits.

## Check the result

Render each edited recipe with `make preview FILE=<path>`. Done when validate reports no
errors and no warnings for the files you touched and each edited recipe fits one page.
If you skip rendering, say that the printed layout was not checked.

Record each user-visible fix under `[Unreleased]` with the `changelog` skill.
