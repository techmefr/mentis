# redis-security-and-observability-pitfalls: origin and source stamps

> Provenance of `skills/redis-security-and-observability-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation-style skill files, never run by us against a Redis server. No
instance was started, no ACL user created and no metric read while writing it.

## Sources (all read in full 2026-10-16, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| redis/agent-skills at commit a84871d (2026-09-08): `skills/redis-security/SKILL.md`, `references/auth.md`, `references/acls.md`, `references/network.md` | MIT, Copyright (c) 2026 Redis, Inc. (`LICENSE` re-read 2026-10-16; frontmatter `license: MIT`) | Authentication and TLS, ACL users and categories, bind, protected-mode and firewall, the `rename-command` example |
| redis/agent-skills at a84871d: `skills/redis-observability/SKILL.md`, `references/metrics.md`, `references/commands.md` | MIT (same file) | The seven INFO metrics and their example alert conditions, SLOWLOG, MEMORY, CLIENT, FT.INFO and FT.PROFILE, the GUI remark |

The redis/docs repository (CC BY-NC-SA 4.0) and valkey-io/valkey-doc (CC BY-SA 4.0) are idea-only for this
programme and were not read for this block. The `redis.io` links in the source files were not followed.

## Version bounds stated in the sources
None. The files give no Redis version for ACLs, TLS, the command categories, `slowlog-log-slower-than` or the
`FT.*` commands, and none is claimed. The skills' own metadata version (0.1.0) is the skills' version, not
Redis's.

## Removed (in the sources, not carried)
- The Java trust-store and `SSLContext` code and the Jedis and redis-py samples: replaced by prose.
- The `iptables` commands and the private-network addresses in the source's `bind` and firewall examples:
  replaced by a documentation address in the one kept sample and by prose.
- The Redis Copilot remark in the GUI paragraph: product description, not a rule.
- The `redis.io` reference links in both skills.
- The source's `rename-command` lines as a recommendation (§1.4), see the next list.

## Not verified
1. **`rename-command` could not be confirmed as current guidance.** The source shows it as an optional
   recommended step; the Redis documentation was not read (idea-only), so §1.4 prefers ACL command categories
   and tells the reader to verify the directive for their server version.
2. **ACL syntax and category contents** (`@read`, `@write`, `@dangerous`, `@admin`, which commands each holds)
   are as the source's table states them; the server's own list was not read.
3. **`slowlog-log-slower-than` default of 10 ms** and the duration unit are the source's statements.
4. **The 80 percent thresholds** (memory against `maxmemory`, hit ratio) are the source's examples and are
   labelled as such in the text.
5. **Own guidance, labelled in the text:** reading the credential from a secret store, checking category
   contents per server version, testing a refused command per user, hit ratio applying to caches only,
   setting thresholds from the instance's own data, recording the slow log before a reset, and every "Checks"
   section.

## Related blocks
`redis-client-and-cluster-pitfalls` (keys, connections, cluster), `datastore-broker-alerting-signals` (alert
rules against an exporter), `observability-instrumentation` (§4: what an alert must be), `security-hardening`,
`source-freshness`.
