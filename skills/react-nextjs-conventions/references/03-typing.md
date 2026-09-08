# react-nextjs-conventions §3 — Typing

> Section 3 of `skills/react-nextjs-conventions`. Read it when props, state or a generic is typed. The other sections and the guardrails stay in `SKILL.md`.

1. `any` is banned, including in a `catch` clause: `unknown` plus narrowing. `catch (e: unknown)` and a type
   guard, not `catch (e: any)`. `any` does not fail locally — it spreads: every value derived from it is
   also unchecked, so one annotation retires the compiler across a whole call path, and the place where the
   type was lost is nowhere near the place the error finally appears.
2. **`Record<string, any>` and `object` are `any` with better manners.** An API payload typed that way
   accepts every property access, so a renamed field reads as `undefined` and the screen renders blank
   rather than failing. If the shape is genuinely unknown, say `unknown` and narrow; if it is known, write
   it down.
3. **No type assertions** (`as`, and the non-null `!`), except `as const`. An assertion is a claim the
   compiler cannot check; a narrowing check is one it can. The non-null `!` deserves its own mention because
   it is the shortest way to convert a compile error into a production one: the value it silences is
   precisely the one that will be missing.
4. **A compiler error is information; never widen a type to make it go away.** The error is the design
   telling you the two shapes do not match, and the choices are to fix the shape or to handle the case —
   both of which end up in the code. An `as unknown as T` records only that somebody was in a hurry.
5. **`@ts-expect-error` rather than `@ts-ignore`, with the reason on the line above.** The expect form fails
   the build once the underlying problem is fixed, so the suppression removes itself; `@ts-ignore` outlives
   its cause and then hides the next, unrelated error at the same spot.
6. **Derive types rather than re-listing fields**: `Pick`/`Omit`/`Partial` off the source type, or inferred
   from the validation schema. A hand-copied subset drifts the day a field is added — and it drifts
   silently, because both declarations still compile, so the mismatch only shows up as a missing value on
   screen.
7. **Don't annotate what inference already knows.** A `const` restating the type of its own initialiser is
   noise that goes stale independently of the value. The place to pin a type deliberately is the boundary:
   an exported function's return type, so a change inside it cannot widen the public shape without a diff
   saying so.
8. A **string union** rather than an `enum` for a fixed set of string values: it needs no runtime object, it
   narrows properly, and it serialises as itself. The runtime object is the practical problem — an `enum`
   value crossing a network or storage boundary arrives as a string that no longer equals the enum member
   it came from.
9. **A discriminated union instead of a bag of optional fields.** `{ status, data?, error? }` allows
   loading-with-data, success-without-data and error-with-data — three states the code must defend against
   for ever, and one of them is what a reader sees when the branch is missing. Keying the union on `status`
   makes them unrepresentable, and then the exhaustive `switch` of §4.7 does the rest.
10. **A type guard must return a predicate.** `function isUser(v: unknown): boolean` narrows nothing, so the
    call site still needs an assertion and the guard becomes decoration. `v is User` is what makes the
    compiler carry the conclusion forward.
11. **`type` or `interface` for object shapes: pick one per project and apply it uniformly.** Both are
    defensible; a codebase using both for the same kind of shape is not. The cost of mixing them is that
    every reader spends a moment wondering whether the choice meant something.
12. **A generic parameter used once is not a generic.** `<T>(value: T) => void` constrains nothing — it is
    `any` with ceremony. A type parameter earns its place when it appears at least twice, tying an input to
    an output or two inputs to each other.
13. **Take the DOM and event types from React's own**, not from a hand-written shape: `FormEvent`,
    `ReactNode`, `ChangeEvent<HTMLInputElement>`, `ComponentProps<typeof Button>`. The last of those is
    worth the habit on its own — a wrapper typed from the component it wraps cannot fall behind it (§8.4).
14. **Two identifiers that are both `string` are interchangeable to the compiler.** Passing an account id
    where a user id was expected typechecks, and the failure is a data one. Where that swap is plausible and
    the consequence is real, a branded type costs one declaration and closes it.
15. **Validate at every untrusted boundary** (API response, `localStorage`/`sessionStorage`, URL query
    params, `postMessage`) with a schema, and derive the type from the schema. This is the correct
    replacement for `as SomeResponse` on a fetch result: the assertion claims a shape, the schema checks
    it. Types are erased at runtime, so a typed response is a description of what the server promised, not
    a statement about what arrived — the two diverge on the day the API is deployed before the client.
16. **The schema is the single source, and it flows outward.** Form types, API types and component props all
    derived from the same declaration means a field added once is a compile error everywhere it now has to
    be handled. Two hand-kept copies of the same shape means it is a runtime surprise in whichever of the
    two nobody remembered.
