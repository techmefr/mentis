# compose-correctness §2 — Flows and phases

Android developer documentation on Compose state, phases and performance, with two Apache-2.0 performance
skills for the details. `collectAsStateWithLifecycle` lives in `androidx.lifecycle:lifecycle-runtime-compose`
and needs version 2.6.0 or later.

## 2.1 Collecting a flow
1. **Collect a flow from outside the composition with `collectAsStateWithLifecycle()`.** The documentation
   calls it the recommended way to collect flows on Android: it ties collection to the lifecycle so the
   app conserves resources. A plain `collectAsState()` keeps collecting while the app is in the background;
   it is for platform-agnostic code, where the lifecycle-aware version is not available.
2. **The default minimum state is `STARTED`.** Use `RESUMED` only for a widget that must collect only
   while it has input focus. Do not use `CREATED`, which leaves collection running while the screen is not
   visible.
3. **Provide an initial value for a cold flow or a `SharedFlow`;** a `StateFlow` supplies its own.
4. **Collect at the caller and pass the value down,** not the flow. A composable that takes a `Flow`
   parameter leaves the collection lifecycle unclear: the flow is recreated on recomposition unless the
   caller remembers it (a practitioner rule from one performance skill).
5. **For a flow that emits many times per frame,** apply `conflate()` and `distinctUntilChanged()` upstream,
   inside a `remember` keyed on the source so the chain is not rebuilt, so the UI only sees changes that
   matter. `distinctUntilChanged` needs a correct `equals` on the emitted type.

## 2.2 Read fast-changing state as late as possible
1. **Compose has three phases per frame: composition, layout, draw.** A state read in a phase invalidates
   that phase and the ones after it, so a read in composition re-runs the most code. The performance
   documentation says to defer reads as long as possible by moving the read into a lambda so it happens only
   when needed.
2. **Use the lambda form of a modifier for a value that changes every frame.** `Modifier.offset { ... }`
   reads in layout where `Modifier.offset(x = ...)` reads in composition; `Modifier.graphicsLayer { ... }`
   (alpha, scale, rotation, translation) and `Modifier.drawBehind { ... }` read in draw. The documentation's
   example is a collapsing toolbar where the scroll offset is passed as a lambda so the read happens in the
   layout phase, and a colour read moved to `drawBehind`. A modifier with only a value form (`padding` has no
   lambda overload in the performance skill's table) needs a custom layout instead.
3. **Pass a hot value across composables as a `() -> T` provider,** and call it inside the lambda modifier
   at the bottom. Passing the plain value forces every composable on the way to recompose when it changes.
4. **Do this only for state that changes more than once per interaction.** For a value that changes on a
   click, the lambda form buys nothing and adds noise.

## 2.3 Backwards writes
1. **Never write to a state that has already been read in the same composition.** The documentation calls
   this a backwards write: the runtime sees a stale read, schedules another recomposition, and can loop
   every frame without end.
2. **Write state in response to an event,** in a lambda such as `onClick`, never in the body of a composable.

## 2.4 Checks
- Background the app: logs from the upstream repository stop within a frame and resume on return.
- During a scroll or animation the parent composable's recomposition count does not climb; only layout or
  draw counters do.
- Grep for `collectAsState(` in Android code, and for `Flow<` in a composable's parameter list.
- Grep for `.value` reads inside a composable body that feed `Modifier.alpha`, `rotate`, `scale`, `offset(`.
