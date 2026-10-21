# llm-pii-and-data-handling-pitfalls: origin and source stamps

> Provenance of `skills/llm-pii-and-data-handling-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Never dogfooded. Nothing was run or built while writing it. Not legal advice.

## Sources (read 2026-10-20, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| protectai/llm-guard (checkout in the working area), LICENSE file read; documentation pages of the anonymise input scanner, the deanonymise output scanner and the sensitive output scanner | MIT (LICENSE file) | Vault and placeholder round trip, entity and pattern detection, English-only note, threshold and allow or hide lists, upstream-training concern, leakage framing |
| microsoft/presidio (commit 4f0e236), LICENSE file read; documentation pages: home, languages, decision process, anonymiser | MIT (LICENSE file) | No-completeness statement, language-bound context words, one language per recogniser, hash salt behaviour, encrypt and decrypt, overlap resolution, diagnostic logging content (§1.2 points 6 to 8, §1.3 points 2 and 2a, §2.2 point 1a) |

## Removed
- Detector model names, benchmark latencies and the default threshold: not carried over; re-read before relying.
- Presidio documentation: not used in the first pass (no licence file in the local copy); a fresh clone on 2026-10-20 had an MIT LICENSE file, which was read, and it is now used (see the sources table).
- Any statement of what a given provider retains or trains on: not read.

## Not verified
1. **Everything still marked "own guidance"** after the 2026-10-20 sourcing pass (language, hashing, overlap, no-completeness and diagnostic-log points are now sourced to Presidio): logging, caching, embeddings, tuning sets, deletion cascade, tenant
   isolation and the seeded-identifier tests come from craft knowledge and were not checked against a product.
2. **Provider terms** change; read them for the endpoint and tier in use.
3. **Scanner behaviour** was read from documentation, not run; names and arguments may have changed.
4. **Legal conclusions** are deliberately absent. Lawfulness, lawful basis, retention periods and processor
   contracts are for a lawyer or the data protection officer.

## Related blocks
`telemetry-sensitive-data-pitfalls`, `gdpr-international-transfers-pitfalls`, `gdpr-breach-notification-and-dpia-pitfalls`,
`agent-memory-and-state-pitfalls`, `llm-app-prompt-injection-and-exfiltration-pitfalls`, `rag-retrieval-quality-pitfalls`,
`ml-training-and-evaluation-pitfalls`, `backup-restore-drill-pitfalls`, `ai-act-obligations-and-omnibus-status-pitfalls`.
