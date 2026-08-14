# vue-nuxt-vuetify-conventions §4 — Naming and style

> Section 4 of `skills/vue-nuxt-vuetify-conventions`. Read it when a symbol, a file or a CSS class has to be named. The other sections and the guardrails stay in `SKILL.md`.

1. Casing fixed per artefact kind (files, components, composables, stores, types, constants) and applied
   without exception.
2. Booleans prefixed `is`/`has`/`can`/`should`. `loading` is ambiguous — a boolean? a promise? a count?
   `isLoading` isn't.
3. A callback parameter is the full singular word of the collection it iterates (`post` in `posts.map`),
   never `p` or `u`. A `reduce` accumulator is named for what it accumulates (`runningTotal`, `byId`),
   never `acc`.
4. Functions declared as arrow functions assigned to a `const`, consistently — the point is one shape
   across the codebase, not a claim that `function` is broken.
5. CSS class names follow a single naming scheme, BEM by default (`.block`, `.block__element`,
   `.block--modifier`) — this is about naming, not about the preprocessor, and applies identically to plain
   CSS.
6. Class and style bindings expressed through the framework's binding syntax rather than string
   concatenation built by hand.
7. Don't hand-import what the framework auto-imports (in Nuxt: composables, components, stores, utils, and
   your own project types). A manual import line for an auto-imported symbol is noise that drifts out of
   date; the fix is usually deleting the import, not aliasing it.
8. Prefer an import alias over a relative path across folders, once the architecture linter resolves it.
