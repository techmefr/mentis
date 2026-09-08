# vue-nuxt-vuetify-conventions §10 — Realtime events

> Section 10 of `skills/vue-nuxt-vuetify-conventions`. Read it when a socket, a broadcast or a live update. The other sections and the guardrails stay in `SKILL.md`.

1. An incoming realtime/websocket message is **translated into an application-level hook or event**, not
   consumed inline in the component that happens to be mounted. A component subscribing directly couples
   the transport to the view and leaks a listener the moment it unmounts. It also makes the feature
   untestable without a live server: the seam you would fake is inside the component.
2. **One place owns the connection and its lifecycle** — connect, authenticate, reconnect, tear down —
   and components subscribe to the application event, not to the socket. When each component connects for
   itself, a user navigating between three pages ends up with three sockets, and none of them closes on
   the route change that created the next one.
3. **Subscribing is scoped, and the scope is what unsubscribes.** Subscribe inside `onMounted` (or the
   composable's own effect scope) and release in `onScopeDispose`/`onUnmounted`, so the handler dies with
   the thing that wanted it. A subscription registered at module scope survives every unmount and keeps
   firing against a component that no longer exists — the classic symptom is a handler running N times
   after visiting a page N times. Remember `keepalive`d pages deactivate rather than unmount: if the
   subscription should pause there, it belongs in `onDeactivated`, not `onUnmounted`.
4. **A payload arriving from the wire is untrusted input**: validate it at the boundary like any other,
   and narrow it — never assert it into the type you were hoping for. It crosses the network from a
   source you do not control on this request, and a message shaped wrong will otherwise surface as a
   render crash three components deep, at whatever moment the sender happens to change.
5. **Treat the message as a hint that something changed, not as the new state.** Use it to refresh the
   affected resource, or to merge a field you can identify by id — do not paint the payload straight into
   the view as if it were a full snapshot. A broadcast is written for many listeners and is routinely a
   partial or stale projection; the row it describes may already have moved on, and it carries whatever
   the sender chose to include rather than what this screen needs.
6. **Assume duplicates and out-of-order arrival.** The same event can be delivered twice, and two events
   about one resource can land in the wrong order. Key updates by resource id plus a version or
   updated-at from the payload, and drop anything not newer than what is already in hand. Applying blind
   means a redelivered "created" duplicates a row, and a late "old value" overwrites a newer one — a bug
   that only appears under load, which is to say in production.
7. **A stream is not a complete log.** Anything broadcast while the tab was asleep, offline or between
   reconnects is simply gone. On reconnect, resynchronise from the API — refetch the list or the record —
   rather than resuming as though nothing was missed. A UI that only ever applies deltas drifts further
   from the truth the longer it stays open, and shows the user a state the database never had.
8. **Nothing connects during SSR.** There is no socket on the server, and opening one there leaks a
   handle per request and diverges the server-rendered markup from the client's. Gate the connection
   behind `import.meta.client` or an `onMounted`, and render the pre-realtime state on the server — see
   §9, this is the same hydration rule applied to a different primitive.
9. **The channel's authorisation is server-side, always.** A private channel is authorised by the server
   on subscribe; a channel name built from an id the client already holds authorises nothing, because the
   client can build any name. If a user could type another tenant's id and receive that tenant's events,
   the bug is in the channel authorisation callback, not in the component.
10. **Subscribe to what is on screen, not to everything and then filter.** A firehose narrowed with a
    client-side `if` still delivered every payload into the browser, where it is readable in the network
    tab — so a field the current user must not see has already leaked, whatever the template renders. The
    filter belongs on the channel, not after it.
11. **A live update must not move the ground under the user.** Applying an incoming change to the row
    someone is editing, or re-sorting a list while they reach for an item, loses their work or their
    click. Either leave what is focused or dirty alone until they are done, or stage the change behind an
    explicit affordance — a "3 new items" banner they choose to apply.
12. **Don't build a realtime path for something a refresh would cover.** A connection, its reconnection
    policy, its authorisation and its resync are permanent cost. Take it on when staleness has a real
    consequence for the user — two people on the same record, a job whose progress they are waiting on —
    not because live updates feel modern. Polling on the screen that needs it is often the honest answer,
    and it is one file instead of five.
