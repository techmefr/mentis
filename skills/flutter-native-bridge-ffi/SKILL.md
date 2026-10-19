---
name: flutter-native-bridge-ffi
description: "Use when Dart code has to call native code: a platform channel or a Pigeon-generated bridge between Flutter and Kotlin, Swift or C++, the thread a channel runs on, a background isolate using a plugin, and dart:ffi (generated bindings, leaf calls, native memory and finalizers, build and link hooks that compile or bundle native code). Covers when to choose which and what must never be edited by hand."
---

# flutter-native-bridge-ffi

Step 6 of the pipeline (`WORKFLOW.md`), for the boundary between Dart and the platform's own language. The
premise: **across a language boundary a string name, a message shape or a pointer's lifetime is checked by
nothing the compiler owns, so the boundary is generated where it can be, typed where it cannot, and kept in
one place**. Permissions and platform prompts are `flutter-conventions` §8; reading untrusted data that
crosses the boundary is `security-hardening`; isolates for heavy Dart work are `flutter-conventions` §2 and
§8.

## When
- A feature needs a platform API no existing plugin offers, or wraps a native library.
- A channel call fails on a background thread, returns twice, or silently loses a field after a rename.
- Hand-written `dart:ffi` bindings, a `DynamicLibrary` lookup, or native memory appears in a diff.
- A package needs to compile or bundle native code.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Channels versus Pigeon, the generated-code contract, threading, background isolates, replying once, the data a channel can carry, web | a channel or a generated bridge is written or reviewed | [`01-channels-and-pigeon.md`](./references/01-channels-and-pigeon.md) |
| 2 | FFI: when to reach for it, generated bindings, leaf calls, native memory and finalizers, build and link hooks and their Dart floors | `dart:ffi`, a native library, or a `hook/` directory is involved | [`02-ffi-and-hooks.md`](./references/02-ffi-and-hooks.md) |

## Output / checkpoint
The bridge was exercised end to end on each platform it targets: a call from Dart reached the native side on
the intended thread, returned once, and carried a changed field through both directions after a rename (§1);
for FFI, the generator was re-run and produced no diff, the analyzer was clean, and the native side was
built through the hook, not by hand (§2). A bridge that compiled on one platform is not verified on the
others.

## Guardrails
- Never edit a generated file by hand; change the definition and regenerate (§1, §2).
- Never split Pigeon-generated Dart and native code across packages, and never expose Pigeon-generated types
  in a public API (§1).
- Never mark a native function as a leaf call unless it neither calls back into Dart nor blocks (§2).
- Never invoke a raw compiler from a hook, and never run a downloaded prebuilt library without checking its
  hash (§2).
- Never rely on a native finalizer to release a resource at process exit (§2).
- Versions: each rule names the version of the page or package it was read from. Nothing was built or run
  while writing this block.

## Origin
Rewritten from the Flutter platform-channels page, the Pigeon README, the Dart ffigen and native-assets
skills of the Flutter agent plugins, the Dart site's hooks page and the `dart:ffi` API reference, read
2026-10-08. Meant to be folded into the same-topic section of `flutter-conventions` (platform channels and
native interop, alongside its section 8 error-code point) when the extended version of that block lands; until
then it stands alone so nothing cites a section that is not on the main branch. 🟡: never run by us; open
points are in [`references/origin.md`](./references/origin.md).
