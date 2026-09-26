"""Front matter + ``##`` section splitting for authored Markdown documents."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import frontmatter
import yaml

SECTION_RE = re.compile(r"^##\s+(?P<title>.+?)\s*#*\s*$")
FENCE_RE = re.compile(r"^(```|~~~)")


class DocumentError(Exception):
    pass


@dataclass(frozen=True)
class Document:
    path: Path
    meta: dict[str, Any]
    body: str


def read_document(path: Path) -> Document:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise DocumentError("file is not valid UTF-8") from exc
    if not text.lstrip().startswith("---"):
        raise DocumentError("missing YAML front matter (file must start with ---)")
    try:
        post = frontmatter.loads(text)
    except yaml.YAMLError as exc:
        raise DocumentError(f"invalid YAML front matter: {exc}") from exc
    if not isinstance(post.metadata, dict):
        raise DocumentError("front matter must be a mapping")
    return Document(path, dict(post.metadata), post.content)


def split_sections(body: str) -> tuple[str, dict[str, str], list[str]]:
    """Split ``body`` on level-2 headings.

    Returns ``(preamble, sections, duplicates)``: text before the first
    ``##`` heading, a mapping of heading title -> stripped section text, and
    any heading titles that appeared more than once.
    """
    preamble: list[str] = []
    sections: dict[str, list[str]] = {}
    duplicates: list[str] = []
    current: list[str] = preamble
    in_fence = False
    for line in body.splitlines():
        if FENCE_RE.match(line.strip()):
            in_fence = not in_fence
        match = None if in_fence else SECTION_RE.match(line)
        if match:
            title = match["title"].strip()
            if title in sections:
                duplicates.append(title)
            current = sections.setdefault(title, [])
            continue
        current.append(line)
    return (
        "\n".join(preamble).strip(),
        {k: "\n".join(v).strip() for k, v in sections.items()},
        duplicates,
    )
