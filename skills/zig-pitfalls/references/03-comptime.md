# zig-pitfalls §3 — Comptime

Rules from the Zig 0.17.0 language reference and release notes unless a rule says otherwise.

## 3.1 What comptime guarantees
1. **A `comptime` parameter must be known at the call site**, otherwise it is a compile error ("unable to
   resolve comptime value"). That is how generics work in Zig: types are first-class values but can only be
   used in expressions known at compile time, so a type parameter is always `comptime T: type`.
2. **A `comptime` expression either evaluates at compile time or fails to compile.** Inside one, every
   variable is a comptime variable, every `if`, `while`, `for` and `switch` is evaluated at compile time,
   `return` and `try` are invalid unless the function itself is called at compile time, and anything with
   runtime side effects is an error (the reference's example is calling an external function).
3. **The same function can run at compile time and at run time**, unchanged. A table built by an ordinary
   function and assigned to a namespace-level constant is computed during compilation.

## 3.2 Using it well
1. **Use comptime to compute constants, build lookup tables and check relationships between constants**; the
   compile-time assertion form is `comptime { assert(...) }` and fails the build instead of the run (see
   `systems-assertion-discipline` §1.4).
2. **Do not use it to hide run-time cost** (own guidance, not a statement of the reference): a generic function
   instantiated for many types multiplies code, and a compile-time loop that is slow to compile costs every
   developer on every build. Prefer a plain run-time function when nothing needs to be known at compile
   time.
3. **Name generic types by assigning them to a constant.** A function returning a `struct` gets the inferred
   name `List(i32)` for messages; an explicit `const Node = struct { ... }` names it directly, and a struct
   can refer to itself through a pointer because top-level declarations are order-independent.

## 3.3 The evaluation limit
1. **Compile-time code has a budget of 1000 backward branches by default**, and exceeding it is a compile
   error ("evaluation exceeded 1000 backwards branches").
2. **`@setEvalBranchQuota(n)` raises it**, and a value smaller than the default or a previously set quota is
   ignored. Raising it is the documented fix, but treat a large quota as a signal that the work may belong at
   run time or in the build step that generates the data (own guidance).

## 3.4 Build-time options are comptime values
A value passed from `build.zig` through an options step and read with `@import("config")` is known at compile
time, so a check on it can be a `@compileError` that never fires for a valid configuration (the build system
page's example). Wiring is in §4.1.

## 3.5 Version drift
Zig 0.17.0 changed several comptime-adjacent details: array multiplication (`a ** b`) was removed in favour of
`@splat`, `void{}` became `{}`, `i0` was removed (use `u0`), and `@hasDecl` now returns true only for public
declarations whichever file it is in. Details and the full list are in §4.4.
