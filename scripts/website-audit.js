/* Local-only, reusable rendered-site checks. Python renders diagnostics for CLI use. */
const fs = require("node:fs/promises");
const path = require("node:path");
const http = require("node:http");

function classify(impact) {
  return ["serious", "critical"].includes(impact) ? "error" : "warning";
}
function localOnly(origin, url) {
  return (
    new URL(url).origin === origin && new URL(origin).hostname === "127.0.0.1"
  );
}
function representativeRoutes(files) {
  const patterns = {
    home: /^index\.html$/,
    recipe: /^recipe-.*\.html$/,
    component: /^component-.*\.html$/,
    menu: /^menus?-.*\.html$/,
    dishoff: /^division-.*\.html$/,
    index: /^index-.*\.html$/,
    versions: /^versions\.html$/,
  };
  return Object.entries(patterns).map(([kind, pattern]) => ({
    kind,
    file: files.sort().find((f) => pattern.test(f)),
  }));
}

async function serve(directory) {
  const root = path.resolve(directory);
  const types = {
    ".html": "text/html",
    ".js": "text/javascript",
    ".css": "text/css",
    ".json": "application/json",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".webp": "image/webp",
    ".woff2": "font/woff2",
  };
  const server = http.createServer(async (req, res) => {
    try {
      const filename = path.resolve(
        root,
        "." + decodeURIComponent(new URL(req.url, "http://localhost").pathname),
      );
      if (!filename.startsWith(root + path.sep)) {
        res.writeHead(403).end();
        return;
      }
      res.setHeader(
        "Content-Type",
        types[path.extname(filename)] || "application/octet-stream",
      );
      res.end(await fs.readFile(filename));
    } catch {
      res.writeHead(404).end();
    }
  });
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  return {
    origin: `http://127.0.0.1:${server.address().port}`,
    close: () => new Promise((resolve) => server.close(resolve)),
  };
}

async function protect(context, origin, blocked) {
  await context.route("**/*", async (route) => {
    if (localOnly(origin, route.request().url())) await route.continue();
    else {
      blocked.push(route.request().url());
      await route.abort("blockedbyclient");
    }
  });
  // WebSockets do not pass through HTTP routing.
  await context.routeWebSocket(/.*/, (socket) => {
    blocked.push(socket.url());
    socket.close();
  });
}

