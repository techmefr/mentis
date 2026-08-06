---
name: dotnet-conventions
description: Use when writing or reviewing C#/.NET (ASP.NET Core, EF Core), applies the highest-value async/await, IDisposable, dependency injection and EF Core patterns from the Roslyn analyzers (CAxxxx) and Meziantou.Analyzer. No internal production experience behind this block, content sourced from established market tooling/guides.
---

# dotnet-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the writing and review of C#/.NET code. **Special
status**: like `go-conventions`, no Xefi production experience behind this file yet: content coming from
the Roslyn analyzers (`Microsoft.CodeAnalysis.NetAnalyzers`, enabled by default since .NET 5) and
Meziantou.Analyzer, not from real review feedback. A solid base to be confronted with the first real .NET
project, not proven doctrine.

**Boundary with the `xefi-claude-skills` plugin** (dedup audit, 2026-08-06): its `csharp` plugin ships 15
skills (async/await with cancellation, constructor DI, logger injection, restrictive access, and a set of
explicit prohibitions). **Where it's installed, it is the authority.** This block keeps the
analyzer-derived baseline for a codebase without it.

## When
As soon as C#/.NET code is written or modified, during `code` (6) or `tdd` (5).

## Steps

### 1. Async/await: the most frequent mistake
1. Never `.Result`/`.Wait()`/`.GetAwaiter().GetResult()` inside a method that's already async (CA1849): a
   classic source of deadlock on the synchronisation context.
2. `async void` reserved for event handlers: elsewhere, exceptions can't be caught and the method doesn't
   compose with `await`.
3. A `Task` that's never `await`-ed or stored (implicit "fire-and-forget") silently swallows its
   exceptions.
4. `ConfigureAwait(false)` in shared library code; less critical on the ASP.NET Core server side (no
   synchronisation context at that level), but worth keeping explicit rather than forgetting it by default
   (CA2007).

### 2. IDisposable and lifecycle
1. An `IDisposable` created locally is disposed on every path (`using`/`using` declaration), including the
   exception paths (CA2000).
2. The full `Dispose(bool)` pattern with `GC.SuppressFinalize` if `IDisposable` is implemented by hand
   (CA1063): never a partial `Dispose()`.
3. `!` (null-forgiving) is not a way to silence the compiler with no real guarantee: every use has to be
   justifiable, not a reflex. Nullable Reference Types enabled consistently across the whole project, not
   partially.
4. A LINQ query re-enumerated several times (multiple enumeration) on a deferred-execution `IEnumerable`
   re-runs the query on every iteration; materialise it (`.ToList()`) if the source is expensive or has a
   side effect (CA1851, known blind spots: check by eye too).
5. An empty `catch {}` or a `catch (Exception) {}` with no log or rethrow swallows a real bug: never a
   silent catch.

### 3. Dependency injection
1. A `Scoped` service never injected into a `Singleton` ("captive dependency"): it freezes for the app's
   whole lifetime (e.g. a `DbContext` shared between concurrent requests).
2. General lifetime rule: a service only depends on a service with a lifetime equal to or longer than its
   own.
3. A `Singleton`/background worker that needs a scoped service goes through `IServiceScopeFactory` to
   create a manual scope: never a direct injection of the scoped service.

### 4. ASP.NET Core and EF Core
1. `AsNoTracking()` on every read-only EF Core query: without it, a measured perf cost (~2x slower at
   scale) and unwanted state tracking.
2. Middleware order checked by eye (`UseRouting`/`UseAuthentication`/`UseAuthorization`): no dedicated
   Roslyn rule, a frequent review mistake with no automatic detection.
3. Minimal API: per-endpoint validation/filters are less visible than in classic Controllers: check
   explicitly at review time that they exist, don't assume they're inherited from elsewhere.

## Output / checkpoint
Code compliant with the four sections above, and a build with no new
`Microsoft.CodeAnalysis.NetAnalyzers`/Meziantou warning introduced by the diff. Checked by `gate` (7) and
`review` (8).

## Guardrails
No comments in the code produced. This block hasn't been confronted with a real production .NET project
at Xefi yet; if a rule here diverges from a real observed need, fix this block rather than treating it as
settled. The Framework Design Guidelines (public API naming) are only relevant for shared library code,
not for internal application code: don't impose them outside that context.

## Origin
Ideas taken from: the `Microsoft.CodeAnalysis.NetAnalyzers` Roslyn analyzers (rules CA2007, CA1849,
CA2000, CA1063, CA1851 cited); Meziantou.Analyzer (async/disposal/culture-invariance); the EF Core
documentation (tracking vs no-tracking); the "captive dependency" pattern documented by the .NET
community. Mechanisms rewritten, no copied text. Market research, no internal production feedback at this
stage.
