from nfl_book.render.env import tex, tex_url


def test_tex_escapes_specials() -> None:
    assert tex("50% & $5 #1 a_b {x} ~ ^") == (
        r"50\% \& \$5 \#1 a\_b \{x\} \textasciitilde{} \textasciicircum{}"
    )


def test_tex_escapes_backslash_once() -> None:
    assert tex("a\\b") == r"a\textbackslash{}b"


def test_tex_none() -> None:
    assert tex(None) == ""


def test_tex_url_keeps_url_but_escapes_hash_and_percent() -> None:
    assert tex_url("https://x.org/a?b=1&c=%20#frag") == r"https://x.org/a?b=1&c=\%20\#frag"
