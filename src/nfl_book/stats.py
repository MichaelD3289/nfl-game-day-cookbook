"""``nfl-book stats``: where the cookbook is thin.

Informational only: gaps never fail anything. The report counts published,
testing and draft content (retired content is ignored), reuses discovery,
validation and :func:`~nfl_book.resolve.resolve`, and never reads or writes
``generated/`` or ``dist/``. The last section lists published recipes and
components whose review is missing or older than ``review_max_age_days``
(:mod:`nfl_book.reviews`), stalest first, as of :attr:`Thresholds.today`.
"""

from __future__ import annotations

import json
from collections import Counter
from collections.abc import Callable
from dataclasses import asdict, dataclass, replace
from datetime import date
from typing import Any

from rich.console import Console
from rich.table import Table

from nfl_book import pipeline, reviews
from nfl_book.errors import ValidationFailed
from nfl_book.models.common import Status
from nfl_book.project import Project
from nfl_book.resolve import BookModel, resolve

MIN_DISHOFFS_PER_DIVISION = 2
MIN_MENUS_PER_TYPE = 3
THIN_BUCKET_SHARE = 0.10
NOT_SET = "(not set)"

COUNTED_STATUSES = (Status.PUBLISHED, Status.TESTING, Status.DRAFT)


def counted(status: Status) -> bool:
    """Statuses the report counts: everything that is or may become part of the book."""
    return status in COUNTED_STATUSES


Cell = str | int | tuple[str, ...] | None


@dataclass(frozen=True)
class Column:
    key: str
    label: str


@dataclass(frozen=True)
class Section:
    id: str
    title: str
    columns: tuple[Column, ...]
    rows: tuple[tuple[Cell, ...], ...]
    empty: str = "None."

    def records(self) -> list[dict[str, Cell]]:
        return [dict(zip((c.key for c in self.columns), row, strict=True)) for row in self.rows]


@dataclass(frozen=True)
class Thresholds:
    min_dishoffs: int = MIN_DISHOFFS_PER_DIVISION
    min_menus: int = MIN_MENUS_PER_TYPE
    thin_share: float = THIN_BUCKET_SHARE
    today: date | None = None
    """Date review ages are measured from; ``None`` means today."""


@dataclass(frozen=True)
class Report:
    thresholds: Thresholds
    sections: tuple[Section, ...]

    def section(self, section_id: str) -> Section:
        return next(s for s in self.sections if s.id == section_id)


SectionBuilder = Callable[[BookModel, Thresholds], list[Section]]


def team_counts(model: BookModel, thresholds: Thresholds) -> list[Section]:
    order = model.settings.league.team_order()
    rows = []
    for division in model.divisions:
        for section in division.teams:
            statuses = Counter(r.meta.status for r in section.recipes)
            published, testing, draft = (statuses[s] for s in COUNTED_STATUSES)
            rows.append(
                (
                    section.team.name,
                    division.division.name,
                    published,
                    testing,
                    draft,
                    len(section.recipes),
                    order[section.team.slug],
                )
            )
    rows.sort(key=lambda r: (r[5], r[2], r[6]))
    columns = (
        Column("team", "Team"),
        Column("division", "Division"),
        Column("published", "Published"),
        Column("testing", "Testing"),
        Column("draft", "Draft"),
        Column("total", "Total"),
    )
    return [Section("teams", "Recipes per team", columns, tuple(r[:6] for r in rows))]


def course_gaps(model: BookModel, thresholds: Thresholds) -> list[Section]:
    buckets = model.settings.course_index.buckets
    rows = []
    for division in model.divisions:
        for section in division.teams:
            have = {r.meta.course for r in section.recipes}
            missing = tuple(b.label for b in buckets if b.id not in have)
            if missing:
                rows.append((section.team.name, division.division.name, missing))
    columns = (Column("team", "Team"), Column("division", "Division"), Column("missing", "Missing"))
    return [
        Section(
            "course-gaps",
            "Teams missing a course",
            columns,
            tuple(rows),
            empty="Every team has every course.",
        )
    ]


