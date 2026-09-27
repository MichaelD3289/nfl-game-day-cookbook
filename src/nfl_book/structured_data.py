"""schema.org ``Recipe`` structured data (JSON-LD) for website recipe pages.

Everything here is pure: it reads authored fields and never guesses. A value that
cannot be stated exactly (a prep time such as "5–10 min (estimated)") is left out
rather than approximated.
"""

from __future__ import annotations

import html
import json
import re
from typing import Any

from nfl_book.config import Settings
from nfl_book.models.content import Recipe

_ISO = re.compile(
    r"^P(?=\d|T\d)(\d+Y)?(\d+M)?(\d+W)?(\d+D)?(T(?=\d)(\d+H)?(\d+M)?(\d+(\.\d+)?S)?)?$"
)
_PROSE = re.compile(
    r"^(?:(?P<h>\d+)\s*(?:hours?|hrs?)\b)?\s*(?:(?P<m>\d+)\s*(?:minutes?|mins?)\b)?$",
    re.IGNORECASE,
)
_ISO_SECONDS = re.compile(r"^P(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?)?$")
_STEP = re.compile(r"^\s*\d+[.)]\s+")
# The index whose bucket names the main ingredient, found by its front-matter field.
_MAIN_INGREDIENT_FIELD = "index.main_ingredient"


def iso_duration(text: str | None) -> str | None:
    """An ISO 8601 duration for ``text``, or None when it is not exactly one.

    Accepts a literal ISO duration (returned unchanged) or prose that is only a
    duration, such as "10 minutes" or "1 hr 30 min". Ranges, qualifiers and
    anything else return None, and so does a zero duration, which says nothing useful.
    """
    text = (text or "").strip()
    if not text:
        return None
    if _ISO.match(text):
        return text if re.search(r"[1-9]", text) else None
    match = _PROSE.match(text)
    if not match or not (match["h"] or match["m"]):
        return None
    hours = f"{int(match['h'])}H" if match["h"] and int(match["h"]) else ""
    minutes = f"{int(match['m'])}M" if match["m"] and int(match["m"]) else ""
    return f"PT{hours}{minutes}" if hours or minutes else None


def _seconds(iso: str) -> int | None:
    """Whole seconds in an ISO duration made of days, hours, minutes and seconds only."""
    match = _ISO_SECONDS.match(iso)
    if not match or iso in ("P", "PT") or iso.endswith("T"):
        return None
    days, hours, minutes, seconds = (int(part or 0) for part in match.groups())
    return ((days * 24 + hours) * 60 + minutes) * 60 + seconds


def _format(seconds: int) -> str:
    hours, rest = divmod(seconds, 3600)
    minutes, secs = divmod(rest, 60)
    parts = [
        f"{hours}H" if hours else "",
        f"{minutes}M" if minutes else "",
        f"{secs}S" if secs else "",
    ]
    return "PT" + ("".join(parts) or "0S")


def total_time(prep: str | None, cook: str | None) -> str | None:
    """Prep plus cook as an ISO duration, when both are known exactly."""
    if not prep or not cook:
        return None
    first, second = _seconds(prep), _seconds(cook)
    if first is None or second is None:
        return None
    return _format(first + second)


def plain_text(md: str) -> str:
    """Inline Markdown reduced to the words a reader sees, on one line."""
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", md)  # [text](url)
    text = re.sub(r"\[([^\]]*)\]\{[^}]*\}", r"\1", text)  # [text]{.class}
    text = text.replace("`", "")
    text = re.sub(r"\*\*(.+?)\*\*|__(.+?)__", lambda m: m[1] or m[2], text, flags=re.DOTALL)
    text = re.sub(r"\*(.+?)\*", r"\1", text, flags=re.DOTALL)
    text = re.sub(r"(?<!\w)_(.+?)_(?!\w)", r"\1", text, flags=re.DOTALL)
    text = re.sub(r"\\([^\w\s])", r"\1", text)  # backslash escapes
    return " ".join(text.split())


def instruction_steps(md: str) -> list[str]:
    """One plain-text step per numbered list item, else per paragraph."""
    lines = md.strip().splitlines()
    if any(_STEP.match(line) for line in lines):
        items: list[list[str]] = []
        for line in lines:
            if _STEP.match(line):
                items.append([_STEP.sub("", line, count=1)])
            elif items:
                items[-1].append(line)
        chunks = ["\n".join(item) for item in items]
    else:
        chunks = re.split(r"\n\s*\n", md)
    return [step for step in (plain_text(chunk) for chunk in chunks) if step]


def _bucket_labels(recipe: Recipe, settings: Settings, field: str) -> list[str]:
    config = next((i for i in settings.indexes if i.field == field), None)
    value = recipe.meta.index.get(field.removeprefix("index."))
    if config is None or value is None:
        return []
    ids = [value] if isinstance(value, str) else value
    labels = {b.id: b.label for b in config.buckets}
    return [labels[i] for i in ids if i in labels]


def recipe_json_ld(
    recipe: Recipe, settings: Settings, *, image_url: str | None, page_url: str | None
) -> dict[str, Any]:
    """schema.org ``Recipe`` data for ``recipe``; keys without a value are left out."""
    meta = recipe.meta
    prep, cook = iso_duration(meta.prep), iso_duration(meta.cook)
    course = settings.course(meta.course)
    keywords = [recipe.team.name, recipe.location]
    keywords += _bucket_labels(recipe, settings, _MAIN_INGREDIENT_FIELD)
    ingredients = [plain_text(item.text) for group in recipe.ingredients for item in group.items]
    steps = instruction_steps(recipe.instructions)
    fields: dict[str, Any] = {
        "name": recipe.title,
        "description": meta.description,
        "image": image_url,
        "recipeYield": meta.yield_,
        "prepTime": prep,
        "cookTime": cook,
        "totalTime": total_time(prep, cook),
        "recipeCategory": course.label if course else None,
        "recipeCuisine": recipe.location,
        "keywords": ", ".join(dict.fromkeys(k for k in keywords if k)),
        "recipeIngredient": [line for line in ingredients if line],
        "recipeInstructions": [{"@type": "HowToStep", "text": step} for step in steps],
        "isBasedOn": meta.source.url if meta.source else None,
        "url": page_url,
    }
    data: dict[str, Any] = {"@context": "https://schema.org", "@type": "Recipe"}
    data.update({key: value for key, value in fields.items() if value})
    return data


def head_html(data: dict[str, Any], canonical: str | None) -> str:
    """A JSON-LD ``<script>`` safe to embed in HTML, plus the canonical link if any."""
    body = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    head = f'<script type="application/ld+json">{body}</script>'
    if canonical:
        head += f'\n<link rel="canonical" href="{html.escape(canonical, quote=True)}">'
    return head
