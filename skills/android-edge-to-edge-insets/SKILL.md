---
name: android-edge-to-edge-insets
description: "Use when an Android app draws edge-to-edge or its content is hidden, doubled-padded or clipped by system UI: enabling edge-to-edge before setContent, the Android 15 and Android 16 enforcement and the opt-out that no longer works, windowSoftInputMode adjustResize, applying Scaffold padding and consuming it, system bar and navigation bar contrast and icon colours, IME insets applied twice, imePadding placed after verticalScroll, WindowInsetsRulers and fitInside, adaptive scaffolds that do not pass padding, Material 2 app bars, list content padding versus parent padding, full-screen dialogs, and orientation and resizability restrictions that are ignored on large screens."
---

# android-edge-to-edge-insets

Step 6 of the pipeline (`WORKFLOW.md`), for the Android window bugs that a phone in portrait with the keyboard closed
never shows: the field covered by the keyboard, the button under the navigation bar, the padding that is applied
twice, the layout that breaks on a tablet. The four sections share one premise: **since Android 15 the app draws
behind the system bars whether or not the code was written for it, so every screen has to say which insets it
consumes and which it leaves to a parent, and "I padded it somewhere above" is the sentence that produces both
the gap and the double gap**. The Compose state and effects rules are in `compose-correctness`; theming, design
and navigation structure are out of scope here, and so is the classic View system.

## When
- Moving an app to target Android 15 or later, or retargeting to Android 16 or 17.
- A text field is hidden by the keyboard, content sits under a system bar, or a bar's background does not reach the
  edge of the screen.
- Adding a `Scaffold`, a bottom bar, an adaptive scaffold, a full-screen dialog or a screen with a text field.
- A tablet, a foldable or a resizable window looks stretched, or the orientation lock stops working.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Window setup: enabling edge-to-edge, enforcement by target SDK, the manifest keyboard mode, bar contrast and icon colours, full-screen dialogs | an Activity is created or edge-to-edge is enabled, or a bar looks wrong | [`01-window-setup.md`](./references/01-window-setup.md) |
| 2 | Applying insets once: Scaffold padding, padding modifiers and consumption, Material 2 bars, adaptive scaffolds, lists, rulers | content is hidden, or padding appears twice | [`02-applying-insets.md`](./references/02-applying-insets.md) |
| 3 | The keyboard: `adjustResize`, `imePadding` and its order, scaffolds with and without IME insets, rulers for the IME | a screen has a text field | [`03-keyboard.md`](./references/03-keyboard.md) |
| 4 | Android 16 and 17 window behaviour: orientation and resizability ignored on large screens, the removed opt-outs | the target SDK is raised, or a layout is wrong on a tablet or a foldable | [`04-android-16-17-window-changes.md`](./references/04-android-16-17-window-changes.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: the app was run with gesture navigation and with three-button
navigation (§1), every screen with a text field was opened with the keyboard up and the last field was visible and
scrollable (§3), a list was scrolled to its ends and its first and last items cleared the bars (§2), and for a
retarget the app was rotated with the keyboard open and run in a window at least 600dp wide (§3, §4). A screen that
was only previewed is not verified.

## Guardrails
- Never add IME padding under a parent that applied the IME insets without consuming them (§3.2).
- Never put the vertical scroll before the IME padding in the modifier chain (§3.2).
- Never pad a list's parent with system insets; give the list its own content padding (§2.4).
- Never wrap an adaptive scaffold in a safe-drawing padding modifier (§2.3).
- Never rely on a manifest orientation or resizability lock for a target of Android 16 or later on a large screen
  (§4.1).
- This block states Android behaviour as of the Android developer pages read on the date in
  [`references/origin.md`](./references/origin.md); the pages show "last updated 2026-10-01" and each rule names the
  API level or target SDK where the page does. Nothing was built or run while writing it.
- Raising `targetSdk`, `compileSdk` or a library version is the user's step; this block names it and stops.

## Origin
Rewritten from the Android developer pages on window insets in Compose, edge-to-edge setup and system bars, the
WindowInsetsRulers page and the Android 15, 16 and 17 behaviour-change pages, and from one Apache-2.0 Android agent
skill on edge-to-edge (read 2026-10-08). 🟡: never run by us; meant to be folded into the same-topic block
(`kotlin-android-conventions`, or a Compose reference next to `compose-correctness`) when PR 118 lands; open points
are in [`references/origin.md`](./references/origin.md).
