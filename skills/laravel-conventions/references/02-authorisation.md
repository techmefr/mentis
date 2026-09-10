# laravel-conventions §2 — Authorisation

> Section 2 of `skills/laravel-conventions`. Read it when an endpoint, a policy or a permission check. The other sections and the guardrails stay in `SKILL.md`.

1. **Never check a role name in code** — no `hasRole('admin')`, no `@role('manager')`. Check a **permission**
   (`can()`, a policy method, a gate). A role is a bundle of permissions that changes with the business; a
   role name in code is a deploy every time it does. The tell that this has gone wrong is a conditional
   naming a job title: the code should be asking what the caller is allowed to *do*, and a job title is
   never the answer to that question. Where a check genuinely depends on the caller being one specific
   principal — a system account, a support impersonation — that is not a role either, it is an attribute of
   the account, and it reads better as one.
2. **Permissions are access rights only**: who may create/update/delete, and which parts of the app they
   reach. A permission must never stand in for what a user *is* or for a business capability — that's a
   domain attribute, not an access right. This one is subtle and worth naming: reusing the permission
   system as a feature flag makes the access model unauditable. The question that separates the two is
   *"would revoking this be a security decision or a product decision?"* — a product decision belongs in a
   feature flag or a plan attribute, and the moment the two share a table nobody can answer "who can see
   this data" from the permission list alone.
3. Authorisation is declared where the entry point is (policy on the resource, check on the action), not
   assumed from the fact that the caller was already authenticated. Authenticated means *we know who this
   is*; authorised means *this one may do this to this record*. Conflating them is the single most common
   way a multi-tenant endpoint leaks: the route is behind the auth middleware, the handler loads by id, and
   nothing ever compares the record's owner to the caller.
4. **An id in the request is an untrusted claim, and the fix is scoping the query, not checking after the
   fetch.** `Model::findOrFail($id)` followed by an ownership check is one forgotten `if` away from an
   IDOR, and worse, it tells the caller the record exists before deciding they may see it. Load through the
   relationship the caller actually has — the tenant, the owner, the team — so a record outside their scope
   is a 404 by construction rather than by remembering. Route binding does not do this for you: it resolves
   an id to a model and holds no opinion about who asked.
5. **The list endpoint and the detail endpoint have to agree, and so do the aggregates beside them.** A
   filtered index with an unscoped `show`, or a scoped table beside summary cards computed over everything,
   are the same defect twice: the scope was applied at one call site instead of being a property of the
   query. Prefer a single scoping mechanism the model owns, so a new endpoint inherits it — and treat any
   count, sum or chart next to a scoped list as part of that list's contract, because a total the user
   cannot reconcile with the rows they see reads as a bug even when the rows are right.
6. **Authorise the write on the fields, not only on the route.** A caller allowed to update a record is not
   automatically allowed to change every column on it — a status, an owner, a price, a tenant key are each
   their own decision. Mass assignment plus a route-level permission is how a self-service profile update
   becomes a privilege escalation. Where a field is only writable by some callers, the request object is
   the place that says so, and the model's fillable list is not an authorisation mechanism.
7. **A policy is not a validation layer, and validation is not authorisation.** *May this caller act on
   this record* is a policy; *is this payload well-formed and consistent* is validation (§6). Mixing them
   produces the two failures nobody tests: a 422 where the honest answer is 403 and the payload should
   never have been read, and a 403 for a malformed request that any caller would have failed.
8. **Read authorisation is authorisation.** The checks tend to land on mutations because that is where the
   damage feels concrete, leaving exports, search, relation includes and notifications to inherit whatever
   the base query happened to be. Those are precisely the surfaces where a scope gap turns into a bulk
   disclosure — a report is a leak with a filename. Anything that can return another tenant's rows gets the
   same treatment as a write.
9. **Carve-outs, stated so they are not invented.** A genuinely public endpoint is a decision, written as
   one where the route is declared. A console command has no caller and therefore no policy — its
   authorisation is *who can deploy and run it*, which is an infrastructure question, so it must not grow
   a `Gate::forUser()` that pretends otherwise. And a first-party service-to-service call authenticates as
   a principal with its own narrow permission set, never by skipping the check because the caller is "ours".
