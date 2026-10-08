# swiftui-correctness §3 — Identity, structure and performance

Apple documentation pages for `ForEach`, `AnyView`, the `task` modifier and `onAppear`, with two MIT-licensed
SwiftUI review skills for the performance and identity rules the pages do not state. The `enumerated()` rule needs
iOS 26 and the image-cache rule iOS 27; both are marked.

## 3.1 Row identity
1. **Identity comes from the element, never from its position.** In a collection that can insert, delete, move or
   filter, `ForEach(items.indices, id: \.self)` and an `enumerated()` sequence identified by `\.offset` make rows
   inherit whatever now sits at that position, so row state resets and animations break. Fixed ranges and
   constant collections are fine. Prefer `Identifiable` types to `id: \.someProperty`.
2. **Keep the index when you need it,** with `ForEach(items.enumerated(), id: \.element.id)` on iOS 26 and later,
   and `ForEach(Array(items.enumerated()), id: \.element.id)` below that; the direct form depends on a conformance
   gated to iOS 26.
3. **Allocate an element's identity when the element is stored,** not while the body runs. Mapping labels to new
   values inside `ForEach` recreates every row if each initialiser makes a `UUID`. A stored `let id = UUID()` is
   correct when the value itself lives in `@State` or a model across evaluations.
4. **Use a compact, immutable key.** `id: \.self` on a whole struct hashes every field for every row on each
   update; keep it for small unique values (integers, UUIDs, URLs, short strings). Never derive identity from an
   editable field: renaming a caption then replaces the row and loses focus and selection.

## 3.2 A constant number of views per element
1. **Each `ForEach` element must produce the same number of top-level views every time,** normally one. The Apple
   page states why: lazy containers query elements lazily, and a count that varies (an `if` that yields one view or
   none) costs performance. Wrap the condition in a container so the count is constant.
2. **Why it matters in detail (the MIT skill):** with a constant count SwiftUI derives row identity from the element
   ids alone; with a varying count it runs every row's body on each update to find out, a cost that grows with the
   list. A bare `if`, `if`/`else` or `switch` at the top of a row counts as varying even when every branch yields
   one view, because the branch taken becomes part of the identity. A `VStack` around the content fixes it; a
   `Group` does not. To drop elements, filter the collection before `ForEach`. A ternary is right when only
   modifier values differ.
3. **To find offenders, run with the launch argument `-LogForEachSlowPath YES`,** which logs `ForEach` instances
   that produce a non-constant number of views (the Apple page documents a launch argument for this; its name is
   from the MIT skill).

## 3.3 Structure that keeps identity stable
1. **Keep conditional values inside the modifier,** `.opacity(isUnavailable ? 0.4 : 1)`, instead of branching the
   whole view with `if`/`else`. A branch changes structural identity and recreates the platform views each time
   the condition flips.
2. **Never add a `View.if()` helper that conditionally transforms its receiver.** It resets state and disrupts
   animations on every flip. Report an existing helper; remove it only in a requested change, since it may have
   many callers.
3. **Avoid `AnyView`.** The Apple page states that when the wrapped type changes the old hierarchy is destroyed and
   a new one built. Use generics, an extracted `View` struct or a builder closure. `AnyShapeStyle` is not a
   performance concern and is the fix when a style ternary has branches of different types.
4. **Extract subviews as `View` structs, not as computed properties or methods returning `some View`,** and keep
   each in its own file; long bodies are a finding. A handful of small private helper properties that belong to the
   same concern as `body` may stay.
5. **Remove a `Group` that wraps one view** and attach the modifiers to the view; it adds nothing and makes the
   compiler check another type through the chain. Groups with siblings, a `ForEach` or conditional branches
   serve a purpose.

## 3.4 Work in init and body
1. **Keep view initialisers trivial.** Non-trivial work moves to `task()` so it runs when the view is shown.
2. **Assume `body` runs often.** Sorting and filtering that can live elsewhere should, and an expensive inline
   transform in a `List` or `ForEach` initialiser (`items.filter { ... }`) is repeated on every evaluation.
   Derive from the source of truth with `let`, or cache in `@State` only with your own invalidation, or the UI
   goes stale.
3. **Use `task()` for asynchronous work tied to the view.** The Apple page: the task starts before the view
   appears and is cancelled if the view is removed or changes identity before it finishes. `onAppear` has no such
   cancellation, and its action completes before the first rendered frame.
4. **Do not keep formatters as properties to format values.** `Text(date, format: .dateTime.day().month())` and
   `Text(100, format: .currency(code: "USD"))` format without one.
5. **Do not store an escaping builder closure on a view;** store the built view value (`@ContentBuilder let content: Content`
   on Xcode 27, `@ViewBuilder` earlier) and let the synthesised initialiser call the builder.
6. **Use lazy stacks for large data in a `ScrollView`.** An eager stack with many children is a finding.

## 3.5 Rows and frequent changes
1. **Pass each row its element** (`BookmarkRow(bookmark: bookmark)`). Passing a store plus an index or id makes
   the row search the collection, so it depends on the whole collection and one change can update every row.
2. **Create and retain per-row models once.** `BookmarkRow(model: BookmarkModel(bookmark: bookmark))` inside a
   body or `ForEach` closure hands every row a new object on each update.
3. **Keep fast-changing measurements out of the environment:** scroll offsets, geometry, drag points, animation
   progress and timer ticks. Each environment write makes SwiftUI inspect the descendant tree even if nobody
   reads the value. Store the raw value in an `@Observable` object and expose a separate stored result that
   changes less often (`hasReachedEnd`); computing that Boolean inside `body` still subscribes the view to every
   raw update.
4. **Use `scrollTransition()` or `visualEffect()` for scroll-driven fades, scales and rotations;** they avoid
   re-evaluating `body`. Keep state when the position also drives application logic.
5. **On iOS 27, `AsyncImage` honours HTTP caching headers,** including in apps with older deployment targets. Do
   not add an image cache or a dependency only to cache those requests; `AsyncImage(request:)` and a supplied
   session give control on an iOS 27 target.

## 3.6 Restructure only against a measured problem
1. **Treat the deep restructurings as a response to a measured update storm,** not as the default style: passing
   one to three fields of a struct individually instead of the whole value; moving a hot field out of an observed
   struct into its own stored property; caching a computed observable property from `didSet`; extracting a
   small `@Observable` for a slice many views read; a separate observable per row where row fields change
   independently. Reading several properties of one observable object is not itself a reason to split a view,
   because Observation already tracks them individually. A cached property needs every update path maintained, or
   the UI shows stale values.
2. **Do not turn a struct into a class only to avoid comparison cost.**
