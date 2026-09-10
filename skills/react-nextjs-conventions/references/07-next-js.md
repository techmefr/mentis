# react-nextjs-conventions §7 — Next.js

> Section 7 of `skills/react-nextjs-conventions`. Read it when the App Router, a server component, a route handler. The other sections and the guardrails stay in `SKILL.md`.

1. Parallelise independent fetches with `Promise.all` in Server Components: one `await` after another
   creates a network waterfall that's invisible when reading the component top to bottom. The cost is
   additive and grows with the page — three sequential 200 ms calls are a 600 ms blank screen that profiles
   as "the backend is slow", and no amount of tuning on the backend will move it.
2. **A slow fetch with no Suspense boundary above it blocks the whole route's first paint.** A `loading.tsx`
   or a `<Suspense>` around the part that waits is what lets the rest of the page arrive immediately;
   without one, the fastest section of the screen is delayed by the slowest, and the user sees nothing
   rather than most of it.
3. `next/dynamic` for any heavy component not needed for the first paint (rich editor, chart, complex
   modal), with `ssr: false` if it depends on the DOM/window — and only then, since that flag also costs
   the server-rendered markup (§10.15).
4. `cookies()`/`headers()`/`draftMode()`/`params`/`searchParams`: always `await` (Next 15+). Forgetting it
   returns a promise that reads as an object, so the code compiles, the property is `undefined`, and the
   bug surfaces as missing data rather than as a missing `await`.
5. **Reading cookies or headers opts the route out of static rendering.** That makes it a decision, not a
   convenience: adding one to a shared helper turns every page that imports it dynamic, and the whole tree
   silently starts rendering per request. Read them as close to the place that needs them as possible, and
   know which behaviour you are choosing.
6. **After a mutation, invalidate what it changed.** A Server Action that writes and returns without
   `revalidatePath`/`revalidateTag` leaves the cached page in place, so the user sees their edit fail to
   appear and tries again — the save worked, the screen lied, and the second attempt is now a duplicate.
7. **`redirect()` and `notFound()` work by throwing.** Nothing after the call runs, and wrapping either in a
   `try`/`catch` swallows the control flow so the navigation never happens; call them outside the `try`, or
   after it. Use `notFound()` for a missing record rather than rendering an empty page, because the status
   code is what a crawler, a monitor and an API caller actually read.
8. An error boundary is a Client Component (`'use client'`); `global-error.tsx` wraps `<html><body>`.
9. **The client boundary is a serialisation boundary.** Props crossing from a Server Component to a Client
   Component must be serialisable, which is why passing a function, a class instance or a Date-keyed Map
   fails with an error that names neither. Pass data down and let the client component own its handlers —
   and remember what else crosses that line: everything sent as a prop is embedded in the HTML payload
   (§9.10).
10. `route.ts` exports **named** handlers (`GET`, `POST`…), never `export default`. The router matches by
    export name, so a default export produces a route that exists and responds 405 to everything, which
    looks like a routing bug rather than a signature one. `page.tsx`/`layout.tsx` and the other convention
    files sit right next to `route.ts` in the same folder and take the opposite rule — default export
    required, no named alternative (§1.3) — so the two file kinds are easy to cross-apply from memory.
11. `next/head` is ignored in the App Router: go through the `Metadata` API. Nothing warns — the tags simply
    do not appear, and it is usually a crawler or a link preview that reports it, weeks later.
12. No mutable module-level state on the server side (`let`/`var` outside a function): it's shared between
    concurrent requests, i.e. between users. A cache keyed by "the current user" written at module scope
    serves one account's data to the next request that arrives, and the more traffic there is the more
    reliably it happens — so it passes every local test and fails in production only.
13. **An exported Server Action is a public endpoint**: it is callable by an unauthenticated client and
    checks authorisation itself. Being imported by one protected page proves nothing — the action is
    reachable by its own generated identifier, independently of any page.
14. **A Server Action's arguments come from the network.** The typed signature is erased at runtime, so the
    types describe an intention and validate nothing: parse the input with a schema at the top of the action
    (§3.15). An action typed to receive an id and handed an object is the same class of hole as a route
    handler that trusts its body.
15. A `GET` handler has no side effect — it gets prefetched and preloaded. A mutation is a `POST`. A
    link the router prefetches on hover will invoke a `GET` that deletes something, without a click.
16. **Middleware is a routing layer, not the authorisation layer.** Its matcher decides where it runs, so it
    is one config edit away from not running on the route that needed it, and it cannot see the record being
    requested. Redirect there if that helps the user; make the decision that matters where the data is
    accessed.
17. **Dynamic segments are strings.** `params.id` is `'12'`, never `12`, so a comparison against a numeric
    identifier fails while both sides look right in the log. Parse at the boundary and keep the parsed value
    for the rest of the request.
18. **`server-only` is a guard worth using.** Marking a module that touches secrets or the database makes an
    accidental import from a Client Component a build error instead of a leak (§9.3) — the import graph is
    what decides, and it is not visible from the file you are editing.
