# typescript-patterns §10 — Typed linting with typescript-eslint

> Section 10 of `skills/typescript-patterns`. Read it when a lint configuration for TypeScript is created or
> changed, a type-aware rule is enabled, a suppression is added, or lint becomes slow. The other sections and the
> guardrails stay in `SKILL.md`. Pinned to **typescript-eslint 8.71** (read 2026-10-02, `references/origin.md`).

1. **Type-aware rules need the type checker, so they need a project.** Rules that read types (floating promises,
   unsafe `any` flows, unnecessary conditions) ask the compiler about the whole program, not the one file. Two
   changes turn them on: use the preset variants whose name ends in "type checked" instead of the plain ones, and
   give the parser a way to find each file's `tsconfig`. The recommended way is the parser's project service
   option set to true; the older explicit list of config paths still works. In the legacy configuration format
   the root directory of the `tsconfig` must be given as well.
2. **Know what each preset contains before choosing.** `recommended` is the base; `strict` adds opinionated rules
   and the plugin suggests it when most of the team is comfortable with the language and the plugin; `stylistic`
   enforces concise, consistent code patterns (consistency rather than bugs). Each has a type-checked version,
   and a "type-checked-only" version that holds just the rules needing types, for layering on top of the
   untyped preset. Every preset except `all`, `strict` and `strict-type-checked` is stable: additions and
   removals happen only in a major release. Those three may change in a minor, so a project on them expects new
   findings when it upgrades, and pins the plugin version in the lock file to choose when.
3. **Three rules this repository tells you to enable are in no preset except `all`.** The consistent type-imports
   rule, the switch exhaustiveness rule and the explicit module boundary types rule are not part of
   `recommended`, `strict` or `stylistic`, in either variant. Enable them by name, with the options below, or the
   "enforced in CI" lines in §6.8 are not true of the project. Check the rule list of the installed version,
   not the preset's reputation.
4. **Enabling one typed rule does not need the whole typed preset,** but it still needs the parser's project
   option on the files it covers, or the rule cannot get types for them.
5. **Files outside the compiler's project are the usual first failure.** The error says the file is not in any
   `tsconfig`. Fix it in this order: add the file to the project's `include` (a tooling config file belongs in a
   small separate config), turn type-aware linting off for it with the preset made for that (the
   disable-type-checked preset, applied to a `files` glob such as plain JavaScript), and only last use the
   project service's allow-default-project list, which is capped (eight files by default, no `**` globs) because
   every file it admits is slow. An `include` that is too wide (`**/*`, or none, which means the same) makes the
   linter parse build output and is a performance bug, not a convenience.
6. **Lint time is roughly build time, so slowness has two suspects.** A slow rule: run the timing option of the
   linter with one type-aware rule at a time, because the first one always looks slowest (it pays for the
   compiler's caches). Or slow types: if the bare compiler is slow on the project, the linter will be too; use the
   compiler's tracing and project references. Out-of-memory crashes come from huge or deeply recursive types; simplify them
   first, and raise Node's old-space limit only as a last resort. Editors cache and so feel faster; the full lint
   runs in CI.
7. **After a file changes on disk, editor findings can be stale.** The linter has no way to tell the editor which
   other files a result depended on, so imported types can be out of date and produce phantom unsafe-`any`
   reports. Restart the linter server before debugging a finding that contradicts the code.
8. **The rules that carry the most weight, and how to set them.**
   - Floating promises: a promise statement must be awaited, returned, given a two-argument `then` or a one-argument
     `catch`, or voided on purpose; an array of promises is reported until combined with one of the concurrency
     helpers. It does not look at promises placed in conditions or callbacks.
   - Misused promises: covers exactly those places (a promise in an `if`, an async function where a callback must
     return nothing, a spread). Keep both rules, because each covers what the other does not.
   - Return-await: use the in-try-catch mode (or always). A returned promise must be awaited inside `try`, and
     inside `catch` when a `finally` follows, or the handler never runs; elsewhere it is style. The mode that never
     awaits is deprecated.
   - Unnecessary condition: relies on the compiler's null checking and flags a valid check on an indexed
     access as unnecessary, because the compiler assumes an index lookup always succeeds. The plugin's own
     remedies are the unchecked-indexed-access compiler option (§6.2, which it calls often unwieldy) or the
     `at` method for a possibly out-of-range read, with a targeted suppression last.
   - Switch exhaustiveness: set it to also report a redundant `default` on a switch that already covers the
     union, so a new union member cannot hide behind it; keep a deliberate `default` only where values from a
     newer peer can outrun the types (a client older than its server), with that reason in the pull request.
   - The no-explicit-any, no-non-null-assertion and the unsafe-assignment, unsafe-argument and unsafe-return rules
     are what keep §1 true after the first deadline.
   - The suppression-comment rule defaults to: ignore and no-check directives reported, expect-error allowed only
     with a description. Keep that default; prefer expect-error to ignore because it fails when the error goes
     away.
9. **A suppression names its rule and its reason, and is scoped to one line.** A file-wide disable for a typed
   rule hides the next real bug in that file. A rule that is wrong for the whole project is turned off in the
   configuration with the reason in the pull request, not in a hundred suppressions.
10. **Formatting is a formatter's job.** The plugin's stylistic rules are not formatting; do not enable
    formatting-shaped rules in the linter and run a formatter beside it.
11. **Check the supported ranges before bumping the compiler.** At 8.71 the plugin supports ESLint 8.57, 9 and 10,
    Node 18.18, 20.9 and 21.1 or later, and TypeScript from 4.8.4 up to **below 6.1.0** (it mirrors a two-year
    support window and does not support beta releases). A compiler outside that range gets no support and no
    accepted bug reports, so a TypeScript major bump is a lint-tooling question first (§11).
