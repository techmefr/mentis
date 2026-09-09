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
