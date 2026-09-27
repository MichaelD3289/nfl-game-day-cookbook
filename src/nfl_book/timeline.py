"""Kickoff timelines: when each game-day task happens, counted back from kickoff.

Menus and dish-offs may list ``timeline`` steps whose ``at`` is one strict, lowercase
spelling per time:

* ``-Nd`` (N 1-7): a whole day before, with no clock time;
* ``-Nh`` (N 1-23), ``-Nm`` (N 1-59) or ``-NhMm``: hours and minutes before kickoff;
* ``kickoff`` and ``halftime``. Halftime has a label but no fixed clock time.

This module is pure: it parses and labels times and checks their order, and knows
nothing about menus or recipes.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol, TypeVar

KICKOFF = "kickoff"
HALFTIME = "halftime"
MAX_STEPS = 6
MAX_TASK_LENGTH = 80

MAX_DAYS = 7
MAX_HOURS = 23
MAX_MINUTES = 59
HALFTIME_ORDER = 1_000_000
"""Sort key for halftime: after kickoff and anything counted back from it."""

ALLOWED_FORMS = (
    "days -1d to -7d, hours -1h to -23h, minutes -1m to -59m, "
    "hours and minutes such as -1h30m, kickoff or halftime"
)

_AT_RE = re.compile(r"^-(?:([1-9]\d*)d|(?:([1-9]\d*)h)?(?:([1-9]\d*)m)?)$")


@dataclass(frozen=True)
class Offset:
    """A parsed ``at``: minutes from kickoff (negative before), or ``None`` for halftime.

    ``clock`` says whether the time maps to a clock time once kickoff is known (whole
    days and halftime do not). ``order`` is the sort key.
    """

    at: str
    minutes: int | None
    clock: bool
    label: str
    order: int


def parse_at(text: str) -> Offset | None:
    """Parse one ``at`` value; ``None`` if it is not an allowed spelling."""
    if text == KICKOFF:
        return Offset(text, 0, True, "Kickoff", 0)
    if text == HALFTIME:
        return Offset(text, None, False, "Halftime", HALFTIME_ORDER)
    match = _AT_RE.match(text)
    if match is None:
        return None
    days, hours, mins = (int(g) if g else None for g in match.groups())
    if days is not None:
        if days > MAX_DAYS:
            return None
        label = "Day before" if days == 1 else f"{days} days before"
        minutes = -days * 24 * 60
        return Offset(text, minutes, False, label, minutes)
    if hours is None and mins is None:
        return None
    if (hours or 0) > MAX_HOURS or (mins or 0) > MAX_MINUTES:
        return None
    parts = []
    if hours:
        parts.append(f"{hours} hr")
    if mins:
        parts.append(f"{mins} min")
    minutes = -((hours or 0) * 60 + (mins or 0))
    return Offset(text, minutes, True, " ".join(parts) + " before", minutes)


def offset_of(text: str) -> Offset:
    """Parse an ``at`` value, raising ``ValueError`` that lists the allowed forms."""
    offset = parse_at(text)
    if offset is None:
        raise ValueError(f"unknown time {text!r}; use {ALLOWED_FORMS}")
    return offset


def check_at(text: str) -> str:
    """Pydantic ``AfterValidator`` for an ``at`` value."""
    offset_of(text)
    return text


class _HasAt(Protocol):
    @property
    def at(self) -> str: ...


S = TypeVar("S", bound=Sequence[_HasAt])


def check_order(steps: S) -> S:
    """Pydantic ``AfterValidator``: steps must be listed in time order (ties allowed)."""
    previous: tuple[int, Offset] | None = None
    for n, step in enumerate(steps):
        offset = parse_at(step.at)
        if offset is None:
            continue
        if previous is not None and offset.order < previous[1].order:
            m, before = previous
            raise ValueError(
                f"steps must be in time order: step {n} ({offset.at}) "
                f"is earlier than step {m} ({before.at}) but listed after it"
            )
        previous = (n, offset)
    return steps
