"""Text helpers shared by the digital formats (website and EPUB)."""

from __future__ import annotations

import json
import re
from urllib.parse import urlsplit

# The print cover marks Quick options with a LaTeX macro; each format spells it its own way.
PRINT_Q_MARK = r"`\QMark{}\ `{=latex}"
WEBSITE_Q_MARK = "[Q]{.q-mark}"
EPUB_Q_MARK = "**Q** "

_PRINT_ONLY_BLOCK = re.compile(r"```\{=latex\}\n.*?\n```", re.DOTALL)
_FENCE_LINE = re.compile(r"(?m)^(:{3,}[^\n]*)$")


def escape_markdown(text: str) -> str:
    """Escape plain text used in Markdown (rich authored body text passes through)."""
    return re.sub(r"([\\`*_{}\[\]<>#|])", r"\\\1", text)


def digital_prose(text: str, q_mark: str) -> str:
    """Authored text without its print-only LaTeX; the Q mark becomes ``q_mark``."""
    return _PRINT_ONLY_BLOCK.sub("", text.replace(PRINT_Q_MARK, q_mark))


def separate_fences(body: str) -> str:
    """Put a blank line around every ``:::`` fence so Pandoc reads it as a div."""
    return _FENCE_LINE.sub(r"\n\1\n", body)


def site_name(url: str) -> str:
    """``https://www.example.com/a/b`` -> ``example.com``: link text for an untitled source."""
    host = urlsplit(url).hostname or url
    return host.removeprefix("www.")


def json_script(data: object) -> str:
    """JSON for a one-line <script> element: no newlines, and no "</" to close it early."""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
