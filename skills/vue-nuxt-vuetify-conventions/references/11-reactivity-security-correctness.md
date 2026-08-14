# vue-nuxt-vuetify-conventions §11 — Reactivity and security correctness (linter-derived)

> Section 11 of `skills/vue-nuxt-vuetify-conventions`. Read it when reviewing a diff, or chasing a reactivity bug. The other sections and the guardrails stay in `SKILL.md`.

1. Never invoke a prop callback (`props.onXxx()`) during the body of `setup()` or inside a `computed`
   getter: that's a side effect on the render path, replayed on every re-evaluation and during SSR. It goes
   in an event handler, a `watch`, or a lifecycle hook.
2. A `watch`/`watchEffect` that registers a listener/timer/observer (`addEventListener`,
   `setInterval`/`setTimeout`, `IntersectionObserver`/`MutationObserver`/`ResizeObserver`,
   `WebSocket`/`EventSource`/`BroadcastChannel`) must have its **exact** cleanup returned or done through
   `onWatcherCleanup`: whatever is added is explicitly removed.
3. Never an auth token/secret in `localStorage`/`sessionStorage`: exposed to any XSS payload. A cookie
   that's `HttpOnly`, `Secure`, `SameSite` and set server-side is the only sane option.
4. `eval()`, `new Function()`, and `setTimeout`/`setInterval` with a string argument are XSS/RCE vectors:
   explicit logic, `JSON.parse` for data.
5. Assigning `innerHTML`/`outerHTML` injects unsanitised markup (a direct DOM XSS sink): `textContent` for
   text, or sanitise before assigning if HTML really is necessary.
6. Server routes (h3): `throw createError()`, never `throw new Error()` — the latter leaks the stack trace
   and internal details.
7. `readValidatedBody()` parses and validates the request body in one step; `readBody()` leaves you to
   remember the validation.
8. The `event` parameter of a `defineEventHandler` is typed explicitly; an untyped handler loses the
   guardrails on `event.context`/`event.node`.
9. No mutable module-level state on the server side, shared between concurrent requests.