async function audit(directory) {
  const { chromium } = require("playwright");
  const AxeBuilder = require("@axe-core/playwright").default;
  const files = await fs.readdir(directory);
  const report = {
    coverage: [],
    routes: representativeRoutes(files),
    findings: [],
    blockedRequests: [],
  };
  for (const route of report.routes) {
    const marker =
      route.kind === "recipe"
        ? "quick-card"
        : route.kind === "dishoff"
          ? "dishoff-"
          : null;
    if (marker)
      for (const file of files.sort()) {
        if (
          file.startsWith(route.kind === "recipe" ? "recipe-" : "division-") &&
          file.endsWith(".html") &&
          (await fs.readFile(path.join(directory, file), "utf8")).includes(
            marker,
          )
        ) {
          route.file = file;
          break;
        }
      }
  }
  const server = await serve(directory);
  let browser;
  const sources = { home: "cover", menu: "game-day-menu", dishoff: "division" };
  const finding = (route, code, message, severity = "error", source) =>
    report.findings.push({
      source:
        source ||
        (route.kind === "versions"
          ? "src/nfl_book/website.py"
          : `templates/website/${sources[route.kind] || route.kind}.qmd.j2`),
      route: route.file,
      code,
      message,
      severity,
    });
  try {
    browser = await chromium.launch({
      executablePath:
        process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH || undefined,
    });
    for (const viewport of [
      { width: 1440, height: 1000 },
      { width: 390, height: 844 },
    ]) {
      const context = await browser.newContext({
        viewport,
        serviceWorkers: "block",
      });
      await protect(context, server.origin, report.blockedRequests);
      const page = await context.newPage();
      page.setDefaultTimeout(5000);
      for (const route of report.routes) {
        if (!route.file) {
          finding(route, "route", `Missing representative ${route.kind} page`);
          continue;
        }
        try {
          const response = await page.goto(`${server.origin}/${route.file}`);
          if (!response.ok()) throw new Error(`HTTP ${response.status()}`);
          const axe = await new AxeBuilder({ page }).analyze();
          for (const violation of axe.violations)
            finding(
              route,
              violation.id,
              `${viewport.width}px: ${violation.help}; ${violation.nodes.map((n) => n.target.join(" ")).join(", ")}`,
              classify(violation.impact),
              violation.id === "color-contrast"
                ? "styles/website.css"
                : undefined,
            );
          if (
            await page.evaluate(
              () =>
                document.documentElement.scrollWidth > window.innerWidth + 1,
            )
          )
            finding(
              route,
              "overflow",
              `${viewport.width}px horizontal overflow`,
              "error",
              "styles/website.css",
            );
          // Start from the document so this tests actual keyboard reachability.
          await page.evaluate(() => document.activeElement.blur());
          await page.keyboard.press("Tab");
          if (
            !(await page.evaluate(
              () => document.activeElement !== document.body,
            ))
          )
            finding(route, "keyboard", "Tab does not reach a control");
          if (route.kind === "recipe")
            await checkRecipe(
              page,
              route,
              finding,
              AxeBuilder,
              report.coverage,
            );
        } catch (error) {
          finding(route, "browser", `${viewport.width}px: ${error.message}`);
        }
      }
      await context.close();
    }
    report.blockedRequests = [...new Set(report.blockedRequests)];
    for (const url of report.blockedRequests)
      finding(
        { kind: "home", file: "index.html" },
        "outbound-request",
        `Blocked external browser request: ${url}`,
        "error",
        "src/nfl_book/website.py",
      );
  } finally {
    if (browser) await browser.close();
    await server.close();
  }
  return report;
}

