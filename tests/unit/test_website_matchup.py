"""Matchup menu: styles/website-matchup.js through Node.

The pairing, fallback, swap and address logic live in JavaScript, so they are tested
with Node and a tiny fake DOM (no jsdom), like the menu builder. The tests are skipped
when Node is not installed. Team slugs and division keys are the league's; every dish id
is synthetic (test- prefix).
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

import pytest

STYLES = Path(__file__).resolve().parents[2] / "styles"
MATCHUP = STYLES / "website-matchup.js"
MENU = STYLES / "website-menu.js"
NODE = shutil.which("node")
pytestmark = pytest.mark.skipif(NODE is None, reason="Node.js is not installed")


def _dish(
    ident: str, team: str, division: str, course: str, pages: list[str] | None = None
) -> dict[str, Any]:
    return {
        "id": ident,
        "title": ident.removeprefix("test-").replace("-", " ").title(),
        "url": f"recipe-{ident}.html",
        "course": course,
        "team": team,
        "division": division,
        "printPages": pages or [],
    }


DATA: dict[str, Any] = {
    "courses": [
        {"id": "appetizers", "label": "Appetizers", "singular": "Appetizer"},
        {"id": "sides", "label": "Sides", "singular": "Side"},
        {"id": "meals", "label": "Meals", "singular": "Meal"},
        {"id": "desserts", "label": "Desserts", "singular": "Dessert"},
    ],
    "divisions": [
        {"key": "afc-east", "name": "AFC East"},
        {"key": "afc-west", "name": "AFC West"},
    ],
    "teams": [
        {"slug": "bills", "name": "Buffalo Bills", "short": "Bills", "division": "afc-east"},
        {
            "slug": "dolphins",
            "name": "Miami Dolphins",
            "short": "Dolphins",
            "division": "afc-east",
        },
        {
            "slug": "broncos",
            "name": "Denver Broncos",
            "short": "Broncos",
            "division": "afc-west",
        },
        {
            "slug": "chiefs",
            "name": "Kansas City Chiefs",
            "short": "Chiefs",
            "division": "afc-west",
        },
        {
            "slug": "raiders",
            "name": "Las Vegas Raiders",
            "short": "Raiders",
            "division": "afc-west",
        },
        {
            "slug": "chargers",
            "name": "Los Angeles Chargers",
            "short": "Chargers",
            "division": "afc-west",
        },
    ],
    "dishes": [
        _dish("test-burnt-end-bites", "chiefs", "afc-west", "appetizers"),
        _dish("test-bbq-beans", "chiefs", "afc-west", "sides"),
        _dish(
            "test-brisket",
            "chiefs",
            "afc-west",
            "meals",
            ["component-test-rub.html", "component-test-bbq-sauce.html"],
        ),
        _dish("test-kc-ribs", "chiefs", "afc-west", "meals", ["component-test-rub.html"]),
        _dish("test-raider-nachos", "raiders", "afc-west", "appetizers"),
        _dish("test-vegas-shrimp", "raiders", "afc-west", "meals"),
        _dish("test-denver-green-chile", "broncos", "afc-west", "sides"),
        _dish("test-rocky-mountain-pie", "broncos", "afc-west", "desserts"),
        _dish("test-buffalo-sliders", "bills", "afc-east", "appetizers"),
    ],
}

# A minimal element tree with the selectors matchup.js uses: tag, .class, [attr] and
# [attr=value] compounds, joined by spaces for descendants. Form controls keep `value`
# and `checked` as plain properties, and `fire(type)` runs an element's listeners.
FAKE_DOM = r"""
function el(tag, attrs, kids, text) {
  const a = Object.assign({}, attrs || {});
  const node = {
    tagName: tag.toUpperCase(),
    hidden: "hidden" in a,
    disabled: false,
    value: "",
    checked: false,
    children: [],
    parentNode: null,
    listeners: {},
    _text: text || "",
    getAttribute: (k) => (k in a ? a[k] : null),
    hasAttribute: (k) => k in a,
    setAttribute: (k, v) => { a[k] = String(v); },
    addEventListener: (type, fn) => {
      (node.listeners[type] = node.listeners[type] || []).push(fn);
    },
    fire: (type) => (node.listeners[type] || []).forEach((fn) => fn({ preventDefault() {} })),
    click: () => node.fire("click"),
    appendChild: (kid) => { kid.parentNode = node; node.children.push(kid); return kid; },
    removeChild: (kid) => { node.children.splice(node.children.indexOf(kid), 1); return kid; },
    get firstChild() { return node.children[0] || null; },
    get className() { return a.class || ""; },
    set className(v) { a.class = v; },
    get textContent() { return node._text + node.children.map((k) => k.textContent).join(""); },
    set textContent(v) { node._text = String(v); node.children = []; },
    classList: {
      toggle: (c, on) => { const s = new Set((a.class || "").split(" ").filter(Boolean));
                           if (on) s.add(c); else s.delete(c); a.class = [...s].join(" "); },
      contains: (c) => (a.class || "").split(" ").includes(c),
    },
  };
  (kids || []).forEach((kid) => node.appendChild(kid));
  node.querySelectorAll = (sel) => all(node).filter((n) => matches(n, sel, node));
  node.querySelector = (sel) => node.querySelectorAll(sel)[0] || null;
  return node;
}
function all(node) {
  return node.children.flatMap((kid) => [kid].concat(all(kid)));
}
function compound(n, part) {
  const m = part.match(/^([a-z]*)((?:\.[\w-]+)*)((?:\[[^\]]+\])*)$/);
  if (!m) throw new Error("fake DOM cannot match " + part);
  if (m[1] && n.tagName !== m[1].toUpperCase()) return false;
  const classes = m[2].split(".").filter(Boolean);
  if (!classes.every((c) => n.classList.contains(c))) return false;
  return (m[3].match(/\[[^\]]+\]/g) || []).every((attr) => {
    const [k, v] = attr.slice(1, -1).split("=");
    return v === undefined ? n.hasAttribute(k) : n.getAttribute(k) === v;
  });
}
function matches(n, sel, scope) {
  const parts = sel.trim().split(/\s+/);
  if (!compound(n, parts.pop())) return false;
  let up = n.parentNode;
  while (parts.length && up && up !== scope.parentNode) {
    if (compound(up, parts[parts.length - 1])) parts.pop();
    up = up.parentNode;
  }
  return !parts.length;
}
function page(json) {
  const spread = el("section", {class: "matchup-spread", hidden: ""}, [
    el("h2", {class: "matchup-title"}),
    el("ol", {class: "matchup-courses"}),
  ]);
  const matchup = el("div", {class: "matchup"}, [
    el("form", {class: "matchup-pickers", hidden: ""}, [
      el("label", {}, [el("select", {name: "away"})]),
      el("label", {}, [el("select", {name: "home"})]),
    ]),
    el("p", {class: "matchup-status"}),
    spread,
    el("div", {class: "matchup-actions", hidden: ""}, [
      el("a", {class: "matchup-builder", href: "menu-builder.html"}),
      el("span", {class: "matchup-served", hidden: ""}, [
        el("button", {class: "print-button"}),
        el("label", {class: "print-with", hidden: ""}, [el("input", {name: "print-with"})]),
        el("span", {class: "shop-actions", hidden: ""}, [
          el("button", {"data-shop": "copy"}), el("span", {class: "shop-status"})]),
      ]),
    ]),
  ]);
  const script = el("script", {type: "application/json", class: "matchup-data"}, [],
                    json === undefined ? JSON.stringify(data) : json);
  const main = el("main", {class: "content"}, [
    el("p", {class: "matchup-nojs"}), matchup, script]);
  const doc = el("body", {}, [main]);
  doc.createElement = (tag) => el(tag);
  return doc;
}
function fakeWindow(search, protocol) {
  const replaced = [];
  return {
    replaced,
    location: { protocol: protocol || "https:", pathname: "/matchup.html",
                search: search || "", hash: "",
                href: "https://example.com/matchup.html" + (search || "") },
    history: { replaceState: (s, t, url) => replaced.push(url) },
    addEventListener: () => {},
    print: () => {},
  };
}
function rows(doc) {
  return doc.querySelectorAll(".matchup-course").map((li) => ({
    course: li.getAttribute("data-course"),
    name: li.querySelector(".matchup-course-name").textContent,
    side: li.querySelector(".matchup-side").textContent,
    link: li.querySelector("a") ? li.querySelector("a").getAttribute("href") : null,
    note: li.querySelector(".matchup-note") ? li.querySelector(".matchup-note").textContent : "",
    swap: li.querySelector(".matchup-swap").disabled,
  }));
}
"""


def node(body: str) -> Any:
    """Run ``body`` (an async function body returning a value) and decode its result."""
    assert NODE is not None
    program = (
        f"global.NflMenu = require({json.dumps(str(MENU))});\n"
        f"const m = require({json.dumps(str(MATCHUP))});\n"
        f"const data = {json.dumps(DATA)};\n{FAKE_DOM}\n"
        "const ids = (spread) => spread.map((e) => e.dish && e.dish.id);\n"
        f"(async () => {{ {body} }})().then("
        "(v) => process.stdout.write(JSON.stringify(v)),"
        "(e) => { console.error(e); process.exit(1); });"
    )
    result = subprocess.run(
        [NODE, "-e", program], capture_output=True, text=True, check=False, timeout=30
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def test_requiring_the_script_does_not_touch_the_dom() -> None:
    assert node("return Object.keys(m).sort();") == sorted(
        [
            "readData",
            "parseMatchup",
            "serializeMatchup",
            "pool",
            "suggest",
            "nextDish",
            "spreadIds",
            "menuBuilderHref",
            "sourceNote",
            "matchupTitle",
            "init",
        ]
    )


def test_parse_matchup_keeps_known_teams_and_dishes() -> None:
    assert node(
        "return [m.parseMatchup('?home=chiefs&away=raiders&pick=test-kc-ribs,nope,"
        "test-bbq-beans', data), m.parseMatchup('?home=jaguars&away=chiefs', data),"
        " m.parseMatchup('?home=chiefs&away=chiefs', data), m.parseMatchup('', data)];"
    ) == [
        {"home": "chiefs", "away": "raiders", "picks": ["test-kc-ribs", "test-bbq-beans"]},
        {"home": "", "away": "chiefs", "picks": []},
        {"home": "chiefs", "away": "", "picks": []},
        {"home": "", "away": "", "picks": []},
    ]


def test_pool_is_own_dishes_then_division_neighbours() -> None:
    assert node(
        "const ex = ['chiefs', 'raiders'];"
        "const p = (t, c, x) => { const r = m.pool(data, t, c, x);"
        "  return {own: r.own.map((d) => d.id), division: r.division.map((d) => d.id)}; };"
        "return [p('chiefs', 'meals', ex), p('raiders', 'sides', ex),"
        " p('raiders', 'sides', ['raiders', 'bills']), p('bills', 'meals', ['bills'])];"
    ) == [
        {"own": ["test-brisket", "test-kc-ribs"], "division": []},
        {"own": [], "division": ["test-denver-green-chile"]},
        {"own": [], "division": ["test-bbq-beans", "test-denver-green-chile"]},
        {"own": [], "division": []},
    ]


def test_suggest_alternates_home_and_away_and_falls_back_to_the_division() -> None:
    assert node(
        "return m.suggest(data, 'chiefs', 'raiders', []).map((e) =>"
        " [e.course, e.side, e.team, e.source, e.dish && e.dish.id,"
        "  e.pool.map((d) => d.id)]);"
    ) == [
        ["appetizers", "home", "chiefs", "team", "test-burnt-end-bites", ["test-burnt-end-bites"]],
        [
            "sides",
            "away",
            "raiders",
            "division",
            "test-denver-green-chile",
            ["test-denver-green-chile"],
        ],
        ["meals", "home", "chiefs", "team", "test-brisket", ["test-brisket", "test-kc-ribs"]],
        [
            "desserts",
            "away",
            "raiders",
            "division",
            "test-rocky-mountain-pie",
            ["test-rocky-mountain-pie"],
        ],
    ]


def test_suggest_falls_back_to_the_other_side() -> None:
    assert node(
        "return m.suggest(data, 'bills', 'raiders', []).map((e) =>"
        " [e.course, e.side, e.team, e.source, e.dish && e.dish.id]);"
    ) == [
        ["appetizers", "home", "bills", "team", "test-buffalo-sliders"],
        ["sides", "away", "raiders", "division", "test-bbq-beans"],
        ["meals", "home", "bills", "other", "test-vegas-shrimp"],
        ["desserts", "away", "raiders", "division", "test-rocky-mountain-pie"],
    ]


def test_suggest_leaves_an_empty_course_and_spread_ids_skip_it() -> None:
    assert node(
        "const d = Object.assign({}, data, {dishes: data.dishes.filter("
        "  (x) => x.course !== 'desserts')});"
        "const s = m.suggest(d, 'chiefs', 'raiders', []);"
        "return [s[3].source, s[3].dish, s[3].pool, m.spreadIds(s)];"
    ) == [
        "none",
        None,
        [],
        ["test-burnt-end-bites", "test-denver-green-chile", "test-brisket"],
    ]


def test_picks_choose_within_the_pool_only() -> None:
    assert node(
        "return [ids(m.suggest(data, 'chiefs', 'raiders', ['test-kc-ribs'])),"
        " ids(m.suggest(data, 'chiefs', 'raiders', ['test-vegas-shrimp']))];"
    ) == [
        [
            "test-burnt-end-bites",
            "test-denver-green-chile",
            "test-kc-ribs",
            "test-rocky-mountain-pie",
        ],
        [
            "test-burnt-end-bites",
            "test-denver-green-chile",
            "test-brisket",
            "test-rocky-mountain-pie",
        ],
    ]


def test_next_dish_wraps_round_the_pool() -> None:
    assert node(
        "const two = data.dishes.filter((d) => d.team === 'chiefs' && d.course === 'meals');"
        "const id = (d) => d && d.id;"
        "return [id(m.nextDish(two, 'test-brisket')), id(m.nextDish(two, 'test-kc-ribs')),"
        " id(m.nextDish(two.slice(0, 1), 'test-brisket')), id(m.nextDish(two, 'nope')),"
        " m.nextDish([], 'test-brisket')];"
    ) == ["test-kc-ribs", "test-brisket", "test-brisket", "test-brisket", None]


def test_serialize_matchup_leaves_out_default_dishes() -> None:
    assert node(
        "const plain = {home: 'chiefs', away: 'raiders', picks: []};"
        "return [m.serializeMatchup(plain, m.suggest(data, 'chiefs', 'raiders', [])),"
        " m.serializeMatchup(plain, m.suggest(data, 'chiefs', 'raiders', ['test-kc-ribs'])),"
        " m.serializeMatchup({home: 'chiefs', away: '', picks: []}, []),"
        " m.serializeMatchup({home: '', away: '', picks: []}, [])];"
    ) == [
        "?home=chiefs&away=raiders",
        "?home=chiefs&away=raiders&pick=test-kc-ribs",
        "?home=chiefs",
        "",
    ]
    assert (
        node(
            "const s = '?home=chiefs&away=raiders&pick=test-kc-ribs';"
            "const st = m.parseMatchup(s, data);"
            "return m.serializeMatchup(st, m.suggest(data, st.home, st.away, st.picks));"
        )
        == "?home=chiefs&away=raiders&pick=test-kc-ribs"
    )


def test_source_notes_and_title() -> None:
    assert node(
        "const note = (h, a, i, d) => m.sourceNote(m.suggest(d || data, h, a, [])[i], d || data);"
        "const noDesserts = Object.assign({}, data, {dishes: data.dishes.filter("
        "  (x) => x.course !== 'desserts')});"
        "const noRaiderMeals = Object.assign({}, data, {dishes: data.dishes.filter("
        "  (x) => x.id !== 'test-vegas-shrimp')});"
        "return [note('chiefs', 'raiders', 0), note('chiefs', 'raiders', 1),"
        " note('bills', 'raiders', 2), note('bills', 'raiders', 2, noRaiderMeals),"
        " note('chiefs', 'raiders', 3, noDesserts),"
        " m.matchupTitle(data, 'chiefs', 'raiders')];"
    ) == [
        "",
        "From the AFC West: no Raiders side yet",
        "No Bills or AFC East meal yet, so the Raiders cover it",
        "No Bills or AFC East meal yet, so the AFC West covers it",
        "No dessert from either side yet",
        "Las Vegas Raiders at Kansas City Chiefs",
    ]


def test_menu_builder_link_and_print_order() -> None:
    assert node(
        "const s = m.suggest(data, 'chiefs', 'raiders', []);"
        "const spreadIds = m.spreadIds(s);"
        "return [m.menuBuilderHref(spreadIds), m.menuBuilderHref([]),"
        " NflMenu.menuPages(spreadIds, s.filter((e) => e.dish).map((e) => e.dish), true)];"
    ) == [
        "menu-builder.html?r=test-burnt-end-bites,test-denver-green-chile,test-brisket,"
        "test-rocky-mountain-pie",
        "menu-builder.html",
        [
            "recipe-test-burnt-end-bites.html",
            "recipe-test-denver-green-chile.html",
            "recipe-test-brisket.html",
            "recipe-test-rocky-mountain-pie.html",
            "component-test-rub.html",
            "component-test-bbq-sauce.html",
        ],
    ]


def test_read_data_survives_broken_json() -> None:
    assert node(
        "return [m.readData(page('{nope')), m.readData(page()).teams.length,"
        " m.init(page('{nope'), fakeWindow(''))];"
    ) == [None, 6, None]


def test_init_renders_the_spread_and_keeps_the_address_in_step() -> None:
    result = node(
        "const doc = page(); const win = fakeWindow('?home=chiefs&away=raiders');"
        "const ui = m.init(doc, win);"
        "const q = (s) => doc.querySelector(s);"
        "const before = {rows: rows(doc), title: q('.matchup-title').textContent,"
        " nojs: q('.matchup-nojs').hidden, pickers: q('.matchup-pickers').hidden,"
        " home: q('select[name=home]').value, away: q('select[name=away]').value,"
        " spread: q('.matchup-spread').hidden, actions: q('.matchup-actions').hidden,"
        " served: q('.matchup-served').hidden, shop: q('.shop-actions').hidden,"
        " withLabel: q('.print-with').hidden,"
        " builder: q('.matchup-builder').getAttribute('href')};"
        "doc.querySelector('.matchup-swap[data-course=meals]').click();"
        "const swapped = {replaced: win.replaced.slice(),"
        " builder: q('.matchup-builder').getAttribute('href'), state: ui.state()};"
        "q('select[name=away]').value = 'broncos'; q('select[name=away]').fire('change');"
        "return {before, swapped, changed: win.replaced[win.replaced.length - 1],"
        " title: q('.matchup-title').textContent, rows: rows(doc)};"
    )
    before = result["before"]
    assert before["rows"] == [
        {
            "course": "appetizers",
            "name": "Appetizer",
            "side": "Home · Kansas City Chiefs",
            "link": "recipe-test-burnt-end-bites.html",
            "note": "",
            "swap": True,
        },
        {
            "course": "sides",
            "name": "Side",
            "side": "Away · Las Vegas Raiders",
            "link": "recipe-test-denver-green-chile.html",
            "note": "From the AFC West: no Raiders side yet",
            "swap": True,
        },
        {
            "course": "meals",
            "name": "Meal",
            "side": "Home · Kansas City Chiefs",
            "link": "recipe-test-brisket.html",
            "note": "",
            "swap": False,
        },
        {
            "course": "desserts",
            "name": "Dessert",
            "side": "Away · Las Vegas Raiders",
            "link": "recipe-test-rocky-mountain-pie.html",
            "note": "From the AFC West: no Raiders dessert yet",
            "swap": True,
        },
    ]
    assert before["title"] == "Las Vegas Raiders at Kansas City Chiefs"
    assert before["nojs"] is True
    assert before["pickers"] is False
    assert (before["home"], before["away"]) == ("chiefs", "raiders")
    assert before["spread"] is False
    assert before["actions"] is False
    assert before["served"] is False
    assert before["shop"] is False
    assert before["withLabel"] is False
    assert before["builder"] == (
        "menu-builder.html?r=test-burnt-end-bites,test-denver-green-chile,test-brisket,"
        "test-rocky-mountain-pie"
    )

    swapped = result["swapped"]
    assert swapped["replaced"][-1] == "/matchup.html?home=chiefs&away=raiders&pick=test-kc-ribs"
    assert "test-kc-ribs" in swapped["builder"]
    assert swapped["state"] == {"home": "chiefs", "away": "raiders", "picks": ["test-kc-ribs"]}

    assert result["changed"] == "/matchup.html?home=chiefs&away=broncos"
    assert result["title"] == "Denver Broncos at Kansas City Chiefs"
    assert result["rows"][2]["link"] == "recipe-test-brisket.html"


def test_init_keeps_print_and_shop_hidden_off_the_web() -> None:
    assert node(
        "const doc = page(); m.init(doc, fakeWindow('?home=chiefs&away=raiders', 'file:'));"
        "return [doc.querySelector('.matchup-actions').hidden,"
        " doc.querySelector('.matchup-served').hidden];"
    ) == [False, True]


def test_init_prompts_until_two_different_teams_are_picked() -> None:
    assert node(
        "const out = [];"
        "for (const search of ['', '?home=chiefs', '?home=chiefs&away=chiefs']) {"
        "  const doc = page(); m.init(doc, fakeWindow(search));"
        "  out.push([doc.querySelector('.matchup-status').textContent,"
        "            doc.querySelector('.matchup-spread').hidden,"
        "            doc.querySelector('.matchup-actions').hidden]); }"
        "return out;"
    ) == [
        ["Pick a home and an away team", True, True],
        ["Pick a home and an away team", True, True],
        ["Pick two different teams", True, True],
    ]


def test_init_shows_an_empty_course_without_a_link() -> None:
    assert node(
        "const d = Object.assign({}, data, {dishes: data.dishes.filter("
        "  (x) => x.course !== 'desserts')});"
        "const doc = page(JSON.stringify(d));"
        "m.init(doc, fakeWindow('?home=chiefs&away=raiders'));"
        "const last = rows(doc)[3];"
        "return [last.link, last.note, last.swap];"
    ) == [None, "No dessert from either side yet", True]


def test_print_bundles_the_spread_then_its_components() -> None:
    assert node(
        "const calls = [];"
        "global.NflPrint = { printBundle: (urls, opts) => {"
        "  calls.push([urls, opts.scale, opts.target.className]); return Promise.resolve(); },"
        "  prefetch: () => {}, tidy: () => {}, isolate: () => {} };"
        "const doc = page(); m.init(doc, fakeWindow('?home=chiefs&away=raiders'));"
        "doc.querySelector('input[name=print-with]').checked = true;"
        "doc.querySelector('.print-button').click();"
        "await new Promise((r) => setTimeout(r, 0));"
        "return calls;"
    ) == [
        [
            [
                "recipe-test-burnt-end-bites.html",
                "recipe-test-denver-green-chile.html",
                "recipe-test-brisket.html",
                "recipe-test-rocky-mountain-pie.html",
                "component-test-rub.html",
                "component-test-bbq-sauce.html",
            ],
            None,
            "matchup-spread",
        ]
    ]


def test_shopping_list_is_titled_after_the_matchup() -> None:
    assert node(
        "const calls = [];"
        "global.NflShop = { listFor: (urls, opts) => {"
        "  calls.push([urls.length, opts.scale, opts.title, opts.url]);"
        "  return Promise.resolve({}); },"
        "  save: () => Promise.resolve('Copied') };"
        "const doc = page(); m.init(doc, fakeWindow('?home=chiefs&away=raiders'));"
        "doc.querySelector('button[data-shop=copy]').click();"
        "await new Promise((r) => setTimeout(r, 0));"
        "return [calls, doc.querySelector('.shop-status').textContent];"
    ) == [
        [
            [
                4,
                None,
                "Las Vegas Raiders at Kansas City Chiefs game-day spread",
                "https://example.com/matchup.html?home=chiefs&away=raiders",
            ]
        ],
        "Copied",
    ]
