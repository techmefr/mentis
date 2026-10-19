# laravel-conventions §2 — Authorisation

> Section 2 of `skills/laravel-conventions`. Read it when an endpoint, a policy or a permission check. The other sections and the guardrails stay in `SKILL.md`.

1. **Never check a role name in code** — no `hasRole('admin')`, no `@role('manager')`. Check a **permission**
   (`can()`, a policy method, a gate). A role is a bundle of permissions that changes with the business; a
   role name in code is a deploy every time it does. The tell is a conditional naming a job title: ask what the caller may *do*. A check on one
   specific principal — a system account, a support impersonation — is an attribute of the account, not a
   role, and reads better as one.
2. **Permissions are access rights only**: who may create/update/delete, and which parts of the app they
   reach. A permission must never stand in for what a user *is* or for a business capability — that's a
   domain attribute. Reusing the permission system as a feature flag makes the access model unauditable.
   The separating question is *"would revoking this be a security decision or a product decision?"* — a
   product decision belongs in a feature flag or a plan attribute, and once the two share a table nobody
   can answer "who can see this data" from the permission list alone.
3. Authorisation is declared where the entry point is (policy on the resource, check on the action), not
   assumed from the caller being authenticated. Authenticated means *we know who this is*; authorised
   means *this one may do this to this record*. Conflating them is the commonest way a multi-tenant
   endpoint leaks: the route is behind the auth middleware, the handler loads by id, and nothing compares
   the record's owner to the caller.
4. **An id in the request is an untrusted claim, and the fix is scoping the query, not checking after the
   fetch.** `Model::findOrFail($id)` followed by an ownership check is one forgotten `if` away from an
   IDOR, and tells the caller the record exists before deciding they may see it. Load through the
   relationship the caller actually has — the tenant, the owner, the team — so a record outside their scope
   is a 404 by construction. Route binding does not do this: it resolves an id to a model and holds no
   opinion about who asked.
5. **The list endpoint and the detail endpoint have to agree, and so do the aggregates beside them.** A
   filtered index with an unscoped `show`, or a scoped table beside summary cards computed over everything,
   are the same defect: the scope was applied at one call site instead of being a property of the
   query. Prefer one scoping mechanism the model owns, so a new endpoint inherits it — and treat any
   count, sum or chart next to a scoped list as part of its contract: a total the user cannot reconcile
   with the rows reads as a bug.
6. **Authorise the write on the fields, not only on the route.** A caller allowed to update a record is not
   automatically allowed to change every column — a status, an owner, a price, a tenant key are each
   their own decision. Mass assignment plus a route-level permission turns a self-service profile update
   into a privilege escalation. Where a field is only writable by some callers, the request object says so;
   the model's fillable list is not an authorisation mechanism.
7. **A policy is not a validation layer, and validation is not authorisation.** *May this caller act on
   this record* is a policy; *is this payload well-formed and consistent* is validation (§6). Mixing them
   produces a 422 where the honest answer is 403 and the payload should never have been read, and a 403
   for a malformed request any caller would have failed.
8. **Read authorisation is authorisation.** Checks tend to land on mutations because the damage feels
   concrete, leaving exports, search, relation includes and notifications to inherit whatever the base
   query was. Those are where a scope gap becomes a bulk disclosure — a report is a leak with a filename.
   Anything that can return another tenant's rows gets the same treatment as a write.
9. **Carve-outs, stated so they are not invented.** A genuinely public endpoint is a decision, written as
   one where the route is declared. A console command has no caller and therefore no policy — its
   authorisation is *who can deploy and run it*, an infrastructure question, so it must not grow a
   `Gate::forUser()` that pretends otherwise. A first-party service-to-service call authenticates as a
   principal with its own narrow permission set, never by skipping the check because the caller is "ours".
10. **A policy method can return `Response::deny($message)` instead of `false`, and the message is the
    difference between a 403 the reader can act on and one they cannot.** "You may not edit this invoice"
    and "invoices are locked once paid" are both denials, but only the second says what would need to be
    true — otherwise every refusal reads the same and the support ticket asks what they did wrong. It stays
    a policy decision (point 7): the message explains *why this caller may not*, never *what is wrong with
    the payload*.
11. **A super-admin bypass is declared once, in `Gate::before()`, never sprinkled as an extra clause in
    every policy method.** `Gate::before` runs ahead of every ability check and can short-circuit the whole
    decision — the shape "this one principal passes everything" needs. An
    `if ($user->isSuperAdmin()) return true;` line copy-pasted into each policy is point 1's mistake in a
    different hat, and silently stops working the day someone adds a policy and forgets it. The bypass only
    reaches checks that go through the Gate — a hand-built query that never calls `can()` gets neither
    bypass nor denial, a reason to route reads through the same gate, not to trust the bypass blindly.
