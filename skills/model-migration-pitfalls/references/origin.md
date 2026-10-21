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

| Source (read 2026-10-20) | Licence | What it gave |
|---|---|---|
| Anthropic: model-deprecations page and models overview, re-opened for the exact figures and sentences credited; OpenAI: deprecations page; Microsoft Foundry: model retirements page; Amazon Bedrock: model lifecycle page | Product documentation, facts only, rewritten, no dates or model lists stated | Lifecycle states, 410 Gone on retired versions, automatic upgrades on managed deployments but not provisioned ones, programmatic status fields on three platforms, SDK treatment of removed parameters, pinned snapshots, tokenizer change (§1.2.1, §1.2.2, §1.3.4, §1.3.8, §2.3.2, §2.3.5) |

## Verified
1. Retired Anthropic models fail on request; deprecation notices go by email; a usage export by key and model exists (§1).
2. Reseller platforms set their own schedules; fine-tunes follow the base model on one vendor (§1.3).
3. Some newer models reject sampling parameters and some thinking settings with a 400 (§2.3.2).

4. Re-checked 2026-10-20 on the pages: email notice and usage export (Anthropic), shutdown date field and fine-tunes following the base (OpenAI), reseller schedules (Anthropic), SDK handling of removed parameters, models-endpoint fields, pinned snapshots before and after the 4.6 generation.
5. **Corrected:** the former wording said the Python SDK removed the sampling parameters; the deprecation page says most SDKs keep them and names the exception more narrowly, so the text now says one language's SDK.
6. Newly sourced concrete points: auto-upgrade on managed deployments (§1.2.2), 410 Gone (§1.3.4), programmatic lifecycle polling (§1.3.8), deprecated models being less reliable (§1.2.2).

## Removed
- Model names, benchmark results, thresholds and workflow configuration of the source: none carried over.
- Provider deprecation lead times, dates, identifier formats and limits: read but not stated, because they change.

## Not opened
- Provider migration guides (as opposed to deprecation pages): not opened.
- inspect_ai: not opened for this block.

## Not verified
1. **Own guidance, still unsourced:** self-hosted pinning (§1.2.4), lead time from your last migration (§1.3.2),
   keeping the set apart from the tuning set (§2.1.3), the fallback-model handling (§2.4), shadow and staged
   cutover (§2.5), the inventory practice beyond the export noted above and the checkpoint paragraph. Searched in
   the four lifecycle pages: they say nothing on shadow traffic or fallbacks.
2. **Provider behaviour** was read for two vendors; other vendors, and self-hosted serving, were not read. It changes;
   re-read before relying on it.
3. **promptfoo behaviour** was read from documentation, not run.

## Related blocks
`llm-eval-regression-pitfalls`, `prompt-versioning-and-change-gating-pitfalls`, `choose-model`,
`llm-cost-latency-control-pitfalls`, `llm-app-prompt-injection-and-exfiltration-pitfalls`, `source-freshness`,
`failure-classification-before-retry`, `agent-run-limits-and-guardrail-pitfalls`.

Independent verification 2026-10-21: 17 checked, 17 matched, 0 corrected, 0 unverified
