# vue-router-pitfalls §4 — Scroll behaviour and typed routes

> Part 4 of `skills/vue-router-pitfalls`. Read it when scroll restoration or anchors misbehave, or when route
> names and params should be checked by the compiler. Sourced from the Vue Router guide pages on scroll
> behaviour and typed routes (commit `e9fc88b`), read 2026-10-16. The page on file-based routing was not read.
> Sentences marked "own guidance" are ours.

## 4.1 Writing a `scrollBehavior`
1. **It needs `history.pushState`**, so it does nothing in a browser without it.
2. **Its arguments are `to`, `from` and `savedPosition`.** `savedPosition` exists only for a back or forward
   navigation (a `popstate`). Return it to get the native-like behaviour of restoring where the user was; return
   `{ top: 0 }` for a new navigation:

```ts
scrollBehavior(to, from, savedPosition) {
  if (savedPosition) return savedPosition
  if (to.hash) return { el: to.hash }
  return { top: 0 }
}
```

3. **Returning nothing, a falsy value or an empty object means no scrolling.** Returning `savedPosition` only
   for back and forward and forgetting the default leaves the user at the old offset on a new page.
4. **`el` takes a CSS selector or an element**, and `top` and `left` then become offsets relative to it. The
   scroll-to-anchor case is `{ el: to.hash }`; add `behavior: 'smooth'` where the browser supports it.
5. **Own guidance:** anchor links need the element to exist when the hook runs. If the target renders after
   data arrives, return a promise (part 4.2) and resolve it after the data is in place.

## 4.2 Waiting before scrolling
1. **Return a promise to delay the scroll**, for example until a page transition has ended. The page's
   example resolves after 500 ms; it says tying this to a transition component's events is up to the app.
2. **Own guidance:** a fixed delay is a guess. Resolve the promise from the event that ends the transition or
   the load, not from a timer, and test it with a slow device profile.

## 4.3 Fixed headers and the cost of the hook
1. **A fixed navigation bar can cover an anchor target.** The page says a static offset may not always work and
   that CSS offsets (`scroll-margin`, `scroll-padding`, pseudo-elements) can lead to unexpected behaviour, so it
   computes the offset in the hook: it reads the element's `scroll-margin-top` with `getComputedStyle` and
   returns it as `top`, letting each element define its own offset.
2. **Setting `scrollBehavior` makes the router take over restoration.** It sets `history.scrollRestoration` to
   `manual`, and computing the positions may trigger layout recalculation. To avoid that cost, do not set
   `scrollBehavior`, or set `history.scrollRestoration` back to `auto`, and the browser restores natively.
3. **Choose one owner.** Own guidance: if the app needs no custom behaviour beyond restoring and top-of-page,
   test whether the native restoration is enough before adding the hook.

## 4.4 Typed routes
1. **A route map lets the compiler check names and params.** Router 4.4 and later can be given a map of
   routes: each entry names the route, its path (shown in autocompletion), the params `push` and `RouterLink`
   accept, the normalised params `useRoute` returns, and the union of its child route names. The map is
   attached by augmenting the `vue-router` module with `TypesConfig`.
2. **The raw and the normalised params differ on purpose.** In the page's example a route accepts a string or
   a number for a param but reading it back always gives a string, because it comes from the URL. A repeated
   param is an array of string or number going in and an array of strings coming out.
3. **Child routes include their parents' params.** In the example the edit route repeats the `name` param of
   its parent.
4. **Writing the map by hand is tedious and error-prone**, in the page's words, and it recommends generating
   routes and types with the built-in file-based routing plugin. Own guidance: if the map is handwritten, add
   a test that compares it with the real routes; and verify the setup by navigating to a deliberately wrong
   name and expecting the type check to fail.

## 4.5 Verify
Navigate by back button, by link and to a hash, and compare the scroll position with the function in part 4.1;
load the page with a fixed header and open an anchor link; and compile a push to a name that does not exist.
