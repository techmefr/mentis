---
name: python-no-magic-strings
description: "Use when a domain value (status, type, kind, mode) or a threshold is written as a bare string or number: give it an Enum/StrEnum or a named constant."
---

# python-no-magic-strings

Narrow trigger extracted from `skills/python-conventions` §3.7, so a bare string or number with
domain meaning routes here directly instead of only through the whole Python block.

## When
Writing or reviewing code that compares against, assigns, or branches on a literal string or number
that carries domain meaning — a status, a type, a category, a threshold or a limit.

## Steps
1. **A domain value (status, type, kind, mode) becomes an `Enum`/`StrEnum`**, typed as that enum on
   the model — not a bare string compared with `==` at every call site.
2. **A threshold or limit becomes a named constant.** A literal `50` in a comparison reads as
   arbitrary; naming it states the rule it enforces.
3. **A literal compared in three files is three chances to typo it** — and the typo is not an error,
   it's a comparison that quietly returns false, so the row is simply never picked up.

## Output / checkpoint
No literal string or number with domain meaning appears unnamed in the diff — each resolves to an
`Enum`/`StrEnum` case or a named constant with one source of truth.

## Guardrails
- A fixed-set value that is also persisted to a database is `python-no-db-cascade-delete`'s sibling
  concern on the schema side, not this file's — this one is about the Python-side comparison.
- The full naming section (casing, generic names, English-only, the underscore-prefix boundary) lives
  in `skills/python-conventions` §3 — read it before treating this as the whole naming rule set.

## Origin
No external source: this is `skills/python-conventions` §3.7 extracted to its own trigger. Written
2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
