const assert = require("node:assert/strict");
const { test } = require("node:test");
const {
  performanceConfig,
  offlineProxy,
} = require("../../scripts/website-performance.js");
test("performance budgets warn and reports stay local", () => {
  const config = performanceConfig(
    ["http://127.0.0.1:1234/index.html"],
    "/tmp/test-reports",
    "/tmp/test-chrome",
    "http://127.0.0.1:4567",
  );
  assert.equal(config.ci.collect.chromePath, "/tmp/test-chrome");
  assert.equal(config.ci.collect.method, "node");
  assert.equal(config.ci.upload.target, "filesystem");
  assert.deepEqual(config.ci.assert.assertions["resource-summary:image:size"], [
    "warn",
    { maxNumericValue: 512000 },
  ]);
  assert.deepEqual(
    config.ci.assert.assertions["resource-summary:script:size"],
    ["warn", { maxNumericValue: 512000 }],
  );
  assert.deepEqual(config.ci.assert.assertions["largest-contentful-paint"], [
    "warn",
    { maxNumericValue: 2500 },
  ]);
});
test("proxy denies outbound HTTP and HTTPS before connecting", async () => {
  const http = require("node:http");
  const source = http.createServer((_req, res) => res.end("test-local"));
  await new Promise((resolve) => source.listen(0, "127.0.0.1", resolve));
  const origin = `http://127.0.0.1:${source.address().port}`;
  const proxy = await offlineProxy(origin);
  try {
    for (const [method, path] of [
      ["GET", "http://example.invalid/"],
      ["CONNECT", "example.invalid:443"],
      ["GET", "http://127.0.0.1:9999/"],
    ]) {
      const status = await new Promise((resolve, reject) => {
        const req = http.request(proxy.origin, { method, path });
        req.on("response", (r) => {
          r.resume();
          resolve(r.statusCode);
        });
        req.on("connect", (r, socket) => {
          socket.destroy();
          resolve(r.statusCode);
        });
        req.on("error", reject);
        req.end();
      });
      assert.equal(status, 403);
    }
    const body = await new Promise((resolve, reject) => {
      http
        .get(proxy.origin, { path: origin + "/index.html" }, (res) => {
          let text = "";
          res.on("data", (chunk) => (text += chunk));
          res.on("end", () => resolve(text));
        })
        .on("error", reject);
    });
    assert.equal(body, "test-local");
  } finally {
    await proxy.close();
    await new Promise((resolve) => source.close(resolve));
  }
});

test("missing audit measurements fail while actual budget overruns warn", () => {
  const { budgetFindings } = require("../../scripts/website-performance.js");
  assert.equal(
    budgetFindings([
      {
        passed: false,
        name: "maxNumericValue",
        actual: 600000,
        expected: 512000,
      },
    ])[0].severity,
    "warning",
  );
  assert.equal(
    budgetFindings([
      {
        passed: false,
        name: "maxNumericValue",
        actual: null,
        expected: 2500,
        message: "Audit failed",
      },
    ])[0].severity,
    "error",
  );
  assert.throws(() => budgetFindings([]));
});

test("Lighthouse collection errors fail instead of becoming budget warnings", () => {
  const { validateReports } = require("../../scripts/website-performance.js");
  const url = "http://127.0.0.1:1234/recipe-test-wings.html";
  validateReports([{ requestedUrl: url, finalDisplayedUrl: url }], [url]);
  assert.throws(() => validateReports([], [url]));
  assert.throws(() =>
    validateReports(
      [
        {
          requestedUrl: url,
          finalDisplayedUrl: url,
          runtimeError: { message: "page failed" },
        },
      ],
      [url],
    ),
  );
  assert.throws(() =>
    validateReports(
      [
        {
          requestedUrl: url,
          finalDisplayedUrl: "chrome-error://chromewebdata/",
        },
      ],
      [url],
    ),
  );
});
