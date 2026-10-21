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

## Own craft, not from a source
Ordering key schemes and rebalancing, move-as-operation payload, concurrent move and WIP races, optimistic rollback, touch and auto-scroll behaviour, state list, virtualization with drag, live-update reconciliation, test list.

## Removed
Library API code and option names beyond the facts cited; the project or pipeline data model behind the columns (a sibling lot); notifications, activity feed and rich text on cards (sibling lot).

## Verified on the second pass, 2026-10-20
5 verified (pointer-without-dragging criterion, minimum target size, colour as sole means, reduced-motion media feature, interaction-animation criterion), 1 corrected (keyboard drag alone does not satisfy the dragging criterion; the menu route does), 0 deleted. Ordering-key, concurrency and WIP points are design practice, not checkable facts, and stay own craft.

## Not verified
1. **Library facts** are the documentation's claims at the commit; none was run. The line has a newer API (a keyboard sensor page lists Tab as an end key by default); re-read before relying.
2. **Live region politeness** and the exact announcement wording are recalled public practice, not re-read; target size, reduced motion and colour were re-read on the second pass.
3. **Framework pointers** name features from memory; no version was checked.
4. **No performance number** is stated; none was measured.
