---
name: backup-restore-drill-pitfalls
description: "Use when backups are designed, reviewed or tested, or a restore or disaster-recovery drill is planned or has just run: set recovery point and time objectives with their owner, prove a restore by performing it, keep one copy out of reach of whoever can damage production, and write down what the drill found."
---

# backup-restore-drill-pitfalls

A method for the question "if this data is gone tonight, how much do we get back and how long does it take".
The usual failures: backups that run green and have never been restored, a copy that the same credentials can
delete, a restore that works for the data and fails for the application, an objective nobody chose, and a
procedure that exists only in the head of someone on leave. The block owns no backup product and no scheduler,
and names none. It sits beside `skills/devops-conventions` §6 point 13 (a backup before a destructive step),
`skills/terraform-state-and-secrets-pitfalls` (state is data too), `skills/redis-conventions` §2 (what a cache
persists), `skills/sql-server-transactions-and-operations` (a database's own tooling) and `skills/chaos-experiment`
(a game day that breaks things on purpose). Related: `skills/documentation-craft-pitfalls` §3 (runbooks),
`skills/blameless-incident-review-pitfalls` (the write-up).

## When
- A system gets its first backup design, or a new datastore joins an existing one.
- Someone asks "are we covered" and the answer is a schedule, not a restore.
- A restore or disaster-recovery drill is planned, run or written up.
- A review checks a retention setting, a replication setup or an access change on the backup path.

## Steps

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | What is protected, recovery point and time objectives, retention, and what backups cannot cover | a backup is designed or reviewed | [`01-objectives-and-design.md`](./references/01-objectives-and-design.md) |
| 2 | Protecting the copy: isolation, immutability, access, and checking that backups still complete | a backup path is hardened or an incident threatens it | [`02-protecting-the-copy.md`](./references/02-protecting-the-copy.md) |
| 3 | The restore drill: scope, execution, validation, timing, and the write-up | a drill is planned, run or reviewed | [`03-the-restore-drill.md`](./references/03-the-restore-drill.md) |

## Output / checkpoint
No pipeline checkpoint. For a design: the protected data list, the agreed objectives and their owner, the
retention, the isolation of the copy and the named restore procedure. For a drill: a plan before it runs (scope,
target environment, success criteria, abort conditions) and a write-up after (measured recovery point and time
against the objectives, what failed, owned fixes, the date of the next drill).

## Guardrails
- Count a backup only after a restore of it has been performed and validated. Never report coverage from a
  green job alone.
- Restore into a separate environment first. Never overwrite production to test a backup.
- Keep one copy that production credentials cannot delete or alter. Never leave every copy reachable with the
  keys of the system it protects.
- Take the objectives from the data's owner and measure against them. Never invent a target to match what the
  setup already achieves.
- Let a person authorise any drill that touches production data or traffic. The block never starts a restore
  itself.

## Origin
A hosted-platform architecture guide on ransomware-resilient backup (CC BY 4.0) and a production-readiness
repository's backup and recovery checks (MIT), both read 2026-10-20 and restated, plus the PostgreSQL manual pages on continuous archiving and backup verification (facts only), plus own guidance flagged in
the references. Provenance, what was removed and not verified: [`references/origin.md`](./references/origin.md).
🟡: never dogfooded.
