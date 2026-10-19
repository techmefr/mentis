# dotnet-async-exception-pitfalls: origin and source stamps

> Provenance of `skills/dotnet-async-exception-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never compiled or run by us.

This block is meant to be folded into the same-topic references of `dotnet-conventions` (async and idioms
sections) and `dotnet-no-swallow-exceptions` when the branch `feat/antislop-lot` (PR 118) lands.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| The ErrorProne.NET analyzer rule pages (ERP021, EPC12, EPC17, EPC18, EPC19, EPC26, EPC31, EPC32, EPC37, EPC38, EPC16) | MIT, read 2026-10-08 | Explicit rethrow, message-only catch, async void delegates, task as string, registration disposal, tasks in using, null tasks, completion source flag, eager validation, re-enumeration, await of null-conditional |
| The Meziantou analyzer rule pages (MA0009, MA0021, MA0022, MA0027, MA0039, MA0050, MA0054, MA0064, MA0066, MA0072, MA0085, MA0100, MA0129, MA0132, MA0147, MA0152, MA0158, MA0173, MA0227, MA0242) | MIT, read 2026-10-08 | Rethrow, inner exception, finally, lock targets and type, anonymous unsubscribe, struct hash keys, set Contains, implicit date conversion, regex timeout, certificate callback, iterator validation, GetOrAdd value evaluation |
| vs-threading rule page VSTHRD011 | MIT, read 2026-10-08 | Lazy of Task deadlock and the async lazy type |
| .NET API pages: Math.Round, DateTimeOffset implicit conversion, ProcessStartInfo.UseShellExecute | CC-BY-4.0, read 2026-10-08 | Midpoint rounding to even; offset by kind; default false on .NET and true on .NET Framework, false needed to redirect streams |
| .NET regular expression best-practices page | CC-BY-4.0, read 2026-10-08 | Timeouts, NonBacktracking from .NET 7, untrusted patterns not protected |

The unlicensed async-guidance repository was used for no phrasing.

## Removed in the verification pass (no page supporting them)
`ExceptionDispatchInfo` advice, exception filters, `OperationCanceledException` handling, `ContinueWith`
scheduler advice, `Task.WhenAll` first-exception behaviour, `Parallel.ForEach` with async lambdas,
`string.GetHashCode` randomisation, disposable-field reassignment and disposable property rules.

## Not verified
1. **Own guidance, flagged as such in the text:** log at the boundary, log once per failure, no exception
   text in user responses, side-effect-free `GetOrAdd` factories, unsubscribe in `Dispose`.
2. **Async void in a task-returning delegate position** is from the EPC17 and MA0147 titles and
   descriptions; the compiler behaviour in each case was not run.
3. **The `LazyInitializer` advice** follows MA0173; the runtime behaviour was not tested.

## Related blocks
`dotnet-conventions` §1, §5 and §7, `dotnet-no-swallow-exceptions`, `dotnet-dispose-what-you-own`,
`observability-instrumentation`.
