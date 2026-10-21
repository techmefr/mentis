# kanban-board-ui-pitfalls: origin and source stamps

> Provenance of `skills/kanban-board-ui-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** No board was built, run or tested while writing it. Read date: 2026-10-20.

## Sources (rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| clauderic/dnd-kit at commit 01bc678 (legacy accessibility guide, keyboard sensor page) | MIT, Copyright (c) 2021 Clauderic Demers (`LICENSE` read 2026-10-20) | Keyboard activation with Enter and Space, arrow movement, Escape to cancel, identity/operation/state framing, role description, instructions on focus, live region announcements, default step size being arbitrary |
| W3C WCAG 2.2 Understanding SC 2.5.7 Dragging Movements, SC 2.5.8 Target Size (Minimum), SC 2.3.3 Animation from Interactions, SC 1.4.1 Use of Color, read 2026-10-20 | W3C document licence, facts only | Single-pointer alternative to dragging, 24 by 24 CSS pixel minimum target and its exceptions, interaction animation can be disabled, colour not the only means (§2.1.1, §2.1.3, §2.3.4, §2.4.1, §2.4.2) |
| W3C Media Queries Level 5, `prefers-reduced-motion` section, read 2026-10-20 | W3C document licence, facts only | `no-preference` and `reduce` values (§2.4.2) |

Second pass, read 2026-10-20 (added rows):

| Source | Licence | What it gave |
|---|---|---|
| rocicorp/fractional-indexing, README and `LICENSE` | CC0 1.0 Universal (`LICENSE` read 2026-10-20, repository licence field cc0-1.0) | Case-sensitive keys, localeCompare gives a wrong order, plain comparison, single-byte sorted alphabets, random jitter against concurrent collisions (§1.1.4, §1.4.4) |
| clauderic/dnd-kit at commit 01bc678, `packages/dom/src/core/plugins/accessibility/LiveRegion.ts`, legacy pointer and touch sensor pages | MIT (licence read earlier the same day) | Live region created with role status, aria-live polite, aria-atomic true; distance and delay activation constraints, tolerance for touch, touch-action recommendation (§2.2.4, §2.3.2) |
| W3C WAI-ARIA 1.2, <https://www.w3.org/TR/wai-aria-1.2/>, full page fetched 2026-10-20 | W3C Document License; facts only | status implicitly polite and atomic; aria-grabbed deprecated, aria-dropeffect treated as deprecated (§2.2.7, added) |
| W3C Pointer Events Level 3, <https://www.w3.org/TR/pointerevents3/>, full page fetched 2026-10-20 | W3C Document License; facts only | touch-action change after pointerdown ignored for that gesture; pointercancel cases; implicit capture release (§2.3.5, §2.3.7 added) |
| RFC 9110 sections 9.2.2, 13.1.1, 15.5.13, <https://www.rfc-editor.org/rfc/rfc9110>, read 2026-10-20 | IETF Trust document; facts only | PUT and DELETE idempotent; If-Match prevents lost updates; 412 (§1.2.5, §1.4.3) |
| HTML Standard, server-sent events, Last-Event-ID header, full page fetched 2026-10-20 | CC BY 4.0 (WHATWG); facts only | Reconnect reports the last event id (§3.3.4) |

## Own craft, not from a source
Ordering key schemes and rebalancing, move-as-operation payload, concurrent move and WIP races, optimistic rollback, touch and auto-scroll behaviour, state list, virtualization with drag, live-update reconciliation, test list.

## Removed
Library API code and option names beyond the facts cited; the project or pipeline data model behind the columns (a sibling lot); notifications, activity feed and rich text on cards (sibling lot).

## Verified on the second pass, 2026-10-20
5 verified (pointer-without-dragging criterion, minimum target size, colour as sole means, reduced-motion media feature, interaction-animation criterion), 1 corrected (keyboard drag alone does not satisfy the dragging criterion; the menu route does), 0 deleted. Ordering-key, concurrency and WIP points are design practice, not checkable facts, and stay own craft.

## Not verified
1. **Library facts** are the documentation's claims at the commit; none was run. The line has a newer API (a keyboard sensor page lists Tab as an end key by default); re-read before relying.
2. **Live region politeness** is now verified (library source and WAI-ARIA 1.2, third pass 2026-10-20); the exact announcement wording is still recalled public practice. Third pass: 11 points verified or added (fractional-key comparison, jitter, If-Match and 412, idempotent methods, live region, ARIA deprecations, activation constraints, touch-action timing, pointer cancel cases, Last-Event-ID), 0 corrected, 0 deleted. Order-key schemes other than fractional keys, WIP races, virtualization and the test lists remain own craft.
3. **Framework pointers** name features from memory; no version was checked.
4. **No performance number** is stated; none was measured.
