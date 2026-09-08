# vue-nuxt-vuetify-conventions §12 — Recurring review patterns (quality debt observed in the field)

> Section 12 of `skills/vue-nuxt-vuetify-conventions`. Read it when reviewing a diff, for the debt that keeps coming back. The other sections and the guardrails stay in `SKILL.md`.

1. **No pre-emptive chunking or retry without a verified backend constraint**, and a notification in a
   loop is sent once. Both are the same mistake: defending against a limit nobody measured, which adds a
   code path that is never exercised and hides the real limit when it eventually shows up.
2. **A summary card above a table recomputes on the table's active filters**, not on the user's full
   scope. Otherwise the card and the rows under it disagree, and the user believes the bigger number —
   which is the one that is wrong for what they are looking at.
3. **Read the backend Resource/Model before writing a table filter or sort**: does the field take an id,
   a name, a slug? A 422 from a live request is not a specification, and trial-and-error against a
   running API produces code that matches one deployment rather than the contract.
4. **An endpoint response carries a status/type *and* a human-readable message**, not just an HTTP code —
   the front has to display something, and "something" invented client-side per call site is how the same
   failure gets three different wordings.
5. **A client-only component**: reach its DOM ref through a `watch` declared `immediate` with
   `flush: 'post'`, and expose its API through `emit('ready', api)`, not `defineExpose` — a client-only
   wrapper does not relay it, so the parent holds a handle to the wrapper and calls methods that are not
   there.
6. **Dark/light switch: cut the CSS transitions during the change** (a temporary class, a double
   `requestAnimationFrame`, an SSR guard) to avoid the flash on refresh. The flash is not cosmetic
   nitpicking — it is the visible symptom of the server having rendered one theme and the client deciding
   another, which is a §9 hydration question wearing a design costume.
7. **A default import from an icon library pulls the whole library**, and a heavy module loaded at the
   level of a rarely visited route bloats the bundle for everyone: named import, lazy component. Measure
   before and after rather than asserting the improvement.
8. **Check a permission name against the backend before wiring a menu entry or a guard on it.** A
   plausible name that does not exist either fails open or hides the entry for absolutely everyone, and
   both are silent — nobody files a bug for a menu item they never knew existed.
9. **Hiding is not authorising.** A guard that only removes a menu entry or disables a button leaves the
   route and the endpoint reachable by anyone who types the URL. The UI check is for clarity; the
   decision belongs to the server, and a review that accepts the first as the second has accepted
   nothing.
10. **A pending flag is reset in every branch, including the failing one.** Setting it before the request
    and clearing it only on success leaves a spinner running forever on the first error, which reads to
    the user as an app that hung rather than an action that failed.
11. **An optimistic update reconciles its failure.** Removing the row, then not putting it back when the
    request rejects, means the screen and the database disagree until a refresh — and the user, who saw
    the row disappear, has no reason to refresh.
12. **Server-side pagination and client-side sorting do not mix.** Sorting the page in hand looks correct
    and orders one slice of the data; the first row of page two contradicts it. Whichever side owns
    ordering owns filtering and paging too.
13. **A search index that caps its result count is a silent ceiling.** If the engine stops counting at N,
    the UI says "N results" and an export quietly truncates — the number is not the total, it is the cap.
    Find the ceiling before building anything on the count, and say so in the interface when the data
    exceeds it.
14. **Copy-pasted instead of extended.** A composable or component duplicated because the near one did
    not quite fit produces two versions that drift, and the next reader cannot tell which is current
    (§2.16). Either widen the existing one or make the difference explicit in the name.
15. **A chain of watchers is a design smell.** When A watches B which watches C, the update order becomes
    emergent, an intermediate render shows a half-updated state, and a bug there is not reproducible by
    reading any single file. Derive with `computed` and keep watchers for genuine side effects.
16. **A `catch` that logs and continues has decided the error does not matter.** Sometimes that is right,
    and then it deserves the one line saying why; usually it means the user gets no feedback and the next
    developer gets no trace. Debug logging left in the diff belongs in the same category.
17. **A component test asserting on a CSS class or on DOM structure breaks on the next restyle** without
    the behaviour having changed. Assert through stable test attributes and visible text, so a red test
    means a real regression rather than a design decision.
