"""Offline numeric stable-tag comparison used by the release workflow."""

from __future__ import annotations

import re
import sys
from collections.abc import Iterable

STABLE = re.compile(r"v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)")


def newest_stable(tags: Iterable[str]) -> str | None:
    versions = {
        tuple(map(int, match.groups())): t
        for t in (t.strip() for t in tags)
        if (match := STABLE.fullmatch(t))
    }
    return versions[max(versions)] if versions else None


def is_latest_stable(tag: str, tags: Iterable[str]) -> bool:
    candidate = STABLE.fullmatch(tag)
    if candidate is None:
        return False
    versions = [
        tuple(map(int, match.groups())) for t in tags if (match := STABLE.fullmatch(t.strip()))
    ]
    return bool(versions) and tuple(map(int, candidate.groups())) == max(versions)


if __name__ == "__main__":
    if sys.argv[1] == "--newest":
        print(newest_stable(sys.stdin) or "")
    else:
        print("true" if is_latest_stable(sys.argv[1], sys.stdin) else "false")
