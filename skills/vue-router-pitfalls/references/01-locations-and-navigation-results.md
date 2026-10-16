# vue-router-pitfalls §1 — Locations and navigation results

> Part 1 of `skills/vue-router-pitfalls`. Read it when code navigates, builds a location or reacts to what a
> navigation did. Sourced from the Vue Router guide pages on navigation, waiting for the result of a
> navigation, dynamic routing and named routes (commit `e9fc88b`), read 2026-10-16. Sentences marked "own
> guidance" are ours.

## 1.1 Building a location
1. **`params` are ignored when `path` is given.** `router.push({ path: '/user', params: { username } })` goes to
   `/user`; `query` is not affected by this. To pass params, use the route `name`, or write the whole path
   yourself. `RouterLink`'s `to` follows the same rules as `push`.
2. **Prefer a name and params, so the router encodes them.** With a manual string or a `path` object you must
   provide an encoded path: apply `encodeURIComponent` to each dynamic segment (it also encodes the `/`). The
   page's example turns `eduardo/san martin` into `eduardo%2Fsan%20martin`. Own guidance: a path assembled from
   user text without encoding is the usual way a segment turns into extra path levels.
3. **Param values are strings or numbers, or arrays of them for repeatable params.** Any other type is
   stringified automatically, so an object or a boolean arrives as text. For an optional param, an empty string
   or `null` removes it.
4. **Named routes avoid URL typos**, in the page's words; a rename then breaks in one place (part 4.4 makes the
   compiler check it).

## 1.2 A navigation is a promise, and it can fail
1. **`push` and `replace` are asynchronous.** Code written on the next line runs before the navigation is done:
   a menu closed there closes at once. Await the returned promise.
2. **A prevented navigation shows up in the resolved value.** The promise resolves to a navigation failure
   when the navigation was prevented, and to a falsy value (usually `undefined`) otherwise; the page does not
   say what a thrown error does to the promise, so do not assume it. The page lists the
   situations that leave the user where they were: already on the target, a guard returned `false`, a newer
   navigation started while a guard was still running, a guard redirected elsewhere, a guard threw.
3. **Test the result before acting:**

```ts
const failure = await router.push({ name: 'profile' })
if (!failure) {
  menuOpen.value = false
}
```

4. **Tell the kinds apart with `isNavigationFailure` and `NavigationFailureType`.** There are three:
   `aborted` (a guard returned `false`), `cancelled` (a new navigation began before this one finished) and
   `duplicated` (already at the target). Called without the type, `isNavigationFailure(value)` only answers
   "is it a failure". A failure carries `to` and `from`, both normalised locations.
5. **A redirect is not a failure.** A guard returning a new location creates a new navigation, so the promise
   comes back falsy. Detect it with `router.currentRoute.value.redirectedFrom`.
6. **Watch failures globally** with the third argument of `router.afterEach((to, from, failure) => ...)`, for
   example for analytics. Do not send a page view when `failure` is set.

## 1.3 Routes added at runtime
1. **`addRoute` and `removeRoute` only register routes.** If the new route matches the page you are on, the
   page does not change until you navigate again; the page's fix is `router.replace(router.currentRoute.value
   .fullPath)`, which can be awaited.
2. **Inside a guard, do not call `replace`: return the location** to trigger a redirection, and make sure the
   new route matches and that the check that adds it is false the second time, or the redirect never ends.
3. **Names are unique across all routes.** Adding a route whose name already exists removes the first one. The
   function `addRoute` returns removes that route; removing a route removes its aliases and children.
4. **Nested routes are added by naming the parent as the first argument** of `addRoute`.

## 1.4 Verify
Navigate with a name and a param containing a slash and read the resulting URL; push to the current location
and read a `duplicated` failure; push to a route whose guard returns `false` and read `aborted`; and run the
code that follows a navigation for each of those three results, to see which of them closed the menu.
