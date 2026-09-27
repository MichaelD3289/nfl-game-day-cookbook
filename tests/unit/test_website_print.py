"""Printing a recipe with its homemade components: styles/website-print.js through Node.

The page list, fetching and address logic live in JavaScript, so they are tested with
Node and a tiny fake DOM (no jsdom). The tests are skipped when Node is not installed.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

import pytest

STYLES = Path(__file__).resolve().parents[2] / "styles"
PRINT = STYLES / "website-print.js"
SCALE = STYLES / "website-scale.js"
NODE = shutil.which("node")
pytestmark = pytest.mark.skipif(NODE is None, reason="Node.js is not installed")

# A minimal stand-in for the elements applyScale touches.
FAKE_DOM = """
function el(attrs, text) {
  const a = Object.assign({}, attrs);
  const classes = new Set();
  return {
    textContent: text || "",
    hidden: true,
    getAttribute: (k) => (k in a ? a[k] : null),
    hasAttribute: (k) => k in a,
    setAttribute: (k, v) => { a[k] = String(v); },
    classList: { toggle: (c, on) => (on ? classes.add(c) : classes.delete(c)),
                 add: (c) => classes.add(c),
                 remove: (c) => classes.delete(c),
                 contains: (c) => classes.has(c) },
    children: [],
    parentNode: null,
  };
}
// An element with `kids` as its children, each pointing back at it.
function tree(kids, className) {
  const node = el({});
  if (className) node.classList.add(className);
  node.children = kids;
  kids.forEach((kid) => { kid.parentNode = node; });
  return node;
}
function fakeRoot(parts, attrs) {
  const r = el(attrs || {});
  r.querySelectorAll = (sel) => parts[sel] || [];
  r.querySelector = (sel) => (parts[sel] || [])[0] || null;
  return r;
}
"""


def node(body: str) -> Any:
    """Run ``body`` (an async function body returning a value) and decode its result."""
    assert NODE is not None
    program = (
        f"global.NflScale = require({json.dumps(str(SCALE))});\n"
        f"const p = require({json.dumps(str(PRINT))});\n"
        f"const s = global.NflScale;\n{FAKE_DOM}\n"
        f"(async () => {{ {body} }})().then("
        "(v) => process.stdout.write(JSON.stringify(v)),"
        "(e) => { console.error(e); process.exit(1); });"
    )
    result = subprocess.run(
        [NODE, "-e", program], capture_output=True, text=True, check=True, timeout=30
    )
    return json.loads(result.stdout)


def test_requiring_the_script_does_not_touch_the_dom() -> None:
    assert node("return Object.keys(p).sort();") == sorted(
        [
            "assemble",
            "extract",
            "footerUrl",
            "init",
            "isolate",
            "menuPages",
            "pageList",
            "prefetch",
            "printBundle",
            "release",
            "tidy",
        ]
    )


def test_page_list_splits_and_dedupes_in_order() -> None:
    assert node('return p.pageList(" b.html  a.html\\nb.html ", null, "c.html a.html", "");') == [
        "b.html",
        "a.html",
        "c.html",
    ]
    assert node("return p.pageList();") == []


def test_prefetch_keeps_order_and_isolates_failures() -> None:
    result = node(
        """
        const calls = [];
        const fetchText = (url) => {
          calls.push(url);
          if (url === "bad.html") return Promise.reject(new Error("404"));
          // The first page answers last; results still come back in input order.
          const delay = url === "a.html" ? 20 : 0;
          return new Promise((ok) => setTimeout(() => ok("<p>" + url + "</p>"), delay));
        };
        const first = await p.prefetch(["a.html", "bad.html", "b.html"], { fetchText });
        const second = await p.prefetch(["b.html", "a.html"], { fetchText });
        return { first, second, calls };
        """
    )
    assert result["first"] == [
        {"url": "a.html", "html": "<p>a.html</p>"},
        {"url": "bad.html", "error": "404"},
        {"url": "b.html", "html": "<p>b.html</p>"},
    ]
    assert result["second"] == [
        {"url": "b.html", "html": "<p>b.html</p>"},
        {"url": "a.html", "html": "<p>a.html</p>"},
    ]
    # Successful pages are cached; the second call fetched nothing.
    assert result["calls"] == ["a.html", "bad.html", "b.html"]


def test_failed_pages_are_retried() -> None:
    result = node(
        """
        let n = 0;
        const fetchText = () => (++n === 1 ? Promise.reject(new Error("offline"))
                                           : Promise.resolve("ok"));
        const first = await p.prefetch(["c.html"], { fetchText });
        const second = await p.prefetch(["c.html"], { fetchText });
        return [first, second, n];
        """
    )
    assert result == [
        [{"url": "c.html", "error": "offline"}],
        [{"url": "c.html", "html": "ok"}],
        2,
    ]


def test_footer_url_is_absolute_and_carries_the_scale() -> None:
    base = "https://example.com/book/recipe-test-citrus-wings.html?scale=3/2#top"
    assert node(
        f"return [p.footerUrl('component-test-wing-sauce.html', {json.dumps(base)}, '3/2'),"
        f" p.footerUrl('component-test-wing-sauce.html', {json.dumps(base)}, '6/4'),"
        f" p.footerUrl('component-test-wing-sauce.html', {json.dumps(base)}, '1'),"
        f" p.footerUrl('component-test-wing-sauce.html', {json.dumps(base)}, null)];"
    ) == [
        "https://example.com/book/component-test-wing-sauce.html?scale=3/2",
        "https://example.com/book/component-test-wing-sauce.html?scale=3/2",
        "https://example.com/book/component-test-wing-sauce.html",
        "https://example.com/book/component-test-wing-sauce.html",
    ]


def test_with_scale_is_exported() -> None:
    assert node(
        'return [s.withScale(new URL("https://x.org/a.html?scale=2&q=1"), "3/2"),'
        ' s.withScale(new URL("https://x.org/a.html?scale=2"), "1")];'
    ) == ["?q=1&scale=3/2", ""]


def test_apply_scale_rewrites_amounts_under_a_root() -> None:
    result = node(
        """
        const cup = el({"data-q": "1", "data-unit": "cup"}, "1 cup");
        const eggs = el({"data-q": "2", "data-q2": "3"}, "2–3");
        const times = el({}, "");
        const label = el({}, "");
        const root = fakeRoot(
          {"span.qty": [cup, eggs], ".yield-times": [times], ".print-scale": [label]},
          {"data-servings": "4", "data-servings-max": "6"},
        );
        const factor = s.applyScale(root, "6/4");
        const scaled = [factor, cup.textContent, eggs.textContent, times.textContent,
                        label.textContent, label.hidden, cup.classList.contains("qty-scaled")];
        s.applyScale(root, "1");
        return [scaled, [cup.textContent, eggs.textContent, times.textContent, label.hidden,
                         cup.classList.contains("qty-scaled")]];
        """
    )
    assert result == [
        ["3/2", "1½ cups", "3–5", " (1½×)", "Scaled 1½× · serves 6–9", False, True],
        ["1 cup", "2–3", "", True, False],
    ]


def test_menu_pages_list_recipes_then_components_once() -> None:
    result = node(
        """
        const bar = el({
          "data-print-pages": "recipe-a.html recipe-b.html",
          "data-print-components": "component-x.html component-y.html component-x.html",
        });
        const bare = el({"data-print-pages": "recipe-a.html"});
        return [p.menuPages(bar, true), p.menuPages(bar, false), p.menuPages(bare, true)];
        """
    )
    assert result == [
        ["recipe-a.html", "recipe-b.html", "component-x.html", "component-y.html"],
        ["recipe-a.html", "recipe-b.html"],
        ["recipe-a.html"],
    ]


def test_isolate_hides_everything_but_the_card_and_release_undoes_it() -> None:
    result = node(
        """
        const header = tree([]), h1 = tree([]), cardA = tree([]), cardB = tree([]);
        const url = tree([], "print-url"), bundle = tree([], "print-bundle");
        const section = tree([h1, cardA, cardB]);
        const main = tree([header, section, url, bundle]);
        const all = {header, h1, cardA, cardB, url, bundle, section, main};
        const has = (k, c) => all[k].classList.contains(c);
        const marks = () => Object.keys(all)
          .filter((k) => has(k, "print-hide") || has(k, "print-target"))
          .map((k) => k + (has(k, "print-target") ? ":target" : ""));
        p.isolate(cardA, main);
        const isolated = marks();
        p.release();
        const released = marks();
        p.isolate(cardB, main);
        p.isolate(cardA, main);
        const again = marks();
        p.release();
        return [isolated, released, again, marks()];
        """
    )
    assert result == [
        ["header", "h1", "cardA:target", "cardB"],
        [],
        ["header", "h1", "cardA:target", "cardB"],
        [],
    ]
