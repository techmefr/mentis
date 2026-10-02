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

