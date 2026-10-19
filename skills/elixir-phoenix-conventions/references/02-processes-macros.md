# § 2 — Processes, supervision, macros, library hygiene

> Section 2 of `skills/elixir-phoenix-conventions`. Read it when a process is started, a GenServer interface is
> added, a macro or `use` is written, or a library is published. Read 2026-10-02 from the Elixir anti-patterns
> catalogue (process-related and meta-programming pages, plus the library items of the design page).

1. **A process models a runtime property, not code organisation.** Use one for concurrency, shared resource
   access or error isolation. A module of pure functions wrapped in a GenServer serialises every caller through
   one mailbox and becomes a bottleneck; keep it modules and functions, and leave the parallelism decision to
   the caller.
2. **One module owns the interface to each process.** Calls and casts to a given GenServer or Agent live in a
   single module that defines the message formats; scattered direct calls duplicate code and let any data shape
   in.
3. **Send a process only the data it needs.** Messages and values captured by a spawned function are copied in
   full into the other process; handing over a whole connection struct to log an address copies all of it.
   Extract the field first, outside the function you spawn.
4. **Start every long-lived process under a supervisor.** A process started outside a tree is hard to observe,
   has no guaranteed start order and no guaranteed stop at shutdown. A library lets its users place its processes
   in their own tree instead of starting them on its own.
5. **Use a macro only when a function cannot do the job.** An unnecessary macro makes the code harder to read
   and reason about for no gain.
6. **Keep a macro's generated code small:** have the macro expand to a call into an ordinary function that does
   the work, so the compiler does not re-expand large bodies at every use (a router with hundreds of routes is
   the example).
7. **Prefer `import` and `alias` to `use`.** The first two are lexical and visible; `use` can inject any code and
   dependencies into the caller, so the reader must know the library's internals, and conflicts surface only at
   compile time.
8. **Watch compile-time dependencies.** A macro's arguments can become compile-time dependencies, so editing one
   file recompiles many. Inspect with the compiler's cross-reference trace for the file, and avoid building
   module names dynamically at compile time in a way the compiler cannot track.
9. **A library keeps to its own namespace.** Every module name starts with the package name: the VM loads one
   module of a given name, so a module defined inside another package's namespace clashes now or when that
   package adds the same name.
10. **A library does not configure itself through the global application environment.** Global settings force
    every dependent in the system to share the value; take options as function arguments or in the child spec
    so each user chooses.
