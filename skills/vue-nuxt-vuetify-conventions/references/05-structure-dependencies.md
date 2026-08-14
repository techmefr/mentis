# vue-nuxt-vuetify-conventions §5 — Structure and dependencies

> Section 5 of `skills/vue-nuxt-vuetify-conventions`. Read it when a file is placed, or an import crosses a layer. The other sections and the guardrails stay in `SKILL.md`.

1. Separate code by **technical concern** vs **functional/business concern** (the layered/OSDD split), and
   `technical/` never imports `functional/`: if a value is missing, the caller passes it as a parameter.
2. Tests and stories sit where the project decided — a dedicated folder mirroring the source tree, or
   co-located — but the decision is uniform. Half a codebase each way costs more than either choice.
3. One package manager per project, and a curated list of approved dependencies. A new dependency is a
   decision (licence, maintenance, bundle weight), not a reflex; check what's already there first.
4. Declarative config in a `config/` folder as soon as N near-identical entities are being wired by hand
   with duplicated watchers and hardcoded arrays.
5. Look for an existing nearby component/composable before writing a new one.
6. **`runtimeConfig` vs `app.config` is a security boundary, not a style choice.** `runtimeConfig`'s
   top-level keys are server-only by default and read from `NUXT_*` environment variables (a secret goes
   here, unnested, never under `public`); only `runtimeConfig.public`/`runtimeConfig.app` cross to the
   client, and a value placed there is as exposed as if it were hardcoded in the bundle. `app.config.ts` is
   for static, non-secret, build-time values (theme tokens, feature toggles) that need hot-reload during
   dev, and **cannot** read an environment variable at all — reaching for it to keep a secret out of the
   bundle is the opposite of what it does. In a layered/OSDD project each layer's own `nuxt.config.ts`
   carries its own `runtimeConfig`, not a single root one. [nuxt.com/docs/4.x/getting-started/configuration,
   nuxt.com/docs/4.x/guide/going-further/runtime-config, read 2026-08-10.]
6. **Nuxt 4's default directory layout, on a plain repo with no layer/OSDD convention installed**:
   `srcDir` defaults to `app/` (components/composables/layouts/middleware/pages/plugins/utils/app.vue all
   move under it, and `~` now resolves to `app/` instead of the project root); `serverDir` moves the other
   way, to `<rootDir>/server` regardless of `srcDir`; `layers/`, `modules/`, `public/` stay resolved from
   `<rootDir>`; and a new `shared/` directory (`shared/utils/`, `shared/types/`) is auto-imported into both
   the Vue app and the Nitro server for code that's genuinely neither. [Same source as point 5 above,
   read 2026-08-10.] **Where `nuxt-osdd` (nuxt-osdd.xefi.com) is installed, it overrides this**: each layer
   already carries its own self-contained `app/` subtree (see that package's own structure), and this
   generic default only applies where no such layer package is installed.
