// Kickoff timeline on the website. Each menu or dish-off timeline lists its steps
// counted back from kickoff; a step with a clock time carries
// data-offset-minutes="-90". Entering a kickoff time shows each step's clock time.
// Without JavaScript, or with no time entered, only the relative labels show. The
// kickoff is kept in the address as ?kickoff=16:25, so a printed or shared page
// reproduces it. Time rules are tested from tests/unit/test_website_timeline.py
// through Node.
(function (root, factory) {
  "use strict";
  var api = factory();
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  } else {
    root.NflTimeline = api;
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

  var DAY = 24 * 60;

  // "16:25" or "16:25:00" -> minutes after midnight; anything else -> null.
  function parseKickoff(text) {
    var match = /^([01]\d|2[0-3]):([0-5]\d)(?::[0-5]\d)?$/.exec(
      String(text || ""),
    );
    if (!match) return null;
    return Number(match[1]) * 60 + Number(match[2]);
  }

  // Minutes after midnight -> "4:25 PM", the same in every locale.
  function formatClock(minutes) {
    var t = ((Math.round(minutes) % DAY) + DAY) % DAY;
    var hours = Math.floor(t / 60);
    var mins = t % 60;
    var shown = hours % 12 === 0 ? 12 : hours % 12;
    return (
      shown + ":" + (mins < 10 ? "0" : "") + mins + (hours < 12 ? " AM" : " PM")
    );
  }

  // The clock time of a step ``offset`` minutes from a ``kickoff`` (minutes after
  // midnight), naming the day when it falls before kickoff day.
  function clockFor(kickoff, offset) {
    var t = kickoff + offset;
    var text = formatClock(t);
    if (t < 0) {
      var days = Math.ceil(-t / DAY);
      text += days === 1 ? " (day before)" : " (" + days + " days before)";
    }
    return text;
  }

  function withKickoff(url, value) {
    var params = url.search
      .replace(/^\?/, "")
      .split("&")
      .filter(function (p) {
        return p && p.split("=")[0] !== "kickoff";
      });
    if (value) params.push("kickoff=" + value);
    return (params.length ? "?" + params.join("&") : "") + url.hash;
  }

  function pad(n) {
    return (n < 10 ? "0" : "") + n;
  }

  function init() {
    var timelines = document.querySelectorAll(".menu-timeline");
    if (!timelines.length) return;
    var inputs = document.querySelectorAll(
      '.timeline-kickoff input[name="kickoff"]',
    );

    // One kickoff per page: every picker, clock and print line follows it.
    function apply(kickoff, updateAddress) {
      var value =
        kickoff === null
          ? ""
          : pad(Math.floor(kickoff / 60)) + ":" + pad(kickoff % 60);
      Array.prototype.forEach.call(inputs, function (input) {
        if (input.value !== value && parseKickoff(input.value) !== kickoff) {
          input.value = value;
        }
      });
      Array.prototype.forEach.call(timelines, function (timeline) {
        var steps = timeline.querySelectorAll(
          ".timeline-step[data-offset-minutes]",
        );
        Array.prototype.forEach.call(steps, function (step) {
          var clock = step.querySelector(".timeline-clock");
          if (!clock) return;
          var offset = Number(step.getAttribute("data-offset-minutes"));
          if (kickoff === null || isNaN(offset)) {
            clock.textContent = "";
            clock.hidden = true;
          } else {
            clock.textContent = clockFor(kickoff, offset);
            clock.hidden = false;
          }
        });
        var line = timeline.querySelector(".print-kickoff");
        if (line) {
          line.textContent =
            kickoff === null ? "" : "Kickoff " + formatClock(kickoff);
          line.hidden = kickoff === null;
        }
      });
      if (updateAddress && window.history && window.history.replaceState) {
        var here = new URL(window.location.href);
        window.history.replaceState(
          null,
          "",
          here.pathname + withKickoff(here, value),
        );
      }
    }

    Array.prototype.forEach.call(inputs, function (input) {
      input.addEventListener("input", function () {
        apply(parseKickoff(input.value), true);
      });
    });
    Array.prototype.forEach.call(
      document.querySelectorAll(".timeline-kickoff"),
      function (picker) {
        picker.hidden = false;
      },
    );
    var initial = new URLSearchParams(window.location.search).get("kickoff");
    apply(parseKickoff(initial), false);
  }

  return {
    parseKickoff: parseKickoff,
    formatClock: formatClock,
    clockFor: clockFor,
    init: init,
  };
});
