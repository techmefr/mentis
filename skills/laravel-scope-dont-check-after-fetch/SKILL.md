---
name: laravel-scope-dont-check-after-fetch
description: "Use when a route resolves an id from the request into a model: never findOrFail then an ownership check, always load through the relationship the caller actually has."
---

# laravel-scope-dont-check-after-fetch

Narrow trigger extracted from `skills/laravel-conventions` §2.4, so an id-in-request endpoint routes
here directly instead of only through the whole Laravel block.

## When
A controller, action or query resolves a model from an id found in the request or the route — even
via route-model-binding — for an authenticated (multi-tenant, owned, or team-scoped) resource.

## Steps
1. **An id in the request is an untrusted claim.** Route binding resolves an id to a model and holds
   no opinion about who asked — it is not an authorisation check.
2. **Scope the query, don't check after the fetch.** `Model::findOrFail($id)` followed by an
   ownership `if` is one forgotten check away from an IDOR, and it also confirms to the caller that
   the record exists before deciding they may see it.
3. **Load through the relationship the caller actually has** — the tenant, the owner, the team — so a
   record outside their scope is a 404 by construction, not by remembering to add a check.
4. **The list endpoint and the detail endpoint have to agree**, and so do any aggregates beside them —
   a scope applied at one call site instead of owned by the query is the same defect surfacing twice.

## Output / checkpoint
Every fetch by id for an authenticated resource goes through a scoped relationship or a single
scoping mechanism the model owns — no route resolves a model and then compares its owner in a
separate `if`.

## Guardrails
- Prefer one scoping mechanism the model owns (a scope, a scoped relation) so a new endpoint inherits
  it automatically, rather than repeating the scope per controller.
- The full authenticated-vs-authorised distinction and why this is the most common multi-tenant leak
  live in `skills/laravel-conventions` §2 — read it before treating this as redundant with a policy.

## Origin
No external source: this is `skills/laravel-conventions` §2.4 extracted to its own trigger. Written
2026-09-09, same pilot as `laravel-no-db-enums`.
