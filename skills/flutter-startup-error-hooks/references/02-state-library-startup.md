# flutter-startup-error-hooks §2 — State library startup traps

Riverpod: the documentation sources of the Riverpod repository's site (the pages under the version 3 concepts
folder and the eager-initialisation how-to), read 2026-10-08. Bloc: the lint-rule pages of the Bloc
repository's docs. The block does not require either library; it applies where one is used. Library-neutral
state-holder rules are in `flutter-conventions` §7.

## 2.1 Riverpod automatic retry
1. **Providers are retried automatically when they throw an exception.** By default up to 10 retries with
   exponential backoff from 200 ms to 6.4 s. Errors (Dart `Error` subtypes) and the `ProviderException`
   wrapper are not retried by default: an error signals a bug, and a wrapper means the provider did not itself
   fail.
2. **A future awaited through the provider's `.future` keeps waiting while retries run,** until retries are
   exhausted or the provider succeeds; so a provider that can never succeed shows as loading for the length
   of the retry schedule before the error appears.
3. **Set a retry policy for the app's failure model.** The policy is a function from retry count and error to
   a delay or `null`; `null` stops. It is set on the root scope or container for all providers, or per
   provider. Returning `null` always disables retry. Whether a failure is worth retrying is a decision: a
   provider whose only failure is a local, deterministic one (a corrupt local database, a missing file) gains
   nothing from retrying and hides the failure behind the loading state (own guidance; the documentation
   explains the mechanism, not this judgement). Disabling retry on a provider also stops dependents of it,
   per the same page.
4. **If failures reach the user fast, the screen needs the error and retry controls** in `flutter-conventions`
   §4 and `flutter-four-async-states`; an automatic retry and a user retry are different policies there.

## 2.2 Eager initialisation
1. **Providers are lazy.** A provider that must exist before the first screen is read at the root.
2. **The documented way:** watch it in a small consumer placed directly under the scope that returns its child
   unchanged. Because the consumer returns the child it was given instead of building the app itself, the
   child does not change when the consumer rebuilds, so only that small widget rebuilds.
3. **Put the consumer in a public widget near the app root** so tests get the same behaviour, instead of
   having the initialisation logic live in `main` (the how-to's own note).
4. **Loading and error states of an eagerly initialised provider** are handled in that same consumer (return a
   loading indicator in place of the child); for the rest of the tree the documentation suggests reading the
   already-resolved value rather than re-handling loading and error everywhere.

## 2.3 Cleanup and experimental APIs
1. **Cancellation, closing streams and similar teardown go in the provider's dispose callback,** which runs
   when the state is destroyed, including when the provider is recomputed. The callback must not trigger side
   effects or modify other providers; register one callback per disposable object.
2. **The mutation API is documented as experimental:** its page says it may change in a breaking way without a
   major version bump. Do not build shared infrastructure on it.

## 2.4 Bloc and Cubit surface
Three lint rules in the Bloc repository's lint package state the public surface; each is a documented rule of
that package (the void-return rule since version `0.2.0-dev.2` of the lint package).
1. **A Cubit's public methods return `void`.** The caller learns the outcome through the state.
2. **A Bloc has no public methods:** it is driven by adding events, and a wrapper method over the add call is
   not needed.
3. **Neither exposes public fields:** state is read from the state object.
These match `flutter-conventions` §7's state-holder rules and serve as a lint-backed check of them.
