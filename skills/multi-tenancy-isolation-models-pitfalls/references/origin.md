# multi-tenancy-isolation-models-pitfalls: origin and source stamps

> Provenance of `skills/multi-tenancy-isolation-models-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from craft knowledge of multi-tenant software and the existing blocks of
this repository. No system was built or run while writing it.

## Sources
No external source was read for this block. The review of candidate sources found no permissively licensed
generic document on isolation models: the PostgreSQL documentation on row-level security was not opened (its
licence was not checked) and no vendor architecture guide was used.

## Not verified
1. **Every database statement** (owners and bypass roles under row-level security, per-session settings leaking
   through connection pools, policy cost, catalogue size with many schemas, cross-engine behaviour) is own
   knowledge and was not checked against any manual. Re-read the manual of your engine and version.
2. **The tier model, sizes and counts at which a model stops working** are deliberately not given; they depend on
   the engine and the workload and must be measured.
3. **Legal points** (deletion duties, backups, retention, residency) are method only and not legal advice.

## Related blocks
`laravel-tenant-context-by-default`, `laravel-tenant-replica`, `authorization-models-and-entitlements-pitfalls`,
`field-and-row-permission-ui-api-pitfalls`, `sql-conventions`, `postgres-operations-and-exposed-api-pitfalls`,
`queue-worker-runtime-pitfalls`, `search-index-sync-pitfalls`, `backup-restore-drill-pitfalls`,
`load-and-capacity-testing-pitfalls`, `security-hardening`, `source-freshness`.
