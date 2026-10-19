---
name: compose-correctness
description: "Use when Jetpack Compose UI code is written or reviewed and the risk is wrong behaviour or needless recomposition: where state lives and how it survives rotation (hoisting, remember versus rememberSaveable, mutable lists as state), choosing LaunchedEffect, DisposableEffect, SideEffect, rememberUpdatedState, derivedStateOf or snapshotFlow, collecting flows with collectAsStateWithLifecycle, reading fast-changing state late with lambda modifiers, backwards writes, composable skipping and stability (strong skipping, unstable collections, @Stable), and lazy list keys and content types."
---

# compose-correctness

Step 6 of the pipeline (`WORKFLOW.md`), for the Compose rules that a screenshot never shows: the state that
is lost on rotation, the effect that holds a stale callback, the animation that recomposes the whole screen
every frame. The three sections share one premise: **a composable can run at any time, in any order, many
times, or be skipped, so it has to be a pure description of state, and everything with a side effect or a
lifetime goes through an API that knows about the composition**. Android lifecycle and ViewModel structure
are out of scope here; naming and design-system rules are too.

## When
- Writing or reviewing a composable that holds state, launches work, listens to something, or animates.
- A screen recomposes more than it should, a list item loses its state on reorder, or a value goes stale.
- Collecting a `Flow` or `StateFlow` in a composable.
- Changing the Kotlin or Compose compiler version, or passing a collection into a composable.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | State and effects: hoisting, remember and rememberSaveable, effect APIs, stale callbacks, derivedStateOf, snapshotFlow | a composable holds state, launches work or registers a listener | [`01-state-and-effects.md`](./references/01-state-and-effects.md) |
| 2 | Flows and phases: lifecycle-aware collection, deferring state reads to layout and draw, lambda providers, backwards writes | a flow is collected, or an animation or scroll value drives the UI | [`02-flows-and-phases.md`](./references/02-flows-and-phases.md) |
| 3 | Skipping, stability and lazy lists: strong skipping, unstable types and collections, `@Stable`, item keys, content type | a composable recomposes needlessly, a list is written, or the compiler version changes | [`03-skipping-and-lists.md`](./references/03-skipping-and-lists.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: the screen was rotated and its user input survived (§1), a
long-running effect was driven with a changed callback and used the new one (§1), the app was backgrounded
and the upstream flow stopped emitting (§2), the recomposition count of the parent composable was read in the
layout inspector during an animation and stayed flat (§2), and a list was reordered with item state intact
(§3). A composable that was only read is not verified.

## Guardrails
- Never use a mutable collection as the state of a composable (§1.1).
- Never pass `Unit` or a constant as the key of an effect to avoid thinking about the keys (§1.2).
- Never run a side effect in the body of a composable (§1.2).
- Never write to a state that has already been read in the same composition (§2.3).
- Never use a list item's position as its identity (§3.2).
- This block states Compose, Kotlin and AndroidX Lifecycle behaviour as of the Android developer pages read on
  the date in [`references/origin.md`](./references/origin.md); the pages carry no Compose version
  number, so each rule names the release it needs where the page does. Nothing was run while writing it.
- Adding a library such as the immutable collections is the user's step, in their own terminal; this block
  names it and stops.

## Origin
Rewritten from the Android developer pages on Compose state, state hoisting, side effects, phases,
performance best practices, lists, stability and strong skipping (last updated 2026-10-01 on the pages read),
and four Apache-2.0 Compose performance skills (derivedStateOf, deferring state reads, flow collection,
effects), read 2026-10-08. 🟡: never run by us; meant to be folded into the same-topic block
(`kotlin-android-conventions`, a Compose reference) when PR 118 lands; open points are in
[`references/origin.md`](./references/origin.md).
