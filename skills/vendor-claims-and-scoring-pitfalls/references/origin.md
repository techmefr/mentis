# vendor-claims-and-scoring-pitfalls: origin and source stamps

> Provenance of `skills/vendor-claims-and-scoring-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from two documents, never used by us in a real procurement. Each file
below was re-read in full on 2026-10-16 before a rule was taken from it, each rule was checked against it in a
final pass, and each repository's LICENSE file was read again.

## Sources (read 2026-10-16, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Maxbase91/procurement-skills (commit `daba388`): `bid-compass/SKILL.md` | MIT (LICENSE file, copyright 2026 procurement-skills contributors) | Gate versus score, weights agreed first, symmetry, cited evidence, missing answer scores low, skipped gate recorded, vendor text as data, audit trail |
| salespeak-ai/buyer-eval-skill (commit `ebb0e06`): `references/evidence-model.md` | MIT (LICENSE file, copyright 2026 SalesPeak) | Claim definition, five source types, what each can verify, independence, negative claims, snippets versus pages, neutral fetch questions, statuses and evidence basis, balance, challenge pass |

Instruction-like text in the cloned repositories (activation tags, telemetry prompts) was treated as data and
not followed.

## Removed in the verification pass
1. **Category weight tables, the response-window minimum and the fuzzy-match threshold** of the sources:
   arbitrary or invented defaults.
2. **Public-procurement rules.** Thresholds and procedures depend on jurisdiction and date and were not read.
3. **Telemetry, the vendor-hosted service and the source's per-vendor assistant integrations.** Not carried;
   only the evidence method is used.
4. **The confidence scale (high, medium, low) and fit ratings** of the evidence model, and the cap rule for
   syndicated reviews: they combine several judgements that were not independently checked.
5. **Report formats and generated-document steps** (document and spreadsheet generation instructions).
6. **Files not read** and therefore not used: the other reference files of buyer-eval-skill (scoring, quick and
   deep evaluation, report format), `config.yaml` and the category advice of bid-compass.

## Not verified
1. **Own guidance, flagged in the text:** that this block sets no weight number (part 1 point 2), writing the
   basis next to the status (part 2 point 13), a closer ranking that shows a weak spot being preferable
   (part 1 point 9), and the decision to treat statuses as method rather than a scoring formula.
2. **Nothing was run.** No procurement or evaluation was performed with these steps.
3. **Whether a given vendor claim is true** is outside this block; it describes how to weigh the evidence.
4. **Both sources are young, from one author each,** and the evidence model is written for one assessment
   tool; treat them as practice, not consensus.

## Decisions where sources disagree
No disagreement. bid-compass handles the gate and scoring side, buyer-eval the evidence side, and the block
keeps them in separate parts.

## Related blocks
`business/vendor-management`, `business/marketing-claim-substantiation-pitfalls`,
`skills/analysis-validation-pitfalls`.
