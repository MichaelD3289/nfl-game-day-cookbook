"""Version-controlled shortlink cache (``data/shortlinks.yml``).

The canonical source URL is always the full URL authored in front matter.
Short URLs are derived data cached here so builds stay offline and stable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from nfl_book.errors import BookError
from nfl_book.models.common import check_url

HEADER = """\
# Version-controlled shortlink cache: canonical source URL -> short URL.
#
# Filled ONLY by `uv run nfl-book prepare-links` (the one network stage).
# Normal builds read this file and never touch the network.
# Commit changes: the short URL is the stable identity printed in the book.
"""


@dataclass
class ShortlinkCache:
    path: Path
    links: dict[str, str] = field(default_factory=dict)

    @classmethod
    def load(cls, path: Path) -> ShortlinkCache:
        if not path.is_file():
            return cls(path)
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            raise BookError(f"{path}: invalid YAML: {exc}") from exc
        links = data.get("links") if isinstance(data, dict) else None
        if links is None:
            links = {}
        if not isinstance(links, dict) or not all(
            isinstance(k, str) and isinstance(v, str) for k, v in links.items()
        ):
            raise BookError(f"{path}: `links` must map full URL strings to short URL strings")
        for full, short in links.items():
            for url in (full, short):
                try:
                    check_url(url)
                except ValueError as exc:
                    raise BookError(f"{path}: {exc}") from exc
        return cls(path, dict(links))

    def get(self, full_url: str) -> str | None:
        return self.links.get(full_url)

    def __contains__(self, full_url: object) -> bool:
        return full_url in self.links

    def add(self, full_url: str, short_url: str) -> None:
        """Record a new mapping. Existing mappings are never replaced."""
        check_url(short_url)
        existing = self.links.get(full_url)
        if existing is not None and existing != short_url:
            raise BookError(
                f"refusing to replace cached short URL for {full_url} "
                f"({existing} -> {short_url}); edit {self.path.name} by hand if intended"
            )
        self.links[full_url] = short_url

    def dump(self) -> str:
        body = yaml.safe_dump(
            {"links": dict(sorted(self.links.items()))},
            sort_keys=False,
            allow_unicode=True,
            width=1000,
        )
        return HEADER + body

    def save(self) -> bool:
        """Write deterministically; return True if the file changed."""
        text = self.dump()
        if self.path.is_file() and self.path.read_text(encoding="utf-8") == text:
            return False
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(text, encoding="utf-8")
        return True