10. **A policy method can return `Response::deny($message)` instead of `false`, and the message is the
    difference between a 403 the reader can act on and one they cannot.** "You may not edit this invoice"
    and "invoices are locked once paid" are both denials, but only the second tells the reader what they
    would need to be true instead — without it, every refusal reads the same and the support ticket asks
    what they did wrong. It stays a policy decision, not validation (point 7): the message explains *why
    this caller may not*, never *what is wrong with the payload*.
11. **A super-admin bypass is declared once, in `Gate::before()`, never sprinkled as an extra clause in
    every policy method.** `Gate::before` runs ahead of every ability check and can short-circuit the whole
    decision, which is exactly the shape "this one principal passes everything" needs — the alternative,
    an `if ($user->isSuperAdmin()) return true;` opening line copy-pasted into each policy, is point 1's
    role-name-in-code mistake wearing a different hat, and it silently stops working the day someone adds a
    policy and forgets the line. The bypass only reaches checks that go through the Gate — a query built by
    hand that never calls `can()` gets no bypass and no denial either, which is a reason to route reads
    through the same gate, not a reason to trust the bypass blindly.
12. **A token's abilities are a second, narrower permission layer under the user's own — a token can only
    do less than its owner, never more.** Issuing a Sanctum token scoped to `['orders:read']` for a
    third-party integration means every request on that token is checked twice: can this *user* do this,
    and does this *token* claim the ability to. Skipping the second check because the first already passed
    turns a scoped API key into a full session token the moment it leaks, which defeats the reason to scope
    it in the first place.
13. **An authorisation denial is a contract worth a test, the same as the success path.** A test that only
    asserts the owner can update the record and never asserts that someone else gets a 403 leaves the
    scoping in point 4 unverified — the query changes, the `findOrFail` comes back, and nothing fails until
    a real other-tenant request does. Assert the status code and, where point 10 applies, the message: a
    403 that silently became a 200 after a refactor is the regression this rule exists to catch.
14. **Policy discovery follows a naming convention, and a policy that breaks it is invisible.** Laravel
    resolves `OrderPolicy` for `Order` automatically; a policy named otherwise, or a model living outside the
    conventional model namespace, needs an explicit registration in the `AuthServiceProvider`'s policy map or
    the framework never finds it. The failure mode is a denial that looks like the check works — `can()`
    returns false for everyone, including the caller who should pass — so it reads as a strict app rather
    than a wiring bug, and it takes a deliberately-permitted test case failing to surface it (point 13).
15. **`Gate::after()` can only widen a result the check itself left open, never overrule one already
    settled.** A closure registered with `after` runs once every ability check has run, but its return value
    is only used when the check resolved to `null` — a policy method that already returned `true` or `false`
    keeps that result no matter what `after` says. The pattern this suits is auditing every decision in one
    place after the fact; using it to bolt on a late veto is the bug, because the veto silently never fires
    once a single policy method starts returning an explicit boolean instead of abstaining. [Laravel
    authorization docs, laravel.com/docs/12.x/authorization, read 2026-09-10.]
16. **`authorizeResource()` wires a whole resource controller to its policy in one line, and the mapping it
    assumes is exactly point 1's action-to-permission list.** `index`/`show`/`store`/`update`/`destroy` each
    resolve to the policy method of the same name, with the model resolved from the route for every method
    except `index`/`store`, which check the policy's class-level ability instead of an instance. Adding a
    custom action to the controller does not fail loudly here: the extra method simply runs unauthorised,
    because `authorizeResource()` only ever wires the conventional seven. [Laravel authorization docs,
    laravel.com/docs/12.x/authorization, read 2026-09-10.]
17. **A policy's own `before()` method is point 11's bypass shape, scoped to one model instead of every
    ability.** Defined *on the policy itself* — distinct from `Gate::before()` in point 11 — it runs ahead of
    every method on that one policy and can short-circuit it the same way. The two exist for different blast
    radii: `Gate::before()` for a principal who passes everything, a policy's own `before()` for a rule that
    applies to every action on one model (an archived record nobody may mutate, regardless of which
    mutation). Neither should duplicate the other; a policy `before()` re-checking "is this the super-admin"
    is point 11's mistake moved one file over. [Laravel authorization docs, laravel.com/docs/12.x/authorization,
    read 2026-09-10.]
