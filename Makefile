# Thin wrappers around the nfl-book CLI and dev tools. Everything runs via uv.
.PHONY: book check links preview pdf website epub test lint format hooks clean browser-test website-audit website-performance

UV ?= uv
BOOK = $(UV) run nfl-book
SITE ?= dist/site
REPORTS ?= website-reports

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

epub:
	$(BOOK) epub

website:
	$(BOOK) website

test:
	$(UV) run pytest

# Formatting hooks from .pre-commit-config.yaml (Ruff for Python, Prettier for Markdown,
# YAML, JSON, JS and CSS) on every file. They fix files in place and fail when they had
# to, so rerun after reviewing the diff.
lint:
	$(UV) run pre-commit run --all-files --show-diff-on-failure
	$(UV) run mypy src tests

format:
	$(UV) run pre-commit run --all-files

# Run the formatting hooks on staged files at every commit.
hooks:
	$(UV) run pre-commit install

clean:
	$(BOOK) clean

# Install npm dependencies and Chromium explicitly before running these local checks.
browser-test:
	npm test
	NFL_BROWSER_TESTS=1 $(UV) run pytest tests/integration/test_website_browser.py

website-audit:
	$(UV) run python scripts/website_audit.py "$(SITE)" --report "$(REPORTS)/accessibility.json"

website-performance:
	$(UV) run python scripts/website_audit.py "$(SITE)" --performance --report "$(REPORTS)/performance.json"
