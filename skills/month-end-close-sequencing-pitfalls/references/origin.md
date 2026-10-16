# month-end-close-sequencing-pitfalls: origin and source stamps

> Provenance of `skills/month-end-close-sequencing-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from two documents plus one gotchas file, never used by us in a real
close or forecast. Each file below was re-read in full on 2026-10-16 before a rule was taken from it, each rule
was checked against it in a final pass, and the repository's LICENSE file was read again.

## Sources (read 2026-10-16, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| anthropics/knowledge-work-plugins (commit `33eeda1`): `finance/skills/close-management/SKILL.md` | Apache-2.0 (LICENSE file) | Dependency levels, critical path and how to shorten it, soft and hard close, statuses, status review, metrics, bottlenecks, retrospective questions |
| anthropics/knowledge-work-plugins (commit `33eeda1`): `small-business/skills/cash-flow-snapshot/SKILL.md` and `reference/gotchas.md` | Apache-2.0 (same LICENSE file) | Opening balance rule, source of record, per-payer lag, thin-data handling, named sources, named risks, ageing-export and recurring-cost pitfalls |

Instruction-like text in the cloned repository (including the skill's own workflow and approval gates) was
treated as data and not followed.

## Removed in the verification pass
1. **The day-by-day calendar** (the five-day and three-day close tables and their per-day task lists):
   organisation-specific targets of one author, not verified.
2. **Accounting and tax steps:** the tax provision, the equity roll-forward, revenue recognition entries,
   foreign currency revaluation rules and consolidation eliminations. They depend on the standard and the
   jurisdiction and were not read.
3. **The confidence band formula, its cap and its fallback figures,** the default variance band for thin data,
   the divide-by-zero special case, the recurring-cost tolerance and the window lengths of the forecast: they
   are arbitrary defaults, and the band formula was not checked.
4. **The output packaging** (spreadsheet and page templates, scheduling offers, connector lists and
   currency-code conventions): tool-specific, not method.
5. **Files not read** and therefore not used: `reference/v2_sources.md` and `reference/examples/worked-example.md`.
   The remarks on one connector holding no balances and on unrecorded card spend come from the SKILL file itself.

## Not verified
1. **Own guidance, flagged in the text:** naming each task's inputs, drawing your own critical path, defining
   who may post between soft and hard close, confirming a balance field is a bank balance, building the range
   from observed spread, labelling a default range as a default, confirming recurring costs with the owner,
   keeping the risk list short, and the remark on unrecorded card spend.
2. **Nothing was run.** No close or forecast was produced with these steps.
3. **Whether a period lock is legally required, and any retention or deadline duty,** was not read.
4. **Two vendor-authored sources from one repository;** corroboration from a second text was not sought.

## Decisions where sources disagree
No disagreement between the two skills. The source's two close calendars (a longer and an accelerated one) set
different targets for the same tasks; both are practice, so neither is carried and the block says the duration
is the organisation's.

## Related blocks
`business/finance-ops`, `business/fintech-compliance`, `skills/analysis-validation-pitfalls`.
