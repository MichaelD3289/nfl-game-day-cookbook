"""The Python -> JavaScript contract for the website's payloads.

Builds the fixture website without rendering, takes every payload the JS reads out of the
generated output (the matchup ``<script>`` data, the ``data-*`` attributes of the Browse
and menu builder pages, ``recipes.json``) and runs the real scripts the site ships
(``browse.js``, ``menu.js``, ``matchup.js``, copied from ``styles/website-*.js``) on them
under Node. It fails when a field the JS reads is missing or renamed on either side.

Hand-written edge cases stay in ``tests/unit/test_website_*.py``. The suggestion form
(``suggest.js``) keeps ``KINDS`` private and has no Node entry point, so its
``data-fields`` payload is not covered here.
"""

from __future__ import annotations

import json
import re
import runpy
import shutil
import subprocess
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

import pytest

from nfl_book.project import Project
from nfl_book.website import build_website

NODE = shutil.which("node")
pytestmark = pytest.mark.skipif(NODE is None, reason="Node.js is not installed")

MATCHUP_TESTS = Path(__file__).resolve().parents[1] / "unit" / "test_website_matchup.py"

# The fields matchup.js reads, by object. The test fails if the JS stops reading one
# (update this list with the JS) or reads one the payload does not have.
MATCHUP_READS = {
    "root": {"courses", "divisions", "teams", "dishes"},
    "root.courses": {"id", "singular"},  # "label" is only the fallback for "singular"
    "root.divisions": {"key", "name"},
    "root.teams": {"slug", "name", "short", "division"},
    "root.dishes": {"id", "title", "url", "course", "team", "division", "print_pages"},
}

# Every key a payload carries, read by the JS or not. Renaming a field in Python changes
# these sets, so the test fails even for a field the fixture's JS paths never read.
MATCHUP_KEYS = {**MATCHUP_READS, "root.courses": {"id", "label", "singular"}}
CATALOG_KEYS = {"version", "edition", "facets", "recipes"}
CATALOG_FACET_KEYS = {"id", "title", "source", "options"}
CATALOG_RECIPE_KEYS = set(
    [
        "id",
        "title",
        "url",
        "photo",
        "photo_size",
        "description",
        "course",
        "course_label",
        "team",
        "location",
        "conference",
        "division",
        "division_name",
        "servings",
        "yield",
        "prep",
        "cook",
        "components",
        "facets",
    ]
)
CATALOG_TEAM_KEYS = {"slug", "name", "short_name", "abbreviation"}


class _Page(HTMLParser):
    """The elements of a generated page that carry the JS's data."""

    def __init__(self) -> None:
        super().__init__()
        self.cards: dict[str, list[dict[str, str | None]]] = {"finder-card": [], "menu-dish": []}
        self.fieldsets: list[dict[str, Any]] = []
        self._open: dict[str, Any] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if tag == "li":
            for name in (data.get("class") or "").split():
                if name in self.cards:
                    self.cards[name].append(data)
        elif tag == "fieldset" and "data-facet" in data:
            self._open = {"id": data["data-facet"], "values": []}
            self.fieldsets.append(self._open)
        elif tag == "input" and self._open is not None and data.get("type") == "checkbox":
            self._open["values"].append(data["value"])

    def handle_endtag(self, tag: str) -> None:
        if tag == "fieldset":
            self._open = None


def _read(path: Path) -> _Page:
    page = _Page()
    page.feed(path.read_text(encoding="utf-8"))
    return page


@pytest.fixture(scope="module")
def site(tmp_path_factory: pytest.TempPathFactory) -> Path:
    from conftest import FIXTURE_BOOK, copy_config, make_project

    content = tmp_path_factory.mktemp("contract") / "book"
    shutil.copytree(FIXTURE_BOOK, content)
    copy_config(content)
    project: Project = make_project(content)
    result = build_website(project, render=False)
    assert result.diagnostics.ok
    return project.generated_dir / "site"


def _matchup_payload(site: Path) -> dict[str, Any]:
    text = (site / "matchup.qmd").read_text(encoding="utf-8")
    found = re.search(r'<script type="application/json" class="matchup-data">(.*?)</script>', text)
    assert found, "matchup.qmd has no matchup-data script"
    payload: dict[str, Any] = json.loads(found[1])
    return payload


