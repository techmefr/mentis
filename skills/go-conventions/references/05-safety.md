# go-conventions §5 — Defensive correctness

> Section 5 of `skills/go-conventions`.

Mistakes the compiler accepts and the runtime punishes. None needs an attacker.

1. A typed nil pointer returned through an interface is not `== nil`: the interface carries a type. A
   function returning an interface returns the literal `nil` for the empty case, never a nil pointer variable.
2. Writing to a nil map panics, reading from it does not. A struct holding a map either initialises it in
   the constructor or creates it on first write inside its methods.
3. `append` reuses the backing array when capacity allows, so two slices can overwrite each other. Where a
   result must not alias its input, cap the input with a full slice expression before appending, or clone.
4. A conversion to a narrower integer wraps silently. Check the range before converting a value that did not
   originate in a type of that width.
5. Floating-point values are not compared with `==`; compare within a tolerance, or use exact arithmetic
   for money. Integer division checks the divisor first: it panics on zero, whereas float division yields an
   infinity or NaN that spreads quietly.
6. Design the zero value to be usable: a type that panics on first use after `var x T` forces every caller to
   remember a constructor. Lazy one-time setup goes through `sync.Once` (or its function-returning forms),
   not a hand-written flag.
7. An exported function returns a copy of an internal slice or map, not the field itself.
8. For reflection code on a recent toolchain, use the generic type-assertion helper of the reflect package
   in place of a bare `Interface()` assertion; check the module version first (`source-freshness`). To confirm:
   the helper's name and the toolchain release that introduced it were not re-read against the standard
   library documentation.
9. Several `init` functions have an unspecified order across files; start-up work goes in an explicit
   constructor called from `main`.