12. **A token's abilities are a second, narrower permission layer under the user's own — a token can only
    do less than its owner, never more.** A Sanctum token scoped to `['orders:read']` for a third-party
    integration means every request on it is checked twice: can this *user* do this, and does this *token*
    claim the ability. Skipping the second check turns a scoped API key into a full session token the moment it leaks.
13. **An authorisation denial is a contract worth a test, the same as the success path.** A test that only
    asserts the owner can update the record, and never that someone else gets a 403, leaves point 4's
    scoping unverified — the `findOrFail` comes back and nothing fails until a real other-tenant request
    does. Assert the status code and, where point 10 applies, the message: a 403 that silently became a 200
    after a refactor is the regression this rule catches.
14. **Policy discovery follows a naming convention, and a policy that breaks it is invisible.** Laravel
    resolves `OrderPolicy` for `Order` automatically; a policy named otherwise, or a model outside the
    conventional model namespace, needs an explicit registration in the `AuthServiceProvider`'s policy map
    or the framework never finds it. The failure looks like the check working — `can()` returns false for
    everyone — and only a deliberately-permitted test case failing surfaces it (point 13).
15. **`Gate::after()` can only widen a result the check itself left open, never overrule one already
    settled.** A closure registered with `after` runs once every ability check has run, but its return value
    is used only when the check resolved to `null` — a policy method that returned `true` or `false`
    keeps that result whatever `after` says. It suits auditing every decision in one place; as a late veto it silently never fires once a
    policy method returns an explicit boolean instead of abstaining. [Laravel authorization docs,
    laravel.com/docs/12.x/authorization, read 2026-09-10.]
16. **`authorizeResource()` wires a whole resource controller to its policy in one line, and the mapping it
    assumes is exactly point 1's action-to-permission list.** `index`/`show`/`store`/`update`/`destroy` each
    resolve to the policy method of the same name, with the model resolved from the route for every method
    except `index`/`store`, which check the policy's class-level ability. A custom action added to the
    controller does not fail loudly: it runs unauthorised, because `authorizeResource()` only wires the
    conventional seven. [Laravel authorization docs, laravel.com/docs/12.x/authorization, read 2026-09-10.]
17. **A policy's own `before()` method is point 11's bypass shape, scoped to one model instead of every
    ability.** Defined *on the policy itself* — distinct from `Gate::before()` in point 11 — it runs ahead of
    every method on that policy and can short-circuit it the same way. `Gate::before()` is for a principal who passes everything, a policy's `before()` for a rule on every
    action on one model (an archived record nobody may mutate). A policy `before()` re-checking "is this
    the super-admin" is point 11's mistake one file over. [Laravel
    authorization docs, laravel.com/docs/12.x/authorization, read 2026-09-10.]
18. **A ternary permission check still has to name the record, or the "fallback" branch quietly becomes the
    loosest rule in the app.** Guest access, a public preview, a degraded mode for a suspended account — each
    is a real authorisation state, not the absence of one, and belongs as its own named ability
    (`view-preview`, `view-limited`) with its own policy method rather than an inline `$user ? $user->can(...)
    : true` at the call site, which is invisible to point 13's tests because nothing forces a test to
    enumerate every caller state the ternary handles.
19. **A middleware-level `can:` check and a controller-level `$this->authorize()` are the same rule expressed
    twice only for as long as someone keeps them in sync.** `Route::get(...)->middleware('can:update,post')`
    checks the same ability the controller would call — pick one place per route and delete the other, so
    a refactor loosening the middleware doesn't leave a controller check nobody re-verifies.
20. **A form's own conditional rendering is not authorisation, and cannot substitute for the server check.**
    A button hidden from a caller lacking the permission is a UX courtesy; the endpoint still needs the
    `can()` or policy check point 3 requires, because a caller can reach the route without the button —
    a gap nobody who only tested through the UI could hit.
21. **A permission's own removal or rename is a data migration, not a code change alone.** Deleting a
    permission a role still references leaves that role — and every user holding it — silently able to
    do less the next time its cached abilities are rebuilt, and renaming one without migrating the
    pivot rows detaches every holder at once. Both are the schema-migration problem
    `skills/laravel-conventions` §3 point 1 describes for an enum value, applied to the permission table.
22. **A broadcast channel's authorisation lives in `routes/channels.php`, and it is its own surface — not
    inherited from the HTTP route that renders the page listening on it.** `Broadcast::channel('orders.{order}', ...)`
    runs its own closure against the connecting user, so a private channel left unauthorised (or
    authorised by presence alone, ignoring the model) leaks every event on it to anyone who can guess the
    channel name, however tightly the HTTP endpoints around the same data are scoped. Point 8 applies here
    in real time instead of per request.
23. **A `FormRequest::authorize()` left returning `true` is not a placeholder, it is the one authorisation
    hook the framework calls before validation runs, disabled.** The scaffolding generates it that way, and
    the gap shows only when someone who should have been refused isn't. `authorize()` is the policy check that belongs on the
    request (point 7), and a permanently-true return is the same as never having asked.
