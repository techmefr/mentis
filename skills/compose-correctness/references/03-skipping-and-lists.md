# compose-correctness §3 — Skipping, stability and lazy lists

Android developer documentation on stability, strong skipping, fixing stability issues and lazy lists. The
stability rules changed with the compiler: strong skipping is enabled by default from Kotlin 2.0.20, and
before that it is an opt-in for a module. Check the Kotlin version first.

## 3.1 What Compose skips
1. **Without strong skipping,** the compiler marks a composable skippable only if all its parameters are
   stable, and compares them with `equals`. A `List`, `Map` or `Set` parameter is unstable, because the
   compiler cannot be sure the collection is immutable, so a composable taking one is not skipped even
   when the contents are the same.
2. **With strong skipping (Kotlin 2.0.20 and later),** every restartable composable becomes skippable, whether
   or not it has unstable parameters. Unstable parameters are compared by instance equality (`===`), stable
   ones by `equals`. So a composable that used to be impossible to skip is now skipped while the same instance
   is passed; a new but equal instance of an unstable type still counts as a change.
3. **Lambdas are memoised under strong skipping,** wrapped in `remember` keyed on what they capture, and the
   documentation notes the common belief that a lambda with an unstable capture is itself unstable is wrong:
   lambdas are always considered stable.
4. **Opt a class back into value comparison with `@Stable`** where new instances of equal objects are created
   each time; the documentation's example is a data source such as a database library that allocates new
   objects for every item of a list whenever one changes. Annotate only when the class really behaves as
   stable: mutable properties must be Compose state.
5. **Prefer immutable collections for what you pass.** The documentation says the compiler treats the
   Kotlinx Immutable Collections as immutable and that the library was still in alpha when the page was
   written, so its API may change. An `@NonSkippableComposable` opts one composable out of strong skipping.
6. **Fix stability only where it is measured.** Enable strong skipping first, the documentation's first step;
   then look at the recomposition counts, and only then restructure types.

## 3.2 Lazy list items
1. **Give every item a stable, unique key.** Without one the item's state is keyed to its position, so an
   item that moves loses its remembered state (a scroll position inside a row, for example). With
   `key = { it.id }` Compose moves the state with the item when the data is reordered.
2. **The key must be a type a `Bundle` can hold** (primitives, strings and similar), because a
   `rememberSaveable` inside an item is saved against it.
3. **Add `contentType` for lists of different item kinds** (Compose 1.2 and later), so Compose reuses
   compositions only between items of the same type.
4. **Do not use the index as the key** for a list that can change; that is the same as no key.

## 3.3 Checks
- Print the stability report for the module (compiler reports) before and after a Kotlin upgrade and
  compare the skippable counts.
- Reorder a list with per-item state: the state follows the item.
- Grep for `items(` and `itemsIndexed(` with no `key =`.
