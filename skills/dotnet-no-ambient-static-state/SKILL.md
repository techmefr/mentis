---
name: dotnet-no-ambient-static-state
description: "Use when reaching for a static mutable field, a singleton .Instance, or an ambient static read like DateTime.Now: inject it instead — that's what makes it testable, and static state makes test order matter."
---

# dotnet-no-ambient-static-state

Narrow trigger extracted from `skills/dotnet-conventions` §4.1, so a static mutable field or an
ambient static read routes here directly instead of only through the whole .NET block.

## When
Writing or reviewing code that reaches for a `public`/`internal static` mutable field or property, a
singleton class with a static `.Instance` holding mutable state, `[ThreadStatic]`, or an ambient
static read such as `DateTime.Now` or a static current-context accessor.

## Steps
1. **No mutable global state.** No `public`/`internal static` mutable field or property, no singleton
   class with a static `.Instance` holding mutable state, no `[ThreadStatic]`.
2. **Ambient static reads (`DateTime.Now`, a static current-context accessor) are injected instead**
   — an abstraction (a clock, a context accessor) passed through the constructor, not called
   statically from inside the method.
3. **That's also what makes the code testable.** A test can substitute a fixed clock or a known
   context; a hardcoded static read cannot be substituted at all.

## Output / checkpoint
No code path in the diff reads a mutable static field/property or calls an ambient static accessor
directly — every such value is injected through the constructor as a dependency.

## Guardrails
- The failure static state produces is the one that costs most to diagnose: state surviving between
  tests makes execution order matter, so a suite fails only when a specific test runs second and
  passes when run alone.
- This is a testability rule first — the production behaviour of a static read and an injected one
  can be identical; the difference only shows up the moment something needs to substitute it.

## Origin
No external source: this is `skills/dotnet-conventions` §4.1 extracted to its own trigger. Written
2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
