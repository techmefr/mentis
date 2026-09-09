---
name: dotnet-options-lifetime-mismatch
description: "Use when injecting IOptions/IOptionsSnapshot/IOptionsMonitor: the three forms are three lifetimes, and mixing them is a captive dependency — a snapshot injected into a singleton is a request-scoped value pinned for the process."
---

# dotnet-options-lifetime-mismatch

Narrow trigger extracted from `skills/dotnet-conventions` §2.18, so an options injection routes here
directly instead of only through the whole .NET block.

## When
Injecting `IOptions<T>`, `IOptionsSnapshot<T>`, or `IOptionsMonitor<T>` into a class — specifically
when that class is registered as a singleton.

## Steps
1. **The three ways to read options are three lifetimes.** The plain `IOptions<T>` form is a value
   read once for the process; the snapshot form is per-request and recomputed; the monitor form is a
   long-lived object that also reports changes.
2. **Mixing them is a captive dependency.** A snapshot injected into a singleton is a request-scoped
   value pinned for the lifetime of the process — the same bug as a scoped service captured by a
   singleton, with none of the usual symptoms, because the value is merely stale rather than throwing
   an object-disposed exception.
3. **A singleton that has to see changed configuration takes the monitor.** Anything else takes the
   plain form and stops there.

## Output / checkpoint
Every singleton in the diff injecting options uses `IOptions<T>` (never changes) or
`IOptionsMonitor<T>` (needs live changes) — never `IOptionsSnapshot<T>`, which is scoped-lifetime only.

## Guardrails
- This is the options-specific case of a captive-dependency lifetime mismatch — the general DI
  lifetime rules live in `skills/dotnet-conventions` §2, including the neighbouring rule on why a
  hand-written factory resolving from the provider is a service locator in disguise.
- The failure here is silent staleness, not a crash — which is exactly why it survives review longer
  than a lifetime mismatch that throws.

## Origin
No external source: this is `skills/dotnet-conventions` §2.18 extracted to its own trigger. Written
2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
