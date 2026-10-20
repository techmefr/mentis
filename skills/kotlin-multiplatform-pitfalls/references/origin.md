# kotlin-multiplatform-pitfalls: origin and source stamps

> Provenance of `skills/kotlin-multiplatform-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from the author's own craft knowledge. Never dogfooded; no multiplatform project was built.

## Sources (read 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| None opened. The review found no creditable source for this gap; the existing Kotlin API-design block already credits the one open source read for the expect/actual seam | n/a | Nothing taken |

## Removed
- Gradle snippets, plugin ids, library names with versions, and Kotlin/Native compiler flags: not covered.
- Desktop, web and server targets: not covered beyond the shared rules.

## Not verified
1. **All runtime statements** (memory model, dispatcher behaviour, Swift export limits, exception crossing, generated names) are general knowledge and were not checked against the current Kotlin documentation or run. The memory model and interop tooling change between releases: re-read before relying.
2. **Compose Multiplatform on iOS** maturity and component gaps change quickly; §2.3 is guidance on method, not a status report.
3. **Library recommendations** are by category, not by name, on purpose.

## Related blocks
`kotlin-android-data-flow-and-api-pitfalls`, `kotlin-android-conventions`, `swift-conventions`, `mobile-crash-symbolication-pitfalls`, `mobile-release`, `source-freshness`.
