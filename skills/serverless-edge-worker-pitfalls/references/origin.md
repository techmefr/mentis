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
| Cloudflare documentation: Workers limits, Queues delivery guarantees | product documentation, facts only, rewritten, read 2026-10-20 | Memory, CPU and background time figures, at-least-once delivery |
| AWS Lambda developer guide: execution environment lifecycle | product documentation, facts only, rewritten, read 2026-10-20 | Freeze after return, reuse, initialisation outside the handler, global variables |

## Removed (stated in the sources, not carried)
- The Wrangler command-line skill, the sandbox, email, Turnstile, Zero Trust, Next.js-on-Cloudflare, agents SDK and profiling skills: other subjects, not read.
- All code samples, the platform-specific limits table values (memory size, CPU milliseconds, background time limit, sampling-rate examples), the pooling service's latency figure and the validation library's version number as recommendations.
- The source's retrieval-first instruction (a harness behaviour) and its documentation URL tables.

## Not verified
1. **Limits.** Checked 2026-10-20 against the live limits page: the figures now quoted in §2.2 and §2.3 (30 s background, 128 MB, CPU per plan). They change; re-read before relying on them.
2. **Configuration keys and command names** (observability switches, type generation, secret command, compatibility flag name) are the files' claims at the commit; none was run.
3. **Non-Cloudflare platforms.** The freeze-after-response remark (§2.2.5) and warm-reuse points (the "Other platforms" heading of part 3, points 1 and 3) are now checked against the Lambda guide only; the timeout ordering (same heading, point 2) and other platforms stay own guidance.
4. **Durable objects.** Only the rules file and skill summary were read; storage-gate, alarm and migration semantics were not.
5. **Own guidance, labelled in the text:** the shared-memory-cache caution (§2.1.3), the write-retry caution (§3.2.2), and every "Checks" section.

## Related blocks
`nestjs-reliability` and `queue-worker-runtime-pitfalls` (long-lived workers), `postgres-operations-and-exposed-api-pitfalls`
(connection budget), `secret-leak-response-pitfalls`, `observability-instrumentation`, `source-freshness`.
