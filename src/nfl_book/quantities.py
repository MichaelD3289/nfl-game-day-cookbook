"""Ingredient amounts and servings, parsed at build time for website scaling.

Ingredient lines stay free Markdown. This module finds the amounts in a line so the
website can rescale them in the browser (``styles/website-scale.js``); the print book
never uses them. An amount is either

* a measured amount anywhere in the line: a number or range followed by a known unit
  (``1 1/2 cups``, ``2–3 tablespoons``, ``(about 12 ounces)``), or
* a count at the start of the line (``3 garlic cloves``, ``1 (15-ounce) can``).

Amounts that describe a portion or a package size do not scale: ``1 tablespoon per
sandwich`` and ``1 can (15 ounces)`` keep their numbers. Authors opt a whole line out
with ``{{no-scale}}`` (frying oil, a pan of water, ...).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from fractions import Fraction

NO_SCALE_RE = re.compile(r"\{\{\s*no-scale\s*\}\}")

UNICODE_FRACTIONS = {
    "½": Fraction(1, 2),
    "¼": Fraction(1, 4),
    "¾": Fraction(3, 4),
    "⅓": Fraction(1, 3),
    "⅔": Fraction(2, 3),
    "⅛": Fraction(1, 8),
    "⅜": Fraction(3, 8),
    "⅝": Fraction(5, 8),
    "⅞": Fraction(7, 8),
}
_UF = "".join(UNICODE_FRACTIONS)

# Written unit -> canonical unit understood by website-scale.js.
UNIT_ALIASES = {
    "teaspoon": "tsp",
    "teaspoons": "tsp",
    "tsp": "tsp",
    "tsp.": "tsp",
    "tablespoon": "tbsp",
    "tablespoons": "tbsp",
    "tbsp": "tbsp",
    "tbsp.": "tbsp",
    "cup": "cup",
    "cups": "cup",
    "pint": "pint",
    "pints": "pint",
    "quart": "quart",
    "quarts": "quart",
    "qt": "quart",
    "gallon": "gallon",
    "gallons": "gallon",
    "ounce": "oz",
    "ounces": "oz",
    "oz": "oz",
    "oz.": "oz",
    "pound": "lb",
    "pounds": "lb",
    "lb": "lb",
    "lbs": "lb",
    "lb.": "lb",
    "lbs.": "lb",
    "gram": "g",
    "grams": "g",
    "g": "g",
    "kilogram": "kg",
    "kilograms": "kg",
    "kg": "kg",
    "milliliter": "ml",
    "milliliters": "ml",
    "millilitre": "ml",
    "millilitres": "ml",
    "ml": "ml",
    "liter": "l",
    "liters": "l",
    "litre": "l",
    "litres": "l",
}
# Canonical unit -> (quantity kind, size in that kind's base unit). Must match the
# UNITS table in styles/website-scale.js.
UNITS = {
    "tsp": ("us-volume", Fraction(1)),
    "tbsp": ("us-volume", Fraction(3)),
    "cup": ("us-volume", Fraction(48)),
    "pint": ("us-volume", Fraction(96)),
    "quart": ("us-volume", Fraction(192)),
    "gallon": ("us-volume", Fraction(768)),
    "oz": ("us-weight", Fraction(1)),
    "lb": ("us-weight", Fraction(16)),
    "ml": ("metric-volume", Fraction(1)),
    "l": ("metric-volume", Fraction(1000)),
    "g": ("metric-weight", Fraction(1)),
    "kg": ("metric-weight", Fraction(1000)),
}
_UNIT_ALT = "|".join(re.escape(u) for u in sorted(UNIT_ALIASES, key=len, reverse=True))

_NUM = rf"(?:\d+\s+\d+/\d+|\d+/\d+|\d+\s?[{_UF}]|\d+(?:\.\d+)?|[{_UF}])"
_RANGE = rf"(?P<low>{_NUM})(?:(?:\s*[-–—]\s*|\s+to\s+)(?P<high>{_NUM}))?"
_ADJ = r"(?:(?P<adj>generous|heaping|heaped|scant|level|rounded)\s+)?"
_START = rf"(?<![\w.,/{_UF}–—-])"

MEASURED_RE = re.compile(rf"{_START}{_RANGE}\s+{_ADJ}(?P<unit>{_UNIT_ALT})(?![\w-])", re.IGNORECASE)
LEAD_RE = re.compile(
    r"^(?:(?:about|approximately|approx\.|scant|generous|heaping|optional:?|up to)\s+)*"
    r"(?:(?:finely\s+grated\s+)?(?:zest|juice)\s+of\s+)?"
    rf"(?P<amount>{_RANGE})(?=\s+(?P<next>[^\s]+))",
    re.IGNORECASE,
)
# A size in brackets right after a package word is per package: "1 can (15 ounces)".
PACKAGE_RE = re.compile(
    r"\b(?:cans?|jars?|packages?|bottles?|box|boxes|bags?|cartons?|tins?|packets?|"
    r"envelopes?|containers?|tubs?|blocks?)\s*\(\s*(?:about\s+)?$",
    re.IGNORECASE,
)
# "1 tablespoon per sandwich", "½ tablespoon at a time", "(15 ounces each)"; but
# "1 teaspoon each cumin and paprika" is a total and scales.
PORTION_RE = re.compile(r"\bper\b|\bat a time\b|\beach\s*$", re.IGNORECASE)
PLUS_RE = re.compile(r"\s*(?:\bplus\b|\+)\s*", re.IGNORECASE)
NOT_COUNTS = {"inch", "inches", "minute", "minutes", "hour", "hours", "degrees", "percent"}
GLUED_RE = re.compile(
    rf"(?<![\w./{_UF}])\d+(?:\.\d+)?(?:g|kg|ml|oz|lbs?|tsp|tbsp)\b", re.IGNORECASE
)
BAD_NUMBER_RE = re.compile(r"(?<![\w/])\d+/(?!\d)|\d+/\d+/\d+|\b\d+/0+\b")
SERVINGS_RE = re.compile(r"^\s*(?P<low>\d+)(?:\s*(?:-|–|—|to)\s*(?P<high>\d+))?\s*$")
_PEOPLE = r"(?P<low>\d+)(?:\s*(?:-|–|—|to)\s*(?P<high>\d+))?"
# "6 servings", "4–6 side servings", "4 people", "about 4 appetizer portions", "serves 6–10".
YIELD_SERVINGS_RES = (
    re.compile(
        rf"^\s*(?:about\s+)?{_PEOPLE}\s+(?:[a-z]+\s+)?(?:servings?|people|portions?)\b",
        re.IGNORECASE,
    ),
    re.compile(rf"\bserves\s+{_PEOPLE}\b", re.IGNORECASE),
    re.compile(rf"\babout\s+{_PEOPLE}\s+(?:[a-z]+\s+)?portions\b", re.IGNORECASE),
)


@dataclass(frozen=True)
class Amount:
    """A scalable amount at ``text[start:end]`` of an ingredient line."""

    start: int
    end: int
    low: Fraction
    high: Fraction | None = None
    unit: str | None = None  # canonical unit; None for a count
    adjective: str | None = None  # "generous", "scant", ... kept when rewritten


def parse_number(text: str) -> Fraction:
    """``2``, ``1.5``, ``1/2``, ``1 1/2``, ``½`` or ``2½`` as an exact fraction."""
    text = text.strip()
    total = Fraction(0)
    if text and text[-1] in UNICODE_FRACTIONS:
        total += UNICODE_FRACTIONS[text[-1]]
        text = text[:-1].strip()
    for part in text.split():
        if "/" in part:
            num, den = part.split("/")
            total += Fraction(int(num), int(den))
        else:
            total += Fraction(part)
    return total


def _portion(text: str, end: int) -> bool:
    """Is the amount ending at ``end`` a per-portion amount ("... per sandwich")?"""
    clause = re.split(r"[,;()]", text[end:], maxsplit=1)[0]
    return bool(PORTION_RE.search(clause))


def _amount(match: re.Match[str], unit: str | None, start: int, end: int) -> Amount | None:
    low = parse_number(match["low"])
    high = parse_number(match["high"]) if match["high"] else None
    if low <= 0 or (high is not None and high <= low):
        return None
    adjective = match["adj"].lower() if unit and match["adj"] else None
    return Amount(start, end, low, high, unit, adjective)


def _merge_plus(text: str, amounts: list[Amount]) -> list[Amount]:
    """Join "1 cup plus 2 tablespoons" into one amount so it converts as a whole."""
    merged: list[Amount] = []
    for amount in amounts:
        last = merged[-1] if merged else None
        if (
            last is not None
            and last.high is None
            and amount.high is None
            and last.unit
            and amount.unit
            and UNITS[last.unit][0] == UNITS[amount.unit][0]
            and PLUS_RE.fullmatch(text[last.end : amount.start])
        ):
            unit = max(last.unit, amount.unit, key=lambda u: UNITS[u][1])
            size = UNITS[unit][1]
            total = (last.low * UNITS[last.unit][1] + amount.low * UNITS[amount.unit][1]) / size
            merged[-1] = Amount(last.start, amount.end, total, None, unit, last.adjective)
        else:
            merged.append(amount)
    return merged


def find_amounts(text: str) -> tuple[tuple[Amount, ...], list[str]]:
    """Scalable amounts in an ingredient line, plus problems that stop it scaling."""
    problems = []
    for bad in GLUED_RE.finditer(text):
        problems.append(f"write a space between the amount and unit in {bad[0]!r} so it can scale")
    for bad in BAD_NUMBER_RE.finditer(text):
        problems.append(f"cannot read the amount {bad[0]!r}")
    if problems:
        return (), problems
    amounts: list[Amount] = []
    for match in MEASURED_RE.finditer(text):
        if PACKAGE_RE.search(text[: match.start()]) or _portion(text, match.end()):
            continue
        amount = _amount(match, UNIT_ALIASES[match["unit"].lower()], *match.span())
        if amount is None:
            problems.append(f"range {match[0]!r} must go from low to high")
        else:
            amounts.append(amount)
    amounts = _merge_plus(text, amounts)
    lead = LEAD_RE.match(text)
    if (
        lead
        and not any(a.start == lead.start("amount") for a in amounts)
        and lead["next"].lower().strip(".,;:") not in NOT_COUNTS
        and not _portion(text, lead.end("amount"))
    ):
        amount = _amount(lead, None, *lead.span("amount"))
        if amount is None:
            problems.append(f"range {lead['amount']!r} must go from low to high")
        else:
            amounts.insert(0, amount)
    return tuple(amounts), problems


def parse_servings(value: int | str) -> tuple[int, int] | None:
    """``6`` or ``"6-8"`` as ``(low, high)``; None when it is not a valid count."""
    if isinstance(value, int):
        return (value, value) if value > 0 else None
    match = SERVINGS_RE.match(value)
    if not match:
        return None
    low = int(match["low"])
    high = int(match["high"] or low)
    return (low, high) if 0 < low <= high else None


def servings_from_yield(text: str) -> tuple[int, int] | None:
    """Servings from a plain "N servings" / "N–M servings" yield, else None."""
    for pattern in YIELD_SERVINGS_RES:
        if match := pattern.search(text):
            low = int(match["low"])
            high = int(match["high"] or low)
            return (low, high) if 0 < low <= high else None
    return None
