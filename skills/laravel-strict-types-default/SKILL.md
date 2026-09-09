---
name: laravel-strict-types-default
description: "Use when creating a new Laravel file and deciding whether to add declare(strict_types=1): default to omitting it, matching artisan make:* — never retrofit an existing file's declaration either way."
---

# laravel-strict-types-default

Narrow trigger extracted from `skills/laravel-conventions` §5.12, so a new file's `strict_types`
declaration routes here directly instead of only through the whole Laravel block.

## When
Creating a new PHP file in a Laravel project and deciding whether to open it with
`declare(strict_types=1)`.

## Steps
1. **The default for a new Laravel file is to omit `declare(strict_types=1)`**, matching what
   `artisan make:*` generates — this overrides `php-patterns`' language-level default precisely at
   this framework's boundary, where request/route/config values cross as loose scalars on purpose.
2. **This is a project-wide decision applied uniformly**, with the framework's own scaffolding as the
   reference point — a codebase half strict and half not gets the downsides of both.
3. **Leave an existing file's declaration exactly as it is either way.** This is a default for new
   files, not a retrofit — don't add or remove the declaration on a file you're editing for an
   unrelated reason.

## Output / checkpoint
A new Laravel file matches whatever `artisan make:*` would generate for that file kind (no
`declare(strict_types=1)` by default); no existing file's declaration is touched as a side effect of
an unrelated change.

## Guardrails
- If the project has explicitly decided otherwise (documented, applied uniformly), follow that
  decision instead — this rule is the default absent such a decision, not an override of one.
- `php-patterns` §1.1 states the opposite default at the plain-PHP level; this rule is specifically
  the Laravel-framework-boundary exception to it, not a contradiction to resolve.

## Origin
No external source: this is `skills/laravel-conventions` §5.12 extracted to its own trigger. Written
2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
