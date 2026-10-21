# kanban-board-ui-pitfalls §1 — Order, moves and concurrency

Sources: own craft, with the fractional-key facts from the fractional-indexing library README (CC0 1.0, read 2026-10-20) and the conditional-request facts from RFC 9110 (sections 9.2.2, 13.1.1, 15.5.13, read 2026-10-20).

## 1.1 How order is stored
1. **Symptom: moving one card rewrites dozens of rows, and two simultaneous moves interleave into a broken order.** Cause: a dense position integer (1, 2, 3...) renumbered on every drop.
2. **Prefer a sparse key that lets an insert touch one row.** Options: integers with gaps (10, 20, 30) and a periodic rebalance; fractional numbers between the neighbours; or a lexicographic string key generated between the neighbours' keys. All three trade one write for an occasional rebalance.
3. **Floating-point midpoints run out.** Repeated insertion between the same two cards eventually gives equal keys; detect "no room" and rebalance the column instead of writing a tie.
4. **String keys must be compared with byte order**, not a locale collation (`collation-and-locale-aware-search-pitfalls`); a locale-aware sort puts keys in a different order than the generator assumed. The fractional-indexing library says its keys are case-sensitive, that a locale-aware comparison such as localeCompare gives a wrong order, and that plain string comparison is the right predicate; it also requires digit alphabets that are single-byte and sorted by character code, which is why plain comparison works.
5. **Add the card id as the final sort tiebreaker** on the server and in the client, so two cards with an equal key always render in the same order everywhere (`data-table-ui-pitfalls` §1.3).
6. **Order belongs to a column.** Moving across columns changes the column and the key together in one write; a card has no global position.
7. **Archived or hidden cards keep their keys**; filtering the board (`filters-search-and-saved-views-pitfalls`) must not renumber what is hidden, or unfiltering shows a scrambled column.

## 1.2 What a move sends
1. **Symptom: a drop sends the full array of card ids for the column, and a concurrent insert by someone else vanishes.** Cause: the payload replaces the column instead of describing the move.
2. **Send the move as an operation:** the card id, the target column, and the card it now follows and precedes (or null at an end). The server computes the key from the neighbours it sees now, not from the ones the client saw.
3. **Accept an optional expected version of the card** so the server can reject a move on a stale card (§1.4).
4. **Return the new key, column and version of the moved card**, and the keys of anything the server had to rebalance, so the client can reconcile without refetching the column.
5. **A move is idempotent per request id**: PUT and DELETE are idempotent by definition in HTTP (RFC 9110), a move sent as POST is not and needs the id; a retry after a timeout must not move the card twice (`laravel-idempotent-jobs` for the server-side pattern).

## 1.3 Moves inside and across columns
1. **Define what a drop on an empty column and on the column header mean:** append at the end or insert at the start, one rule, shown by the drop indicator.
2. **A column change is often a status change with side effects** (a timestamp, an assignee, a notification, a required field). Those run on the server in the same transaction as the move, not in the drag handler.
3. **A move that needs more information opens a form, and the card stays in its old column until it is saved.** Symptom: a card sits in "Done" with no completion date because the dialog was cancelled.
4. **Forbidden transitions are enforced by the server and previewed by the client.** Grey the columns a card cannot enter during the drag, and still answer a forced request with a clear refusal.
5. **Moving several selected cards is one operation with one result per card** (`data-table-ui-pitfalls` §1.5 for the report shape).

## 1.4 Two people move the same card
1. **Symptom: the card ends in a column neither person chose, or a move is silently undone.** Cause: last write wins on column and key with no check.
2. **Decide the rule per field.** Moving a card two people agree needs no ceremony; moving it to two different columns needs a visible loser.
3. **Use a version or updated-at check on the card** (over HTTP, an entity tag sent in If-Match makes the server refuse the write with 412 when the card changed, which RFC 9110 describes as preventing the lost update). On mismatch, return the current card, refuse the move, and let the client put the card back and explain ("moved by Sam while you were dragging").
4. **Ordering conflicts are usually benign:** two inserts between the same neighbours can both succeed with distinct keys. Make the tiebreak deterministic rather than raising an error. Two clients that generate a key between the same neighbours produce the same key; the library README points to added random jitter as the way to lower the chance of that collision, and the server computing the key (§1.2.2) removes it for the common case.
5. **A card edited while it is being dragged keeps the edit.** Merge by field; do not replace the card object with the dragged copy.
6. **A card deleted by someone else mid-drag** returns "not found"; remove it and say so rather than showing a generic failure.

## 1.5 Optimistic update and rollback
1. **Moving the card at once is expected; the server stays the judge.** Apply the move locally, send it, and reconcile with the response.
2. **Keep the previous position until the server confirms**, so a rollback restores column and place, not just the column.
3. **Symptom: a card flickers back and forward.** Cause: a live update for the same card arrives between the drop and its confirmation. Ignore or queue incoming changes for a card that has a move in flight, then apply the newest.
4. **Serialize moves of one card** (a second drag waits or replaces the first) so responses cannot arrive out of order and leave a stale position.
5. **A failed move states why and offers retry**, in a status message that does not depend on colour (§2.4).

## 1.6 WIP limits and column rules
1. **A work-in-progress limit is a rule about the count of cards in a column, so the server counts and refuses.** A client-only limit is a suggestion that two tabs break.
2. **Race: two users each drop the last allowed card.** Enforce with a transaction that checks the count under a lock or with a conditional write; the loser gets the same refusal as a forbidden transition.
3. **Decide soft or hard.** A soft limit warns and allows (the column header turns to a warning with text), a hard limit refuses. Say which in the interface and in the setting.
4. **Count what the rule means:** all cards, or only unarchived ones, or per assignee. A filtered board still shows the true count, not the number of visible cards.
5. **Show "3 of 5" in the column header** as text, and announce the refusal when a drop is rejected (§2.4).
6. **Limit changes do not evict existing cards**; a column over its new limit stays over until cards leave, and the header says it is over.

## Checks
- Two browsers drop cards into the same gap: both persist, the order is identical in both after reload.
- A drop sends one operation, not a column array; killing the request and retrying moves the card once.
- Two tabs drop the last WIP slot: one succeeds, one is refused with a message and rolled back.
- A forced request for a forbidden transition is refused by the server.
