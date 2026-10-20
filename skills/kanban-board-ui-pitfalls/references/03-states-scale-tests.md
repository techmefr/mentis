# kanban-board-ui-pitfalls §3 — States, scale and tests

Sources: own craft; no source text taken.

## 3.1 States
1. **A board has more states than "loaded".** Render each distinctly: first load (column skeletons), empty board (call to action to add a card), empty column (a drop hint, not a blank gap), refreshing (cards stay, a quiet indicator), failed load (error with retry), partial failure (one column failed, others shown), failed move, conflict (§1.4), over-limit column (§1.6), and read-only (no permission, no handles).
2. **Symptom: "No cards" displayed while the request failed.** Same rule as tables (`data-table-ui-pitfalls` §2.1).
3. **A permission change shows as a read-only board, not as a broken drag.** Hide the handle, keep the card readable, and refuse on the server as well (`field-and-row-permission-ui-api-pitfalls`).
4. **Column totals and counts say what they cover** when the board is filtered ("4 shown of 12").
5. **A card in a column that was just deleted or renamed** is moved to a defined place by the server, and the client says where.

## 3.2 Long columns and virtualization
1. **Symptom: the board freezes with a few hundred cards per column.** Cause: every card is mounted, each with its own drag listeners and observers.
2. **Page or window each column independently.** Load the first screen of a column, add more on scroll, and show the true count from the server.
3. **Virtualization and drag interact badly.** A dragged card must stay mounted when it leaves the viewport, and drop targets that are not rendered cannot be hit. Keep the active card out of the windowing, and let auto-scroll (§2.3) bring targets into view.
4. **Dropping into a column whose neighbours are not loaded** still needs neighbours for the key (§1.2): send the nearest rendered neighbour, or "top" and "bottom", and let the server place it.
5. **Keep cards light:** a title and a few fields; load details on open. Avatar and attachment images load lazily.
6. **Do not animate the whole board on every change;** animate only the moved card, and not at all under reduced motion (§2.4).

## 3.3 Live updates from other users
1. **Symptom: the board is stale until a page reload, then a card jumps.** Subscribe to changes for the board and apply them as card-level patches (`card moved`, `card edited`), not whole-board refetches.
2. **Ignore your own echo.** Tag each change with the request id so the client does not apply the server's copy of a move over the optimistic state (§1.5).
3. **Do not move cards under a pointer that is dragging;** queue changes until the drop, then reconcile.
4. **A reconnect refetches what it missed** (changes since a version, or the column) rather than assuming nothing happened.
5. **Say who moved a card** in an announcement or the activity trail when it changes under the user's eyes. The activity feed itself is out of scope here.

## 3.4 Tests
1. **Order tests on the server:** insertion at the start, middle, end and between equal keys; a rebalance; the same result for two interleaved moves.
2. **A concurrency test:** two moves of one card and two drops into one WIP slot in parallel; exactly the expected winners.
3. **Idempotence:** the same move request twice moves once.
4. **Permission tests:** a user without the right is refused on move and on a forbidden transition even with a forged request.
5. **Component tests for the keyboard path:** pick up, move, drop, cancel; the live region text; focus after a drop and after a refusal.
6. **A touch and pointer test** on activation distance: a click opens the card, a drag moves it.
7. **A scale test with a seeded large column:** scrolling and dragging stay responsive; measure in the project's own environment rather than trusting a number here.
8. **A rollback test:** a failing server returns the card to its place and shows the message.

## 3.5 Framework pointers
1. **dnd-kit** (React, Vue, Svelte and Solid bindings in its current line) provides sensors, a keyboard sensor, announcements and sortable helpers; its accessibility guide is the reference for instructions and live regions. Re-read for the version in use.
2. **Vuetify, Quasar and similar kits** have no board component; a draggable-list package or the browser's native drag events cover pointer use, and native drag events give no keyboard support, so §2.1 stays your work.
3. **Laravel and Livewire** back-ends store keys and counts; the lock for §1.6 is a database transaction, not a cache flag (`laravel-idempotent-jobs`).
4. **Server-rendered boards** still need the move menu (§2.1): it works with a plain form post and no script.

## Checks
- Every state in §3.1 has a test or a visible fixture.
- A 1,000-card column scrolls and accepts a drop at the end.
- Two browsers see each other's moves without reload and without a flicker for the mover.
