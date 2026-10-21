# kotlin-multiplatform-pitfalls §2 — Runtime, interop and delivery

Source: own craft knowledge, with the points marked "Kotlin docs" checked on 2026-10-20 against the Kotlin documentation (Apache-2.0 repository, rewritten in our words, nothing copied). Runtime and interop behaviour is to be re-read in the documentation of the versions in use.

## 2.1 Coroutines and threads
1. **Inject dispatchers and scopes into shared classes.** A class that picks the main dispatcher itself cannot be tested without a platform main thread and carries a platform assumption into common code.
2. **Symptom: a crash on iOS when a callback lands on a background thread, or UI updates from the wrong thread.** Cause: a result delivered on a worker dispatcher reaches platform UI code. Fix: switch to the main dispatcher at the edge where state reaches the UI.
3. **The current memory model allows sharing objects across threads, but a shared mutable object still needs synchronisation.** Use a mutex, a single-threaded dispatcher, or confine state to one coroutine; do not rely on old advice about freezing objects, which belongs to the previous memory model. Kotlin docs: the current native memory manager keeps objects on a shared heap reachable from any thread, with a tracing collector; the page does not mention freezing, and says nothing about synchronising shared mutable state (that part is own guidance). Its leak check is to force a collection and read the heap size; globals are the commonly cited leak source. In unit tests nothing runs the main thread queue, so the main dispatcher needs a test replacement.
4. **Cancellation must be cooperative on every platform.** Tie work to a scope the platform owner cancels (a view model scope on Android, an explicit scope owned by the Swift side), or work continues after the screen is gone.
5. **Do not expose a suspend function or a flow to Swift without a wrapper in mind.** Swift sees them through generated bridges with limits: cancellation, generics and error types do not map cleanly. Kotlin docs: a suspending function becomes a function with a completion handler whose last parameter carries an error; without the throws annotation only the cancellation exception reaches the caller as an error; calling it as an async function from Swift is documented as highly experimental. Offer a small callback or async wrapper at the boundary and test it from Swift.

## 2.2 Swift and Objective-C interop
1. **The exported surface is what the generated framework shows,** and everything public in an exported module is visible. Export only a facade module; keep the rest internal.
2. **Generics, sealed hierarchies, default arguments, inline value classes and extension functions reach Swift in reduced forms** (lost type information, no default arguments, wrapped names). Kotlin docs, generics only: Objective-C has lightweight generics on classes only (not interfaces or functions), a type parameter without a non-null bound gives nullable results, there is no variance, and upper bounds mostly have no effect. Confirmed on the interop page (read 2026-10-20): inline value classes are not supported in the generated header (arguments map to the underlying type or a generic object), extensions on library or interface types become plain functions with an extra receiver parameter, and top-level functions are grouped in a class named after the file. Kotlin collections passed to Swift are converted, which costs time, and the page lists no support for sealed hierarchies or default arguments (nothing said either way; that part stays own guidance). Design the API a Swift developer would call: concrete types, plain functions, explicit parameters.
3. **Kotlin exceptions that cross to Swift are fatal unless declared for it.** Declare which exceptions may cross, or return a result type; never let an unexpected exception reach an iOS caller. Confirmed (Kotlin docs): only exceptions listed in the throws annotation, or their subclasses, become an error object; any other exception reaching Swift or Objective-C is unhandled and terminates the program.
4. **Naming collisions with Objective-C types appear in the framework.** Prefix or rename the public types that clash and keep names stable across releases; renaming is a breaking change for the iOS app. Kotlin docs: two same-named classes from different packages in one framework are renamed by the compiler by an algorithm that is not stable between releases, so rename them yourself; a name attribute sets the Swift name, and overloads whose parameter names clash are called with named arguments.
5. **Check:** open the generated header (or the Swift view of the framework) and call each public entry point once from a small Swift test. Types that look wrong are cheaper to fix now.

## 2.3 Shared UI with Compose Multiplatform
1. **Decide per screen whether the UI is shared.** Shared UI trades platform feel and some native components for one codebase; keep platform-specific screens (camera, maps, payments) native and embedded.
2. **Resources, fonts, text input, accessibility and gestures differ per platform.** Test on a real iOS device for scrolling, keyboard and screen-reader behaviour, not only on the Android emulator.
3. **Check accessibility labels and dynamic type on each platform.** Shared components inherit gaps in both.
4. **Keep platform lifecycle handling at the edge:** back handling, deep links and permission requests are platform events that call into shared state holders.

## 2.4 Build, size and release
1. **The iOS framework build is the slow leg.** Keep the shared module's dependency graph modest, build only the needed architectures in development and all of them in release, and use build caching in the pipeline.
2. **Test each target in the pipeline,** using a macOS runner for the Apple targets. A pipeline that builds only Android ships an iOS app nobody compiled.
3. **Version the shared module with the apps,** and release the apps together when the shared API changes; a shared change that is fine on Android can break the iOS build days later.
4. **Watch binary size and symbol exposure on release builds** and keep minification and stripping options on for the release configuration of each target.
5. **Crash reports need symbolication for Kotlin frames on iOS.** Upload the debug symbols for each release (`mobile-crash-symbolication-pitfalls`), or reports show only addresses.

## Checks
- Dispatchers and scopes are injected; state reaches the UI on the main thread (§2.1).
- Exported surface is a facade, exercised from Swift (§2.2).
- Shared UI decided per screen and tested on a real iOS device (§2.3).
- Every target builds and tests in the pipeline; symbols are uploaded (§2.4).
