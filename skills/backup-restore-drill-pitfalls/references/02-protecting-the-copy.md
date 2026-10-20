# backup-restore-drill-pitfalls §2 — Protecting the copy

> Part 2 of `skills/backup-restore-drill-pitfalls`. Read it when a backup path is hardened or an incident
> threatens it.
> Sources, read 2026-10-20: Azure Architecture Center, "Design a ransomware-resilient backup architecture by
> using Azure Backup" (CC BY 4.0); mercari/production-readiness-checklist, "Automatic Datastore Backups" (MIT).
> Sentences marked "own guidance" are ours.

1. **Assume the attacker or the mistake reaches the backups too.** The Azure guide starts from the point that
   ransomware targets production and backup systems, so recovery data must be impossible to delete or modify,
   recoverable independently of production, spread across administrative and regional boundaries, and testable.
   Use those four properties as the review checklist.
2. **Make at least one copy immutable for its retention period.** The guide has recovery points that cannot be
   deleted, altered or shortened before retention ends, locks the setting after validating the policy, and adds
   soft delete, multi-person authorisation and role separation. Own guidance, product-independent: write-once
   storage or a vault lock, with the lock applied only after the policy is confirmed, since an unlockable wrong
   policy is itself a problem.
3. **Separate who administers backups from who administers production.** The guide isolates backup
   administration with separate privileged groups, just-in-time elevation, conditional access and break-glass
   accounts, and keeps production operators out of broad rights over the vaults. Symptom: the account that can
   drop the database can also delete every backup. Check: list who can delete a recovery point and compare it
   with who can reach production.
4. **Keep a copy in another account and another region.** The guide stores a second independent copy in a
   different subscription and region, because a vault protects resources in its own region and a compromised
   control plane or region must not take the copy with it. Own guidance: the equivalent anywhere is a second
   account or project, not another folder in the same one.
5. **Do not let the backup depend on the keys it protects.** Own guidance: if the backups are encrypted with a
   key held only in the production system, losing that system loses the backups. Store key material and its
   recovery path separately, and test recovering a key.
6. **Alert outside the production scope.** The guide monitors backup jobs, policy changes, vault access, failures
   and delete operations centrally and routes alerts, where possible, outside the compromised production scope.
   Own guidance: a silent backup failure and a deleted schedule are the two incidents nobody sees; alert on the
   absence of a recent successful backup as well as on errors (`skills/observability-instrumentation` §4).
7. **A green job does not prove recoverability.** The guide says backup success alone does not show the recovery
   time objective can be met. Own guidance: add a periodic integrity check where the tool offers one, and the
   restore drill of `references/03-the-restore-drill.md`.
8. **Restore compromised systems into a clean environment.** The guide restores into a newly provisioned,
   network-isolated environment built from infrastructure code, validates data and application, and only then
   promotes it and redirects traffic; it prefers this over an in-place restore for ransomware, and accepts an
   in-place restore for accidental deletion or a failed deployment when the infrastructure is trusted. Use the
   same split: in place only when the cause is known to be harmless.
9. **Verify the restored point predates the damage.** The guide has operators choose the latest point before
   the suspected compromise and repeat with an earlier one if validation fails. Own guidance: write how you
   decide when the damage began, from logs and from data, before you pick the point.
10. **Cover the odd stores.** Own guidance: a managed service's snapshots may live and die with the resource,
    deletion of the resource may delete its snapshots, and a SaaS tool you depend on may keep no backup you can
    reach. List each and either export it on a schedule or accept the loss in writing.
11. **Account for cost and growth.** Own guidance: retention multiplies storage; check the bill and the restore
    time as data grows, since a restore that took an hour at a tenth of the size is the one that fails the
    objective next year.
12. **Remember the human error that backups cover least.** Own guidance: the most common event is a person
    running the wrong command in the wrong place. Pair backups with safeguards on destructive commands
    (`skills/docker-destructive-guardrails-pitfalls`) and a delay on deletes of the data itself.
