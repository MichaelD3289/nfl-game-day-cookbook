"""Offline EPUB package, navigation, and resource checks (not EPUBCheck)."""

import posixpath
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlsplit
from zipfile import ZIP_STORED, BadZipFile, ZipFile

from nfl_book.errors import Diagnostics


def check_epub(path: Path, diags: Diagnostics, expected: set[str] | None = None) -> None:
    try:
        with ZipFile(path) as archive:
            names = set(archive.namelist())
            if archive.read("mimetype") != b"application/epub+zip":
                raise ValueError("Invalid mimetype")
            first = archive.infolist()[0]
            if first.filename != "mimetype" or first.compress_type != ZIP_STORED:
                raise ValueError("mimetype must be first and uncompressed")
            container = ET.fromstring(archive.read("META-INF/container.xml"))
            rootfile = container.find(".//{*}rootfile")
            if rootfile is None:
                raise ValueError("Missing package rootfile")
            package_path = rootfile.attrib["full-path"]
            package = ET.fromstring(archive.read(package_path))
            manifest = {i.attrib["id"]: i for i in package.findall(".//{*}manifest/{*}item")}
            if not any("nav" in i.get("properties", "").split() for i in manifest.values()):
                raise ValueError("Missing EPUB navigation document")
            for item in manifest.values():
                target = posixpath.normpath(
                    posixpath.join(posixpath.dirname(package_path), unquote(item.attrib["href"]))
                )
                if target not in names:
                    raise ValueError(f"Missing manifest resource: {target}")
            for ref in package.findall(".//{*}spine/{*}itemref"):
                if ref.get("idref") not in manifest:
                    raise ValueError("Spine references missing manifest item")
            docs = {n: ET.fromstring(archive.read(n)) for n in names if n.endswith(".xhtml")}
            ids = {}
            for name, doc in docs.items():
                values = [e.attrib["id"] for e in doc.iter() if "id" in e.attrib]
                if len(values) != len(set(values)):
                    raise ValueError(f"Duplicate anchor in {name}")
                ids[name] = set(values)
            missing = (expected or set()) - set().union(*ids.values())
            if missing:
                raise ValueError(f"Missing content anchors: {sorted(missing)}")
            for name, doc in docs.items():
                for element in doc.iter():
                    for attribute in ("href", "src"):
                        value = element.get(attribute)
                        if not value:
                            continue
                        url = urlsplit(value)
                        if url.scheme or url.netloc:
                            if attribute == "src":
                                raise ValueError(f"Non-embedded resource: {value}")
                            continue
                        target = (
                            posixpath.normpath(
                                posixpath.join(posixpath.dirname(name), unquote(url.path))
                            )
                            if url.path
                            else name
                        )
                        if target not in names:
                            raise ValueError(f"{name}: missing resource {value}")
                        if url.fragment and unquote(url.fragment) not in ids.get(target, set()):
                            raise ValueError(f"{name}: missing link target {value}")
    except (OSError, BadZipFile, ET.ParseError, KeyError, ValueError, IndexError) as exc:
        diags.error("epub-package", str(exc), path)
