# c-conventions §6 — Headers, macros and structure

> Section 6 of `skills/c-conventions`. Read it when a header, an include guard, a macro or the split of a
> module into files is written. The header rules are the ones of the C family and are shared with
> `skills/cpp-conventions` §6; the macro rules matter more in C, where the preprocessor is the only
> abstraction tool. The other sections and the guardrails stay in `SKILL.md`.

1. **A header compiles on its own.** It has its include guard, it includes every header it needs, and including
   it first in an empty file succeeds. A header that works only when someone else included a dependency
   before it breaks the day an include is removed from an unrelated file.
2. **The guard name is derived from the project and the full path** of the header
   (`PROJECT_SRC_NET_SOCKET_H`), so two headers called `socket.h` in different directories cannot collide.
   The guard closes the file.
3. **Include what you use.** A source or header file includes directly the header that declares each symbol it
   refers to, and does not count on a header included by another header. Removing an include from a header must
   not break its users. A source file includes its own header first, which proves the header is
   self-contained.
4. **A header declares; it does not define.** No object definitions and no non-inline function definitions in a
   header that several files include: each translation unit would get its own copy or the link would fail.
   Everything used by more than one file is declared in a header; everything used by one file is declared `static`
   in that file, which is internal linkage and keeps it out of the global symbol space.
5. **No cyclic dependencies between source files.** Two modules that include each other cannot be built,
   tested or reasoned about separately. Break the cycle by moving the shared part down into a third module.
6. **Avoid non-constant global variables.** They hide dependencies and are exposed to unpredictable changes, and in
   a threaded program they are shared state (§4.1). Pass the state in a structure.
7. **Macros last, and with a prefix.** Prefer an inline function for computation, an enumeration or a constant
   for names. A macro is invisible to the compiler's type checking and to debuggers, has global scope, and makes
   the code a reader sees different from the code the compiler sees. When one is unavoidable, give it a
   project-specific prefix and an upper-case name, and never use macros to generate the pieces of a public
   interface (declaring fields, functions or types through macro expansion), since every error message then has
   to be read through the expansion and tools cannot refactor it.
8. **A macro argument is evaluated once or the macro says so.** A function-like macro that uses an argument
   twice runs its side effects twice [PRE31]; do not pass `x++` to such a macro, and prefer a function
   so the question does not arise. Never put preprocessor directives inside the argument list of a function-like
   macro invocation [PRE32]; its behaviour is undefined. Do not build a universal character name by token
   concatenation [PRE30].
9. **Keep a module's interface small.** A header exposes what callers need and nothing else. A type whose
    layout callers must not depend on is exposed as a pointer to an incomplete structure declared in the
    header, with the definition kept in the source file and creation and destruction functions in the header.
