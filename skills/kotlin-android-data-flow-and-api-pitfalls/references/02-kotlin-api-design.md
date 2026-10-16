# kotlin-android-data-flow-and-api-pitfalls §2 — Kotlin API design

Source: the kotlin-api-design skill and its three references (function ownership, value classes, multiplatform
boundaries) of the chrisbanes skills repository (Apache-2.0, commit f8703a3, read 2026-10-16), rewritten.

## 2.1 Function ownership
1. **Put a function on the smallest accurate semantic owner.** An extension changes the call shape, not who owns
   the behaviour.
2. **An extension on a string, primitive, collection, flow, framework or third-party type needs all of**: a narrow
   private or internal scope that is cohesive, validity for every receiver value, no policy, state, I/O or
   dependency, clearly better receiver syntax, and no better project-owned owner. One failure forbids it.
3. **Pick by meaning**: project-owned intrinsic behaviour is a member; a stateless operation between peers with no
   single owner is a top-level function; construction or parsing is a factory on the target type or a named
   top-level function; retained policy, state, I/O, clock, locale or dependencies belong to an injected
   collaborator; only a type-native operation that passed point 2 is an extension.
4. **Not reading instance state is not evidence that a function belongs at file scope.** Keep an intrinsic
   private member where it is.
5. **When moving a function, update calls and imports and keep or deprecate the old public entry point**,
   unless the release is explicitly breaking. If an interface member changes, check implementers as well as
   callers: a deprecated forwarding extension does not keep source compatibility there.
6. **Check nullable receivers, generics and the rule that a later member wins over an extension** before adding
   one; compile and test.
7. **A public mapping over a sealed result names every caller-visible outcome.** A catch-all branch that hides a
   subtype is flagged, because explicit branches keep the contract exhaustive and the smart casts.

## 2.2 Value classes and data classes
1. **A single field with domain meaning (an identifier, an email address, a percentage) is an inline value
   class**; a single field with no domain meaning stays the primitive or a type alias; several fields are a
   data class.
2. **Keep a data class when equality must differ from the wrapped value's.** A value class delegates equality to
   the underlying type, so a wrapper meant to compare case-insensitively cannot be one.
3. **Check the contract before changing the type**: serialization (a serialisable data class encodes as an
   object, a value class as the wrapped value), callers that use copy or destructuring, Java and reflection
   boundaries (Java sees the underlying type; generic and `Any` uses box), and nullable, generic or vararg hot
   paths (they box, so measure first). A value class cannot have a constructor body, a late-initialised
   property, a delegated property or a backing field beyond the constructor value.
4. **For Compose stability, a value class is the better fix than an `@Immutable` wrapper added only to tell
   types apart**, after confirming the underlying type is stable. Never change a public serialisation or API
   contract just to silence a report.
5. **Do not replace a clear multi-field data class with bit-packing** unless profiling shows allocation cost.

## 2.3 Multiplatform boundaries
1. **Keep common APIs semantic and put platform mechanics behind a small `expect` and `actual` declaration or
   an interface.** The common name describes the capability (the current region), not the platform route to it.
2. **Use `expect` and `actual` for simple compile-time specialisation; use a common interface when callers need
   fakes, injected dependencies, runtime choice or lifecycle ownership.** An operation that needs an activity or
   a view controller is the second kind, and a generic context often hides that lifecycle.
3. **Keep business branching in common code**; an actual or a binding only translates.
4. **Reject platform types in common signatures** (a context, an activity, a resource id, a platform URI, a
   bundle, a view controller, a platform permission enum), a one-platform parameter and a broad platform object.
5. **For shared UI, keep platform-specific composables at the leaves, pass the modifier through every expected
   composable that emits UI, hide native view lifecycle inside the actual and keep side effects in lifecycle-aware
   effects with stable keys.** If a third platform forces a change in common callers, return to the choice of
   boundary.
6. **Define what a suspend platform call promises**: a share sheet launched is not the same as sharing completed.
7. **Compile every affected source set and test common code with a fake** where possible.
