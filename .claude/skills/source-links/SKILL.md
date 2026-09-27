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
  uses the network. It:
  - shortens every uncached URL of non-retired content (drafts included) with TinyURL
  - appends the result to `data/shortlinks.yml`
    It is never run automatically by `build`, `make pdf` or `preview`.
- It never rewrites existing entries or source files. Never edit or replace an
  existing short URL automatically; ask the user first.
- Commit `data/shortlinks.yml` together with the content that needed it.
- Every other command is offline. A published item whose URL is not in the cache
  fails `validate`/`build` (`preview` only warns) with an error naming the file. Run `prepare-links` to fix it.
- QR codes are generated deterministically from the full source URL at build
  time; the printed link text uses the short URL. Nothing about them is committed.
- If the network is unavailable, tell the user. Don't invent short URLs.
