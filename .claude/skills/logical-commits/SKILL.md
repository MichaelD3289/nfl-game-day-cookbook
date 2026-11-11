---
name: logical-commits
description: Turn working-tree changes in the NFL cookbook into a small set of logical Conventional Commits, with a plan the user approves first, and title the pull request. Use for every commit or PR in this repo, including "commit this" and mixed uncommitted work.
---

# Logical commits

**Core principle:** each commit is one coherent change that makes sense on its own. That
means one change, not one file, directory or edit session. The release commit belongs to
`creating-release`.

## 1. Inspect

- Run `git status` and read every diff, including untracked files, staged changes and
  unstaged changes.
- Treat existing staging as a record of the last action; the boundaries come from the
  diff itself.
- Check `git log --oneline` for the scopes and wording already in use.
- The changes must be finished. If they aren't, stop and say so, and group the diff as
  it stands.

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

Format: `<type>(<scope>): <imperative summary>`, with the scope taken from
`git log --oneline`. Add a body when the reason isn't obvious.

| Type       | Use for                                                              |
| ---------- | -------------------------------------------------------------------- |
| `feat`     | New recipe, component, menu, index, CLI command or Make target       |
| `fix`      | Wrong recipe content, source, timing, broken reference or layout bug |
| `refactor` | Restructure without changing output                                  |
| `test`     | Test-only changes                                                    |
| `docs`     | README, AGENTS.md, `docs/`, skills                                   |
| `build`    | `pyproject.toml`, `uv.lock`, Makefile, hooks                         |
| `chore`    | Maintenance that fits nothing else                                   |

Good examples:

```
feat(recipes): add Buffalo chicken dip
fix(components): correct buffalo sauce ratios and source link
fix(layout): put quick options after recipe instructions
docs(skills): add logical-commits skill
```

Too vague: `fix: changes`, `chore: updates`, `fix: recipes`.

Commits are the repository owner's work only: the message ends with the summary or body,
with no trailers. Keep the git author config as it is.

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

Approval of the plan is the only gate: it authorizes all of its commits in the order
shown, and nothing is staged, committed or stashed before it.

## 5. Create the commits

For each approved commit, in order:

1. Re-check the diff. If it has materially changed since approval, stop and re-plan.
2. Stage only that commit's files or hunks by explicit path or pathspec.
3. Run `git diff --cached --stat` and confirm it matches the plan.
4. Commit with the approved message. The pre-commit hooks format staged files; if they
   change anything, re-stage those files and commit again.

`make check` runs on `git push` (the pre-push hook), so the branch must be **green**
before it leaves the machine. To check one commit alone while the rest of the tree is
dirty, set the rest aside with
`git stash push --keep-index -u -m "logical-commits:<branch>:<n>"`, capture its SHA from
`git stash list --format='%H %gs'`, run `make check`, then `git stash apply <sha>` and
drop that entry once the tree is back.

## 6. Verify

- Show `git log --oneline` for the new commits.
- Run `git status` and report exactly what is still uncommitted; "everything is
  committed" means a clean tree.

## Pull request title

PRs are squash-merged, so the **PR title becomes the one commit on `main`**. Title it
like a commit message, `<type>(<scope>): <summary>`, naming the PR's main change. The
title and description carry no AI attribution.
