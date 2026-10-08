# swiftui-correctness: origin and source stamps

> Provenance of `skills/swiftui-correctness`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run on a real SwiftUI app by us. No project was
built, no preview was rendered and no Instruments trace was recorded while writing it.

**Fold-in note.** This block is meant to be folded into `swift-conventions` (new references, or an extended
section on views) when PR 118 lands and the Swift blocks are consolidated. It is standalone only so that it does
not depend on a block that is not yet on main.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Apple developer documentation pages for `State`, `Bindable`, the `Observable` macro, `ForEach`, `NavigationStack`, `navigationDestination(for:destination:)`, `sheet(item:)`, `AnyView`, `task`, `onAppear`, `onChange`, `animation(_:value:)`, `cornerRadius`, `foregroundStyle`, `Button`, `LabelStyle` (icon only), `accessibilityLabel`, `onTapGesture`, `dynamicTypeSize`, `accessibilityReduceMotion`, `Text`, `LocalizedStringKey`, `containerRelativeFrame`, `safeAreaInset`, `@Entry`, and the SwiftData CloudKit sync page | Apple proprietary (facts only, rewritten) | §1.1 points 2 to 3, §1.2 points 1 and 4, §1.3 point 1, §2.1 points 1 and 2, §2.2 point 1, §2.5 point 1, §3.2 point 1, §3.3 point 3, §3.4 point 3, §4.1, §4.2 points 2 and 3, §4.3 point 1, §4.4 points 5 and 6 |
| An MIT-licensed SwiftUI review skill (modern API, views, data, navigation, performance, accessibility, localisation, resizability and hygiene references) | MIT (LICENSE read, copyright 2026) | every remaining rule, including the iOS 27 and Xcode 27 points |
| A second MIT-licensed SwiftUI skill (SKILL.md and its correctness checklist) | MIT (LICENSE read, copyright 2026) | corroboration of the state, identity, environment and display-scale rules |

Apple pages were read through the documentation JSON that backs developer.apple.com, so only the prose was
available; code samples and link text inside sentences were not.

## Rewrite notes
The first MIT skill is written as an instruction to a reviewer and asserts several rules with "always" and
"never". Each was kept only where an Apple page, the second skill or the rule's own reasoning supports it, and
the reason is given in the rule. The skill's project policy (default to the newest iOS, avoid UIKit, no
third-party framework without asking, one type per file) is not general and was left out apart from the extraction
rule in §3.3.

## Not verified
1. **iOS 27 and Xcode 27 API names and behaviour** (`ToolbarOverflowMenu`, `visibilityPriority`,
   `topBarPinnedTrailing`, `alert(_:item:)`, `@ContentBuilder`, the `@State` macro keeping a private initial
   expression, `AsyncImage` HTTP caching, the missing launch screen rejection, `UIRequiresFullScreen`) come from
   one MIT skill; the Apple pages read confirm the `@State` macro exists from Xcode 27 and nothing else here.
2. **`-LogForEachSlowPath`** is named by the MIT skill; the Apple `ForEach` page says a launch argument exists
   and does not give the name in the text read.
3. **`ForEach` over `enumerated()` directly** needs a conformance the MIT skill gates to iOS 26; not checked
   against the SDK.
4. **A `confirmationDialog` attached inside a `ToolbarOverflowMenu` never appears** is a statement of the MIT skill
   only.
5. **SwiftData property defaults.** "A default value or optional" is from the MIT skill; the Apple page read lists
   unique constraints, non-optional relationships and the deny delete rule.
6. **`scrollTransition`, `visualEffect`, `@Animatable` and `@ScaledMetric` behaviour** was not read on Apple pages.
7. **Dropped from the source list:** the folding-phone material (reserved regions, `ArrangementView`, vertical
   toolbars, hinge angle: iOS 27.1 only and unconfirmed on any Apple page), Liquid Glass adoption, Swift Charts
   and Instruments trace recording and analysis, "doc comments on public declarations" (conflicts with the house
   rule on comments), "unit tests for core logic" (covered elsewhere), the 90/8/2 test ratio, and a third MIT
   skill collection that was not read.
8. **Written by us, not sourced:** the checkpoint in Output and the wording of the guardrails.

## Related blocks
`compose-correctness` (the same premise on Android: a UI function that can run at any time), `accessibility`
(web only, the shared RGAA reasoning), `testing-anti-patterns`.
