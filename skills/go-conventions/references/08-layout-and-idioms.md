# go-conventions §8 — Layout and idioms

> Section 8 of `skills/go-conventions`.

1. Start flat. Add a package when a boundary appears, and name it after what it provides; a package called
   `utils`, `common` or `helpers` is a missing name. Code that must not be imported from outside goes under
   `internal`.
2. The interface belongs to the consumer, not the producer: accept interfaces, return concrete types. An
   interface with one implementation and no second consumer is speculation.
3. Do not mirror a layered architecture in package names (a `services`, a `repositories`) unless the project
   already has one. The two source sets disagree on this; the choice here is the smaller structure.
4. The module path is lower-case and matches the repository location; multi-word segments use hyphens.
5. Read the `go` directive of the module before judging an idiom. Where the toolchain has since added a
   replacement (range over an integer, the `slices` and `maps` packages, the per-iteration loop variable, the
   v2 random package, a root-scoped file API), flag the old form in new code only; legacy files stay
   untouched unless asked (`code-baseline`).
6. A feature is not done until it can be observed: structured logging with context (the standard `slog`),
   metrics whose labels have bounded cardinality, and a trace span across a remote call.