24. **A policy method's extra parameters compare against a second model, not just the acting user and the
    target resource.** `update(User $user, Invoice $invoice, LineItem $lineItem)` lets the check confirm
    the line item belongs to that invoice — checking only `$user`/`$invoice` passes a caller who owns the
    invoice but edits a line item borrowed from someone else's, point 4's IDOR one join deeper.
25. **A notification's `via()` channel does not carry its own authorisation — the notifiable resolved for
    it has to be the same one the caller was already checked against.** Queuing a notification onto a user
    id read from the request, rather than the model already scoped and authorised earlier in the request
    (point 4), reopens the gap in a background job where nothing renders a 403: the job quietly notifies
    the wrong account.
26. **`$request->user()->cannot()` outside a controller does not throw on its own — it returns a boolean,
    and the caller has to act on it.** Inside a controller, `$this->authorize()` throws an
    `AuthorizationException` the handler turns into a 403; from a command, a job or a console script there
    is no HTTP response to fall back on, so skipping the explicit `throw_unless()` / manual throw around a
    bare `cannot()` lets an unauthorised action inside a queued job proceed — the async equivalent of §11
    point 1's "throw, never return."
27. **A policy method written only for an authenticated user silently denies every guest, which reads as a
    strict app rather than the intended behaviour for a genuinely public ability.** Typing the user
    parameter as nullable (`viewAny(?User $user)`) and returning `true` for the guest case is how
    `Gate::authorize()` and `@can` correctly allow anonymous access to a public listing — a method that
    doesn't accept null falls through to a blanket denial that looks identical to a restricted ability.
28. **Implicit route-model binding does not scope a nested resource to its parent on its own — `scopeBindings()`
    is the mechanism, not a side effect of nesting the routes.** `Route::resource('teams.projects', ...)`
    resolves `{project}` by its own primary key whichever `{team}` is in the URL, so a caller swapping the
    team segment for one they don't belong to still resolves a real project unless the group is wrapped in
    `->scopeBindings()`, which constrains the child's resolution to a relationship on the parent. Without
    it, this is point 4's IDOR hiding in routing configuration. [Laravel routing documentation,
    laravel.com/docs/12.x/routing, read 2026-09-10.]
29. **`Gate::authorize()` — the standalone facade call, not `$this->authorize()` on a controller — throws the
    same `AuthorizationException` from anywhere the container can be reached, which is what point 26 needs
    for a console command or a job with no controller to inherit the helper from.** A bare `cannot()` plus
    a hand-rolled `throw` duplicates it; `Gate::authorize()` gives a job or Artisan command the same
    fail-loud contract a controller gets. [Laravel authorization
    documentation, laravel.com/docs/12.x/authorization, read 2026-09-10.]
30. **`Gate::inspect()` returns the full `Response` object instead of a boolean, the only way to surface
    point 10's denial message outside a controller's automatic exception handling.** A Blade component, an
    API resource deciding whether to include a field, or a notification building its own payload need the
    *reason* a check failed; `can()`/`cannot()` collapse it, so a UI showing "invoices are locked once paid"
    next to a disabled button calls `inspect()`. [Laravel authorization documentation,
    laravel.com/docs/12.x/authorization, read 2026-09-10.]
31. **A password-confirmation requirement is a separate authorisation-adjacent gate from the permission
    check itself, and it belongs on the route, not folded into the policy.** The `password.confirm` middleware
    re-verifies the caller before a sensitive action (changing an email, revoking every session) runs — a
    policy answering "may this user do this" cannot also answer "did this session prove it recently," and
    stuffing a session-freshness check into a policy conflates two questions, as point 7 forbids for
    validation. [Laravel authentication documentation, laravel.com/docs/12.x/authentication, read
    2026-09-10.]
32. **Batch-checking several abilities at once (`Gate::any()`/`Gate::none()`, or `@canany` in a Blade view)
    is a single decision about "may this caller do at least one of these," not a shortcut for looping over
    `can()` and stopping at the first pass.** A hand-rolled loop reintroduces the risk of an enumeration hidden in control flow; the batch helper's argument list is the enumeration, so
    a missing ability is visible at the call site. [Laravel authorization
    documentation, laravel.com/docs/12.x/authorization, read 2026-09-10.]
33. **A Sanctum token's `currentAccessToken()` returns `null` for a request authenticated through the web
    guard (a normal logged-in session), not only for an unauthenticated one — code that calls `tokenCan()`
    unconditionally assumes every authenticated request carries a token.** Point 12 treats a token's
    abilities as a narrower layer under the user's own; a policy or middleware written only against the API
    guard and reused for a route also reachable through the session guard must check for a null token
    before asking what it can do, or it throws on a first-party browser session never issued a scoped
    token. [Laravel Sanctum documentation, laravel.com/docs/12.x/sanctum, read 2026-09-10.]
