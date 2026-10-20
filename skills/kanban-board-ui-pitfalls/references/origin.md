# kanban-board-ui-pitfalls: origin and source stamps

> Provenance of `skills/kanban-board-ui-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** No board was built, run or tested while writing it. Read date: 2026-10-20.

## Sources (rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| clauderic/dnd-kit at commit 01bc678 (legacy accessibility guide, keyboard sensor page) | MIT, Copyright (c) 2021 Clauderic Demers (`LICENSE` read 2026-10-20) | Keyboard activation with Enter and Space, arrow movement, Escape to cancel, identity/operation/state framing, role description, instructions on focus, live region announcements, default step size being arbitrary |

## Own craft, not from a source
Ordering key schemes and rebalancing, move-as-operation payload, concurrent move and WIP races, optimistic rollback, touch and auto-scroll behaviour, state list, virtualization with drag, live-update reconciliation, test list.

## Removed
Library API code and option names beyond the facts cited; the project or pipeline data model behind the columns (a sibling lot); notifications, activity feed and rich text on cards (sibling lot).

## Not verified
1. **Library facts** are the documentation's claims at the commit; none was run. The line has a newer API (a keyboard sensor page lists Tab as an end key by default); re-read before relying.
2. **Accessibility guidance** beyond the library page (target size, reduced motion, live region politeness) is recalled public practice, not re-read in this pass.
3. **Framework pointers** name features from memory; no version was checked.
4. **No performance number** is stated; none was measured.
