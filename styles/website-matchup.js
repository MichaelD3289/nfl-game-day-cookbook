// Matchup menu on the website. matchup.qmd carries the published dishes, teams,
// divisions and courses as JSON (script.matchup-data), so picking two teams works when
// the page is opened from files, with no fetch. Without JavaScript the page shows a
// note pointing to Browse recipes instead.
//
// Courses take turns: the home team leads the first course, the away team the second,
// and so on. A leading team without a dish for its course falls back to its division
// (never either matchup team), then to the other side's own dishes, then to the other
// side's division. Swap steps through the dishes of the source that was chosen, so the
// note beside the course stays true. Picks are deterministic and live in the page
// address (?home=chiefs&away=raiders&pick=id), which lists only swapped courses.
// Printing and the shopping list fetch the recipe pages through print.js and shop.js,
// so they need a served site (http or https) and stay hidden otherwise.
// Tested from tests/unit/test_website_matchup.py.
(function (root, factory) {
  "use strict";
  var api = factory(root);
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  } else {
    root.NflMatchup = api;
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

  var BUILDER = "menu-builder.html";

  function toArray(list) {
    return Array.prototype.slice.call(list || []);
  }

  // A sibling script's API (NflMenu, NflPrint, NflShop), if loaded. print.js and
  // shop.js load after this script, so callers look them up when they need them.
  function sibling(name) {
    if (root && root[name]) return root[name];
    if (typeof globalThis !== "undefined" && globalThis[name])
      return globalThis[name];
    return null;
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

  function find(list, key, value) {
    for (var i = 0; i < list.length; i += 1) {
      if (list[i][key] === value) return list[i];
    }
    return null;
  }

  // ------------------------------------------------------------------ data
  // {courses, divisions, teams, dishes} from the page, or null.
  function readData(doc) {
    var el = doc && doc.querySelector && doc.querySelector(".matchup-data");
    if (!el) return null;
    try {
      var data = JSON.parse(el.textContent);
      return data && data.teams && data.dishes && data.courses ? data : null;
    } catch (e) {
      return null;
    }
  }

  // {home, away, picks}: unknown teams become "", the same team twice drops away, and
  // picks keep known dish ids in address order.
  function parseMatchup(search, data) {
    var p = params(search);
    function team(slug) {
      return slug && find(data.teams, "slug", slug) ? slug : "";
    }
    var home = team(p.home);
    var away = team(p.away);
    if (away && away === home) away = "";
    var picks = String(p.pick || "")
      .split(",")
      .filter(function (id) {
        return id && find(data.dishes, "id", id);
      });
    return { home: home, away: away, picks: picks };
  }

  // "?home=x&away=y&pick=a,b" (only courses swapped away from their first dish), or "".
  function serializeMatchup(state, spread) {
    var parts = [];
    if (state.home) parts.push("home=" + encodeURIComponent(state.home));
    if (state.away) parts.push("away=" + encodeURIComponent(state.away));
    var picks = (spread || [])
      .filter(function (entry) {
        return entry.dish && entry.pool.length && entry.dish !== entry.pool[0];
      })
      .map(function (entry) {
        return encodeURIComponent(entry.dish.id);
      });
    if (picks.length) parts.push("pick=" + picks.join(","));
    return parts.length ? "?" + parts.join("&") : "";
  }

  // A team's own dishes for a course, and its division neighbours' dishes (teams in
  // `exclude` left out), both in book order.
  function pool(data, teamSlug, courseId, exclude) {
    var team = find(data.teams, "slug", teamSlug);
    var own = [];
    var division = [];
    data.dishes.forEach(function (dish) {
      if (dish.course !== courseId) return;
      if (dish.team === teamSlug) own.push(dish);
      else if (
        team &&
        dish.division === team.division &&
        (exclude || []).indexOf(dish.team) < 0
      )
        division.push(dish);
    });
    return { own: own, division: division };
  }

  // One entry per course: {course, side, team, opponent, source, dish, pool}. `team`
  // leads the course; `pool` is the list the dish came from, so Swap stays inside it.
  function suggest(data, home, away, picks) {
    var both = [home, away];
    return data.courses.map(function (course, index) {
      var side = index % 2 === 0 ? "home" : "away";
      var lead = side === "home" ? home : away;
      var other = side === "home" ? away : home;
      var mine = pool(data, lead, course.id, both);
      var theirs = pool(data, other, course.id, both);
      var choices = [
        ["team", mine.own],
        ["division", mine.division],
        ["other", theirs.own],
        ["other", theirs.division],
      ];
      var source = "none";
      var list = [];
      for (var i = 0; i < choices.length; i += 1) {
        if (choices[i][1].length) {
          source = choices[i][0];
          list = choices[i][1];
          break;
        }
      }
      var dish = null;
      (picks || []).some(function (id) {
        dish = find(list, "id", id);
        return dish;
      });
      return {
        course: course.id,
        side: side,
        team: lead,
        opponent: other,
        source: source,
        dish: dish || list[0] || null,
        pool: list,
      };
    });
  }

  // The dish after `currentId` in `list`, wrapping round; the first for an unknown id.
  function nextDish(list, currentId) {
    if (!list || !list.length) return null;
    for (var i = 0; i < list.length; i += 1) {
      if (list[i].id === currentId) return list[(i + 1) % list.length];
    }
    return list[0];
  }

  function spreadIds(spread) {
    return spread
      .filter(function (entry) {
        return entry.dish;
      })
      .map(function (entry) {
        return entry.dish.id;
      });
  }

  function menuBuilderHref(ids) {
    return (
      BUILDER +
      (ids.length ? "?r=" + ids.map(encodeURIComponent).join(",") : "")
    );
  }

  function courseWord(data, id) {
    var course = find(data.courses, "id", id);
    return course ? String(course.singular || course.label).toLowerCase() : id;
  }

  function teamOf(data, slug) {
    return find(data.teams, "slug", slug) || { short: slug, name: slug };
  }

  function divisionName(data, key) {
    var division = find(data.divisions || [], "key", key);
    return division ? division.name : key;
  }

  // Why a course's dish is not the leading team's own, or "" when it is.
  function sourceNote(entry, data) {
    var word = courseWord(data, entry.course);
    var lead = teamOf(data, entry.team);
    if (entry.source === "none") return "No " + word + " from either side yet";
    if (entry.source === "division") {
      return (
        "From the " +
        divisionName(data, lead.division) +
        ": no " +
        lead.short +
        " " +
        word +
        " yet"
      );
    }
    if (entry.source === "other" && entry.dish) {
      var cover =
        entry.dish.team === entry.opponent
          ? "the " + teamOf(data, entry.opponent).short + " cover it"
          : "the " + divisionName(data, entry.dish.division) + " covers it";
      return (
        "No " +
        lead.short +
        " or " +
        divisionName(data, lead.division) +
        " " +
        word +
        " yet, so " +
        cover
      );
    }
    return "";
  }

  function matchupTitle(data, home, away) {
    return teamOf(data, away).name + " at " + teamOf(data, home).name;
  }

  // ------------------------------------------------------------------ page
  function init(doc, win) {
    doc = doc && doc.querySelector ? doc : root.document;
    win = win || root;
    if (!doc) return null;
    var container = doc.querySelector(".matchup");
    var data = readData(doc);
    if (!container || !data) return null;
    var loc = win.location || {};
    var served = /^https?:$/.test(loc.protocol || "");
    var noJs = doc.querySelector(".matchup-nojs");
    var pickers = container.querySelector(".matchup-pickers");
    var homeSelect = container.querySelector("select[name=home]");
    var awaySelect = container.querySelector("select[name=away]");
    var status = container.querySelector(".matchup-status");
    var spreadEl = container.querySelector(".matchup-spread");
    var title = spreadEl && spreadEl.querySelector(".matchup-title");
    var list = spreadEl && spreadEl.querySelector(".matchup-courses");
    var actions = container.querySelector(".matchup-actions");
    var builder = actions && actions.querySelector(".matchup-builder");
    var servedEl = actions && actions.querySelector(".matchup-served");
    var printButton = servedEl && servedEl.querySelector(".print-button");
    var withLabel = servedEl && servedEl.querySelector(".print-with");
    var toggle = withLabel && withLabel.querySelector("input[name=print-with]");
    var shopButtons = servedEl
      ? toArray(servedEl.querySelectorAll("button[data-shop]"))
      : [];
    var shopStatus = servedEl && servedEl.querySelector(".shop-status");
    var busy = false;
    var raw = params(loc.search);
    var state = parseMatchup(loc.search, data);
    var clash = Boolean(raw.home && raw.home === raw.away && state.home);
    var spread = [];

    function ready() {
      return Boolean(state.home && state.away);
    }

    function address() {
      return (
        (loc.pathname || "") +
        serializeMatchup(state, spread) +
        (loc.hash || "")
      );
    }

    function fullAddress() {
      var href = String(loc.href || "").split(/[?#]/)[0];
      return href + serializeMatchup(state, spread);
    }

    function remember() {
      var history = win.history;
      if (!history || !history.replaceState) return;
      try {
        history.replaceState(null, "", address());
      } catch (e) {
        // Opened from a file, some browsers refuse to change the address.
      }
    }

    function menuDishes() {
      return spread
        .filter(function (entry) {
          return entry.dish;
        })
        .map(function (entry) {
          return {
            id: entry.dish.id,
            url: entry.dish.url,
            printPages: entry.dish.printPages || [],
          };
        });
    }

    function pages(withComponents) {
      var menu = sibling("NflMenu");
      var dishes = menuDishes();
      if (!menu) {
        return dishes.map(function (dish) {
          return dish.url;
        });
      }
      return menu.menuPages(spreadIds(spread), dishes, withComponents);
    }

    function courseItem(entry) {
      var course = find(data.courses, "id", entry.course) || {};
      var lead = teamOf(data, entry.team);
      var item = doc.createElement("li");
      item.className = "matchup-course";
      item.setAttribute("data-course", entry.course);
      var name = doc.createElement("span");
      name.className = "matchup-course-name";
      name.textContent = course.singular || course.label || entry.course;
      item.appendChild(name);
      var side = doc.createElement("span");
      side.className = "matchup-side";
      side.textContent =
        (entry.side === "home" ? "Home" : "Away") + " · " + lead.name;
      item.appendChild(side);
      if (entry.dish) {
        var link = doc.createElement("a");
        link.className = "matchup-dish";
        link.setAttribute("href", entry.dish.url);
        link.textContent = entry.dish.title;
        item.appendChild(link);
      }
      var text = sourceNote(entry, data);
      if (text) {
        var note = doc.createElement("p");
        note.className = "matchup-note";
        note.textContent = text;
        item.appendChild(note);
      }
      var swap = doc.createElement("button");
      swap.className = "matchup-swap";
      swap.setAttribute("type", "button");
      swap.setAttribute("data-course", entry.course);
      swap.setAttribute(
        "aria-label",
        "Swap the " + courseWord(data, entry.course),
      );
      swap.textContent = "Swap";
      swap.disabled = entry.pool.length < 2;
      swap.addEventListener("click", function () {
        swapCourse(entry.course);
      });
      item.appendChild(swap);
      return item;
    }

    function showButtons() {
      var ids = spreadIds(spread);
      var components = ids.length && pages(true).length > ids.length;
      if (withLabel) withLabel.hidden = !components;
      if (printButton) printButton.disabled = busy || !ids.length;
      shopButtons.forEach(function (button) {
        button.disabled = busy || !ids.length;
      });
    }

    function render() {
      spread = ready()
        ? suggest(data, state.home, state.away, state.picks)
        : [];
      if (homeSelect) homeSelect.value = state.home;
      if (awaySelect) awaySelect.value = state.away;
      if (status) {
        status.textContent = ready()
          ? ""
          : clash
            ? "Pick two different teams"
            : "Pick a home and an away team";
      }
      if (list) {
        while (list.firstChild) list.removeChild(list.firstChild);
        spread.forEach(function (entry) {
          list.appendChild(courseItem(entry));
        });
      }
      if (title) {
        title.textContent = ready()
          ? matchupTitle(data, state.home, state.away)
          : "";
      }
      if (spreadEl) spreadEl.hidden = !ready();
      var ids = spreadIds(spread);
      if (builder) builder.setAttribute("href", menuBuilderHref(ids));
      if (actions) actions.hidden = !ids.length;
      showButtons();
    }

    function swapCourse(courseId) {
      state.picks = spread
        .map(function (entry) {
          if (entry.course !== courseId) return entry.dish;
          return nextDish(entry.pool, entry.dish && entry.dish.id);
        })
        .filter(function (dish, index) {
          var entry = spread[index];
          return dish && entry.pool.length && dish !== entry.pool[0];
        })
        .map(function (dish) {
          return dish.id;
        });
      render();
      remember();
    }

    function pickTeams() {
      state.home = homeSelect ? homeSelect.value : "";
      state.away = awaySelect ? awaySelect.value : "";
      clash = Boolean(state.home && state.home === state.away);
      if (clash) state.away = "";
      state.picks = [];
      render();
      if (clash && awaySelect) awaySelect.value = "";
      remember();
    }

    function setBusy(on) {
      busy = on;
      showButtons();
    }

    function withComponents() {
      return Boolean(toggle && toggle.checked);
    }

    function printSpread() {
      var printer = sibling("NflPrint");
      if (!printer || !spreadIds(spread).length) return;
      setBusy(true);
      printer
        .printBundle(pages(withComponents()), { scale: null, target: spreadEl })
        .then(null, function () {
          printer.tidy();
          printer.isolate(
            spreadEl,
            doc.querySelector("main.content") || doc.body,
          );
          win.addEventListener("afterprint", printer.tidy, { once: true });
          win.print();
        })
        .then(function () {
          setBusy(false);
        });
    }

    function shop(how) {
      var lists = sibling("NflShop");
      if (!lists || !spreadIds(spread).length) return;
      if (shopStatus) shopStatus.textContent = "";
      setBusy(true);
      lists
        .listFor(pages(withComponents()), {
          scale: null,
          title:
            matchupTitle(data, state.home, state.away) + " game-day spread",
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

    [homeSelect, awaySelect].forEach(function (select) {
      if (select) select.addEventListener("change", pickTeams);
    });
    if (pickers) {
      pickers.addEventListener("submit", function (event) {
        event.preventDefault();
      });
    }
    if (served && servedEl) {
      if (printButton) printButton.addEventListener("click", printSpread);
      if (toggle) {
        toggle.addEventListener("change", function () {
          var printer = sibling("NflPrint");
          if (toggle.checked && printer && spreadIds(spread).length)
            printer.prefetch(pages(true));
        });
      }
      shopButtons.forEach(function (button) {
        button.addEventListener("click", function () {
          shop(button.getAttribute("data-shop"));
        });
      });
      servedEl.hidden = false;
      var shopActions = servedEl.querySelector(".shop-actions");
      if (shopActions) shopActions.hidden = false;
    }

    render();
    if (noJs) noJs.hidden = true;
    if (pickers) pickers.hidden = false;
    return {
      render: render,
      state: function () {
        return {
          home: state.home,
          away: state.away,
          picks: state.picks.slice(),
        };
      },
    };
  }

  return {
    readData: readData,
    parseMatchup: parseMatchup,
    serializeMatchup: serializeMatchup,
    pool: pool,
    suggest: suggest,
    nextDish: nextDish,
    spreadIds: spreadIds,
    menuBuilderHref: menuBuilderHref,
    sourceNote: sourceNote,
    matchupTitle: matchupTitle,
    init: init,
  };
});
