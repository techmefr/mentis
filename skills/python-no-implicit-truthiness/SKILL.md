---
name: python-no-implicit-truthiness
description: "Use when checking a value that could be None, 0, an empty string, or an empty collection: never bare if x, always is None/is not None or an explicit emptiness check."
---

# python-no-implicit-truthiness

Narrow trigger extracted from `skills/python-conventions` §2.1–§2.2, so a bare truthiness check
routes here directly instead of only through the whole Python block.

## When
Writing or reviewing a condition on a value that could legitimately be `0`, `""`, `[]`, `{}`, or a
third-party object — anywhere the intent is "is this missing" rather than "is this falsy".

## Steps
1. **`if x is None:` / `is not None`, always**, when the question is presence — `if x:` is also
   false for a valid `0`, `""`, `[]`, `{}`, so a legitimate empty value takes the missing-value
   branch.
2. **`x or default` replaces a legitimate `0` or `""` with the default** — the same trap in
   assignment form.
3. **`if not items` does not distinguish "no list" from "an empty list".** State which one is meant.
4. **A bare `if value` on a third-party object** silently calls whatever truthiness that object
   defined — read what it actually returns before trusting it.

## Output / checkpoint
Every presence check in the diff is `is None`/`is not None` (or an explicit `len(x) == 0` when
emptiness, not absence, is the actual question) — no bare `if x:`/`if not x:` where `x` could be a
legitimate falsy value.

## Guardrails
- The bug this produces never reproduces on the developer's own data — a quantity of zero, an empty
  note, a customer with no orders yet — which is exactly why it survives review.
- Where the boundary itself should express presence/absence in its return type, that's
  `skills/python-conventions` §2.3 — read it for the public-boundary shape of this same question.

## Origin
No external source: this is `skills/python-conventions` §2.1–§2.2 extracted to its own trigger. The
reasoning stays in the parent block. Written 2026-09-09, same restructuring pilot as
`laravel-no-db-enums`.
