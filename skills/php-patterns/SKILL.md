---
name: php-patterns
description: Use when writing or reviewing pure PHP at the language level, whatever the framework, typing, error handling, OOP patterns. The framework layer above it is skills/laravel-conventions; reviewing a diff is the PHP reviewer's job. Little internal production experience on this language, content sourced from PHP-FIG (PSR) and established market standards.
---

# php-patterns

Step 6 of the pipeline (`WORKFLOW.md`), upstream of the Laravel layer: the language itself, before
the Eloquent/Laravel conventions that stack on top (see `gimli`, `morpheus`).

**Boundary with the `xefi-claude-skills` plugin** (dedup audit, 2026-08-06): its `laravel` plugin ships 45
skills on the framework layer — routing, tests, config, control flow, package choices, CRUD via the REST
API. **Where it's installed, it is the authority there.** This block stays deliberately below it: the PHP
language itself, on any framework. Don't add a Laravel rule here.

## When
As soon as PHP is written or reviewed, on any framework: this block is the common base, the Laravel
conventions apply on top of it, not instead of it.

## Steps

### 1. Typing: modern PHP (8.x) is no longer untyped PHP
1. Typed function/method signatures (parameters + return), including an explicit `void`/`?type`; an
   untyped parameter is a regression, not a neutral style in PHP 8+.
2. `readonly` on properties that never change after construction (value objects, DTOs): prevents an
   accidental deep mutation.
3. Union types (`int|string`) rather than `mixed` out of reflex: `mixed` expresses no intent, an
   explicit union type documents the real contract.
4. Native PHP 8.1+ enums (`enum ... : string`) rather than class constants scattered around to
   represent a closed set of values.

### 2. Error handling
1. A specific exception thrown (a dedicated class, not a generic `\Exception`) as soon as the caller
   has to be able to tell the error case apart to react differently.
2. A `catch` that swallows the exception without rethrowing or logging it hides a real bug: never a
   silent `catch`, even as a last resort.
3. An ambiguous `null` return (failure vs legitimate absence): prefer an exception for a real
   failure, `null`/an option only for an expected and documented absence.

### 3. OOP and structure
1. Composition rather than deep inheritance (>2 levels): deep inheritance couples behaviours that
   should stay independent.
2. An interface defined at the edge (a service's public contract) even with a single implementation:
   makes replacement/mocking easier without breaking the caller.
3. A mutable static property = hidden global state: to be avoided except in an explicitly accepted
   case (immutable config, not a counter that changes).
4. `match` (PHP 8+) rather than `switch` for a simple value comparison: no implicit fallthrough,
   returns a value directly.

## Output / checkpoint
Code compliant with the three sections above, checked on top of the applicable Laravel conventions
through `gate` (7) and `review` (8, `gimli`).

## Guardrails
No comments in the code produced (Xefi team rule, all repos). This block has no deep internal
production experience behind it (g.compigni is new to PHP, as noted on `gimli`): if a rule here
diverges from a real need observed in the field, fix this block rather than treating it as settled.

## Origin
Sourced from PHP-FIG (PSR-12 style, the base PSRs), the official PHP documentation (types, enums,
`readonly`, `match`) and established modern PHP market practice. Mechanisms rewritten, no copied
text. Market research, no deep internal production feedback at this stage: same uncertainty status
as `gimli`.
