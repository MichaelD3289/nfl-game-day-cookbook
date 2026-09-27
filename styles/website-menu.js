// Build your own menu on the website. menu-builder.qmd lists every published recipe by
// course, each row carrying its filter values (data-facets, as on Browse recipes) and
// the component pages its recipe prints (data-print-pages). Without JavaScript the page
// is a plain list of links, and the filters, Add buttons and summary stay hidden.
//
// Picked dishes and the menu-wide scale live in the page address (?r=id,id&scale=2), so
// a menu can be bookmarked or shared, and in localStorage, so it survives a return visit
// without one. An address with r= always wins over what was stored. Filters are not
// kept. Picking, filtering and the summary work when the page is opened from files;
// printing and the shopping list fetch the recipe pages through print.js and shop.js,
// so they need a served site (http or https) and stay hidden otherwise.
// Tested from tests/unit/test_website_menu.py.
(function (root, factory) {
  "use strict";
  var api = factory(root);
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  } else {
    root.NflMenu = api;
    if (typeof document !== "undefined") {
      if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", function () {
          api.init();
        });
      } else {
        api.init();
      }
    }
  }
})(this, function (root) {
  "use strict";

  var STORAGE_KEY = "nfl-menu-builder";
  var LIST_TITLE = "Your game-day menu";

  function toArray(list) {
    return Array.prototype.slice.call(list || []);
  }

  // A sibling script's API (NflBrowse, NflScale, NflPrint, NflShop), if loaded. print.js
  // and shop.js load after this script, so callers look them up when they need them.
  function sibling(name) {
    if (root && root[name]) return root[name];
    if (typeof globalThis !== "undefined" && globalThis[name])
      return globalThis[name];
    return null;
  }

  // ------------------------------------------------------------------ selection
  // `ids` without unknown or repeated ids, in menu order (the order of `known`).
  function normalise(ids, known) {
    return known.filter(function (id) {
      return ids.indexOf(id) >= 0;
    });
  }

  // A valid ?scale= value, reduced ("4/2" -> "2"), or null for none or 1×.
  function normaliseScale(text) {
    var s = sibling("NflScale");
    if (!s || text == null || !s.parseFactor(text)) return null;
    var value = s.reduce(text);
    return value === "1" ? null : value;
  }

  function params(search) {
    var result = {};
    String(search || "")
      .replace(/^\?/, "")
      .split("&")
      .forEach(function (pair) {
        if (!pair) return;
        var at = pair.indexOf("=");
        var key = at < 0 ? pair : pair.slice(0, at);
        var value = at < 0 ? "" : pair.slice(at + 1);
        try {
          result[decodeURIComponent(key)] = decodeURIComponent(
            value.replace(/\+/g, " "),
          );
        } catch (e) {
          result[key] = value;
        }
      });
    return result;
  }

  // {r: [id, ...], scale: "3/2" | null, listed: whether the address has an r key}.
  function parseSelection(search, known) {
    var p = params(search);
    var listed = Object.prototype.hasOwnProperty.call(p, "r");
    return {
      r: listed ? normalise(p.r.split(","), known) : [],
      scale: normaliseScale(p.scale),
      listed: listed,
    };
  }

  // "?r=a,b&scale=3/2", or "" for an empty 1× menu. "/" is left unescaped.
  function serializeSelection(selection, known) {
    var parts = [];
    var ids = normalise(selection.r || [], known);
    if (ids.length) parts.push("r=" + ids.map(encodeURIComponent).join(","));
    var scale = normaliseScale(selection.scale);
    if (scale) parts.push("scale=" + scale);
    return parts.length ? "?" + parts.join("&") : "";
  }

  // The address wins when it names dishes (even none: ?r=); otherwise what was stored.
  function initialSelection(search, stored, known) {
    var fromUrl = parseSelection(search, known);
    if (fromUrl.listed || !stored)
      return { r: fromUrl.r, scale: fromUrl.scale };
    return {
      r: normalise(Array.isArray(stored.r) ? stored.r : [], known),
      scale: normaliseScale(stored.scale),
    };
  }

  // win.localStorage, or null where reading it throws (blocked storage, sandboxing).
  function storageOf(win) {
    try {
      return (win && win.localStorage) || null;
    } catch (e) {
      return null;
    }
  }

  function loadStored(storage) {
    try {
      var value = storage && JSON.parse(storage.getItem(STORAGE_KEY) || "null");
      return value && typeof value === "object" ? value : null;
    } catch (e) {
      return null;
    }
  }

  function saveStored(storage, selection) {
    if (!storage) return false;
    try {
      storage.setItem(
        STORAGE_KEY,
        JSON.stringify({ r: selection.r, scale: selection.scale || "1" }),
      );
      return true;
    } catch (e) {
      return false;
    }
  }

  function addDish(ids, id, known) {
    return normalise(ids.concat([id]), known);
  }

  function removeDish(ids, id) {
    return ids.filter(function (other) {
      return other !== id;
    });
  }

  // ------------------------------------------------------------------ summary
  // [{id, label, dishes: [dish, ...]}] for the picked `ids`, in course order.
  function groupByCourse(ids, dishes, courses) {
    return courses
      .map(function (course) {
        return {
          id: course.id,
          label: course.label,
          dishes: dishes.filter(function (dish) {
            return dish.course === course.id && ids.indexOf(dish.id) >= 0;
          }),
        };
      })
      .filter(function (group) {
        return group.dishes.length;
      });
  }

  // The recipe pages of `ids` in menu order, then (when asked) every component page
  // they print, once each, in order of first appearance.
  function menuPages(ids, dishes, withComponents) {
    var picked = dishes.filter(function (dish) {
      return ids.indexOf(dish.id) >= 0;
    });
    var pages = picked.map(function (dish) {
      return dish.url;
    });
    if (withComponents) {
      picked.forEach(function (dish) {
        dish.printPages.forEach(function (url) {
          if (pages.indexOf(url) < 0) pages.push(url);
        });
      });
    }
    return pages;
  }

  function countLabel(n) {
    if (!n) return "No dishes yet";
    return n + (n === 1 ? " dish" : " dishes");
  }

  // The text for a "suggest this menu" issue: each course's dishes, then the address.
  function suggestionText(groups, address) {
    if (!groups.length) return "";
    var lines = groups.map(function (group) {
      return (
        group.label +
        ": " +
        group.dishes
          .map(function (dish) {
            return dish.team ? dish.title + " (" + dish.team + ")" : dish.title;
          })
          .join(", ")
      );
    });
    if (address) lines.push(address);
    return lines.join("\n");
  }

  // ------------------------------------------------------------------ reading the page
  function text(el, selector) {
    var found = el.querySelector(selector);
    return found ? found.textContent.replace(/\s+/g, " ").trim() : "";
  }

  // [{id, course, url, title, team, printPages, facets, el, button}] from the rows.
  function readDishes(container) {
    var browse = sibling("NflBrowse");
    var rows = browse
      ? browse.readCards(container, ".menu-dish")
      : toArray(container.querySelectorAll(".menu-dish")).map(function (el) {
          return { id: el.getAttribute("data-id"), facets: {}, el: el };
        });
    return rows.map(function (row) {
      var el = row.el;
      return {
        id: row.id,
        course: el.getAttribute("data-course"),
        url: el.getAttribute("data-url"),
        title: text(el, ".menu-dish-name"),
        team: text(el, ".menu-dish-team"),
        printPages: (el.getAttribute("data-print-pages") || "")
          .split(/\s+/)
          .filter(Boolean),
        facets: row.facets,
        el: el,
        button: el.querySelector(".menu-add"),
      };
    });
  }

  // [{id, label, el}] from the course sections, in page order.
  function readCourses(container) {
    return toArray(container.querySelectorAll(".menu-course")).map(
      function (el) {
        return {
          id: el.getAttribute("data-course"),
          label: text(el, ".menu-course-title"),
          el: el,
        };
      },
    );
  }

  // ------------------------------------------------------------------ page wiring
  function init(doc, win) {
    doc = doc && doc.querySelector ? doc : root.document;
    win = win || root;
    var container = doc && doc.querySelector(".menu-builder");
    var aside = container && container.querySelector(".menu-summary");
    if (!aside) return null;
    var browse = sibling("NflBrowse");
    var form = container.querySelector(".finder-filters");
    var facets = browse && form ? browse.readFacets(form) : [];
    var dishes = readDishes(container);
    var courses = readCourses(container);
    var known = dishes.map(function (dish) {
      return dish.id;
    });
    var storage = storageOf(win);
    var loc = win.location || {};
    var served = /^https?:$/.test(loc.protocol || "");
    var status = container.querySelector(".finder-status");
    var empty = container.querySelector(".finder-empty");
    var clearFilters = container.querySelector(".finder-clear");
    var count = aside.querySelector(".menu-count");
    var scaleLabel = aside.querySelector(".menu-summary-scale");
    var picked = aside.querySelector(".menu-picked");
    var note = aside.querySelector(".menu-empty-note");
    var scaleButtons = toArray(
      aside.querySelectorAll(".menu-scale button[data-factor]"),
    );
    var actions = aside.querySelector(".menu-actions");
    var printButton = actions && actions.querySelector(".print-button");
    var withLabel = actions && actions.querySelector(".print-with");
    var toggle = withLabel && withLabel.querySelector("input[name=print-with]");
    var shopButtons = actions
      ? toArray(actions.querySelectorAll("button[data-shop]"))
      : [];
    var shopStatus = actions && actions.querySelector(".shop-status");
    var clearMenu = aside.querySelector(".menu-clear");
    var suggestBox = doc.querySelector(".suggest[data-kind=menu]");
    var busy = false;
    var selection = initialSelection(loc.search, loadStored(storage), known);

    // Filters: rows and whole courses that do not match are hidden.
    function filter() {
      if (!browse || !form) return;
      var state = browse.formState(facets);
      var shown = 0;
      dishes.forEach(function (dish) {
        var on = browse.matches(dish, state);
        dish.el.hidden = !on;
        if (on) shown += 1;
      });
      courses.forEach(function (course) {
        course.el.hidden = !dishes.some(function (dish) {
          return dish.course === course.id && !dish.el.hidden;
        });
      });
      browse.showCounts(facets, browse.countOptions(dishes, facets, state));
      if (status) {
        status.textContent =
          "Showing " +
          shown +
          " of " +
          dishes.length +
          (dishes.length === 1 ? " recipe" : " recipes");
      }
      if (empty) empty.hidden = shown > 0;
      if (clearFilters) clearFilters.disabled = !Object.keys(state).length;
    }

    function address() {
      return (
        (loc.pathname || "") +
        serializeSelection(selection, known) +
        (loc.hash || "")
      );
    }

    function fullAddress() {
      var href = String(loc.href || "").split(/[?#]/)[0];
      return href + serializeSelection(selection, known);
    }

    function remember() {
      saveStored(storage, selection);
      var history = win.history;
      if (!history || !history.replaceState) return;
      try {
        history.replaceState(null, "", address());
      } catch (e) {
        // Opened from a file, some browsers refuse to change the address.
      }
    }

    function summaryItem(dish) {
      var item = doc.createElement("li");
      var link = doc.createElement("a");
      link.href = dish.url;
      link.textContent = dish.title;
      item.appendChild(link);
      if (dish.team) {
        var team = doc.createElement("span");
        team.className = "menu-picked-team";
        team.textContent = " " + dish.team;
        item.appendChild(team);
      }
      var remove = doc.createElement("button");
      remove.type = "button";
      remove.className = "menu-remove";
      remove.textContent = "Remove";
      remove.setAttribute("aria-label", "Remove " + dish.title);
      remove.addEventListener("click", function () {
        selection.r = removeDish(selection.r, dish.id);
        changed();
      });
      item.appendChild(remove);
      return item;
    }

    function showSummary() {
      var ids = selection.r;
      var groups = groupByCourse(ids, dishes, courses);
      dishes.forEach(function (dish) {
        if (!dish.button) return;
        var on = ids.indexOf(dish.id) >= 0;
        dish.button.setAttribute("aria-pressed", on ? "true" : "false");
        dish.button.textContent = on ? "Added" : "Add";
        dish.el.classList.toggle("is-picked", on);
      });
      if (count) count.textContent = countLabel(ids.length);
      if (note) note.hidden = ids.length > 0;
      if (picked) {
        while (picked.firstChild) picked.removeChild(picked.firstChild);
        groups.forEach(function (group) {
          var course = doc.createElement("li");
          course.className = "menu-picked-course";
          var heading = doc.createElement("span");
          heading.className = "menu-picked-label";
          heading.textContent = group.label;
          course.appendChild(heading);
          var list = doc.createElement("ul");
          group.dishes.forEach(function (dish) {
            list.appendChild(summaryItem(dish));
          });
          course.appendChild(list);
          picked.appendChild(course);
        });
      }
      var s = sibling("NflScale");
      var factor = s && selection.scale ? s.parseFactor(selection.scale) : null;
      if (scaleLabel) {
        scaleLabel.textContent = factor ? "Scaled " + s.describe(factor) : "";
        scaleLabel.hidden = !factor;
      }
      var current = selection.scale || "1";
      scaleButtons.forEach(function (button) {
        var value = normaliseScale(button.getAttribute("data-factor")) || "1";
        button.setAttribute(
          "aria-pressed",
          value === current ? "true" : "false",
        );
      });
      var components =
        ids.length && menuPages(ids, dishes, true).length > ids.length;
      if (withLabel) withLabel.hidden = !components;
      if (printButton) printButton.disabled = busy || !ids.length;
      shopButtons.forEach(function (button) {
        button.disabled = busy || !ids.length;
      });
      if (clearMenu) clearMenu.disabled = !ids.length;
      if (suggestBox) {
        var idea = suggestionText(groups, ids.length ? fullAddress() : "");
        var fields = {};
        try {
          fields = JSON.parse(suggestBox.getAttribute("data-fields") || "{}");
        } catch (e) {
          fields = {};
        }
        fields.idea = idea;
        suggestBox.setAttribute("data-fields", JSON.stringify(fields));
        var link = suggestBox.querySelector(".suggest-github");
        if (link && link.href) {
          try {
            var url = new URL(link.href);
            if (idea) url.searchParams.set("idea", idea);
            else url.searchParams.delete("idea");
            link.href = url.toString();
          } catch (e) {
            // Leave the plain link.
          }
        }
      }
    }

    function changed() {
      showSummary();
      remember();
    }

    function pages() {
      return menuPages(selection.r, dishes, Boolean(toggle && toggle.checked));
    }

    function setBusy(on) {
      busy = on;
      showSummary();
    }

    function printMenu() {
      var printer = sibling("NflPrint");
      if (!printer || !selection.r.length) return;
      setBusy(true);
      printer
        .printBundle(pages(), { scale: selection.scale, target: aside })
        .then(null, function () {
          printer.tidy();
          printer.isolate(aside, doc.querySelector("main.content") || doc.body);
          win.addEventListener("afterprint", printer.tidy, { once: true });
          win.print();
        })
        .then(function () {
          setBusy(false);
        });
    }

    function shop(how) {
      var lists = sibling("NflShop");
      if (!lists || !selection.r.length) return;
      if (shopStatus) shopStatus.textContent = "";
      setBusy(true);
      lists
        .listFor(pages(), {
          scale: selection.scale,
          title: LIST_TITLE,
          url: fullAddress(),
        })
        .then(function (model) {
          return lists.save(how, model);
        })
        .then(
          function (message) {
            if (shopStatus) shopStatus.textContent = message;
          },
          function () {
            if (shopStatus) shopStatus.textContent = "Couldn't make the list";
          },
        )
        .then(function () {
          setBusy(false);
        });
    }

    dishes.forEach(function (dish) {
      if (!dish.button) return;
      dish.button.addEventListener("click", function () {
        var on = selection.r.indexOf(dish.id) >= 0;
        selection.r = on
          ? removeDish(selection.r, dish.id)
          : addDish(selection.r, dish.id, known);
        changed();
      });
    });
    scaleButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        selection.scale = normaliseScale(button.getAttribute("data-factor"));
        changed();
      });
    });
    if (clearMenu) {
      clearMenu.addEventListener("click", function () {
        selection.r = [];
        changed();
      });
    }
    if (form) {
      form.addEventListener("change", filter);
      form.addEventListener("submit", function (event) {
        event.preventDefault();
      });
    }
    if (clearFilters && browse) {
      clearFilters.addEventListener("click", function () {
        browse.setForm(facets, {});
        filter();
      });
    }
    if (served && actions) {
      if (printButton) printButton.addEventListener("click", printMenu);
      if (toggle) {
        toggle.addEventListener("change", function () {
          var printer = sibling("NflPrint");
          if (toggle.checked && printer && selection.r.length)
            printer.prefetch(pages());
        });
      }
      shopButtons.forEach(function (button) {
        button.addEventListener("click", function () {
          shop(button.getAttribute("data-shop"));
        });
      });
      actions.hidden = false;
      var shopActions = actions.querySelector(".shop-actions");
      if (shopActions) shopActions.hidden = false;
    }

    filter();
    changed();
    if (form && browse) form.hidden = false;
    dishes.forEach(function (dish) {
      if (dish.button) dish.button.hidden = false;
    });
    aside.hidden = false;
    return {
      selection: function () {
        return { r: selection.r.slice(), scale: selection.scale };
      },
    };
  }

  return {
    parseSelection: parseSelection,
    serializeSelection: serializeSelection,
    initialSelection: initialSelection,
    loadStored: loadStored,
    saveStored: saveStored,
    storageOf: storageOf,
    addDish: addDish,
    removeDish: removeDish,
    groupByCourse: groupByCourse,
    menuPages: menuPages,
    countLabel: countLabel,
    suggestionText: suggestionText,
    readDishes: readDishes,
    readCourses: readCourses,
    init: init,
  };
});
