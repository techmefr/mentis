# rich-text-editor-pitfalls: origin and source stamps

> Provenance of `skills/rich-text-editor-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** No editor was built, run or tested while writing it. Read date: 2026-10-20.

## Sources (rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| facebook/lexical at commit ee98bf4 (docs: serialization, concepts/keyboard-accessibility, collaboration/faq) | MIT, Copyright (c) Meta Platforms, Inc. and affiliates (`LICENSE` read 2026-10-20) | JSON tree against HTML and Markdown outputs, clipboard order, Tab and Escape contract, toolbar tab stop, typeahead listbox wiring, two source-of-truth options for collaboration |
| yjs/yjs at commit 47a4940 (`THREAT_MODEL.md`) | MIT (`LICENSE` read 2026-10-20) | Trusted-peer assumption, malicious write peers, fork for suggestion-only users, server-side filtering as antipattern, update size limits |
| ueberdosis/tiptap at commit 664d82a | MIT, Copyright (c) 2025 Tiptap GmbH (`LICENSE.md` read 2026-10-20) | Nothing used: the repository documents only point to a hosted collaboration service, so no rule rests on it |

## Own craft, not from a source
Storage format trade-offs and versioning, sanitise-on-write-and-render, paste rules, limits on the projection, mentions as references and their notification timing, versions against live co-editing, snapshots, undo per user, read-only rendering, accessibility checklist beyond the cited facts, tests and framework pointers.

## Removed
Allow-list contents and sanitiser options (`csp-and-sanitiser-pitfalls`), file upload handling (its own block), library installation and plugin code, hosted collaboration products.

## Not verified
1. **Library facts** (clipboard order, Tab and Escape contract, listbox wiring, collaboration options) are the documentation's claims at the commit; none was run.
2. **Threat model statements** are the project's claims; no protocol was tested.
3. **ARIA and WCAG points** beyond the library facts were recalled from public practice, not re-read. Re-read before relying.
4. **Framework pointers** name features from memory; no version was checked.
5. **No number** (limits, sizes, timeouts) is stated; none was measured.
