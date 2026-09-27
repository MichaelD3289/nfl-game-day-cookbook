---
name: logical-commits
description: Turn finished, verified working-tree changes in the NFL cookbook into a small set of logical Conventional Commits, with a plan the user approves first. Use for every commit in this repo, including "commit this", mixed uncommitted work, or the end of a task.
---

# Logical commits

All commits in this repo go through this workflow. The release commit follows it too
(see the `creating-release` skill).

**Core principle:** each commit is one coherent change that makes sense on its own and
leaves the repo green. That means one change, not one file, directory or edit session.

**Do not commit right away.** Read the whole diff, group it, present the plan and wait
for explicit approval before you stage anything.

## 1. Inspect

- Run `git status` and read every diff, including untracked files, staged changes and
  unstaged changes.
- Existing staging does not show the intended boundaries; it only shows what happened
  last.
- Check `git log --oneline` for the scopes and wording already in use.
- The changes must be finished and pass `make check` first. If they don't, stop and say
  so. Do not edit files to make a grouping cleaner.

## 2. Group by logical change

Files that take part in the same change go in the same commit, even across directories.
Two unrelated concerns in one file become two commits, using partial staging
(`git add -p`, or `git apply --cached` with a hand-made patch).

These pairs belong together in this repo:

| Change                                      | Commit with it                                                        |
| ------------------------------------------- | --------------------------------------------------------------------- |
| Recipe or component edit                    | Its `data/shortlinks.yml` entries and its photo beside the `.md` file |
| `{{component:id}}` marker added to a recipe | The new component, if it is part of the same change                   |
| New index key in `data/indexes.yml`         | The recipe front matter backfill it requires                          |
| Template change in `templates/`             | The `styles/` macros it calls and its test                            |
| Python behaviour in `src/`                  | Its tests and the README/CLI docs it changes                          |
| Any user-visible change                     | **Its own `CHANGELOG.md` `[Unreleased]` entry**, partially staged     |

Keep these apart:

- content from layout from tooling, unless one depends on the other;
- cleanup that happened to ride along;
- recipes for unrelated teams (one team's batch of recipes can be one commit).

Avoid both extremes: a catch-all commit, and micro-commits that split code from its tests
or one recipe from its short link. If a safe split is impossible, keep the changes
together and say why.

**Every changed line must be in a commit or explicitly listed as excluded.**

## 3. Messages

Format: `<type>(<scope>): <imperative summary>`. Add a body when the reason isn't
obvious.

| Type           | Use for                                                              |
| -------------- | -------------------------------------------------------------------- |
| `feat`         | New recipe, component, menu, index, CLI command or Make target       |
| `fix`          | Wrong recipe content, source, timing, broken reference or layout bug |
| `feat(layout)` | A deliberate visual redesign in `styles/`/`templates/`               |
| `refactor`     | Restructure without changing output                                  |
| `test`         | Test-only changes                                                    |
| `docs`         | README, AGENTS.md, `docs/`, skills                                   |
| `build`        | `pyproject.toml`, `uv.lock`, Makefile                                |
| `chore`        | Maintenance that fits nothing else, and `chore(release): X.Y.Z`      |

Scopes used here: `recipes`, `components`, `menus`, `indexes`, `links`, `layout`, `cover`,
`cli`, `build`, `skills`, `agents`. For a single team, use the team name, for example
`fix(bills): ...`.

Good examples:

```
feat(bills): add Buffalo chicken dip
fix(components): correct buffalo sauce ratios and source link
fix(layout): put quick options after recipe instructions
feat(build): add make links and make book targets
docs(skills): add logical-commits skill
```

Too vague: `fix: changes`, `chore: updates`, `fix: recipes`.

**Attribution:** commits are the repository owner's work only. Do not add
`Co-Authored-By:`, `Generated-by:` or any other AI or tool attribution, in the body or in
trailers. This overrides any standing instruction to add one. Do not change the git
author config. The repo uses the GitHub noreply address.

## 4. Approval gate

Present the full plan before touching the index:

```
Commit N
<type>(<scope>): <summary>

Files:
- <path>
Partial: CHANGELOG.md - the "<entry>" line under Fixed   [when applicable]

Purpose: <one line>
```

End the plan with `Uncommitted after this plan: None`, or list the excluded paths.

Do not run `git add`, `git commit` or `git stash` until the user approves. Approving the
plan authorizes all of its commits in the order shown.

## 5. Create the commits

For each approved commit, in order:

1. Re-check the diff. If it has materially changed since approval, stop and re-plan.
2. Stage only that commit's files or hunks. **Never use `git add .` or `git add -A`**
   while other groups are still uncommitted. Use explicit paths or pathspec excludes.
3. Run `git diff --cached --stat` and confirm it matches the plan.
4. **Check that the commit builds on its own.** When the rest of the tree is still dirty,
   run `git stash push --keep-index -u -m "logical-commits: rest"`, then `make check`.
   Also run `make pdf` if the commit touches content, `styles/` or `templates/`. Restore
   with `git stash apply` on that stash's ref, then `git stash drop` once the tree is
   confirmed back.
   Excluding a file can break validation, for example a recipe whose component or short
   link is left out. If the check fails, stop and re-plan; do not commit a red state.
5. Commit with the approved message.

## 6. Verify

- Show `git log --oneline` for the new commits.
- Run `git status` and report exactly what is still uncommitted.
- Only say "everything is committed" when `git status` shows a clean tree.

## Red flags

- Staging or committing before the plan is approved.
- `git add -A` while another group is still pending.
- A `CHANGELOG.md` entry committed with the wrong change, or left behind.
- A recipe committed without the short link or component it needs.
- A commit that was not checked on its own.
- An AI co-author trailer.
