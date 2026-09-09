---
name: laravel-no-magic-strings
description: "Use when a domain value (status, type, kind, mode), a queue/config/event name, or a threshold is written as a bare string or number: give it a name."
---

# laravel-no-magic-strings

Narrow trigger extracted from `skills/laravel-conventions` §5.3, so a bare string or number with
domain meaning routes here directly instead of only through the whole Laravel block.

## When
Writing or reviewing code that compares against, assigns, or branches on a literal string or number
that carries domain meaning — a status, a type, a category, a queue name, a config key, an event
name, or a threshold.

## Steps
1. **A domain value (status, type, kind, mode) becomes an enum.** A bare `'active'`/`'pending'`
   string compared with `===` is one typo away from a silent false, in every place it's repeated.
2. **A queue name, config key or event name becomes a constant or a config entry**, not a string
   retyped at every call site — a rename then means finding every occurrence by hand.
3. **A threshold becomes a named constant.** `if ($count > 50)` reads as an arbitrary number; naming
   it states the rule it enforces.

## Output / checkpoint
No literal string or number with domain meaning appears more than once in the diff, or unnamed at
all — each resolves to an enum case, a constant, or a config entry with one source of truth.

## Guardrails
- This is the string/number half of `skills/laravel-conventions` §5.3's pair with point 11 (English
  everywhere) and point 8 (dates through localised accessors, never a hand-rolled lookup array) —
  read `skills/laravel-conventions` §5 before treating a hardcoded lookup table as an exception.
- A fixed-set domain value stored in the database is also `laravel-no-db-enums`'s concern — the two
  overlap where the value is both compared in PHP and persisted.

## Origin
No external source: this is `skills/laravel-conventions` §5.3 extracted to its own trigger. Written
2026-09-09, same pilot as `laravel-no-db-enums`.
