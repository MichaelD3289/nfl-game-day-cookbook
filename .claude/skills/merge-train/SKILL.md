---
name: merge-train
description: "Merge a batch of open pull requests in dependency order and cut releases between them: a read-only survey, a release plan the user approves, rebases of stacked PRs, admin squash merges, and checks that each release published. Use when asked to merge the open PRs, group PRs into releases, or run a merge train."
---

# Merge train

A merge train has two phases. Phase 1 is read-only and ends with a plan the user
approves. Phase 2 carries the plan out. Every merge, push, rebase and version bump waits
for that approval.

Each release in the train follows `creating-release`, and each commit you make follows
`logical-commits`. This skill adds only what comes from merging several PRs in a row.

## Phase 1: survey and plan

Run `git fetch origin` first, and read `main` as `origin/main`. Local `main` is often
behind.

1. **Find what's already on `main` but unreleased.** Use `gh release list`,
   `gh api repos/{owner}/{repo}/compare/<latest-tag>...main`, and the `[Unreleased]`
   section of `CHANGELOG.md` on `origin/main`. Dependency bumps with no CHANGELOG entry
   don't need a release of their own.
2. **Read every open PR** with `gh pr view <n> --json`, using the fields
   `baseRefName,headRefOid,files,commits,statusCheckRollup,mergeStateStatus,closingIssuesReferences`.
   For each PR, record:
   - its base branch (any base other than `main` means it's **stacked**);
   - files it shares with other PRs, and what those shared hunks change;
   - its CHANGELOG sections, which set the bump;
   - its CI status;
   - its linked issues. A PR whose issue carries `in-progress` stays out of the train;
     name it in the plan.
3. **Order the merges.** Dependencies merge first, and each stacked PR merges right
   after its base.
4. **Place the releases,** using the bump table in `creating-release`:
   - A release always ships a coherent state. Recipes removed in one PR and replaced in
     the next go out in the same release.
   - A large or risky change, such as a site redesign, gets a release of its own. Then
     the rest isn't held up by its review, and a patch release can fix it.
   - Every release contains at least one change a reader or user would notice.
5. **Present the plan** as a table with one row per step, in order: the PR or release,
   what it contains, the bump and version, and its risks. Name the single biggest risk.
   Ask once whether admin bypass and force-pushes are approved for the whole train.

Phase 1 is done when every open PR appears in the plan or in its excluded list, and the
user has approved the plan.

## Phase 2: run the train

### Merging

`main` requires a code-owner approval, a passing `Validate` check and an up-to-date
branch. The owner is the only code owner and can't approve their own PRs, so merges use
`gh pr merge <n> --squash --admin --match-head-commit <sha>`. Merge once CI is green,
unless the user says to force a PR through.

PRs are squash-merged and their head branches are deleted. When a base branch is
deleted, GitHub retargets the PRs stacked on it to `main`.

### Rebasing a stacked PR

After its base is squash-merged, a stacked PR still carries the base's original commits.
A three-way merge can then silently keep `main`'s version of lines the stacked PR had
changed (for example, a recipe count on the cover). Replay only the PR's own commits:

```sh
git rebase --onto origin/main <old-base-head-sha> <branch>
git range-diff <old-base-head-sha>..<old-branch-sha> origin/main..<branch>
git diff origin/main -- <files both PRs touched>
```

The rebase is done when `range-diff` shows the PR's commits unchanged, and the shared
lines show the stacked PR's values.

### Rebasing onto a fresh release

After a release, a rebased PR's CHANGELOG lines can land under the version that was just
released instead of `[Unreleased]`. Read `git diff origin/main -- CHANGELOG.md` after
every rebase. Move each entry under `[Unreleased]` inside the commit that owns it.

### Pushing

Push rebased branches with `git push --force-with-lease=<branch>:<expected-old-sha>`.
Pushes run the pre-push hook. pre-commit hides the output of hooks that pass, so a line
like `make check....Passed` means the whole suite ran.

### Releasing

Branch each release from a freshly fetched `origin/main` into its own worktree, and run
`creating-release` there. To watch publication, find the "Tag release from main" run
with `gh run list --commit <merge-sha>`. That run tags the commit and calls the release
workflow.

A release is done when `gh release view vX.Y.Z` lists the book PDF, the eight division
booklets, the recipe cards PDF, the EPUB and the website zip.

### Root causes

A failure in a hook, build step or tool gets its root cause found before the train moves
on. When tests run inside git hooks, check afterwards that `.git/config` still has
`core.bare = false` and no `[user]` section the tests added. Report every problem you
leave unfixed.

### Housekeeping

Remove each merged branch's worktree and local branch once no command is running in it.
Worktrees you didn't create belong to other sessions; list them in the report.

## Report

Finish with:

- a table of merges in order, each with its squash commit SHA;
- each release with its URL and asset count;
- every step that differed from the approved plan, and why;
- open problems found and not fixed.
