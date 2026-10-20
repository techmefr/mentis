# comments-and-activity-feed-pitfalls: origin and source stamps

> Provenance of `skills/comments-and-activity-feed-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** No comment thread or feed was built, run or tested while writing it. Read date: 2026-10-20.

## Sources

| Source | Licence | What it gave |
|---|---|---|
| W3C WAI-ARIA Authoring Practices, feed pattern (https://www.w3.org/WAI/ARIA/apg/patterns/feed/) | W3C document licence (liability, trademark and permissive-software terms; not MIT, Apache-2.0 or CC BY) | Facts only, rewritten in our words, no text copied: feed and article roles, busy flag, position and set size (-1 unknown), suggested keys, nested feed for comments. Read 2026-10-20 through a summarising fetcher, not the raw page |
| HTML Standard, the `time` element (https://html.spec.whatwg.org/multipage/text-level-semantics.html#the-time-element) | CC BY 4.0 for the text, read in the repository LICENSE file on 2026-10-20 (code snippets BSD-3-Clause) | `datetime` attribute rules. Read through a summarising fetcher, first 100000 characters of the page only |

Credit: WHATWG, HTML Standard, https://html.spec.whatwg.org/ (CC BY 4.0).

No permissive source on comment threads, moderation, audit logs or activity feeds as data models was found, searched: W3C ARIA authoring practices, HTML Standard, the licence files of the common headless UI libraries (none documents comment systems). Platform help pages of commercial products were not opened.

Related blocks `rich-text-editor-pitfalls`, `in-app-notifications-pitfalls`, `data-table-ui-pitfalls`, `field-and-row-permission-ui-api-pitfalls` and `dsar-handling-pitfalls` were read inside this repository to avoid duplicating them.

## Own craft, not from a source
Everything except the points credited in the table: polymorphic target trade-offs, thread depth and tombstones, edit and delete semantics, mention notification rules, the four rights, visibility classes, moderation, feed against audit log, event codes, cursor paging with anchors, live-update reconciliation, accessibility list, retention, tests and framework pointers.

## Removed
Editor internals (`rich-text-editor-pitfalls`), notification centre design (`in-app-notifications-pitfalls`), tamper-evident ledger design and legal retention periods (business and legal choices), moderation policy writing.

## Not verified
1. **Still unverified: everything not credited above**, which is the data model, threading, edits, deletes, mentions, permissions, visibility classes, moderation, audit separation, cursor paging, live updates and tests.
2. **Accessibility**: feed roles, busy flag, position and size, and the time element are verified (read 2026-10-20). Live regions, focus after send or delete and hover-only menus remain recalled practice. Re-read before relying.
2b. **Verified in this pass**: §2.2.8, §2.5.1, §2.5.8, §2.5.9 to §2.5.11 (added). Corrected: none. Deleted: none.
3. **Framework pointers** name features from memory; no version was checked.
4. **No number** (edit window, page size, retention period) is stated; none was measured.
5. **Audit and erasure** interplay is a design note, not legal advice.
