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
| cure53/DOMPurify README and `LICENSE` | Apache-2.0 (the `LICENSE` file read 2026-10-20 is the Apache License 2.0 text; the README was read for facts only) | Sanitise last, mutation caveat, allow-lists, update cadence, server-side DOM, default URI schemes, hook caveat (§1.3.3, §1.3.5, §1.3.11, §1.3.12) |
| WHATWG HTML Standard, link types (noopener, noreferrer), read 2026-10-20 through a summarising fetcher | CC BY 4.0 (WHATWG) | A new-tab target implies no-opener; no-referrer is the extra effect (§1.3.5) |
| W3C WCAG 2.2 Understanding SC 1.1.1, read 2026-10-20; W3C UI Events (composition events), read 2026-10-20 | W3C document licence, facts only | Text alternatives and decorative images (§1.3.6); composition sessions and the composing flag (§2.5.5) |
| W3C ARIA Authoring Practices Guide, toolbar pattern and button pattern, read 2026-10-20 | W3C document licence, facts only | One tab stop for a toolbar, arrow keys inside, three-controls guidance, toggle button with `aria-pressed` and a label that does not change (§2.4.3, §2.4.4) |
| W3C WAI-ARIA 1.2, definitions of `aria-multiline` and the `status` role, read 2026-10-20 | W3C document licence, facts only | Multi-line text box property, status as an advisory live region (§2.4.1, §2.4.5) |

## Own craft, not from a source
Storage format trade-offs and versioning, sanitise-on-write-and-render, paste rules, limits on the projection, mentions as references and their notification timing, versions against live co-editing, snapshots, undo per user, read-only rendering, accessibility checklist beyond the cited facts, tests and framework pointers.

## Removed
Allow-list contents and sanitiser options (`csp-and-sanitiser-pitfalls`), file upload handling (its own block), library installation and plugin code, hosted collaboration products.

## Verified on the second pass, 2026-10-20
4 verified (toolbar keyboard model, toggle button state, multi-line property, status role), 1 corrected (the multi-line point is a property of the text box role, not a separate role; toggle labels must stay constant), 0 deleted. Sanitising, storage and paste points are security and design practice, not re-read here (see the sanitiser block).

## Verified on the third pass, 2026-10-20
5 sourced (sanitise last, default URI schemes, sanitiser upkeep and server DOM, composition sessions, alternative text), 2 corrected (§1.3.5: the extra `rel` is for the referrer, not the opener; §1.3.6: decoration needs an explicit empty alternative, not a required text), 0 deleted. Two points added (§1.3.11, §1.3.12). The Lexical documentation was not re-read. Hostile sample lists, storage format trade-offs, paste rules, mention timing and the collaboration role split stay own craft: no permissive source found, searched: the repositories and pages above. One licence note: the DOMPurify `LICENSE` read showed only the Apache 2.0 text with a blank copyright template, so no copyright line is recorded.

## Not verified
1. **Library facts** (clipboard order, Tab and Escape contract, listbox wiring, collaboration options) are the documentation's claims at the commit; none was run.
2. **Threat model statements** are the project's claims; no protocol was tested.
3. **WCAG points** (contrast and zoom, alternative text on images, live-region politeness wording) were recalled from public practice, not re-read; the toolbar, toggle button, multi-line and status points were re-read. Re-read before relying.
4. **Framework pointers** name features from memory; no version was checked.
5. **No number** (limits, sizes, timeouts) is stated; none was measured.
