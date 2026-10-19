# swiftui-correctness §4 — Accessibility, localisation and layout

Apple documentation pages for `Button`, `LabelStyle`, `accessibilityLabel`, `onTapGesture`, `dynamicTypeSize`,
`accessibilityReduceMotion`, `Text`, `LocalizedStringKey` and `containerRelativeFrame`, with two MIT-licensed
SwiftUI review skills for the rules the pages do not state. Rules about `.font(_:scaled)`, the launch screen and
full-screen apps are tied to the iOS 26 and iOS 27 SDKs and marked.

## 4.1 Controls a screen reader can use
1. **A tappable element is a `Button`.** Use `onTapGesture()` only when the tap location or tap count is needed.
   The Apple page says that a control functionally equivalent to a button should be one. When a tap gesture is
   unavoidable, add `.accessibilityAddTraits(.isButton)` or similar so VoiceOver announces it.
2. **A button whose label is an image needs a text label.** Build it with the title-and-symbol initialiser,
   `Button("Add User", systemImage: "plus", action: addUser)`. The Apple page says the convenience initialisers let
   the button adapt in toolbars and menus and help accessibility, and warns against labels made only of images
   with no accessibility label. To keep the icon alone on screen, apply `.labelStyle(.iconOnly)`: the title still
   describes the control to VoiceOver.
3. **Give a `Menu` a text title as well as an icon** (`Menu("Options", systemImage: "ellipsis.circle")`); VoiceOver
   reads the title.
4. **Label images that carry meaning and hide those that do not.** `Image(decorative:)` or `accessibilityHidden()`
   for decoration; otherwise `accessibilityLabel()`. The Apple page adds that the label should not repeat the
   control's trait: "Play", not "Play button".
5. **When a label changes often or is long,** `accessibilityInputLabels()` gives Voice Control a stable name (a
   live price, with the company name as an input label).
6. **Do not rely on colour alone.** When colour distinguishes states, respect `accessibilityDifferentiateWithoutColor`
   and add an icon, pattern or stroke.

## 4.2 Text size and motion
1. **Use text styles, not fixed sizes.** `.font(.body)` and the like follow Dynamic Type. If a custom size is
   required, `@ScaledMetric` scales it up to iOS 18 targets, and `.font(.body.scaled(by:))` is available from
   iOS 26.
2. **Read the text-size setting from `@Environment(\.dynamicTypeSize)`,** whose value reports
   `isAccessibilitySize`, to pick a layout that fits the largest sizes. `sizeCategory` and `ContentSizeCategory`
   are soft-deprecated for this.
3. **When `@Environment(\.accessibilityReduceMotion)` is true, avoid large motion.** The Apple page says UI should
   avoid large animations, especially ones simulating the third dimension; the MIT skill's concrete fix is an
   opacity change instead.
4. **An animated modifier that animates a value uses `@Animatable`,** not the deprecated `AnimatableModifier`;
   chain animations with the `completion` closure of `withAnimation()`, not several calls separated by delays.

## 4.3 Text that can be localised
1. **A string literal in `Text` is a localisation key; a `String` variable is shown verbatim.** The Apple pages for
   `Text` and `LocalizedStringKey` say the literal initialiser looks the key up and a variable avoids
   localisation, which suits user-provided values. To localise a variable on purpose, make a
   `LocalizedStringKey` from it.
2. **Never build text by adding strings or `Text` values.** `Text("Folder: " + name)` produces a plain `String`
   whose literal part is not localised; interpolate: `Text("Folder: \(name)")`. For mixed styles interpolate styled
   `Text` values: `Text("\(red)\(blue)")`.
3. **Store text that will be displayed as `LocalizedStringResource`** in new properties, parameters and enum
   payloads; `Text` shows a plain `String` verbatim and converting one at runtime does not make Xcode extract it.
   Existing parameters typed `LocalizedStringKey` are valid, and retyping stored `String` stays out of unrelated
   work.
4. **Inside a package or framework, name the bundle:** `Text("Reading list", bundle: #bundle)`. `#bundle` also works
   in frameworks where `Bundle.module` does not; with no bundle SwiftUI searches the main bundle and can leave text
   untranslated without any error.
5. **Read locale, calendar and time zone from the environment** (`\.locale`, `\.calendar`, `\.timeZone`); the
   `.current` values ignore preview and per-view overrides.
6. **Let grammar agree automatically** for English, French, German, Portuguese, Spanish and Italian:
   `Text("^[\(count) person](inflect: true)")`. Add translator comments for ambiguous words and explain every
   placeholder.
7. **Keep the project's existing localisation resources.** Moving `.strings` and `.stringsdict` to a String Catalog
   is a requested change, not part of adding a string.

## 4.4 Layout that follows the window
1. **Choose layouts from size classes, not device idiom or orientation.** Read
   `@Environment(\.horizontalSizeClass)` and `\.verticalSizeClass`; neither `UIDevice` idiom nor rotation describes
   the available space on a resizable iPad window or a folding phone. Test `== .regular` for the expanded layout:
   size classes are optional, and `!= .compact` treats `nil` as spacious.
2. **Treat forced size-class overrides as findings;** they stop descendants responding to real window changes.
3. **Rely on SwiftUI's default safe-area insets.** Remove padding that imitates a system inset (a fixed gap for the
   home indicator). Do not substitute `safeAreaPadding()` for a guessed inset; it adds a design margin and is for
   intentional extra space.
4. **Name the edges when content must extend past a safe area:** `.ignoresSafeArea(edges: .top)`. An unqualified
   `ignoresSafeArea()` is for decoration (backgrounds, gradients, scrims); on content it can put text and controls
   under system bars.
5. **Attach pinned bars with `safeAreaInset()`, and with `safeAreaBar()` from iOS 26,** which reserve space as well
   as placing the view. The Apple page for `safeAreaInset` describes the inset growing the safe area of the
   modified view by the content's size.
6. **Prefer `containerRelativeFrame()`, `visualEffect()` or `Layout` to `GeometryReader`** where they can do the
   job. The Apple page for `containerRelativeFrame` defines the size as the nearest container minus any safe area
   insets.
7. **Read display scale from `@Environment(\.displayScale)`,** not from a process-global screen.
8. **Give screens that assume everything fits a scroll view or a `ViewThatFits` fallback** (sign-up, purchase,
   introductions), so bottom actions stay reachable in a short window.
9. **Keep selection and navigation state above a size-class branch.** When size classes choose different view
   hierarchies, state inside the replaced one loses its identity and resets.

## 4.5 SDK facts that fail a release rather than a screen
1. **Declare a launch screen.** The MIT skill reports that App Store Connect rejects iOS 27 SDK builds without one;
   check `UILaunchScreen` in the Info.plist, the generated launch-screen build setting or an existing storyboard
   configuration, and leave project-setting changes to the developer.
2. **Flag `UIRequiresFullScreen`.** With the iOS 27 SDK it no longer prevents resizing, so code that relies on it
   must adapt. Do not remove it unasked.
