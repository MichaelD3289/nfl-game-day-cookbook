"""Kickoff timeline times: parsing, labels, ordering."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from nfl_book.timeline import (
    HALFTIME,
    KICKOFF,
    MAX_STEPS,
    MAX_TASK_LENGTH,
    Offset,
    check_at,
    check_order,
    parse_at,
)


@dataclass(frozen=True)
class Step:
    at: str


@pytest.mark.parametrize(
    ("text", "minutes", "clock", "label"),
    [
        ("-1d", -1440, False, "Day before"),
        ("-2d", -2880, False, "2 days before"),
        ("-7d", -10080, False, "7 days before"),
        ("-4h", -240, True, "4 hr before"),
        ("-1h", -60, True, "1 hr before"),
        ("-23h", -1380, True, "23 hr before"),
        ("-30m", -30, True, "30 min before"),
        ("-59m", -59, True, "59 min before"),
        ("-1h30m", -90, True, "1 hr 30 min before"),
        ("-23h59m", -1439, True, "23 hr 59 min before"),
        ("kickoff", 0, True, "Kickoff"),
    ],
)
def test_parse_at(text: str, minutes: int, clock: bool, label: str) -> None:
    assert parse_at(text) == Offset(text, minutes, clock, label, minutes)
    assert check_at(text) == text


def test_halftime_has_a_label_but_no_clock_time() -> None:
    offset = parse_at(HALFTIME)
    assert offset is not None
    assert offset.minutes is None
    assert offset.clock is False
    assert offset.label == "Halftime"
    assert offset.order > 0


def test_limits() -> None:
    assert KICKOFF == "kickoff"
    assert MAX_STEPS == 6
    assert MAX_TASK_LENGTH == 80


@pytest.mark.parametrize(
    "text",
    [
        "",
        "-",
        "-0m",
        "-0h",
        "-0d",
        "-01h",
        "-05m",
        "-90m",
        "-60m",
        "-24h",
        "-8d",
        "-1d4h",
        "-1h0m",
        "-30m1h",
        "+30m",
        "4h",
        "30m",
        "-4H",
        "-1D",
        " -4h",
        "-4h ",
        "Kickoff",
        "KICKOFF",
        "Halftime",
        "-1.5h",
        "-1 h",
        "-1hr",
        "-30min",
    ],
)
def test_rejects(text: str) -> None:
    assert parse_at(text) is None
    with pytest.raises(ValueError, match="-1d") as info:
        check_at(text)
    assert "kickoff" in str(info.value)
    assert "halftime" in str(info.value)


def test_sort_order() -> None:
    times = ["halftime", "-30m", "kickoff", "-1d", "-4h", "-2d", "-1h30m"]
    offsets = [parse_at(t) for t in times]
    assert all(offsets)
    ordered = sorted((o for o in offsets if o), key=lambda o: o.order)
    assert [o.at for o in ordered] == ["-2d", "-1d", "-4h", "-1h30m", "-30m", "kickoff", "halftime"]


def test_check_order_accepts_equal_times() -> None:
    steps = [Step("-1d"), Step("-30m"), Step("-30m"), Step("kickoff"), Step("halftime")]
    assert check_order(steps) == steps


def test_check_order_names_the_out_of_order_step() -> None:
    steps = [Step("-1d"), Step("-30m"), Step("-4h")]
    with pytest.raises(ValueError) as info:
        check_order(steps)
    assert str(info.value) == (
        "steps must be in time order: "
        "step 2 (-4h) is earlier than step 1 (-30m) but listed after it"
    )
