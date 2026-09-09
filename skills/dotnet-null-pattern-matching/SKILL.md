---
name: dotnet-null-pattern-matching
description: "Use when testing a value for null: prefer the pattern form (is null / is not null) over the equality operator — and never == inside an equality operator's own body, that's infinite recursion, not a style choice."
---

# dotnet-null-pattern-matching

Narrow trigger extracted from `skills/dotnet-conventions` §5.6, so a null check routes here directly
instead of only through the whole .NET block.

## When
Writing or reviewing a null check — especially inside a type's own `operator ==`/`Equals` override,
where the wrong form is a functional bug, not just a style deviation.

## Steps
1. **Test null with the pattern form** (`is null` / `is not null`) rather than the equality operator,
   and avoid the roundabout not-null spellings.
2. This is a preference in ordinary code — an informed override is fine.
3. **Inside an equality-operator body, using the equality operator is infinite recursion**, not a
   style choice. `is null`/`is not null` is the only correct form there, because `==` calls the very
   operator being defined.

## Output / checkpoint
Null checks in the diff use `is null`/`is not null`; any `operator ==`/`Equals` override in the diff
never compares to `null` with `==` inside its own body.

## Guardrails
- The pattern form isn't just style inside an overload — a type that overrides `==` and then checks
  `x == null` inside that same overload recurses until it stack-overflows, which is why this is a
  correctness rule at that one call site specifically.
- The rest of the disposal/nullability/enumeration section lives in `skills/dotnet-conventions` §5 —
  read it for the neighbouring rules this one sits beside.

## Origin
No external source: this is `skills/dotnet-conventions` §5.6 extracted to its own trigger. Written
2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
