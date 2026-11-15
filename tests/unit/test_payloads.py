"""The shared payload serializer: dataclass fields become snake_case JSON keys."""

from __future__ import annotations

import json
from dataclasses import dataclass

from nfl_book.payloads import attribute_json, omit_none, script_json, to_payload, write_json


@dataclass(frozen=True)
class _Leaf:
    print_pages: tuple[str, ...]
    yield_: str | None
    group: str | None = omit_none()


@dataclass(frozen=True)
class _Root:
    leaves: tuple[_Leaf, ...]
    facets: dict[str, tuple[str, ...]]
    pair: tuple[int, int] | None


def test_fields_become_keys_in_declaration_order() -> None:
    root = _Root((_Leaf(("a.html",), None),), {"main-ingredient": ("beef",)}, (1, 2))
    assert to_payload(root) == {
        "leaves": [{"print_pages": ["a.html"], "yield": None}],
        "facets": {"main-ingredient": ["beef"]},
        "pair": [1, 2],
    }


def test_omit_none_field_is_written_when_set() -> None:
    assert to_payload(_Leaf((), "x", "afc-east")) == {
        "print_pages": [],
        "yield": "x",
        "group": "afc-east",
    }


def test_script_json_is_one_line_without_closing_tags() -> None:
    text = script_json({"a": "</script>", "b": "é"})
    assert "</" not in text and "\n" not in text
    assert json.loads(text) == {"a": "</script>", "b": "é"}


def test_attribute_and_file_json() -> None:
    root = _Root((), {"team": ("bills",)}, None)
    assert json.loads(attribute_json(root.facets)) == {"team": ["bills"]}
    assert write_json(root).endswith("}\n")
