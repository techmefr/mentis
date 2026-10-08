# swiftui-correctness §2 — State and data flow

Apple documentation pages for `State`, `Bindable`, the `Observable` macro, `onChange`, `@Entry` and the SwiftData
CloudKit sync page, with two MIT-licensed SwiftUI review skills for the rules the pages do not state. The
`@Observable` approach needs iOS 17 or later; points about Xcode 27 are marked.

## 2.1 Owning state
1. **Declare view-owned `@State` as `private`, in the highest view that needs it.** The Apple page says why:
   a non-private property can be set through the memberwise initialiser, which conflicts with the storage
   SwiftUI manages. Share it down as a read-only value, or as a `Binding` when the child must write.
2. **A `@State` default is evaluated whenever SwiftUI instantiates the view,** so the page warns against side
   effects and heavy work in it, and recommends deferring creation of an expensive object until the view appears.
   With Xcode 27 `@State` is a macro (the Apple page says so), and an MIT skill states it then keeps a private property's initial
   expression for one-time evaluation; a non-private property is evaluated again whenever the parent rebuilds
   the view. Recommend privacy for existing state, but do not change it unasked: a caller may supply the value
   through the initialiser.
3. **Give each `@State` property exactly one initial value.** If `init()` assigns it, leave the declaration without
   an initial expression and assign once; both together can fail to compile on Xcode 27, and where it compiles the
   declaration's value wins.
4. **Do not copy a parent's changing input into `@State`** as if it tracked the parent. State is storage local to
   the view; an input that changes belongs in a property or a binding, and an intentional one-time seed is stated
   as such.
5. **An expensive reference that is not observable can live in `@State` as a cache** (an image-processing
   context, say): it persists across updates and is not tracked.

## 2.2 Observable models
1. **Share data with `@Observable` classes, owned with `@State` and passed with `@Bindable` or `@Environment`.**
   The page's contract: a view re-evaluates when a property it reads in its body changes, not when another
   property of the same object does.
2. **Mark an `@Observable` class `@MainActor`** unless the project makes main-actor isolation the default. A
   model without it is a finding.
3. **Prefer `@Observable` to `ObservableObject`, `@Published`, `@StateObject`, `@ObservedObject` and
   `@EnvironmentObject`,** which stay only where unavoidable or in legacy integration. Code that must keep
   `ObservableObject` (for a Combine debouncer, say) imports Combine itself; SwiftUI no longer re-exports it.
4. **Observation tracks stored properties.** Reading a computed property records every stored property its getter
   reads, so a getter does not narrow a dependency. A stored struct is one dependency: reading
   `library.book.title` also subscribes to changes of `library.book.pageCount`. To narrow it, split the fields
   into stored properties or make the nested model observable; do this when an update storm is measured, not by
   reflex.
5. **Give custom value types stored in an observable class `Equatable` conformance** so assignments equal to the
   current value do not notify. Structs and enums with associated values need explicit conformance; an array is
   equatable only when its elements are.

## 2.3 Bindings
1. **Prefer a binding projected from `@State`, `@Binding` or `@Bindable` (including key paths) to
   `Binding(get:set:)` in a body.** A closure binding adds allocations and comparison problems that cause needless
   updates. For a conversion or a lookup, expose a writable computed property on the model (`$model.distanceInMiles`)
   or a labelled subscript.
2. **A setter and `onChange()` are not interchangeable.** A binding's setter handles every write through it,
   equal-value writes included; `onChange()` responds to value changes, including programmatic ones. Moving a side
   effect from one to the other changes when it runs, so check before refactoring, and leave a custom binding alone
   when the replacement is unclear.
3. **Bind a numeric `TextField` to a numeric value with a format,** `TextField("Score", value: $score, format: .number)`,
   and add the keyboard type as well; the keyboard modifier alone does not make the field numeric.

## 2.4 Storage and scenes
1. **Never use `@AppStorage` inside an `@Observable` class,** even marked `@ObservationIgnored`: a change then does
   not update views. Use it in the view, or read and write the store from the model and expose a stored property.
2. **Never keep secrets in `@AppStorage` or `UserDefaults`.** Use the keychain.
3. **Keep window-specific UI state in the scene root `@State` or `@SceneStorage`** (active tab, displayed record,
   navigation path). In an app with several scenes, `@AppStorage`, singletons and shared observable models couple
   separate windows, which must be able to navigate independently on iPad and on a folding phone.

## 2.5 Environment values
1. **Create custom entries with the `@Entry` macro** on an extension of `EnvironmentValues` (the same macro serves
   focused values, transactions and container values) instead of a hand-written key type with a default.
2. **An `@Entry` default must stay equal across reads.** A new reference instance, `.now` or `UUID()` as the
   default produces a different default each time, and every reader updates on unrelated environment changes.
   Use an optional entry with no explicit default, or a shared `static let`. Xcode 27 diagnoses reference-type
   defaults but misses some changing value types, and adding `Equatable` does not stabilise a changing value.
   Constant defaults (`true`, `1`, `.orange`) are fine.
3. **Do not put a closure in an environment or focused value.** A stored closure cannot be compared, so readers
   update without a meaningful change (Xcode 27 warns); wrapping it in a struct changes nothing. Pass a struct or
   an `@Observable` object holding the data and a method, optionally `callAsFunction()`. System actions such as
   `\.dismiss` and `\.openURL` need no replacement.
4. **Remove key-path `@Environment` and `@FocusedValue` properties the view never reads:** the declaration alone
   subscribes the view. An unused type-based declaration costs nothing at runtime but is dead code.

## 2.6 SwiftData with CloudKit sync
1. **The Apple sync page lists what CloudKit cannot support:** unique constraints, because changes are synchronised
   concurrently and CloudKit cannot enforce them; non-optional relationships, because the servers do not guarantee
   atomic processing of relationship changes, so every relationship is optional; and the deny delete rule.
2. **Set a relationship's inverse explicitly** when SwiftData cannot infer it reliably, before saving, because
   CloudKit processes changes in an indeterminate order.
3. **Give model properties a default value or make them optional** (an MIT skill's rule; the Apple page was not read
   for it).
4. **A CloudKit schema is additive once promoted to production:** model types cannot be deleted and existing
   attributes cannot be changed. Initialise the schema during development, in debug builds only, and promote it
   before release.
5. **A count that must stay live is not a fetch count.** `fetchCount()` does not update by itself; a `@Query`
   or another trigger does.
