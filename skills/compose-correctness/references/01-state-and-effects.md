# compose-correctness §1 — State and effects

Android developer documentation for Compose state, state hoisting and side effects, with four Apache-2.0
Compose performance skills for the derived-state and effect rules. `remember` and `rememberSaveable` exist
in every Compose release; the lifecycle-aware collection in §2 needs lifecycle-runtime-compose 2.6 or later.

## 1.1 Where state lives
1. **Hoist state to the lowest common ancestor that needs it.** A stateless composable takes its value and
   an event lambda; the caller owns the state. State that is only UI element state (an expanded flag) can stay
   inside the composable, wrapped in `rememberSaveable` if it must survive recreation. Business state lives
   in a state holder or ViewModel, not in the composable.
2. **`remember` survives recomposition, not recreation.** A configuration change or process recreation drops
   it. User input and anything the user would be annoyed to retype uses `rememberSaveable`, which saves
   whatever a `Bundle` can hold or a custom saver.
3. **Never use a mutable collection as state.** An `ArrayList` or `mutableListOf()` is not observable, so
   changing it does not recompose, and the user sees stale data. Hold an observable `State<List<T>>` and
   replace the list with an immutable `listOf` copy.
4. **Use `remember` for expensive work in the body,** keyed on its inputs, so it does not run again on every
   recomposition; a `remember` that reads a parameter without keying on it freezes the first value (§1.4).

## 1.2 Choosing an effect
1. **Composables should be free of side effects,** because recomposition can happen in any order, many
   times, or be discarded. Anything that changes the world (a network call, a navigation, a snackbar, a
   listener) goes through an effect API, called from a controlled place that knows the composable's
   lifecycle. Keep the work in an effect UI-related.
2. **Need a coroutine:** `LaunchedEffect(keys)`. It starts when the composable enters the composition, is
   cancelled when it leaves, and restarts with a fresh coroutine when a key changes. List every value the
   effect reads as a key; `LaunchedEffect(true)` is as suspicious as `while (true)`: it has valid uses, so
   stop and confirm you mean one.
3. **Need setup and teardown with no coroutine:** `DisposableEffect(keys)`, whose last statement is an
   `onDispose { }` that releases what you registered. It runs on key change and when the composable leaves.
4. **Publishing Compose state to code that is not Compose:** `SideEffect`, which runs after every successful
   composition. It is for a thin hand-off, not for work.

## 1.3 A long effect that uses a callback
1. **Wrap the callback in `rememberUpdatedState`** and read the wrapped value inside the effect. Otherwise the
   effect captures the lambda it was launched with, and a new one passed on a later recomposition is
   ignored. The documentation's example is a timeout callback inside an effect that must not restart when the
   callback changes. Compose reads the latest value without restarting the coroutine.

## 1.4 Derived state and what it costs
1. **Use `derivedStateOf` when an input changes more often than the result you need.** The documentation's
   case is a scroll position that changes constantly while the UI only needs a flag for crossing a threshold;
   it acts like `distinctUntilChanged` for state. The documentation also warns it is expensive and should
   only be used to avoid recomposition when the result has not changed.
2. **Do not use it when the output changes as often as the input.** Concatenating two name strings is the
   documented bad example; read them directly.
3. **Wrap it in `remember`,** otherwise a new derived state is created on every composition and nothing is
   filtered.
4. **Key the `remember` on any non-state value the derivation captures** (a parameter, a threshold). A
   captured plain value is read once when the derivation is created and then goes stale.
5. **For a one-off reaction to a derived value** (analytics, a snackbar), use
   `LaunchedEffect(state) { snapshotFlow { ... }.collect { ... } }`, with a `distinctUntilChanged` if the
   value can repeat. The read happens in the coroutine, not in the composition, and the composable does not
   recompose for it. (From one Apache-2.0 performance skill, consistent with the documentation's mention of
   `snapshotFlow` in the side-effects page.)

## 1.5 Checks
- Rotate the screen with text typed in: it is still there.
- Pass a changed callback to a screen with a long-running effect: the new one is invoked.
- Grep for `LaunchedEffect(Unit)` and `LaunchedEffect(true)`: each one is a deliberate choice you can
  explain, or it is replaced by a real key.
- Grep for `derivedStateOf` outside `remember`, and for `mutableListOf` used as composable state.
