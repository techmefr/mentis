# angular-signals-rxjs-ssr-pitfalls §5 — DI tokens, app initializers, typed forms, updates

Four small areas where Angular has one right primitive and an older or hand-rolled alternative that fails
quietly.

## 5.1 Injection tokens
1. **Use an `InjectionToken` for any non-class dependency** (configuration, a primitive, a function, an
   interface). Giving it a `factory` makes it provided in root by default, so it needs no entry in a providers
   array, and the factory can itself call `inject()` for its dependencies.
2. **Define a token once and import it everywhere.** Angular matches providers to injection points by the token
   object, not by its description. Two tokens with the same description are different tokens, and an injection point using the
   second cannot see the value provided for the first.
3. **Keep `inject()` calls at the top of the class** (§4).

## 5.2 App initializers
1. **Use `provideAppInitializer()` for work that must finish before the app starts** (loading configuration or
   language data). The function runs in an injection context; if it returns a Promise or an Observable,
   initialisation waits for it.
2. **`APP_INITIALIZER` is deprecated since Angular 19.** The new function is the replacement, built on the same
   mechanism.

## 5.3 Route data as inputs
1. **Enable `withComponentInputBinding()` in `provideRouter`** to receive resolved route data directly as
   component inputs, with `input()` or `input.required()` named after the resolver keys, instead of reading
   `ActivatedRoute` by hand.

## 5.4 Typed forms
1. **Make controls `nonNullable` when `null` is not a valid value.** A plain control resets to `null`; a
   `nonNullable` control resets to its initial value. The option changes runtime behaviour of `reset()`, so
   flip it deliberately on an existing form.
2. **`NonNullableFormBuilder` removes the boilerplate.** `fb.nonNullable.group({...})`, or inject
   `NonNullableFormBuilder`, marks every control.
3. **A disabled control disappears from `group.value`,** which is therefore typed as a `Partial` of the group,
   so each member may be `undefined`. Handle that case in the code that reads it.
4. **Reactive forms do not refresh a zoneless view on their own** (§3).

## 5.5 Updating Angular
1. **Update one major version at a time.** From a version more than one major behind, update to the next major,
   then the next. `ng update` works from a version within one major of the target, and the target must still be
   supported.
2. **Let `ng update` run the migrations,** and follow the interactive update guide for manual steps between the
   two versions.
3. **Never force the update past peer-dependency conflicts;** resolve them. Forcing is a recommendation of one
   MIT skill set, not of the Angular documentation, which says nothing on the flag.

## Verification
- Start the app with the token provided in one place only and inspect that no injection error appears (§5).
- After an update, run the build and the tests before the next major (§5).
