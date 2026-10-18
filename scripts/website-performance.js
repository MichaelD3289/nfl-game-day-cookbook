/* Lighthouse CI stays local; only budget misses are warning-only. */
const fs = require("node:fs/promises");
const path = require("node:path");
const http = require("node:http");
const { spawn } = require("node:child_process");
const {
  serve,
  localOnly,
  representativeRoutes,
} = require("./website-audit.js");

async function offlineProxy(origin) {
  const server = http.createServer((req, res) => {
    let allowed = false;
    try {
      allowed = localOnly(origin, req.url);
    } catch {}
    if (!allowed) {
      res.writeHead(403).end();
      return;
    }
    const upstream = http.request(
      req.url,
      { method: req.method, headers: req.headers },
      (response) => {
        res.writeHead(response.statusCode, response.headers);
        response.pipe(res);
      },
    );
    upstream.on("error", () => res.writeHead(502).end());
    req.pipe(upstream);
  });
  // Chrome may reset rejected background connections before reading the response.
  server.on("connection", (socket) =>
    socket.on("error", () => socket.destroy()),
  );
  server.on("connect", (_req, socket) => {
    socket.end("HTTP/1.1 403 Forbidden\r\nConnection: close\r\n\r\n");
  });
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  return {
    origin: `http://127.0.0.1:${server.address().port}`,
    close: () => new Promise((resolve) => server.close(resolve)),
  };
}
function performanceConfig(urls, directory, chrome, proxy) {
  return {
    ci: {
      collect: {
        method: "node",
        url: urls,
        numberOfRuns: 1,
        chromePath: chrome,
        settings: {
          onlyCategories: ["performance"],
          chromeFlags: `--headless --no-sandbox --disable-quic --proxy-server=${proxy} --proxy-bypass-list=<-loopback> --host-resolver-rules="MAP * ~NOTFOUND, EXCLUDE 127.0.0.1"`,
        },
      },
      assert: {
        assertions: {
          "resource-summary:image:size": [
            "warn",
            { maxNumericValue: 500 * 1024 },
          ],
          "resource-summary:script:size": [
            "warn",
            { maxNumericValue: 500 * 1024 },
          ],
          "largest-contentful-paint": ["warn", { maxNumericValue: 2500 }],
        },
      },
      upload: {
        target: "filesystem",
        outputDir: path.join(directory, "reports"),
      },
    },
  };
}
async function run(site, reportFile) {
  const directory = path.resolve(path.dirname(reportFile));
  await fs.mkdir(directory, { recursive: true });
  const routes = representativeRoutes(await fs.readdir(site));
  if (routes.some((r) => !r.file))
    throw new Error("Missing representative site pages");
  const server = await serve(site);
  let proxy;
  try {
    proxy = await offlineProxy(server.origin);
    const chrome =
      process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH ||
      require("playwright").chromium.executablePath();
    const config = performanceConfig(
      routes.map((r) => `${server.origin}/${r.file}`),
      directory,
      chrome,
      proxy.origin,
    );
    const configPath = path.join(directory, "lighthouserc.json");
    await fs.writeFile(configPath, JSON.stringify(config, null, 2));
    const cli = require.resolve("@lhci/cli/src/cli.js");
    for (const command of ["collect", "assert", "upload"]) {
      const code = await new Promise((resolve, reject) => {
        const child = spawn(
          process.execPath,
          [cli, command, `--config=${configPath}`],
          {
            cwd: directory,
            stdio: "inherit",
            env: { ...process.env, CHROME_PATH: chrome },
          },
        );
        child.on("error", reject);
        child.on("exit", resolve);
      });
      if (code !== 0)
        throw new Error(`Lighthouse CI ${command} failed (${code})`);
    }
    const reportDir = path.join(directory, ".lighthouseci");
    const reportFiles = (await fs.readdir(reportDir)).filter((f) =>
      /^lhr-.*\.json$/.test(f),
    );
    validateReports(
      await Promise.all(
        reportFiles.map(async (f) =>
          JSON.parse(await fs.readFile(path.join(reportDir, f), "utf8")),
        ),
      ),
      config.ci.collect.url,
    );
    const assertions = JSON.parse(
      await fs.readFile(
        path.join(directory, ".lighthouseci", "assertion-results.json"),
        "utf8",
      ),
    );
    return { findings: budgetFindings(assertions), routes };
  } finally {
    if (proxy) await proxy.close();
    await server.close();
  }
}
function validateReports(reports, urls) {
  if (reports.length !== urls.length)
    throw new Error("Missing Lighthouse page reports");
  for (const url of urls) {
    const report = reports.find((r) => r.requestedUrl === url);
    if (!report || report.runtimeError || report.finalDisplayedUrl !== url)
      throw new Error(
        `Lighthouse did not successfully load ${url}: ${report?.runtimeError?.message || "missing or redirected report"}`,
      );
  }
}
function budgetFindings(assertions) {
  if (!assertions.length)
    throw new Error("Lighthouse produced no budget results");
  return assertions
    .filter((a) => !a.passed)
    .map((a) => ({
      source: "scripts/website-performance.js",
      code: "performance",
      route: a.url,
      severity:
        Number.isFinite(a.actual) && a.name === "maxNumericValue" && !a.message
          ? "warning"
          : "error",
      message: `${a.auditId}: ${a.message || `${a.actual} exceeds budget ${a.expected}`}`,
    }));
}
module.exports = {
  performanceConfig,
  offlineProxy,
  run,
  budgetFindings,
  validateReports,
};
if (require.main === module) {
  run(process.argv[2], process.argv[3])
    .catch((error) => ({
      findings: [
        {
          source: "scripts/website-performance.js",
          severity: "error",
          code: "performance",
          message: error.message,
        },
      ],
    }))
    .then(async (report) => {
      await fs.writeFile(
        process.argv[3],
        JSON.stringify(report, null, 2) + "\n",
      );
      process.exitCode = report.findings.some((f) => f.severity === "error")
        ? 1
        : 0;
    });
}
