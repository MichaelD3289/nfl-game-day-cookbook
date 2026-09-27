---
name: source-links
description: Manage recipe/component source URLs, the data/shortlinks.yml cache and QR codes (nfl-book prepare-links). Use when validation reports a missing short URL.
---

# Source links, short links and QR codes

> **Working from a GitHub issue?** Claim it first ([AGENTS.md](../../../AGENTS.md) rule
> 15). If the issue already has the `in-progress` label, stop and ask a human; do not
> work on it without their explicit permission. Otherwise add the label before you
> change anything.

- Front matter always holds the **full canonical URL** in `source.url`. Never put
  a short link there.
- `make links` / `uv run nfl-book prepare-links` (alias `prepare`) is the **only** command that
  uses the network. Without `--check` it:
  - shortens every uncached URL of non-retired content (drafts included) with TinyURL
  - appends the result to `data/shortlinks.yml`
    It is never run automatically by `build`, `make pdf` or `preview`. With `--check` it
    shortens nothing (see below).
- It never rewrites existing entries or source files. Never edit or replace an
  existing short URL automatically; ask the user first.
- Commit `data/shortlinks.yml` together with the content that needed it.
- Every other command is offline. A published item whose URL is not in the cache
  fails `validate`/`build` (`preview` only warns) with an error naming the file. Run `prepare-links` to fix it.
- QR codes are generated deterministically from the full source URL at build
  time; the printed link text uses the short URL. Nothing about them is committed.
- If the network is unavailable, tell the user. Don't invent short URLs.

## Dead or moved sources

- Run `uv run nfl-book prepare-links --check` (add `--report FILE` for a Markdown list),
  or read the open `link-rot` issue. It lists dead links, permanent redirects and pages
  it could not verify, with the files that use each URL. It changes nothing.
- For each entry, open the listed file and pick a replacement source by hand: the
  redirect target, a new page with the same recipe, or a Wayback Machine snapshot (the
  report links them for dead pages).
- Change `source.url` only with the user's agreement.
- A new URL needs `prepare-links` to add a new short link. Never edit or replace an
  existing entry in `data/shortlinks.yml`.
- "Could not verify" (HTTP 401, 403 or 429) often means bot protection. Check the page
  in a browser before treating it as dead.
