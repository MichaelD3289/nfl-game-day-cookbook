"""Render browser findings using the book's source-aware Diagnostics format."""

import argparse
import json
import subprocess
from pathlib import Path

from nfl_book.errors import Diagnostics


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", type=Path)
    parser.add_argument("--report", type=Path, default=Path("website-reports/accessibility.json"))
    parser.add_argument(
        "--performance", action="store_true", help="Run local Lighthouse CI budgets"
    )
    args = parser.parse_args()
    args.report.parent.mkdir(parents=True, exist_ok=True)
    diags = Diagnostics()
    script = Path(__file__).with_name(
        "website-performance.js" if args.performance else "website-audit.js"
    )
    try:
        result = subprocess.run(
            ["node", str(script), str(args.site), str(args.report)], check=False, timeout=900
        )
        report = json.loads(args.report.read_text())
        for item in report["findings"]:
            add = diags.error if item["severity"] == "error" else diags.warning
            add(item["code"], f"{item.get('route', '')}: {item['message']}", Path(item["source"]))
        if result.returncode and diags.ok:
            diags.error("browser", f"Browser audit exited {result.returncode}", script)
    except (OSError, ValueError, KeyError, subprocess.TimeoutExpired) as exc:
        diags.error("browser", str(exc), script)
    for diagnostic in diags:
        print(diagnostic.format())
    return 0 if diags.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
