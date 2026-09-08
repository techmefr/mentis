# § 2 — Shared data and page props

> Section 2 of `skills/inertia-conventions`. Read it when a prop is added to a page, when something is
> put in `HandleInertiaRequests::share()`, or when a page's payload is made cheaper.

1. **Data every page needs (the authenticated user, flash messages, feature flags) goes through
   `HandleInertiaRequests::share()`**, once, not repeated in every controller's props array. A prop
   duplicated across twenty controllers because nobody centralised it is the tell that it belongs in
   `share()`. The cost of the duplication is not the typing: it is that the twenty copies stop agreeing,
   and the page that got missed shows a stale feature flag or an empty user object.
2. **Props are the page's contract with its controller — type them.** Generate the frontend type from
   the same Laravel Data DTO/resource the controller returns rather than hand-writing a parallel
   interface that can drift from what the backend actually sends. A hand-written interface is a claim
   about the server, checked by nothing: it keeps declaring a field non-nullable for weeks after a
   migration made it nullable, and the reader sees `undefined` rendered where a value should be.
3. **Partial reloads (`only`/`except`) for a page that re-visits itself with unchanged sections** (a
   filtered table re-requesting only the table's data, not the whole page's props again) — cheaper than
   a full prop payload, and the reason to reach for it is a measured or obvious cost, not a default on
   every visit. Reached for by default it becomes the mechanism behind point 8's stale sections.
4. **A prop that's expensive to compute and not needed for the first paint is `Inertia::lazy()`/deferred**
   rather than computed eagerly on every request that touches the page, including ones that never scroll
   to where it's used.
5. **Everything in `share()` is serialised into every page the user can reach.** Sharing a whole model
   ships every column it doesn't hide — not just the ones the layout reads — to every page, including the
   ones where it is never rendered. Share the handful of fields the shared layout actually uses. The
   difference shows up twice: in the size of every response, and in what point 6 makes readable.
6. **The props of the first load are embedded in the HTML document, and every later payload is a plain
   JSON response.** Both are readable by whoever is viewing the page: view-source, devtools, the browser
   cache. A prop is therefore published to that reader whether or not any component renders it — so an
   internal cost, a moderation note, another tenant's row or a soft-deleted record must not be in the
   props at all. Filtering in the component hides it from the layout, not from the reader.
7. **A prop given as a closure is not computed when a partial reload leaves it out; a prop given as an
   already-computed value is computed either way.** A prop written as `$this->expensiveStats()` runs on
   every visit that touches the action, including one that asked only for the table; the same prop
   wrapped in a closure runs only on the requests that actually send it. This is the difference between
   a partial reload that saves work and one that only saves bandwidth.
8. **A partial reload's `only` list is a promise, and a prop left out of it keeps its previous value on
   the client.** Nothing errors: the section simply goes on displaying what it had. So a prop renamed on
   the server, or a new prop the section now depends on, produces a page where one region is stale and
   the rest is current — the hardest symptom to attribute, because a refresh fixes it.
9. **A deferred prop is a third state, next to loaded and empty.** The component renders once before the
   second request arrives, so any code that reads the prop's length, iterates it or destructures it on
   first render crashes on the initial paint. Render the not-yet-here state explicitly; it is the state
   the reader sees most often on a slow connection.
10. **Flash messages are consumed by the request that reads them.** A flash prop shared into every page
    is read once and gone, so a partial reload that leaves the flash prop out (point 8) keeps the old
    toast on screen, and a request whose page never displays it has already spent it. Read the flash
    where it is shown, and clear it on the client when the visit that carried it finishes.
11. **The props are the page's weight.** A page passing a full collection with every relation eagerly
    loaded is a payload the reader downloads on every visit to it, on every device. Pass the fields the
    page renders, paginate what is long, and treat "the query is fast" as a separate question from "the
    response is small" — the two have different fixes.
12. **If the frontend types are generated, generating them belongs in the gate.** A generator that is run
    by hand is a generator that stops being run: the checked-in types then describe the backend as it was
    at the last person's convenience, and type-checking the frontend confirms a stale claim. Either the
    generation runs in CI and the diff is checked, or the types are honestly hand-written and known to be
    a claim (point 2) — the failure mode is a generated file that everybody trusts and nobody regenerates.
13. **A prop the layout cannot render without has to survive partial reloads.** Marking it always-present
    is what makes a partial reload safe for the shared chrome; without it, every `only` list in the app
    has to remember to include the layout's own props, and the one that forgets renders a header with no
    user in it.
14. **A visit replaces the props wholesale, so a component that copied a prop into local state does not
    see the new value.** This is the same mechanism as any props-to-state copy in the underlying
    framework, but it fires on navigation rather than on a parent re-render, which makes it look like
    Inertia lost the update. Derive from the prop, or key the component so it is recreated.