def _node(program: str, argument: dict[str, Any]) -> dict[str, Any]:
    assert NODE is not None
    result = subprocess.run(
        [NODE, "-e", program, json.dumps(argument)],
        capture_output=True,
        text=True,
        check=False,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr
    report: dict[str, Any] = json.loads(result.stdout)
    return report


BROWSE_PROGRAM = r"""
const spec = JSON.parse(process.argv[1]);
const b = require(spec.browse);
global.NflBrowse = b;
const menu = require(spec.menu);
const node = (attrs, extra) => Object.assign({
  getAttribute: (k) => (k in attrs ? attrs[k] : null),
  querySelector: () => null,
}, extra || {});
const list = (cards) => ({ querySelectorAll: () => cards.map((a) => node(a)) });

const cards = b.readCards(list(spec.cards));
const fieldsets = spec.fieldsets.map((f) => node({ "data-facet": f.id }, {
  querySelectorAll: () => f.values.map((value) => ({ value, checked: false })),
}));
const facets = b.readFacets({ querySelectorAll: () => fieldsets });
const filtered = {};
facets.forEach((facet) => facet.options.forEach((option) => {
  filtered[facet.id + "/" + option] =
    b.filterRecipes(cards, { [facet.id]: [option] }).map((card) => card.id);
}));
const dishes = menu.readDishes(list(spec.dishes));
const ids = dishes.map((dish) => dish.id);
process.stdout.write(JSON.stringify({
  card_ids: cards.map((c) => c.id),
  filtered,
  dishes: dishes.map((d) => ({
    id: d.id, course: d.course, url: d.url, print_pages: d.print_pages,
    facets: d.facets,
  })),
  pages: menu.menuPages(ids, dishes, true),
}));
"""


def test_browse_and_menu_builder_read_the_catalog_facets(site: Path) -> None:
    catalog = json.loads((site / "recipes.json").read_text(encoding="utf-8"))
    browse, builder = _read(site / "browse.qmd"), _read(site / "menu-builder.qmd")
    for page in (browse, builder):
        assert [f["id"] for f in page.fieldsets] == [f["id"] for f in catalog["facets"]]
        for fieldset, facet in zip(page.fieldsets, catalog["facets"], strict=True):
            assert fieldset["values"] == [o["id"] for o in facet["options"]]
    report = _node(
        BROWSE_PROGRAM,
        {
            "browse": str(site / "browse.js"),
            "menu": str(site / "menu.js"),
            "cards": browse.cards["finder-card"],
            "dishes": builder.cards["menu-dish"],
            "fieldsets": browse.fieldsets,
        },
    )
    recipes = catalog["recipes"]
    assert set(catalog) == CATALOG_KEYS
    assert all(set(f) >= CATALOG_FACET_KEYS for f in catalog["facets"])
    assert all(set(r) == CATALOG_RECIPE_KEYS for r in recipes)
    assert all(set(r["team"]) == CATALOG_TEAM_KEYS for r in recipes)
    assert report["card_ids"] == [r["id"] for r in recipes]
    assert report["filtered"], "no facet options to filter by"
    for facet in catalog["facets"]:
        for option in facet["options"]:
            expected = [r["id"] for r in recipes if option["id"] in r["facets"][facet["id"]]]
            assert report["filtered"][f"{facet['id']}/{option['id']}"] == expected
    assert any(ids for ids in report["filtered"].values()), "every filter matched nothing"
    # The menu builder reads each dish's course, url and facets from the rendered rows.
    by_id = {r["id"]: r for r in recipes}
    assert {d["id"] for d in report["dishes"]} == set(by_id)
    for dish in report["dishes"]:
        assert dish["course"] == by_id[dish["id"]]["course"]
        assert dish["url"] == by_id[dish["id"]]["url"]
        assert dish["facets"] == by_id[dish["id"]]["facets"]
    # ... and the matchup payload prints the same component pages as the builder rows.
    matchup = {d["id"]: d["print_pages"] for d in _matchup_payload(site)["dishes"]}
    assert {d["id"]: d["print_pages"] for d in report["dishes"]} == matchup
    assert any(matchup.values()), "no fixture dish prints a component page"


MATCHUP_PROGRAM = (
    r"""
const spec = JSON.parse(process.argv[1]);
global.NflMenu = require(spec.menu);
const m = require(spec.matchup);
const reads = {};
const note = (kind, prop) => { (reads[kind] = reads[kind] || new Set()).add(prop); };
// Records every field the script reads, by the object it reads it from.
function track(value, kind) {
  if (value === null || typeof value !== "object") return value;
  return new Proxy(value, { get(target, prop, receiver) {
    const found = Reflect.get(target, prop, receiver);
    if (typeof prop === "symbol") return found;
    if (Array.isArray(target)) return /^\d+$/.test(prop) ? track(found, kind) : found;
    note(kind, prop);
    return track(found, kind + "." + prop);
  } });
}
const parse = JSON.parse;
JSON.parse = (text) => track(parse(text), "root");
"""
    + "\n"
    + "FAKE_DOM"
    + r"""
const payload = spec.payload_text;
const data = m.readData({ querySelector: () => ({ textContent: payload }) });
if (!data) throw new Error("matchup.js read no data from the page payload");
const everyone = parse(payload).teams.map((t) => t.slug);
const notes = new Set();
everyone.forEach((home) => everyone.forEach((away) => {
  m.suggest(data, home, away, []).forEach((entry) => {
    notes.add(m.sourceNote(entry, data));
    m.spreadIds([entry]);
  });
  m.matchupTitle(data, home, away);
}));
const doc = page(payload);
const calls = [];
global.NflPrint = { printBundle: (urls) => { calls.push(urls); return Promise.resolve(); },
  prefetch: () => {}, tidy: () => {}, isolate: () => {} };
m.init(doc, fakeWindow("?home=" + spec.home + "&away=" + spec.away));
doc.querySelector("input[name=print-with]").checked = true;
doc.querySelector(".print-button").click();
new Promise((r) => setTimeout(r, 0)).then(() => {
  process.stdout.write(JSON.stringify({
    reads: Object.fromEntries(Object.entries(reads).map(([k, v]) => [k, [...v].sort()])),
    notes: [...notes].sort(),
    bundles: calls,
  }));
});
"""
)


def test_matchup_reads_only_fields_the_payload_has(site: Path) -> None:
    payload = _matchup_payload(site)
    text = (site / "matchup.qmd").read_text(encoding="utf-8")
    raw = re.search(r'class="matchup-data">(.*?)</script>', text)
    assert raw
    fake_dom: str = runpy.run_path(str(MATCHUP_TESTS))["FAKE_DOM"]
    teams = sorted({d["team"] for d in payload["dishes"]})
    assert len(teams) >= 2
    report = _node(
        MATCHUP_PROGRAM.replace("FAKE_DOM", fake_dom),
        {
            "menu": str(site / "menu.js"),
            "matchup": str(site / "matchup.js"),
            "payload_text": raw[1],
            "home": teams[0],
            "away": teams[1],
        },
    )
    shapes = {
        "root": payload,
        "root.courses": payload["courses"][0],
        "root.divisions": payload["divisions"][0],
        "root.teams": payload["teams"][0],
        "root.dishes": payload["dishes"][0],
    }
    for kind, keys in MATCHUP_KEYS.items():
        found = payload if kind == "root" else payload[kind.split(".")[1]]
        for item in [found] if kind == "root" else found:
            assert set(item) == keys, f"{kind} carries {sorted(item)}, not {sorted(keys)}"
    for kind, wanted in MATCHUP_READS.items():
        read = set(report["reads"].get(kind, []))
        missing = read - set(shapes[kind])
        assert not missing, f"matchup.js reads {sorted(missing)} from {kind}; payload has none"
        assert wanted <= read, f"matchup.js no longer reads {sorted(wanted - read)} from {kind}"
    # The data drove real behaviour: the notes name teams and divisions, and the print
    # bundle lists the recipes, then the components they print.
    assert any("AFC East" in note for note in report["notes"])
    (bundle,) = report["bundles"]
    dishes = {d["url"]: d for d in payload["dishes"]}
    recipes = [url for url in bundle if url in dishes]
    components: list[str] = []
    for url in recipes:
        components += [p for p in dishes[url]["print_pages"] if p not in components]
    assert components, "the chosen spread prints no component page"
    assert bundle == recipes + components
