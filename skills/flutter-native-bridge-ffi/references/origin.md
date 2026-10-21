# flutter-native-bridge-ffi: origin and source stamps

> Provenance of `skills/flutter-native-bridge-ffi`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us. No bridge was generated, no library
built and no hook run while writing it. Overlaps with `skills/flutter-conventions` (2026-10-19); cross-referenced, not merged.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Flutter platform-channels page (repository text) | CC-BY-3.0 text, BSD code (repository LICENSE), read 2026-10-08 | Two routes, web note, main-thread rule, background isolates, task queues, codec types |
| Pigeon README (version 29.0.7, SDK `^3.11.0`) | BSD-3-Clause (file), read 2026-10-08 | Typed bridge, same-version rule, no split across packages, reply once, error translation, task queue, native-interop mode |
| Agent-plugins ffigen skill (file dated 2026-05-28) | BSD-3-Clause (file), read 2026-10-08 | Generate bindings, inclusion lists, generator location, leaf rule, analyzer step |
| Agent-plugins native-assets skill (constraints section only) | BSD-3-Clause (file), read 2026-10-08 | Hook locations, toolchain package, hash checks, offline fallback |
| Dart site hooks page | CC-BY-4.0 text, BSD-3-Clause code (file), read 2026-10-08 | Dart 3.10 and 3.13 floors, link hook purpose |
| Dart API reference: leaf flag (Dart 3.13.5), typed-list view, native finalizer | Site terms not read; facts only, no text copied | Leaf requirements and effect, view lifetime, finalizer guarantees |
| Dart C-interop overview | Site terms not read; facts only | Recommendation to generate wrappers, hooks naming |

## Re-read 2026-10-20 (verification pass)
Opened that day and each figure checked: the Flutter platform-channels page (Pigeon as the typed alternative,
the codec's types, main-thread rule for platform-to-Dart calls only, root and registered background isolates,
task queues on Android and iOS, JavaScript interop for web); the Pigeon README from the repository (licence file
re-read: BSD-3-Clause; channels for Windows and Linux, experimental native interop on Android, iOS and macOS,
same-version rule, no split across packages, generated types in public APIs strongly discouraged, task queue
annotation an error with native interop, error translation, synchronous methods and replying once, definition
file outside `lib`); the Dart hooks page (build hooks 3.10, link hooks and recorded-use tree-shaking 3.13,
`hook/` files, helper packages under dependencies); the Dart C-interop page (ffigen recommended for large APIs,
hooks formerly called native assets); the Dart API pages for the leaf flag, the typed-list view and the
native finalizer (all as 2.3 and 2.4 state; the finalizer detach on manual close is the documented pattern).
Corrected: 1.3.4 (the current page no longer says a channel method must always be on the main thread).
Added: 2.5.5. Still unsourced: the five points marked own guidance below. Pigeon's README does not list enums
among the types it adds, so that word was dropped from 1.5.
## Removed in the verification pass (no page supporting them)
"Pair the allocator and the deallocator exactly" (the allocator API page read states no such rule), "a
reply twice or never" as a documented failure (only the exactly-once advice is documented), "one channel
directory" as a sourced rule (kept as our guidance), "validate every target operating system" as a sourced
rule (kept as our guidance).

## Not verified
1. **Own guidance, flagged in the text:** channels in one directory behind an interface (1.1.5), one owner
   per side and round-trip test (1.2.5), justification checklist (2.1.1), ownership notes (2.4.2), build on
   each shipped target (2.5.5).
2. **The native-assets skill was read for its constraints section only;** its step-by-step sections and
   examples were not studied.
3. **Pigeon's native-interop mode** is experimental per its README and was not exercised.
4. **API reference pages were read through a fetch tool that summarises,** so wording was not compared
   sentence by sentence; the Dart 3.13.5 stamp is from that page.
5. **How Kotlin and Swift generated signatures look** was not checked beyond the README text.

## Related blocks
`flutter-conventions` (§2, §8), `security-hardening`, `flutter-agent-loop`, `flutter-release-toolchain-hygiene`.
