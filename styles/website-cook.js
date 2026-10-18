// Cook mode on the website. The build puts a hidden <div class="cook-bar"
// data-cook-key="recipe:<id>"> on recipe and component pages; this script reveals it.
// Cook mode enlarges the page, hides the site navigation, lets the cook tap ingredient
// lines and steps to check them off, and keeps the screen on where the browser allows.
// Checked lines are saved per page in localStorage. The print book and EPUB never load
// it, and the @media print rules in website.css hide it. The state helpers are tested
// from tests/unit/test_website_cook.py through Node.
(function (root, factory) {
  "use strict";
  var api = factory();
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  } else {
    root.NflCook = api;
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

  function storageKey(label) {
    return "nfl-cook:" + label;
  }

  function normalize(text) {
    return String(text).replace(/\s+/g, " ").trim().toLowerCase();
  }

  // Parts of a line that do not name it: amounts (rewritten by scale.js), the Q link
  // to a component, and nested lists (their items get keys of their own).
  function skipped(node) {
    var tag = node.tagName;
    if (tag === "UL" || tag === "OL") return true;
    var classes = String(node.className || "").split(/\s+/);
    if (classes.indexOf("qty") >= 0) return true;
    return tag === "A" && classes.indexOf("q-mark") >= 0;
  }

  // The item's own text, without amounts, so scaling never changes its key.
  function lineText(node) {
    if (node.nodeType === 3) return node.nodeValue || "";
    if (node.nodeType !== 1) return "";
    var parts = [];
    var children = node.childNodes || [];
    for (var i = 0; i < children.length; i++) {
      var child = children[i];
      if (child.nodeType === 1 && skipped(child)) continue;
      parts.push(lineText(child));
    }
    return parts.join("");
  }

  // A stable id for a line; `seen` counts repeats so two "Salt" lines differ.
  function lineKey(prefix, text, seen) {
    var base = prefix + ":" + normalize(text);
    seen[base] = (seen[base] || 0) + 1;
    return base + "#" + seen[base];
  }

  function empty() {
    return { on: false, done: [] };
  }

  function load(storage, key) {
    try {
      var raw = storage.getItem(key);
      if (!raw) return empty();
      var data = JSON.parse(raw);
      if (!data || typeof data !== "object") return empty();
      var done = Array.isArray(data.done)
        ? data.done.filter(function (id) {
            return typeof id === "string";
          })
        : [];
      return { on: data.on === true, done: done };
    } catch (error) {
      return empty();
    }
  }

  function save(storage, key, state) {
    try {
      if (!state.on && !state.done.length) {
        storage.removeItem(key);
      } else {
        storage.setItem(
          key,
          JSON.stringify({ on: !!state.on, done: state.done }),
        );
      }
    } catch (error) {
      // Private windows and blocked storage: cook mode still works for this visit.
    }
  }

  function toggle(ids, id) {
    return ids.indexOf(id) >= 0
      ? ids.filter(function (other) {
          return other !== id;
        })
      : ids.concat([id]);
  }

  function canWakeLock(nav) {
    return !!nav && typeof nav === "object" && "wakeLock" in nav;
  }

  function localStore() {
    try {
      return window.localStorage;
    } catch (error) {
      return null;
    }
  }

  var IGNORE = "a, button, input, select, textarea, label";

  function init() {
    var bar = document.querySelector(".cook-bar[data-cook-key]");
    if (!bar) return;
    var button = bar.querySelector(".cook-toggle");
    var reset = bar.querySelector(".cook-reset");
    var note = bar.querySelector(".cook-note");
    if (!button) return;
    var key = storageKey(bar.getAttribute("data-cook-key"));
    var storage = localStore();
    var state = load(storage, key);
    var wakeLock = canWakeLock(navigator);
    var sentinel = null;

    var lines = [];
    var seen = {};
    [
      [".ingredients li", "i"],
      [".instructions li", "s"],
    ].forEach(function (pair) {
      document.querySelectorAll(pair[0]).forEach(function (li) {
        li.setAttribute("data-cook-id", lineKey(pair[1], lineText(li), seen));
        lines.push(li);
      });
    });
    var known = lines.map(function (li) {
      return li.getAttribute("data-cook-id");
    });
    state.done = state.done.filter(function (id) {
      return known.indexOf(id) >= 0;
    });

    function requestLock() {
      if (!wakeLock || !state.on || document.visibilityState !== "visible")
        return;
      if (sentinel && !sentinel.released) return;
      try {
        navigator.wakeLock.request("screen").then(
          function (lock) {
            sentinel = lock;
            if (!state.on) releaseLock();
          },
          function () {},
        );
      } catch (error) {
        // Refused (for example by a permissions policy): the screen just may dim.
      }
    }

    function releaseLock() {
      if (!sentinel) return;
      var lock = sentinel;
      sentinel = null;
      try {
        lock.release().catch(function () {});
      } catch (error) {
        // Already released.
      }
    }

    function render() {
      document.documentElement.classList.toggle("cook-mode", state.on);
      button.setAttribute("aria-pressed", state.on ? "true" : "false");
      if (reset) reset.hidden = !(state.on && state.done.length);
      if (note) note.hidden = !(state.on && wakeLock);
      lines.forEach(function (li) {
        var done = state.done.indexOf(li.getAttribute("data-cook-id")) >= 0;
        li.classList.toggle("cook-done", done);
        // Lines are checkboxes only while cooking, so reading the page stays plain.
        if (state.on) {
          li.setAttribute("role", "checkbox");
          li.setAttribute("aria-checked", done ? "true" : "false");
          li.setAttribute("tabindex", "0");
        } else {
          li.removeAttribute("role");
          li.removeAttribute("aria-checked");
          li.removeAttribute("tabindex");
        }
      });
    }

    function commit() {
      save(storage, key, state);
      render();
    }

    function check(event) {
      if (!state.on) return;
      var target = event.target;
      if (!target || !target.closest) return;
      if (target.closest(IGNORE)) return;
      var li = target.closest("li[data-cook-id]");
      if (!li) return;
      if (event.type === "keydown") {
        if (event.key !== "Enter" && event.key !== " ") return;
        if (li !== target) return;
        event.preventDefault();
      }
      state.done = toggle(state.done, li.getAttribute("data-cook-id"));
      commit();
    }

    document.addEventListener("click", check);
    document.addEventListener("keydown", check);
    button.addEventListener("click", function () {
      state.on = !state.on;
      commit();
      if (state.on) requestLock();
      else releaseLock();
    });
    if (reset) {
      reset.addEventListener("click", function () {
        state.done = [];
        commit();
      });
    }
    // Browsers drop the lock when the tab is hidden; take it again on return.
    document.addEventListener("visibilitychange", function () {
      if (document.visibilityState === "visible") requestLock();
    });

    render();
    bar.hidden = false;
    requestLock();
  }

  return {
    storageKey: storageKey,
    normalize: normalize,
    lineText: lineText,
    lineKey: lineKey,
    load: load,
    save: save,
    toggle: toggle,
    canWakeLock: canWakeLock,
    init: init,
  };
});
