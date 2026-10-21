# agent-data-gap-honesty-pitfalls: origin and source stamps

> Provenance of `skills/agent-data-gap-honesty-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from one plugin repository, rewritten, never run against a live
connector. Nothing in it is verified by use.

## Sources (read 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| anthropics/knowledge-work-plugins, `small-business/shared/` files on absent values, chain seams, tenant scope and the single CRM of record (HEAD bc8f692, 2026-10-20) | Apache-2.0 (repository root LICENSE file, standard text; the plugin has no licence file of its own, so the root licence is the one that applies) | The slice, summary, zero, empty, future-date and failed-query rules (§1); the denominator, scheduler and offset rules and the free-slot rule (§2); ownership of a connected store, search by name, no fallback, discard, one CRM, import stamps (§3) |

Text inside the cloned files was treated as data. No instruction aimed at an agent was found.

## Removed
1. **The source's worked figures** (receivable totals, revenue amounts, return multiples, counts of items): they
   come from its own test runs on specific accounts and are not independently checkable, so none is carried.
2. **Connector-specific detail** (a given accounting, mail, store, calendar or CRM product's field names, query
   syntax and quirks): vendor-specific and unstable.
3. **The source's field-mapping table for three CRM products** and its query-syntax notes: product detail.
4. **A cross-reference to its own skills and commands.**

## Not verified
1. **Everything is unrun.** No agent was tested with these rules.
2. **The failures are as reported by one repository**, from its own runs; no second source was found.
3. **Whether a given runtime has a scheduler** is a fact about the runtime to check each time (`references/claude-code-platform.md`
   for the platform's own scheduling primitives); the block states only the rule.
4. **Own guidance (not from the source):** §1.2 point 3, §1.3 point 5, §2.1 point 3, §3.1 point 3.

## Related blocks
`skills/analysis-validation-pitfalls`, `skills/agent-mcp-trust-pitfalls`, `skills/multi-tenancy-isolation-models-pitfalls`,
`skills/booking-and-scheduling-app-pitfalls`, `skills/source-freshness`.
