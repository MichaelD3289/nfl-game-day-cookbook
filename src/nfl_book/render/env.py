"""Jinja environment for generating Quarto (QMD) fragments.

Delimiters are ``<< >>`` / ``<% %>`` / ``<# #>`` so that LaTeX braces and
Quarto shortcodes (``{{< include >}}``) can be written literally in templates.
"""

from __future__ import annotations

import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

TEX_SPECIALS = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}
TEX_RE = re.compile("|".join(re.escape(c) for c in TEX_SPECIALS))
URL_RE = re.compile(r"[\\%#{}]")


def tex(value: object) -> str:
    """Escape plain text for use inside a LaTeX macro argument."""
    if value is None:
        return ""
    return TEX_RE.sub(lambda m: TEX_SPECIALS[m.group()], str(value))


def tex_url(value: object) -> str:
    """Escape a URL for the first argument of ``\\href``."""
    if value is None:
        return ""
    return URL_RE.sub(lambda m: "\\" + m.group(), str(value))


def make_env(templates_dir: Path) -> Environment:
    env = Environment(
        loader=FileSystemLoader(templates_dir),
        block_start_string="<%",
        block_end_string="%>",
        variable_start_string="<<",
        variable_end_string=">>",
        comment_start_string="<#",
        comment_end_string="#>",
        undefined=StrictUndefined,
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=False,
    )
    env.filters["tex"] = tex
    env.filters["tex_url"] = tex_url
    return env
