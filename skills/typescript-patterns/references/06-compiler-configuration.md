# typescript-patterns §6 — Compiler configuration and the type-check gate

> Section 6 of `skills/typescript-patterns`. Read it when a `tsconfig` is created or changed, a compiler
> option is turned off to get past an error, a build that "passes" is being trusted, or a lint rule set is
> chosen. The other sections and the guardrails stay in `SKILL.md`.

1. **A new project starts with `strict`, from the first commit.** The strict switch enables a family of
   checks (null checking, implicit `any`, function parameter variance, bound-call checking, property
   initialisation, `this` typing, always-strict emit, unknown catch variables, built-in iterator return types: nine in all, see §11.6); retrofitting them to a large
   codebase is a project of its own, and adding them on day one costs nothing. An existing project keeps the
   configuration it has: raising strictness is a decision with its own plan, usually package by package
   through separate configurations, and never a side effect of a feature (the guardrail of this block).
2. **Three checks beyond strict are worth enabling in new code.** Unchecked indexed access types a lookup as
   possibly missing (§4, point 9); exact optional property types separates an absent property from an
   undefined one (§4, point 8); the implicit-override check makes a renamed base method an error in its
   subclasses. The switch-fallthrough and implicit-return checks catch the branch that forgot to return.
3. **A type-only import is stated.** The type-import syntax, enforced by the module-syntax option, erases
   an import that exists only for the compiler, so the runtime graph contains only runtime dependencies and a
   circular type reference does not become a circular module. The isolated-modules option makes each file
   compile on its own, which transpile-only tools require.
4. **`target`, `lib` and module resolution describe the runtime, not the editor.** A wrong module-resolution
   mode compiles imports that fail at run time (a missing file extension under native ESM, a package
   exports map ignored). Set them to what the bundler or the runtime does, and let the framework's generated
   base configuration set them when one exists.
5. **A path alias is resolved twice.** The compiler's alias setting only informs the type checker; the
   bundler, the test runner and the runtime each need the same mapping. One source of truth (the base
   configuration the others extend) and an import that works in the test runner are the check; an alias
   that type-checks and fails at run time is the usual symptom.
6. **Transpilation is not type-checking.** Modern bundlers and dev servers strip types without checking them,
   so a build that succeeds says nothing about type errors. The type check runs as its own step, in CI and
   before a change is reported done, with the project's own command (the compiler in no-emit mode, or the
   framework's wrapper that includes generated types) (`skills/gate`).
7. **Skipping library checks is a trade, written down.** Turning off the check of declaration files saves
   time and hides a conflict between two packages' types; if it is on, the project says why, and own
   declarations are still checked.
8. **Lint rules that need type information pair with the compiler.** The ones that matter most: floating
   promises (§2, point 1), misused promises in places that expect a synchronous callback, unnecessary
   conditions on values the type says cannot be nullish, consistent type imports, an exhaustiveness check on
   switches, no explicit `any`, and a ban on suppression directives without a description. Several of these are in no preset and must be enabled by name (§10.3). They are errors in
   CI, not warnings that accumulate.
9. **The project's own code is `.ts`.** A declaration file (`.d.ts`) describes code that exists elsewhere,
   such as a plain-JavaScript library; writing one beside own TypeScript hides implementation behind a
   second source of truth that the compiler does not check against it.
10. **Third-party types match the installed major.** The community type package follows the library's major
    version; a mismatch types an API that no longer exists. A library with no types gets the smallest
    declaration the code uses, not a blanket `any` module that silences everything it exports.
11. **Generated types are regenerated, never edited.** Types derived from an API schema, a database or a
    query language come from a command listed in the project, are committed or generated in CI by a stated
    policy, and a CI step fails when the generated output differs from what is committed, so the contract
    cannot drift unnoticed (`skills/api-design`).
