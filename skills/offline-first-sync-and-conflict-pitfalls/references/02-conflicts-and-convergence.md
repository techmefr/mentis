# offline-first-sync-and-conflict-pitfalls §2 — Conflicts and convergence

Sources: the Writes guide of the Electric documentation at commit 3f9809f (rebasing the overlay, rejection context), read 2026-10-20. The rest of this section is own guidance from craft knowledge: no convergent-data-type documentation was read (the Yjs repository reports no detected licence and was not opened; the Automerge licence file was read but its documentation was not used).

## 2.1 Decide who wins, per thing
1. **Last write wins is a rule, so choose it on purpose** (own guidance). Symptom: a card is silently moved back, or a long description edited on two devices keeps only one version. Check: for each entity, list the fields two people can plausibly edit at once. Fix: row-level last write for rarely edited records, field-level for forms, a merge for text, an explicit conflict screen where losing data costs money.
2. **Field-level merge beats row-level.** Two people editing different fields of one record should both win; sending the whole row from the device overwrites the other person's field (own guidance). Fix: send only changed fields, with the value the user saw as the base.
3. **A base version turns a silent loss into a detectable conflict.** Send the version the edit started from; the server compares it with the current one, applies if equal, or runs the rule (own guidance). Symptom without it: the device's old copy overwrites newer data after it reconnects.
4. **Show the loser what happened.** "Your edit to the title was replaced by a newer one" with a way to reapply it (own guidance). A silent drop reads as a bug.

## 2.2 Types that merge by construction
1. **Counters, sets and sequences can be built so concurrent changes combine without a conflict** (own guidance): a counter stored as increments instead of a total, a set as additions and removals instead of the whole list. Symptom of storing the total: two offline "+1" become one. Fix: store the operation, derive the total.
2. **Convergence is not validity.** Peers can all reach the same state and that state can still break a rule (two bookings for the same slot, a negative stock). Run the business invariant on the server after merging and have a resolution for violations (own guidance; the same point for shared text is in `skills/rich-text-editor-pitfalls`).
3. **A merge model keeps history,** so deleted or sensitive content may stay recoverable and files grow (own guidance). Decide on compaction and on how a person's removed data is actually erased when law requires it.

## 2.3 Deletes, identifiers, ordering
1. **A delete needs a record that it happened.** Symptom: a device that was offline pushes the old row back and the deleted item reappears. Fix: a tombstone or deleted-at marker kept long enough to outlast the longest supported offline period (own guidance, links to §3.3).
2. **Create identifiers on the client that cannot collide,** and use the same identifier as the idempotency key for the queued create (own guidance). Symptom of server-generated ids only: a queued create retried after a timeout creates two rows. Fix: a client-generated unique identifier accepted by the server.
3. **Order of queued writes matters when they touch the same thing.** Send them in the order made, one thread per entity, and stop an entity's queue when its head fails (own guidance). Symptom: an update sent before the create it depends on.
4. **Do not trust device clocks for ordering** (own guidance). A phone with a wrong date can win every "latest" comparison for the next year. Fix: the server stamps order, or a logical counter per device is combined with a server-assigned sequence.
5. **Positions in a list are a conflict magnet.** Moving items by index breaks when another move arrives first; the techniques are in `skills/kanban-board-ui-pitfalls`.

## 2.4 Checks (own guidance)
1. Two devices, one record, both offline, edit the same field and then different fields, reconnect in both orders; compare results with the stated rule.
2. Delete on one device, edit on another, reconnect; the result must be the one the rule says.
3. Replay the same queued create twice; one row.
