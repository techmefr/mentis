# flutter-native-bridge-ffi: origin and source stamps

> Provenance of `skills/flutter-native-bridge-ffi`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us. No bridge was generated, no library
built and no hook run while writing it. This block is meant to be folded into the same-topic reference of
`flutter-conventions` (a native-interop section next to its platform error-code point) when the extended
version of that block, on the unmerged branch of PR 118, lands; until then it stands alone so nothing cites a
section that is not on the main branch.

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
