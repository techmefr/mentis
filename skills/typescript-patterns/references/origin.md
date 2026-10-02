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
