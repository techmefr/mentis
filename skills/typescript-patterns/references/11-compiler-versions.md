# typescript-patterns §11 — Compiler versions: the 6.0 defaults and the move to 7

> Section 11 of `skills/typescript-patterns`. Read it when a project upgrades the compiler across a major,
> a new project picks its compiler version, a `tsconfig` option starts reporting a deprecation, or a build
> breaks right after an upgrade with missing global names or misplaced output files. The other sections and
> the guardrails stay in `SKILL.md`. Pinned to the **TypeScript 6.0** release notes (read 2026-10-02,
> `references/origin.md`); the registry's latest compiler that day was 7.0.2, whose own notes were not read.

1. **State which compiler major the project is on before applying §6.** The 6.0 release is a transition
   release: it keeps API compatibility with 5.9, changes several defaults and deprecates a list of options that
   the native-port 7.0 line does not support at all. A rule in §6 about a default holds for 6.0 and later; on
   5.x the same setting has to be written out.
2. **Defaults that changed in 6.0, so a bare `tsconfig` now means something else.** `strict` is on by default;
   `module` defaults to the ESM value; `target` floats to the newest supported ECMAScript version (2025 at that
   release); side-effect imports are checked by default; the lib-replacement lookup is off by default; the
   `rootDir` is the directory of the `tsconfig` file instead of being inferred from the inputs; and `types`
   defaults to an empty list instead of "everything under the types packages directory". Write the settings the
   project depends on explicitly rather than inheriting them, so a future default cannot move the project.
3. **The two edits most upgrades need.** Set `types` to the exact list of global-declaring packages (typically the
   runtime's and the test runner's); the tell is a flood of "cannot find name" errors for the runtime's globals
   and built-in modules. Set `rootDir` when the layout has sources deeper than the config file; the tell is output
   appearing under an extra directory level. An explicit `types` list is also faster to build: the release notes
   report 20 to 50 percent on projects that set it. A wildcard entry restores the old behaviour for a migration
   but is not a destination.
4. **Deprecated options are removed in 7.0, so deprecations are fixed, not silenced.** An `ignoreDeprecations`
   setting for the 6.0 value only postpones the error. Treat the list as a migration backlog:
   - the ES5 target and the downlevel-iteration option (the lowest target becomes ES2015; compile older output
     with an external tool);
   - the Node10-style module resolution: move to the Node-next mode for code that runs on Node directly, or to the
     bundler mode when a bundler or another runtime resolves imports (6.0 also allows the bundler mode with the
     CommonJS module setting, as a stepping stone);
   - the classic resolution, the AMD, UMD, SystemJS and none module values, and the single-output-file option;
   - the base-URL option: remove it and write the prefix into each `paths` entry, because it also acts as an
     implicit lookup root for bare imports;
   - turning off the ES-module-interop and synthetic-default-import options (the safer behaviour is always on, so
     `import * as express` becomes a default import);
   - turning off always-strict emit (all code is treated as strict-mode JavaScript, so identifiers named after
     reserved words must be renamed);
   - the `module` keyword for namespaces, the import `asserts` keyword and the no-default-lib directive.
5. **Passing files on the command line while a config exists is now an error.** Compiling a single file with the
   config ignored used to be silent; use the explicit ignore-config flag when that is the intent, and prefer a
   project-level script that never passes files.
6. **The strict family has nine members, not eight.** The list in §6.1 predates the built-in iterator return
   check (added to the family in 5.6), which types the return value of built-in iterators as undefined instead
   of any. Turning `strict` on enables all nine; and the option's own page warns that later versions may add checks under the
   same switch, so a compiler upgrade can add errors without a config change.
7. **Two options enforce a runtime reality the type checker cannot see.** Under the erasable-syntax-only option the
   compiler rejects constructs a type-stripping runtime cannot erase: enums, runtime namespaces, class parameter
   properties, import-equals and export-equals assignments, and angle-bracket assertions. A project run directly
   by Node's type stripping (supported since v23.6 per the option's page) turns it on, and the enum advice in §3
   becomes a requirement. The verbatim-module-syntax option makes imports and exports without a `type`
   modifier stay in the output, and with a module setting that implies CommonJS an ES import becomes an error
   instead of being rewritten; it is the clean way to guarantee §6.3's erased type imports across single-file
   compilers.
8. **A path alias with a leading `#/` is now possible** in Node-next and bundler modes (package `imports` entries
   such as `#/*`), which Node resolves at run time (newer Node 20 releases and later) without a bundler setting. Prefer it over a compiler-only alias for a
   package that runs unbundled (§6.5 explains why compiler-only aliases fail at run time).
9. **Do not move to 7 on the compiler's release alone.** Check, in this order: the type-aware lint plugin's
   supported range (the pinned 8.71 stops below 6.1.0, §10.11, so a 7.x compiler is outside it), the framework's
   generated base configuration, the test runner's transform and every build tool that imports the compiler as a
   library (the native port changes how tools drive it; that interface was not read). Land the 6.0 deprecations
   first, with the deprecation setting unset, then switch. If the 7 line is wanted earlier, a separate branch with
   the lint step disabled is a decision to record, not a default.
10. **Re-read the release notes of every minor, not only the majors.** The warning in rule 6 means a
    minor can fail a build. Pin the compiler in the lock file, upgrade on purpose, and run the type check
    (`skills/gate`) before the change is reported done.
