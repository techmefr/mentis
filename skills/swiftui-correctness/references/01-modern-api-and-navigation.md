# swiftui-correctness §1 — Modern API, navigation and presentation

Apple documentation pages for `NavigationStack`, `navigationDestination(for:destination:)`, `sheet(item:)`,
`cornerRadius`, `onChange` and `animation(_:value:)`, with an MIT-licensed SwiftUI review skill for the soft
deprecations and the iOS 27 toolbar rules. Version marks are the source's: iOS 26 and iOS 27 SDKs, Xcode 27.

## 1.1 Soft deprecations compile silently
1. **A clean build does not prove the code uses current API.** Many older SwiftUI declarations carry an
   availability mark that makes them soft-deprecated: Xcode stays quiet. When in doubt, read the symbol's
   `@available` declaration in the SDK, and list soft-deprecated calls in a review even though the compiler does
   not.
2. **Replace these, which the sources name as superseded:**
   - `foregroundColor()` becomes `foregroundStyle()`.
   - `cornerRadius()` becomes `clipShape(.rect(cornerRadius:))` (the Apple page itself says to use a clip shape
     instead).
   - `accentColor()` becomes `tint()`, with the asset catalog's accent colour as the app-wide default.
   - `tabItem()` becomes the `Tab` API.
   - The one-parameter closure of `onChange()` becomes the two-parameter form or the form with no parameter.
   - `animation(_:)` without a value becomes `animation(_:value:)`, which animates only when the watched value
     changes (the Apple page describes exactly that behaviour).
   - `NavigationView` becomes `NavigationStack` or `NavigationSplitView`.
   - `.navigationBarLeading` and `.navigationBarTrailing` become placements that name a purpose
     (`.cancellationAction`, `.confirmationAction`, `.primaryAction`), or `.topBarLeading` and `.topBarTrailing`
     when no role fits.
   - `showsIndicators: false` in a scroll view initialiser becomes `.scrollIndicators(.hidden)`.
   - `overlay()`, `background()` and `mask()` given a view argument take a builder closure instead. Style
     arguments such as `.background(.indigo)` stay.
3. **`colorScheme()` is not replaced by `preferredColorScheme()`.** The latter affects the whole screen or sheet;
   the environment override `.environment(\.colorScheme, .light)` keeps the original scope of the view and its
   descendants.
4. **During feature work, report an unrelated modernisation and do not apply it unasked.** A requested change
   stays the change; the rewrite of surrounding modifiers goes in a separate suggestion.

## 1.2 One stack, one destination per type
1. **Use one `NavigationStack` (or `NavigationSplitView`) per navigation hierarchy** and describe what a data
   type opens with `navigationDestination(for:destination:)`; present it with a link that carries a value of that
   type. A stack can share control of its state when it is built with a binding to an array of values: the stack
   appends and removes entries, and code that edits the array changes what is on screen.
2. **Never mix value links with destination-closure links.** `NavigationLink(destination:)` and
   `navigationDestination(for:)` in the same hierarchy cause problems the source calls significant; pick the
   value form.
3. **Register a destination type once per stack.** Competing registrations of the same type in one stack are a
   finding. Independent stacks, such as one per tab, can each register the same type.
4. **Do not attach `navigationDestination(for:)` inside a lazy container.** Such a container creates children
   only when they are needed to render, so the stack may never see the destination. Attach it outside the
   container (Apple page).

## 1.3 Sheets, alerts and dialogs follow the value, not a flag
1. **A sheet that shows an optional value uses `sheet(item:)`.** The binding is the source of truth: when the item
   is non-nil the sheet shows content built from it, and when the item changes the old sheet is dismissed and
   replaced. This removes the second, separate Boolean that can disagree with the value.
2. **With Xcode 27, an alert or confirmation dialog about one optional value uses `alert(_:item:)` or
   `confirmationDialog(_:item:)`.** The closures receive the unwrapped value and the optional becomes `nil` on
   dismissal. The source states these overloads compile into the app and reach back to iOS 15, or iOS 16 when the
   title is a `LocalizedStringResource`, with no availability check.
3. **Attach a `confirmationDialog()` to the control that triggers it,** so the transition starts from the right
   source. An exception: inside an iOS 27 `ToolbarOverflowMenu` the system owns the menu and a dialog attached to a
   button inside it never appears even though the action runs; attach it to a view outside the menu and drive it
   with state.
4. **An alert whose only button is an "OK" that merely dismisses needs no action closure** at all.

## 1.4 Toolbars on iOS 27
1. **Give toolbar items a purpose, not a side.** Semantic placements let each device position items, including
   a vertical bar that sorts by role. Put related controls (previous and next) in one `ToolbarItemGroup` rather
   than separate items split by fixed spacers; that works on any supported version.
2. **Use `ToolbarOverflowMenu` for overflow actions on iOS 27.** When items do not fit, the system moves them into
   its own overflow menu, and a hand-built ellipsis `Menu` then becomes a nested submenu while
   `ToolbarOverflowMenu` contributes its actions directly.
3. **Set `visibilityPriority` on actions that matter.** Without priorities overflow starts at the trailing end
   regardless of importance. Reserve `.topBarPinnedTrailing` for at most one indispensable action; pinning several
   defeats the adaptive overflow.
4. **Check the toolchain before recommending an API.** Some of these need Xcode 27 or later and a few Xcode 27.2
   with iOS 26.4; a runtime availability check cannot make an older SDK recognise a new declaration. Read the
   project's deployment target first and leave it unchanged.
