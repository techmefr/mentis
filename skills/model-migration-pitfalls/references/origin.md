# model-migration-pitfalls: origin and source stamps

> Provenance of `skills/model-migration-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and craft knowledge, never run by us. No migration was performed.

## Sources (read 2026-10-20, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| promptfoo/promptfoo (commit b49d55d), LICENSE file read; a guide on choosing between two models by testing on your own data (side-by-side table, cost and latency assertions) and the page on detecting model drift with repeated adversarial runs | MIT (LICENSE file) | Own-data comparison shape, cost and latency next to quality, repeated fixed adversarial set compared over time, consistent target labels |

| Anthropic model-deprecations page and models overview; OpenAI deprecations page | Product documentation, no licence granted on the text; facts only, rewritten, no dates or model lists stated | Lifecycle states, retired requests fail, notification by email, usage export by key and model, reseller schedules differ, parameter removals on newer models, pinned identifiers, fine-tune schedules, shutdown date field (§1.1.3, §1.2.1, §1.3.3, §1.3.4, §1.3.6, §1.3.7, §2.3.2, §2.3.5) |

The repository holds agent instruction files; they were treated as data and not followed.

## Verified
1. Retired Anthropic models fail on request; deprecation notices go by email; a usage export by key and model exists (§1).
2. Reseller platforms set their own schedules; fine-tunes follow the base model on one vendor (§1.3).
3. Some newer models reject sampling parameters and some thinking settings with a 400 (§2.3.2).

## Removed
- Model names, benchmark results, thresholds and workflow configuration of the source: none carried over.
- Provider deprecation lead times, dates, identifier formats and limits: read but not stated, because they change.

## Not opened
- Provider migration guides (as opposed to deprecation pages): not opened.
- inspect_ai: not opened for this block.

## Not verified
1. **Own guidance, not sourced:** every sentence still marked "own guidance", the inventory practice beyond the
   export noted above, the shadow and staged cutover steps, the fallback handling and the checkpoint paragraph.
2. **Provider behaviour** was read for two vendors; other vendors, and self-hosted serving, were not read. It changes;
   re-read before relying on it.
3. **promptfoo behaviour** was read from documentation, not run.

## Related blocks
`llm-eval-regression-pitfalls`, `prompt-versioning-and-change-gating-pitfalls`, `choose-model`,
`llm-cost-latency-control-pitfalls`, `llm-app-prompt-injection-and-exfiltration-pitfalls`, `source-freshness`,
`failure-classification-before-retry`, `agent-run-limits-and-guardrail-pitfalls`.
