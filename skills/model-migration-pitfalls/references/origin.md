# model-migration-pitfalls: origin and source stamps

> Provenance of `skills/model-migration-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and craft knowledge, never run by us. No migration was performed.

## Sources (read 2026-10-20, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| promptfoo/promptfoo (commit b49d55d), LICENSE file read; a guide on choosing between two models by testing on your own data (side-by-side table, cost and latency assertions) and the page on detecting model drift with repeated adversarial runs | MIT (LICENSE file) | Own-data comparison shape, cost and latency next to quality, repeated fixed adversarial set compared over time, consistent target labels |

The repository holds agent instruction files; they were treated as data and not followed.

## Removed
- Model names, benchmark results, thresholds and workflow configuration of the source: none carried over.
- Provider deprecation lead times, identifier formats and limits: not read, so not stated.

## Not opened
- Provider migration guides and deprecation pages: not re-read in this pass; idea-level knowledge only.
- inspect_ai: not opened for this block.

## Not verified
1. **Own guidance, not sourced:** every sentence marked "own guidance", the inventory and calendar practice, the
   shadow and staged cutover steps, the fallback handling and the checkpoint paragraph.
2. **Provider behaviour** (alias movement, retirement handling, parameter support) differs by vendor and changes;
   re-read before relying on it.
3. **promptfoo behaviour** was read from documentation, not run.

## Related blocks
`llm-eval-regression-pitfalls`, `prompt-versioning-and-change-gating-pitfalls`, `choose-model`,
`llm-cost-latency-control-pitfalls`, `llm-app-prompt-injection-and-exfiltration-pitfalls`, `source-freshness`,
`failure-classification-before-retry`, `agent-run-limits-and-guardrail-pitfalls`.
