// Print button on the website. The button prints the page as it is shown, so amounts
// scaled by scale.js print scaled. The @media print rules in website.css hide the site
// chrome and lay the page out for paper. Without JavaScript the button stays hidden.
(function () {
  "use strict";

  // The page's own address (including ?scale=), printed at the bottom of the sheet.
  function stampAddress() {
    var main = document.querySelector("main.content") || document.body;
    var line = main.querySelector(".print-url");
    if (!line) {
      line = document.createElement("p");
      line.className = "print-url";
      main.appendChild(line);
    }
    var here = new URL(window.location.href);
    line.textContent = here.origin + here.pathname + here.search;
  }

  function init() {
    var bars = document.querySelectorAll(".print-bar");
    if (!bars.length) return;
    Array.prototype.forEach.call(bars, function (bar) {
      var button = bar.querySelector(".print-button");
      if (!button) return;
      button.addEventListener("click", function () {
        stampAddress();
        window.print();
      });
      bar.hidden = false;
    });
    // Also covers printing from the browser menu or a keyboard shortcut.
    window.addEventListener("beforeprint", stampAddress);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
