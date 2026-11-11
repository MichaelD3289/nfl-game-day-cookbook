# Tagging, retries and republishing

Read this when publication failed or was skipped. `.github/scripts/tag_release.py` is
the code these rules describe.

`auto-tag.yml` reads the merged `main` commit's `pyproject.toml` and compares its
stable `X.Y.Z` with the highest existing stable tag (by version number, not by date):

| State at the `main` commit                                                              | Automatic result                                      |
| --------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| Package version is higher than every existing stable tag                                | Create the version tag at this commit and run Release |
| Package version equals the highest stable tag, and that tag points to this exact commit | Reuse the tag and run Release (safe retry)            |
| Same version tag points to a different commit                                           | Skip; the existing tag stays where it is              |
| Package version is lower than the highest stable tag                                    | Skip, even if an older tag points to this commit      |
| A tag is pushed without a push to `main`                                                | No automatic publication                              |

Unsupported prerelease or development versions fail with a clear error, and so does a
`CHANGELOG.md` without a `## [X.Y.Z] - YYYY-MM-DD` heading for the version.

- **A failed automatic run:** rerun it; it reuses its tag at the same commit.
- **Rebuilding an existing release's assets:**
  `gh workflow run release.yml --ref main -f tag=vX.Y.Z`. This never creates a tag, and
  the tag's commit must be in `main` history.
- **A tag that blocks publication**, or a fix that changes code or workflows: prepare a
  newer version with the bump rules and merge it into `main`.

The `v*` tag ruleset stops non-admins from moving or deleting tags; creating them is
left to automation by project rule.
