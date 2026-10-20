# agent-memory-and-state-pitfalls: origin and source stamps

> Provenance of `skills/agent-memory-and-state-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Never dogfooded. Nothing was run or built while writing it.

## Sources (read 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| LangGraph repository LICENSE, and its persistence and stores documentation pages | MIT (licence file read) | Checkpoints scoped per thread, in-memory checkpointer lost on restart, checkpoints accumulate with a suggested cleanup job (§1.2.5, §2.2.5); namespace-keyed memory, prefix reads, silent result limit (§2.1.5, §2.1.6) |
| Letta repository LICENSE, and its agent memory guide | Apache-2.0 (licence file read) | Agents edit their own memory through tools, a block can be attached to several agents (§1.1.5) |

Facts only; the points are rewritten in our words.

## Verified
1. User-scoped memory keyed by a namespace is a real design in a mainstream framework, which supports the
   "scope key in every read" rule (§2.1.1) in shape; the scope-before-ranking order was not tested.
2. Agents writing their own memory is a real feature, which supports treating the model's choice as a write path (§1.1.2).
3. No automatic expiry was documented for stored items in the pages read, so §2.2 lifetimes stay the caller's job.

## Removed
- Product-specific behaviour beyond the pages read; numeric limits other than the documented default of ten results,
  which is framework specific and given only as an example.
- Microsoft HAX toolkit and Google PAIR material are not relevant here and were not used.

## Not verified
1. **Everything not listed under Verified** remains own guidance: write gating, provenance fields, poisoning through
   memory, summary drift, deletion cascading, the tests in §3.
2. **Vector store filtering** (before or after the nearest-neighbour search): the stores page does not document filter
   behaviour; re-read the store in use. Read-only blocks and block size limits were not covered by the Letta page.
3. **Poisoning through memory** is described from the general mechanism of indirect injection; the attack was
   not reproduced.

## Related blocks
`agent-context-hygiene-pitfalls`, `llm-app-prompt-injection-and-exfiltration-pitfalls`, `llm-pii-and-data-handling-pitfalls`,
`rag-retrieval-quality-pitfalls`, `multi-agent-design-pitfalls`, `agent-run-limits-and-guardrail-pitfalls`.
