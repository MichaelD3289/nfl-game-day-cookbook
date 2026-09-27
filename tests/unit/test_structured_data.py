"""schema.org Recipe structured data built from authored recipe fields."""

import json

import pytest

from nfl_book.structured_data import (
    head_html,
    instruction_steps,
    iso_duration,
    plain_text,
    total_time,
)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("PT20M", "PT20M"),
        ("PT1H30M", "PT1H30M"),
        ("P1D", "P1D"),
        ("10 minutes", "PT10M"),
        ("10 min", "PT10M"),
        ("1 hour", "PT1H"),
        ("2 Hours", "PT2H"),
        ("1 hour 30 minutes", "PT1H30M"),
        ("1 hr 30 min", "PT1H30M"),
        ("90 mins", "PT90M"),
        ("  45 minutes ", "PT45M"),
    ],
)
def test_iso_duration_accepts_iso_or_exact_prose(text: str, expected: str) -> None:
    assert iso_duration(text) == expected


@pytest.mark.parametrize(
    "text",
    [
        "15 min (estimated)",
        "15 minutes (source listed)",
        "5–10 min",
        "5-10 minutes",
        "About 10 hours, temperature-guided",
        "20 minutes active",
        "1 hour plus chilling",
        "overnight",
        "1/2 hour",
        "1.5 hours",
        "P",
        "PT",
        "PT1H2",
        "",
        None,
    ],
)
def test_iso_duration_rejects_anything_else(text: str | None) -> None:
    assert iso_duration(text) is None


@pytest.mark.parametrize("text", ["0 minutes", "0 hr 0 min", "PT0M", "PT0S", "P0D"])
def test_iso_duration_treats_zero_as_unknown(text: str) -> None:
    assert iso_duration(text) is None


def test_total_time_adds_parsed_durations() -> None:
    assert total_time("PT15M", "PT20M") == "PT35M"
    assert total_time("PT45M", "PT20M") == "PT1H5M"
    assert total_time("PT1H", "P1D") == "PT25H"
    assert total_time("PT15M", None) is None
    assert total_time(None, "PT20M") is None


def test_plain_text_strips_markdown() -> None:
    text = "Spoon **the dip** over *each* _slider_, see [the note](https://x.test) and `this`"
    assert plain_text(text) == "Spoon the dip over each slider, see the note and this"
    assert plain_text("Salt \\& pepper,\n  to   taste") == "Salt & pepper, to taste"
    assert plain_text("[Q]{.q-mark} Hot") == "Q Hot"


def test_instruction_steps_split_numbered_lists_and_paragraphs() -> None:
    listed = "1. Form 12 patties and\n   cook until done.\n2. Spoon the **dip** over each slider."
    assert instruction_steps(listed) == [
        "Form 12 patties and cook until done.",
        "Spoon the dip over each slider.",
    ]
    assert instruction_steps("Bake the wings, then toss them in the sauce.") == [
        "Bake the wings, then toss them in the sauce."
    ]
    assert instruction_steps("Heat the oil.\n\nFry the wings.\n\n") == [
        "Heat the oil.",
        "Fry the wings.",
    ]


def test_head_html_escapes_script_end_and_adds_canonical() -> None:
    data = {"@type": "Recipe", "name": "Sneaky </script><b>"}
    head = head_html(data, 'https://x.test/recipe-a.html?a=1&b="2"')
    script = head.split("</script>")[0]
    assert script.startswith('<script type="application/ld+json">')
    body = script.removeprefix('<script type="application/ld+json">')
    assert "</" not in body
    assert json.loads(body) == data
    assert head.endswith(
        '<link rel="canonical" href="https://x.test/recipe-a.html?a=1&amp;b=&quot;2&quot;">'
    )
    assert "canonical" not in head_html(data, None)