def dishoff_gaps(model: BookModel, thresholds: Thresholds) -> list[Section]:
    rows = tuple(
        (d.division.name, len(d.dishoffs))
        for d in model.divisions
        if len(d.dishoffs) < thresholds.min_dishoffs
    )
    return [
        Section(
            "dish-off-gaps",
            f"Divisions with fewer than {thresholds.min_dishoffs} dish-offs",
            (Column("division", "Division"), Column("dish_offs", "Dish-offs")),
            rows,
            empty="Every division has enough dish-offs.",
        )
    ]


def index_spread(model: BookModel, thresholds: Thresholds) -> list[Section]:
    recipes = model.recipes
    total = len(recipes)
    columns = (Column("bucket", "Bucket"), Column("recipes", "Recipes"), Column("note", "Note"))
    sections = []
    for index in model.indexes:
        rows: list[tuple[Cell, ...]] = []
        for bucket in index.sections:
            count = len(bucket.recipes)
            thin = total > 0 and count < thresholds.thin_share * total
            rows.append((bucket.bucket.label, count, "thin" if thin else ""))
        unset = sum(1 for r in recipes if not index.definition.buckets_for(r))
        if unset:
            rows.append((NOT_SET, unset, ""))
        sections.append(
            Section(f"index-{index.definition.id}", index.definition.title, columns, tuple(rows))
        )
    return sections


def _component_rows(model: BookModel) -> list[tuple[Cell, ...]]:
    kinds = [k.id for k in model.settings.component_kinds]
    rows = []
    for component in model.components_by_id.values():
        if not counted(component.meta.status):
            continue
        usage = model.usage.get(component.id)
        direct = len(usage.direct) if usage else 0
        total = len(usage.all) if usage else 0
        key = (total, kinds.index(component.kind.id), component.title.casefold(), component.id)
        row = (
            component.title,
            component.id,
            component.kind.label,
            component.meta.status.value,
            direct,
            total,
        )
        rows.append((key, row))
    rows.sort(key=lambda item: item[0])
    return [row for _, row in rows]


COMPONENT_COLUMNS = (
    Column("component", "Component"),
    Column("id", "Id"),
    Column("kind", "Kind"),
    Column("status", "Status"),
    Column("direct", "Direct"),
    Column("total", "Total"),
)


def component_usage(model: BookModel, thresholds: Thresholds) -> list[Section]:
    return [
        Section(
            "components",
            "Recipes using each component",
            COMPONENT_COLUMNS,
            tuple(_component_rows(model)),
        )
    ]


def unreferenced_components(model: BookModel, thresholds: Thresholds) -> list[Section]:
    rows = tuple(r for r in _component_rows(model) if r[-1] == 0)
    return [
        Section(
            "unreferenced-components",
            "Components no recipe uses",
            COMPONENT_COLUMNS,
            rows,
            empty="Every component is used.",
        )
    ]


def menu_type_gaps(model: BookModel, thresholds: Thresholds) -> list[Section]:
    counts = Counter(m.menu_type.id for m in model.menus)
    rows = tuple(
        (t.title, counts[t.id])
        for t in model.settings.menu_types
        if counts[t.id] < thresholds.min_menus
    )
    return [
        Section(
            "menu-type-gaps",
            f"Menu types with fewer than {thresholds.min_menus} menus",
            (Column("menu_type", "Menu type"), Column("menus", "Menus")),
            rows,
            empty="Every menu type has enough menus.",
        )
    ]


