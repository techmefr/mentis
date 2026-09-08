# vue-nuxt-vuetify-conventions §3 — Typing

> Section 3 of `skills/vue-nuxt-vuetify-conventions`. Read it when props, emits, refs or a store return type are written. The other sections and the guardrails stay in `SKILL.md`.

1. `any` is banned; `unknown` keeps the value opaque and forces the narrowing you needed anyway. The two
   narrow exceptions — an untyped third-party lib with no shim available, and a generic parameter
   defaulting for backwards-compatible inference — stay confined to one file. `any` does not fail where
   it is written, it disables checking everywhere the value travels afterwards, which is why the cost is
   never local.
2. `import type` for type-only symbols, so the build can erase them. A value import for a type also drags
   the module into the client bundle, and a type-only file imported for its side effects is a runtime
   dependency nobody declared.
3. Business types live in one predictable place per module rather than next to whichever component first
   needed them, and the project's prefix/casing convention is applied uniformly (a mixed codebase is
   worse than either convention).
4. A mapped type (`Record<K, V>`) rather than an interface with an index signature.
5. Annotate explicitly by default; fall back to inference only where the explicit type would be genuinely
   unreadable. An annotation is a contract the compiler checks against the body; inference just reports
   whatever the body happens to return today, so a mistake there renames the contract instead of failing.
6. No type assertion (`as`) where a narrowing check would do: an assertion is a claim the compiler can't
   check. `!` is the same claim in shorter form, and it fails the same way — at runtime, on the one row
   where the field really was absent.
7. **Props are typed, not described.** Use the type-only `defineProps<T>()` with `withDefaults` rather
   than the runtime object form, so the shape is checked at every call site instead of only validated in
   dev. A prop that has a default is never `undefined` where it is used — typing it optional as well
   forces every template to guard against a state that cannot happen.
8. **Emits carry a typed payload.** `defineEmits(['save'])` accepts anything at all as the argument, so
   the parent's handler and the child's `emit` can disagree indefinitely. Declaring the call signatures
   makes the payload part of the component's contract, which is what a parent is actually coupling to.
9. **A `ref` with no initial value includes `undefined` — say so once, at the declaration.** `ref<T>()`
   is `Ref<T | undefined>`, and the honest fix is annotating it that way and handling the empty case, not
   asserting it away at each read. A template ref to a child component is nullable in the same way —
   `ref<InstanceType<typeof Cmp> | null>` — because it is null until mounted, and code that runs before
   mount is exactly the code that gets this wrong.
10. **Don't hand-write a type the API already defines.** Derive the response shape from the typed client,
    the generated schema or the model layer (§13). A duplicated interface has no link to the source it
    copies: the backend renames a field, the copy still compiles, and the failure is a blank cell in
    production rather than a red build. Where nothing generated exists, one hand-written type per
    resource, in one place, and it is the thing that gets updated.
11. **Validate at the boundary, then trust the type inside.** One parse or guard where data enters — an
    API response, a query param, a realtime payload, `localStorage` — and after it the rest of the module
    works with a real type. Validation scattered deep means every caller re-checks or, more often, none
    of them does, and the ownership of "is this shape true" belongs to nobody.
12. **Prefer a discriminated union to a record of optionals.** Six optional fields describe sixty-four
    states, and most of them are impossible; the type stops helping and every consumer writes defensive
    checks for combinations the code can never produce. A union keyed on `status` (or `kind`) makes the
    real states enumerable and lets the compiler tell a caller they forgot one.
13. **Two ids that must not be swapped should not both be `string`.** A user id and an agency id are
    interchangeable to the compiler while they share a primitive type, and the argument order of a
    two-parameter call is the only thing preventing the mix-up. Distinct aliases document intent; a
    branded type actually enforces it. Reserve it for identifiers that cross module boundaries — this is
    not worth doing for every string in the app.
14. **`as const` on a literal table**, so the derived union stays exact instead of widening to `string`
    and losing every case the compiler could have checked for you — including the exhaustiveness of the
    `switch` that consumes it.
15. **A generic component types its slot props.** A slot whose payload is untyped pushes the consumer
    back to `any` inside their template, which puts the hole back in the one place a reviewer is least
    likely to look. If the component is generic over its item type, the slot signature carries that
    parameter.
16. **The store's public surface is annotated.** A store or composable return type left to inference
    exports whatever its body currently produces, so a refactor inside it changes the contract of every
    consumer without touching a single consumer's file. Stating the return type turns that into a compile
    error where it belongs — in the store.
