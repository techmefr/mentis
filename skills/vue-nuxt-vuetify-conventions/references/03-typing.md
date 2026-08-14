# vue-nuxt-vuetify-conventions §3 — Typing

> Section 3 of `skills/vue-nuxt-vuetify-conventions`. Read it when props, emits, refs or a store return type are written. The other sections and the guardrails stay in `SKILL.md`.

1. `any` is banned; `unknown` keeps the value opaque and forces the narrowing you needed anyway. The two
   narrow exceptions — an untyped third-party lib with no shim available, and a generic parameter defaulting
   for backwards-compatible inference — stay confined to one file.
2. `import type` for type-only symbols, so the build can erase them.
3. Business types live in one predictable place per module rather than next to whichever component first
   needed them, and the project's prefix/casing convention is applied uniformly (a mixed codebase is worse
   than either convention).
4. A mapped type (`Record<K, V>`) rather than an interface with an index signature.
5. Annotate explicitly by default; fall back to inference only where the explicit type would be genuinely
   unreadable.
6. No type assertion (`as`) where a narrowing check would do: an assertion is a claim the compiler can't
   check.