18. **A ternary permission check still has to name the record, or the "fallback" branch quietly becomes the
    loosest rule in the app.** Guest access, a public preview, a degraded mode for a suspended account — each
    is a real authorisation state, not the absence of one, and it belongs as its own named ability
    (`view-preview`, `view-limited`) with its own policy method rather than an inline `$user ? $user->can(...)
    : true` at the call site. The inline version is invisible to point 13's test suite, because nothing
    forces a test to enumerate every caller state the ternary silently handles.
19. **A middleware-level `can:` check and a controller-level `$this->authorize()` are the same rule expressed
    twice only for as long as someone remembers to keep them in sync.** `Route::get(...)->middleware('can:update,post')`
    checks the same ability the controller would otherwise call — pick one place per route and delete the
    other, so a refactor that loosens the middleware doesn't leave a controller check nobody re-verifies as
    still being the real gate.
20. **A form's own conditional rendering is not authorisation, and cannot substitute for the server check.**
    A button hidden from a caller who lacks the permission is a UX courtesy; the endpoint behind it still
    needs the same `can()` or policy check point 3 already requires, because a caller can reach the route
    without ever seeing the button. Treating the frontend gate as sufficient is how an endpoint ships with no
    server-side check at all — nobody who only tested through the UI could have hit the gap.
21. **A permission's own removal or rename is a data migration, not a code change alone.** Deleting a
    permission that a role still references leaves that role — and every user holding it — silently able to
    do less the next time that role's cached abilities are rebuilt, and renaming one without migrating the
    pivot rows attached to the old name detaches every holder from it at once. Both are the schema-migration
    problem `skills/laravel-conventions` §3 point 1 describes for an enum value, applied to the permission
    table instead of a status column.
22. **A broadcast channel's authorisation lives in `routes/channels.php`, and it is its own surface — not
    inherited from the HTTP route that happens to render the page listening on it.** `Broadcast::channel('orders.{order}', ...)`
    runs its own closure against the connecting user, so a private channel left unauthorised (or
    authorised by presence alone, ignoring the model) leaks every event broadcast on it to anyone who can
    guess the channel name, regardless of how tightly the HTTP endpoints around the same data are scoped.
    Point 8's "read authorisation is authorisation" applies here in real time instead of per request.
23. **A `FormRequest::authorize()` left returning `true` is not a placeholder, it is the one authorisation
    hook the framework calls before validation runs, disabled.** Laravel's request-class scaffolding
    generates it that way, and it is easy to leave in place because the endpoint still works for every
    legitimate caller — the gap only shows up when someone who should have been refused isn't. Point 7's
    "a policy is not a validation layer" cuts the other way here too: `authorize()` is the policy check that
    belongs on the request, and a permanently-true return value is the same as never having asked.
24. **A policy method's extra parameters compare against a second model, not just the acting user and the
    target resource.** `update(User $user, Invoice $invoice, LineItem $lineItem)` lets the check confirm
    the line item actually belongs to that invoice before allowing the edit — omitting the extra parameter
    and checking only `$user`/`$invoice` passes a caller who owns the invoice but is editing a line item
    borrowed from someone else's, which is point 4's IDOR-by-relationship-scoping problem one join deeper.
25. **A notification's `via()` channel does not carry its own authorisation — the notifiable resolved for
    it has to be the same one the caller was already checked against.** Queuing a notification onto a user
    id read from the request, rather than the model already scoped and authorised earlier in the same
    request (point 4), reopens the same gap in a background job where nothing renders a 403 for anyone to
    notice: the job just quietly notifies the wrong account.
26. **`$request->user()->cannot()` outside a controller does not throw on its own — it returns a boolean,
    and the caller has to act on it.** Inside a controller, `$this->authorize()` throws an
    `AuthorizationException` the handler turns into a 403; the same check run from a command, a job or a
    console script has no HTTP response to fall back on, so skipping the explicit `throw_unless()` /
    manual throw around a bare `cannot()` call is how an unauthorised action inside a queued job silently
    proceeds instead of stopping, the async equivalent of §11 point 1's "throw, never return."
27. **A policy method written only for an authenticated user silently denies every guest, which reads as a
    strict app rather than as the intended behaviour for a genuinely public ability.** Typing the user
    parameter as nullable (`viewAny(?User $user)`) and returning `true` for the guest case is how
    `Gate::authorize()` and `@can` correctly allow anonymous access to a public listing — a policy method
    that doesn't accept null and is never resolved for a guest falls through to a blanket denial that looks
    identical to the ability existing but being restricted, not absent.
