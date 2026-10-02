# kotlin-android-conventions §2 — Functions, API shape, errors

> Section 2 of `skills/kotlin-android-conventions`. Read it when a signature, an extension, a factory, an
> exception or a published API is written. The other sections and the guardrails stay in `SKILL.md`.

1. **A property or a function?** A property when the computation does not throw, is cheap (or cached on first
   use) and returns the same result while the object state is unchanged; otherwise a function.
2. **Extension functions are encouraged** for behaviour that works mainly on one object, but keep their
   visibility as narrow as sense allows (local, member extension or private top-level) so they do not pollute
   the public API.
3. **`infix` only for two objects in a similar role,** and never for a function that mutates its receiver.
4. **A factory function does not reuse the class name** unless it has no special meaning; give it a name that
   says why it is special. Several overloaded constructors that cannot be one constructor with defaults become
   named factory functions.
5. **Throw by kind of fault.** A caller-supplied argument that makes the call impossible: the argument
   precondition (throws an illegal-argument error). A wrong object state: the state precondition (throws an
   illegal-state error). A branch that must not be reached: the unreachable helper. Messages say what was
   expected and what was received. Preconditions on nullable values also smart-cast.
6. **Exceptions are unchecked.** Catch only what you can handle or translate; keep the original cause when
   rethrowing another type; release resources with the language's scoped-use function rather than by hand in
   a `finally`. The serious `Error` branch (memory exhaustion, stack overflow) is not something to catch and
   recover from.
7. **A custom exception** extends the most specific standard type that fits and carries the cause.
8. **Library code (a published module) adds three rules:** explicit visibility on every member, explicit
   return and property types (so an implementation change cannot silently change the API), and a doc comment
   on every public member except overrides with nothing to add. This is the one place comments are the
   product, not narration.
