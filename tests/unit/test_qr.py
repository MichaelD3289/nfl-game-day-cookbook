from pathlib import Path

from nfl_book.qr import generate_qr_codes, qr_png, write_qr


def test_qr_is_deterministic() -> None:
    assert qr_png("https://sho.rt/abc") == qr_png("https://sho.rt/abc")
    assert qr_png("https://sho.rt/abc") != qr_png("https://sho.rt/abd")
    assert qr_png("https://sho.rt/abc").startswith(b"\x89PNG")


def test_write_qr_skips_identical_bytes(tmp_path: Path) -> None:
    path = tmp_path / "q.png"
    assert write_qr(path, "https://sho.rt/1") is True
    assert write_qr(path, "https://sho.rt/1") is False
    assert write_qr(path, "https://sho.rt/2") is True


def test_generate_qr_codes_media_keys(tmp_path: Path) -> None:
    media = generate_qr_codes([("recipe", "r1", "https://sho.rt/1")], tmp_path, "../qr")
    assert media == {"recipe:r1": "../qr/recipe-r1.png"}
    assert (tmp_path / "recipe-r1.png").is_file()
