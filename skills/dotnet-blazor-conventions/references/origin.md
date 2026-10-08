# dotnet-blazor-conventions: origin and source stamps

> Provenance of `skills/dotnet-blazor-conventions`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us. mentis had no Blazor block; this
one is new and not meant to be folded into another.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Blazor docs: component lifecycle, prerendering, render modes | CC-BY-4.0, read 2026-10-08 | Double initialisation, `PersistentComponentState`, `[PersistentState]` for .NET 10 and later, Auto mode behaviour and client project requirement |
| Blazor docs: JavaScript interoperability (from .NET, to .NET) | CC-BY-4.0, read 2026-10-08 | No JS during prerendering, `JSDisconnectedException`, `DotNetObjectReference` disposal, `IAsyncDisposable` pattern, public invokable methods |
| Blazor docs: dependency injection, Entity Framework Core, state, synchronization context | CC-BY-4.0, read 2026-10-08 | Circuit-length scopes, `DbContext` factory, event unsubscription, `InvokeAsync` |
| Blazor docs: components, overwriting parameters, events, forms, error handling | CC-BY-4.0, read 2026-10-08 | Parameter rule, `EventCallback`, form name and antiforgery, production error messages, detailed errors default, error boundaries |

## Removed in the verification pass (no page supporting them)
`IJSInProcessRuntime` WebAssembly-only claim, the "invokable method silently fails if not public" wording,
and the `DbContext` "never" wording (now our own guidance following from where the code runs).

## Not verified
1. **Own guidance, flagged as such in the text:** awaited lifecycle methods, idempotent initialisation,
   `_ = InvokeAsync`, singleton sharing across circuits (inference from DI), instance over static invokable
   methods, JS calls per render, server-side validation, stable error message.
2. **`DataAnnotationsValidator` requirement** was not re-read on the forms page.
3. **Pre-.NET 10 callback registration details** for `PersistentComponentState` were not re-read.

## Related blocks
`dotnet-conventions`, `dotnet-aspnet-efcore-pitfalls`, `security-hardening`.
