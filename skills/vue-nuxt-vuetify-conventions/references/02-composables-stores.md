# vue-nuxt-vuetify-conventions §2 — Composables and stores

> Section 2 of `skills/vue-nuxt-vuetify-conventions`. Read it when logic moves out of a component, or a store is touched. The other sections and the guardrails stay in `SKILL.md`.

1. **A composable owns exactly one domain**, and a function lives in the composable whose subject it
   matches — a contract-sync function belongs in the contract composable, never in the contract-line one.
   The name is a promise about what's inside; "I was already in this file" is how that promise breaks.
2. **No namespace stutter**: a member reached through something that already names its domain doesn't
   repeat it. `useContract().sync()`, not `useContract().syncContract()`.
3. A store (Pinia or equivalent) is for state genuinely shared across **unrelated** components or pages.
   Everything else stays a composable, a `ref`, or an SSR-safe shared state primitive — a store used as a
   convenient global is how state becomes untraceable.
4. `defineStore()` is called once at module level, never inside a `setup()`/composable/function body:
   otherwise each call recreates a store definition instead of reusing the shared singleton.
5. Async loading and error state belong to whatever owns the fetch, exposed explicitly (`data`,
   `pending`, `error`), never inferred by the caller from a null check. A caller reading emptiness as
   "still loading" cannot tell it apart from "loaded, and there is nothing", and will render a spinner
   forever on the one account that legitimately has no rows.
6. A data-fetching composable carries its own fetch and returns `data`/`refresh`. The caller asks for the
   subject, not for the request: `refresh()` is a word the view can use, a re-issued `$fetch` is not.
7. **Decide, deliberately, whether the state is shared or per-caller — and say which in the name.** A
   `ref` created inside the composable gives every caller its own copy; a `ref` at module scope makes one
   copy for everybody. Both are legitimate and they look identical from the call site, which is why the
   bug is silent: two components that were each supposed to hold their own selection end up fighting over
   one, or a value meant to be global resets because a second caller made a second copy. If a composable
   shares, its name or its doc line should let the caller know before they read the body.
8. **Module-scope state is shared across requests on the server.** In SSR the module is instantiated once
   per process, not once per visitor, so a `ref` declared outside the composable body carries one user's
   data into the next user's render. Use the framework's request-scoped primitive (`useState` in Nuxt)
   for anything that must be shared and server-rendered. This is not a performance nuance — it is a
   cross-account data leak, and it does not reproduce locally where you are the only visitor.
9. **A composable that touches lifecycle, injection or the route must be called synchronously in
   `setup`.** After an `await`, the active component instance is gone: `onMounted` never registers,
   `inject` returns the default, and the composable silently does nothing rather than failing loudly.
   Call it first, then await — or move the async work behind a function the composable returns.
10. **Deduplicate a request that is already in flight.** A store action fetching on mount and again from
    a watcher fires twice on the first render; keep the pending promise and return it to the second
    caller. Without that, two responses race and the one that wins is whichever the network delivered
    last, which is not necessarily the one for the current arguments.
11. **Provide one reset, don't reset field by field at the call site.** Hand-written teardown forgets the
    field somebody adds next month, and the symptom lands far away — stale filters after a logout, a
    previous customer's rows on the next customer's page. One reset in the store is one place to keep
    true.
12. **A getter is a projection, not a fetch.** No side effects and no async inside a `computed`: it
    re-runs whenever its dependencies change, at a moment you don't choose, and a request from inside it
    is a request you cannot cancel, sequence or count. If loading has to be triggered by reading, make it
    an explicit call.
13. **A watcher created outside a component's scope never stops.** A composable that watches must either
    be called from `setup` — so the component's effect scope disposes it — or own the stop handle and
    release it in `onScopeDispose`. An orphaned watcher keeps recomputing against unmounted state and is
    a real memory leak, not a tidiness point.
14. **A store may import another store; a cycle between two is a design error.** When A needs B and B
    needs A, the shared derivation belongs in a composable both can call, or one of them owns the state
    outright. Circular store access resolves at import time in an order nobody controls, so it fails as
    `undefined` on a field that plainly exists.
15. **Don't put in a store what the URL should own.** A filter, a tab, a page number or a selected id
    that lives only in memory cannot be linked, bookmarked or reloaded, and the user's back button
    silently disagrees with the screen. Route query is the store for anything the user would expect to
    survive a refresh or land in a colleague's chat; the store keeps what is genuinely ephemeral.
16. **Check for a nearby composable before writing a second one.** Two composables covering the same
    subject diverge — one gets a fix, the other keeps the bug, and a reviewer cannot tell which the next
    component should call. This is the `SKILL.md` guardrail; the reason it is a guardrail is that
    duplication here is cheap to create and expensive to notice.
17. **A setup store is the default once a store needs anything an options store can't express** (a watcher
    inside the store, a composable called from it, a private ref that isn't part of the public surface).
    An options store's `state`/`getters`/`actions` split is easier to read for a plain data bag, but it has
    no room for private state or lifecycle — picking setup-style only once the store outgrows options is
    how a project ends up with both shapes and no reason a reader can find for which store uses which.
    [pinia.vuejs.org/core-concepts]
18. **`storeToRefs`, never destructuring the store object directly, when a component needs individual
    properties.** Destructuring a Pinia store's state or getters copies the current value out and detaches
    it from reactivity — the component keeps whatever the value was at that instant and never sees the
    store change again, silently, with no warning at build or run time. `storeToRefs` produces refs that
    stay wired to the store, which is the whole reason the helper exists rather than just documenting the
    pitfall. [pinia.vuejs.org]
19. **`$subscribe` for anything reacting to *how* the state changed, not a `watch` on the whole store.** A
    plain `watch(() => store.$state, ...)` fires on every mutation and hands back only the new value; the
    store's own subscription fires once per patch (not once per field inside it) and hands back the
    mutation's type and payload, which is what a persistence layer or an audit log actually needs to know
    — whether the change was a direct assignment, a `$patch` object, or a `$patch` function.
    [pinia.vuejs.org/core-concepts/state.html]
20. **`$patch` for a mutation that touches several fields together**, rather than assigning them one at a
    time. Several separate assignments are several separate reactivity triggers and several separate
    devtools entries for what is conceptually one state transition; `$patch` (an object or a function)
    applies the whole group as one, which is also what makes a subscriber's `mutation.type` of `"patch
    object"` meaningful in the first place.
21. **A cross-cutting concern shared by every store — persistence, undo, analytics — is a Pinia plugin, not
    logic pasted into each store's actions.** A plugin receives every store as it's created and can extend
    it uniformly (add a property, wrap `$subscribe`, wrap `$onAction`); copying the same `localStorage`
    sync or the same logging call into ten stores means ten places to fix the day the behavior changes,
    and the tenth one is the one somebody forgets. [pinia.vuejs.org/core-concepts/plugins.html]
22. **`$onAction` for observing an action's lifecycle (before it runs, after it resolves, if it throws)
    without editing the action itself.** Wrapping every action's body in a manual try/catch to log or to
    time it duplicates the same boilerplate per action and is easy to skip on the next one added; a single
    `$onAction` subscriber (typically inside the plugin from the previous point) sees every action already,
    including ones added later, with nothing added at each call site.
