from __future__ import annotations

from pydantic import Field, model_validator

from nfl_book.models.common import NonEmpty, Slug, StrictModel


class Team(StrictModel):
    slug: Slug
    name: NonEmpty
    short_name: NonEmpty
    abbreviation: NonEmpty
    location: NonEmpty


class DivisionConfig(StrictModel):
    id: Slug
    name: NonEmpty
    teams: list[Team] = Field(min_length=1)


class ConferenceConfig(StrictModel):
    id: Slug
    name: NonEmpty
    full_name: NonEmpty
    divisions: list[DivisionConfig] = Field(min_length=1)


class Division(StrictModel):
    """A division flattened with its conference, as used by the rest of the book."""

    conference_id: Slug
    conference_name: str
    id: Slug
    name: str
    teams: tuple[Team, ...]

    @property
    def key(self) -> str:
        """Globally unique division id, e.g. ``afc-east``."""
        return f"{self.conference_id}-{self.id}"


class League(StrictModel):
    conferences: list[ConferenceConfig] = Field(min_length=1)

    @model_validator(mode="after")
    def _unique(self) -> League:
        slugs = [t.slug for d in self.divisions for t in d.teams]
        dupes = sorted({s for s in slugs if slugs.count(s) > 1})
        if dupes:
            raise ValueError(f"duplicate team slugs: {', '.join(dupes)}")
        keys = [d.key for d in self.divisions]
        if len(keys) != len(set(keys)):
            raise ValueError("duplicate division ids within a conference")
        return self

    @property
    def divisions(self) -> list[Division]:
        return [
            Division(
                conference_id=c.id,
                conference_name=c.name,
                id=d.id,
                name=d.name,
                teams=tuple(d.teams),
            )
            for c in self.conferences
            for d in c.divisions
        ]

    @property
    def teams(self) -> list[Team]:
        return [t for d in self.divisions for t in d.teams]

    def division(self, conference_id: str, division_id: str) -> Division | None:
        for d in self.divisions:
            if d.conference_id == conference_id and d.id == division_id:
                return d
        return None

    def division_by_key(self, key: str) -> Division | None:
        return next((d for d in self.divisions if d.key == key), None)

    def team(self, slug: str) -> tuple[Division, Team] | None:
        for d in self.divisions:
            for t in d.teams:
                if t.slug == slug:
                    return d, t
        return None

    def team_order(self) -> dict[str, int]:
        return {t.slug: i for i, t in enumerate(self.teams)}
