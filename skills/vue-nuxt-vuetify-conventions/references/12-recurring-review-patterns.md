# vue-nuxt-vuetify-conventions §12 — Recurring review patterns (quality debt observed in the field)

> Section 12 of `skills/vue-nuxt-vuetify-conventions`. Read it when reviewing a diff, for the debt that keeps coming back. The other sections and the guardrails stay in `SKILL.md`.

1. No pre-emptive chunking/retry without a verified backend constraint. A notification in a loop = once.
2. A summary card above a table: the total recomputed on the table's **active filters**, not on the user's
   full scope.
3. Table filter: read the backend Resource/Model (does the field take an id, a name, a slug?) before writing
   the `whereIn`/sort. A 422 from a live request is not a specification.
4. Endpoint response: a status/type **and** a human-readable message, not just an HTTP code — the front has
   to display something.
5. A client-only component: DOM ref through `watch(..., { immediate: true, flush: 'post' })`; API exposed
   through `emit('ready', api)`, not `defineExpose` (a client-only wrapper doesn't relay it).
6. Dark/light switch: cut the CSS transitions during the change (a temporary class, a double
   `requestAnimationFrame`, an SSR guard) to avoid the flash on refresh.
7. A default import from an icon lib (the whole lib instead of one icon), or a heavy module loaded at the
   level of a rarely visited route, bloats the bundle for nothing: named import / lazy component.
8. Check the permission name against the backend before wiring a menu entry or a guard on it: a plausible
   name that doesn't exist fails open or hides the entry for everyone.
