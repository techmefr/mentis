# offline-first-sync-and-conflict-pitfalls §1 — Choosing the write path

Sources: the Writes guide, the Shapes guide and the Security guide of the Electric documentation at commit 3f9809f, read 2026-10-20. "Own guidance" marks craft knowledge.

## 1.1 Four patterns, in order of effort
1. **Online writes: the interface waits for the server.** The Electric guide lists dashboards, analytics, cloud-side processing and anything that needs the network anyway, such as taking a payment, as good fits. Symptom of choosing it wrongly: spinners on every save on a patchy connection. Check: ask for each write "does it have to succeed before the user moves on".
2. **Optimistic state: show the change at once, send it, drop the local copy when the real one arrives.** It takes the network off the write path and works for offline writes, but the simple form is scoped to one component and lost on reload. Symptom: another screen shows the old value, or the change vanishes after a refresh. Fix: move to pattern 3 when more than one place reads the data or writes must survive a restart.
3. **Shared, persistent optimistic state.** The unsent changes live in a store shared by all components and saved on the device, and screens combine synced data with them when reading. The guide calls it a pragmatic middle: good experience without a heavy dependency, and rollback is clear because the synced data is never mutated.
4. **Through the local database.** Application code reads and writes a local database and the changes sync in the background. The guide's version keeps an immutable synced table, a separate local-changes table and a view that combines them, with write triggers on the view. The price named there is a larger local schema, a heavier dependency and loss of the original context when a write is rolled back.
5. **Choose per entity, not per application** (own guidance). A shopping list can sit on pattern 3 while checkout stays on pattern 1.

## 1.2 Keeping two kinds of state apart
1. **The synced copy is a read-only mirror; unsent changes are a separate overlay.** The Electric guide points out the benefit: in the worst case you can wipe the local overlay or resync the server state without untangling a mixed store. Symptom of mixing them: a rejected write leaves a corrupted copy nobody can tell from the real one. Check: after a rejected write, is the screen back to the server's value without a manual refresh.
2. **Rollback needs the write's context.** The guide's third pattern rolls back individual writes because it still has them; the fourth loses that context. Decide what you show: "your change was not accepted: <reason>", keep the draft for retry, or discard (own guidance).
3. **A rejected write can invalidate later writes that depended on it.** The guide notes the shared store could also remove related local writes. Symptom: item B was added to a list item A that the server refused. Fix: record dependencies between queued writes, or batch dependent writes into one (own guidance).
4. **Rebase local changes when other people's updates arrive.** The shared-persistent example in the guide matches each local write against incoming synced data and rebases the overlay on concurrent changes. Without it the overlay shows values the server has already superseded.

## 1.3 The server stays the arbiter
1. **The server validates every queued write as if it were new.** The device is untrusted and the time between the user's action and arrival may be days (own guidance). Symptom: a limit, a permission or a price check enforced only in the interface, so a late write passes.
2. **Electric itself covers the read path only** (the guide states it does not do write-path sync and that you send writes through your own API). Symptom of assuming otherwise: edits that never reach the database. Check: where is the write endpoint, and what authenticates it.
3. **The write API returns a result per queued mutation** (accepted, rejected with reason, already applied) so the client can settle each one (own guidance).

## 1.4 Checks (own guidance)
1. For one entity, take the device offline, edit, reload the app, reconnect, and confirm the edit arrives once.
2. Make the server refuse one write and confirm the screen returns to the server value and says why.
