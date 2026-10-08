# flutter-startup-error-hooks: origin and source stamps

> Provenance of `skills/flutter-startup-error-hooks`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and source reading, never run by us. No app was built or started
while writing it. This block is meant to be folded into `flutter-conventions` §9 (hooks and startup, after its
crash-reporting point) and §7 (state library specifics) when their owner chooses; until then it stands alone
so nothing is added to an existing block.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Flutter documentation page on handling errors (fetched from docs.flutter.dev) | CC-BY-3.0 text, BSD code (repository LICENSE), read 2026-10-08 | Scope of the two hooks, presenting the error, returning `true` |
| Flutter API reference: `PlatformDispatcher.onError`, `SchedulerBinding.addPostFrameCallback`, `AppLifecycleState` | BSD-3, read 2026-10-08 | Return contract and fallback, post-frame semantics, no guaranteed lifecycle notification |
| Startup skill of an MIT-licensed Flutter skills repository (file) | MIT, read 2026-10-08 | Launch order, hooks first, first-frame reads, deferred warm-up, flush observer, unwrapping |
| Bootstrap and startup-gate references of a second MIT-licensed Flutter skills repository (files) | MIT, read 2026-10-08 | The disagreement on zones (1.4), retry disabled at the root scope |
| Riverpod site docs: retry, auto dispose, mutations, eager initialisation pages (files) | MIT, read 2026-10-08 | Retry defaults and rules, eager consumer, dispose callback, experimental mutations |
| Bloc docs: three lint-rule pages (files) | MIT, read 2026-10-08 | Public surface rules and the lint package version of the void rule |

## Removed in the verification pass (no page supporting them)
The claim that returning `false` makes the process exit or hang (the API reference says only that a fallback
such as printing to the error stream is used), the "about 38 seconds" retry total and "about ten tries up to a
few seconds" paraphrases (replaced by the documented 10 retries, 200 ms to 6.4 s), the "never any zone" rule
as universal (two sources disagree).

## Not verified
1. **Own guidance, flagged in the text:** an error hook never throws (1.3), features expose a flush (1.6.3),
   the retry judgement for local deterministic failures (2.1.3).
2. **The current setup guide of any crash SDK** was not read, so whether a given SDK wants a zone is open.
3. **Riverpod and Bloc versions:** the clone's documentation was read, not the released package pages; the
   Riverpod pages sit under the version 3 concepts folder.
4. **The Flutter error-handling page was read through a fetch tool that summarises pages,** so its wording
   was not compared sentence by sentence.
5. **An unwrapped-cause accessor** on `ProviderException` was not looked up; the text names no property.

## Related blocks
`flutter-conventions` (§1, §4, §7, §9), `flutter-four-async-states`, `flutter-dispose-what-you-create`,
`observability-instrumentation`.
