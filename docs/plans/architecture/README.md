# Architecture deepening tickets

These tickets came from an architecture review of `src/nfl_book` on 2026-11-14, against `main` at `b27c1ab`. They are not filed as GitHub issues. To start one, file it and claim it under AGENTS.md rule 15, or ask the maintainer. Terms such as _included content_, _edition_, _page view_ and _address_ are defined in [`GLOSSARY.md`](../../../GLOSSARY.md).

Work them in this order:

| Ticket                                                                                         | Blocked by |
| ---------------------------------------------------------------------------------------------- | ---------- |
| [A. Keep drafts and retired items out of production build models](a-included-content-model.md) | –          |
| [B. Give every labelled item one address](b-item-addresses.md)                                 | –          |
| [C. Build each page from typed data once](c-typed-page-views.md)                               | A, B       |
| [D. Share one build entry point and one Quarto adapter](d-edition-and-quarto-adapter.md)       | –          |
| [E. Test the Python → JS website payloads against the real JS](e-js-payload-contract.md)       | C          |

Line references point at `b27c1ab`. Check them again before you start, because the code may have moved.
