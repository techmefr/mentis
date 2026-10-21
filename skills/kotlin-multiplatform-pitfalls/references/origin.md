# kotlin-multiplatform-pitfalls: origin and source stamps

> Provenance of `skills/kotlin-multiplatform-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from the author's own craft knowledge, with part of the runtime claims checked against the Kotlin documentation on 2026-10-20. Never dogfooded; no multiplatform project was built.

## Sources (read 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| Kotlin documentation: multiplatform hierarchy, expect and actual, Objective-C interop, native memory manager | Apache-2.0 (`LICENSE` of the documentation repository read 2026-10-20; it names no separate documentation licence); rewritten, nothing copied | Template and explicit edges (§1.2.1), prefer interfaces over expect (§1.1.4), shared heap (§2.1.3), suspend bridge (§2.1.5), generics limits (§2.2.2), exception rule (§2.2.3), name clashes (§2.2.4) |
| JetBrains/kotlin-web-site `LICENSE`, and the kotlinlang.org pages for multiplatform hierarchy, expected and actual declarations, Objective-C interop and Compose Multiplatform; the docs source files for the native memory manager and Objective-C interop | Apache-2.0 (`LICENSE` re-read 2026-10-20: template copyright line, covers documentation source); the hosted pages are the same documentation, read for facts and rewritten | Hierarchy template rules and opt-out, interface-first advice and Beta status, exception rule, naming stability warning, shared heap and leak check, Compose caveats |
| Kotlin/kotlinx.coroutines: `LICENSE.txt` and `kotlinx-coroutines-test/README.md` | Apache-2.0, Copyright 2000-2020 JetBrains s.r.o. and Kotlin Programming Language contributors (read 2026-10-20) | Dispatcher injection, global main-dispatcher swap |
| The existing Kotlin API-design block's open source for the expect/actual seam | credited in that block | Not re-read |

## Removed
- Gradle snippets, plugin ids, library names with versions, and Kotlin/Native compiler flags: not covered.
- Desktop, web and server targets: not covered beyond the shared rules.

## Not verified
1. **Checked:** default hierarchy template, expect and actual advice, shared-heap memory manager, exception crossing, suspend bridge, generics limits, name clashes. **Also checked 2026-10-20:** value classes unsupported in the export, extension and top-level mapping, and the main-thread queue in unit tests. **Also checked 2026-10-20:** dispatcher injection (coroutines test readme), name clash algorithm not stable between releases, Compose component and resource caveats, Beta status of expected and actual classes. **Unverified:** default arguments and sealed hierarchies in the export (the interop page is silent), thread-affinity of callbacks, cancellation scoping, library choices (time, network, storage, serialisation, injection, and the reflection-based container remark), version catalogue, build speed, Swift export (the page was not found at the URL tried), shared UI maturity (the page read gives no stability labels), symbol upload. The memory model and interop tooling change between releases: re-read before relying.
2. **Compose Multiplatform on iOS** maturity and component gaps change quickly; §2.3 is guidance on method, not a status report.
3. **Library recommendations** are by category, not by name, on purpose.

## Related blocks
`kotlin-android-data-flow-and-api-pitfalls`, `kotlin-android-conventions`, `swift-conventions`, `mobile-crash-symbolication-pitfalls`, `mobile-release`, `source-freshness`.
