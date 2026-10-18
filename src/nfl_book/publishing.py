"""Where releases are published, and the names of the files every release attaches."""

from uuid import NAMESPACE_URL, uuid5

REPOSITORY = "https://github.com/MichaelD3289/nfl-game-day-cookbook"
RELEASES = f"{REPOSITORY}/releases"
EPUB_FILENAME = "nfl-game-day-cookbook.epub"
# The same for every edition, so reading apps treat a new edition as an update of the
# book already in the library rather than a second copy.
EPUB_IDENTIFIER = f"urn:uuid:{uuid5(NAMESPACE_URL, REPOSITORY)}"


BOOKLET_FILENAME_PREFIX = "nfl-game-day-recipe-booklet"


def booklet_filename(division_key: str) -> str:
    """Stable release asset name for a configured division key."""
    return f"{BOOKLET_FILENAME_PREFIX}-{division_key}.pdf"
