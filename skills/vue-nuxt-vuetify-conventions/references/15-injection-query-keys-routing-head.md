# vue-nuxt-vuetify-conventions §15 — Injection, query keys, routing and head

> Section 15 of `skills/vue-nuxt-vuetify-conventions`. Read it when a value is passed down a tree without
> props, a server-state query is keyed, a route guard or middleware is written, or a page's title and meta
> are set. The other sections and the guardrails stay in `SKILL.md`.

## Provide and inject

1. **An injection key is a typed symbol defined once, never a string.** A string key collides with whatever
   another module chose, and returns `unknown` at the call site. Declare the key as a symbol typed with the
   value's interface, export it from the shared layer that both provider and consumers may import (§5), and
   let the type flow through both ends. A rename is then a compile error, not an empty injection.
2. **`inject` can return nothing, and the consumer says what that means.** Wrap the call in a small
   `useX` function: if the provider is missing it throws a named error ("must be used inside the X
   provider"), and every caller gets a defined value. A non-null assertion at each call site hides the
   mistake until a descendant is mounted outside its provider, and the resulting `undefined` surfaces three
   components away from the cause.
3. **The provider owns the mutations.** Provide a read-only view of the state and explicit functions that
   change it; do not provide the raw mutable ref. A descendant that can write the state is a descendant
   nobody can find by searching for the writes, and the same state ends up edited from four places with
   four sets of validation.
4. **Choose the channel by scope.** Data needed by one subtree (a form group, a table with its toolbar, a
   family of compound components) is provided. Server state is the query cache's job, and state shared by
   unrelated parts of the application is a store (§2). Injection used as a hidden global is a store without
   the tooling, and a component that injects it cannot be understood from its props.
5. **Inject during setup, before the first await.** The injection context exists while the component's
   setup runs synchronously; a call made later, inside a callback or after an await in a plain setup
   function, finds no current instance and returns the default. A composable that injects follows the same
   rule as one that registers a lifecycle hook (§11, point 18): it is called from setup, unconditionally.

## Keys of server-state queries

6. **The reactive source goes into the key, not its value.** A query library caches by key and refetches
   when the key changes. Passing the ref, the computed or a getter keeps the key reactive; reading `.value`
   at the call site freezes it at its first value, and the screen shows the first id's data for every id
   that follows. The fetch function reads the same inputs through `toValue`.
7. **Every variable the fetcher reads is in the key.** A filter, a page number, a locale or a tenant used
   in the request but absent from the key serves one user's page to another's request. The test is
   mechanical: remove a variable from the key and ask whether the cache would still tell two different
   requests apart.
8. **Keys are arrays ordered from broad to specific, built by one factory.** `['orders', 'list', filters]`
   and `['orders', 'detail', id]` let a mutation invalidate by prefix (everything about orders, or only the
   lists) without enumerating keys. Hand-typing the key at each use is how an invalidation misses one
   spelling, and the stale screen is reported as a cache bug.
9. **A mutation invalidates, or updates, on purpose.** After a write, invalidate the prefix whose data
   changed. An optimistic update captures the previous cache value before writing and restores it in the
   error path; an optimistic update without that rollback leaves the interface showing a state the server
   refused (`skills/testing-anti-patterns` lists it among the regressions agents introduce).

## Router and middleware

10. **Watch what you need from the route, not the route.** `watch(() => route.params.id, …)` runs when the
    id changes; watching the route object also runs on a query-string or hash change and refetches for no
    reason. Read parameters through a getter, and treat a parameter as a string or an array of strings
    until it has been validated.
11. **A client-side guard is a convenience, never the lock.** A guard keyed on route meta (`requiresAuth`)
    redirects an unauthenticated visitor before a flash of protected UI; it protects no data, because the
    API is called directly. The authorisation decision lives in the server (`skills/auth-session-conventions`)
    and the guard only mirrors it. A guard returns a decision (cancel, a location to redirect to, or nothing
    to continue) and does not call a `next` callback in new code.
12. **Route middleware reads its arguments, not the ambient route.** In Nuxt a route middleware receives
    the target and the origin as parameters; the composable that returns the current route does not describe
    the navigation in flight, so reading it there guards the wrong page. Redirect by returning a
    navigation, cancel by returning an abort, and keep the body cheap: it runs on the server for the first
    request and on the client for every later navigation.
13. **Server middleware sets context and never answers.** A Nitro middleware runs before every route, and
    before asset requests too. It may attach to the event context or set headers; returning a value from it
    ends the request. Anything heavier than reading a header (a database call, a token exchange) belongs in
    the route or in a dedicated utility called by the routes that need it.
14. **Rendering strategy is declared in one place.** `routeRules` in the Nuxt config states, per path
    pattern, whether a route is prerendered, rendered on each request, served from a revalidating cache, or
    client-only, plus its redirects and headers. A scattering of per-page overrides makes the rendering model
    unknowable; and because the rules are applied at build and server start, they are verified against the
    production build, not the dev server.
15. **`definePageMeta` takes static values only.** It is hoisted out of the component by the compiler, so
    reactive data and function calls in it are not evaluated the way they read. Type the custom meta fields
    once by augmenting the meta interface, never by casting at the use site.

## Head and meta

16. **Static head in the config, reactive head in the component.** The config's head entry is for values
    that never change (charset, viewport, site-wide icons). A page title, description and social tags depend
    on the page's data, so they are set with the head composables inside setup, where they follow reactive
    state and are rendered on the server. Assigning `document.title` by hand skips the server render and is
    overwritten on navigation.
17. **Strings in the head are i18n output.** The title and description are built from translation keys
    (§6), so a locale switch updates them; a hard-coded English title on a French page is the most
    visible untranslated string the site has, and the one a search result shows.
18. **Tags only a crawler needs are server-only.** The composable for server-only meta keeps them out of
    the client bundle and the payload. Inline script and style entries in the head are the same sink as
    `v-html` (§16): never built from data a user wrote.
19. **A response served by the Nitro layer is serialised as JSON.** A date arrives as a string and a class
    instance as a plain object, whereas the payload of the page-data composables is serialised in a form
    that preserves dates and collections. Type the client side for what actually crosses the wire, and give
    a type that must survive a JSON response an explicit serialisation method. Trimming the payload with the
    composable's pick or transform option shrinks what is sent; it does not skip the request.
20. **A path is resolved from the configuration, not from the default layout.** The source directory, and
    the directories for pages, layouts, middleware and plugins, are settings that a project can override (a
    layered or feature-sliced structure often does). Read the project's Nuxt configuration before assuming where
    a file belongs or before searching for one; the server directory and the configuration files stay at the
    project root whichever source directory is chosen. A file created in the default location of a project that
    moved it is silently ignored, which reads as "the middleware does not run".