async function checkRecipe(page, route, finding, AxeBuilder, coverage) {
  let scaled = false;
  const control = page.locator('.scaler button[data-factor="2"]');
  if (
    (await control.count()) &&
    (await page.locator(".ingredients .qty").count())
  ) {
    scaled = true;
    coverage.push("scaling");
    await control.focus();
    const focus = await control.evaluate((el) => {
      const s = getComputedStyle(el);
      return (
        (s.outlineStyle !== "none" && parseFloat(s.outlineWidth) > 0) ||
        s.boxShadow !== "none"
      );
    });
    if (!focus)
      finding(
        route,
        "focus",
        "Scaling button has no visible keyboard focus",
        "error",
        "styles/website.css",
      );
    const servings = page.locator('input[name="servings"]');
    if (await servings.count()) {
      const base = Number(
        await page.locator(".scaler").getAttribute("data-servings"),
      );
      await servings.fill(String(base * 2));
      await page.waitForURL(/scale=2/);
      const status = page.locator(".scale-status");
      if (
        !page.url().includes("scale=2") ||
        !(await status.innerText()).includes("Scaled") ||
        (await status.getAttribute("aria-live")) !== "polite"
      )
        finding(
          route,
          "servings",
          "Servings input did not update scale and live status",
        );
      await page.locator('.scaler button[data-factor="1"]').click();
      await control.focus();
    }
    const original = await page.locator(".ingredients .qty").allTextContents();
    await page.keyboard.press("Enter");
    await page.waitForURL(/scale=2/);
    if (
      (await control.getAttribute("aria-pressed")) !== "true" ||
      !page.url().includes("scale=2")
    )
      finding(
        route,
        "scaling",
        "Keyboard scaling did not update pressed state and URL",
      );
    if (
      JSON.stringify(original) ===
      JSON.stringify(await page.locator(".ingredients .qty").allTextContents())
    )
      finding(route, "scaling", "Scaling did not change ingredient quantities");
  }
  const quick = page.locator(".quick-card a[data-carry-scale]").first();
  if (await quick.count()) {
    coverage.push("quick-options");
    if (scaled && !(await quick.getAttribute("href")).includes("scale=2"))
      finding(route, "quick-options", "Q link lost scale");
    await quick.focus();
    await Promise.all([
      page.waitForURL(/component-/),
      page.keyboard.press("Enter"),
    ]);
    if (
      !page.url().includes("component-") ||
      (scaled && !page.url().includes("scale=2"))
    )
      finding(
        route,
        "quick-options",
        "Q link did not navigate to scaled component",
      );
    await page.goBack();
  }
  const open = page.locator(".suggest-open").first();
  if (await open.count()) {
    coverage.push("suggestion");
    await open.focus();
    await page.keyboard.press("Enter");
    await page.locator("dialog[open]").waitFor();
    if (
      !(await page.evaluate(
        () => document.activeElement.closest("dialog") !== null,
      ))
    )
      finding(route, "suggestion-focus", "Dialog did not receive focus");
    // Native dialogs may Tab into browser chrome (activeElement is body),
    // but must never focus background page controls.
    for (let i = 0; i < 12; i++) {
      await page.keyboard.press("Tab");
      if (
        !(await page.evaluate(
          () =>
            document.activeElement === document.body ||
            document.activeElement.closest("dialog") !== null,
        ))
      )
        finding(route, "suggestion-focus", "Tab escaped modal dialog");
    }
    for (const violation of (await new AxeBuilder({ page }).analyze())
      .violations)
      finding(
        route,
        violation.id,
        `Suggestion dialog: ${violation.help}; ${violation.nodes.map((n) => n.target.join(" ")).join(", ")}`,
        classify(violation.impact),
      );
    await page.keyboard.press("Escape");
    if (!(await open.evaluate((el) => el === document.activeElement)))
      finding(route, "suggestion-focus", "Escape did not restore opener focus");
  }
  coverage.push("print");
  await page.evaluate(() => {
    window.__printed = false;
    window.print = () => {
      window.__printed = true;
    };
  });
  await page.locator(".print-button").focus();
  await page.keyboard.press("Enter");
  await page.waitForFunction(() => window.__printed === true);
  if (!(await page.evaluate(() => window.__printed)))
    finding(route, "print", "Keyboard print did not invoke print");
  const ingredients = await page.locator(".ingredients ul").allTextContents();
  const instructions = await page.locator(".instructions").innerText();
  await page.emulateMedia({ media: "print" });
  for (const selector of [".ingredients", ".instructions", ".print-url"])
    if (!(await page.locator(selector).isVisible()))
      finding(
        route,
        "print",
        `${selector} is missing in print`,
        "error",
        "styles/website.css",
      );
  if (
    JSON.stringify(ingredients) !==
      JSON.stringify(await page.locator(".ingredients ul").allTextContents()) ||
    instructions !== (await page.locator(".instructions").innerText())
  )
    finding(
      route,
      "print",
      "Print changed recipe content",
      "error",
      "styles/website.css",
    );
  for (const selector of [
    ".ingredients .qty",
    ".quick-card",
    ...(scaled ? [".print-scale"] : []),
  ]) {
    for (const element of await page.locator(selector).all())
      if (!(await element.isVisible()))
        finding(
          route,
          "print",
          `${selector} is hidden in print`,
          "error",
          "styles/website.css",
        );
  }
  if (await page.locator(".print-button").isVisible())
    finding(
      route,
      "print",
      "Print control remains on printed page",
      "error",
      "styles/website.css",
    );
  await page.emulateMedia({ media: "screen" });
}
module.exports = {
  audit,
  classify,
  localOnly,
  representativeRoutes,
  serve,
  protect,
};
if (require.main === module) {
  audit(process.argv[2])
    .then(async (report) => {
      await fs.writeFile(
        process.argv[3],
        JSON.stringify(report, null, 2) + "\n",
      );
      process.exitCode = report.findings.some((f) => f.severity === "error")
        ? 1
        : 0;
    })
    .catch(async (error) => {
      await fs.writeFile(
        process.argv[3],
        JSON.stringify({
          routes: [],
          blockedRequests: [],
          findings: [
            {
              source: "scripts/website-audit.js",
              severity: "error",
              code: "browser",
              message: error.message,
            },
          ],
        }),
      );
      process.exitCode = 1;
    });
}
