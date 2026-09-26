"""Deterministic QR codes for short URLs, written to ``generated/qr``."""

from __future__ import annotations

import io
from collections.abc import Iterable
from pathlib import Path

import qrcode
from qrcode.constants import ERROR_CORRECT_M


def qr_png(url: str) -> bytes:
    code = qrcode.QRCode(error_correction=ERROR_CORRECT_M, box_size=10, border=2)
    code.add_data(url)
    code.make(fit=True)
    buffer = io.BytesIO()
    code.make_image(fill_color="black", back_color="white").save(buffer, format="PNG")
    return buffer.getvalue()


def write_qr(path: Path, url: str) -> bool:
    """Write the PNG only if its bytes changed; return True when written."""
    data = qr_png(url)
    if path.is_file() and path.read_bytes() == data:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return True


def generate_qr_codes(
    items: Iterable[tuple[str, str, str]], qr_dir: Path, relative_to: str = "../qr"
) -> dict[str, str]:
    """``items`` are (kind, id, short_url); returns media keys -> relative paths."""
    media = {}
    for kind, item_id, short_url in items:
        name = f"{kind}-{item_id}.png"
        write_qr(qr_dir / name, short_url)
        media[f"{kind}:{item_id}"] = f"{relative_to}/{name}"
    return media
