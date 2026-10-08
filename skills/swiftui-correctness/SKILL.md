---
name: swiftui-correctness
description: "Use when SwiftUI code is written or reviewed and the risk is wrong behaviour, lost state or needless redraws rather than a crash: soft-deprecated modifiers that compile without a warning, NavigationStack destination registration and mixing value links with destination-closure links, sheets and alerts driven by a Boolean plus a separate value, @State ownership and privacy, @Observable models and their main-actor isolation, Binding(get:set:) in a body, @AppStorage inside a model, environment values that hold closures or unstable defaults, ForEach identity from indices or offsets, a varying number of views per row, conditional-modifier helpers and AnyView, work in init or body, task versus onAppear, SwiftData with CloudKit constraints, icon-only buttons, tap gestures used as buttons, Dynamic Type, Reduce Motion, string concatenation that defeats localisation, size classes versus device idiom, and safe-area handling."
---

# swiftui-correctness

Step 6 of the pipeline (`WORKFLOW.md`), for the SwiftUI mistakes that build cleanly, look right in a preview and are
wrong on a device: a navigation destination registered twice, a view model that is rebuilt on every parent update,
a row that loses its state when the list changes, a button no screen reader can name. The four sections share one
premise: **a SwiftUI view is a cheap value that the framework re-creates at any time, so identity, ownership and
dependencies have to be stated in the types, and the compiler's silence says nothing about whether they are**. A
soft deprecation produces no warning at all. Swift language style and concurrency are out of scope; UIKit and
macOS-only APIs are out too.

## When
- Writing or reviewing a SwiftUI view, a view model that a view reads, or a navigation or presentation flow.
- A list loses row state, scrolls badly or redraws everything on one change.
- Adding a button, an icon, an animation or a piece of user-facing text.
- Moving an app to a newer SDK, or reading a diff that touches modifiers the compiler no longer flags.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Modern API, navigation and presentation: soft deprecations, one stack and one destination per type, item-driven sheets and alerts, toolbar placements | a modifier, a navigation link, a sheet, an alert or a toolbar is written or reviewed | [`01-modern-api-and-navigation.md`](./references/01-modern-api-and-navigation.md) |
| 2 | State and data flow: @State ownership, @Observable models, bindings, storage, environment values, SwiftData with CloudKit | a view owns or reads state, a model is introduced, or a value is passed through the environment | [`02-state-and-data-flow.md`](./references/02-state-and-data-flow.md) |
| 3 | Identity, structure and performance: ForEach identity, a constant number of views per row, conditional modifiers, work in init and body, task, rows and frequent changes | a list or grid is written, a screen is slow, or a view's body grows | [`03-identity-and-performance.md`](./references/03-identity-and-performance.md) |
| 4 | Accessibility, localisation and layout: buttons and labels, Dynamic Type, Reduce Motion, localised text, size classes, safe areas | a control, a piece of text, an animation or a layout that adapts is written or reviewed | [`04-accessibility-localisation-layout.md`](./references/04-accessibility-localisation-layout.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: the screen was run with the target iOS version, a list row was
edited, reordered and deleted with its state intact (§3), the screen was driven with the largest Dynamic Type size
and with VoiceOver reading every control by name (§4), a navigation path was pushed from two places and popped
without a duplicate destination warning (§1), and the strings were checked in a second language (§4). A view that
was only read, or only previewed in one size and one language, is not verified.

## Guardrails
- Never register `navigationDestination(for:)` and link with `NavigationLink(destination:)` in the same navigation
  hierarchy (§1.2).
- Never leave view-owned `@State` non-private, and never give it two initial values (§2.1).
- Never identify rows by index or offset in a collection that can change (§3.1).
- Never put a closure, or a value that changes at scroll or animation speed, in an environment entry (§2.5, §3.5).
- Never use a tap gesture where a `Button` fits, and never ship an icon-only control without a text label (§4.1).
- Never build user-facing text by concatenating strings (§4.3).
- This block states SwiftUI behaviour for the iOS 26 and iOS 27 SDKs as of the Apple documentation pages and the MIT
  skill files read on the date in [`references/origin.md`](./references/origin.md); each rule names the OS or Xcode
  version where its source does. Nothing was built or run while writing it.
- Raising a deployment target, adding a package or editing project settings is the user's step; this block names it
  and stops.

## Origin
Rewritten from the Apple documentation pages for SwiftUI state, observation, navigation, presentation, `ForEach`,
tasks, accessibility and localisation, from two MIT-licensed SwiftUI review skills, and from the SwiftData
CloudKit page (all read 2026-10-08). 🟡: never run by us; meant to be folded into the same-topic block
(`swift-conventions`) when PR 118 lands; open points are in [`references/origin.md`](./references/origin.md).
