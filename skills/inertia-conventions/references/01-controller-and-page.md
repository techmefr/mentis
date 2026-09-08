# § 1 — The controller owns the page, not an API endpoint

> Section 1 of `skills/inertia-conventions`. Read it when a controller action that renders a page is
> written or modified, or when a route for a page is added.

1. **A controller action returns `Inertia::render('Page/Name', [...])`**, not a JSON resource. The
   second argument is exactly the page component's props — there is no separate serialisation layer to
   design, and no REST resource class needed for a page's own data. The response Inertia builds is not a
   JSON document a consumer parses; it is the input to one specific component, and the only contract it
   has to satisfy is that component's own. Designing a resource class on top of it invents a second shape
   to keep in sync with the first, and the two drift in the direction of whichever one the tests cover.
2. **Never build a JSON API endpoint whose only consumer is the page itself.** If a component's data
   comes from `Inertia::render`'s props, adding a `fetch`/`axios` call to a matching API route duplicates
   the same data through two paths that can now disagree. An endpoint is only justified when something
   genuinely needs to poll or be called from outside a full Inertia visit (e.g. a live search-as-you-type
   suggestion list, a webhook). The failure is not the extra code: it is that the two paths apply
   authorization, scoping and formatting separately, so a fix to one leaves the other serving the old
   answer. What the reader sees is a page whose figures change when they refresh.
3. **Routing is Laravel's, entirely.** No client-side router (`vue-router`, `react-router`) — Inertia
   intercepts `<Link>` clicks and `router.visit()` calls and asks Laravel's own router for the next
   page. A route that exists on the frontend but not in `routes/web.php` doesn't exist. A second router
   also means a second definition of what is authorized: the client's route table has no access to the
   policy that guards the page, so it will happily navigate somewhere the server then refuses.
4. **The page component name is a string resolved at runtime, so renaming a page file is a runtime
   break, not a compile error.** Inertia's resolver looks the name up against the pages directory in the
   browser, after the request has already succeeded — the server logs are clean, the response is 200, and
   the reader gets a blank screen or a resolver error in the console. Rename the string and the file in
   the same change, and grep for the old name before finishing: nothing else will tell you.
5. **A mutation ends in a redirect, not in a rendered page.** `POST`/`PUT`/`PATCH`/`DELETE` actions
   finish with `back()` or `to_route(...)`; Inertia follows the redirect and renders the target page. An
   action that returns `Inertia::render` directly from a `POST` renders the right component but leaves
   the browser's URL and history entry on the submitted route, so the reader's next refresh or back
   button re-submits the form or lands somewhere that no longer exists.
6. **A redirect away from a `PUT`, `PATCH` or `DELETE` has to be a 303, not a 302.** On a 302 the browser
   re-issues the *same* method against the redirect target, so a `DELETE` that redirects to the index
   arrives there as a `DELETE` and gets a 405 — the row was deleted, and the reader sees an error page.
   Laravel's Inertia integration converts the status for you when the redirect comes from the normal
   helpers; a hand-built `response()->setStatusCode(302)` does not.
7. **A redirect to an external URL cannot be a normal redirect.** An Inertia visit is an XHR: it follows
   the redirect itself, receives HTML from a site that knows nothing about Inertia, and fails to parse
   it. `Inertia::location($url)` is the form that tells the client to do a real browser navigation. The
   symptom otherwise is a click that appears to do nothing, with a parse error in the console.
8. **Authorize before the props are computed, in the controller.** A prop that is computed and then
   hidden by the component is still in the payload the browser received (§2.6) — the reader can read it
   in devtools. Authorization that lives only in the page's markup protects the layout, not the data.
9. **A page's own state that belongs in a link belongs in the query string, read server-side.** Filters,
   the page number, the sort column: read them from Laravel's request and pass the resolved values back
   as props. Keeping them in client state means a shared or bookmarked URL reproduces the empty page
   rather than the one the sender was looking at, and the back button loses the reader's filtering.
10. **A page route lives in the middleware group that includes `HandleInertiaRequests`.** Outside it, the
    action still returns an Inertia response, but nothing shares data into it and nothing negotiates the
    initial HTML — so a browser hitting that route directly downloads a JSON body or displays it as text.
    The same applies to a page route accidentally declared in the API routes file.
11. **A 404 or 403 raised inside a page action needs a page of its own.** By default the exception
    renders Laravel's own HTML error page, which arrives inside an XHR that Inertia cannot swap in: the
    click does nothing at all, and the reader has no way to tell a missing record from a broken app.
    Either render the error states as Inertia pages, or teach the exception handler to convert them.
12. **One action, one page.** An action that branches to two different component names for two kinds of
    caller is two pages sharing a route: the props each branch needs diverge, the tests have to assert
    both, and the reader's URL no longer says which one they are on. Split the route.