def stale_review_section(model: BookModel, thresholds: Thresholds) -> list[Section]:
    columns = (
        Column("item", "Item"),
        Column("kind", "Kind"),
        Column("id", "Id"),
        Column("last_reviewed", "Last reviewed"),
        Column("age_days", "Age (days)"),
    )
    limit = model.settings.book.review_max_age_days
    if limit is None:
        return [
            Section(
                "stale-reviews",
                "Stale reviews",
                columns,
                (),
                empty="Review age check is off: set review_max_age_days in data/book.yml.",
            )
        ]
    stale = reviews.stale_reviews(
        model.recipes_by_id.values(),
        model.components_by_id.values(),
        limit,
        thresholds.today,
    )
    rows = tuple(
        (
            s.item.title,
            s.kind,
            s.item.id,
            s.last_reviewed_at.isoformat() if s.last_reviewed_at else "never",
            s.age_days,
        )
        for s in stale
    )
    return [
        Section(
            "stale-reviews",
            f"Published items not reviewed in {limit} days (stalest first)",
            columns,
            rows,
            empty=f"Every published recipe and component was reviewed in the last {limit} days.",
        )
    ]


# Report order. A new section appends its builder here.
SECTION_BUILDERS: tuple[SectionBuilder, ...] = (
    team_counts,
    course_gaps,
    dishoff_gaps,
    index_spread,
    component_usage,
    unreferenced_components,
    menu_type_gaps,
    stale_review_section,
)


def load_model(project: Project) -> BookModel:
    """Validated content resolved with every counted status; errors name their files."""
    loaded = pipeline.load(project, require_shortlinks=False)
    if not loaded.diagnostics.ok:
        raise ValidationFailed(loaded.diagnostics)
    return resolve(loaded.settings, loaded.content, loaded.shortlinks.links, include=counted)


def report_for(model: BookModel, thresholds: Thresholds) -> Report:
    # Through the module, so tests that pin reviews.current_date apply here too.
    thresholds = replace(thresholds, today=thresholds.today or reviews.current_date())
    sections = tuple(s for build in SECTION_BUILDERS for s in build(model, thresholds))
    return Report(thresholds, sections)


def build_report(project: Project, thresholds: Thresholds | None = None) -> Report:
    return report_for(load_model(project), thresholds or Thresholds())


# Rendering --------------------------------------------------------------------


def _json_cell(value: Cell) -> Any:
    return list(value) if isinstance(value, tuple) else value


def _json_default(value: object) -> str:
    if isinstance(value, date):
        return value.isoformat()
    raise TypeError(f"cannot write {type(value).__name__} as JSON")


def render_json(report: Report) -> str:
    data = {
        "thresholds": asdict(report.thresholds),
        "sections": [
            {
                "id": s.id,
                "title": s.title,
                "rows": [{k: _json_cell(v) for k, v in r.items()} for r in s.records()],
            }
            for s in report.sections
        ],
    }
    return json.dumps(data, indent=2, default=_json_default)


def _text(value: Cell) -> str:
    if value is None:
        return ""
    return ", ".join(value) if isinstance(value, tuple) else str(value)


def _md_cell(value: Cell) -> str:
    return _text(value).replace("|", "\\|")


def render_markdown(report: Report) -> str:
    parts = []
    for section in report.sections:
        lines = [f"## {section.title}", ""]
        if section.rows:
            lines.append("| " + " | ".join(_md_cell(c.label) for c in section.columns) + " |")
            lines.append("|" + "|".join(" --- " for _ in section.columns) + "|")
            lines.extend("| " + " | ".join(_md_cell(v) for v in row) + " |" for row in section.rows)
        else:
            lines.append(section.empty)
        parts.append("\n".join(lines))
    return "\n\n".join(parts) + "\n"


def render_table(report: Report, console: Console) -> None:
    for section in report.sections:
        if not section.rows:
            console.print(f"[bold]{section.title}[/bold]: {section.empty}", highlight=False)
            console.print()
            continue
        table = Table(title=section.title, title_justify="left", title_style="bold")
        for i, column in enumerate(section.columns):
            values = [row[i] for row in section.rows]
            numeric = any(isinstance(v, int) for v in values) and all(
                v is None or isinstance(v, int) for v in values
            )
            table.add_column(column.label, justify="right" if numeric else "left")
        for row in section.rows:
            table.add_row(*(_text(v) for v in row))
        console.print(table)
        console.print()
