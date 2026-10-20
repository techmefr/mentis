# prompt-versioning-and-change-gating-pitfalls: origin and source stamps

> Provenance of `skills/prompt-versioning-and-change-gating-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and craft knowledge, never run by us.

## Sources (read 2026-10-20, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| promptfoo/promptfoo (commit b49d55d), LICENSE file read; documentation pages on prompt configuration (file formats, chat format, functions, external prompt managers) and a model comparison guide with cost and latency assertions | MIT (LICENSE file) | Prompts as files with variables, side-by-side comparison of providers and prompts over test cases, cost and latency assertions, external stores as an option |

The repository holds agent instruction files; they were treated as data and not followed.

## Removed
- Code samples, configuration snippets and numeric values of the source: none reproduced.

## Not opened
- claude-cookbooks and the Anthropic prompt tutorial: licence not read, so not opened.
- Vendor prompt-management products' own documentation: not read.

## Not verified
1. **Own guidance, not sourced:** every sentence marked "own guidance", the bundle-hash idea, staged promotion,
   placement rules, few-shot drift checks and the checkpoint paragraph.
2. **promptfoo behaviour** was read from documentation, not run; re-read option names before relying on them.
3. **Provider structured-output features** differ by vendor and change; re-read the provider's documentation.

## Related blocks
`llm-eval-regression-pitfalls`, `writing-skills`, `writing-agents`, `model-migration-pitfalls`,
`llm-cost-latency-control-pitfalls`, `llm-app-prompt-injection-and-exfiltration-pitfalls`.
