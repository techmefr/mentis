# angular-signals-rxjs-ssr-pitfalls §3 — Zoneless

Without zone.js, Angular no longer learns that "something async happened" from patched browser APIs. It
refreshes a view only when a notification reaches it, so state changed any other way leaves the screen stale
without an error. The documentation states zoneless is the default from Angular 21; on version 20 it is
enabled with `provideZonelessChangeDetection()`. Check the version in use before applying this section.

## 3.1 Removing zone.js
1. **Remove it from the build as well as from the bootstrap.** zone.js is normally loaded through the
   `polyfills` option of both the `build` and `test` targets in the workspace configuration; remove `zone.js`
   and `zone.js/testing` from both. A project with an explicit polyfills file removes the two imports there.
2. **Then drop the dependency.** The package is no longer needed once it is out of the build.
3. **Make sure nothing still overrides the default,** such as a call to `provideZoneChangeDetection` in the
   bootstrap providers.

## 3.2 What notifies Angular
1. **These trigger a refresh:** `markForCheck` (called by the async pipe), `ComponentRef.setInput`, updating a
   signal read in a template, bound host or template listener callbacks, and attaching a view that one of
   those marked dirty. State changed any other way is invisible.
2. **`OnPush` is the recommended step towards zoneless** for application components, not a requirement. A
   `Default` component works as long as it notifies through one of the mechanisms above. A library component that
   hosts user components created with `ViewContainerRef.createComponent` cannot use `OnPush`, because the
   hosted component may still rely on zone.js.
3. **`NgZone.run` and `NgZone.runOutsideAngular` stay.** They are compatible with zoneless, and removing them
   can regress libraries used by apps that still run zone.js.

## 3.3 Stability hooks that go silent
1. **Remove `NgZone.onMicrotaskEmpty`, `NgZone.onUnstable` and `NgZone.onStable`.** They never emit in a
   zoneless app. `NgZone.isStable` is always `true`, so it cannot gate code.
2. **Replace "wait for Angular to finish" with a render hook.** `afterNextRender` for a single change
   detection, `afterEveryRender` when a condition may span several rounds.
3. **Or wait on the DOM directly.** Where the code only needs a DOM state, `MutationObserver` is more direct
   than a render hook.

## 3.4 SSR needs PendingTasks
1. **Server rendering used zone.js to learn when the app is stable.** Without it, async work that must finish
   before serialisation has to be registered with the `PendingTasks` service. Serialisation waits for the first
   moment no task is pending.
2. **Use `run` for the common case,** which wraps an async function; use `add` and the returned cleanup (in
   `finally`) when the shape is more complex.
3. **For an Observable, `pendingUntilEvent()` from the interop package** keeps the app unstable until it
   emits, completes, errors or is unsubscribed.
4. **The framework already registers its own work,** such as an ongoing navigation or an incomplete
   `HttpClient` request; only your own async work needs it.

## 3.5 Reactive forms
1. **Form model updates do not schedule change detection.** `setValue`, `patchValue` and `FormArray.push`
   update state and emit form observables, but no refresh follows.
2. **Connect the form to a notification:** `markForCheck()` from a `valueChanges` subscription, or reflect the
   data through signals the template reads.

## 3.6 Tests
1. **`TestBed` is zoneless by default,** even when zone.js is loaded; add `provideZoneChangeDetection()` to the
   test providers to get zone behaviour.
2. **Prefer `await fixture.whenStable()` to `fixture.detectChanges()`** in new tests. Forcing detection hides a
   missing notification the production app would not get. Existing suites that use `detectChanges()` are not
   worth mass conversion.
3. **A component that changes template values without a notification throws
   `ExpressionChangedAfterItHasBeenCheckedError` in the test.** Fix a production component with a signal or
   `markForCheck`. A test-only wrapper may call `fixture.changeDetectorRef.markForCheck()`.
4. **`provideCheckNoChangesConfig({exhaustive: true, interval})`** checks periodically for bindings updated
   without a notification and throws the same error. It is a debugging aid.

## Verification
- Start the app with zone.js removed from both build targets and complete an async flow (a request, a timer, a
  form update); the screen must reflect the result (§3).
- Grep for `onStable`, `onMicrotaskEmpty`, `onUnstable` and `isStable`; no remaining use as a gate (§3).
- Server-render a page whose data comes from a custom async call; the HTML must contain the result (§3).
