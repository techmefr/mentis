# vue-router-pitfalls §3 — Route components, params and history

> Part 3 of `skills/vue-router-pitfalls`. Read it when a page shows stale data after a param change, route
> components are imported or split, or a deep link or a missing page misbehaves. Sourced from the Vue Router
> guide pages on dynamic matching, the Composition API, lazy loading and history modes (commit `e9fc88b`), read
> 2026-10-16. Sentences marked "own guidance" are ours.

## 3.1 The same component is reused when a param changes
1. **Going from `/users/ann` to `/users/bob` keeps the same component instance.** The router reuses it because
   both locations render the same component. The consequence the page states: some of its lifecycle hooks are
   not called again. Own guidance: a fetch placed in `onMounted` or `created` therefore runs once and the page
   keeps showing the first user.
2. **React to the change instead.** Either watch the param, `watch(() => route.params.id, ...)`, or use
   `onBeforeRouteUpdate`, which can also cancel the navigation:

```ts
onBeforeRouteUpdate(async (to, from) => {
  if (to.params.id !== from.params.id) {
    user.value = await fetchUser(to.params.id as string)
  }
})
```

3. **Check the param actually changed.** The page's Composition API example compares `to.params.id` and
   `from.params.id` because only the query or the hash may have changed.
4. **Own guidance:** load the first value through the same path. A watcher with `immediate: true`, or a
   function called from both the watcher and setup, is a single code path; a fetch in `onMounted` and a second
   one in the watcher is two.

## 3.2 Watch the property, not the route
1. **The route object is reactive, but do not watch all of it.** The page says in most cases you should avoid
   watching the whole object and watch the properties you expect to change: a getter such as
   `() => route.params.id`.
2. **Templates may use `$route` and `$router` directly**, so a component that only reads them in the template
   does not need `useRoute` or `useRouter`.
3. **Own guidance:** a watcher on the whole object fires for a hash change that no code reads, which is the
   usual source of a fetch that runs twice.

## 3.3 Lazy-loaded route components
1. **Use a dynamic import for every route component.** The page says it is generally a good idea to always do
   so. The `component` option takes a function that returns a promise of a component; the router fetches it the
   first time the route is entered and uses the cached version after that. With a bundler such as Vite or
   webpack this gives code splitting without further setup.
2. **Do not use `defineAsyncComponent` as the route component.** The page says the two features are distinct:
   an async component may be used inside a route component, but the route component itself should be the plain
   function.
3. **A functional component as a route component needs a `displayName`**, because the router otherwise cannot
   tell it from a lazy-loading function.
4. **To put several components in one chunk**, name the chunk. Vite: `build.rollupOptions.output.manualChunks`
   with a list of files. Webpack: the same `webpackChunkName` comment in each import.
5. **Own guidance, verify:** a single static `import` of a page component anywhere in the entry graph defeats
   the split for that page. Build the app, open the bundle report and check that each page appears in its own
   chunk and not in the entry chunk.
6. **A lazy route fails when its chunk cannot be fetched** (offline, or a new deploy removed the old file). The
   page does not describe this case; own guidance: make `router.onError` visible during a manual test with the
   network offline, so the failure is a decision and not a blank page.

## 3.4 History mode, the server fallback and the 404 page
1. **`createWebHistory` is the recommended mode and needs a server fallback.** Without it, opening
   `/user/id` directly returns a 404 from the server. Configure the server to answer any path that is not a
   static asset with the app's `index.html`. The page gives examples for Apache, nginx, Node and other hosts.
2. **A fallback hides real 404s from the server.** Every path now returns the app, so add a catch-all route in
   the app to render the not-found page: `{ path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound }`.
   The page's alternative on a Node server is to match the URL with the router on the server and answer 404
   when nothing matches (server-side rendering).
3. **To navigate to the catch-all by name, give it the path as an array.** The page's example splits the
   current path (without its first character, to avoid a target starting with two slashes) and keeps the query
   and hash.
4. **A subfolder deployment needs `base`** on `createWebHistory` and a matching change in the server
   configuration examples, which assume the root.
5. **Hash mode needs no server setup**, because the part after `#` is never sent to the server, but the page
   says it is bad for search engines. Use it only where a server fallback is impossible.
6. **Memory mode (`createMemoryHistory`) does not read the URL and does not start the first navigation.** It is
   for non-browser environments and server rendering; push the initial location yourself after
   `app.use(router)`.

## 3.5 Verify
Navigate between two ids and check the displayed data and the number of fetches; request a deep link and an
unknown path from the server that will host the build and read the status codes and the page; build the
app and read which chunk holds each page.
