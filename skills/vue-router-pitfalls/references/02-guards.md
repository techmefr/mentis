# vue-router-pitfalls §2 — Navigation guards

> Part 2 of `skills/vue-router-pitfalls`. Read it when a guard or a redirect rule is written or misbehaves.
> Sourced from the Vue Router guide page on navigation guards and the page on the Composition API (commit
> `e9fc88b`), read 2026-10-16. Sentences marked "own guidance" are ours.

## 2.1 What a guard may return
1. **Return `false` to cancel**, a route location to redirect, or nothing (also `undefined` or `true`) to let
   the navigation continue to the next guard. Async guards work the same way. Cancelling by `false` resets
   the browser URL to that of the route you came from if the change came from the address bar or the back
   button.
2. **A redirect drops the current navigation and starts a new one** from the same `from`, so every guard runs
   again for the new target. The location may carry options such as `replace: true`.
3. **Throwing an error cancels the navigation** and calls the callbacks registered with `router.onError()`.
4. **A guard that returns a promise delays the navigation**, which stays pending until all guards have
   resolved.

## 2.2 Redirect loops
1. **Every redirect rule needs a condition that stops on its own target.** The page's login example checks
   that the target is not already the login route before redirecting there, and marks the check with a warning
   about infinite redirects.
2. **Runtime routes have the same trap.** A guard that adds a route and redirects to the same full path
   needs a check that is false the second time (part 1.3).
3. **Verify** by navigating, signed out, to the login route itself and to a protected route, and see one hop
   each.

## 2.3 The legacy `next` callback
1. **A third argument `next` is still supported, but it was a common source of mistakes**, and the page says an RFC
   proposed removing it. Return values replace it.
2. **If it is used, call it exactly once on every path.** The page's bad example calls `next({ name: 'Login'
   })` in an `if` and then `next()` unconditionally, so the unauthenticated user triggers both; the fix is an
   `else`. A path through the guard that never calls it leaves the navigation pending: the page says a navigation stays pending until every hook has resolved (re-read 2026-10-20; it does not spell out the `next` case, so this is the consequence, not a quoted rule).
3. **`next` with a callback exists only for `beforeRouteEnter`**, where the component instance does not yet
   exist; the callback receives it after the navigation is confirmed. The other in-component guards already
   have `this`.

## 2.4 Which guard runs when
The full order of a navigation, from the page:
1. `beforeRouteLeave` in the components being left.
2. Global `beforeEach`.
3. `beforeRouteUpdate` in reused components.
4. `beforeEnter` in route records.
5. Async route components are resolved.
6. `beforeRouteEnter` in the components being entered.
7. Global `beforeResolve`.
8. The navigation is confirmed.

Points that follow from it:
1. **`beforeEnter` runs only when entering from a different route.** It does not run when only the `params`,
   `query` or `hash` change, for example `/users/2` to `/users/3`, or one hash to another on the same path.
   Own guidance: a rule that must hold for every id, such as a per-resource permission check, belongs in a
   global guard, in `beforeEnter` plus `beforeRouteUpdate`, or at the data call.
2. **On a parent route, `beforeEnter` does not run between its children**, because the parent is not entered
   again. Put it on the child routes if it must run there.
3. **`beforeEnter` takes an array**, which is useful for sharing small guards between routes.
4. **`beforeResolve` runs after the async components and the in-component guards**, just before confirming.
   The page names it the ideal place to fetch data or do anything you want to avoid when the user cannot
   enter the page, for example asking for a permission that a route's `meta` flag requires.
5. **`afterEach` cannot change the navigation.** It suits analytics, the document title and announcing a page
   change for accessibility, and it receives the failure as a third argument (part 1.2).

## 2.5 Reaching the app from a guard
1. **`inject()` works in a global guard** (from Vue 3.3) for anything given with `app.provide()`, including a
   Pinia store; the page's example reads a store inside `beforeEach`. Own guidance: create the stores the
   guard needs after the app is installed, and test the guard with the same install order.
2. **In components, use the composable forms.** `onBeforeRouteUpdate` and `onBeforeRouteLeave` work in any
   component rendered by `RouterView`, not only the route component itself; they have no `this`.

## 2.6 Leave guards for unsaved work
1. **Cancel the navigation by returning `false`** from `beforeRouteLeave` or `onBeforeRouteLeave` after asking
   the user, so a change of page does not drop an edit.
2. **A cancelled navigation shows as an `aborted` failure** to code that awaited the push (part 1.2): use it to
   keep the form open, not to show an error.

## 2.7 Verify
Write the guard table of the router (which rule, which guard, which navigation it must cover) and test one
navigation of each kind: a different route, a param change on the same route, a hash change, a back-button
move, and a navigation by `RouterLink`.
