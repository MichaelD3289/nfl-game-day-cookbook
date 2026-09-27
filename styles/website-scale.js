// Recipe scaling on the website. The build marks each scalable amount as
// <span class="qty" data-q="3/2" data-q2="2" data-unit="cup" data-adj="scant">; this
// script multiplies them and rewrites each one in the most readable kitchen unit.
// The print book never loads it. Conversion rules are tested from
// tests/unit/test_website_scale.py through Node.
(function (root, factory) {
  "use strict";
  var api = factory();
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  } else {
    root.NflScale = api;
    if (typeof document !== "undefined") {
      if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", api.init);
      } else {
        api.init();
      }
    }
  }
})(this, function () {
  "use strict";

  // Canonical units (must match UNITS in src/nfl_book/quantities.py). `size` is in the
  // kind's base unit, `fractions` are the fractional parts cooks can measure, `min` and
  // `max` bound the amounts shown in that unit, and `rank` orders units by size.
  var UNITS = {
    tsp: {
      kind: "us-volume",
      size: 1,
      one: "teaspoon",
      many: "teaspoons",
      fractions: [0, 1 / 8, 1 / 4, 1 / 2, 3 / 4],
      min: 1 / 8,
      max: 4,
    },
    tbsp: {
      kind: "us-volume",
      size: 3,
      one: "tablespoon",
      many: "tablespoons",
      fractions: [0, 1 / 2],
      min: 1,
      max: 12,
    },
    cup: {
      kind: "us-volume",
      size: 48,
      one: "cup",
      many: "cups",
      fractions: [0, 1 / 4, 1 / 3, 1 / 2, 2 / 3, 3 / 4],
      min: 1 / 4,
      max: Infinity,
    },
    pint: {
      kind: "us-volume",
      size: 96,
      one: "pint",
      many: "pints",
      input: true,
    },
    quart: {
      kind: "us-volume",
      size: 192,
      one: "quart",
      many: "quarts",
      fractions: [0, 1 / 4, 1 / 2, 3 / 4],
      min: 1,
      max: Infinity,
      large: true,
    },
    gallon: {
      kind: "us-volume",
      size: 768,
      one: "gallon",
      many: "gallons",
      fractions: [0, 1 / 4, 1 / 2, 3 / 4],
      min: 1,
      max: Infinity,
      large: true,
    },
    oz: {
      kind: "us-weight",
      size: 1,
      one: "ounce",
      many: "ounces",
      fractions: [0, 1 / 4, 1 / 2, 3 / 4],
      min: 1 / 4,
      max: 16,
    },
    lb: {
      kind: "us-weight",
      size: 16,
      one: "pound",
      many: "pounds",
      fractions: [0, 1 / 4, 1 / 2, 3 / 4],
      min: 1 / 2,
      max: Infinity,
    },
    ml: { kind: "metric-volume", size: 1, one: "ml", many: "ml", metric: true },
    l: {
      kind: "metric-volume",
      size: 1000,
      one: "l",
      many: "l",
      metric: true,
      min: 1,
    },
    g: { kind: "metric-weight", size: 1, one: "g", many: "g", metric: true },
    kg: {
      kind: "metric-weight",
      size: 1000,
      one: "kg",
      many: "kg",
      metric: true,
      min: 1,
    },
  };
  // Mixed amounts shown as "<major> + <minor>" when no single unit reads well.
  var PAIRS = [
    ["cup", "tbsp"],
    ["cup", "tsp"],
    ["tbsp", "tsp"],
    ["lb", "oz"],
    ["quart", "cup"],
  ];
  var GLYPHS = [
    [1 / 8, "⅛"],
    [1 / 4, "¼"],
    [1 / 3, "⅓"],
    [1 / 2, "½"],
    [2 / 3, "⅔"],
    [3 / 4, "¾"],
  ];
  var COMPOUND_PENALTY = 0.03; // prefer "6 tablespoons" to an exact "⅓ cup + 2 teaspoons"
  var EPS = 1e-9;

  function parseFactor(text) {
    if (text == null || text === "") return null;
    var parts = String(text).split("/");
    var value =
      parts.length === 2 ? Number(parts[0]) / Number(parts[1]) : Number(text);
    return isFinite(value) && value > 0 && value <= 100 ? value : null;
  }

  function glyph(fraction) {
    for (var i = 0; i < GLYPHS.length; i++) {
      if (Math.abs(GLYPHS[i][0] - fraction) < 1e-6) return GLYPHS[i][1];
    }
    return "";
  }

  // 2.5 -> "2½", 0.25 -> "¼", 3 -> "3" (for values already on a measurable fraction).
  function number(value) {
    var whole = Math.floor(value + 1e-6);
    var part = glyph(value - whole);
    if (!part) return String(Math.round(value));
    return (whole ? String(whole) : "") + part;
  }

  function metricNumber(value, large) {
    var step = large
      ? value < 10
        ? 0.05
        : 0.5
      : value < 10
        ? 0.5
        : value < 100
          ? 1
          : 5;
    var rounded = Math.max(step, Math.round(value / step) * step);
    return String(Number(rounded.toFixed(2)));
  }

  function word(key, value, adjective) {
    var unit = UNITS[key];
    var name = value > 1 + EPS ? unit.many : unit.one;
    return (adjective ? adjective + " " : "") + name;
  }

  // Closest measurable amount of `key` to `x` (in that unit), or null outside its range.
  function nearest(key, x) {
    var unit = UNITS[key];
    var best = null;
    var base = Math.floor(x);
    for (var whole = Math.max(0, base - 1); whole <= base + 1; whole++) {
      for (var i = 0; i < unit.fractions.length; i++) {
        var candidate = whole + unit.fractions[i];
        if (candidate < unit.min - EPS || candidate > unit.max + EPS) continue;
        if (best === null || Math.abs(candidate - x) < Math.abs(best - x) - EPS)
          best = candidate;
      }
    }
    return best;
  }

  function allowed(key, original) {
    var unit = UNITS[key];
    var source = UNITS[original];
    if (unit.kind !== source.kind || unit.input) return false;
    return !unit.large || source.size >= unit.size;
  }

  function units(original) {
    return Object.keys(UNITS)
      .filter(function (key) {
        return allowed(key, original);
      })
      .sort(function (a, b) {
        return UNITS[b].size - UNITS[a].size;
      });
  }

  function metric(base, original) {
    var keys = units(original);
    for (var i = 0; i < keys.length; i++) {
      var unit = UNITS[keys[i]];
      if (
        unit.min === undefined ||
        base / unit.size >= unit.min - EPS ||
        i === keys.length - 1
      ) {
        var text = metricNumber(base / unit.size, unit.size > 1);
        return text + " " + unit.one;
      }
    }
    return "";
  }

  // Best readable form of `base` (an amount in the kind's base unit).
  function choose(base, original) {
    var candidates = [];
    var keys = units(original);
    keys.forEach(function (key) {
      var size = UNITS[key].size;
      var value = nearest(key, base / size);
      if (value === null) return;
      candidates.push({
        parts: [[key, value]],
        error: Math.abs(value * size - base) / base,
        rank: size,
      });
    });
    PAIRS.forEach(function (pair) {
      if (keys.indexOf(pair[0]) < 0 || keys.indexOf(pair[1]) < 0) return;
      var major = UNITS[pair[0]];
      var minor = UNITS[pair[1]];
      // Only cups keep a fraction before the "+": "⅓ cup + 2 teaspoons", "1 tablespoon + …".
      var steps = pair[0] === "cup" ? major.fractions : [0];
      var x = base / major.size;
      var top = null;
      for (var whole = Math.floor(x); whole >= 0 && top === null; whole--) {
        for (var i = steps.length - 1; i >= 0; i--) {
          var candidate = whole + steps[i];
          if (candidate <= x + EPS && candidate >= major.min - EPS) {
            top = candidate;
            break;
          }
        }
      }
      if (top === null) return;
      var rest = base - top * major.size;
      if (rest <= EPS) return;
      var small = nearest(pair[1], rest / minor.size);
      if (small === null || small === 0) return;
      var total = top * major.size + small * minor.size;
      candidates.push({
        parts: [
          [pair[0], top],
          [pair[1], small],
        ],
        error: Math.abs(total - base) / base + COMPOUND_PENALTY,
        rank: major.size,
      });
    });
    candidates.sort(function (a, b) {
      var diff = Math.round(a.error * 1000) - Math.round(b.error * 1000);
      return diff || b.rank - a.rank;
    });
    return candidates[0] || null;
  }

  function formatParts(parts, adjective) {
    return parts
      .map(function (part, i) {
        return (
          number(part[1]) +
          " " +
          word(part[0], part[1], i === 0 ? adjective : "")
        );
      })
      .join(" + ");
  }

  function formatMeasured(low, high, unitKey, adjective) {
    var unit = UNITS[unitKey];
    var lo = low * unit.size;
    if (unit.metric) {
      var text = metric(lo, unitKey);
      if (high == null) return text;
      var hiText = metric(high * unit.size, unitKey);
      var loParts = text.split(" ");
      var hiParts = hiText.split(" ");
      if (loParts[1] === hiParts[1]) return loParts[0] + "–" + hiText;
      return text + " to " + hiText;
    }
    if (high == null) {
      var best = choose(lo, unitKey);
      return best ? formatParts(best.parts, adjective) : "";
    }
    // Ranges share one unit: the one that fits both ends best.
    var hi = high * unit.size;
    var pick = null;
    units(unitKey).forEach(function (key) {
      var size = UNITS[key].size;
      var a = nearest(key, lo / size);
      var b = nearest(key, hi / size);
      if (a === null || b === null) return;
      var error = Math.max(
        Math.abs(a * size - lo) / lo,
        Math.abs(b * size - hi) / hi,
      );
      if (
        pick === null ||
        Math.round(error * 1000) < Math.round(pick.error * 1000)
      ) {
        pick = { key: key, a: a, b: b, error: error };
      }
    });
    if (!pick) return "";
    if (Math.abs(pick.a - pick.b) < EPS) {
      return number(pick.a) + " " + word(pick.key, pick.a, adjective);
    }
    return (
      number(pick.a) +
      "–" +
      number(pick.b) +
      " " +
      word(pick.key, pick.b, adjective)
    );
  }

  function countEnd(value, direction) {
    if (Math.abs(value - Math.round(value)) < 0.1 && Math.round(value) > 0) {
      return String(Math.round(value));
    }
    if (value < 1) {
      var best = null;
      GLYPHS.slice(1).forEach(function (g) {
        if (best === null || Math.abs(g[0] - value) < Math.abs(best[0] - value))
          best = g;
      });
      return best[1];
    }
    return String(direction < 0 ? Math.floor(value) : Math.ceil(value));
  }

  // Counts stay whole: 1.5 eggs reads "1–2", half an onion reads "½".
  function formatCount(low, high) {
    if (high == null) {
      var near = Math.round(low);
      if (Math.abs(low - near) < 0.1 && near > 0) return String(near);
      if (low < 1) return countEnd(low, 0);
      return Math.floor(low) + "–" + Math.ceil(low);
    }
    var a = countEnd(low, -1);
    var b = countEnd(high, 1);
    return a === b ? a : a + "–" + b;
  }

  // Text for one amount multiplied by `factor`.
  function scale(amount, factor) {
    var low = amount.low * factor;
    var high = amount.high == null ? null : amount.high * factor;
    if (!amount.unit) return formatCount(low, high);
    return formatMeasured(low, high, amount.unit, amount.adjective || "");
  }

  // ------------------------------------------------------------------ page wiring
  function describe(factor) {
    var whole = Math.floor(factor + 1e-6);
    var part = glyph(factor - whole);
    if (Math.abs(factor - Math.round(factor)) < 1e-6)
      return Math.round(factor) + "×";
    if (part) return (whole ? whole : "") + part + "×";
    return Math.round(factor * 100) / 100 + "×";
  }

  // Printout header for a scaled page: "Scaled 2× · serves 8–12". `low`/`high` are the
  // servings as written, or null when the recipe does not say.
  function printLabel(factor, low, high) {
    var text = "Scaled " + describe(factor);
    if (!low) return text;
    var a = Math.max(1, Math.round(low * factor));
    var b = Math.max(1, Math.round((high || low) * factor));
    return text + " · serves " + (a === b ? a : a + "–" + b);
  }

  // "10/4" -> "5/2", "8/4" -> "2": short, readable ?scale= values.
  function reduce(text) {
    var parts = String(text).split("/");
    if (parts.length !== 2) return String(text);
    var a = Math.round(Number(parts[0]));
    var b = Math.round(Number(parts[1]));
    for (var x = a, y = b; y; ) {
      var t = y;
      y = x % y;
      x = t;
    }
    return b / x === 1 ? String(a / x) : a / x + "/" + b / x;
  }

  // `url` with ?scale= set to `value` ("1" removes it); "/" is left unescaped.
  function withScale(url, value) {
    var params = url.search
      .replace(/^\?/, "")
      .split("&")
      .filter(function (p) {
        return p && p.split("=")[0] !== "scale";
      });
    if (value !== "1") params.push("scale=" + value);
    return (params.length ? "?" + params.join("&") : "") + url.hash;
  }

  function readAmount(span) {
    return {
      low: parseFactor(span.getAttribute("data-q")),
      high: span.hasAttribute("data-q2")
        ? parseFactor(span.getAttribute("data-q2"))
        : null,
      unit: span.getAttribute("data-unit") || null,
      adjective: span.getAttribute("data-adj") || "",
    };
  }

  function init() {
    var panel = document.querySelector(".scaler");
    if (!panel) return;
    var spans = Array.prototype.slice.call(
      document.querySelectorAll("span.qty"),
    );
    spans.forEach(function (span) {
      span.setAttribute("data-original", span.textContent);
    });
    var buttons = panel.querySelectorAll("button[data-factor]");
    var people = panel.querySelector("input[name=servings]");
    var note = panel.querySelector(".scale-note");
    var status = panel.querySelector(".scale-status");
    var baseServings = Number(panel.getAttribute("data-servings")) || null;
    var maxServings =
      Number(panel.getAttribute("data-servings-max")) || baseServings;
    var printNote = document.querySelector(".print-scale");
    var factorText = "1";

    function apply(text, fromPeople) {
      var factor = parseFactor(text) || 1;
      factorText = Math.abs(factor - 1) < EPS ? "1" : reduce(text);
      spans.forEach(function (span) {
        var original = span.getAttribute("data-original");
        span.textContent =
          factorText === "1" ? original : scale(readAmount(span), factor);
        span.classList.toggle("qty-scaled", factorText !== "1");
      });
      Array.prototype.forEach.call(buttons, function (button) {
        var match =
          Math.abs(parseFactor(button.getAttribute("data-factor")) - factor) <
          1e-6;
        button.setAttribute("aria-pressed", match ? "true" : "false");
      });
      if (people && !fromPeople && baseServings) {
        people.value = String(Math.max(1, Math.round(baseServings * factor)));
      }
      if (note) note.hidden = factorText === "1";
      if (status)
        status.textContent =
          factorText === "1" ? "" : "Scaled " + describe(factor);
      if (printNote) {
        printNote.hidden = factorText === "1";
        printNote.textContent =
          factorText === "1"
            ? ""
            : printLabel(factor, baseServings, maxServings);
      }
      document.querySelectorAll("a[data-carry-scale]").forEach(function (link) {
        var url = new URL(link.getAttribute("href"), window.location.href);
        link.setAttribute(
          "href",
          url.pathname.split("/").pop() + withScale(url, factorText),
        );
      });
      var here = new URL(window.location.href);
      window.history.replaceState(
        null,
        "",
        here.pathname + withScale(here, factorText),
      );
    }

    Array.prototype.forEach.call(buttons, function (button) {
      button.addEventListener("click", function () {
        apply(button.getAttribute("data-factor"), false);
      });
    });
    if (people && baseServings) {
      people.addEventListener("input", function () {
        var wanted = Math.round(Number(people.value));
        if (wanted >= 1 && wanted <= 500)
          apply(wanted + "/" + baseServings, true);
      });
    }
    panel.hidden = false;
    var initial = new URLSearchParams(window.location.search).get("scale");
    apply(parseFactor(initial) ? initial : "1", false);
  }

  return {
    UNITS: UNITS,
    scale: scale,
    parseFactor: parseFactor,
    reduce: reduce,
    describe: describe,
    printLabel: printLabel,
    init: init,
  };
});
