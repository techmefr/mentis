# cpp-conventions §7 — Hardening, functions, templates and performance

> Section 7 of `skills/cpp-conventions`. Read it when build flags change, a function signature is chosen, a
> template or a concept is written, or an optimisation is considered. The other sections and the guardrails
> stay in `SKILL.md`.

**Hardening is shared, not repeated.** The warning set, the library precondition checks (`_GLIBCXX_ASSERTIONS`
or the libc++ hardening mode in production, the debug modes only in test builds), the stack, control-flow and
linker options, the sanitizers and the fuzzing expectation are `skills/c-conventions` §5, and they apply to C++
without change. What C++ adds to it is two lines: build the whole program, libraries included, with the same
standard-library checks (mixing translation units compiled with a container-layout-changing debug mode and
without it breaks), and run the thread sanitizer on every threaded test suite.

**Functions.**
1. **A function does one logical operation and is short.** Name a meaningful operation; give an operation that
   can be reused a name; prefer pure functions (the same inputs give the same result, nothing else changes),
   which are easier to reason about, test and parallelise. A lambda is for a simple function object used in one
   place; it captures by reference only if it is used locally, never when it is returned, stored or passed to
   another thread; it does not use the default by-copy capture when it captures `this`.
2. **Pass information the conventional way.** A cheap-to-copy "in" parameter (up to two or three machine words)
   by value, other "in" parameters by reference to `const`; an "in-out" parameter by non-const reference; a
   "will-move-from" parameter by rvalue reference and moved from; a forwarded parameter by forwarding
   reference and only forwarded. An "out" value is a return value, several are a struct. Do not return `const
   T`. Use a pointer rather than a reference when "no argument" is valid.
3. **Spell the contract in the signature.** A function that must not throw is `noexcept` (§3.6); one that may
   run at compile time is `constexpr`; an unused parameter is unnamed; a default argument is preferred to an
   overload that only fills a value; no C-style variadic arguments.
4. **A function that takes a pointer says what ownership means** (§2.5); a pointer that cannot be null is a
   reference or a non-null wrapper.

**Templates.**
5. **Every template argument has a concept.** Constraining the argument documents it and turns a page of
   deep instantiation errors into one line at the call site. Prefer the standard concepts, name a concept for
   what it means (not for the syntax it checks), define it in terms of use patterns, give it a complete set of
   operations, and require only essential properties. Avoid highly visible unconstrained templates with
   common names, which capture calls meant for something else.
6. **Keep templates simple.** Use them to raise the level of abstraction for algorithms, containers and ranges;
   use a function object to pass an operation to an algorithm; use an alias template to hide detail; prefer
   `using` over `typedef`; minimise the context a template depends on; place members that do not depend on the
   parameter in a non-template base. Do not specialise function templates (overload them); use brace
   initialisation inside templates; do not make a member function template virtual; do not naively templatise a
   class hierarchy, and do not mix hierarchies and arrays. Inside a template, an unqualified call to a
   non-member function is a customisation point: make that your intent.
7. **Metaprogramming only when needed.** Compute values at compile time with `constexpr` functions and types
   with aliases, use the standard library's facilities, and an existing library beyond that. Check that a class
   meets a concept with a `static_assert`.

**Performance.**
8. **Do not optimise without a reason, and measure.** Optimisation that is not needed produces errors and
   maintenance cost; claims about performance without measurements are folklore, and modern hardware and
   optimisers surprise experts. Do not assume complicated code is faster than simple code, or low-level code
   faster than high-level code.
9. **Design to enable optimisation.** Rely on the static type system (it is checked and optimised for free),
   do work at compile time instead of run time, remove needless aliases and indirections, cut allocations and
   deallocations and keep them off the hot path, use compact data
   structures and access memory predictably, avoid context switches on the critical path. Put the most-used
   member of a time-critical structure first.
