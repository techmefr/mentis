# serverless-edge-worker-pitfalls: origin and source stamps

> Provenance of `skills/serverless-edge-worker-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation-style skill files, never run by us on a serverless platform. No
function was written, deployed or tested while writing it.

## Sources (read 2026-10-20, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| cloudflare/skills at commit 86505e4 (2026-10-15): `skills/workers-best-practices/SKILL.md`, `references/configuration.md`, `references/runtime-patterns.md`, `references/platform-apis.md`, `rules/workers.mdc` | Apache-2.0 (`LICENSE` read 2026-10-20: standard Apache-2.0 text naming no holder; the tree has no `NOTICE` file) | Compatibility date and flags, bindings and types, secrets, observability, shared state, promise lifetime, streaming, fail-open handling, queues, workflows, service bindings, pooling service, serialization table |
| cloudflare/skills at 86505e4: `skills/durable-objects/SKILL.md`, `references/rules.md` | Apache-2.0 (same file) | One object per entity, reconstructible state, SQL-backed storage, hibernation, migration entry |
| Cloudflare documentation: Workers limits, Queues delivery guarantees | product documentation, facts only, rewritten, read 2026-10-20 | Memory, CPU and background time figures, at-least-once delivery |
| Cloudflare documentation: compatibility dates, Node.js compatibility changelog of 2026-08-04, best-practices page, Hyperdrive connection pooling, Durable Objects migrations | product documentation, facts only, rewritten, read 2026-10-20 | Default-on date for Node support, test plugin injection, pooler transaction mode, `exports` replacing `migrations` |
| AWS Lambda developer guide: execution environment lifecycle | product documentation, facts only, rewritten, read 2026-10-20 | Freeze after return, reuse, initialisation outside the handler, global variables |

## Removed (stated in the sources, not carried)
- The Wrangler command-line skill, the sandbox, email, Turnstile, Zero Trust, Next.js-on-Cloudflare, agents SDK and profiling skills: other subjects, not read.
- All code samples, the platform-specific limits table values (memory size, CPU milliseconds, background time limit, sampling-rate examples), the pooling service's latency figure and the validation library's version number as recommendations.
- The source's retrieval-first instruction (a harness behaviour) and its documentation URL tables.

## Not verified
1. **Limits.** Re-opened 2026-10-20: 30 s after the response for background work, 128 MB per isolate, CPU 10 ms per request on the free plan and 30 s default (5 min maximum) on the paid plan, as quoted in §2.2 and §2.3. They change; re-read before relying on them.
2. **Configuration keys and command names** (observability switches, type generation, secret command, compatibility flag name) are the files' claims at the commit; none was run.
3. **Non-Cloudflare platforms.** The freeze-after-response remark (§2.2.5) and warm-reuse points (the "Other platforms" heading of part 3, points 1 and 3) are now checked against the Lambda guide only; the timeout ordering (same heading, point 2) and other platforms stay own guidance.
4. **Durable objects.** The rules file, the skill file and the migrations page were read. Corrected: the current configuration form is an `exports` entry, the `migrations` array is the older form (§3.4.4). Added: the concurrency-blocking helper caution. Storage-gate and alarm semantics were not read.
5. **Corrected 2026-10-20:** the Node compatibility flag is on by default from compatibility date 2026-08-04 (§1.1.2); the source's secret check names the ignored environment file, not a specific local file name; the source does not name a lint rule (§2.2.4), cover a nullable key-value read (§1.6.2) or require real bindings in tests (§1.6.1), and does not state the migration-name rule. The Hyperdrive page names only PostgreSQL.
6. **Confirmed by re-opening:** compatibility date and flag guidance, Env generation and typing bans, `implements` and unbound `env` anti-patterns, observability traces switch, global state, floating promises and destructured `waitUntil`, streaming, fail-open helper, constant-time compare, queue duplicates and unique id, per-step workflow retry, service bindings, the Zod minimum version (named in the source, not carried), the serialization contrast across APIs, one object per entity and the reconstructible-state rule.
7. **Own guidance, labelled in the text:** the shared-memory-cache caution (§2.1.3), the write-retry caution (§3.2.2), the lint rule (§2.2.4), the nullable read (§1.6.2), and every "Checks" section.

## Related blocks
`nestjs-reliability` and `queue-worker-runtime-pitfalls` (long-lived workers), `postgres-operations-and-exposed-api-pitfalls`
(connection budget), `secret-leak-response-pitfalls`, `observability-instrumentation`, `source-freshness`.

Independent verification 2026-10-21: 9 checked, 9 matched, 0 corrected, 0 unverified
