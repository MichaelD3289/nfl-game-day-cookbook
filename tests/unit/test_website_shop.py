"""Shopping lists on the website: styles/website-shop.js through Node.

The list is read from a page's ingredient markup as shown (scaled amounts included), so
it is tested with Node and a tiny fake DOM (no jsdom). Skipped when Node is missing.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

import pytest

STYLES = Path(__file__).resolve().parents[2] / "styles"
SCALE = STYLES / "website-scale.js"
PRINT = STYLES / "website-print.js"
SHOP = STYLES / "website-shop.js"
NODE = shutil.which("node")
pytestmark = pytest.mark.skipif(NODE is None, reason="Node.js is not installed")

# Elements with tag names, computed textContent and a small selector engine: tag, .class
# and [attr] parts, descendant combinators and comma lists. Enough for shop.js.
FAKE_DOM = r"""
function h(tag, attrs, kids) {
  const a = Object.assign({}, attrs || {});
  const classes = new Set(String(a.class || "").split(/\s+/).filter(Boolean));
  delete a.class;
  const node = {
    tagName: tag.toUpperCase(),
    children: [],
    childNodes: [],
    parentNode: null,
    hidden: false,
    getAttribute: (k) => (k in a ? a[k] : null),
    hasAttribute: (k) => k in a,
    setAttribute: (k, v) => { a[k] = String(v); },
    classList: { toggle: (c, on) => (on ? classes.add(c) : classes.delete(c)),
                 add: (c) => classes.add(c),
                 remove: (c) => classes.delete(c),
                 contains: (c) => classes.has(c) },
    get textContent() {
      return node.childNodes.map((k) => (typeof k === "string" ? k : k.textContent)).join("");
    },
    set textContent(v) { node.childNodes = [String(v)]; node.children = []; },
    querySelectorAll: (sel) => select(node, sel),
    querySelector: (sel) => select(node, sel)[0] || null,
  };
  (kids || []).forEach((kid) => {
    node.childNodes.push(kid);
    if (typeof kid !== "string") { node.children.push(kid); kid.parentNode = node; }
  });
  return node;
}
function simple(node, part) {
  const m = part.match(/^([a-z0-9]*)((?:\.[\w-]+)*)((?:\[[\w-]+\])*)$/i);
  if (!m) throw new Error("unsupported selector " + part);
  if (m[1] && node.tagName !== m[1].toUpperCase()) return false;
  const classes = m[2].split(".").filter(Boolean);
  const attrs = (m[3].match(/[\w-]+/g) || []);
  return classes.every((c) => node.classList.contains(c)) &&
    attrs.every((k) => node.hasAttribute(k));
}
function matches(node, parts, top) {
  if (!simple(node, parts[parts.length - 1])) return false;
  let rest = parts.slice(0, -1);
  for (let up = node.parentNode; rest.length && up && up !== top.parentNode; up = up.parentNode) {
    if (simple(up, rest[rest.length - 1])) rest = rest.slice(0, -1);
  }
  return rest.length === 0;
}
function select(root, sel) {
  const lists = sel.split(",").map((s) => s.trim().split(/\s+/));
  const found = [];
  (function walk(node) {
    node.children.forEach((kid) => {
      if (lists.some((parts) => matches(kid, parts, root))) found.push(kid);
      walk(kid);
    });
  })(root);
  return found;
}
// A page shaped like Quarto's output for the test-buffalo-sliders fixture.
function page(title, groups) {
  const kids = [h("h2", {}, ["Ingredients"])];
  groups.forEach(([heading, lines]) => {
    const items = lines.map((line) => h("li", {}, [h("p", {}, line)]));
    const body = heading ? [h("h3", {}, [heading]), h("ul", {}, items)] : [h("ul", {}, items)];
    kids.push(h("section", { class: "level3" }, body));
  });
  const main = h("main", { class: "content" }, [
    h("section", { class: "level1" }, [h("h1", {}, [title])]),
    h("section", { class: "level2 ingredients" }, kids),
    h("section", { class: "level2 instructions" }, [h("ol", {}, [h("li", {}, ["Cook."])])]),
  ]);
  const body = h("body", {}, [main]);
  return { body, querySelector: body.querySelector, querySelectorAll: body.querySelectorAll };
}
const qty = (q, unit, text) =>
  h("span", Object.assign({ class: "qty", "data-q": q }, unit ? { "data-unit": unit } : {}),
    [text]);
