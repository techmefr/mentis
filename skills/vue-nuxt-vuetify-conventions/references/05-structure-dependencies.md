# vue-nuxt-vuetify-conventions §5 — Structure and dependencies

> Section 5 of `skills/vue-nuxt-vuetify-conventions`. Read it when a file is placed, or an import crosses a layer. The other sections and the guardrails stay in `SKILL.md`.

1. **Separate code by technical concern vs functional/business concern** (the layered/OSDD split), and
   `technical/` never imports `functional/`: if a value is missing, the caller passes it as a parameter.
   The direction is the whole point — a technical helper that reaches into a business module cannot be
   reused by the next business module, which is the only reason it was put in `technical/`.
2. **Tests and stories sit where the project decided** — a dedicated folder mirroring the source tree, or
   co-located — but the decision is uniform. Half a codebase each way costs more than either choice,
   because now every reader has to check both places before concluding a test does not exist.
3. **One package manager per project, and a curated list of approved dependencies.** A new dependency is
   a decision (licence, maintenance, bundle weight, supply-chain surface), not a reflex; check what's
   already there first. Two lockfiles in a repo means two different dependency trees get installed
   depending on who ran what, and the CI is the one that disagrees.
4. **Declarative config in a `config/` folder** as soon as N near-identical entities are being wired by
   hand with duplicated watchers and hardcoded arrays. The threshold is when adding the N+1th requires
   editing more than one file.
5. **Look for an existing nearby component/composable before writing a new one** (§2.16).
6. **`runtimeConfig` vs `app.config` is a security boundary, not a style choice.** `runtimeConfig`'s
   top-level keys are server-only by default and read from `NUXT_*` environment variables (a secret goes
   here, unnested, never under `public`); only `runtimeConfig.public`/`runtimeConfig.app` cross to the
   client, and a value placed there is as exposed as if it were hardcoded in the bundle. `app.config.ts`
   is for static, non-secret, build-time values (theme tokens, feature toggles) that need hot-reload
   during dev, and **cannot** read an environment variable at all — reaching for it to keep a secret out
   of the bundle is the opposite of what it does. In a layered/OSDD project each layer's own
   `nuxt.config.ts` carries its own `runtimeConfig`, not a single root one.
   [nuxt.com/docs/4.x/getting-started/configuration,
   nuxt.com/docs/4.x/guide/going-further/runtime-config, read 2026-08-10.]
7. **Nuxt 4's default directory layout, on a plain repo with no layer/OSDD convention installed**:
   `srcDir` defaults to `app/` (components/composables/layouts/middleware/pages/plugins/utils/app.vue all
   move under it, and `~` now resolves to `app/` instead of the project root); `serverDir` moves the
   other way, to `<rootDir>/server` regardless of `srcDir`; `layers/`, `modules/`, `public/` stay
   resolved from `<rootDir>`; and a new `shared/` directory (`shared/utils/`, `shared/types/`) is
   auto-imported into both the Vue app and the Nitro server for code that's genuinely neither. [Same
   source as point 6 above, read 2026-08-10.] **Where the company's `nuxt-osdd` package is installed, it
   overrides this**: each layer already carries its own self-contained `app/` subtree (see that package's
   own structure), and this generic default only applies where no such layer package is installed.
8. **A layer boundary that only exists in prose does not exist.** Enforce the allowed import directions
   with the project's dependency linter or its path configuration, so a wrong-direction import fails a
   build rather than waiting for a reviewer to notice. This is the §11 rule applied to architecture:
   prefer the mechanism the toolchain enforces over the sentence someone has to remember.
9. **Aliases rather than deep relative paths** — but verify the dependency linter and the type checker
   both resolve the alias before migrating a tree to it. An alias that only the bundler understands
   produces a build that works and a checker that reports every file as broken, which gets "fixed" by
   turning the checker off.
10. **A `shared/` or `utils/` directory is a boundary, not a bucket.** A helper with exactly one caller
    belongs next to that caller; moved to the shared tree it acquires a reputation as common
    infrastructure it never earned, and the next person edits it for their case without knowing who else
    depends on it. Promote on the second real caller (this is the same threshold the design-patterns
    block uses).
11. **A circular import resolves in an order nobody controls.** Two modules importing each other work
    until the day the entry point changes, then fail as `undefined` on a symbol that plainly exists
    (§2.14). If two modules need each other, something they both need belongs in a third.
12. **Keep the server boundary physical.** Server-only code lives under the server tree, so an accidental
    import from a component is impossible rather than merely discouraged — a comment saying "server only"
    has no effect on the bundler, and the failure mode is server logic and its secrets shipped to the
    browser without anything reporting it.
13. **Environment variables are read in one place.** Scattered through modules, they stop being
    answerable: nobody can say what the application needs in order to boot, so a missing variable
    surfaces as a feature that silently does nothing in one environment. Read them in the config,
    validate them there, and hand the rest of the code a typed object.
14. **Check the platform before adding a dependency for one helper.** `Intl` formats dates, numbers and
    currencies; `structuredClone` deep-copies; `URL` and `URLSearchParams` parse; `crypto` hashes and
    makes ids. A package added for one function is a package to audit, update and ship forever.
15. **The lockfile is part of the change.** A dependency added without it installs a different version on
    the next machine, which turns "works locally" into a claim about one developer's node_modules rather
    than about the repository.
16. **A layer's precedence is fixed and worth knowing before debugging "my override didn't apply".** The
    project's own files win over anything in `extends`, and among extended layers the ones listed last
    lose to the ones listed first — configuration is merged (not replaced) through the framework's own
    deep-merge, so two layers each setting one key of the same object both survive, but two layers setting
    the *same* key resolve by that order, not by which one "feels more specific". [nuxt.com/docs/4.x/guide
    /going-further/layers]
17. **A remote layer (a git ref, an npm package) is a dependency you audit before extending it, not a free
    template.** Extending a layer runs its `nuxt.config` and any build-time code it ships inside your own
    project, with your project's environment — the trust boundary is the same one that applies to any
    installed dependency, and "it's just a Nuxt layer" is not an exemption from checking what it does.
18. **Each layer owns its full `app/` subtree and its own dependencies, not a shared one assembled by the
    consuming project.** A layer that expects the host project to already have a package installed breaks
    the moment it's extended somewhere that doesn't; a self-contained layer with its own `package.json`
    (or its dependencies declared explicitly) is reusable, one that reaches up into whatever happens to be
    around it is coupled to a specific host and only looks reusable.
19. **A monorepo settles on one lockfile at the workspace root, not one per package.** Workspaces (npm,
    pnpm or yarn) exist precisely so every package resolves from the same dependency graph; a package with
    its own lockfile silently opts itself out of that graph and can end up on a different version of a
    shared dependency than every sibling package, which is the same two-lockfiles failure as point 3, one
    level down the tree.
20. **Auto-scanned components and composables are named to avoid cross-layer collision, not just
    cross-file collision within one layer.** Two layers each auto-registering a `Button` component or a
    `useUser` composable resolve by layer order (point 16) rather than by an error, so the wrong one can
    win silently; a prefix or namespace tied to the owning layer turns a silent shadowing into a name that
    is unambiguous to grep for.
21. **A layer is deleted by deleting its directory, not by disabling it in config.** A layer commented out
    of `extends` but left on disk still ships in the repository, still gets modified by someone who finds
    it while searching, and still shows up in a dependency audit as installed — treat an unused layer the
    way an unused dependency is treated: removed, not merely unwired.
