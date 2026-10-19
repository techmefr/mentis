# cpp-conventions §6 — Headers, namespaces and structure

> Section 6 of `skills/cpp-conventions`. Read it when a header, an include, a forward declaration, a
> namespace, a macro or the layout of a module is written. The rules for self-contained headers, guards,
> include-what-you-use, no definitions in headers and no cycles between files are the ones of
> `skills/c-conventions` §6.1 to §6.5 and apply unchanged; this section adds what C++ introduces. The other
> sections and the guardrails stay in `SKILL.md`.

1. **Follow the project's file conventions.** Interface files and implementation files use the project's
   suffixes (`.h` and `.cpp` or `.cc` unless the code base already uses another pair). Do not mix two
   conventions in one project.
2. **A source file includes its own header first,** then the others, so the header is proven self-contained.
   Quotes are for files next to the including file, angle brackets for the rest; spell the include paths in a
   way every supported platform accepts.
3. **Templates and inline functions are defined in the header,** next to their declaration or in a file the
   header includes. Do not hide the definitions in a separately included implementation file; that practice
   has been dropped by the style guide it came from.
4. **Avoid forward declarations where an include works.** A forward declaration saves compile time and
   recompilation, but it hides a dependency, defeats automatic tools looking for the defining module and can
   be broken by a later change to the library it forward-declares. Include the header you need; use a forward declaration only where the include creates a
   real cycle or a measured build cost.
5. **Namespaces express logical structure.** Put the code of a module in a namespace named for it. A header never
   carries a global `using namespace`, because every file that includes it inherits the directive; a source
   file may use one for the standard library, during a migration, or inside a local scope. File-local
   entities go in an unnamed namespace (or `static`) in the source file, never in a header.
6. **Small and time-critical functions may be `inline`; constant-computable ones are `constexpr`.** A function
   that might need evaluating at compile time is declared `constexpr`; the compiler, not the programmer,
   decides what to inline in the general case.
7. **Macros are the last tool.** Do not use them for constants (use `constexpr`), for functions (use inline
   functions or templates), for types (use aliases with `using`, not `typedef`) or to generate pieces of an
   interface. If a macro is unavoidable, its name is in upper case, unique (a project prefix), and it is defined
   as close to its use as possible and undefined after. Macros do not respect scope or types, and the code
   you read differs from the code the compiler sees.
8. **Do not add to the standard namespace,** and do not rely on names pulled in indirectly by another header
   (§6.3 of `c-conventions` states the same for any include).
9. **Prefer C++ to C in new code.** Where C is unavoidable, stay in the subset both languages share and build it as C++;
   when a C interface has to be called, wrap it in C++ in the calling code with a type that owns the resource (§2.1).
10. **Modules.** Where the project's standard and toolchain support C++20 modules, treat the introduction of
    modules as a project decision with a migration plan, not a per-file change; this block takes no rule from
    a source on module layout.
