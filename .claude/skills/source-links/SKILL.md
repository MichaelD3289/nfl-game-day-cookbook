---
name: source-links
description: "Source URLs and short links: adding or changing a source.url, a 'no short URL cached' error, or dead or moved sources from prepare-links --check or the link-rot issue."
---

# Source links and short links

- `source.url` in front matter always holds the **full canonical URL**.
- `make links` (`uv run nfl-book prepare-links`) shortens every uncached URL of
  non-retired content, drafts included, with TinyURL and appends it to
  `data/shortlinks.yml`. Commit that file together with the content that needed it.
- Existing short URLs change only by hand, with the user's agreement;
  `prepare-links` refuses to replace them. Stale entries are harmless.
- A published item whose URL is not cached fails `validate` and `build`; `preview` only
  warns.
- The printed source text uses the short URL. QR codes are built at build time and
  open the item's website page (or the full source URL for drafts); they do not depend
  on `shortlinks.yml`.
- If the network is unavailable, leave the URL uncached and tell the user; validate
  keeps failing until `prepare-links` runs.

## Dead or moved sources

1. Run `uv run nfl-book prepare-links --check` (add `--report FILE` for a Markdown
   list), or read the open `link-rot` issue. It lists dead links, permanent redirects
   and pages it could not verify, with the files that use each URL, and changes nothing.
2. "Could not verify" (HTTP 401, 403 or 429) often means bot protection. Check the page
   in a browser before treating it as dead.
3. For each dead or moved entry, open the listed file and pick a replacement source by
   hand: the redirect target, a new page with the same recipe, or a Wayback Machine
   snapshot (the report links them for dead pages).
4. With the user's agreement, change `source.url` and run `make links` for the new
   short link.

Done when every reported URL is either replaced (with the user's agreement, its new
short link added, validate clean) or confirmed live in a browser and reported back.
