---
name: kotlin-multiplatform-pitfalls
description: "Use when writing or reviewing a Kotlin Multiplatform or Compose Multiplatform project that shares code between Android, iOS and other targets: source-set layout and dependencies, what belongs in common code, coroutines and threading on iOS, Swift interop of Kotlin APIs, shared storage and networking, and build and release friction."
---

# kotlin-multiplatform-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for code compiled once and run on several platforms. The premise: **common code
compiles everywhere and still behaves differently on each target**: a dependency that exists only on one platform
fails at the iOS link step, a coroutine that is fine on Android crashes the iOS app from the wrong thread, a Kotlin
type reaches Swift as something unusable, a shared module grows until the iOS build takes ten minutes. The seam
between common and platform code (`expect`/`actual` versus interfaces) is in
`kotlin-android-data-flow-and-api-pitfalls` §2.3; Android-only rules are in `kotlin-android-conventions`.

## When
- A shared module, source set or target is added, or its dependencies change.
- Common code touches time, files, storage, networking, threads or the UI.
- A Kotlin API is exposed to Swift or Objective-C.
- A shared module's build time, binary size or release step is the complaint.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Source sets, common versus platform code, dependencies, libraries for storage, network and time | a module, target or dependency is added or reorganised | [`01-structure-and-common-code.md`](./references/01-structure-and-common-code.md) |
| 2 | Coroutines and threads on iOS, Swift interop, Compose Multiplatform, build and release | code crosses to iOS, or a build or crash on one platform is the problem | [`02-runtime-interop-and-delivery.md`](./references/02-runtime-interop-and-delivery.md) |

## Output / checkpoint
For a change touching this block: every target in the project compiles and its tests run (not only Android), the
common source set imports only multiplatform dependencies, exposed APIs were called once from Swift, and
coroutine scopes and dispatchers are injected, not created in common code.

## Guardrails
- Keep common code to what is truly portable (§1.1). Never import a platform class in the common source set.
- Pick libraries that declare every target you ship (§1.3). Never assume an Android library has an iOS variant.
- Inject dispatchers and scopes (§2.1). Never hard-code a main-thread assumption in common code.
- Design the exported surface for Swift callers (§2.2). Never export the whole module by default.
- Build and test every target in the pipeline (§2.4). Never gate only on the Android build.
- Plugin, library and compiler versions move fast; re-read the release notes of the versions in use (🟡, nothing here was built).

## Origin
Written from our own craft knowledge of Kotlin Multiplatform practice, with the source-set, interop and memory points checked on 2026-10-20 against the Kotlin documentation (Apache-2.0 repository). No source text was taken. See
[`references/origin.md`](./references/origin.md).
