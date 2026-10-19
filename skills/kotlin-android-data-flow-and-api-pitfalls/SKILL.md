---
name: kotlin-android-data-flow-and-api-pitfalls
description: "Use when structuring an Android app's data and UI layers or designing Kotlin APIs: offline-first repositories, flows instead of snapshots, sealed UI state, state flows in view models, sync with backoff, and where Kotlin functions, value classes and multiplatform platform boundaries belong."
---

# kotlin-android-data-flow-and-api-pitfalls

Step 5 of the pipeline (`WORKFLOW.md`), for Kotlin on Android and shared Kotlin code. The premise: **a repository
that returns a snapshot, a view model that exposes a cold flow, or an extension function that hides a
dependency each works in the first screen and rots by the fifth**, because the data can change under the
caller, the UI cannot show every state, and nobody owns the behaviour. Android edge-to-edge and security rules
are `android-edge-to-edge-insets` and `android-security-hardening`; the Gradle and R8 side is
`android-agp9-r8-gradle`.

## When
- A repository, data source, view model or UI state class is added or its shape changes.
- A background sync, a local database or a remote source is wired to the screen.
- A Kotlin extension function, a factory, a one-field wrapper type or an `expect` declaration is added.

## Steps

**Read only the part the task meets.** They are independent.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Android data flow: layers, offline-first reads, writes, sync, UI state, state flows, events | a repository, a view model or a screen state is written | [`01-android-data-flow.md`](./references/01-android-data-flow.md) |
| 2 | Kotlin API design: function ownership, value classes versus data classes, multiplatform boundaries | an extension, a factory, a wrapper type or a platform seam is added | [`02-kotlin-api-design.md`](./references/02-kotlin-api-design.md) |

## Output / checkpoint
Each repository method says whether it returns a stream or performs a write, each screen state is a closed
hierarchy the UI handles exhaustively, and each new function names its semantic owner. A claim that a screen
"handles loading and errors" without naming the state type that carries them is not verified.

## Guardrails
- Never expose repository reads as one-shot snapshots when the data can change (part 1).
- Never add an extension on a standard or framework type that hides parsing, repository access or clock policy
  (part 2).
- Never put a platform type in a common signature (part 2).
- No block and no agent installs a library: the blocks name it and the user installs it (`CONVENTIONS.md`).
- Versions: the rules are architecture guidance, not API reference; each names its source. Nothing was built
  or run while writing this block.

## Origin
Rewritten from the Now in Android architecture guide (Apache-2.0) and the Kotlin API design skill of the
chrisbanes skills repository (Apache-2.0), read 2026-10-16. Meant to be folded into the Kotlin language block when
the extended language blocks (the unmerged PR 118) land; until then it stands alone. 🟡: never run by us; open
points are in [`references/origin.md`](./references/origin.md).
