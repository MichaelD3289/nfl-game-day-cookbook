"""Assemble the Pages site: the newest release at the root and every kept one in /vX.Y.Z/.

GitHub Pages serves only the latest deployment, so each release deploys all versions
together. The release workflow downloads earlier releases into an archive folder:
``<tag>.json`` (``gh release view --json tagName,publishedAt,assets``) and, when the
release has one, ``<tag>/nfl-game-day-website.zip``. This module works offline on
that folder plus the fresh build, and prints the tag served at the site root.

Images under each build's ``assets/`` are stored once in ``media/``, named by a hash of
their contents, and every version's pages link to that copy. Release ZIPs are untouched.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import sys
import zipfile
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import unquote, urlsplit

from nfl_book.errors import Diagnostics
from nfl_book.publishing import RELEASES
from nfl_book.release_policy import STABLE
from nfl_book.website_check import check_site

WEBSITE_ZIP = "nfl-game-day-website.zip"
VERSIONS_MARKER = "<!-- site-versions -->"
# Pages sites are capped at about 1 GB.
SIZE_WARNING = 800 * 1024 * 1024
MEDIA = "media"
# Attributes that carry URLs, and CSS url(...) in style attributes, <style> and .css files.
URL_ATTRIBUTE = re.compile(
    r"""(\b(?:src|href|content|poster|data-src)\s*=\s*)(["'])(.*?)\2""", re.I | re.S
)
SRCSET = re.compile(r"""(\bsrcset\s*=\s*)(["'])(.*?)\2""", re.I | re.S)
CSS_URL = re.compile(r"""(url\(\s*)(["']?)([^"')\s]+)\2(\s*\))""", re.I)
NOINDEX = '<meta name="robots" content="noindex">'
BANNER_STYLE = (
    "position:fixed;left:0;right:0;bottom:0;z-index:2000;padding:.5rem 1rem;"
    "background:#fff3cd;color:#3d2e00;border-top:1px solid #e0c36b;text-align:center"
)


@dataclass(frozen=True)
class Edition:
    tag: str
    date: str
    pdf: str | None
    epub: str | None = None


def _version(tag: str) -> tuple[int, int, int] | None:
    match = STABLE.fullmatch(tag)
    return (int(match[1]), int(match[2]), int(match[3])) if match else None


def _editions(
    archive: Path, pdf: str, diags: Diagnostics, epub: str | None = None
) -> dict[str, tuple[Edition, bool]]:
    """Stable releases by tag, with whether each one published a website ZIP."""
    found = {}
    for path in sorted(archive.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            tag = str(data["tagName"])
            names = {str(asset["name"]) for asset in data.get("assets", [])}
        except (OSError, ValueError, KeyError, TypeError) as error:
            diags.warning("site-archive", f"Unreadable release metadata: {error}", path)
            continue
        if _version(tag) is None:
            continue
        date = str(data.get("publishedAt") or "")[:10]
        link = f"{RELEASES}/download/{tag}/{pdf}" if pdf in names else None
        book = f"{RELEASES}/download/{tag}/{epub}" if epub and epub in names else None
        found[tag] = (Edition(tag, date, link, book), WEBSITE_ZIP in names)
    return found


def _extract(bundle: Path, target: Path) -> str | None:
    """Unpack a website ZIP; return why it is unusable, or None."""
    try:
        with zipfile.ZipFile(bundle) as archive:
            for name in archive.namelist():
                parts = PurePosixPath(name).parts
                if name.startswith(("/", "\\")) or ".." in parts or ":" in name:
                    return f"unsafe path in ZIP: {name}"
            broken = archive.testzip()
            if broken is not None:
                return f"corrupt ZIP member: {broken}"
            archive.extractall(target)
    except (OSError, zipfile.BadZipFile, EOFError) as error:
        return f"unreadable ZIP: {error}"
    if not (target / "index.html").is_file():
        return "ZIP has no index.html"
    return None


def _mark(folder: Path, tag: str, latest: Path, *, archived: bool) -> None:
    """Add noindex to every page; older editions also get a banner and their own PDF."""
    for page in folder.rglob("*.html"):
        text = page.read_text(encoding="utf-8")
        text = re.sub(r"(<head\b[^>]*>)", rf"\1\n{NOINDEX}", text, count=1, flags=re.I)
        if archived:
            relative = page.relative_to(folder)
            up = "../" * len(relative.parts)
            same = relative.as_posix() if (latest / relative).is_file() else "index.html"
            banner = (
                f'<div class="archived-version" role="note" style="{BANNER_STYLE}">'
                f"You're viewing {html.escape(tag)}. "
                f'<a href="{up}{same}">See the latest version →</a></div>'
                "<style>body{padding-bottom:3rem}</style>"
            )
            text = re.sub(r"(<body\b[^>]*>)", rf"\1\n{banner}", text, count=1, flags=re.I)
            text = text.replace(f"{RELEASES}/latest/download/", f"{RELEASES}/download/{tag}/")
        page.write_text(text, encoding="utf-8")


def _share_media(out: Path, builds: dict[Path, list[Path]]) -> None:
    """Move every build's ``assets/`` into ``media/<sha256><ext>`` and relink its pages.

    ``builds`` maps each build folder to the version folders nested inside it (the root
    build contains them all), whose files belong to those versions instead.
    """
    media = out / MEDIA
    media.mkdir(exist_ok=True)
    used: set[str] = set()
    for build, nested in builds.items():
        shared: dict[Path, Path] = {}
        assets = build / "assets"
        for path in sorted(p for p in assets.rglob("*") if p.is_file()):
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            target = media / f"{digest}{path.suffix.lower()}"
            if target.exists():
                path.unlink()
            else:
                path.replace(target)
            shared[path.resolve()] = target
        if assets.is_dir():
            shutil.rmtree(assets)
        skip = [*nested, media]
        for page in build.rglob("*"):
            if not page.is_file() or any(page.is_relative_to(n) for n in skip):
                continue
            if page.suffix in (".html", ".css"):
                text = page.read_text(encoding="utf-8")
                relinked = _relink(text, page, shared, used)
            elif page.name == "search.json":
                text = page.read_text(encoding="utf-8")
                index = json.loads(text)
                data = _relink_json(index, build / "index.html", shared, used)
                relinked = text if data == index else json.dumps(data, ensure_ascii=False)
            else:
                continue
            if relinked != text:
                page.write_text(relinked, encoding="utf-8")
    for path in media.iterdir():
        if path.name not in used:
            path.unlink()


def _shared(url: str, page: Path, shared: dict[Path, Path], used: set[str]) -> str:
    """The media link replacing ``url`` from ``page``, or ``url`` itself."""
    parts = urlsplit(html.unescape(url))
    if parts.scheme or parts.netloc or not parts.path or parts.path.startswith("/"):
        return url
    target = shared.get((page.parent / unquote(parts.path)).resolve())
    if target is None:
        return url
    used.add(target.name)
    return os.path.relpath(target, page.parent).replace(os.sep, "/")


def _relink(text: str, page: Path, shared: dict[Path, Path], used: set[str]) -> str:
    def attribute(match: re.Match[str]) -> str:
        return match[1] + match[2] + _shared(match[3], page, shared, used) + match[2]

    def srcset(match: re.Match[str]) -> str:
        candidates = []
        for candidate in match[3].split(","):
            url, _, size = candidate.strip().partition(" ")
            candidates.append(" ".join(filter(None, [_shared(url, page, shared, used), size])))
        return match[1] + match[2] + ", ".join(candidates) + match[2]

    def css(match: re.Match[str]) -> str:
        return match[1] + match[2] + _shared(match[3], page, shared, used) + match[2] + match[4]

    text = CSS_URL.sub(css, text)
    if page.suffix == ".html":
        text = SRCSET.sub(srcset, URL_ATTRIBUTE.sub(attribute, text))
    return text


def _relink_json(data: Any, page: Path, shared: dict[Path, Path], used: set[str]) -> Any:
    """Relink asset paths in Quarto's search index (relative to the build root)."""
    if isinstance(data, str):
        return _shared(data, page, shared, used) if "assets/" in data else data
    if isinstance(data, list):
        return [_relink_json(item, page, shared, used) for item in data]
    if isinstance(data, dict):
        return {key: _relink_json(value, page, shared, used) for key, value in data.items()}
    return data


def _version_list(editions: list[Edition], root: str, prefix: str) -> str:
    items = []
    for edition in editions:
        href = "index.html" if edition.tag == root else f"{edition.tag}/index.html"
        label = f'<a href="{prefix}{href}">{edition.tag}</a>'
        if edition.tag == root:
            label += " (latest)"
        if edition.date:
            label += f" · {edition.date}"
        if edition.pdf:
            label += f' · <a href="{edition.pdf}">PDF</a>'
        if edition.epub:
            label += f' · <a href="{edition.epub}">EPUB</a>'
        items.append(f"<li>{label}</li>")
    return '<ul class="site-versions">\n' + "\n".join(items) + "\n</ul>"


def assemble(
    tag: str,
    site: Path,
    archive: Path,
    out: Path,
    pdf: str,
    diags: Diagnostics,
    epub: str | None = None,
) -> str | None:
    """Build ``out`` and return the tag served at its root (None when nothing is kept).

    ``tag`` is the release just built into ``site``. The root is always the newest
    stable version available, so rebuilding an older tag never puts older content
    there. The caller still compares the root with the newest stable tag, because a
    missing or corrupt newest ZIP leaves an older version as the newest available.
    """
    if out.exists():
        diags.error("site-archive", "Output folder already exists; remove it first.", out)
        return None
    editions = _editions(archive, pdf, diags, epub)
    out.mkdir(parents=True)
    kept: list[Edition] = []
    if _version(tag) is not None:
        if (site / "index.html").is_file():
            shutil.copytree(site, out / tag)
            kept.append(editions.get(tag, (Edition(tag, "", None), True))[0])
        else:
            diags.warning("site-archive", "Fresh website build has no index.html.", site)
    for other, (edition, has_zip) in editions.items():
        if other == tag or not has_zip:
            continue
        bundle = archive / other / WEBSITE_ZIP
        if not bundle.is_file():
            diags.warning("site-archive", f"Website ZIP for {other} was not downloaded.", bundle)
            continue
        problem = _extract(bundle, out / other)
        if problem:
            shutil.rmtree(out / other, ignore_errors=True)
            diags.warning("site-archive", f"Skipping {other}: {problem}", bundle)
            continue
        kept.append(edition)
    if not kept:
        return None
    kept.sort(key=lambda e: _version(e.tag) or (0, 0, 0), reverse=True)
    root = kept[0].tag
    latest = out / root
    # The root copy of the latest edition is the one search engines should index.
    for item in latest.iterdir():
        if item.is_dir():
            shutil.copytree(item, out / item.name)
        else:
            shutil.copyfile(item, out / item.name)
    for edition in kept:
        _mark(out / edition.tag, edition.tag, latest, archived=edition.tag != root)
    for page in out.rglob("versions.html"):
        text = page.read_text(encoding="utf-8")
        if VERSIONS_MARKER in text:
            prefix = "../" * (len(page.relative_to(out).parts) - 1)
            text = text.replace(VERSIONS_MARKER, _version_list(kept, root, prefix))
            page.write_text(text, encoding="utf-8")
    builds = {out: [out / e.tag for e in kept]}
    builds.update({out / e.tag: [] for e in kept})
    _share_media(out, builds)
    check_site(out, diags)
    size = sum(p.stat().st_size for p in out.rglob("*") if p.is_file())
    if size > SIZE_WARNING:
        diags.warning(
            "site-archive",
            f"Pages site is {size // 2**20} MB, close to the 1 GB Pages limit.",
            out,
        )
    return root


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", required=True, help="tag of the fresh build")
    parser.add_argument("--site", type=Path, required=True, help="fresh website build")
    parser.add_argument("--archive", type=Path, required=True, help="downloaded releases")
    parser.add_argument("--out", type=Path, required=True, help="Pages folder to create")
    parser.add_argument("--pdf", required=True, help="PDF asset name")
    parser.add_argument("--epub", help="EPUB asset name (editions before the EPUB have none)")
    args = parser.parse_args(argv)
    diags = Diagnostics()
    root = assemble(args.tag, args.site, args.archive, args.out, args.pdf, diags, args.epub)
    annotate = os.environ.get("GITHUB_ACTIONS") == "true"
    for item in diags:
        prefix = f"::{item.severity.value}::" if annotate else ""
        print(prefix + item.format(), file=sys.stderr)
    print(root or "")
    return 0 if diags.ok else 1


if __name__ == "__main__":
    sys.exit(main())
