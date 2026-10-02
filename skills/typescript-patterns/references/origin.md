# typescript-patterns — origin and source stamps

> Provenance of `skills/typescript-patterns`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

Internal synthesis based on the operator's real production experience (long-standing JS/TS, see
`frodo`/`legolas`) and established TypeScript recommendations (official handbook on discriminated
unions, `as const`). No single external repo retained: this is a language block, not a framework one,
so there's no "expert X" source to credit as with the market-sourced framework conventions.

**Sections 4 to 7, 2026-10-02.** Sections 1 to 3 are the block as it was, moved unchanged into `references/`
when the block became a router. Sections 4 to 7 are new. Idea taken from two public repositories, read
2026-10-02: the ECC rules repository (MIT licence), whose TypeScript rule files covered the language at the
level of types, immutability, errors and validation, and the Front-End-Checklist repository (licence
unclear, so **no wording was taken**; only the list of topics was used to find the gap in browser-side
JavaScript, and every statement was written from the platform specifications and the vendor documentation).
Mechanisms rewritten in our terms. Differences on purpose: the upstream response-envelope type and the
generic repository interface are not adopted (`skills/api-design` and `skills/code-baseline` are our
position), the upstream console-output hook is not taken (the lint rule and the logging rule live in `skills/browser-runtime`, which was written in parallel from the same checklist topics and owns the browser-owned half: storage, the shape check after parsing, debounce, console output, messages and the error handler), and the type-versus-
interface advice already in §1 is not repeated. The facts come from the TypeScript handbook and compiler
option reference (strict family, indexed access, exact optional properties, `satisfies`, module syntax,
suppression directives), the HTML living standard and MDN for the storage, URL, abort, observer and
visibility behaviours, the Temporal proposal documentation for §7.8 and §7.9, and the Intl documentation,
written from knowledge of them and **not re-fetched on the day**. Re-verify before 🟢: the exact members of
the strict family (§6.1), the status of Temporal in the target runtimes (§7.8), and the lint rule names in
§6.8 against the installed plugin version.

**Function and type design, Node runtime, 2026-10-02.** §8 and §9 are new, from two public repositories read
that day from shallow clones, both MIT-licensed: the TypeScript style guide by `mkosir` (its skill references on
types, variables, functions, naming, discriminated unions, source organisation and tests, last commit
2026-09-03) for §8, and the Node skill of `mcollina/skills` (its rules on streams, graceful shutdown and stuck
processes, last commit 2026-08-17) for §9. Mechanisms rewritten in our terms; no sentence or example copied.
Differences on purpose: the guide's comment and TSDoc advice is not taken (this repository's house rule is no
comments in produced code), its React and test-description conventions are left to the framework blocks, and its
fixed lint-rule configuration is reduced to naming the rule where it exists. The `close-with-grace` and
`why-is-node-running` packages are named as the source names them; they were not installed or run here, and no
statement about their behaviour goes beyond what that source says. **Facts that move:** the lint rule names
(`explicit-module-boundary-types`) and the `erasableSyntaxOnly` option (TypeScript 5.8 and later) were taken from
the guide, not re-read in the typescript-eslint or compiler documentation. **Not read, a stated gap:** the
typescript-eslint rule documentation and the TypeScript handbook were not available among the cloned sources of this
pass; the Node documentation itself (streams, process signals) was not read, so §9 carries the claims of its
source only. §8.4 points to the existing enum rule in §3.


**Typed linting, compiler versions, typed database client, 2026-10-02.** §10, §11 and §12 are new, and two lines
of §6 are corrected. Primary sources, read the same day from shallow clones: the typescript-eslint repository
(MIT; documentation sources and the plugin's preset and rule files, plugin 8.71.0, the latest on the registry that
day) for §10; the TypeScript website repository (documentation licensed CC BY 4.0, code MIT; the 6.0 release
notes, the compiler-option reference pages for strict, verbatim module syntax, erasable syntax only,
side-effect imports and lib replacement, and the option-relations script that lists the strict family) for §11
and the §6 corrections; and the Prisma documentation repository (the version 7 tree, the release-status and
coming-from-7 pages) for §12. That last repository carries no licence file, so under rule B of
`CONVENTIONS.md` it is idea only: mechanisms and facts were taken and every sentence and example is ours. The
website's CC BY 4.0 documentation was likewise rewritten, with no copied sentence, attributed here to the
TypeScript documentation (Microsoft and contributors), not endorsed by the licensor.

**Corrections to earlier text, with their evidence.** (1) §6.1 listed eight members of the strict family; the
website's option-relations table lists nine, the ninth being the built-in iterator return check (in the table
against 5.6). (2) §6.8 and the earlier guidance implied that the consistent type-imports, switch-exhaustiveness
and explicit-boundary-types rules ship in the presets; the plugin's preset files contain none of the three
outside the `all` preset, now §10.3. (3) The earlier origin note said the exhaustiveness and boundary-types rule
names were taken from a style guide and not re-read; they now exist in the plugin's rule list at 8.71 (checked by
file), and the boundary-types rule carries no deprecation marker in its source.

**Facts that move, with their pin.**
- typescript-eslint 8.71: supported compiler range up to below 6.1.0, ESLint 8.57 to 10, Node 18.18 or later
  (§10.11); which presets are stable (§10.2); which rules are in which preset (§10.3). Re-read on each minor.
- TypeScript 6.0 defaults and deprecations (§11.2 to §11.5); the registry's latest compiler on the day was 7.0.2,
  and the documentation clone had release notes only through 6.0, so **nothing about 7.0 itself was read**: §11
  states only what the 6.0 notes say about 7.0, and the lint plugin's range. This is the largest gap in this pass.
- Prisma ORM 7.10 stable, 8.0 release candidate, general availability expected October 2026, the registry's
  tag split on the day (§12.1); the strict-undefined-checks and relation-joins features are previews in the 7
  tree (§12.4, §12.8); client error classes and the codes P2002, P2003, P2025 and P2034 (§12.6).

**Not read, stated.** The TypeScript handbook chapters on narrowing, generics and modules beyond what §1 to §9
already assert (this pass used the release notes and option reference, not the handbook pages); the
typescript-eslint rule pages beyond the ones named in §10.8; the Prisma transaction, extension, raw-SQL and
migration pages (the first is covered from another source in `skills/nestjs-node-conventions`); the Prisma 8
query API in depth. **Ruled out as instruction-like text in a source:** the Prisma query-optimization page
carries a prompt addressed to an AI coding assistant telling it to install and configure a package; it was read
as data and nothing was installed.
