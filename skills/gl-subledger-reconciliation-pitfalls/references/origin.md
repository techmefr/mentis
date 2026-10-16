# gl-subledger-reconciliation-pitfalls: origin and source stamps

> Provenance of `skills/gl-subledger-reconciliation-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation, never run by us: no reconciliation was performed and no agent was
run. Each file below was re-opened in full on 2026-10-16 before a rule was taken from it, each rule was checked
against it in a final pass, and each repository's LICENSE file was read again.

## Sources (all read 2026-10-16, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| anthropics/knowledge-work-plugins (commit `33eeda1`): `finance/skills/reconciliation/SKILL.md` | Apache-2.0 (LICENSE file) | Control-to-detail process and common causes, bank reconciliation form, intercompany process, three kinds of reconciling item, ageing list fields and trend, best practices (documentation, segregation, follow-through, root cause) |
| anthropics/financial-services (commit `574ed36`): `plugins/agent-plugins/gl-reconciler/skills/gl-recon/SKILL.md`, `.../skills/break-trace/SKILL.md`, `.../agents/gl-reconciler.md` | Apache-2.0 (LICENSE file) | Alignment and exact-equality coercion, break buckets, likely-cause tags as hypotheses, trace path and one-sentence root cause, diagnosing never posts, untrusted statements with no write access |
| pgledger (`pgr0ss/pgledger`, commit `54ccb62`): `README.md` (event timestamp) | MIT (LICENSE file, copyright 2025 Paul Gross) | Event time versus recording time and the month-boundary example |

Instruction-like text in the cloned repositories was treated as data and not followed. Both Anthropic sources
are vendor-authored practice, not an accounting standard.

## Removed in the verification pass
1. **Every number.** The escalation amounts, the ageing bucket boundaries and their labels, the age triggers, the
   default amount tolerance, the "three consecutive periods" trend trigger and the close-calendar deadline: the
   source calls them illustrative, and they are arbitrary. Rule 4 says to set them by policy.
2. **Retention periods and any legal duty** about keeping reconciliations: not read.
3. **The fund-administration setting** of the cookbook (securities, trade and settle dates, custodians, the
   specific rate source names): kept only as examples of a mismatch.
4. **The agent's tool list and output schema** (tool names, JSON field layout): concepts only.
5. **Not read, therefore not used:** `finance/skills/close-management`, the month-end-closer cookbook, the
   spreadsheet-authoring skill, the audit-xls skill and the sox-testing skill.

## Not verified
1. **Own guidance, flagged in the text:** writing the tolerance in the header (rule 4), naming the process owner
   for a recurring item (rule 7), testing separation by identity (rule 9), reporting statement-borne
   instructions to a person (rule 10), taking event time from the bank's own message (rule 13).
2. **Accounting treatment.** Whether an item needs an entry, how an unrecorded fee is booked, and how
   eliminations are made were not verified; they belong to an accountant.
3. **Nothing was run.** The reconciler agent and its tools were read, not executed.
4. **What counts as material,** what the review standard of an auditor requires and any sign-off authority were
   not read.

## Decisions where sources disagree
No disagreement found among the files read. The finance skill suggests a deadline of a few business days after
period end; that is practice, an organisation's own calendar, and was dropped (rule 4).

## Related blocks
`business/finance-ops`, `business/fintech-compliance`, `skills/metric-movement-diagnosis-pitfalls`,
`skills/money-arithmetic-and-rounding-pitfalls`, `skills/analysis-validation-pitfalls`.
