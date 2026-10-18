const assert = require("node:assert/strict");
const { test } = require("node:test");
const {
  classify,
  localOnly,
  representativeRoutes,
} = require("../../scripts/website-audit.js");

test("serious and critical violations fail; lesser impacts remain warnings", () => {
  assert.deepEqual(["minor", "moderate", "serious", "critical"].map(classify), [
    "warning",
    "warning",
    "error",
    "error",
  ]);
});
test("browser requests are limited to the exact local audit origin", () => {
  const origin = "http://127.0.0.1:8765";
  assert.equal(localOnly(origin, `${origin}/recipe-test-wings.html`), true);
  for (const url of [
    "https://example.invalid/submit",
    "http://127.0.0.1:9999/",
    "http://localhost:8765/",
  ])
    assert.equal(localOnly(origin, url), false);
});
test("representatives are discovered from the rendered files without production ids", () => {
  const routes = representativeRoutes([
    "index.html",
    "recipe-test-wings.html",
    "component-test-sauce.html",
    "menu-test-menu.html",
    "division-afc-east.html",
    "index-course.html",
    "versions.html",
  ]);
  assert.equal(routes.length, 7);
  assert.equal(
    routes.find((r) => r.kind === "recipe").file,
    "recipe-test-wings.html",
  );
});

test("real browser detects a serious fixture defect and blocks outbound fetch", async () => {
  const { chromium } = require("playwright");
  const AxeBuilder = require("@axe-core/playwright").default;
  const { protect } = require("../../scripts/website-audit.js");
  const browser = await chromium.launch({
    executablePath:
      process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH || undefined,
  });
  try {
    const context = await browser.newContext({ serviceWorkers: "block" });
    const blocked = [];
    await protect(context, "http://127.0.0.1:8765", blocked);
    const page = await context.newPage();
    await page.setContent(
      '<html lang="en"><title>Synthetic test control</title><main><h1>Test recipe</h1><button></button></main></html>',
    );
    const axe = await new AxeBuilder({ page }).analyze();
    const defect = axe.violations.find((v) => v.id === "button-name");
    assert.ok(defect, "unlabelled synthetic control must be detected");
    assert.equal(classify(defect.impact), "error");
    assert.equal(
      await page.evaluate(async () => {
        try {
          await fetch("https://example.invalid/test-no-network");
          return false;
        } catch {
          return true;
        }
      }),
      true,
    );
    assert.deepEqual(blocked, ["https://example.invalid/test-no-network"]);
  } finally {
    await browser.close();
  }
});

test("missing site fails promptly without leaving an HTTP server running", () => {
  const { spawnSync } = require("node:child_process");
  const fs = require("node:fs");
  const os = require("node:os");
  const path = require("node:path");
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), "test-audit-"));
  try {
    const report = path.join(temporary, "report.json");
    const result = spawnSync(
      process.execPath,
      [
        path.resolve(__dirname, "../../scripts/website-audit.js"),
        path.join(temporary, "test-missing"),
        report,
      ],
      { timeout: 5000 },
    );
    assert.equal(result.error, undefined);
    assert.equal(result.status, 1);
    assert.equal(
      JSON.parse(fs.readFileSync(report)).findings[0].severity,
      "error",
    );
  } finally {
    fs.rmSync(temporary, { recursive: true });
  }
});
