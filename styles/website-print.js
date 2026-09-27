// Print button on the website. The button prints the page as it is shown, so amounts
// scaled by scale.js print scaled. The @media print rules in website.css hide the site
// chrome and lay the page out for paper. Without JavaScript the button stays hidden.
//
// A recipe that uses homemade components lists their pages in the print bar's
// data-print-pages. When the site is served over http(s), ticking "Include homemade
// components" fetches those pages, and printing appends each one (at the recipe's scale)
// on its own sheet after the recipe. Tested from tests/unit/test_website_print.py.
(function (root, factory) {
  "use strict";
  var api = factory(root);
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  } else {
    root.NflPrint = api;
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

  // Parts of a fetched page that never print, or would repeat the host page's controls.
  var STRIP = [
    "script",
    ".print-bar",
    ".scaler",
    ".suggest",
    ".print-url",
    ".print-bundle",
  ];
  var IMAGE_TIMEOUT = 3000;

  function each(list, fn) {
    Array.prototype.forEach.call(list, fn);
  }

  // NflScale from scale.js, when the page loads it.
  function scaler() {
    if (root && root.NflScale) return root.NflScale;
    if (typeof globalThis !== "undefined" && globalThis.NflScale)
      return globalThis.NflScale;
    return null;
  }

  // Page lists from any number of whitespace-separated attributes, first use kept.
  function pageList() {
    var seen = {};
    var pages = [];
    each(arguments, function (attr) {
      String(attr || "")
        .split(/\s+/)
        .forEach(function (page) {
          if (page && !seen[page]) {
            seen[page] = true;
            pages.push(page);
          }
        });
    });
    return pages;
  }

  // ------------------------------------------------------------------ fetching
  var pending = {}; // url -> Promise of the page's HTML (successes stay cached)
  var settled = {}; // url -> last result, for printing synchronously from the menu

  function fetchPage(url) {
    return fetch(url, { credentials: "same-origin" }).then(function (response) {
      if (!response.ok) throw new Error("HTTP " + response.status);
      return response.text();
    });
  }

  // [{url, html} | {url, error}] in the order of `urls`; one failure spoils nothing else.
  function prefetch(urls, options) {
    var fetchText = (options && options.fetchText) || fetchPage;
    return Promise.all(
      urls.map(function (url) {
        if (!pending[url]) {
          pending[url] = new Promise(function (resolve) {
            resolve(fetchText(url));
          });
          pending[url].catch(function () {
            delete pending[url]; // try again next time
          });
        }
        return pending[url].then(
          function (html) {
            settled[url] = { url: url, html: html };
            return settled[url];
          },
          function (error) {
            settled[url] = {
              url: url,
              error: String((error && error.message) || error),
            };
            return settled[url];
          },
        );
      }),
    );
  }

  // Results for every url already fetched, or null while any is still unknown.
  function cached(urls) {
    var entries = urls.map(function (url) {
      return settled[url];
    });
    return entries.every(Boolean) ? entries : null;
  }

  // ------------------------------------------------------------------ assembling
  function currentScale() {
    var s = scaler();
    var text = new URLSearchParams(window.location.search).get("scale");
    return s && text && s.parseFactor(text) ? s.reduce(text) : null;
  }

  // Absolute address of `url` (relative to `base`) with ?scale= set, for a sheet footer.
  function footerUrl(url, base, scale) {
    var address = new URL(url, base);
    address.hash = "";
    var s = scaler();
    var factor = s && scale ? s.parseFactor(scale) : 0;
    var text = factor && Math.abs(factor - 1) > 1e-9 ? s.reduce(scale) : "1";
    var search = s ? s.withScale(address, text) : address.search;
    return address.origin + address.pathname + search;
  }

  // The printable content of a fetched page, as a detached element. `pageUrl` resolves
  // its relative image and link addresses.
  function extract(doc, pageUrl) {
    var main =
      doc.querySelector("main.content") ||
      doc.querySelector("main") ||
      doc.body;
    var box = doc.createElement("div");
    var panel = main.querySelector(".scaler[data-servings]");
    if (panel) {
      ["data-servings", "data-servings-max"].forEach(function (name) {
        if (panel.hasAttribute(name))
          box.setAttribute(name, panel.getAttribute(name));
      });
    }
    each(main.childNodes, function (node) {
      box.appendChild(node.cloneNode(true));
    });
    STRIP.forEach(function (selector) {
      each(box.querySelectorAll(selector), function (el) {
        el.parentNode.removeChild(el);
      });
    });
    // The host page keeps its ids; copies would duplicate them.
    each(box.querySelectorAll("[id]"), function (el) {
      el.removeAttribute("id");
    });
    each(box.querySelectorAll("img"), function (img) {
      if (img.getAttribute("loading") === "lazy")
        img.setAttribute("loading", "eager");
    });
    if (pageUrl) {
      [
        ["img[src]", "src"],
        ["a[href]", "href"],
      ].forEach(function (pair) {
        each(box.querySelectorAll(pair[0]), function (el) {
          try {
            el.setAttribute(
              pair[1],
              new URL(el.getAttribute(pair[1]), pageUrl).href,
            );
          } catch (e) {
            // Leave an address the browser cannot parse as it was.
          }
        });
      });
    }
    return box;
  }

  function mainContent() {
    return document.querySelector("main.content") || document.body;
  }

  function removeBundle() {
    each(document.querySelectorAll(".print-bundle"), function (bundle) {
      bundle.parentNode.removeChild(bundle);
    });
  }

  function paragraph(className, text) {
    var p = document.createElement("p");
    p.className = className;
    p.textContent = text;
    return p;
  }

  // Appends one sheet per entry to the page's content, replacing any earlier bundle.
  function assemble(entries, options) {
    options = options || {};
    var base = options.base || window.location.href;
    var s = scaler();
    removeBundle();
    var bundle = document.createElement("div");
    bundle.className = "print-bundle";
    entries.forEach(function (entry) {
      var section = document.createElement("section");
      section.className = "print-page";
      var address = new URL(entry.url, base).href;
      if (entry.html == null) {
        var name = address.split("?")[0].split("/").pop() || entry.url;
        section.appendChild(
          paragraph(
            "print-note",
            "Couldn't load " + name + "; print it from its own page.",
          ),
        );
      } else {
        var doc = new DOMParser().parseFromString(entry.html, "text/html");
        var box = document.importNode(extract(doc, address), true);
        each(box.attributes, function (attr) {
          section.setAttribute(attr.name, attr.value);
        });
        while (box.firstChild) section.appendChild(box.firstChild);
        if (options.scale && s) s.applyScale(section, options.scale);
      }
      section.appendChild(
        paragraph("print-url", footerUrl(entry.url, base, options.scale)),
      );
      bundle.appendChild(section);
    });
    mainContent().appendChild(bundle);
    return bundle;
  }

  // Resolves once every image under `root` has loaded or failed, or after `timeout` ms.
  function imagesLoaded(root, timeout) {
    var waiting = Array.prototype.filter.call(
      root.querySelectorAll("img"),
      function (img) {
        return !img.complete;
      },
    );
    if (!waiting.length) return Promise.resolve();
    return new Promise(function (resolve) {
      var left = waiting.length;
      var timer = setTimeout(resolve, timeout);
      function one() {
        left -= 1;
        if (!left) {
          clearTimeout(timer);
          resolve();
        }
      }
      waiting.forEach(function (img) {
        img.addEventListener("load", one, { once: true });
        img.addEventListener("error", one, { once: true });
      });
    });
  }

  // Fetches `urls`, appends them to the page, prints, and tidies up afterwards.
  function printBundle(urls, options) {
    options = options || {};
    return prefetch(urls, options).then(function (entries) {
      var bundle = assemble(entries, options);
      return imagesLoaded(
        bundle,
        options.timeout == null ? IMAGE_TIMEOUT : options.timeout,
      ).then(function () {
        window.addEventListener("afterprint", removeBundle, { once: true });
        window.print();
      });
    });
  }

  // ------------------------------------------------------------------ page wiring
  // The page's own address (including ?scale=), printed at the bottom of the sheet.
  // Only the page's own line: each bundled sheet carries its own address.
  function stampAddress() {
    var main = mainContent();
    var line = null;
    var bundle = null;
    each(main.children, function (child) {
      if (child.classList.contains("print-url")) line = child;
      if (child.classList.contains("print-bundle")) bundle = child;
    });
    if (!line) {
      line = paragraph("print-url", "");
      main.insertBefore(line, bundle);
    }
    var here = new URL(window.location.href);
    line.textContent = here.origin + here.pathname + here.search;
  }

  function init() {
    var bars = document.querySelectorAll(".print-bar");
    if (!bars.length) return;
    // Pages opened from files cannot fetch each other, so the option needs a server.
    var served = /^https?:$/.test(window.location.protocol);
    var extras = [];
    each(bars, function (bar) {
      var button = bar.querySelector(".print-button");
      if (!button) return;
      var pages = pageList(bar.getAttribute("data-print-pages"));
      var label = bar.querySelector(".print-with");
      var toggle = label && label.querySelector("input[name=print-with]");
      var withPages = Boolean(served && pages.length && toggle);
      if (withPages) {
        label.hidden = false;
        extras.push({ toggle: toggle, pages: pages });
        var warm = function () {
          if (toggle.checked) prefetch(pages);
        };
        toggle.addEventListener("change", warm);
        warm(); // the browser may restore a ticked box
      }
      button.addEventListener("click", function () {
        stampAddress();
        if (!withPages || !toggle.checked) {
          window.print();
          return;
        }
        button.disabled = true;
        printBundle(pages, { scale: currentScale() }).then(
          function () {
            button.disabled = false;
          },
          function () {
            button.disabled = false;
            removeBundle();
            window.print();
          },
        );
      });
      bar.hidden = false;
    });
    // Also covers printing from the browser menu or a keyboard shortcut.
    window.addEventListener("beforeprint", function () {
      stampAddress();
      if (document.querySelector(".print-bundle")) return;
      extras.some(function (extra) {
        if (!extra.toggle.checked) return false;
        var entries = cached(extra.pages);
        if (entries) assemble(entries, { scale: currentScale() });
        return true;
      });
    });
    window.addEventListener("afterprint", removeBundle);
  }

  return {
    pageList: pageList,
    prefetch: prefetch,
    footerUrl: footerUrl,
    extract: extract,
    assemble: assemble,
    printBundle: printBundle,
    init: init,
  };
});
