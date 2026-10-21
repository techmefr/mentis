# agent-memory-and-state-pitfalls: origin and source stamps

> Provenance of `skills/agent-memory-and-state-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Never dogfooded. Nothing was run or built while writing it.

## Sources (read 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| LangGraph repository LICENSE, and its persistence and stores documentation pages | MIT (licence file read) | Checkpoints scoped per thread, in-memory checkpointer lost on restart, checkpoints accumulate with a suggested cleanup job (§1.2.5, §2.2.5); namespace-keyed memory, prefix reads, silent result limit (§2.1.5, §2.1.6) |
| Letta repository LICENSE, and its agent memory guide | Apache-2.0 (licence file read) | Agents edit their own memory through tools, a block can be attached to several agents (§1.1.5) |

| Mem0 repository LICENSE and its documentation pages on update, delete, memory expiration, entity-scoped memory | Apache-2.0 (licence file read 2026-10-20) | Expiration hides without deleting, malformed date fails open, scope fields not required to be null, delete then verify (§2.1.8, §2.2.1, §2.2.6, §2.3.1) |
| Google ADK documentation repository LICENSE and its state and memory pages | Apache-2.0 (licence file read 2026-10-20) | Prefix-scoped state levels, in-memory services lost on restart (§1.2.5, §2.1.7) |
| Anthropic memory-tool documentation page | Product documentation, facts only, read 2026-10-20 | Sensitive data validation, size caps, expiry of unused files, path traversal (§1.2.2, §1.2.6, §2.2.3) |

LangGraph and Letta pages were re-opened on 2026-10-20 at their current addresses, because the earlier pages moved. LangGraph: stores, checkpointers and memory concept pages (MIT, licence file re-read). Letta: memory and MemFS pages (Apache-2.0, licence file re-read).

Facts only; the points are rewritten in our words.

## Verified
1. User-scoped memory keyed by a namespace is a real design in a mainstream framework, which supports the
   "scope key in every read" rule (§2.1.1) in shape; the scope-before-ranking order was not tested.
2. Agents writing their own memory is a real feature, which supports treating the model's choice as a write path (§1.1.2).
3. No automatic expiry was documented for stored items in the pages read, so §2.2 lifetimes stay the caller's job.

4. Re-checked 2026-10-20: prefix reads, silent truncation at the default of ten, backend-dependent order, in-memory store for development only (LangGraph stores page); thread identifier as key and storage growth (checkpointer page).
5. **Corrected:** the former claim that a memory block can be attached to many agents came from a page that has moved; the current Letta pages describe shared memory repositories and a version history, and the text now says so. The former claim that a cron-style deletion was suggested for checkpoints was not found on the current pages and is dropped; the current pages show a growth note and pruning operations instead.
6. Newly sourced pitfalls: path escape (§1.2.6), scope level (§2.1.7), unspecified scope field (§2.1.8), expiry is not deletion (§2.2.6).

## Removed
- Product-specific behaviour beyond the pages read; numeric limits other than the documented default of ten results,
  which is framework specific and given only as an example.
- Microsoft HAX toolkit and Google PAIR material are not relevant here and were not used.

## Not verified
1. **Still own guidance, not sourced:** write gating by user statement (§1.1.1, §1.1.2), provenance fields (§1.1.3), facts
   not instructions (§1.2.1), summary drift (§1.2.3), task state files (§1.2.4), the tests and diagnosis in §3, derivation
   links for deletion (§2.3.1 beyond the verify step), visible use of memory (§2.2.4). Searched: LangGraph, Letta, Mem0, ADK
   and the Anthropic memory-tool pages; none documents poisoning through stored memory.
2. **Vector store filtering** (before or after the nearest-neighbour search): the stores page does not document filter
   behaviour; re-read the store in use. Read-only blocks and block size limits were not covered by the Letta page.
3. **Poisoning through memory** is described from the general mechanism of indirect injection; the attack was
   not reproduced.

## Related blocks
`agent-context-hygiene-pitfalls`, `llm-app-prompt-injection-and-exfiltration-pitfalls`, `llm-pii-and-data-handling-pitfalls`,
`rag-retrieval-quality-pitfalls`, `multi-agent-design-pitfalls`, `agent-run-limits-and-guardrail-pitfalls`.
