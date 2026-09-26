# Thin wrappers around the nfl-book CLI and dev tools. Everything runs via uv.
.PHONY: check preview pdf test lint clean

UV ?= uv
BOOK = $(UV) run nfl-book

check: lint test
	$(BOOK) validate

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
