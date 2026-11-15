# NFL Game Day Cookbook

This is the shared language for the cookbook's content and its builds: the print book, recipe cards, division booklets, the website and the EPUB.

## Content

**Published**:
The status that lets a recipe, component or menu reach a production build and get a page on the website.
_Avoid_: live, released, public

**Included content**:
The recipes, components and menus that one build admits, decided by status and, for a division booklet, by division.
_Avoid_: visible content, active content

## Builds

**Edition**:
One versioned build of the book: its settings, its included content, its media and its version number. Every build target renders an edition.
_Avoid_: release (that is the tagged version), build (that is the process)

**Page view**:
The data one page shows for one item or listing, prepared once for a given output format.
_Avoid_: context, page data

**Address**:
Every way to point at an item: its cross-reference label, slug, page and website URL.
_Avoid_: link, ref, route
