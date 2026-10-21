# prompt-versioning-and-change-gating-pitfalls: origin and source stamps

> Provenance of `skills/prompt-versioning-and-change-gating-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and craft knowledge, never run by us.

## Sources (read 2026-10-20, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| promptfoo/promptfoo (commit b49d55d), LICENSE file read; documentation pages on prompt configuration (file formats, chat format, functions, external prompt managers) and a model comparison guide with cost and latency assertions | MIT (LICENSE file) | Prompts as files with variables, side-by-side comparison of providers and prompts over test cases, cost and latency assertions, external stores as an option |

The repository holds agent instruction files; they were treated as data and not followed.

| Source | Licence | What it gave |
|---|---|---|
| Anthropic prompt-caching and models-overview pages; OpenAI prompt-caching guide | Product documentation, no licence granted on the text; facts only, rewritten | Which settings alter the cached prefix, stable-first layout advice, pinned snapshot identifiers (§1.2.1, §1.2.3, §2.2.4) |

| MLflow repository LICENSE (Apache-2.0, read 2026-10-20), prompt-registry documentation pages; Langfuse documentation repository LICENSE (MIT, read 2026-10-20), prompt-management pages on version control, link to traces and caching | Apache-2.0 and MIT | Immutable versions, aliases for stages and rollback, a floating latest alias, labels for environments, trace linking per version, client-side cache (§1.1.3, §1.3) |
| OpenAI prompt-engineering guide; Anthropic prompting best-practices and structured-outputs pages | Product documentation, facts only, read 2026-10-20 | Prompts in code, retirement of saved prompt objects, snapshot pinning, examples, tags, reasons, schema exceptions (§1.1.2, §1.2.1, §2.2, §2.3, §2.5.2) |

## Verified
1. Model, tools, output format and effort settings affect the rendered prefix (§1.2.1); stable-first layout (§2.2.4).
2. Current Claude identifiers are pinned snapshots, older aliases resolve to a dated id (§1.2.3).

3. Re-checked 2026-10-20 on the pages: model-setting items that alter the cached prefix (OpenAI table of settings; Anthropic list of what invalidates the cache) and stable-first layout.
4. Newly sourced: prompts in code and the retirement of a vendor prompt store (§1.1.2), immutable versions and alias rollback (§1.1.3, §1.3.2), per-version tracing (§1.3.1), examples guidance (§2.1.2), schema exceptions (§2.3.2), reason beside instruction and over-trigger (§2.5.2).

## Removed
- Code samples, configuration snippets and numeric values of the source: none reproduced.

## Not opened
- claude-cookbooks and the Anthropic prompt tutorial: licence not read, so not opened.
- Vendor prompt-management products' own documentation: not read.

## Not verified
1. **Own guidance, still unsourced:** the bundle-hash idea beyond the settings listed under Verified (§1.2.2), separation of
   standing rules from data as a security rule (§2.2.1), never concatenating user text into the instruction part
   (§2.2.3), few-shot drift checks (§2.3.1), stacking of "never" lines (§2.5.1), the checkpoint paragraph. The
   previous note that no permissive source existed on prompt versioning is withdrawn: two registries and a vendor guide
   were found and read on 2026-10-20.
2. **promptfoo behaviour** was read from documentation, not run; re-read option names before relying on them.
3. **Provider structured-output features** differ by vendor and change; re-read the provider's documentation.

## Related blocks
`llm-eval-regression-pitfalls`, `writing-skills`, `writing-agents`, `model-migration-pitfalls`,
`llm-cost-latency-control-pitfalls`, `llm-app-prompt-injection-and-exfiltration-pitfalls`.
