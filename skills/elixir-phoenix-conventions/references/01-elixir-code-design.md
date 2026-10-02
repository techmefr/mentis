# § 1 — Assertive code, return types, data modelling

> Section 1 of `skills/elixir-phoenix-conventions`. Read it when a function head, a `with`, an option list, a
> map access or a conversion from text is written. Read 2026-10-02 from the Elixir anti-patterns catalogue
> (code-related and design-related pages).

1. **Pick the access that states whether the key must exist.** `map.key` asserts presence and raises when the
   key is missing; `map[:key]` says the key is optional and yields `nil`. Using the dynamic form on a key that
   always exists hides a missing key until a `nil` surfaces somewhere else.
2. **Match the shapes you handle and let the rest crash.** A function that always returns something, whatever
   the input, gives callers a false impression of success. Pattern-match the known cases; the process is
   supervised, so an unexpected shape is reported and restarted instead of propagated as a plausible value.
3. **Use `and`, `or` and `not` when the operands are meant to be booleans,** and the truthy operators only when
   `nil` or `false` is expected. The strict forms fail early if a value such as `:undefined` or `:error`
   returned from Erlang code slips in as an operand.
4. **A `with` focuses on the success path.** Do not collect the errors of several steps in one large `else`;
   it is then unclear which step produced which error. Normalise each step's return shape in a small private
   function, so the `with` has little or no `else`.
5. **In multi-clause heads, extract only what the clause or guard needs.** Values used just in the body are
   taken in the body, so a reader sees at a glance what selects the clause.
6. **Never create atoms from external text.** Atoms are not garbage-collected and their number is capped by the
   VM; converting request or response strings to new atoms lets an outsider exhaust it. Map the strings you
   accept to atoms explicitly (a fixed lookup), or use the existing-atom conversion knowing its code-loading
   caveats.
7. **A function whose options change its return type is several functions.** Give each return shape its own
   name instead of an option that switches between them.
8. **Replace overlapping boolean options with one atom option.** Two flags whose combinations have precedence
   rules (an admin flag that overrides an editor flag) are one role value in disguise.
9. **Use `case` and pattern matching, not `try/rescue`, for expected failures.** When a library offers both a
   tuple-returning and a bang (raising) version of a function, use the tuple version for flow control. A `throw`
   is acceptable to abort a deep computation only if it is caught in the same module and never leaks into the
   API.
10. **Model structured values as structs, not as bare strings or floats.** A string address parsed in several
    places wants a struct and one parse function; money wants a decimal-based or dedicated type, not a float.
11. **Keep multi-clause functions to one concern.** Clauses with unrelated behaviour (the docs full of "if the
    first argument is X") are separate functions or modules. A function that treats any input of its kind
    identically is fine.
12. **Group related arguments in a map, struct or keyword list when a function takes many;** if the arguments are
    truly unrelated the function is doing too much and is split.
13. **Keep structs under 32 fields.** At 32 or more the VM switches to a larger map representation with higher
    memory use and fewer optimisations, so split the struct.
14. **Name things well rather than comment them.** Give magic numbers a named module attribute and use the
    language's documentation attributes for public API; do not comment self-explanatory code.
