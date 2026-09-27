"""Stable-ID references: component markers and cross-reference labels.

Authors reference a component from an ingredient line with
``{{component:<component-id>}}``. The marker is removed from the displayed
text and replaced by the Q marker plus a page reference when rendered.

Every page-addressable item gets a LaTeX label derived from its stable ID;
LaTeX resolves page numbers from these labels at compile time.
"""

from __future__ import annotations

import re

from nfl_book.models.common import SLUG_PATTERN
from nfl_book.models.content import Ingredient, IngredientGroup
from nfl_book.quantities import NO_SCALE_RE, find_amounts

MARKER_RE = re.compile(r"\{\{\s*component\s*:\s*(?P<id>[^{}\s]*)\s*\}\}")
BRACES_RE = re.compile(r"\{\{.*?\}\}")
BULLET_RE = re.compile(r"^[-*+]\s+(?P<text>.+)$")
GROUP_RE = re.compile(r"^###\s+(?P<title>.+?)\s*#*\s*$")
SLUG_RE = re.compile(SLUG_PATTERN)


def html_id(label: str) -> str:
    """The HTML id for a label in digital outputs (website, EPUB): ``recipe:x`` -> ``recipe-x``."""
    return label.replace(":", "-")


def recipe_label(recipe_id: str) -> str:
    return f"recipe:{recipe_id}"


def recipe_end_label(recipe_id: str) -> str:
    return f"recipe:{recipe_id}:end"


def component_label(component_id: str) -> str:
    return f"component:{component_id}"


def division_label(division_key: str) -> str:
    return f"division:{division_key}"


def menu_label(menu_id: str) -> str:
    return f"menu:{menu_id}"


def team_label(team_slug: str) -> str:
    return f"team:{team_slug}"


def section_label(section_id: str) -> str:
    return f"section:{section_id}"


def index_label(index_id: str) -> str:
    return f"index:{index_id}"


def find_markers(text: str) -> list[str]:
    """Any ``{{...}}`` constructs in free text (markers are illegal there)."""
    return BRACES_RE.findall(text)


def parse_ingredients(text: str) -> tuple[tuple[IngredientGroup, ...], list[str]]:
    """Parse an ``## Ingredients`` section.

    Accepts bullet lines, optionally grouped under ``### Subheading`` lines.
    Returns the groups plus human-readable problems (empty when valid).
    """
    problems: list[str] = []
    groups: list[tuple[str | None, list[Ingredient]]] = [(None, [])]
    for lineno, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        if group := GROUP_RE.match(line):
            groups.append((group["title"], []))
            continue
        bullet = BULLET_RE.match(line)
        if not bullet:
            problems.append(
                f"Ingredients line {lineno}: expected '- item' or '### Group', got {line!r}"
            )
            continue
        item, item_problems = parse_ingredient(bullet["text"])
        problems.extend(f"Ingredients line {lineno}: {p}" for p in item_problems)
        if item:
            groups[-1][1].append(item)
    result = tuple(IngredientGroup(h, tuple(items)) for h, items in groups if items)
    for heading, items in groups:
        if heading is not None and not items:
            problems.append(f"Ingredients group {heading!r} has no items")
    if not result and not problems:
        problems.append("Ingredients section has no items")
    return result, problems


def parse_ingredient(text: str) -> tuple[Ingredient | None, list[str]]:
    fixed = len(NO_SCALE_RE.findall(text))
    braces = BRACES_RE.findall(text)
    markers = list(MARKER_RE.finditer(text))
    problems = []
    if fixed > 1:
        problems.append("only one {{no-scale}} marker is allowed per ingredient line")
    if len(braces) != len(markers) + fixed:
        bad = [b for b in braces if not (MARKER_RE.fullmatch(b) or NO_SCALE_RE.fullmatch(b))]
        problems.append(
            f"malformed marker {bad[0]!r}; use {{{{component:<component-id>}}}} or {{{{no-scale}}}}"
        )
    if len(markers) > 1:
        problems.append("only one component reference is allowed per ingredient line")
    component = None
    if markers:
        component = markers[0]["id"]
        if not SLUG_RE.match(component):
            problems.append(f"invalid component id {component!r} in reference")
    display = " ".join(NO_SCALE_RE.sub(" ", MARKER_RE.sub(" ", text)).split())
    if not display:
        problems.append("ingredient needs text besides the component reference")
    amounts, amount_problems = find_amounts(display)
    if fixed and not amounts and not amount_problems:
        problems.append("{{no-scale}} is only needed on a line with an amount; remove it")
    if not fixed:
        problems.extend(f"{p} (or mark the line {{{{no-scale}}}})" for p in amount_problems)
    if problems:
        return None, problems
    return Ingredient(display, component, () if fixed else amounts), []
