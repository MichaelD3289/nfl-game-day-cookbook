"""Schemas for the authored configuration in ``data/``."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import Field, model_validator

from nfl_book.models.common import NonEmpty, Slug, StrictModel


class Bucket(StrictModel):
    id: Slug
    label: NonEmpty
    short_label: str | None = None

    @property
    def singular(self) -> str:
        return self.short_label or self.label


class IndexConfig(StrictModel):
    """One entry of ``data/indexes.yml``. ``options`` feeds custom index kinds."""

    id: Slug
    title: NonEmpty
    kind: Slug = "field"
    field: str | None = None
    required: bool = False
    multiple: bool = False
    intro: str | None = None
    buckets: list[Bucket] = Field(min_length=1)
    options: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _unique_buckets(self) -> IndexConfig:
        ids = [b.id for b in self.buckets]
        if len(ids) != len(set(ids)):
            raise ValueError(f"index {self.id!r} has duplicate bucket ids")
        return self


class IndexesFile(StrictModel):
    indexes: list[IndexConfig]

    @model_validator(mode="after")
    def _checks(self) -> IndexesFile:
        ids = [i.id for i in self.indexes]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate index ids")
        if "course" not in ids:
            raise ValueError("an index with id 'course' is required (recipe layout uses it)")
        return self


class MenuType(StrictModel):
    id: Slug
    title: NonEmpty
    description: str | None = None


class MenuTypesFile(StrictModel):
    menu_types: list[MenuType]


class ComponentKind(StrictModel):
    id: Slug
    label: NonEmpty
    short_label: str | None = None

    @property
    def singular(self) -> str:
        return self.short_label or self.label


class ComponentKindsFile(StrictModel):
    component_kinds: list[ComponentKind] = Field(min_length=1)


class PhotoVariant(StrictModel):
    """One output's recipe photo: a centred square crop, never enlarged."""

    format: Literal["jpeg", "webp"]
    size: int = Field(ge=64, le=4000, description="Square side in pixels.")
    quality: int = Field(ge=1, le=100)


class PhotoSettings(StrictModel):
    # Defaults mirror data/book.yml, which explains the sizes.
    web: PhotoVariant = PhotoVariant(format="webp", size=400, quality=80)
    print: PhotoVariant = PhotoVariant(format="jpeg", size=500, quality=82)

    @model_validator(mode="after")
    def _print_is_jpeg(self) -> PhotoSettings:
        if self.print.format != "jpeg":
            raise ValueError("print photos must be jpeg (pdflatex cannot embed webp)")
        return self


class BookConfig(StrictModel):
    title: NonEmpty
    subtitle: str | None = None
    output_filename: NonEmpty = "book.pdf"
    paper: str = "letter"
    suggestion_form_url: str | None = Field(
        None,
        pattern=r"^https://",
        description="Web app that files anonymous website suggestions as issues.",
    )
    photos: PhotoSettings = PhotoSettings()


class CoverMeta(StrictModel):
    """Front matter of ``book/frontmatter/cover.md`` (all optional overrides)."""

    title: str | None = None
    subtitle: str | None = None
    tagline: str | None = None
