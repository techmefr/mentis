---
name: kanban-board-ui-pitfalls
description: "Use when a kanban board, card board or drag-to-reorder list across columns is written or reviewed in a business application, whatever the framework: how card order is stored (position integers against ordering keys), what a move sends to the server, two users moving the same card, work-in-progress limits and who enforces them, drag and drop with a keyboard and screen reader alternative, touch and auto-scroll, the empty, loading, failed-move and conflict states, long columns (paging and virtualization), plus the tests that catch them."
---

# kanban-board-ui-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the board every tracker, CRM pipeline and task tool ends up with. The premise:
**a board is a list whose order is data, edited by several people at once, through a gesture that excludes anyone without a
mouse**. It looks right with one user and ten cards; it breaks on the second tab, the second hundred cards and the first
keyboard user. The data model of the project or the pipeline behind the columns is not covered here; table, filter and
dashboard neighbours are `data-table-ui-pitfalls`, `filters-search-and-saved-views-pitfalls` and `dashboard-ui-pitfalls`;
semantics and widget markup are in `accessibility`.

## When
- A board, lane view or "move card to column" interface is built or reviewed.
- A user reports "my card went back", "two cards swapped", "it saved but another person sees the old order", "I cannot move it without a mouse".
- A column is expected to hold more cards than one screen or one response.

## Steps

**Read the section the task meets.** Each ends with checks.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Order storage, move payload, concurrent moves, optimistic update and rollback, WIP limits, column rules | a move is saved, or order is stored | [`01-order-moves-concurrency.md`](./references/01-order-moves-concurrency.md) |
| 2 | Drag and drop, keyboard and screen reader alternative, announcements, touch, scrolling, reduced motion | a card can be dragged | [`02-drag-keyboard-access.md`](./references/02-drag-keyboard-access.md) |
| 3 | States, long columns and virtualization, live updates, tests, framework pointers | a board ships, scales or is tested | [`03-states-scale-tests.md`](./references/03-states-scale-tests.md) |

## Output / checkpoint
A change is done when: a card move is one server operation with the source, target and neighbours; order survives
concurrent moves; a WIP limit is enforced by the server; every drag has a keyboard route with announcements; every state
in §3.1 renders distinctly; and the tests in §3.4 exist. No checkpoint is written: a craft block, 🟡, nothing here was
run in an application.

## Guardrails
- Send a move as card, target column and neighbours (§1.2). Never send the whole reordered board.
- Order by a key that lets one insert touch one row (§1.1). Never renumber every card on each drop.
- Enforce WIP limits and permissions on the server (§1.6). Never rely on the client hiding a drop target.
- Give every drag a keyboard route and a spoken result (§2.1). Never ship a board that works with a pointer only.
- Roll back a failed optimistic move and say why (§1.5). Never leave the card where the server did not put it.
- Facts about a library are for the commit stamped in `references/origin.md`; re-read before relying.

## Origin
Own craft knowledge, with the drag and drop accessibility facts re-read in the dnd-kit documentation (MIT, read
2026-10-20). Details in [`references/origin.md`](./references/origin.md).
