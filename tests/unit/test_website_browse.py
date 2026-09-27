"""Browse recipes filters: styles/website-browse.js through Node.

The filter, count and address logic live in JavaScript, so they are tested with Node and
a tiny fake DOM (no jsdom). The tests are skipped when Node is not installed.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

import pytest

BROWSE = Path(__file__).resolve().parents[2] / "styles" / "website-browse.js"
NODE = shutil.which("node")
pytestmark = pytest.mark.skipif(NODE is None, reason="Node.js is not installed")

FIXTURES = """
const facets = [
  {id: "course", options: ["appetizers", "sides", "desserts"]},
  {id: "main-ingredient", options: ["poultry", "beef"]},
  {id: "team", options: ["bills", "dolphins"]},
];
const recipes = [
  {id: "test-a", facets: {course: ["appetizers"], "main-ingredient": ["poultry"], team: ["bills"]}},
  {id: "test-b", facets: {course: ["sides"], "main-ingredient": ["beef"], team: ["bills"]}},
  {id: "test-c", facets: {course: ["appetizers"], "main-ingredient": ["beef"], team: ["dolphins"]}},
  {id: "test-d", facets: {course: ["desserts"], "main-ingredient": [], team: ["dolphins"]}},
];
"""

# Elements with just what init touches: attributes, classes, hidden, listeners and
# querySelector(All) over a fixed map of selectors.
FAKE_DOM = """
function el(attrs, parts) {
  const a = Object.assign({}, attrs);
  const classes = new Set();
  const listeners = {};
  const node = {
    textContent: "",
    hidden: true,
    checked: false,
    disabled: false,
    value: a.value || "",
    parentNode: null,
    getAttribute: (k) => (k in a ? a[k] : null),
    setAttribute: (k, v) => { a[k] = String(v); },
    classList: { toggle: (c, on) => (on ? classes.add(c) : classes.delete(c)),
                 add: (c) => classes.add(c),
                 remove: (c) => classes.delete(c),
                 contains: (c) => classes.has(c) },
    addEventListener: (type, fn) => { (listeners[type] = listeners[type] || []).push(fn); },
    fire: (type) => (listeners[type] || []).forEach((fn) => fn({preventDefault() {}})),
    querySelectorAll: (sel) => (parts && parts[sel]) || [],
    querySelector: (sel) => ((parts && parts[sel]) || [])[0] || null,
  };
  return node;
}
function option(value) {
  const count = el({});
  const input = el({value});
  const label = el({}, {".finder-count": [count]});
  input.parentNode = label;
  return {input, label, count};
}
function page(search) {
  const opts = {};
  const fieldsets = facets.map((f) => {
    const list = f.options.map((o) => (opts[f.id + ":" + o] = option(o)));
    return el({"data-facet": f.id}, {"input[type=checkbox]": list.map((o) => o.input)});
  });
  const form = el({}, {"fieldset[data-facet]": fieldsets});
  const cards = recipes.map((r) => {
    const card = el({"data-id": r.id, "data-facets": JSON.stringify(r.facets)});
    card.hidden = false;
    return card;
  });
  const status = el({}), empty = el({}), clear = el({});
  const finder = el({}, {".finder-filters": [form], ".finder-card": cards,
    ".finder-status": [status], ".finder-empty": [empty], ".finder-clear": [clear]});
  const doc = el({}, {".finder": [finder]});
  const replaced = [];
  const winListeners = {};
  const win = {
    location: {pathname: "/browse.html", search: search || "", hash: ""},
    history: {replaceState: (s, t, url) => replaced.push(url)},
    addEventListener: (type, fn) => { winListeners[type] = fn; },
    popstate: () => winListeners.popstate(),
  };
  const shown = () => cards.filter((c) => !c.hidden).map((c) => c.getAttribute("data-id"));
  const counts = (facet) => facets.find((f) => f.id === facet).options
    .map((o) => opts[facet + ":" + o].count.textContent);
  const dimmed = () =>
    Object.keys(opts).filter((k) => opts[k].label.classList.contains("is-empty"));
  return {doc, win, form, opts, status, empty, clear, replaced, shown, counts, dimmed};
}
"""


def node(body: str) -> Any:
    """Run ``body`` (a function body returning a value) and decode its result."""
    assert NODE is not None
    program = (
        f"const b = require({json.dumps(str(BROWSE))});\n{FIXTURES}\n{FAKE_DOM}\n"
        f"process.stdout.write(JSON.stringify((() => {{ {body} }})()));"
    )
    result = subprocess.run(
        [NODE, "-e", program], capture_output=True, text=True, check=True, timeout=30
    )
    return json.loads(result.stdout)


def test_requiring_the_script_does_not_touch_the_dom() -> None:
    assert node("return Object.keys(b).sort();") == sorted(
        [
            "countOptions",
            "filterRecipes",
            "formState",
            "init",
            "matches",
            "parseState",
            "readCards",
            "readFacets",
            "serializeState",
            "setForm",
            "showCounts",
        ]
    )


def test_parse_state_keeps_known_values_in_facet_order() -> None:
    assert node(
        'return b.parseState("?team=dolphins,nobody&course=sides,appetizers,sides'
        '&unknown=x&main-ingredient=", facets);'
    ) == {"course": ["appetizers", "sides"], "team": ["dolphins"]}
    assert node('return [b.parseState("", facets), b.parseState("?", facets)];') == [{}, {}]


def test_serialize_state_round_trips() -> None:
    result = node(
        """
        const state = {team: ["bills"], course: ["sides", "appetizers"]};
        const text = b.serializeState(state, facets);
        return [text, b.parseState(text, facets), b.serializeState({}, facets),
                b.serializeState({course: []}, facets)];
        """
    )
    assert result == [
        "?course=appetizers,sides&team=bills",
        {"course": ["appetizers", "sides"], "team": ["bills"]},
        "",
        "",
    ]


def test_matches_is_or_within_a_facet_and_and_across_facets() -> None:
    result = node(
        """
        const ids = (state) => b.filterRecipes(recipes, state).map((r) => r.id);
        return [
          ids({}),
          ids({course: ["appetizers", "sides"]}),
          ids({course: ["appetizers"], "main-ingredient": ["beef"]}),
          ids({"main-ingredient": ["poultry"], team: ["dolphins"]}),
          b.matches(recipes[3], {"main-ingredient": ["beef"]}),
        ];
        """
    )
    assert result == [
        ["test-a", "test-b", "test-c", "test-d"],
        ["test-a", "test-b", "test-c"],
        ["test-c"],
        [],
        False,
    ]


def test_counts_ignore_the_facets_own_selection() -> None:
    result = node('return b.countOptions(recipes, facets, {course: ["appetizers"]});')
    assert result == {
        # Other courses still show what choosing them would add.
        "course": {"appetizers": 2, "sides": 1, "desserts": 1},
        "main-ingredient": {"poultry": 1, "beef": 1},
        "team": {"bills": 1, "dolphins": 1},
    }


def test_init_applies_the_address_and_updates_on_change() -> None:
    result = node(
        """
        const p = page("?course=appetizers&team=dolphins");
        b.init(p.doc, p.win);
        const first = {
          visible: !p.form.hidden, shown: p.shown(), status: p.status.textContent,
          empty: p.empty.hidden, course: p.counts("course"), dimmed: p.dimmed(),
          checked: p.opts["course:appetizers"].input.checked, clear: p.clear.disabled,
        };
        p.opts["team:dolphins"].input.checked = false;
        p.opts["main-ingredient:poultry"].input.checked = true;
        p.form.fire("change");
        const second = {shown: p.shown(), url: p.replaced.slice(-1)[0]};
        p.opts["course:appetizers"].input.checked = false;
        p.opts["course:desserts"].input.checked = true;
        p.form.fire("change");
        const none = {shown: p.shown(), empty: p.empty.hidden, status: p.status.textContent};
        p.clear.fire("click");
        const cleared = {shown: p.shown(), url: p.replaced.slice(-1)[0],
          checked: p.opts["course:desserts"].input.checked, clear: p.clear.disabled};
        p.win.location.search = "?course=sides";
        p.win.popstate();
        return [first, second, none, cleared, p.shown()];
        """
    )
    first, second, none, cleared, popped = result
    assert first == {
        "visible": True,
        "shown": ["test-c"],
        "status": "Showing 1 of 4 recipes",
        "empty": True,
        "course": ["(1)", "(0)", "(1)"],
        "dimmed": ["course:sides", "main-ingredient:poultry"],
        "checked": True,
        "clear": False,
    }
    assert second == {
        "shown": ["test-a"],
        "url": "/browse.html?course=appetizers&main-ingredient=poultry",
    }
    assert none == {"shown": [], "empty": False, "status": "Showing 0 of 4 recipes"}
    assert cleared == {
        "shown": ["test-a", "test-b", "test-c", "test-d"],
        "url": "/browse.html",
        "checked": False,
        "clear": True,
    }
    assert popped == ["test-b"]


def test_read_cards_takes_a_selector() -> None:
    result = node(
        """
        const dish = el({"data-id": "test-a", "data-facets": '{"course": ["appetizers"]}'});
        const bad = el({"data-id": "test-b", "data-facets": "{oops"});
        const box = el({}, {".menu-dish": [dish, bad], ".finder-card": []});
        return [b.readCards(box).length,
                b.readCards(box, ".menu-dish").map((c) => [c.id, c.facets])];
        """
    )
    assert result == [0, [["test-a", {"course": ["appetizers"]}], ["test-b", {}]]]


def test_form_helpers_read_set_and_badge_the_boxes() -> None:
    result = node(
        """
        const p = page("");
        const fs = b.readFacets(p.form);
        b.setForm(fs, {course: ["sides"], team: ["dolphins", "nobody"]});
        const state = b.formState(fs);
        b.showCounts(fs, b.countOptions(recipes, facets, state));
        return [state, p.counts("course"), p.counts("team"), p.dimmed()];
        """
    )
    assert result == [
        {"course": ["sides"], "team": ["dolphins"]},
        ["(1)", "(0)", "(1)"],
        ["(1)", "(0)"],
        # Ticked boxes stay bright even when they would give nothing.
        ["main-ingredient:poultry", "main-ingredient:beef"],
    ]


def test_init_without_a_finder_does_nothing() -> None:
    assert node("return b.init(el({}, {}), {});") is None
