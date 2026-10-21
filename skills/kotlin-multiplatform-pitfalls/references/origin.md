# kotlin-multiplatform-pitfalls: origin and source stamps

> Provenance of `skills/kotlin-multiplatform-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from the author's own craft knowledge, with part of the runtime claims checked against the Kotlin documentation on 2026-10-20. Never dogfooded; no multiplatform project was built.

## Sources (read 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| Kotlin documentation: multiplatform hierarchy, expect and actual, Objective-C interop, native memory manager | Apache-2.0 (`LICENSE` of the documentation repository read 2026-10-20; it names no separate documentation licence); rewritten, nothing copied | Template and explicit edges (§1.2.1), prefer interfaces over expect (§1.1.4), shared heap (§2.1.3), suspend bridge (§2.1.5), generics limits (§2.2.2), exception rule (§2.2.3), name clashes (§2.2.4) |
| The existing Kotlin API-design block's open source for the expect/actual seam | credited in that block | Not re-read |

## Removed
- Gradle snippets, plugin ids, library names with versions, and Kotlin/Native compiler flags: not covered.
- Desktop, web and server targets: not covered beyond the shared rules.

## Not verified
1. **Checked:** default hierarchy template, expect and actual advice, shared-heap memory manager, exception crossing, suspend bridge, generics limits, name clashes. **Also checked 2026-10-20:** value classes unsupported in the export, extension and top-level mapping, and the main-thread queue in unit tests. **Unverified:** default arguments in the export, sealed hierarchies, dispatcher injection, thread-affinity of callbacks, cancellation scoping, library choices (time, network, storage, serialisation, injection), version catalogue, build speed, Swift export, shared UI maturity, symbol upload. The memory model and interop tooling change between releases: re-read before relying.
2. **Compose Multiplatform on iOS** maturity and component gaps change quickly; §2.3 is guidance on method, not a status report.
3. **Library recommendations** are by category, not by name, on purpose.

## Related blocks
`kotlin-android-data-flow-and-api-pitfalls`, `kotlin-android-conventions`, `swift-conventions`, `mobile-crash-symbolication-pitfalls`, `mobile-release`, `source-freshness`.
