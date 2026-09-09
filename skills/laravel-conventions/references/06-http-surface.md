# laravel-conventions §6 — HTTP surface

> Section 6 of `skills/laravel-conventions`. Read it when a route, a controller action, a FormRequest, a response shape. The other sections and the guardrails stay in `SKILL.md`.

**Before applying this section's REST/resource-routing point, or an installed catalogue's stricter
version of it (e.g. a mandatory REST package), check the specific controller** — what it returns, where
it's routed — **not just whether the project depends on that package.** A project can genuinely run
Inertia for its pages and a REST package for a separate real API surface at the same time; the package
being installed doesn't make every 5-verb controller a REST endpoint, and an Inertia page controller
(no separate API, a controller returns a page and its props directly) is exactly the shape this catches
wrong if the check stops at the project level. See `skills/inertia-conventions` §4 before applying this
section wholesale to that architecture.

1. REST routes follow one consistent URI structure across the app, declared through the framework's
   resource routing rather than hand-rolled verb by verb. A URI names resources, not actions — the verb is
   the HTTP method, so a path segment that is a verb (`/users/create-and-notify`) is the signal that an
   action class is being exposed as a route instead of a resource. Nesting stops at one level: past that
   the parent is decoration, and the child is addressable on its own.
2. Standard CRUD on a model is declared through the resource/REST mechanism the project standardises on — a
   hand-rolled CRUD stack for a plain model is five endpoints of avoidable code and a sixth behaviour that
   differs. Reach for a hand-written route when the operation is genuinely not CRUD on a resource, and give
   it a resource-shaped URI anyway.
3. **Refer to routes by name, never by rebuilding the URL.** A named route survives a prefix change, a
   locale segment and a domain move; a concatenated string is found later by grep, in the one template
   nobody grepped.
4. **Route binding resolves, it does not authorise.** Implicit binding turns an id into a model and holds no
   opinion about who asked — §2 point 4 is the other half, and a nested route needs its binding **scoped**
   to the parent, or the child of *another* parent resolves happily from a guessed id.
5. **Validation in a FormRequest**, with each field's rules expressed as an **array** of entries rather than
   a pipe-delimited string: a string breaks the moment a rule contains a delimiter, and an array diffs
   cleanly. One request class per action, not one shared between store and update — the two have different
   required fields, and sharing them is how `required` quietly becomes `sometimes` for both.
6. **Use the validated payload, never the raw request afterwards.** Reading the request again past
   validation bypasses it: the value used is the one that was never checked, and mass-assigning the raw
   input reintroduces every field the rules were there to exclude. This is the failure that leaves no
   trace, because the endpoint works for well-behaved callers.
7. **`nullable`, `sometimes` and an absent key are three different contracts**, and a partial update has to
   say which it means: a field absent from a `PATCH` keeps its value, a field sent as `null` clears it, and
   conflating the two makes "clear this field" impossible to express. Pick per field, deliberately.
8. **A FormRequest's `authorize()` is not the policy.** It is a convenient place to call one, and putting
   the rule itself there hides it from every other caller of the same operation. The policy owns the rule
   (§2); the request delegates to it.
9. **Query parameters are input too.** Filters, sorts, includes and page size arrive as strings from the
   client and get validated like a body — an unvalidated sort column is an information leak at best and an
   error at worst, and an unbounded page size is a denial of service anyone can trigger with a URL. Cap it,
   default it, and validate the filter names against a list the endpoint owns.
10. **Serialise through a resource, not the model.** A model returned directly serialises whatever it
    happens to serialise, so a new column reaches the API the day it is migrated and a hidden one reaches
    it the day someone removes it from `$hidden`. A resource makes the payload a decision, and it is where
    the difference between the internal shape and the published shape lives.
11. **A response carries a status/type and a human-readable message**, not just an HTTP code: the frontend
    has to display something. Keep the envelope identical across endpoints, including the error case —
    a client that has to branch on two shapes will handle one of them wrong.
12. **The status code is part of the contract, and the defaults are not enough.** A creation answers 201
    with the location of the thing created, a delete that returns nothing answers 204, a validation failure
    422, a conflicting state 409. And the authorisation pair is a decision, not an accident: 403 tells the
    caller the record exists, 404 does not (§2 point 4).
13. **Never hand-roll content negotiation.** The framework already decides JSON versus a rendered response
    from the request itself; a controller branching on whether the caller expects JSON is a second
    implementation of that decision, and it drifts — one branch gets the new field. §11 carries the same
    rule for exceptions, which is where it usually starts.
14. **An HTTP API has consumers you do not deploy.** Removing a field, renaming one, or narrowing a type is
    breaking even when every in-repo caller is updated, so it goes through the additive-then-remove path in
    `skills/deprecation-migration` rather than landing in one commit. §10 holds the layer question; this is
    the contract question.
15. **A `POST` may run twice.** Clients retry, users double-click, proxies replay. An endpoint whose second
    execution creates a second row needs either a natural uniqueness constraint in the database or an
    idempotency key the caller supplies — a check-then-insert in PHP loses the race it was written for.
16. User-facing email or in-app messaging is not the controller's job: it goes through a notification, and
    §8 owns why.
17. **`HandlePrecognitiveRequests` runs the same FormRequest the real submission runs, stopped before the
    controller.** Adding it to a route is what makes point 5's rules reusable for as-you-type validation
    without a second endpoint — the trap is a rule that only makes sense once the operation actually runs
    (a uniqueness check against a row the precognitive request itself is about to create) reporting a false
    positive on every keystroke; scope those rules to skip during a precognitive request rather than
    disabling the check.
18. **`Http::pool()` runs independent outbound calls concurrently from one place, not from several
    sequential `Http::get()` calls inside a loop.** It is the outbound-call equivalent of
    `skills/python-conventions` §4.1's `gather`: three sequential 300 ms calls are a near-second response
    that profiles as "the third-party API is slow", and nothing on their side will move it. Failure still
    needs a decision per response — the pool returns one response or exception per call, and treating the
    whole pool as failed because one call did loses the ones that succeeded.
