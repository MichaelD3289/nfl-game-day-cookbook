"""Kickoff clock times in styles/website-timeline.js, run through Node.

The website works out each timeline step's clock time in the browser, so the time
rules live in JavaScript. These tests need Node.js and are skipped when it is not
installed.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

import pytest

from nfl_book.project import Project
from nfl_book.website import build_website

SCRIPT = Path(__file__).resolve().parents[2] / "styles" / "website-timeline.js"
NODE = shutil.which("node")
pytestmark = pytest.mark.skipif(NODE is None, reason="Node.js is not installed")


def node(expression: str) -> Any:
    assert NODE is not None
    program = (
        f"const t = require({json.dumps(str(SCRIPT))});\n"
        f"process.stdout.write(JSON.stringify({expression}));"
    )
    result = subprocess.run(
        [NODE, "-e", program], capture_output=True, text=True, check=True, timeout=30
    )
    return json.loads(result.stdout)


def test_clock_times_read_the_same_in_every_locale() -> None:
    assert node("[0, 720, 985, 1439].map(t.formatClock)") == [
        "12:00 AM",
        "12:00 PM",
        "4:25 PM",
        "11:59 PM",
    ]


def test_kickoff_accepts_the_time_input_formats_only() -> None:
    values = ["16:25", "16:25:00", "00:00", "23:59", "24:00", "4:25 PM", "", "16:60", "1625"]
    assert node(f"{json.dumps(values)}.map(t.parseKickoff)") == [
        985,
        985,
        0,
        1439,
        None,
        None,
        None,
        None,
        None,
    ]


def test_steps_before_midnight_name_the_day() -> None:
    assert node(
        "[t.clockFor(985, -240), t.clockFor(985, 0), t.clockFor(60, -240),"
        " t.clockFor(60, -60), t.clockFor(60, -1500), t.clockFor(60, -1560),"
        " t.clockFor(60, -3000)]"
    ) == [
        "12:25 PM",
        "4:25 PM",
        "9:00 PM (day before)",
        "12:00 AM",
        "12:00 AM (day before)",
        "11:00 PM (2 days before)",
        "11:00 PM (3 days before)",
    ]


def test_clock_times_from_generated_markup(fixture_book: Project) -> None:
    site = build_website(fixture_book, render=False).document.parent
    page = (site / "menus-fast-day-1.qmd").read_text()
    offsets = [int(value) for value in re.findall(r'data-offset-minutes="(-?\d+)"', page)]
    assert offsets == [-90, -30, 0]
    kickoff = node('t.parseKickoff("13:00")')
    assert node(f"{json.dumps(offsets)}.map(o => t.clockFor({kickoff}, o))") == [
        "11:30 AM",
        "12:30 PM",
        "1:00 PM",
    ]
