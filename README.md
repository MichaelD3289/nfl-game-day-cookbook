# NFL Game Day Cookbook

## Read & download

Explore recipes online, print the cookbook, or download the website to serve locally.

| Format                 | Open or download                                                                                                               |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **Website**            | [Browse the cookbook](https://michaeld3289.github.io/nfl-game-day-cookbook/)                                                   |
| **Printable cookbook** | [Download PDF](https://github.com/MichaelD3289/nfl-game-day-cookbook/releases/latest/download/nfl-game-day-recipe-booklet.pdf) |
| **Ebook**              | [Download EPUB](https://github.com/MichaelD3289/nfl-game-day-cookbook/releases/latest/download/nfl-game-day-cookbook.epub)     |
| **Website archive**    | [Download HTML ZIP](https://github.com/MichaelD3289/nfl-game-day-cookbook/releases/latest/download/nfl-game-day-website.zip)   |

These links follow the latest published stable release.

[All release assets](https://github.com/MichaelD3289/nfl-game-day-cookbook/releases/latest) ·
[Release notes & earlier versions](https://github.com/MichaelD3289/nfl-game-day-cookbook/releases)

## How it works

A "book as code" pipeline. Recipes are authored as Markdown with YAML front matter.
The pipeline validates them, resolves them into a book model, renders that model to
Quarto QMD through Jinja2 templates, and compiles a PDF with Quarto + LaTeX. LaTeX
resolves every page number from labels. Python never computes one.

```
Markdown/YAML ──discover──▶ Pydantic models ──validate──▶ resolve (published only)
      ──▶ Jinja2 ─▶ generated/book/*.qmd + manifest.json ──quarto/LaTeX──▶ dist/*.pdf
      ──▶ post-build: PDF named destinations ─▶ pagemap.json ─▶ manifest checks
```

## Contributing

Recipe suggestions, homemade components, division dish-offs, rivalry menus, and other
game-day spreads are welcome—even without coding experience.
See [CONTRIBUTING.md](CONTRIBUTING.md) to suggest a dish or open a pull request.
Please follow the [code of conduct](CODE_OF_CONDUCT.md); report security issues using
[SECURITY.md](SECURITY.md).

## License

Software and developer documentation: [MIT](LICENSE).
Original cookbook writing and original images: [CC BY 4.0](LICENSE-CONTENT.md).
Both allow commercial reuse under their terms. Third-party recipes, photos, and other
material retain their own rights; see [third-party notices](THIRD_PARTY.md).

## Requirements

- [uv](https://docs.astral.sh/uv/). Python and every Python dependency are managed with
  `uv sync`.
- For PDFs only: [Quarto](https://quarto.org) and TinyTeX (`quarto install tinytex`).
  Everything else, including validation, QMD generation and the tests, works without
  them.

## Layout

| Path                                              | What                                                              |
| ------------------------------------------------- | ----------------------------------------------------------------- |
| `data/book.yml`                                   | Book title, paper, output settings and review age limit           |
| `data/nfl.yml`                                    | Conferences, divisions and 32 teams (drives the directory layout) |
| `data/indexes.yml`                                | Search-index definitions (course, main ingredient, ...)           |
| `data/menu-types.yml`, `data/component-kinds.yml` | Menu groups and "Make It or Buy It" kinds                         |
| `data/shortlinks.yml`                             | Cached source URL → short URL (written only by `prepare-links`)   |
| `recipes/<conf>/<div>/<team>/<id>.md`             | One recipe. Its team comes from the path                          |
| `components/<kind>/<id>.md`                       | Shared sauces, dips, seasonings, ...                              |
| `menus/game-day/<type>/<id>.yml`                  | Game-day menus                                                    |
| `menus/divisions/<conf>/<div>/<id>.yml`           | Division dish-offs                                                |
| `book/frontmatter/cover.md`                       | Cover copy                                                        |
| `templates/`, `styles/`                           | Jinja2 QMD templates and LaTeX styles                             |
| `generated/`, `dist/`                             | Build output (git-ignored, never edited)                          |
| `tests/fixtures/sample-book/`                     | Synthetic content used by the tests                               |

## Content format

```markdown
---
id: buffalo-sliders # must match the file name
title: Buffalo Chicken Sliders
status: draft # draft | testing | published | retired
course: appetizers # a bucket of the `course` index
yield: 12 sliders
servings: 4-6 # optional; people fed, when yield isn't "N servings"
index: # one value per index in data/indexes.yml
  main_ingredient: poultry
  practical_time: under-30-minutes
  cost: pantry-friendly
quick_options: # optional per-recipe override of a component's quick_buy
  wing-sauce: Frank's RedHot Wings Sauce
source:
  url: https://example.com/full/original/url
---

## Ingredients

- 1 cup wing sauce {{component:wing-sauce}}

## Instructions

...
```

Ingredient lines stay free text, but the build reads their amounts so the website can
scale them (see below). Lead with the amount (`1 1/2 cups beef broth`, `3 garlic
cloves`) and write a space before the unit. Add `{{no-scale}}` to a line whose amount
must not change with the batch size, such as frying oil measured by pot depth.

Components use the sections `## Ingredients`, `## From Scratch` and an optional
`## Note`, plus the front-matter fields `quick_buy` and `always_include`. A component
that no published recipe reaches (directly or through other components) is left out of
the book unless it sets `always_include: true`.

## Commands

```sh
uv sync                                   # install
make book                                 # everything: make links, then make pdf
uv run nfl-book validate [PATHS...]       # validate everything (optionally report only PATHS)
uv run nfl-book stats [--format json|markdown]  # where the cookbook is thin (or `make stats`)
uv run nfl-book prepare-links             # the ONLY network step (or `make links`): fill data/shortlinks.yml
uv run nfl-book preview PATH [--no-pdf]   # render one recipe/component (drafts allowed)
uv run nfl-book build [--no-pdf] [--strict]   # published-only book -> dist/
uv run nfl-book clean                     # remove generated/ and dist/
uv run nfl-book new recipe --team bills --slug buffalo-sliders
uv run nfl-book new component --kind sauces --slug wing-sauce
```

Global options `--root`, `--content`, `--generated` and `--dist` point the CLI at
another content tree. For example, to build the fixture book:

```sh
D=$(mktemp -d); cp -R tests/fixtures/sample-book/. "$D"; cp data/{book,nfl,indexes,menu-types,component-kinds}.yml "$D/data/"
uv run nfl-book --content "$D" --generated "$D/generated" --dist "$D/dist" build --no-pdf
```

Make targets: `make check` (lint, tests, validate), `make test`, `make lint`,
`make preview FILE=...`, `make pdf`, `make stats` (`FORMAT=markdown` or `FORMAT=json`)
and `make clean`.

`nfl-book stats` shows where the cookbook is thin. It counts published, testing and
draft content (not retired) and lists recipes per team by status (fewest first), teams
missing a course, divisions with fewer than two dish-offs, recipes per index bucket
(buckets under 10% of recipes are marked thin), how many recipes use each component
and which components none use, and game-day menu types with fewer than three menus. It
is informational: warnings and errors belong to `validate`, and it exits non-zero only
when content fails to load.

## How page numbers work

Every page places LaTeX labels (`recipe:<id>`, `recipe:<id>:end`, `component:<id>`,
`division:<key>`, `menu:<id>`, `index:<id>`, ...). Indexes, contents and "used in" lists
print `\pageref`-style references to those labels. After compiling, the build reads the
PDF's named destinations into `generated/pagemap.json`, then checks them against
`generated/book/manifest.json`. Every expected anchor must exist, and a recipe should
start and end on the same page. Overflows are warnings, or errors with `--strict`.

## Shortlinks and QR codes

Source URLs in front matter are always full, canonical URLs. `prepare-links` shortens
any uncached URL of published content and appends the result to `data/shortlinks.yml`.
It never rewrites existing entries or source files. Builds read that cache offline, so
a published recipe whose URL is missing from it fails validation. QR codes are generated
deterministically and open the item's website page (see below); without `website_url`,
and for draft previews, they encode the full source URL. The printed source link text
uses the short URL.

See `AGENTS.md` for the rules contributors (human or AI) follow.

## Recipe quality reviews

Use the project Claude skill: `/review-recipes buffalo-wings`,
`/review-recipes buffalo-wings, beer-brats`, `/review-recipes afc/east/bills`, or
`/review-recipes all`.
It coordinates research workers and an editorial orchestrator across city fit,
authenticity, source fidelity, ingredient specificity and Make It or Buy It coverage.
Default mode recommends corrections and records completed-review metadata;
`--apply` also applies adjudicated fixes, while `--read-only` preserves metadata.
Reports go under `docs/reviews/`. See `.claude/skills/review-recipes/SKILL.md`.

Recipes and components support optional, non-printing metadata:

```yaml
last_reviewed_at: null # or YYYY-MM-DD after a completed review
last_reviewed_notes: null # outcome, outstanding findings and report path
```

A review date does not mean a recipe passed. Incomplete reviews do not replace
prior completed-review metadata. Existing recipes and components begin with empty
fields; no historical review dates are inferred. These fields do not affect booklet
content.

`review_max_age_days` in `data/book.yml` (365) sets how old a review may get.
`nfl-book validate` warns about each published recipe or component whose
`last_reviewed_at` is missing or older than that, and about dates after today,
naming the file. These are warnings only, so `make check` and `build --strict` stay
green. Remove the setting or set it to `null` to turn the check off.

## Website output

```sh
make website                              # offline HTML build -> dist/site/
uv run nfl-book website --no-render        # generate only -> generated/site/
python3 -m http.server 8000 --directory dist/site
```

Open `http://localhost:8000` after starting the preview server. Quarto is required
for the HTML build; TinyTeX is needed only for the PDF. Local builds never deploy.
The website uses the same published sources as the PDF, with separate web templates
and styles, searchable recipes, division/team navigation, menus, indexes, photos,
and linked Q quick-option cards. Editorial review metadata stays private.

Recipe and component pages can be **scaled** (½× to 4×, or by the number of people
when a recipe has servings). Amounts are converted to the most readable unit, so
tripling 4 teaspoons reads ¼ cup; counts stay whole and ranges stay ranges. The
scale is kept in the page URL (`?scale=2`) and carried to linked component pages.
The yield scales too: every count and measured amount in it ("8 large or 12 standard
bagels" doubles both), except per-portion counts ("4 shrimp each") and sizes
("12-inch"). A yield with no number, such as "One 13-by-9-inch pizza", shows the
batch count instead ("(2×)").
`styles/website-scale.js` does the conversion in the browser; its tests run with
Node.js and are skipped when Node is not installed. The PDF is never scaled.

Recipe, component, game-day menu and division pages have a **Print** button
(`styles/website-print.js`, shown only when JavaScript runs). The `@media print`
rules in `styles/website.css` hide the site chrome and lay a recipe out on one page
where it fits. The browser prints the page as shown, so a scaled recipe prints its
scaled amounts, with a "Scaled 2× · serves 12" note and the page address at the foot.

Recipe, component, division, menu and Make It or Buy It pages have **Suggest**
prompts. They open prefilled quick issue templates on GitHub and, once
`suggestion_form_url` is set in `data/book.yml`, a form that needs no GitHub
account. Setup is in [docs/website-suggestions.md](docs/website-suggestions.md).

When `website_url` is set in `data/book.yml`, every published recipe and component
page in the PDF links to its page in the same edition of the website
(`vX.Y.Z/recipe-<id>.html` or `vX.Y.Z/component-<id>.html`, using the package version)
through a short "View this page online" label and its QR code, and the cover explains
this once. The website pages show the same QR code, captioned "Scan to open on your
phone". Every release keeps its site at `/vX.Y.Z/`, so the
links match the printing; they open only after that version is released. The links are
built offline from that one URL; drafts are never
linked, and the build fails if a link would open a page the website does not publish.

### Publishing to GitHub Pages

One-time repository setup: in **Settings → Pages**, choose **GitHub Actions** as
the build/deployment source. In **Settings → Environments → github-pages**, allow
`main` for the automatic release workflow (and `v*` if rebuilding from tag refs).

Release by updating the version with `uv version`, dating its CHANGELOG section, and
merging/pushing that commit to `main`. Do not create or push release tags manually.
Two workflows handle publication:

1. **Tag release from main** compares `pyproject.toml` with the highest existing stable
   version tag numerically. A higher `X.Y.Z` version creates an annotated tag at the
   pushed commit. Equal or lower versions create no tag; prerelease/development
   versions are rejected. Other tag names are ignored.
2. **Release** is called directly after tagging. It checks main ancestry, validates,
   builds the PDF, website ZIP and EPUB, publishes all three assets, and deploys every website
   version to `https://MichaelD3289.github.io/nfl-game-day-cookbook/`.

The direct call is necessary because tags pushed with GitHub's built-in token do not
trigger another push workflow. No personal access token is required. Manually pushed
tags do not trigger publication.

Both merged branches and direct pushes to `main` are eligible. A failed automatic run
can be rerun: the highest stable version's tag is reused only when it already points
to that exact pushed commit. Equal-version tags on different commits and all lower
versions are skipped. Squash merges and merge commits change commit identity, so do
not pre-tag feature branches. Local-only tags are invisible to CI; let automation
create the tag after merging. Existing tags are never moved. The Release workflow also permits rebuilding an existing tag from the
Actions tab; it does not create tags. Fixes requiring source changes need a new version.
Publishers are serialized, and older releases cannot replace the current site.

The website shows its build version and links to the latest PDF, an **All versions**
page and earlier GitHub releases.

#### Website versions

Pages serves only its latest deployment, so each release deploys every version at
once. The Release workflow downloads the website ZIP of each earlier stable release,
and `python -m nfl_book.site_archive` assembles them offline into `_pages/`:

- `/` serves the newest stable release, so existing links keep working;
- `/vX.Y.Z/` serves each release with a website ZIP, including deep links such as
  `/v0.6.0/recipe-<id>.html`;
- older versions get a banner linking to the same page in the latest version (or its
  home page if the page is gone), link to their own PDF, and carry `noindex`; the
  `/vX.Y.Z/` copy of the latest release carries `noindex` too;
- `versions.html` lists every kept version with its date and PDF;
- images (photos and QR codes under each build's `assets/`) are stored once in
  `media/`, named by a SHA-256 hash of their contents, and every version's pages
  link there with relative paths. A photo replaced in a later release gets a new
  hash, so older versions keep showing the old one. Images no version links to are
  removed, and the assembled site must pass the same offline link check as a build,
  so a missed reference fails the deploy. Release ZIPs stay self-contained.

There is no `/latest/` folder; the root is the latest version. Prereleases and tags
created before HTML support have no website ZIP and are not included. A missing or
corrupt ZIP is skipped with a warning. Pages is deployed only when the assembled root
is the newest stable tag, so rebuilding an older tag still deploys the full set with
the newest release at the root, and a missing newest ZIP skips the deploy instead of
putting older content there. Every version is kept; the workflow warns when the site
nears the 1 GB Pages limit.

### Short descriptions

Recipes and components may include a one-sentence `description` in front matter.
Describe the actual dish and its defining ingredients in plain language (roughly
12–22 words for a recipe; components can be shorter). It is not printed in the PDF.
New recipe and component scaffolds include an empty field.

On the website every recipe list (team cards, indexes, menus, dish-offs) shows the
same entry: the dish name, a small **team · course** line (the team is left out on a
card that is already about that team) and the description. Recipe and component pages
show the description under the title. Make It or Buy It shows each component as a
card with its description and a **Used in** row linking the recipes that call for it.
Game-day menu preview cards show the menu's "why it works" line and each dish's name
and team/course, and leave the dish descriptions to the full menu page.

### Preview builds

To look at a branch before it is released, run the **Preview build** workflow from the
Actions tab on that branch, or add the `preview` label to its pull request (it then
rebuilds on every push until the label is removed). The run uploads the website, PDF
and EPUB as workflow artifacts that expire after 14 days. Nothing is tagged, released
or deployed to Pages, so production is untouched. The preview website says so in a
banner on every page (`nfl-book website --preview "<label>"`); its version and
download links still point at the latest release. Unzip the website artifact and
serve it with `python3 -m http.server -d <folder>`: opening `index.html` directly
works too, but search needs a server.

## EPUB output

Run `make epub` (or `uv run nfl-book epub`) to create
`dist/nfl-game-day-cookbook.epub`. Quarto is required; TinyTeX is not.
Use `uv run nfl-book epub --no-render` to generate sources under `generated/epub`.

EPUB is reflowable: readers control font size and pagination. Recipes are grouped
by division and team, followed by game-day menus and Make It or Buy It components,
with the linked indexes at the back. Each recipe, component and menu opens on its own
page. Photos are embedded; source links and each page's "View this page online" link
(to the same edition of the website, from `website_url`) need internet. The book keeps
one identifier across editions, so reading apps update it in place.
The templates and reader-friendly single-column styles live in `templates/epub/` and
`styles/epub.css`. PDF one-page rules do not apply to EPUB.

The build checks EPUB packaging, navigation, content anchors, and embedded resources
before replacing an existing output. The release workflow publishes it alongside PDF
and HTML. For independent standards validation, install EPUBCheck separately and run
`epubcheck dist/nfl-game-day-cookbook.epub`. Always preview layout in an EPUB reader
after styling changes; package checks cannot certify visual appearance.
