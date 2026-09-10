# vue-nuxt-vuetify-conventions §11 — Reactivity and security correctness (linter-derived)

> Section 11 of `skills/vue-nuxt-vuetify-conventions`. Read it when reviewing a diff, or chasing a reactivity bug. The other sections and the guardrails stay in `SKILL.md`.

1. **Never invoke a prop callback (`props.onXxx()`) during the body of `setup()` or inside a `computed`
   getter**: that's a side effect on the render path, replayed on every re-evaluation and during SSR. It
   goes in an event handler, a `watch`, or a lifecycle hook. The symptom is a callback that fires twice
   on the server and once more per unrelated render, so the count depends on what else changed.
2. **A `watch`/`watchEffect` that registers a listener, timer or observer must return its exact cleanup**
   — `addEventListener`, `setInterval`/`setTimeout`,
   `IntersectionObserver`/`MutationObserver`/`ResizeObserver`,
   `WebSocket`/`EventSource`/`BroadcastChannel` — or do it through `onWatcherCleanup`: whatever is added
   is explicitly removed. "Exact" is the load-bearing word: removing a listener with a different function
   reference removes nothing, and it looks like cleanup in the diff.
3. **Never an auth token or secret in `localStorage`/`sessionStorage`**: it is readable by any XSS
   payload, including one arriving through a dependency you did not write. A cookie that is `HttpOnly`,
   `Secure`, `SameSite` and set server-side is the only sane option — the point being that the JavaScript
   on the page cannot read it at all.
4. **`eval()`, `new Function()`, and `setTimeout`/`setInterval` with a string argument are XSS/RCE
   vectors**: explicit logic, `JSON.parse` for data.
5. **Assigning `innerHTML`/`outerHTML` injects unsanitised markup** (a direct DOM XSS sink):
   `textContent` for text, or sanitise before assigning if HTML really is necessary. `v-html` is the same
   sink with framework syntax — the fact that it is a template directive rather than a DOM call changes
   nothing.
6. **A `computed` is pure.** Mutating another `ref` from inside a getter either loops or produces a value
   that depends on evaluation order, and evaluation order is not yours to choose: a getter runs when
   something reads it, which can be a template, a watcher or the SSR pass. If a read has to cause a
   change, that is a `watch`.
7. **Watch a getter, not an object, unless you mean deep.** `watch(obj, ...)` does not fire when a nested
   property changes; `watch(() => obj.x, ...)` says exactly what you depend on. `deep: true` works and
   costs a full traversal on every change, so it is a decision rather than a default — and on a large
   payload it is the decision that makes a page feel slow for no visible reason.
8. **A `v-for` key is a stable identity, never the array index.** With the index, removing or reordering
   a row makes Vue reuse the wrong DOM node, so an input's typed value, an open menu or a checked box
   silently belongs to a different record. Nothing errors, and the user is the one who discovers it.
9. **`v-if` and `v-for` never share an element**, and filtering does not happen in the template: derive
   the list in a `computed`. In the template, the condition is evaluated per item on every render, and
   the intent — "this list, filtered" — is spread across two directives.
10. **Server routes (h3): `throw createError()`, never `throw new Error()`** — the latter leaks the stack
    trace and internal details to the client, which is a disclosure bug, not a formatting one.
11. **`readValidatedBody()` parses and validates the request body in one step**; `readBody()` leaves you
    to remember the validation. The same holds for the query and the route params — they are strings from
    the client, they are not typed by the route's shape, and
    `getValidatedQuery`/`getValidatedRouterParams` exist so that the validation cannot be the step
    someone skips.
12. **Never read a user's identity from something the client can set.** A header, a query parameter or a
    body field naming the current user or tenant is an assertion by the caller; the identity comes from
    the session the server resolved. This is the shape that turns an ordinary endpoint into horizontal
    privilege escalation.
13. **Never build a redirect target from user input without an allow-list.** A `?next=` taken at face
    value is an open redirect, which is what makes a phishing link look like it came from your domain.
14. **The `event` parameter of a `defineEventHandler` is typed explicitly**; an untyped handler loses the
    guardrails on `event.context`/`event.node`. And do not assume a field another layer was supposed to
    put on `event.context` is there — check it, because the failure mode of a missing middleware is a
    route that runs unauthenticated rather than one that errors.
15. **No mutable module-level state on the server side, shared between concurrent requests.** See §2.8:
    this is the same defect seen from the server route rather than from the composable, and it is a
    cross-account leak either way.
16. **An endpoint that accepts an unbounded collection does unbounded work.** Cap the array length, the
    page size and the upload size at the boundary; without a cap, one caller decides how much CPU and
    memory the process spends, and the first time it happens it will not be a caller acting in good
    faith.
17. **A CSRF cookie is `httpOnly`, `Secure` and at minimum `SameSite=Lax`; `Strict` where the app has no
    cross-site entry point to preserve.** The double-submit pattern (a cookie value echoed back in a
    request header) only defends anything if the cookie itself cannot be read or forged by the page that
    is attacking the user — a cookie set without `httpOnly` is one `document.cookie` away from being
    replayed by the same XSS payload §11.3 already worries about, and a missing `SameSite` lets a
    cross-site form submit it on the victim's behalf without needing to read it at all.
18. **A composable called conditionally, or inside a loop, is a composable whose internal `ref`s and
    lifecycle hooks attach to a render that may not happen the same way twice.** Vue's own composable
    contract assumes a stable call order across renders — the same reason hooks work in other reactive
    frameworks — so gate the *logic* inside the composable with an early return, not the *call* to the
    composable itself with a surrounding `if`.
19. **`markRaw()` on a third-party instance a component only holds a reference to** (a map, a chart, an
    editor) stops Vue from wrapping it in a reactive proxy it was never designed to survive. Without it,
    the library's own internal mutations run through Vue's proxy traps on every call, which is wasted work
    at best and, for an object whose class checks `this instanceof X`, an object that fails its own
    identity check at worst.
20. **A ref or computed that is genuinely never read outside its own module is dead reactive state, not a
    cheap safety net.** Every `ref` left in a component "in case a future feature needs it" is change
    detection Vue pays for on every mutation, for a subscriber that does not exist; delete it with the
    feature it was speculating for, and let the feature that actually needs it declare its own.
