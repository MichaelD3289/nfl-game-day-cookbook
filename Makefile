# Thin wrappers around the nfl-book CLI and dev tools. Everything runs via uv.
.PHONY: book check links preview pdf test lint clean

UV ?= uv
BOOK = $(UV) run nfl-book

# Full book from a fresh checkout: short links (network), then validate + PDF.
# Run sequentially so links are cached before the build validates them.
book:
	$(MAKE) links
	$(MAKE) pdf

check: lint test
	$(BOOK) validate

# Only networked target: TinyURL short links for every non-retired recipe/component
# source not yet in data/shortlinks.yml. Commit that file afterwards.
links:
	$(BOOK) prepare-links

# make preview FILE=recipes/afc/east/bills/<id>.md
preview:
	@test -n "$(FILE)" || { echo "usage: make preview FILE=path/to/recipe-or-component.md"; exit 2; }
	$(BOOK) preview $(FILE)

pdf:
	$(BOOK) build

test:
	$(UV) run pytest

lint:
	$(UV) run ruff format --check src tests
	$(UV) run ruff check src tests
	$(UV) run mypy src tests

clean:
	$(BOOK) clean
