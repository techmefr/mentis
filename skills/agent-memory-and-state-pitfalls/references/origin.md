# agent-memory-and-state-pitfalls: origin and source stamps

> Provenance of `skills/agent-memory-and-state-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Never dogfooded. Nothing was run or built while writing it.

## Sources (read 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| None | n/a | Every point is own guidance from craft experience. No external text was read or taken. |

Memory libraries and a memory-oriented skill collection were candidate sources in the review; their licence files
were not read here, so none of them was opened.

## Removed
- Product-specific behaviour of any memory library: not read, so none described.
- Numeric limits (entry caps, lifetimes, similarity thresholds): none verified, none given.

## Not verified
1. **Everything.** The whole block is own guidance; no point was checked against a store, a framework or a paper.
2. **Vector store filtering** (before or after the nearest-neighbour search) differs by product; re-read the
   documentation of the store in use.
3. **Poisoning through memory** is described from the general mechanism of indirect injection; the attack was
   not reproduced.

## Related blocks
`agent-context-hygiene-pitfalls`, `llm-app-prompt-injection-and-exfiltration-pitfalls`, `llm-pii-and-data-handling-pitfalls`,
`rag-retrieval-quality-pitfalls`, `multi-agent-design-pitfalls`, `agent-run-limits-and-guardrail-pitfalls`.
