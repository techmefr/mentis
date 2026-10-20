# serverless-edge-worker-pitfalls: origin and source stamps

> Provenance of `skills/serverless-edge-worker-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation-style skill files, never run by us on a serverless platform. No
function was written, deployed or tested while writing it.

## Sources (read 2026-10-20, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| cloudflare/skills at commit 86505e4 (2026-10-15): `skills/workers-best-practices/SKILL.md`, `references/configuration.md`, `references/runtime-patterns.md`, `references/platform-apis.md`, `rules/workers.mdc` | Apache-2.0 (`LICENSE` read 2026-10-20; the repository's `NOTICE` was not looked for) | Compatibility date and flags, bindings and types, secrets, observability, shared state, promise lifetime, streaming, fail-open handling, queues, workflows, service bindings, pooling service, serialization table |
| cloudflare/skills at 86505e4: `skills/durable-objects/SKILL.md`, `references/rules.md` | Apache-2.0 (same file) | One object per entity, reconstructible state, SQL-backed storage, hibernation, migration entry |

## Removed (stated in the sources, not carried)
- The Wrangler command-line skill, the sandbox, email, Turnstile, Zero Trust, Next.js-on-Cloudflare, agents SDK and profiling skills: other subjects, not read.
- All code samples, the platform-specific limits table values (memory size, CPU milliseconds, background time limit, sampling-rate examples), the pooling service's latency figure and the validation library's version number as recommendations.
- The source's retrieval-first instruction (a harness behaviour) and its documentation URL tables.

## Not verified
1. **Limits.** The memory cap, CPU limits per plan and the background-work time limit are stated in the files and not recited here; the figures in the files differ between their own pages (the files mention both a bundled and a standard CPU limit) and were not checked against the live limits page.
2. **Configuration keys and command names** (observability switches, type generation, secret command, compatibility flag name) are the files' claims at the commit; none was run.
3. **Non-Cloudflare platforms.** Section 3.6, the "freeze after response" remark (§2.2.5) and the timeout ordering are our own guidance; no AWS or other platform source was read. Re-read the platform's documentation before relying on them.
4. **Durable objects.** Only the rules file and skill summary were read; storage-gate, alarm and migration semantics were not.
5. **Own guidance, labelled in the text:** the shared-memory-cache caution (§2.1.3), the write-retry caution (§3.2.2), and every "Checks" section.

## Related blocks
`nestjs-reliability` and `queue-worker-runtime-pitfalls` (long-lived workers), `postgres-operations-and-exposed-api-pitfalls`
(connection budget), `secret-leak-response-pitfalls`, `observability-instrumentation`, `source-freshness`.
