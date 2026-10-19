# data-fetching-state-conventions §2 — Server state: cache, keys, staleness, invalidation, mutations

> Section 2 of `skills/data-fetching-state-conventions`. Read it when data is fetched, cached, refreshed,
> mutated or prefetched. Terms are those of the query-cache library the sources describe (v5); another library
> maps them. The hook and composable spelling of each rule is in the stack blocks listed in `SKILL.md`.

## Keys and functions
1. **A key identifies the data and is the function's dependency list.** It is an array, serialisable, hashed
   deterministically (object property order does not matter, array order does). Every variable the fetch
   function reads and that can change goes in the key; a variable left out means two requests share one cache
   entry. A lint rule for exhaustive dependencies exists in the library's plugin.
2. **Co-locate key and function in one helper** (`queryOptions`, `infiniteQueryOptions`), so the key is built in
   one place, usages share it, and the types follow. Components override only presentation options such as
   `select`.
3. **The fetch function resolves with data or throws.** An HTTP client that does not throw on a 4xx or 5xx
   (the browser `fetch` is one) must be wrapped so a non-OK response throws, otherwise the failure is cached as
   data. Resolving `undefined` is treated as a failure: return `null` for "nothing".
4. **Pass the abort signal the library supplies to the request**, so a superseded or unmounted query cancels its
   request instead of racing the next one.
5. **Serial dependent requests are a waterfall.** A second request that needs the first's result costs a round
   trip; where possible, restructure the endpoint so one request returns both. Prefetch data before the
   component that needs it renders (on route entry, on hover intent) and keep nested components from each
   starting their own chain.

## Staleness
6. **Staleness is a per-resource decision.** By default cached data counts as stale at once, so a new consumer,
   a refocused window or a reconnect triggers a background refetch; unused entries are discarded after five
   minutes; a failing query retries three times with backoff before showing an error. Choose `staleTime` for
   the data: seconds-to-minutes for a list; `Infinity` for data only an invalidation should refresh (an
   invalidation still refetches it); `'static'` for data nothing should refetch, invalidation included. A balance,
   a stock level or a permission is not cached for minutes.
7. **Do not retry what cannot succeed.** A 401, 403 or 404 retried three times is load without benefit; set
   `retry` per error class. In tests, turn retries off or an error case times out.
8. **Disable with a condition, not with a conditional call.** The `enabled` option (or the type-safe skip token)
   gates a dependent query. A disabled query with no data is pending and idle, so a spinner keyed on "pending"
   shows forever: key it on "pending and fetching". A skipped query cannot be refetched manually; if a manual
   trigger is needed use the `enabled: false` form.
9. **Server rendering: a client per request.** Create the cache client for each request (or each server
   component), prefetch in the loader, dehydrate it into the page, and hydrate it on the client. Dehydration
   keeps only successful queries by default; a failed prefetch is retried on the client and the server output
   shows a loading state, which is right for non-critical content; for critical content, await the fetch
   without swallowing errors and answer with the right status. The serialiser of most frameworks cannot carry
   `undefined`, `Error`, `Date`, `Map`, `Set` or `BigInt` out of a query: return plain data.
10. **Data rendered on the server and fetched again by a client component can drift.** The cache cannot
    revalidate a server component. Pick one owner per piece of data, or accept `staleTime: Infinity` for it.

## Changing data
11. **Invalidate; do not hand-write the cache.** After a successful mutation, invalidate by key prefix (every
    list of that resource), or exactly, or with a predicate. Invalidation marks matching entries stale
    regardless of `staleTime` and refetches the ones in use. Return the invalidation promise from the success
    callback so the mutation stays pending until fresh data arrived, if the screen must not show stale rows in
    between.
12. **Optimistic updates have two shapes; pick the smaller.** Rendering the pending mutation's *variables* in
    the list (with a pending style) needs no cache write and no rollback, and failure is just a state to show
    with a retry; use it when one place shows the result. Writing to the cache in the mutation's start handler
    updates every consumer, but must return the previous value as a rollback for the error and settle handlers,
    cancel in-flight reads of that key first, and still invalidate when settled. An optimistic write without a
    rollback leaves the UI asserting something the server refused.
13. **Mutations do not retry by default**, and run in parallel. Give a mutation a scope when order matters (they
    then run one at a time). Callbacks passed to the trigger call run once and only while the component is still
    mounted; put the data-contract effects (invalidation) in the mutation definition and screen effects (a
    toast, a navigation) at the call site.
14. **Use the promise form of a mutation only when composing**, and handle its rejection; otherwise use the
    callback form (`skills/react-nextjs-conventions` §6.8 states it for hooks).

## Rendering cost
15. **Select the slice a component needs** with `select`, and keep that function referentially stable (defined
    outside the render or memoised), because it reruns when its identity changes. Results are structurally
    shared, so unchanged data keeps its reference; that only works for JSON-compatible values. Do not
    destructure the result with a rest pattern, since the library tracks which fields a component reads and
    rest destructuring marks them all as read. The returned result object itself is not stable between renders;
    the `data` inside is.

## Tests
16. **A fresh cache client per test**, retries off, no shared module-level client, and the network mocked at
    the boundary (not the hook). A shared client leaks state between tests and parallel tests influence each
    other. In Jest, an infinite garbage-collection time avoids the "did not exit" warning.

## Mechanical checks

```
grep -rnE "queryKey: *\[" src | grep -v "queryOptions"
grep -rnE "fetch\(" src | grep -v "ok"
grep -rnE "staleTime|gcTime" src
grep -rnE "retry:" src
grep -rnE "new QueryClient" src
grep -rnE "\.\.\.[a-z]+\} *= *use(Query|InfiniteQuery|Mutation)" src
grep -rnE "setQueryData" src
```

- A literal `queryKey` outside the helper module is rule 2.
- `new QueryClient` at module level in server-rendered code is rule 9; in a client-only app it is fine.
- Every `setQueryData` is checked against rule 11-12: is there a rollback, and is the key invalidated afterwards.
