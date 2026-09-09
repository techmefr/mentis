---
name: dotnet-no-swallow-exceptions
description: "Use when writing or reviewing a catch block: never an empty catch {} or a catch (Exception) {} with no log or rethrow — it reports success having done nothing, and leaves no log entry when the incident happened."
---

# dotnet-no-swallow-exceptions

Narrow trigger extracted from `skills/dotnet-conventions` §5.5, so a `catch` block routes here
directly instead of only through the whole .NET block.

## When
Writing or reviewing any `try`/`catch` — a boundary converting a library exception, a background
operation, a fire-and-forget `Task`.

## Steps
1. **An empty `catch {}` or a `catch (Exception) {}` with no log or rethrow swallows a real bug.**
   Never a silent catch.
2. **The visible consequence is a request that reports success having done nothing.** The invisible
   one is that the log has no entry at the moment the incident actually happened.
3. **A `Task` never awaited or stored is the same failure in fire-and-forget clothes.** It silently
   swallows its exceptions unless something explicitly observes them.

## Output / checkpoint
Every `catch` in the diff either logs with the original exception, rethrows (bare `throw` or
`ExceptionDispatchInfo` to preserve the stack), or does something concrete — never empty, never
log-only-then-continue on a path that should have failed.

## Guardrails
- Catching by type, not by message, is what survives a refactor — a broad `catch (Exception)` that
  also swallows a genuine bug in the handling code itself is the specific failure this rule targets.
- A fire-and-forget `Task` needs an explicit continuation or a supervised background-task pattern to
  observe its exceptions — `skills/dotnet-conventions` §1 covers the async-specific version.

## Origin
No external source: this is `skills/dotnet-conventions` §5.5 (and the fire-and-forget note in §1)
extracted to its own trigger. Written 2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
