# cpp-conventions §3 — Errors and exceptions

> Section 3 of `skills/cpp-conventions`. Read it when a function can fail, when `throw`, `catch` or
> `noexcept` is written, when an error code or an `expected`-style result is returned, or when a constructor
> cannot establish its invariant. Resource release is §2. The other sections and the guardrails stay in
> `SKILL.md`.

**The project's choice comes first.** The core guidelines assume exceptions; one large style guide forbids
them in its own code base, and a code base built without exceptions cannot use a library that throws, and a
library that throws cannot be used from code built without them. Check the build flags and the libraries
before writing any of what follows. Points 1 to 7 are the exception-based discipline; points 8 and 9 are the
discipline when exceptions are not available.

1. **Decide the error-handling strategy early, around invariants.** Decide what an error is, who detects it,
   who reports it and who handles it, before the first function is written; retrofitting one is where code
   bases go wrong. Define the invariant of each class (§4.5) and make errors the cases where an invariant cannot
   be established or a function cannot do its job.
2. **Throw to say "I cannot do my task".** That is the use of an exception: a function that cannot perform
   what its name promises throws, rather than returning an ignorable code, and the caller either handles it or
   lets it pass up. Use exceptions for error handling only, not for ordinary control flow: implementations are
   optimised on the assumption that they are rare.
3. **A constructor establishes its invariant or throws.** An object whose constructor failed must not exist, so
   no "valid" flag, no two-step `init()` that leaves a half-built object.
4. **Throw purpose-designed types, by value; catch by reference.** Use user-defined types, ideally derived
   from the standard exception base, and not built-in types such as `int` or `const char*`. Catch a hierarchy
   by reference to avoid slicing, and order `catch` clauses from most to least specific.
5. **Do not catch everywhere.** A function that cannot handle an error leaves it alone; a `try`/`catch` in
   every function is a sign of unsystematic handling or of low-level resource management that should have
   been RAII. Catch where you can do something about it: at the boundary of a thread, a request or the program.
   Use a scope-exit action object only when no suitable resource handle exists. Code that
   holds a raw owning pointer must not throw; wrap the resource in a handle first.
6. **`noexcept` is a promise.** Mark a function `noexcept` when leaving it by an exception is impossible or
   unacceptable. Destructors, deallocation functions, `swap`, and the copy and move construction of exception
   types must never fail. Move operations and `swap` should be `noexcept`: a throwing move breaks what callers assume,
   and a non-throwing one is used more efficiently by the standard library and the language. Do not use dynamic
   exception specifications.
7. **Preconditions and postconditions are stated.** State them in the interface, so the caller knows what is
   required and the callee knows what it may assume, and check at run time what cannot be checked at compile
   time (§1.1, `c-conventions` §5.4).
8. **Without exceptions, fail fast or use error codes systematically.** Choose one: terminate on the error (and
   say so in the interface), or return a result type that carries either the value or the error and that the
   caller must inspect. Do not mix styles within one layer. Simulate RAII for cleanup. Avoid error handling
   through global state such as an error-number variable.
9. **A constructor that can fail, without exceptions, is built by a factory.** A static function that returns
   the result type, with the constructor private, keeps invalid objects from existing; an `init()` method after
   construction does not.
10. **A result type is a legitimate choice for expected failures** (parse errors, missing files) even in a code
    base that uses exceptions for the unexpected; the rule is to be consistent within a module and to
    document which functions report how.
