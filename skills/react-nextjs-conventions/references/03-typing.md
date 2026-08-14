# react-nextjs-conventions §3 — Typing

> Section 3 of `skills/react-nextjs-conventions`. Read it when props, state or a generic is typed. The other sections and the guardrails stay in `SKILL.md`.

1. `any` is banned, including in a `catch` clause: `unknown` plus narrowing. `catch (e: unknown)` and a type
   guard, not `catch (e: any)`.
2. **No type assertions** (`as`, and the non-null `!`), except `as const`. An assertion is a claim the
   compiler cannot check; a narrowing check is one it can.
3. **Derive types rather than re-listing fields**: `Pick`/`Omit`/`Partial` off the source type, or inferred
   from the validation schema. A hand-copied subset drifts the day a field is added.
4. A **string union** rather than an `enum` for a fixed set of string values: it needs no runtime object, it
   narrows properly, and it serialises as itself.
5. `type` or `interface` for object shapes: **pick one per project and apply it uniformly**. Both are
   defensible; a codebase using both for the same kind of shape is not.
6. **Validate at every untrusted boundary** (API response, `localStorage`/`sessionStorage`, URL query
   params, `postMessage`) with a schema, and derive the type from the schema. This is the correct
   replacement for `as SomeResponse` on a fetch result: the assertion claims a shape, the schema checks it.
