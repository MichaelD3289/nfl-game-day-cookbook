import pytest

from nfl_book.release_policy import is_latest_stable, newest_stable


@pytest.mark.parametrize(
    ("tag", "tags", "expected"),
    [
        ("v1.2.0", ["v1.1.0", "v1.2.0", "v2.0.0-rc.1"], True),
        ("v1.1.0", ["v1.1.0", "v1.2.0"], False),
        ("v1.9.0", ["v1.9.0", "v1.10.0"], False),
        ("v2.0.0-rc.1", ["v1.2.0", "v2.0.0-rc.1"], False),
        ("v1.0.0", ["v1.0.0"], True),
        ("not-a-version", ["not-a-version"], False),
    ],
)
def test_only_highest_stable_tag_can_deploy(tag: str, tags: list[str], expected: bool) -> None:
    assert is_latest_stable(tag, tags) is expected


@pytest.mark.parametrize(
    ("tags", "expected"),
    [
        (["v1.9.0\n", "v1.10.0\n", "v2.0.0-rc.1\n"], "v1.10.0"),
        (["v0.1.0"], "v0.1.0"),
        (["v2.0.0-rc.1", "main"], None),
        ([], None),
    ],
)
def test_newest_stable_tag(tags: list[str], expected: str | None) -> None:
    assert newest_stable(tags) == expected