const mark = () => h("a", { class: "q-mark", href: "component-test-blue-cheese-dip.html" }, ["Q"]);
function sliders() {
  return page("Test Buffalo Sliders", [
    ["Sliders", [
      [qty("1", "lb", "1 lb"), " ground chicken"],
      [qty("12", null, "12"), " slider buns"],
      ["2 cups oil for the griddle"],
      [qty("1/2", "cup", "1/2 cup"), " blue cheese dip ", mark()],
    ]],
    ["To serve", [["Celery sticks & carrot sticks (100% optional)"]]],
  ]);
}
function dip() {
  return page("Test Blue Cheese Dip", [
    [null, [[qty("1", "cup", "1 cup"), " sour cream"], ["Salt to taste"]]],
  ]);
}
"""


def node(body: str) -> Any:
    """Run ``body`` (an async function body returning a value) and decode its result."""
    assert NODE is not None
    program = (
        f"global.NflScale = require({json.dumps(str(SCALE))});\n"
        f"global.NflPrint = require({json.dumps(str(PRINT))});\n"
        f"const shop = require({json.dumps(str(SHOP))});\n{FAKE_DOM}\n"
        f"(async () => {{ {body} }})().then("
        "(v) => process.stdout.write(JSON.stringify(v)),"
        "(e) => { console.error(e); process.exit(1); });"
    )
    result = subprocess.run(
        [NODE, "-e", program], capture_output=True, text=True, check=True, timeout=30
    )
    return json.loads(result.stdout)


def test_requiring_the_script_does_not_touch_the_dom() -> None:
    assert node("return Object.keys(shop).sort();") == sorted(
        [
            "build",
            "copy",
            "csvField",
            "download",
            "filename",
            "fromDocument",
            "fromHtml",
            "init",
            "lineText",
            "listFor",
            "save",
            "sections",
            "splitLine",
            "toCsv",
            "toText",
        ]
    )


def test_csv_fields_follow_rfc_4180() -> None:
    assert node(
        'return ["2 cups", "salt, to taste", \'12" pizza\', "a\\nb", "a\\rb", ""]'
        ".map(shop.csvField);"
    ) == ["2 cups", '"salt, to taste"', '"12"" pizza"', '"a\nb"', '"a\rb"', ""]


def test_split_line_takes_a_leading_amount_only() -> None:
    assert node(
        'return [shop.splitLine("1 cup sour cream", "1 cup"),'
        ' shop.splitLine("Juice of 1 lime", "1"),'
        ' shop.splitLine("Salt to taste", null)];'
    ) == [
        {"amount": "1 cup", "item": "sour cream", "text": "1 cup sour cream"},
        {"amount": "", "item": "Juice of 1 lime", "text": "Juice of 1 lime"},
        {"amount": "", "item": "Salt to taste", "text": "Salt to taste"},
    ]


def test_line_text_drops_the_quick_mark_and_extra_space() -> None:
    assert (
        node(
            'const li = h("li", {}, [h("p", {}, ["\\n  ", qty("1/2", "cup", "1/2 cup"),'
            ' "  blue cheese dip ", mark(), "\\n"])]);'
            "return shop.lineText(li);"
        )
        == "1/2 cup blue cheese dip"
    )


def test_sections_keep_headings_and_order() -> None:
    assert node("return shop.sections(sliders().body);") == [
        {
            "heading": "Sliders",
            "lines": [
                {"amount": "1 lb", "item": "ground chicken", "text": "1 lb ground chicken"},
                {"amount": "12", "item": "slider buns", "text": "12 slider buns"},
                {
                    "amount": "",
                    "item": "2 cups oil for the griddle",
                    "text": "2 cups oil for the griddle",
                },
                {"amount": "1/2 cup", "item": "blue cheese dip", "text": "1/2 cup blue cheese dip"},
            ],
        },
        {
            "heading": "To serve",
            "lines": [
                {
                    "amount": "",
                    "item": "Celery sticks & carrot sticks (100% optional)",
                    "text": "Celery sticks & carrot sticks (100% optional)",
                }
            ],
        },
    ]


def test_from_document_scales_amounts_but_not_no_scale_lines() -> None:
    result = node(
        'const doc = sliders();\nreturn [shop.fromDocument(doc, "component-test-x.html", "2"),'
        ' shop.fromDocument(dip(), "https://x.org/recipe-test-y.html?scale=2#top", null)];'
    )
    scaled, plain = result
    assert scaled["title"] == "Test Buffalo Sliders"
    assert scaled["kind"] == "component"
    assert scaled["url"] == "component-test-x.html"
    lines = [line["text"] for line in scaled["sections"][0]["lines"]]
    assert lines == [
        "2 pounds ground chicken",
        "24 slider buns",
        "2 cups oil for the griddle",
        "1 cup blue cheese dip",
    ]
    assert plain["kind"] == "recipe"
    assert plain["sections"] == [
        {
            "heading": None,
            "lines": [
                {"amount": "1 cup", "item": "sour cream", "text": "1 cup sour cream"},
                {"amount": "", "item": "Salt to taste", "text": "Salt to taste"},
            ],
        }
    ]


BUILD = """
const recipe = shop.fromDocument(sliders(), "recipe-test-buffalo-sliders.html", null);
const sauce = shop.fromDocument(dip(), "component-test-blue-cheese-dip.html", null);
const model = shop.build(
  [recipe, sauce, { url: "component-test-wing-sauce.html", error: "HTTP 404" }],
  { title: "Test Buffalo Sliders", scale: SCALE,
    url: "https://x.org/recipe-test-buffalo-sliders.html" },
);
"""


def test_text_list_groups_by_recipe_and_component_without_merging() -> None:
    text = node(BUILD.replace("SCALE", '"2"') + "return shop.toText(model);")
    assert text == (
        "Shopping list: Test Buffalo Sliders (scaled 2×)\n"
        "https://x.org/recipe-test-buffalo-sliders.html\n"
        "\n"
        "TEST BUFFALO SLIDERS\n"
        "Sliders\n"
        "- 1 lb ground chicken\n"
        "- 12 slider buns\n"
        "- 2 cups oil for the griddle\n"
        "- 1/2 cup blue cheese dip\n"
        "To serve\n"
        "- Celery sticks & carrot sticks (100% optional)\n"
        "\n"
        "TEST BLUE CHEESE DIP (homemade component)\n"
        "- 1 cup sour cream\n"
        "- Salt to taste\n"
        "\n"
        "COMPONENT-TEST-WING-SAUCE.HTML (homemade component)\n"
        "Couldn't load component-test-wing-sauce.html; see its page.\n"
    )
    unscaled = node(BUILD.replace("SCALE", '"1"') + "return shop.toText(model);")
    assert unscaled.startswith("Shopping list: Test Buffalo Sliders\n")


def test_csv_list_has_bom_header_and_crlf_rows() -> None:
    csv = node(BUILD.replace("SCALE", "null") + "return shop.toCsv(model);")
    assert csv.startswith("﻿For,Section,Amount,Item\r\n")
    assert csv.endswith("\r\n")
    rows = csv[1:].split("\r\n")
    assert rows[1:4] == [
        "Test Buffalo Sliders,Sliders,1 lb,ground chicken",
        "Test Buffalo Sliders,Sliders,12,slider buns",
        "Test Buffalo Sliders,Sliders,,2 cups oil for the griddle",
    ]
    assert "Test Buffalo Sliders,To serve,,Celery sticks & carrot sticks (100% optional)" in rows
    assert "Test Blue Cheese Dip (homemade component),,1 cup,sour cream" in rows
    assert (
        "component-test-wing-sauce.html (homemade component),,,"
        "Couldn't load component-test-wing-sauce.html; see its page."
    ) in rows


def test_list_for_fetches_pages_in_order_and_keeps_failures() -> None:
    model = node(
        """
        const docs = { "<dip>": dip(), "<sliders>": sliders() };
        global.DOMParser = class { parseFromString(html) { return docs[html]; } };
        const fetchText = (url) => {
          if (url === "component-test-bad.html") return Promise.reject(new Error("404"));
          const delay = url === "recipe-test-buffalo-sliders.html" ? 20 : 0;
          const html = url.startsWith("recipe") ? "<sliders>" : "<dip>";
          return new Promise((ok) => setTimeout(() => ok(html), delay));
        };
        const here = { title: "Card", kind: "recipe", url: "here.html", sections: [] };
        return shop.listFor(
          ["recipe-test-buffalo-sliders.html", "component-test-bad.html",
           "component-test-blue-cheese-dip.html"],
          { scale: "2", title: "Test Quick Kickoff", url: "menus.html#k", here, fetchText },
        );
        """
    )
    assert model["title"] == "Test Quick Kickoff"
    assert model["scale"] == "2"
    assert model["url"] == "menus.html#k"
    groups = model["groups"]
    assert [g["title"] for g in groups] == [
        "Card",
        "Test Buffalo Sliders",
        "component-test-bad.html",
        "Test Blue Cheese Dip",
    ]
    assert [g["kind"] for g in groups] == ["recipe", "recipe", "component", "component"]
    assert groups[2]["error"] == "Couldn't load component-test-bad.html; see its page."
    assert groups[3]["sections"][0]["lines"][0]["text"] == "2 cups sour cream"


def test_file_names_come_from_the_page_and_card() -> None:
    assert node(
        'return [shop.filename("https://x.org/b/recipe-test-buffalo-sliders.html?scale=2", "txt"),'
        ' shop.filename("file:///b/menus-fast-day-1.html#menu-test-quick-kickoff", "csv"),'
        ' shop.filename("https://x.org/", "txt")];'
    ) == [
        "shopping-list-recipe-test-buffalo-sliders.txt",
        "shopping-list-menus-fast-day-1-menu-test-quick-kickoff.csv",
        "shopping-list-index.txt",
    ]


def test_save_copies_the_text_list_and_reports_refusal() -> None:
    result = node(
        """
        const model = {title: "Test", url: "https://x.org/menu-builder.html", scale: null,
                       groups: []};
        const copied = [];
        const clip = (ok) => ({writeText: (text) => {
          copied.push(text);
          return ok ? Promise.resolve() : Promise.reject(new Error("denied"));
        }});
        // The refused path falls back to a hidden textarea, which also fails here.
        const box = {style: {}, setAttribute() {}, select() {},
                     parentNode: {removeChild() {}}};
        global.document = {createElement: () => box, body: {appendChild() {}},
                           execCommand: () => false};
        Object.defineProperty(globalThis, "navigator",
                              {value: {clipboard: clip(true)}, configurable: true});
        const ok = await shop.save("copy", model);
        Object.defineProperty(globalThis, "navigator",
                              {value: {clipboard: clip(false)}, configurable: true});
        const refused = await shop.save("copy", model);
        return [ok, refused, copied.length, copied[0] === shop.toText(model)];
        """
    )
    assert result == ["Copied", "Couldn't copy; use Download", 2, True]
