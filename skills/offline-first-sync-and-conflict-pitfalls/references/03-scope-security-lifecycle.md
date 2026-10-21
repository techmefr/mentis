# offline-first-sync-and-conflict-pitfalls §3 — Scope, security, transport and lifecycle

Sources: the Shapes, Security and Troubleshooting guides of the Electric documentation at commit 3f9809f, read 2026-10-20. "Own guidance" marks craft knowledge.

## 3.1 What a device holds
1. **Sync a defined subset, not the database.** Electric calls the subset a shape: one table, an optional filter and an optional column list. Symptom of syncing too much: a slow first load and personal data on a device that does not need it. Check: list the shapes per screen with the filter each uses and estimate the row count for the heaviest user.
2. **A shape is single-table and its definition does not change once created** (statements of the guide at the commit). To change the scope, create a new one. Symptom: a screen that needs related rows fetches several shapes; plan the joins on the client (own guidance), and use the guide's sub-query filters for membership-style scopes.
3. **Filters must be repeatable.** The guide rules out non-deterministic functions such as the current time in a filter. A "last 30 days" window is therefore a client-side or periodic re-creation concern (own guidance on the workaround).
4. **Restrict columns,** so internal fields never leave the server (the guide has a column clause; the principle is `skills/field-and-row-permission-ui-api-pitfalls` §2).

## 3.2 A sync endpoint is public until you secure it
1. **The sync service exposes everything its database user can read to any client that can reach it.** The guide says the API is public by default and must be secured in production. Check: connect without credentials from outside; the answer must be a refusal. Fix: put an authorising proxy in front, and give the database user only the tables synced (the guide has a separate page on database permissions).
2. **Authorise at the proxy per request, and build the filter on the server.** The client names what it wants; the proxy decides the filter (for example the person's organisation) and adds it. Symptom of letting the client send the filter: a person changes the identifier in the request and syncs someone else's rows (own guidance).
3. **The service's secret never goes to the client.** The guide says the proxy adds it when forwarding. Symptom: the secret visible in the browser's network log.
4. **Network rules protect server-to-server sync but not a browser or a phone,** because their addresses are not fixed (the guide makes this point). Do not treat an IP allow-list as client authorisation.
5. **Encrypted payloads sync like plain ones.** If end-to-end encryption is needed, the server cannot filter on encrypted columns; decide what stays clear for scoping (the guide lists encryption as supported at the client or in middleware; key management is yours).
6. **Remove local data at logout and on account switch,** and when access is revoked (own guidance). Symptom: the previous user's records readable by the next person on a shared device. Fix: wipe the local database and the queued writes, after warning about unsent changes.

## 3.3 Long offline and local changes
1. **State the longest offline period you support** (own guidance; the shared-text article in `skills/rich-text-editor-pitfalls` §2 makes the same point for collaboration). Beyond it, a device does a full resync and unsent changes are shown to the user for re-applying, not pushed blindly.
2. **Tombstones and server logs must be kept at least that long** (§2.3). A server that compacts its history sooner forces a full resync, so decide the numbers together.
3. **A local schema change needs a migration on every device,** including devices that skip versions (own guidance). Symptom: after an update the app is empty or crashes on old data. Fix: version the local schema, migrate forward, and on failure resync from the server rather than guess.
4. **The first sync can be large,** so show progress, allow resume, and avoid blocking the whole interface (own guidance).
5. **Storage is finite and can be evicted by the platform** (browsers may clear it, phones run low). Treat the local copy as a cache of the server plus a queue, and warn before the queue is the only copy of the user's work (own guidance).

## 3.4 Transport pitfalls
1. **Several open streaming connections can exhaust a browser's per-host limit under the older HTTP version,** and the page, its hot reload and its sync all slow down. The Electric troubleshooting page recommends serving over a protocol that multiplexes connections, including in development through a local reverse proxy. Symptom: pages hang when six or more subscriptions are open.
2. **A proxy that buffers or caches the wrong way breaks live updates.** The same page says streaming responses must not be buffered, and that the sync service's cache headers must be respected, because they let many clients share one upstream request; disabling caching altogether removes that benefit. The client falls back to polling when streaming connections close at once.
3. **Back off on reconnect** and do not retry all clients at the same instant after an outage (own guidance, the client in the source retries with growing delays).

## 3.5 Test list (own guidance)
1. Airplane mode for a day of edits, then reconnect. 2. Kill the app mid-sync. 3. A device away longer than the stated limit. 4. Two users on one device. 5. A rejected write in the middle of a queue. 6. Upgrade the app with unsent changes. 7. Revoke access while the device is offline, then reconnect.
