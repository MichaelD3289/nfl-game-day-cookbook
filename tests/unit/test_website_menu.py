"""Build your own menu: styles/website-menu.js through Node.

The selection, address, storage and summary logic live in JavaScript, so they are tested
with Node and a tiny fake DOM (no jsdom). The tests are skipped when Node is not
installed. Dish ids follow the synthetic sample book (test- prefix).
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

import pytest

STYLES = Path(__file__).resolve().parents[2] / "styles"
MENU = STYLES / "website-menu.js"
SCALE = STYLES / "website-scale.js"
BROWSE = STYLES / "website-browse.js"
NODE = shutil.which("node")
pytestmark = pytest.mark.skipif(NODE is None, reason="Node.js is not installed")

KNOWN = ["test-buffalo-sliders", "test-citrus-wings", "test-lemon-bars"]

DISHES = """
const dishes = [
  {id: "test-buffalo-sliders", course: "appetizers", url: "recipe-test-buffalo-sliders.html",
   title: "Buffalo Sliders", team: "Buffalo Bills",
   printPages: ["component-test-blue-cheese-dip.html"]},
  {id: "test-citrus-wings", course: "meals", url: "recipe-test-citrus-wings.html",
   title: "Citrus Wings", team: "Miami Dolphins",
   printPages: ["component-test-wing-sauce.html", "component-test-blue-cheese-dip.html"]},
  {id: "test-lemon-bars", course: "desserts", url: "recipe-test-lemon-bars.html",
   title: "Lemon Bars", team: "", printPages: []},
];
const courses = [
  {id: "appetizers", label: "Appetizers"},
  {id: "meals", label: "Meals"},
  {id: "desserts", label: "Desserts"},
];
"""

# A minimal element tree with the selectors menu.js and browse.js use: tag, .class,
# [attr] and [attr=value] compounds, joined by spaces for descendants.
FAKE_DOM = r"""
function el(tag, attrs, kids, text) {
  const a = Object.assign({}, attrs || {});
  const node = {
    tagName: tag.toUpperCase(),
    hidden: "hidden" in a,
    disabled: false,
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
    click: () => (node.listeners.click || []).forEach((fn) => fn({ preventDefault() {} })),
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
function dish(id, course, title, team, pages) {
  const attrs = {class: "menu-dish", "data-id": id, "data-course": course,
                 "data-facets": "{}", "data-url": "recipe-" + id + ".html"};
  if (pages) attrs["data-print-pages"] = pages;
  return el("li", attrs, [
    el("a", {class: "menu-dish-name"}, [], title),
    el("span", {class: "menu-dish-team"}, [], team),
    el("button", {class: "menu-add", hidden: ""}, [], "Add"),
  ]);
}
function page() {
  const factors = ["1/2", "1", "3/2", "2"].map((f) =>
    el("button", {type: "button", "data-factor": f}, [], f));
  const aside = el("aside", {class: "menu-summary", hidden: ""}, [
    el("p", {class: "menu-count"}),
    el("p", {class: "menu-summary-scale", hidden: ""}),
    el("ol", {class: "menu-picked"}),
    el("p", {class: "menu-empty-note"}),
    el("div", {class: "menu-scale"}, factors),
    el("div", {class: "menu-actions", hidden: ""}, [
      el("button", {class: "print-button"}),
      el("label", {class: "print-with", hidden: ""}, [el("input", {name: "print-with"})]),
      el("span", {class: "shop-actions", hidden: ""}, [
        el("button", {"data-shop": "copy"}), el("span", {class: "shop-status"})]),
    ]),
    el("button", {class: "menu-clear"}),
  ]);
  const builder = el("div", {class: "menu-builder"}, [
    el("form", {class: "finder-filters", hidden: ""}),
    el("div", {class: "menu-dishes"}, [
      el("p", {class: "finder-status"}),
      el("section", {class: "menu-course", "data-course": "appetizers"}, [
        el("h2", {class: "menu-course-title"}, [], "Appetizers"),
        el("ul", {}, [dish("test-buffalo-sliders", "appetizers", "Buffalo Sliders",
                           "Buffalo Bills", "component-test-blue-cheese-dip.html")]),
      ]),
      el("section", {class: "menu-course", "data-course": "meals"}, [
        el("h2", {class: "menu-course-title"}, [], "Meals"),
        el("ul", {}, [dish("test-citrus-wings", "meals", "Citrus Wings", "Miami Dolphins")]),
      ]),
      el("p", {class: "finder-empty", hidden: ""}),
    ]),
    aside,
  ]);
  const suggest = el("div", {class: "suggest", "data-kind": "menu", "data-fields": "{}"}, [
    el("a", {class: "suggest-github"}),
  ]);
  suggest.querySelector(".suggest-github").href =
    "https://github.com/o/r/issues/new?template=quick-menu.yml";
  const doc = el("body", {}, [builder, suggest]);
  doc.createElement = (tag) => el(tag);
  return doc;
}
function memoryStorage(initial) {
  const data = Object.assign({}, initial || {});
  return { data, getItem: (k) => (k in data ? data[k] : null),
           setItem: (k, v) => { data[k] = String(v); } };
}
function fakeWindow(search, storage, protocol) {
  const replaced = [];
  return {
    replaced,
    localStorage: storage,
    location: { protocol: protocol || "https:", pathname: "/menu-builder.html",
                search: search || "", hash: "",
                href: "https://example.com/menu-builder.html" + (search || "") },
    history: { replaceState: (s, t, url) => replaced.push(url) },
  };
}
"""


def node(body: str) -> Any:
    """Run ``body`` (an async function body returning a value) and decode its result."""
    assert NODE is not None
    program = (
        f"global.NflScale = require({json.dumps(str(SCALE))});\n"
        f"global.NflBrowse = require({json.dumps(str(BROWSE))});\n"
        f"const m = require({json.dumps(str(MENU))});\n"
        f"const known = {json.dumps(KNOWN)};\n{DISHES}\n{FAKE_DOM}\n"
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
            "addDish",
            "countLabel",
            "groupByCourse",
            "init",
            "initialSelection",
            "loadStored",
            "menuPages",
            "parseSelection",
            "readCourses",
            "readDishes",
            "removeDish",
            "saveStored",
            "serializeSelection",
            "storageOf",
            "suggestionText",
        ]
    )


def test_parse_selection_keeps_known_dishes_in_menu_order() -> None:
    assert node(
        "return ["
        'm.parseSelection("?r=test-lemon-bars,nope,test-buffalo-sliders,test-lemon-bars'
        '&scale=6/4", known),'
        ' m.parseSelection("?r=&scale=1", known),'
        ' m.parseSelection("?scale=0", known),'
        ' m.parseSelection("", known)];'
    ) == [
        {"r": ["test-buffalo-sliders", "test-lemon-bars"], "scale": "3/2", "listed": True},
        {"r": [], "scale": None, "listed": True},
        {"r": [], "scale": None, "listed": False},
        {"r": [], "scale": None, "listed": False},
    ]


def test_serialize_selection_round_trips() -> None:
    result = node(
        """
        const sel = {r: ["test-lemon-bars", "test-buffalo-sliders", "gone"], scale: "4/2"};
        const text = m.serializeSelection(sel, known);
        const back = m.parseSelection(text, known);
        return [text, back, m.serializeSelection({r: [], scale: "1"}, known),
                m.serializeSelection({r: [], scale: "3/2"}, known)];
        """
    )
    assert result == [
        "?r=test-buffalo-sliders,test-lemon-bars&scale=2",
        {"r": ["test-buffalo-sliders", "test-lemon-bars"], "scale": "2", "listed": True},
        "",
        "?scale=3/2",
    ]


def test_the_address_wins_over_what_was_stored() -> None:
    result = node(
        """
        const stored = {r: ["test-citrus-wings", "gone"], scale: "3"};
        return [m.initialSelection("?r=test-lemon-bars", stored, known),
                m.initialSelection("?r=", stored, known),
                m.initialSelection("", stored, known),
                m.initialSelection("?scale=2", null, known),
                m.initialSelection("", {r: "junk", scale: "x"}, known)];
        """
    )
    assert result == [
        {"r": ["test-lemon-bars"], "scale": None},
        {"r": [], "scale": None},
        {"r": ["test-citrus-wings"], "scale": "3"},
        {"r": [], "scale": "2"},
        {"r": [], "scale": None},
    ]


def test_storage_survives_blocked_or_broken_storage() -> None:
    result = node(
        """
        const good = memoryStorage();
        const saved = m.saveStored(good, {r: ["test-lemon-bars"], scale: null});
        const loaded = m.loadStored(good);
        const throwing = { getItem() { throw new Error("blocked"); },
                           setItem() { throw new Error("full"); } };
        const blockedWin = {};
        Object.defineProperty(blockedWin, "localStorage", { get() { throw new Error("no"); } });
        return [saved, good.data, loaded, m.saveStored(throwing, {r: []}),
                m.loadStored(throwing), m.loadStored(memoryStorage({"nfl-menu-builder": "{"})),
                m.storageOf(blockedWin), m.saveStored(null, {r: []}), m.loadStored(null)];
        """
    )
    assert result == [
        True,
        {"nfl-menu-builder": '{"r":["test-lemon-bars"],"scale":"1"}'},
        {"r": ["test-lemon-bars"], "scale": "1"},
        False,
        None,
        None,
        None,
        False,
        None,
    ]


def test_add_and_remove_keep_menu_order_without_repeats() -> None:
    assert node(
        "let ids = m.addDish([], 'test-lemon-bars', known);"
        " ids = m.addDish(ids, 'test-buffalo-sliders', known);"
        " ids = m.addDish(ids, 'test-lemon-bars', known);"
        " const added = ids.slice();"
        " ids = m.addDish(ids, 'unknown', known);"
        " return [added, ids, m.removeDish(ids, 'test-lemon-bars'), m.removeDish(ids, 'x')];"
    ) == [
        ["test-buffalo-sliders", "test-lemon-bars"],
        ["test-buffalo-sliders", "test-lemon-bars"],
        ["test-buffalo-sliders"],
        ["test-buffalo-sliders", "test-lemon-bars"],
    ]


def test_group_by_course_follows_course_order_and_skips_empty_courses() -> None:
    assert node(
        "return m.groupByCourse(['test-lemon-bars', 'test-buffalo-sliders'], dishes, courses)"
        ".map((g) => [g.id, g.label, g.dishes.map((d) => d.id)]);"
    ) == [
        ["appetizers", "Appetizers", ["test-buffalo-sliders"]],
        ["desserts", "Desserts", ["test-lemon-bars"]],
    ]


def test_menu_pages_list_recipes_then_their_components_once() -> None:
    ids = "['test-citrus-wings', 'test-buffalo-sliders', 'test-lemon-bars']"
    assert node(
        f"return [m.menuPages({ids}, dishes, true), m.menuPages({ids}, dishes, false),"
        " m.menuPages([], dishes, true)];"
    ) == [
        [
            "recipe-test-buffalo-sliders.html",
            "recipe-test-citrus-wings.html",
            "recipe-test-lemon-bars.html",
            "component-test-blue-cheese-dip.html",
            "component-test-wing-sauce.html",
        ],
        [
            "recipe-test-buffalo-sliders.html",
            "recipe-test-citrus-wings.html",
            "recipe-test-lemon-bars.html",
        ],
        [],
    ]


def test_count_label() -> None:
    assert node("return [0, 1, 2, 12].map(m.countLabel);") == [
        "No dishes yet",
        "1 dish",
        "2 dishes",
        "12 dishes",
    ]


def test_suggestion_text_lists_courses_then_the_address() -> None:
    result = node(
        """
        const groups = m.groupByCourse(known, dishes, courses);
        return [m.suggestionText(groups, "https://example.com/menu-builder.html?r=a"),
                m.suggestionText([], "https://example.com/")];
        """
    )
    assert result == [
        "Appetizers: Buffalo Sliders (Buffalo Bills)\n"
        "Meals: Citrus Wings (Miami Dolphins)\n"
        "Desserts: Lemon Bars\n"
        "https://example.com/menu-builder.html?r=a",
        "",
    ]


def test_init_restores_the_menu_and_keeps_address_and_storage_in_step() -> None:
    result = node(
        """
        const doc = page();
        const storage = memoryStorage();
        const win = fakeWindow("?r=test-citrus-wings&scale=2", storage);
        const api = m.init(doc, win);
        const q = (s) => doc.querySelector(s);
        const pressed = () => doc.querySelectorAll(".menu-add")
          .map((b) => b.getAttribute("aria-pressed") + ":" + b.textContent);
        const first = {
          selection: api.selection(), pressed: pressed(),
          count: q(".menu-count").textContent, scale: q(".menu-summary-scale").textContent,
          picked: q(".menu-picked").textContent, shown: [q(".menu-summary").hidden,
            q(".menu-actions").hidden, q(".shop-actions").hidden, q(".menu-add").hidden],
          factor: doc.querySelectorAll("button[data-factor]")
            .map((b) => b.getAttribute("aria-pressed")),
          status: q(".finder-status").textContent,
          printWith: q(".print-with").hidden,
        };
        q(".menu-add").click();
        doc.querySelector("button[data-factor]").click();
        const second = {
          selection: api.selection(), pressed: pressed(),
          count: q(".menu-count").textContent, printWith: q(".print-with").hidden,
          address: win.replaced[win.replaced.length - 1], stored: Object.assign({}, storage.data),
          idea: JSON.parse(q(".suggest").getAttribute("data-fields")).idea,
          github: new URL(q(".suggest-github").href).searchParams.get("idea"),
        };
        q(".menu-remove").click();
        q(".menu-clear").click();
        const third = {
          selection: api.selection(), count: q(".menu-count").textContent,
          address: win.replaced[win.replaced.length - 1],
          print: q(".print-button").disabled, clear: q(".menu-clear").disabled,
          github: new URL(q(".suggest-github").href).searchParams.has("idea"),
        };
        return {first, second, third};
        """
    )
    assert result["first"] == {
        "selection": {"r": ["test-citrus-wings"], "scale": "2"},
        "pressed": ["false:Add", "true:Added"],
        "count": "1 dish",
        "scale": "Scaled 2×",
        "picked": "MealsCitrus Wings Miami DolphinsRemove",
        "shown": [False, False, False, False],
        "factor": ["false", "false", "false", "true"],
        "status": "Showing 2 of 2 recipes",
        "printWith": True,
    }
    assert result["second"] == {
        "selection": {"r": ["test-buffalo-sliders", "test-citrus-wings"], "scale": "1/2"},
        "pressed": ["true:Added", "true:Added"],
        "count": "2 dishes",
        "printWith": False,
        "address": "/menu-builder.html?r=test-buffalo-sliders,test-citrus-wings&scale=1/2",
        "stored": {
            "nfl-menu-builder": '{"r":["test-buffalo-sliders","test-citrus-wings"],"scale":"1/2"}'
        },
        "idea": "Appetizers: Buffalo Sliders (Buffalo Bills)\n"
        "Meals: Citrus Wings (Miami Dolphins)\n"
        "https://example.com/menu-builder.html?r=test-buffalo-sliders,test-citrus-wings"
        "&scale=1/2",
        "github": "Appetizers: Buffalo Sliders (Buffalo Bills)\n"
        "Meals: Citrus Wings (Miami Dolphins)\n"
        "https://example.com/menu-builder.html?r=test-buffalo-sliders,test-citrus-wings"
        "&scale=1/2",
    }
    assert result["third"] == {
        "selection": {"r": [], "scale": "1/2"},
        "count": "No dishes yet",
        "address": "/menu-builder.html?scale=1/2",
        "print": True,
        "clear": True,
        "github": False,
    }


def test_init_uses_storage_without_an_address_and_hides_actions_off_the_web() -> None:
    result = node(
        """
        const doc = page();
        const storage = memoryStorage({"nfl-menu-builder": '{"r":["test-buffalo-sliders"]}'});
        const win = fakeWindow("", storage, "file:");
        const api = m.init(doc, win);
        return [api.selection(), doc.querySelector(".menu-actions").hidden,
                doc.querySelector(".menu-summary").hidden,
                m.init(el("body", {}, []), win)];
        """
    )
    assert result == [{"r": ["test-buffalo-sliders"], "scale": None}, True, False, None]
