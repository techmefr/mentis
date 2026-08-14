# vue-nuxt-vuetify-conventions §10 — Realtime events

> Section 10 of `skills/vue-nuxt-vuetify-conventions`. Read it when a socket, a broadcast or a live update. The other sections and the guardrails stay in `SKILL.md`.

1. An incoming realtime/websocket message is **translated into an application-level hook or event**, not
   consumed inline in the component that happens to be mounted. A component subscribing directly couples
   the transport to the view and leaks a listener the moment it unmounts.
2. One place owns the connection and its lifecycle (connect, reconnect, teardown); components subscribe to
   the application event, not to the socket.
3. A payload arriving from the wire is untrusted input: validate it at the boundary like any other.
