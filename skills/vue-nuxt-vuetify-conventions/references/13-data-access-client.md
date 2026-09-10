# vue-nuxt-vuetify-conventions §13 — The data-access client

> Section 13 of `skills/vue-nuxt-vuetify-conventions`. Read it when the front end talks to the backend and the
> project ships a typed client for it. The other sections and the guardrails stay in `SKILL.md`.

Conditional like §8: it applies where the project has a **typed client over its REST API** — an
active-record-style model layer, a generated SDK, a query-builder wrapper. Where there is none, only point 6
holds and the rest is not a gap to fill by hand.

1. **Where a model exists for the resource, every call to it goes through the model** — never a raw
   `$fetch`/`useFetch`/`axios` call to the same endpoint next to it. Two access paths to one resource
   means the URL, the field list and the pagination limit are declared twice and drift once.
2. **Never hand-build the query payload the client generates.** A REST package with a search envelope
   (`lomkit/laravel-rest-api` and its `{ filters, includes, scopes }` shape is the case in reach here)
   exposes a builder precisely because the envelope is easy to get subtly wrong, and hand-writing it also
   throws away the typing. If a resource has no model yet, declare one before writing the call rather
   than after the second copy.
3. **Don't carry another ORM's surface over by muscle memory.** A client that reads like Eloquent or
   Prisma is not that ORM: a method that doesn't exist is a runtime error, and one that exists with
   different semantics (an eager-load helper that filters instead of includes) is worse, because it
   returns something. Read the client's own API for find-by-key, eager loading and relation filtering.
4. **A list is not the same type on both sides of hydration.** A client that wraps collections typically
   returns a plain array during SSR and its own list object once hydrated, so a ref holding one is typed
   for both. Typed as the array alone it type-checks on the server and breaks in the browser — the
   failure that only shows up after a real page load, never in the editor.
5. **Two handles on the same record are one record.** Where the client caches by identity, a field
   assignment is local dirty state on that handle until it is persisted; other components holding the
   record keep seeing the last applied values. Persist through the client's save path. A local-apply
   escape hatch, where one exists, advances the shared copy without a round trip — reach for it only with
   a stated reason, never as a cheaper save. Don't hand-patch a list after a delete either: a
   self-filtering collection already dropped the row, and a manual `splice` on top removes a second one.
6. **A response is untrusted input, whatever produced it.** Validate at the boundary, and never render a
   client object straight into the template (`{{ instance }}`): a non-serialisable handle either prints
   internals or breaks hydration, and the field you meant is the one to interpolate.
7. **The page size lives with the model, not at the call site.** When each screen passes its own limit,
   the API's real cap is nobody's knowledge: one list shows 15 rows, another asks for 500 and gets 100
   without saying so, and an export silently truncates (§12.13). Declare the default on the resource and
   override it where there is a reason.
8. **A model method is a request, not a cache.** Two components each asking the model for the same list
   issue two calls unless something deduplicates them — the client's own caching, or the composable that
   owns the fetch (§2.10). Assuming the client caches because it looks like an ORM is how a page makes
   eleven identical requests and nobody notices until the network tab is open.
9. **Extend the client with a wrapper, never by patching its prototype.** A method added onto the
   vendor's class works until the version that ships a method of the same name, and then the collision is
   silent: one of the two wins depending on load order. Wrapping keeps the house behaviour attributable
   and upgradable (§8.7 is the same rule for a generated component).
10. **Catch the client's own error type, not a generic `Error`.** The validation details the API returned
    — which field, which rule — are on the typed error, and they are exactly what the form has to display
    (§12.4). A `catch (e)` that only reads `e.message` throws away the per-field information and leaves
    the UI saying "an error occurred" beside a form the user cannot fix.
11. **An absent field is not a null field.** With sparse fieldsets or a partial include, a property the
    request did not ask for is simply missing, and treating it as "no value" writes an emptiness the user
    never entered — dangerous on a save, since a payload built from a partially loaded record can blank
    columns it never fetched. Distinguish "not requested" from "requested and empty", and never persist a
    record the current view only partially loaded.
12. **The server authorises an include, not the client.** A relation the builder is willing to request is
    not a relation this user may read; if it comes back, that is the server's decision, and if it comes
    back when it should not, the bug is in the backend's authorisation rather than in the query. Don't
    design a screen around a nested include being available until the API has actually returned it for a
    non-privileged account.

13. **A call the user can re-trigger needs a cancellation path.** A search-as-you-type or a fast tab switch
    fires a new request before the previous one resolves; without an `AbortController` per call (aborting
    the prior one before issuing the next), the responses can land out of order and the slower, stale one
    overwrites the fresher result on screen. One controller can also cover several calls that must cancel
    together — a single `abort()` stops all of them, which is cheaper than tracking each request's own flag.
14. **A non-idempotent call (create, most updates) is not safe to retry blindly.** A network timeout after
    the server already processed the request, followed by an automatic retry, can create the record twice
    or apply the update twice; a client-generated idempotency key the server deduplicates on, or a retry
    limited to genuinely idempotent calls (a plain `GET`, a `PUT` that replaces rather than increments), is
    what makes a retry safe rather than a second side effect.
15. **A mutation invalidates what it changed, not the whole cache.** Deleting a record and leaving three
    other components holding the stale list is the same failure as §13.5 for a single record, scaled to a
    collection: the model's own cache/refetch hook (or the composable that owns the fetch, §2.10) has to be
    told which resource changed, rather than the caller assuming every reader will eventually refetch on its
    own.
16. **Cursor-based pagination and offset-based pagination answer different questions, and swapping one for
    the other mid-project changes correctness, not just the URL shape.** An offset drifts under concurrent
    inserts/deletes — page 2 can repeat or skip a row that moved past the boundary between two requests — a
    cursor tied to a stable, unique, ordered field does not. Read which one the client's builder actually
    issues before assuming "page 2" means the same list twice.
17. **A file upload through the typed client is still a `multipart/form-data` request underneath**, and the
    model's usual JSON-shaped call is often the wrong method for it — check whether the client exposes a
    dedicated upload path before hand-rolling a `FormData` alongside a model that expects one. Progress
    reporting, if the screen shows it, comes from the transport layer the client wraps, not from the model.
18. **A `PATCH` and a `PUT` through the model are not interchangeable even when the client accepts either.**
    A partial-update method that sends only the changed fields and a replace method that sends the whole
    record diverge the moment a field the current view never loaded (point 11) is part of the payload: the
    replace form blanks it, the partial form leaves it untouched. Which one the model's "update" call
    actually issues is worth confirming once per resource rather than assumed from the method's name.
19. **A version or `updatedAt` field the client exposes on a record is there for optimistic-concurrency
    checks, not display filler.** Sending it back on save lets the server reject a write against data the
    user never saw (someone else changed the record in between) instead of silently overwriting their
    change; dropping the field from the payload because "the form doesn't show it" throws away the one
    signal that would have caught the conflict.

## Where the org catalogue governs
A house client is the authority on its own API surface, its decorators and its config. This section is the
generic shape of the rule — go through the model, don't rebuild its payload, type for both sides of
hydration — so the rules survive on a project with no such package, and so an agent recognises a house
override as an override.
