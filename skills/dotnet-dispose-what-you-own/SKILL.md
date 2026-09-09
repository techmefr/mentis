---
name: dotnet-dispose-what-you-own
description: "Use when a disposable value comes from DI or a factory: dispose what this code created, nothing else — an injected dependency belongs to the container, and a pooled HttpClient belongs to the factory."
---

# dotnet-dispose-what-you-own

Narrow trigger extracted from `skills/dotnet-conventions` §5.9–§5.10, so a disposable obtained
through DI or a factory routes here directly instead of only through the whole .NET block.

## When
Writing or reviewing code that holds an `IDisposable`/`IAsyncDisposable` obtained from constructor
injection, a factory (`IHttpClientFactory`, a connection factory), or the DI container directly.

## Steps
1. **Dispose what you own, and nothing else.** An injected dependency belongs to the container;
   disposing it takes it away from every other holder.
2. **A singleton disposed by the first request that used it fails for the second**, with an
   object-disposed exception nobody can trace back to a stray `using`. The rule is mechanical: if
   this code created it, this code disposes it.
3. **The shared `HttpClient` is the standard case in both directions.** Creating one per request
   exhausts sockets, because the connection lingers after the object is gone; disposing one obtained
   from `IHttpClientFactory` breaks the pooling the factory exists to provide. Take it from the
   factory and do not dispose it.

## Output / checkpoint
No `using`/`Dispose()` call in the diff targets a value that arrived through constructor injection or
a factory — only values this code's own constructor called directly.

## Guardrails
- A disposable resolved from the DI container's root provider is held until the process ends if never
  disposed by the container's own scope — that's a separate leak, covered in
  `skills/dotnet-conventions` §2.11, not a reason to dispose it by hand.
- An async resource still follows this ownership rule, but through `await using`, not `using` — see
  `skills/dotnet-conventions` §5.11 for the async-specific mechanics.

## Origin
No external source: this is `skills/dotnet-conventions` §5.9–§5.10 extracted to its own trigger.
Written 2026-09-09, same restructuring pilot as `laravel-no-db-enums`.
