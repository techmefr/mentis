# comments-and-activity-feed-pitfalls: origin and source stamps

> Provenance of `skills/comments-and-activity-feed-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** No comment thread or feed was built, run or tested while writing it. Read date: 2026-10-20.

## Sources

| Source | Licence | What it gave |
|---|---|---|
| W3C WAI-ARIA Authoring Practices, feed pattern (https://www.w3.org/WAI/ARIA/apg/patterns/feed/) | W3C document licence (liability, trademark and permissive-software terms; not MIT, Apache-2.0 or CC BY) | Facts only, rewritten in our words, no text copied: feed and article roles, busy flag, position and set size (-1 unknown), suggested keys, nested feed for comments. First read 2026-10-20 through a summarising fetcher; re-read on the raw page the same day: feed and article roles, label and description, position and set size (total loaded or total in the feed, -1 when undetermined), busy flag and the warning about resetting it, Page Down, Page Up, Control+End, Control+Home as recommended, nested feed for comments, the load-by-focus contract |
| HTML Standard, the `time` element (https://html.spec.whatwg.org/multipage/text-level-semantics.html#the-time-element) | CC BY 4.0 for the text, read in the repository LICENSE file on 2026-10-20 (code snippets BSD-3-Clause) | `datetime` attribute rules. Read through a summarising fetcher, first 100000 characters of the page only |

Credit: WHATWG, HTML Standard, https://html.spec.whatwg.org/ (CC BY 4.0). The `time` element was re-read in the full single-page standard on 2026-10-20 (datetime attribute, no element children without it, valid syntaxes, local date and time without offset versus global date and time).

Second pass, read 2026-10-20 (added rows):

| Source | Licence | What it gave |
|---|---|---|
| W3C Activity Streams 2.0 Core and Vocabulary, <https://www.w3.org/TR/activitystreams-core/>, <https://www.w3.org/TR/activitystreams-vocabulary/> | W3C Document License; facts only, own words | Actor, type, object, target as the shape of an event; Tombstone with formerType and deleted (§1.2.4, §2.1.6) |
| RFC 4287, The Atom Syndication Format, sections 4.1.1 and 4.2.6, 8.4, <https://www.rfc-editor.org/rfc/rfc4287> | IETF Trust document; facts only | Permanent entry id, same id means same entry, latest update shown, id spoofing warning (§2.3.4) |
| W3C WCAG 2.2, SC 2.1.1 and 1.4.13, full page fetched 2026-10-20 | W3C Document License; facts only | Keyboard operability; hover and focus content rules (§2.5.6) |

No permissive source on comment threads, moderation, audit logs or activity feeds as data models was found, searched: W3C ARIA authoring practices, HTML Standard, the licence files of the common headless UI libraries (none documents comment systems). Platform help pages of commercial products were not opened.

Related blocks `rich-text-editor-pitfalls`, `in-app-notifications-pitfalls`, `data-table-ui-pitfalls`, `field-and-row-permission-ui-api-pitfalls` and `dsar-handling-pitfalls` were read inside this repository to avoid duplicating them.

## Own craft, not from a source
Everything except the points credited in the table: polymorphic target trade-offs, thread depth and tombstones, edit and delete semantics, mention notification rules, the four rights, visibility classes, moderation, feed against audit log, event codes, cursor paging with anchors, live-update reconciliation, accessibility list, retention, tests and framework pointers.

## Removed
Editor internals (`rich-text-editor-pitfalls`), notification centre design (`in-app-notifications-pitfalls`), tamper-evident ledger design and legal retention periods (business and legal choices), moderation policy writing.

## Not verified
1. **Still unverified: everything not credited above**, which is the data model, threading, edits, deletes, mentions, permissions, visibility classes, moderation, audit separation, cursor paging, live updates and tests.
2. **Accessibility**: feed roles, busy flag, position and size, and the time element are verified (read 2026-10-20). Live regions, focus after send or delete and hover-only menus remain recalled practice. Re-read before relying.
2b. **Verified in the first pass**: §2.2.8, §2.5.1, §2.5.8, §2.5.9 to §2.5.11 (added). Corrected: none. Deleted: none. **Second pass 2026-10-20**: the feed and time claims re-checked on the raw pages (all confirmed); tombstone vocabulary, event shape, entry identity and spoofing, load-by-focus contract, hover-only menus verified or added (5 points); 0 corrected, 0 deleted. Everything on threading depth, edit windows, visibility classes, moderation and audit design stays own craft.
3. **Framework pointers** name features from memory; no version was checked.
4. **No number** (edit window, page size, retention period) is stated; none was measured.
5. **Audit and erasure** interplay is a design note, not legal advice.
