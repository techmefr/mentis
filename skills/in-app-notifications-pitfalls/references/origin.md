# in-app-notifications-pitfalls: origin and source stamps

> Provenance of `skills/in-app-notifications-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** No notification centre was built, run or tested while writing it. Read date: 2026-10-20.

Dogfood 2026-10-20: one static read on a real project, nothing run; fixes: role inbox read semantics against the per-user rule, capped list against full count, failed load shown as empty, grouping race and idempotent increment, seen state only with a popover, skip-when line.

## Sources (rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| facebook/lexical at commit ee98bf4 (`docs/concepts/keyboard-accessibility.md`) | MIT, Copyright (c) Meta Platforms, Inc. and affiliates (`LICENSE` read 2026-10-20) | One fact: a hidden status region, polite by default, created once and reused for announcements |
| novuhq/novu | Mixed: MIT for most of the tree, a separate enterprise licence for some packages (`LICENSE-MIT`, `LICENSE-ENTERPRISE` seen 2026-10-20) | Nothing: the mixed licence made it not worth the risk, so it was not read beyond the licence files |

## Own craft, not from a source
Per-recipient model, seen against read, count derivation, grouping, digests, preference matrix and mandatory classes, retention, push against polling and gap recovery, inbox states, accessibility of the badge and the live region, open-time authorisation, test list and framework pointers.

## Removed
Mail template authoring (`customer-email-review-pitfalls`), phone push registration (`flutter-notifications-background`), vendor products for notification infrastructure.

## Not verified
1. **Everything but one fact is own knowledge**: no external claim was checked against a source.
2. **The live-region fact** is one library's documentation at the commit; it was not run.
3. **Accessibility points** other than that one are recalled public practice, not re-read. Re-read before relying.
4. **Framework pointers** name features from memory; no version was checked.
5. **No number** (poll interval, retention period, group window) is stated; none was measured.
