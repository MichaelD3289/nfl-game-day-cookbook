from __future__ import annotations

from enum import StrEnum
from typing import Annotated
from urllib.parse import urlparse

from pydantic import AfterValidator, BaseModel, ConfigDict, StringConstraints

SLUG_PATTERN = r"^[a-z0-9]+(?:-[a-z0-9]+)*$"

Slug = Annotated[str, StringConstraints(pattern=SLUG_PATTERN)]
"""Stable lowercase identifier: letters, digits, single hyphens."""

NonEmpty = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


def check_url(value: str) -> str:
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc or " " in value:
        raise ValueError(f"not an absolute http(s) URL: {value!r}")
    return value


HttpUrlStr = Annotated[str, AfterValidator(check_url)]
"""An absolute http(s) URL kept byte-for-byte as authored (it is a cache key)."""


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, populate_by_name=True)


class Status(StrEnum):
    DRAFT = "draft"
    TESTING = "testing"
    PUBLISHED = "published"
    RETIRED = "retired"


class SourceLink(StrictModel):
    url: HttpUrlStr
    title: str | None = None
