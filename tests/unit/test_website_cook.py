"""Cook mode state helpers in styles/website-cook.js, run through Node.

Cook mode runs in the browser, so its check-off keys and saved state live in
JavaScript. These tests need Node.js and are skipped when it is not installed.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "styles" / "website-cook.js"
NODE = shutil.which("node")
pytestmark = pytest.mark.skipif(NODE is None, reason="Node.js is not installed")

# Minimal stand-ins for DOM nodes and Web Storage, so the helpers run without a browser.
PRELUDE = """
const c = require(SCRIPT);
function text(value) { return { nodeType: 3, nodeValue: value }; }
function el(tag, className, children) {
  return { nodeType: 1, tagName: tag.toUpperCase(), className: className || "",
           childNodes: children || [] };
}
function memory() {
  const data = {}; const calls = [];
  return {
    data, calls,
    getItem(k) { calls.push(["get", k]); return k in data ? data[k] : null; },
    setItem(k, v) { calls.push(["set", k]); data[k] = String(v); },
    removeItem(k) { calls.push(["remove", k]); delete data[k]; },
  };
}
const broken = {
  getItem() { throw new Error("denied"); },
  setItem() { throw new Error("quota"); },
  removeItem() { throw new Error("denied"); },
};
"""


def node(body: str) -> Any:
    assert NODE is not None
    program = PRELUDE.replace("SCRIPT", json.dumps(str(SCRIPT))) + (
        f"process.stdout.write(JSON.stringify((() => {{ {body} }})()));"
    )
    result = subprocess.run(
        [NODE, "-e", program], capture_output=True, text=True, check=True, timeout=30
    )
    return json.loads(result.stdout)


def test_storage_key_is_per_page() -> None:
    assert node('return c.storageKey("recipe:test-citrus-wings");') == (
        "nfl-cook:recipe:test-citrus-wings"
    )


def test_line_key_ignores_quantities_and_scaling() -> None:
    result = node(
        """
        const line = (amount, scaled) => el("li", "", [
          el("span", scaled ? "qty qty-scaled" : "qty", [text(amount)]),
          text(" ground   chicken "),
          el("a", "q-mark", [text("Q")]),
        ]);
        const plain = c.lineText(line("1 lb", false));
        const doubled = c.lineText(line("2 lb", true));
        return [plain, doubled,
                c.lineKey("i", plain, {}), c.lineKey("i", doubled, {})];
        """
    )
    assert result[0] == result[1]
    assert result[2] == result[3] == "i:ground chicken#1"


def test_line_text_uses_the_item_itself_not_nested_lists() -> None:
    result = node(
        """
        const step = el("li", "", [
          el("p", "", [text("Make the "), el("strong", "", [text("Sauce")])]),
          el("ul", "", [el("li", "", [text("nested detail")])]),
        ]);
        return c.lineKey("s", c.lineText(step), {});
        """
    )
    assert result == "s:make the sauce#1"


def test_duplicate_lines_get_distinct_keys() -> None:
    result = node(
        """
        const seen = {};
        return [c.lineKey("i", "Salt", seen), c.lineKey("i", " salt ", seen),
                c.lineKey("s", "salt", seen), c.lineKey("i", "Pepper", seen)];
        """
    )
    assert result == ["i:salt#1", "i:salt#2", "s:salt#1", "i:pepper#1"]


def test_load_falls_back_when_storage_fails_or_holds_junk() -> None:
    result = node(
        """
        const junk = memory(); junk.data.k = "{not json";
        const wrong = memory(); wrong.data.k = JSON.stringify({ on: "yes", done: [1, "a"] });
        return [c.load(broken, "k"), c.load(null, "k"), c.load(junk, "k"),
                c.load(memory(), "k"), c.load(wrong, "k")];
        """
    )
    empty = {"on": False, "done": []}
    assert result[:4] == [empty, empty, empty, empty]
    assert result[4] == {"on": False, "done": ["a"]}


def test_save_and_load_round_trip() -> None:
    result = node(
        """
        const s = memory();
        c.save(s, "k", { on: true, done: ["i:salt#1", "s:stir#1"] });
        return c.load(s, "k");
        """
    )
    assert result == {"on": True, "done": ["i:salt#1", "s:stir#1"]}


def test_save_of_an_empty_state_removes_the_item() -> None:
    result = node(
        """
        const s = memory();
        c.save(s, "k", { on: true, done: [] });
        c.save(s, "k", { on: false, done: [] });
        return [s.calls, "k" in s.data];
        """
    )
    assert result == [[["set", "k"], ["remove", "k"]], False]


def test_save_swallows_storage_errors() -> None:
    result = node(
        """
        c.save(broken, "k", { on: true, done: ["a"] });
        c.save(broken, "k", { on: false, done: [] });
        c.save(null, "k", { on: true, done: [] });
        return "ok";
        """
    )
    assert result == "ok"


def test_toggle_returns_a_new_list() -> None:
    result = node(
        """
        const before = ["a", "b"];
        const added = c.toggle(before, "c");
        const removed = c.toggle(added, "a");
        return [before, added, removed];
        """
    )
    assert result == [["a", "b"], ["a", "b", "c"], ["b", "c"]]


def test_wake_lock_is_used_only_where_supported() -> None:
    result = node(
        "return [c.canWakeLock({ wakeLock: {} }), c.canWakeLock({}), c.canWakeLock(undefined)];"
    )
    assert result == [True, False, False]
