"""The one serializer for every JSON payload the website's JavaScript reads.

Payloads are frozen dataclasses (``catalog.py`` and ``website_pages.py``). A dataclass
field becomes a JSON key of the same name, so a key is renamed by renaming the field, and
every key is snake_case because Python field names are. A trailing underscore (for a
reserved word such as ``yield_``) is dropped. Tuples become lists. A field marked
``omit_none`` is left out when it is ``None``; every other ``None`` is written as ``null``.
``tests/integration/test_website_payload_contract.py`` runs the real ``styles/website-*.js``
on the payloads built here, so a renamed field fails there.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import field, fields, is_dataclass
from typing import Any

__all__ = ["attribute_json", "omit_none", "script_json", "to_payload", "write_json"]

_OMIT_NONE = "omit_none"


def omit_none() -> Any:
    """A dataclass field that is left out of the payload when it is ``None``."""
    return field(default=None, metadata={_OMIT_NONE: True})


def to_payload(value: object) -> Any:
    """``value`` as plain JSON data: dicts, lists, strings, numbers, booleans, ``None``."""
    if is_dataclass(value) and not isinstance(value, type):
        found: dict[str, Any] = {}
        for item in fields(value):
            inner = getattr(value, item.name)
            if inner is None and item.metadata.get(_OMIT_NONE):
                continue
            found[item.name.rstrip("_")] = to_payload(inner)
        return found
    if isinstance(value, Mapping):
        return {str(key): to_payload(inner) for key, inner in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_payload(inner) for inner in value]
    return value


def attribute_json(value: object) -> str:
    """JSON for an HTML attribute (``data-facets``, ``data-fields``); the template escapes it."""
    return json.dumps(to_payload(value), ensure_ascii=False)


def script_json(value: object) -> str:
    """JSON for a one-line ``<script>`` element: no newlines, and no ``</`` to close it early."""
    text = json.dumps(to_payload(value), ensure_ascii=False, separators=(",", ":"))
    return text.replace("</", "<\\/")


def write_json(value: object, *, indent: int = 2) -> str:
    """JSON for a data file the site serves (``recipes.json``), ending in a newline."""
    return json.dumps(to_payload(value), ensure_ascii=False, indent=indent) + "\n"
