# angular-signals-rxjs-ssr-pitfalls §1 — RxJS interop

Signals hold a current value and never notify synchronously; Observables push a stream and need a
subscription. The interop functions bridge the two, and each bridge has one failure mode that shows up as an
`undefined` flash, a leak or a missed value.

## 1.1 toSignal
1. **A signal always has a value; an Observable may not.** Without an `initialValue`, the signal reads
   `undefined` until the first emission, which is the same trade the async pipe makes with `null`. Give an
   `initialValue`, or use `requireSync: true` only for sources that emit synchronously on subscription (a
   `BehaviorSubject`): the option asserts the guarantee and removes `undefined` from the type.
2. **It subscribes immediately.** The subscription may run side effects now, not when the template first reads
   the signal. Call it once and reuse the returned signal; calling it again for the same Observable opens a
   second subscription.
3. **It needs an injection context.** Call it in a field initializer or constructor of a component or service.
   Anywhere else, pass the `Injector` explicitly.
4. **Cleanup is automatic, with an opt-out.** It unsubscribes when the owner is destroyed. `manualCleanup` is
   for Observables that complete on their own.
5. **Errors and completion behave differently.** An error from the source is thrown when the signal is read. Completion keeps the last emitted value. Handle
   expected errors in the pipe (`catchError`) before `toSignal`.
6. **Equal-looking values can still notify.** Consecutive emissions that differ by reference but not by
   meaning re-run every consumer. The `equal` option takes a comparison function and suppresses the update
   when it returns true.

## 1.2 takeUntilDestroyed
1. **Inside an injection context it needs no argument.** A constructor or field initializer of a component,
   directive, service or pipe infers the `DestroyRef`.
2. **Outside one it must receive a `DestroyRef`.** In `ngOnInit`, `ngAfterViewInit` or any regular method the
   call throws the injection-context error (NG0203). Inject `DestroyRef` as a field and pass it:
   `takeUntilDestroyed(this.destroyRef)`.
3. **Prefer it to a hand-made destroy subject.** A subject that is never completed keeps its subscribers; the
   operator is scoped to the owner's lifetime.

## 1.3 toObservable
1. **It reads the signal through an effect, so it is asynchronous.** On subscription the first value may arrive
   synchronously; every later value arrives after the signal stabilises. Several `set` calls in a row emit only
   the last value.
2. **That makes it the right entry for debouncing and for switching to the latest request.** Convert the
   signal, apply the RxJS operators, convert back with `toSignal` if a template reads the result.
3. **It also needs an injection context** or an explicit `Injector`.

## 1.4 rxResource
1. **It is the resource API with an Observable loader.** The `stream` function receives the `params` value and
   returns an Observable; it runs again each time `params` produces a new value.
2. **The stream must emit a value or an error before it completes.** The Angular error reference NG0991
   describes what happens otherwise and how to avoid it; read it when a resource never settles.

## 1.5 State holders
1. **Do not keep component state in a `BehaviorSubject`.** A `signal` is read synchronously, composes with
   `computed`, and needs no subscription management. Use `toObservable` at the edge where an RxJS operator is
   needed.
2. **Keep Observables for what is a stream:** events, debounced input, request cancellation.

## Verification
- Destroy the component (navigate away) and confirm the source has no subscribers left.
- Render the component before the first emission and confirm the screen shows the loading state, not `undefined`.
- Make the source error once and confirm the page degrades instead of throwing at the template read.
