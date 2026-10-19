# react-nextjs-conventions §14 — Next.js 16 Cache Components

> Section 14 of `skills/react-nextjs-conventions`. Read it when the project's `next.config` sets
> `cacheComponents: true` (on in the recommended defaults of a new app), when a route sets `dynamic`, `revalidate` or `fetchCache`, when
> `"use cache"` appears, or when a Next 15 app is being moved to 16. Without the flag, the older model of §7 applies
> and this section does not. **Version stamp:** documentation of the framework's repository read 2026-10-02 (latest
> release that day: 16.3.8). Items marked `[verify]` appear in that documentation but were not confirmed to exist in
> the release a project has installed; read the docs shipped in the installed package
> (`node_modules/next/dist/docs/`, from 16.2, `skills/source-freshness` §3.6) before relying on them.

## The model
1. **Nothing is cached unless you say so.** With the flag on, every fetch runs at request time until a
   `"use cache"` directive marks a page, a component or a function as cacheable. Existing `fetch`
   caching and `unstable_cache` keep working and can be migrated later.
2. **A route renders as a static shell plus streamed parts.** At build time the tree is rendered: cached results,
   synchronous pure work and module imports become part of the shell; each `<Suspense>` fallback is shipped in it;
   what needs the request (cookies, headers, search parameters, unknown route parameters, uncached async data)
   streams at request time. This is Partial Prerendering and is the only mode.
3. **Everything async that is neither cached nor inside a boundary is an error to fix**, not a style choice. The
   dev overlay reports a "blocking route" insight naming the component. Either cache it, wrap it in `<Suspense>`
   with a fallback that makes sense, or (for work that must run per request) call `connection()` first and wrap.
   Insights do not show in the HTTP response, which still returns 200: read the overlay or the dev log.

## Writing cached code
4. **`"use cache"` goes on an async function, component, page or layout; at the top of a file it caches every
   export** (all of them must be async). Prefer data-level caching for a fetch shared by several components and
   UI-level caching for a whole block of markup.
5. **Pair every cache directive with `cacheLife`**; without it the implicit `default` profile applies (stale 5
   minutes, revalidate 15 minutes), which hides the intent at the call site and in nested cached scopes. Built-in
   profiles: seconds, minutes, hours, days, weeks, max, or a custom profile. A very short lifetime keeps the
   result out of the static shell.
6. **Arguments and captured outer variables form the cache key** (with the build id). Everything that changes the
   result must therefore be an argument or a captured value, and arguments and return values must be serialisable:
   plain objects, arrays, primitives, with elements and server actions only passed through, never inspected.
7. **A cached scope cannot read `cookies()`, `headers()` or `searchParams`, directly or through a helper it
   calls.** Read them outside, extract the value, and pass it in as an argument. A runtime-bound lifetime has two
   variants: private (executes on the server, reads runtime data directly, cached in the browser) and remote
   (durable store shared across instances, worth the network round trip only at a high hit rate).
8. **The default store is in memory and per instance.** On serverless it is discarded with the instance and is
   scoped to one deployment, since the key includes the build id; unlike the old data cache it does not persist
   across deployments. Choose the remote variant or a cache handler where durability matters.
9. **`React.cache` does not cross a cache scope**: each cached function has its own, so it cannot hand data into
   one; where matching calls must share work, use the private variant or a stale-forever lifetime.
10. **Do not rely on `Math.random()`, `Date.now()`, `new Date()` or `crypto.randomUUID()` during prerender**:
    they fail the build and are not cleared by the opt-out below. Defer them to request time (`connection()`
    plus `<Suspense>`) or cache the result so all users share one value. `performance.now()` for timing is
    exempt.
11. **Read local files that never change once, at module scope**, not inside a render, where they count as
    uncached async data.
12. **Push awaits down the tree.** The deeper the dynamic read sits, the more of the page is in the shell: pass the
    `params` promise (or `cookies()` result) to the child that needs it and await there, instead of awaiting in a
    layout, which makes the layout itself dynamic.

## Dynamic routes
13. **`generateStaticParams` must return at least one param.** An empty array errors; removing the export opts
    out of regenerating, so the route renders on every request even when it uses `"use cache"`. Unlisted paths
    are still rendered on request.
14. **`dynamicParams` is not supported** and fails the build; to reject unknown params, call `notFound()` when
    the param resolves to nothing.
15. **Client hooks that read the route** (`useParams`, `usePathname`, the segment hooks) suspend when the pathname
    depends on parameters not yet known; `useSearchParams` always needs a `<Suspense>` boundary.

## Segment config and migration
16. **After enabling the flag, `dynamic`, `revalidate` and `fetchCache` exports error.** Replacement: remove
    `force-dynamic` (uncached async work already runs at request time); for `force-static` and `dynamic =
    'error'` cache the data with `"use cache"` and a lifetime and remove the config; replace `revalidate > 0`
    with a `cacheLife` profile and `revalidate = 0` by removing it; `fetchCache` becomes "inside a cache scope or
    not"; `noStore()` is unneeded (use `connection()` plus `<Suspense>` for request-time work); `runtime =
    'edge'` must move, as the feature needs the Node.js runtime.
17. **Migrate incrementally if the app is large**: opt routes out of validation per segment (`instant = false`,
    `[verify]`) so the app builds, then convert one route at a time. The opt-out marks a segment as allowed to
    block; it does not make it dynamic and does not clear the synchronous-time/random errors of rule 10.
18. **Navigation keeps state.** With the flag on, the previous route is hidden, not unmounted (React `Activity`):
    state is preserved, effects are cleaned up while hidden and recreated on return, and a few recent routes are
    kept. Dropdowns, dialogs and tests that assumed unmounting need a look.

## Invalidation (extends §7.6)
19. **Tag cached data with `cacheTag` inside the cached scope and choose the invalidation by the behaviour:**
    `updateTag(tag)` for read-your-own-writes after a mutation (Server Action only; the next request waits for
    fresh data); `revalidateTag(tag, profile)` for stale-while-revalidate, with a profile as the required second
    argument (`'max'` serves cached data while it refreshes), usable in Server Actions and Route Handlers (a
    webhook); `revalidatePath` unchanged. Tags are case-sensitive and at most 256 characters.
20. **Prefetching `[verify]`.** With partial prefetching enabled, a link prefetches the route's app shell; setting
    `prefetch` on a link also prefetches cached content that depends on its URL data, at the cost of a server
    invocation per link. Do not enable it on long lists.

## Mechanical checks

```
grep -rnE "cacheComponents" next.config.*
grep -rnE "export const (dynamic|revalidate|fetchCache|dynamicParams|runtime) *=" app
grep -rnE "['\"]use cache" app src 2>/dev/null
grep -rnE "cacheLife|cacheTag" app src 2>/dev/null
grep -rnE "new Date\(\)|Date\.now\(\)|Math\.random\(\)|randomUUID\(\)" app src 2>/dev/null
grep -rnE "unstable_noStore|noStore\(" app src 2>/dev/null
grep -rnE "generateStaticParams" -A3 app | grep -E "return \[\]"
grep -rnE "revalidateTag\([^,)]*\)" app src 2>/dev/null
```

- A `"use cache"` with no `cacheLife` in sight is rule 5. A cached function that calls `cookies()` or `headers()`
  (or a helper that does) is rule 7.
- `revalidateTag` with one argument is a finding on 16: the profile is required.
- Segment config exports in a project with the flag on are rule 16; with the flag off they are normal.
