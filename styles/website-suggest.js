// Anonymous suggestion form: posts to the Apps Script web app in data/book.yml
// (suggestion_form_url), which files the GitHub issue. See docs/website-suggestions.md.
(function () {
  "use strict";

  var KINDS = {
    edit: {
      heading: "Suggest an edit",
      fields: [
        { id: "item", label: "Recipe or component", readonly: true },
        { id: "change", label: "What should change?", multiline: true, required: true,
          hint: "Even a single ingredient, amount, or step is helpful." },
        { id: "why", label: "Why? (optional)", multiline: true,
          hint: "A source, your cooking experience, or local knowledge." }
      ]
    },
    recipe: {
      heading: "Suggest a recipe",
      fields: [
        { id: "team", label: "Team", required: true },
        { id: "dish", label: "Dish name or idea", required: true,
          hint: "A rough description is fine." },
        { id: "details", label: "Anything else? (optional)", multiline: true }
      ]
    },
    component: {
      heading: "Suggest a Make It or Buy It component",
      fields: [
        { id: "name", label: "Component name or idea", required: true },
        { id: "details", label: "Anything else? (optional)", multiline: true }
      ]
    },
    menu: {
      heading: "Suggest a game-day menu",
      fields: [
        { id: "idea", label: "Menu idea", multiline: true, required: true,
          hint: "The teams, matchup, or occasion, and any dishes you have in mind." },
        { id: "details", label: "Anything else? (optional)", multiline: true }
      ]
    },
    "dish-off": {
      heading: "Suggest a division dish-off",
      fields: [
        { id: "division", label: "Division", readonly: true },
        { id: "idea", label: "Dish-off idea", multiline: true, required: true },
        { id: "details", label: "Anything else? (optional)", multiline: true }
      ]
    }
  };

  var FROM = [
    { id: "name", label: "Your name or nickname (optional)",
      hint: "Shown publicly on the suggestion so we can credit you." },
    { id: "github", label: "GitHub username (optional)",
      hint: "Linked on the suggestion. We can't verify it, so it isn't @mentioned." },
    { id: "email", label: "Email (optional)", type: "email",
      hint: "Never published. Sent privately to the maintainer in case of questions." }
  ];

  function el(tag, attrs, text) {
    var node = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (key) { node.setAttribute(key, attrs[key]); });
    if (text) node.textContent = text;
    return node;
  }

  function field(prefix, spec, value) {
    var id = "suggest-" + prefix + "-" + spec.id;
    var wrap = el("div", { class: "suggest-field" });
    wrap.appendChild(el("label", { for: id }, spec.label));
    var input = el(spec.multiline ? "textarea" : "input", {
      id: id, name: prefix + "-" + spec.id, maxlength: spec.multiline ? "5000" : "200"
    });
    if (!spec.multiline) input.type = spec.type || "text";
    if (spec.multiline) input.rows = 3;
    if (spec.required) input.required = true;
    if (spec.readonly) input.readOnly = true;
    if (value) input.value = value;
    wrap.appendChild(input);
    if (spec.hint) wrap.appendChild(el("small", {}, spec.hint));
    return wrap;
  }

  function open(button) {
    var box = button.closest(".suggest");
    var kind = box.getAttribute("data-kind");
    var spec = KINDS[kind];
    var context = JSON.parse(box.getAttribute("data-fields") || "{}");
    var github = box.querySelector(".suggest-github").href;

    var dialog = el("dialog", { class: "suggest-dialog", "aria-labelledby": "suggest-title" });
    var form = el("form", { method: "dialog" });
    form.appendChild(el("h2", { id: "suggest-title" }, spec.heading));
    form.appendChild(el("p", { class: "suggest-note" },
      "No account needed. Your suggestion becomes a public GitHub issue that we research " +
      "before changing the cookbook."));
    var about = el("fieldset", {});
    about.appendChild(el("legend", {}, "Your suggestion"));
    spec.fields.forEach(function (f) {
      if (f.readonly && !context[f.id]) return;
      about.appendChild(field("s", f, context[f.id]));
    });
    form.appendChild(about);
    var from = el("fieldset", {});
    from.appendChild(el("legend", {}, "About you (all optional)"));
    FROM.forEach(function (f) { from.appendChild(field("f", f, "")); });
    form.appendChild(from);
    // Honeypot: hidden from people, filled in by naive bots.
    var trap = el("div", { class: "suggest-trap", "aria-hidden": "true" });
    trap.appendChild(el("input", { name: "website", tabindex: "-1", autocomplete: "off" }));
    form.appendChild(trap);
    var status = el("p", { class: "suggest-status", role: "status" });
    form.appendChild(status);
    var actions = el("div", { class: "suggest-buttons" });
    var cancel = el("button", { type: "button", class: "suggest-cancel" }, "Cancel");
    var send = el("button", { type: "submit", class: "suggest-send" }, "Send suggestion");
    actions.appendChild(cancel);
    actions.appendChild(send);
    form.appendChild(actions);
    dialog.appendChild(form);
    document.body.appendChild(dialog);

    cancel.addEventListener("click", function () { dialog.close(); });
    dialog.addEventListener("close", function () { dialog.remove(); button.focus(); });

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var fields = {};
      Object.keys(context).forEach(function (key) { fields[key] = context[key]; });
      spec.fields.forEach(function (f) {
        var input = form.elements.namedItem("s-" + f.id);
        if (input) fields[f.id] = input.value.trim();
      });
      var who = {};
      FROM.forEach(function (f) {
        who[f.id] = form.elements.namedItem("f-" + f.id).value.trim();
      });
      var payload = {
        kind: kind,
        fields: fields,
        from: who,
        page: window.location.href,
        website: form.elements.namedItem("website").value
      };
      send.disabled = true;
      status.textContent = "Sending…";
      // A text/plain body keeps this a simple request (no CORS preflight).
      fetch(button.getAttribute("data-endpoint"), {
        method: "POST",
        body: JSON.stringify(payload)
      })
        .then(function (response) { return response.json(); })
        .then(function (result) {
          if (!result.ok) throw new Error(result.error || "failed");
          form.replaceChildren(
            el("h2", { id: "suggest-title" }, "Thanks!"),
            el("p", {}, "Your suggestion was sent. We'll research it before updating the cookbook.")
          );
          if (result.url) {
            var link = el("a", { href: result.url, target: "_blank", rel: "noopener" },
              "View your suggestion on GitHub");
            form.appendChild(el("p")).appendChild(link);
          }
          var done = el("button", { type: "button", class: "suggest-send" }, "Close");
          done.addEventListener("click", function () { dialog.close(); });
          form.appendChild(done);
        })
        .catch(function () {
          send.disabled = false;
          status.replaceChildren(
            document.createTextNode("Sorry, that didn't go through. Try again, or "),
            el("a", { href: github, target: "_blank", rel: "noopener" }, "suggest on GitHub"),
            document.createTextNode(" instead.")
          );
        });
    });

    dialog.showModal();
    var first = form.querySelector("input:not([readonly]), textarea");
    if (first) first.focus();
  }

  document.querySelectorAll(".suggest-open").forEach(function (button) {
    if (!KINDS[button.closest(".suggest").getAttribute("data-kind")]) return;
    button.hidden = false;
    button.addEventListener("click", function () { open(button); });
  });
})();
