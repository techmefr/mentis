# redis-conventions: origin and source stamps

> Provenance of `skills/redis-conventions`. Read it when tracing a rule to its source or checking freshness
> (`skills/source-freshness`), never to apply a rule.

Written 2026-10-02 from primary sources only, all read that day. Status: **new block, base to confront with
a real project**, no in-house production experience (🟡 in `CATALOG.md`).

| Source | Read | Licence | Treatment |
|---|---|---|---|
| The vendor's public development skills repository for the server (modelling, connections, clustering, observability, security, search, semantic cache), last pushed 2026-09-08 | 2026-10-02 | MIT | Rewrite with credit. §1, §4, §5, §6, §7 take the mechanisms (structure by access pattern, key naming, pool or multiplex, pipelining, scan not keys, timeouts, hash tags, replica reads, metrics, least-privilege users) and re-explain them with the failure each one prevents |
| The vendor's documentation: key eviction, keys and expiration, persistence, transactions, scripting (EVAL intro), pipelining, publish-subscribe, distributed locks, security, latency, cluster specification (page versions "latest" on the read date) | 2026-10-02 | Documentation licence is non-commercial share-alike | **Idea only.** Facts were checked against it and every sentence here is our own wording; no phrasing, example or table is reused |

**Not taken.** The search-module, vector and semantic-cache skills: a separate subject with a preview
service in it, not covered here (see the search-engines block for the general search discipline). Client
code samples per language: they age fastest and the rules do not need them. Numeric defaults (slow-log
threshold, hit-ratio target, pipeline batch size): the vendor's examples give figures, none is a standard,
so none is recited; measure on the deployment.

**Disagreements resolved.** The vendor skill recommends renaming dangerous commands; the vendor's own
security documentation marks that directive deprecated in favour of access rules. The block follows the
documentation (§5.6).

**Version-bound statements.** Access control lists (6 and later), conditional string set and delete commands
(8.4 and later), client-side caching (needs the newer protocol). Re-read the "latest" pages before relying on
any of them for a server older than the read date.

**Reasoning of ours, not a source statement:** §2 points 2, 7, 8; §3 point 8 and the fencing clause of
point 9; §4 points 4, 6, 8; §7 point 4.
