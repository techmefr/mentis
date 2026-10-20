# backup-restore-drill-pitfalls: origin and source stamps

> Provenance of `skills/backup-restore-drill-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from two published sources and own craft knowledge, never run as a real
restore drill by us.

## Sources (read 2026-10-20, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| MicrosoftDocs/architecture-center, page "Design a ransomware-resilient backup architecture by using Azure Backup" (docs/security/ransomware-resilient-backup-architecture/index.md, dated 2026-07-07; LICENSE file read: Creative Commons Attribution 4.0 International; repository pushed 2026-10-20) | CC BY 4.0 | Four properties of recovery data; immutability with a late lock; backup administration separated from production; second independent copy in another account and region; monitoring outside the production scope; backup success is not recovery proof; clean-environment restore with validation before promotion; in-place restore only for harmless causes; choosing a point before the damage |
| mercari/production-readiness-checklist, docs/concepts/automatic-backups.md and docs/references/pre-production-checklist.md, data-storage section (LICENSE file read: MIT, Copyright 2020 Mercari, Inc.; repository last pushed 2021-11-22) | MIT | Events a backup answers; backups on a schedule and before risky events; recovery procedure defined and tested; for the most critical level, practised on a schedule and recorded in the on-call playbook |

Credit as the licences require: Microsoft Azure Architecture Center, CC BY 4.0 (https://github.com/MicrosoftDocs/architecture-center); Mercari production readiness checklist, MIT, Copyright 2020 Mercari, Inc. (https://github.com/mercari/production-readiness-checklist). The text was rewritten, not reproduced; no endorsement by either author is implied.

## Removed
1. **Every figure**: retention days, recovery time limits, drill intervals, alert thresholds and the Azure
   guide's baseline ranges. They belong to a system and its owner.
2. **All product names, vault settings and the managed-service component walk-through**: runtime detail.
3. **No backup tool's own documentation was read** (a database backup tool's repository reports its licence as
   unasserted and was not opened). Nothing names a tool's options or commands.

## Not verified
1. Most points on point-in-time recovery, key custody, erasure replay, restore timing phases and drill
   technique are own guidance from the craft; no source on them was read.
2. The ransomware guide is written for one cloud provider's managed service; the product-independent
   restatement in §2 is our judgement.
3. The database vendors' own backup and recovery documentation was not read, so engine-specific behaviour
   (log archiving, consistency checks) is stated generically.
4. No backup was taken and no restore performed in writing this block.

## Related blocks
`skills/devops-conventions`, `skills/terraform-state-and-secrets-pitfalls`, `skills/redis-conventions`,
`skills/sql-server-transactions-and-operations`, `skills/chaos-experiment`, `skills/documentation-craft-pitfalls`,
`skills/blameless-incident-review-pitfalls`, `skills/production-readiness-review`, `business/data-protection`,
`skills/source-freshness`.
