# in-app-notifications-pitfalls: origin and source stamps

> Provenance of `skills/in-app-notifications-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** No notification centre was built, run or tested while writing it. Read date: 2026-10-20.

Dogfood 2026-10-20: one static read on a real project, nothing run; fixes: role inbox read semantics against the per-user rule, capped list against full count, failed load shown as empty, grouping race and idempotent increment, seen state only with a popover, skip-when line.

## Sources (rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| facebook/lexical at commit ee98bf4 (`docs/concepts/keyboard-accessibility.md`) | MIT, Copyright (c) Meta Platforms, Inc. and affiliates (`LICENSE` read 2026-10-20) | One fact: a hidden status region, polite by default, created once and reused for announcements |
| WCAG 2.2 understanding pages, SC 4.1.3 Status Messages and SC 2.2.1 Timing Adjustable (W3C, read 2026-10-20) | W3C document, facts only, own words, pages credited | status roles and the focus rule, the common failure of assertive on unimportant content, the time-limit options applied to toasts |
| novuhq/novu | Mixed: MIT for most of the tree, a separate enterprise licence for some packages (`LICENSE-MIT`, `LICENSE-ENTERPRISE` seen 2026-10-20) | Nothing: the mixed licence made it not worth the risk, so it was not read beyond the licence files |
| RFC 9110 sections 9.2.1 (safe methods) and 13.1.2, <https://www.rfc-editor.org/rfc/rfc9110>, re-read 2026-10-20 | IETF Trust document; facts only | GET is safe, prefetching rationale (§1.2.5); conditional GET |
| RFC 8058, Signaling One-Click Functionality for List Email Headers, section 3.1, <https://www.rfc-editor.org/rfc/rfc8058>, read 2026-10-20 | IETF Trust document; facts only | One-click header pair, DKIM, POST without cookies or authorization, opaque identifier (§1.6.6) |
| W3C WAI-ARIA 1.2, WCAG 2.2 (SC 2.2.1, 4.1.2, 4.1.3), ARIA Authoring Practices (disclosure, modal dialog), full pages fetched 2026-10-20 | W3C Document License; facts only | Status, log, alert live region defaults; aria-relevant defaults; timing options; name requirement; disclosure keys (§2.3.1, §2.3.3, §2.3.7) |
| HTML Standard, server-sent events (Last-Event-ID) and navigator.onLine, full page fetched 2026-10-20 | CC BY 4.0 (WHATWG); facts only | Reconnect with last event id; onLine true means might be online, inherently unreliable (§2.1.2, §2.1.4, §2.1.6) |
| RFC 9110 section 13.1.2 If-None-Match (read 2026-10-20) | IETF standard, facts only, own words | Conditional GET with a tag list and 304 |
| HTML Standard, page visibility (read 2026-10-20) | CC BY 4.0 (WHATWG), facts only | Document has a visibility state, visible or hidden, read through visibilityState and hidden, with a change event |

## Own craft, not from a source
Per-recipient model, seen against read, count derivation, grouping, digests, preference matrix and mandatory classes, retention, push against polling and gap recovery, inbox states, accessibility of the badge and the live region, open-time authorisation, test list and framework pointers.

## Removed
Mail template authoring (`customer-email-review-pitfalls`), phone push registration (`flutter-notifications-background`), vendor products for notification infrastructure.

## Not verified
1. **Everything but three facts is own knowledge** (live-region creation, status roles, toast time limit); no other claim was checked.
   No permissive source found for notification data models, grouping, preferences or retention, searched: the licence-checked repositories above, W3C pages.
2. **The live-region fact** is one library's documentation at the commit; it was not run.
3. **Accessibility points** other than the live-region, status-role and time-limit ones are recalled public practice, not re-read. The claim that a region inserted with its message is often not announced was not confirmed by any page read.
4. **Framework pointers** name features from memory; no version was checked.
5. **Verified 2026-10-20 (second pass, same day):** safe-method rationale, one-click unsubscribe requirements, live region role defaults, SC 2.2.1 numbers, SC 4.1.2, SSE Last-Event-ID, onLine reliability; 1 narrowed (disclosure pattern does not define Escape: §2.3.7 now says so), 0 deleted, 1 added (§2.1.2 onLine caveat) and 1 added (RFC 8058 in §1.6.6). **Earlier:** conditional polling with If-None-Match and 304; existence of the visibility state a poller can read. **Still unverified:** that a hidden tab slows its timers (browser behaviour, not stated in the page read) and the claim about a region inserted with its message (WCAG 4.1.3 page read says nothing on it).
6. **No number** (poll interval, retention period, group window) is stated; none was measured.

Independent verification 2026-10-21: 17 checked, 16 matched, 1 corrected, 0 unverified
