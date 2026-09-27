// Browse recipes filters on the website. browse.qmd lists every published recipe as a
// card whose data-facets holds its filter values (course, main ingredient, practical
// time, ingredient cost, conference, division, team; the same ids as recipes.json).
// Without JavaScript the filter form stays hidden and every card shows.
//
// Choices within one filter widen the list (Appetizer or Side); choices across filters
// narrow it (Appetizer and Poultry). Each choice shows how many recipes it would give,
// counted as if that filter's own choices were cleared, and choices that would give none
// are dimmed. The chosen filters live in the page address (?course=appetizers,sides) so a
// view can be shared, bookmarked or restored with Back.
// Tested from tests/unit/test_website_browse.py.
(function (root, factory) {
  "use strict";
  var api = factory(root);
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  } else {
    root.NflBrowse = api;
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

  function decode(text) {
    try {
      return decodeURIComponent(text.replace(/\+/g, " "));
    } catch (e) {
      return "";
    }
  }

  // {facet: [option, ...]} from a query string, keeping only known facets and options,
  // each once and in the facet's own option order. facets: [{id, options: [id, ...]}].
  function parseState(search, facets) {
    var raw = {};
    String(search || "")
      .replace(/^\?/, "")
      .split("&")
      .forEach(function (pair) {
        if (!pair) return;
        var at = pair.indexOf("=");
        var key = decode(at < 0 ? pair : pair.slice(0, at));
        var value = at < 0 ? "" : pair.slice(at + 1);
        raw[key] = (raw[key] || []).concat(value.split(",").map(decode));
      });
    var state = {};
    facets.forEach(function (facet) {
      var chosen = raw[facet.id] || [];
      var picked = facet.options.filter(function (option) {
        return chosen.indexOf(option) >= 0;
      });
      if (picked.length) state[facet.id] = picked;
    });
    return state;
  }

  // The query string for state: "" when nothing is chosen, else "?a=x,y&b=z" in facet
  // and option order.
  function serializeState(state, facets) {
    var parts = [];
    facets.forEach(function (facet) {
      var chosen = state[facet.id] || [];
      var picked = facet.options.filter(function (option) {
        return chosen.indexOf(option) >= 0;
      });
      if (picked.length) {
        parts.push(
          encodeURIComponent(facet.id) +
            "=" +
            picked.map(encodeURIComponent).join(","),
        );
      }
    });
    return parts.length ? "?" + parts.join("&") : "";
  }

  // Any chosen option within a facet (OR), every facet with a choice (AND).
  function matches(recipe, state, skip) {
    return Object.keys(state).every(function (facet) {
      var chosen = state[facet];
      if (facet === skip || !chosen.length) return true;
      var values = (recipe.facets && recipe.facets[facet]) || [];
      return chosen.some(function (option) {
        return values.indexOf(option) >= 0;
      });
    });
  }

  function filterRecipes(recipes, state) {
    return recipes.filter(function (recipe) {
      return matches(recipe, state);
    });
  }

  // {facet: {option: n}}: the recipes each option would show, counted with the other
  // facets' choices applied and this facet's own choices ignored.
  function countOptions(recipes, facets, state) {
    var counts = {};
    facets.forEach(function (facet) {
      var tally = {};
      facet.options.forEach(function (option) {
        tally[option] = 0;
      });
      recipes.forEach(function (recipe) {
        if (!matches(recipe, state, facet.id)) return;
        ((recipe.facets && recipe.facets[facet.id]) || []).forEach(
          function (option) {
            if (option in tally) tally[option] += 1;
          },
        );
      });
      counts[facet.id] = tally;
    });
    return counts;
  }

  function toArray(list) {
    return Array.prototype.slice.call(list || []);
  }

  // [{id, facets, el}] from the rendered cards.
  function readCards(container) {
    return toArray(container.querySelectorAll(".finder-card")).map(
      function (card) {
        var facets = {};
        try {
          facets = JSON.parse(card.getAttribute("data-facets") || "{}");
        } catch (e) {
          facets = {};
        }
        return { id: card.getAttribute("data-id"), facets: facets, el: card };
      },
    );
  }

  // [{id, options, inputs}] from the form's fieldsets.
  function readFacets(form) {
    return toArray(form.querySelectorAll("fieldset[data-facet]")).map(
      function (fieldset) {
        var inputs = toArray(fieldset.querySelectorAll("input[type=checkbox]"));
        return {
          id: fieldset.getAttribute("data-facet"),
          options: inputs.map(function (input) {
            return input.value;
          }),
          inputs: inputs,
        };
      },
    );
  }

  function plural(n) {
    return n === 1 ? "recipe" : "recipes";
  }

  function init(doc, win) {
    doc = doc && doc.querySelector ? doc : root.document;
    win = win || root;
    var container = doc && doc.querySelector(".finder");
    var form = container && container.querySelector(".finder-filters");
    if (!form) return null;
    var facets = readFacets(form);
    var cards = readCards(container);
    var status = container.querySelector(".finder-status");
    var empty = container.querySelector(".finder-empty");
    var clear = container.querySelector(".finder-clear");

    function fromForm() {
      var state = {};
      facets.forEach(function (facet) {
        var picked = facet.inputs
          .filter(function (input) {
            return input.checked;
          })
          .map(function (input) {
            return input.value;
          });
        if (picked.length) state[facet.id] = picked;
      });
      return state;
    }

    function toForm(state) {
      facets.forEach(function (facet) {
        var chosen = state[facet.id] || [];
        facet.inputs.forEach(function (input) {
          input.checked = chosen.indexOf(input.value) >= 0;
        });
      });
    }

    function render(state) {
      var shown = 0;
      cards.forEach(function (card) {
        var on = matches(card, state);
        card.el.hidden = !on;
        if (on) shown += 1;
      });
      var counts = countOptions(cards, facets, state);
      facets.forEach(function (facet) {
        facet.inputs.forEach(function (input) {
          var n = counts[facet.id][input.value] || 0;
          var label = input.parentNode;
          var badge =
            label &&
            label.querySelector &&
            label.querySelector(".finder-count");
          if (badge) badge.textContent = "(" + n + ")";
          if (label && label.classList)
            label.classList.toggle("is-empty", n === 0 && !input.checked);
        });
      });
      var active = Object.keys(state).length > 0;
      if (status) {
        status.textContent =
          "Showing " +
          shown +
          " of " +
          cards.length +
          " " +
          plural(cards.length);
      }
      if (empty) empty.hidden = shown > 0;
      if (clear) clear.disabled = !active;
      return shown;
    }

    function remember(state) {
      var loc = win.location;
      var history = win.history;
      if (!loc || !history || !history.replaceState) return;
      try {
        history.replaceState(
          null,
          "",
          loc.pathname + serializeState(state, facets) + loc.hash,
        );
      } catch (e) {
        // Opened from a file, some browsers refuse to change the address.
      }
    }

    function update() {
      var state = fromForm();
      render(state);
      remember(state);
    }

    function restore() {
      var state = parseState(win.location ? win.location.search : "", facets);
      toForm(state);
      render(state);
    }

    form.addEventListener("change", update);
    form.addEventListener("submit", function (event) {
      event.preventDefault();
    });
    if (clear) {
      clear.addEventListener("click", function () {
        toForm({});
        update();
      });
    }
    if (win.addEventListener) win.addEventListener("popstate", restore);
    restore();
    form.hidden = false;
    return { update: update, restore: restore };
  }

  return {
    parseState: parseState,
    serializeState: serializeState,
    matches: matches,
    filterRecipes: filterRecipes,
    countOptions: countOptions,
    readCards: readCards,
    readFacets: readFacets,
    init: init,
  };
});
