---
name: laravel-permissions-not-roles
description: "Use when an authorisation check names a role (hasRole/@role) or is written on a fresh permission: never check a role name in code — check a permission (can(), a policy method, a gate)."
---

# laravel-permissions-not-roles

Narrow trigger extracted from `skills/laravel-conventions` §2.1–§2.2, so a role-name check routes
here directly instead of only through the whole Laravel block.

## When
Writing or reviewing an authorisation check — `hasRole('admin')`, `@role('manager')` in a Blade
directive, a conditional naming a job title — or defining a new permission.

## Steps
1. **Never check a role name in code.** No `hasRole('admin')`, no `@role('manager')`. Check a
   **permission** (`can()`, a policy method, a gate) instead.
2. **A role is a bundle of permissions that changes with the business; a role name in code is a
   deploy every time it does.** A conditional naming a job title is the tell — the code should ask
   what the caller is allowed to *do*, and a job title is never the answer.
3. **A check genuinely depending on one specific principal** (a system account, a support
   impersonation) is not a role either — it is an attribute of the account, and reads better as one.
4. **Permissions are access rights only** — who may create/update/delete, and which parts of the app
   they reach. A permission must never stand in for a business capability or a feature flag: ask
   *"would revoking this be a security decision or a product decision?"* A product decision belongs
   in a feature flag or a plan attribute, never the permission table.

## Output / checkpoint
No authorisation check in the diff names a role directly — every check goes through `can()`, a
policy method, or a gate backed by a permission, and every permission added reads as an access
right, not a capability or a plan tier.

## Guardrails
- Reusing the permission system as a feature flag makes the access model unauditable — the moment
  access rights and product flags share a table, nobody can answer "who can see this data" from the
  permission list alone.
- The declared-at-the-entry-point rule (policy on the resource, not assumed from authentication) is
  `skills/laravel-conventions` §2.3, and the id-scoping rule is `laravel-scope-dont-check-after-fetch`
  — read them for the neighbouring authorisation rules this one sits beside.

## Origin
No external source: this is `skills/laravel-conventions` §2.1–§2.2 extracted to its own trigger.
Written 2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
