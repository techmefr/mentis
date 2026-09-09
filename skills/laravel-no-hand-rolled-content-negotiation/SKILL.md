---
name: laravel-no-hand-rolled-content-negotiation
description: "Use when a controller branches on whether the caller expects JSON: never — the framework already decides JSON versus a rendered response from the request itself."
---

# laravel-no-hand-rolled-content-negotiation

Narrow trigger extracted from `skills/laravel-conventions` §6.13, so a controller branching on
expected response format routes here directly instead of only through the whole Laravel block.

## When
Writing or reviewing a controller (or a catch block) that checks `wantsJson()`,
`Accept`/`Content-Type` headers, or any equivalent to decide by hand whether to return JSON or a
rendered view/response.

## Steps
1. **Never hand-roll content negotiation.** The framework already decides JSON versus a rendered
   response from the request itself.
2. **A controller branching on whether the caller expects JSON is a second implementation of that
   decision, and it drifts** — one branch gets the new field, the other is forgotten.
3. Let the framework's own negotiation (route/response macros, exception handler rendering) make the
   decision; the controller returns data or throws, not a format-branched response.

## Output / checkpoint
No controller or catch block in the diff branches on `wantsJson()`/`Accept` header/equivalent to
build two different response shapes by hand — the framework's own negotiation decides.

## Guardrails
- The same rule applies to exceptions — `skills/laravel-conventions` §11 covers the failure-path
  version of this, and `laravel-throw-dont-return-errors` is its standalone trigger.
- If a genuinely custom negotiation rule is needed project-wide, it belongs in one place (a macro, a
  renderer override), not repeated per controller.

## Origin
No external source: this is `skills/laravel-conventions` §6.13 extracted to its own trigger. Written
2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
