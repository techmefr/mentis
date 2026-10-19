# angular-signals-rxjs-ssr-pitfalls §4 — Signal and template mistakes

These are the mistakes the Angular lint plugin has rules for. They are structural: the code compiles and
usually renders, and the symptom is a condition that is always true, a reactive context that never re-runs,
or a template that thrashes. Run the project's own lint setup on the diff; this section says what each rule
is protecting.

## 4.1 Signals and reactive contexts
1. **Call a signal to read it.** A signal is a function, so `if (mySignal)` tests that the function exists and
   is always true. Write `if (mySignal())`. The same holds in comparisons and logical expressions.
2. **A reactive context must read a signal.** `computed`, `linkedSignal`, `effect` and `afterRenderEffect` re-run
   when a signal they read changes. One that reads none runs once and never again: either a signal call was
   forgotten (`firstName` for `firstName()`), or the value is static and should be a constant, a `signal`, or
   `afterNextRender` for the render-effect case. A helper function or service method inside the context may
   read signals the linter cannot see, so a silent linter does not prove the context is reactive.
3. **A `computed` must return a value.** One that returns nothing is a mistake.
4. **Read without subscribing with `untracked`.** A signal read wrapped in `untracked` is not a dependency of
   the effect; use it for logging or for calling code that reads signals you do not want tracked.
5. **Expose a readonly view of a writable signal.** `asReadonly()` gives consumers the value without a setter.

## 4.2 Lifecycle and injection
1. **Lifecycle hooks are not async.** Angular calls `ngOnInit` and the others and moves on; it does not wait
   for the returned promise, so an `async ngOnInit` suggests a wait that does not happen and the component
   renders with incomplete data. Call an async function from the hook, or use a resolver, a signal or an
   Observable.
2. **Never call a lifecycle method yourself.** `this.ngOnInit()` can run a hook twice or out of order. Share
   logic through a separate method. The one exception is `super.ngOnInit()` in a derived class.
3. **Declare `inject()` calls at the top of the class.** Fields initialise in declaration order, so a field
   above the `inject()` that reads the service sees `undefined`, and the error points at the reader. The
   compiler misses the case where the read hides behind a getter or a method. A helper that wraps `inject()`
   has the same constraint.
4. **`takeUntilDestroyed()` outside an injection context needs a `DestroyRef`** (§1).
5. **Avoid `forwardRef`.** It hides a circular dependency; restructure, use an interface token, or move the
   shared logic to another service.
6. **Avoid developer-preview APIs in production.** They are complete but sit outside the breaking-change policy
   and may change in a patch release.

## 4.3 Templates
1. **Do not negate an async pipe.** The pipe emits `null` before the first value, so `!(x | async)` is true at
   first and can thrash the layout or fire requests for a component that should not show. Test the loaded
   value, or read a signal.
2. **Mind the banana in the box.** Two-way binding is `[(ngModel)]`, parentheses inside brackets. The reversed
   `([ngModel])` is a one-way binding from the template to the component, so typing never updates the value.
3. **Use property binding for dynamic attributes.** `[attr]="value"` over `attr="{{ value }}"`: interpolation
   stringifies and re-parses, binding passes the value. Mixed text such as `alt="Image of {{ name }}"` is fine.
4. **Use `ngSrc` for images** (the image directive) instead of a raw `src`. It lazy-loads, enforces width and
   height against layout shift, generates `srcset` and gives priority hints. `data:` URIs are the exception.
   Image performance more broadly is in `webperf`.
5. **Do not bind `outerHTML`.** It replaces the node Angular holds, so the first render works and the next
   update fails with `NoModificationAllowedError`. To render markup inside the element use `[innerHTML]` (which
   sanitises; untrusted content still needs `security-hardening`); to swap the element use `@if` or `@switch`.
6. **Use the contextual `@for` variables** (`$first`, `$last`, `$even`, `$odd`, `$index`, `$count`) instead of
   hand-rolled index arithmetic, and `@empty` instead of a separate `@if` on the collection length.
7. **Do not declare impure pipes.** An impure pipe runs on every change detection pass, so a list of 100 items
   can call it 100 times per pass. Keep pipes pure.

## Verification
- Run the project's Angular lint configuration over the changed files and fix the structural findings (the
  rules above exist under the same names in the lint plugin).
- For §4 points 1 and 2, change the signal's value in a test and assert the condition or the derived value
  actually changes.
