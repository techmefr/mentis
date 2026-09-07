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
   CSS. Three shapes are outside the scheme whatever the preprocessor: a **grandchild**
   (`.block__element__sub`) — flatten it, or promote it to its own block, since BEM has no third level; a
   **bare modifier** (`.active`, `.small`) — it says nothing about what it modifies and collides across
   blocks, so it carries its base; and **camel or Pascal case** — the scheme is kebab-case. A preprocessor's
   `&__element`/`&--modifier` nesting under one block root is a shorthand for exactly these selectors, not a
   licence for a different set.
6. Class and style bindings expressed through the framework's binding syntax rather than string
   concatenation built by hand, and split along what actually varies: static class names stay in the static
   attribute, dynamic ones in the bound one. A static name packed into the bound attribute, or a
   template-literal that concatenates the two, hides which half a reader can rely on — the framework merges
   them anyway, so composing one expression by hand buys nothing. Past two dynamic entries, name the
   intent in a `computed` (`cardModifiers`) instead of growing the literal in the template. Use classes for
   finite states (variant, active, size) and a bound style only for continuous values (a position, a
   transform driven by data). Where the framework can read a reactive value from inside the style block
   itself, that beats bridging it through a bound style as a custom property; take the bridge when the
   direct form would genuinely be more complex, and say which case you're in.
7. Don't hand-import what the framework auto-imports (in Nuxt: composables, components, stores, utils, and
   your own project types). A manual import line for an auto-imported symbol is noise that drifts out of
   date; the fix is usually deleting the import, not aliasing it. A folder the framework doesn't scan by
   default is **opted into the scan** (Nuxt: `imports.dirs`) rather than imported by hand file by file — one
   config line against an import in every consumer. Don't list folders already scanned: that reads as not
   knowing what was auto-imported. What genuinely keeps an import is a third-party package and a real name
   collision, and the collision is disambiguated in the one file that has it, not aliased globally.
8. Prefer an import alias over a relative path across folders, once the architecture linter resolves it.
