# D. Share one build entry point and one Quarto adapter across all targets

The book, cards, booklets, website, EPUB and preview each repeat load → resolve → media and their own Quarto call. Because of that, they have three different error contracts and two sources for the edition version. **From code:**

- `render/quarto.render_pdf` raises a bare `BookError` that names no file, which breaks AGENTS.md rule 7.
- `website.py` and `epub.py` read the version from `pyproject.toml`, but `render/pages.py:165, 181, 264` use `__version__` from installed metadata. If the installed package is out of date, QR codes and edition links can point at a different version than the site footer. My judgment, not observed.
- Division booklets rebuild `Project` with a different `generated_dir` (`pipeline.py:195-201`), which moves `qr_dir` and `photo_cache_dir` (`project.py:99-105`) into each booklet's folder, so the photo cache isn't shared.

### Now and wanted

**From code:**

- The load/resolve/media steps are repeated in `pipeline.py:92-122, 186-238`, `cards.py:20-104`, `digital.py:22-65`, `epub.py:99-200`, `preview.py:37-80` and `stats.py:306-311`.
- `website.py:509` calls `load()` a second time just to read settings.
- `cards.py:56-89` copies `assemble`'s page and manifest loop.
- Tests monkeypatch `shutil.which` and `subprocess.run` inside each module (`test_website.py:91-138`, `test_epub.py:145-153`).
- `build_website` hard-codes its navigation twice (`website.py:267-274`, `596-619`) and keeps three asset lists that must match (`539-573`, `650-652`).

Wanted:

- `published_edition(project, build_dir, division=None, include=published)` returns `Edition(settings, model, media, version, diagnostics)`. It reads the version from `pyproject.toml`, once.
- A Quarto runner is passed in as a dependency, with the real runner by default and a fake in tests. It reports a missing binary or a failed render through Diagnostics, naming the document and including the end of the log. Book, cards, booklets, website, EPUB and preview all use it.
- `qr_dir` and `photo_cache_dir` always sit under the root `generated/`.
- Cards use `assemble`.
- `build_website` takes its navigation and assets from one navigation definition and one asset table, and builds its Quarto config with a pure function.

### Done when

- With the fake runner, a test shows that a missing `quarto` and a failed render each produce a Diagnostics error naming the document, for PDF, website and EPUB.
- No test monkeypatches `subprocess` or `shutil.which` in a build module.
- `rg -n 'pyproject.toml' src/nfl_book` finds one read, and `render/pages.py` no longer uses `__version__` for edition URLs.
- Building two booklets reuses one photo cache: the second booklet reports cache hits in `PhotoStats`.
- `rg -n '\bload\(' src/nfl_book/website.py` finds no second load.
- Adding an asset to the asset table is enough for it to appear in `resources`, be copied and get a script tag. A test shows this.
- `make check` passes, and `make pdf` and the website build succeed locally with Quarto installed.

### Context

- CHANGELOG `Fixed`: Quarto errors name the document, and edition links and the footer use the same version.
- CHANGELOG `Changed`: booklets share the book's photo and QR cache.

### Watch out for

Moving `qr_dir` changes the paths booklet QMD files reference. Check that booklet PDFs still find their QR images.
