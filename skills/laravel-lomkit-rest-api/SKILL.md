---
name: laravel-lomkit-rest-api
description: "Use when a Laravel project exposes models through lomkit/laravel-rest-api (Resources, Controllers, Rest::resource routes, actions, instructions, search and mutate payloads): what the package whitelists, how its authorisation layers work, and the mistakes that bypass them. Not for Inertia pages or plain controllers."
---

# laravel-lomkit-rest-api

Step 6 of the pipeline (`WORKFLOW.md`). The package turns a declared Resource into a small fixed set of
endpoints. Its safety comes entirely from **declaration**: what is not declared is refused. Most defects in
this stack are code that steps around that declaration. Sits under `skills/laravel-conventions` §6 (HTTP
surface), which prefers the package's filters over hand-built endpoints; it does not apply to an Inertia
project (`skills/inertia-conventions` §4).

**Special status.** New block, 🟡: written from the guidance the package itself ships, never run on real work
in house. Requirements at the reading: PHP 8.2+, Laravel 12 or 13. Method and config names are version facts;
re-read the package documentation for the pinned version (`skills/source-freshness`).

## When
A file under the app's REST resources or controllers directory, a `Rest::resource(...)` line, a `Lomkit\Rest`
import, or a client payload with `search`, `mutate`, `filters`, `includes`, `gates` or `instructions`.

## Steps
1. **Extend, do not parallel.** For a model the package already exposes, add a Resource field, an action or
   an instruction. Do not add a plain resource route for the same model: the two authorisation paths drift.
   A project without the package is not pushed toward it; recommend it only where rich filtering, batch
   mutation or schema introspection clearly fit, and name the dependency without installing it.
2. **Whitelist by declaration.** The Resource's `fields`, `relations`, `scopes`, `actions` and `instructions`
   are the whole surface; a new column on the table is not exposed until it is listed. Narrow any list per
   request or per permission through the request argument every method receives. Relations use the package's
   own relation classes pointing at a **Resource**, never the Eloquent relation classes or a model.
3. **Baseline constraints live in the base resource's query hooks** (search, mutate, destroy, restore,
   force-delete queries): tenant scoping and visibility are set there once. A change that touches those hooks
   preserves what they already apply (`skills/laravel-tenant-context-by-default`).
4. **Policies are the authority.** Every exposed model needs a policy with `viewAny`, `view`, `create`,
   `update`, `replicate`, `delete`, `restore`, `forceDelete`, and `attach{Model}` / `detach{Model}` for each
   many-to-many relation that may be mutated; a missing method blocks the operation. Never switch the
   authorisation flag off to unblock a test: write the policy (`skills/laravel-permissions-not-roles`).
   Authorisation results are cached per user and resource for a few minutes by default, so a policy change
   looks ineffective until the cache is disabled or expires; check that before debugging the policy.
5. **Gates are a client convenience, not enforcement.** The client may ask the server to evaluate listed
   abilities per row and embed the result. The server still enforces on the real call.
6. **Mutation is batched but all-or-nothing on authorisation.** One denied item fails the whole batch. A
   response lists affected ids, not models: re-query for the record. Through-relations can be read, never
   mutated; chain through the intermediate relation. Constrain relation writes with the required and
   prohibited-on-create/update helpers rather than ad hoc validation.
7. **Actions for writes, instructions for reads.** Do not write a custom controller method for a use case
   the package models. An action declares how it is targeted: standalone (no models), classic (whatever the
   search resolves, **every model if search is omitted**), or targeted (explicit ids, required, capped, ids the
   caller cannot see are skipped). Give a destructive or bulk action the targeted form so omitting the
   argument is a validation error, not a mass update, and lower the id cap when the blast radius should be
   smaller. Standalone and targeted are mutually exclusive and combining them throws. An action's field
   payload is a list of name and value pairs, not an object. A queued action dispatches one job per chunk.
8. **Includes are not nested.** An include takes filters, sorts, scopes, limit and selects but not another
   include; go deeper with one include per level and register the chained relation on the intermediate
   resource. An include alias must be an identifier, unique, and not collide with a field, relation or the
   gates key.
9. **A custom response class can undo the whitelist.** Mapping from the model directly bypasses field
   shaping and authorisation. Use it only to reshape output, reading through the same allowed fields.
10. **Soft-delete routes are opt-in at the route** even when the model uses soft deletes.
11. **Every request is JSON.** The package refuses a request without the JSON accept header. Live form
    validation uses the precognition header when enabled in configuration (`skills/laravel-precognitive-request-scoping`).
12. **Document with the existing path.** The package integrates with an OpenAPI generator extension; the
    built-in Swagger path is being superseded, so no new customisation there for new work.

## Output / checkpoint
No exposed model without a full policy, no route for a package-managed model outside `Rest::resource`, no
bulk action that can run unscoped, and no field exposed that is not listed on purpose. Checked at `gate` (7)
and `review` (8).

## Guardrails
No comments in the code produced. New and changed code only (`skills/code-baseline` §0). A genuine defect in
the package goes to its tracker with a reproduction, not into an app-local shim
(`skills/code-baseline` §7 on customising a third party).

## Origin
Rewritten from the `laravel-rest-api` skill file shipped inside `lomkit/laravel-rest-api` itself (MIT,
cloned 2026-10-02, repository head dated 2026-08-17; package requirements from its `composer.json`):
declaration whitelist, hook layers, policy and gate model, action targeting states, include and alias rules,
soft-delete opt-in and the custom-response warning. The documentation site was not re-read: details beyond
that file are unverified. Mechanisms only, rewritten in our words.
