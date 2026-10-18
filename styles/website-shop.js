// Shopping list on the website: "Download .txt", "Download .csv" and "Copy" in a print
// bar. The list is read from the ingredient lists as the page shows them, so amounts
// scaled by scale.js come out scaled and {{no-scale}} lines come out as written. Lines
// are grouped by recipe and component and never merged.
//
// On a recipe or component page the list starts with the page's own ingredients, which
// works even when the page is opened from files. With "Include homemade components"
// ticked on a served site (http or https), the component pages in the bar's
// data-print-pages are fetched through print.js (sharing its cache) and added at the
// page's scale. A game-day menu or dish-off card lists its recipes, then its components
// if ticked, as written; it needs a served site, so opened from files it does nothing.
// Without JavaScript the buttons stay hidden. Tested from tests/unit/test_website_shop.py.
(function (root, factory) {
  "use strict";
  var api = factory(root);
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  } else {
    root.NflShop = api;
    if (typeof document !== "undefined") {
      if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", api.init);
      } else {
        api.init();
      }
    }
  }
})(this, function (root) {
  "use strict";

  var COMPONENT = " (homemade component)";

  function each(list, fn) {
    Array.prototype.forEach.call(list, fn);
  }

  // A sibling script's API (NflScale from scale.js, NflPrint from print.js), if loaded.
  function sibling(name) {
    if (root && root[name]) return root[name];
    if (typeof globalThis !== "undefined" && globalThis[name])
      return globalThis[name];
    return null;
  }

  function squash(text) {
    return String(text || "")
      .replace(/\s+/g, " ")
      .trim();
  }

  // "component-x.html" from "https://site/book/component-x.html?scale=2#top".
  function fileName(url) {
    return (
      String(url || "")
        .split(/[?#]/)[0]
        .split("/")
        .pop() || ""
    );
  }

  function kindOf(url) {
    return /^component-/.test(fileName(url)) ? "component" : "recipe";
  }

  // ------------------------------------------------------------------ reading pages
  // An ingredient line's text as shown, without the "Q" link to a component's page.
  function lineText(li) {
    var text = squash(li.textContent);
    var mark = li.querySelector("a.q-mark");
    var q = mark ? squash(mark.textContent) : "";
    if (q && text.slice(-q.length) === q)
      text = squash(text.slice(0, -q.length));
    return text;
  }

  // {amount, item, text}: the amount only when the line starts with its marked amount.
  function splitLine(text, qtyText) {
    var amount = squash(qtyText);
    if (amount && text.indexOf(amount) === 0) {
      return {
        amount: amount,
        item: squash(text.slice(amount.length)),
        text: text,
      };
    }
    return { amount: "", item: text, text: text };
  }

  // The ingredient lists under `root` in page order: [{heading, lines}].
  function sections(root) {
    var out = [];
    var current = null;
    each(
      root.querySelectorAll(".ingredients h3, .ingredients li"),
      function (node) {
        if (node.tagName === "H3") {
          current = { heading: squash(node.textContent) || null, lines: [] };
          out.push(current);
          return;
        }
        var text = lineText(node);
        if (!text) return;
        if (!current) {
          current = { heading: null, lines: [] };
          out.push(current);
        }
        var qty = node.querySelector("span.qty");
        current.lines.push(splitLine(text, qty ? qty.textContent : ""));
      },
    );
    return out.filter(function (section) {
      return section.lines.length;
    });
  }

  function mainOf(doc) {
    return (
      doc.querySelector("main.content") || doc.querySelector("main") || doc.body
    );
  }

  // One recipe's or component's group, read from a page. With `scale`, the amounts are
  // rewritten first (a fetched page arrives as written).
  function fromDocument(doc, url, scale) {
    var main = mainOf(doc);
    var s = sibling("NflScale");
    if (scale && s) s.applyScale(main, scale);
    var h1 = main.querySelector("h1");
    return {
      title: squash(h1 ? h1.textContent : "") || fileName(url),
      kind: kindOf(url),
      url: url,
      sections: sections(main),
    };
  }

  function fromHtml(html, url, scale) {
    var doc = new DOMParser().parseFromString(html, "text/html");
    return fromDocument(doc, url, scale);
  }

  // ------------------------------------------------------------------ the list
  // {title, scale, url, groups}; a page that failed to load keeps its place as an error.
  function build(groups, options) {
    options = options || {};
    return {
      title: options.title || "",
      scale: options.scale || null,
      url: options.url || "",
      groups: groups.map(function (group) {
        if (!group.error) return group;
        var name = fileName(group.url) || group.url;
        return {
          title: name,
          kind: kindOf(group.url),
          url: group.url,
          sections: [],
          error: "Couldn't load " + name + "; see its page.",
        };
      }),
    };
  }

  // The list for `options.here` (a group already read from this page), then `urls`,
  // fetched through print.js and read at `options.scale`, in that order.
  function listFor(urls, options) {
    options = options || {};
    var groups = options.here ? [options.here] : [];
    var printer = sibling("NflPrint");
    var fetching =
      !urls.length || !printer
        ? Promise.resolve(
            urls.map(function (url) {
              return { url: url, error: "unavailable" };
            }),
          )
        : printer.prefetch(urls, { fetchText: options.fetchText });
    return fetching.then(function (entries) {
      entries.forEach(function (entry) {
        var group = null;
        if (entry.html != null) {
          try {
            group = fromHtml(entry.html, entry.url, options.scale);
          } catch (e) {
            group = null;
          }
        }
        groups.push(
          group || { url: entry.url, error: entry.error || "unreadable" },
        );
      });
      return build(groups, options);
    });
  }

  function scaleNote(scale) {
    var s = sibling("NflScale");
    var factor = s && scale ? s.parseFactor(scale) : 0;
    if (!factor || Math.abs(factor - 1) < 1e-9) return "";
    return " (scaled " + s.describe(factor) + ")";
  }

  function forLabel(group) {
    return group.title + (group.kind === "component" ? COMPONENT : "");
  }

  function toText(model) {
    var out = ["Shopping list: " + model.title + scaleNote(model.scale)];
    if (model.url) out.push(model.url);
    model.groups.forEach(function (group) {
      out.push("");
      out.push(
        group.title.toUpperCase() +
          (group.kind === "component" ? COMPONENT : ""),
      );
      if (group.error) {
        out.push(group.error);
        return;
      }
      group.sections.forEach(function (section) {
        if (section.heading) out.push(section.heading);
        section.lines.forEach(function (line) {
          out.push("- " + line.text);
        });
      });
    });
    return out.join("\n") + "\n";
  }

  // One CSV field (RFC 4180): quoted when it holds a quote, comma or line break.
  function csvField(value) {
    var text = value == null ? "" : String(value);
    return /[",\r\n]/.test(text) ? '"' + text.replace(/"/g, '""') + '"' : text;
  }

  // Amounts keep their units ("1 cup + 2 tablespoons" once scaled), so there is no
  // separate unit column. The byte order mark lets spreadsheets read it as UTF-8.
  function toCsv(model) {
    var rows = [["For", "Section", "Amount", "Item"]];
    model.groups.forEach(function (group) {
      var who = forLabel(group);
      if (group.error) {
        rows.push([who, "", "", group.error]);
        return;
      }
      group.sections.forEach(function (section) {
        section.lines.forEach(function (line) {
          rows.push([who, section.heading || "", line.amount, line.item]);
        });
      });
    });
    return (
      "\uFEFF" +
      rows
        .map(function (row) {
          return row.map(csvField).join(",");
        })
        .join("\r\n") +
      "\r\n"
    );
  }

  // "shopping-list-<page>[-<card anchor>].<ext>" from a page address.
  function filename(base, ext) {
    var page = fileName(base).replace(/\.html?$/i, "") || "index";
    var hash = String(base || "").split("#")[1] || "";
    return "shopping-list-" + page + (hash ? "-" + hash : "") + "." + ext;
  }

  // ------------------------------------------------------------------ saving
  function download(name, text, mime) {
    var url = URL.createObjectURL(new Blob([text], { type: mime }));
    var link = document.createElement("a");
    link.href = url;
    link.download = name;
    link.hidden = true;
    document.body.appendChild(link);
    link.click();
    link.parentNode.removeChild(link);
    setTimeout(function () {
      URL.revokeObjectURL(url);
    }, 1000);
  }

  function copyFallback(text) {
    var box = document.createElement("textarea");
    box.value = text;
    box.setAttribute("readonly", "");
    box.style.position = "fixed";
    box.style.opacity = "0";
    document.body.appendChild(box);
    box.select();
    var ok = false;
    try {
      ok = document.execCommand("copy");
    } catch (e) {
      ok = false;
    }
    box.parentNode.removeChild(box);
    return ok;
  }

  // Resolves true once `text` is on the clipboard, false when the browser refuses.
  function copy(text) {
    var clip = typeof navigator !== "undefined" && navigator.clipboard;
    if (clip && clip.writeText) {
      return clip.writeText(text).then(
        function () {
          return true;
        },
        function () {
          return copyFallback(text);
        },
      );
    }
    return Promise.resolve(copyFallback(text));
  }

  // ------------------------------------------------------------------ page wiring
  function currentScale() {
    var s = sibling("NflScale");
    var text = new URLSearchParams(window.location.search).get("scale");
    return s && text && s.parseFactor(text) ? s.reduce(text) : null;
  }

  function pageAddress() {
    return window.location.href.split("#")[0];
  }

  // The list for a recipe or component page's bar: this page as shown, then its
  // component pages when ticked (and the site is served).
  function pageList(bar, served) {
    var printer = sibling("NflPrint");
    var here = fromDocument(document, window.location.href, null);
    var toggle = bar.querySelector("input[name=print-with]");
    var pages =
      served && printer && toggle && toggle.checked
        ? printer.pageList(bar.getAttribute("data-print-pages"))
        : [];
    return listFor(pages, {
      scale: currentScale(),
      title: here.title,
      url: pageAddress(),
      here: here,
    });
  }

  // The list for a menu card: its recipes, then its components when ticked, as written.
  function menuList(bar) {
    var printer = sibling("NflPrint");
    var toggle = bar.querySelector("input[name=print-with]");
    var card = bar.closest(".menu-card") || bar.parentNode;
    var heading = card.querySelector("h2");
    var anchor = card.querySelector("[id]");
    var pages = printer
      ? printer.menuPages(bar, Boolean(toggle && toggle.checked))
      : [];
    return listFor(pages, {
      scale: null,
      title: squash(heading ? heading.textContent : ""),
      url: pageAddress() + (anchor ? "#" + anchor.id : ""),
    });
  }

  function wire(actions, served) {
    var bar = actions.closest(".print-bar");
    if (!bar) return;
    var menu = bar.classList.contains("print-menu");
    if (menu && !served) return;
    var status = actions.querySelector(".shop-status");
    var buttons = actions.querySelectorAll("button[data-shop]");
    function busy(on) {
      each(buttons, function (button) {
        button.disabled = on;
      });
    }
    function say(text) {
      if (status) status.textContent = text;
    }
    each(buttons, function (button) {
      button.addEventListener("click", function () {
        var how = button.getAttribute("data-shop");
        busy(true);
        say("");
        (menu ? menuList(bar) : pageList(bar, served))
          .then(function (model) {
            if (how === "copy") {
              return copy(toText(model)).then(function (ok) {
                say(ok ? "Copied" : "Couldn't copy; use Download");
              });
            }
            if (how === "csv") {
              download(
                filename(model.url, "csv"),
                toCsv(model),
                "text/csv;charset=utf-8",
              );
            } else {
              download(
                filename(model.url, "txt"),
                toText(model),
                "text/plain;charset=utf-8",
              );
            }
            say("Downloaded");
          })
          .catch(function () {
            say("Couldn't make the list");
          })
          .then(function () {
            busy(false);
          });
      });
    });
    actions.hidden = false;
  }

  function init() {
    // Pages opened from files cannot fetch each other, so extra pages need a server.
    var served = /^https?:$/.test(window.location.protocol);
    each(
      document.querySelectorAll(".print-bar .shop-actions"),
      function (actions) {
        wire(actions, served);
      },
    );
  }

  return {
    lineText: lineText,
    splitLine: splitLine,
    sections: sections,
    fromDocument: fromDocument,
    fromHtml: fromHtml,
    build: build,
    listFor: listFor,
    toText: toText,
    csvField: csvField,
    toCsv: toCsv,
    filename: filename,
    download: download,
    copy: copy,
    init: init,
  };
});
