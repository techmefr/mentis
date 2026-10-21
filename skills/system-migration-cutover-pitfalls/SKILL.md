---
name: system-migration-cutover-pitfalls
description: "Use when data or traffic moves from one system to another and users depend on the result: replacing an application, a vendor, a database engine or a data model, merging two systems, or moving a tenant. Inventory and field mapping with an owner, profiling the source, a resumable loader that quarantines rejects, side effects switched off during the load, timed dry runs on a copy, reconciliation by counts, sums and sampled rows, a rollback designed before the cutover, and the cutover itself: big bang versus phased, why application dual writes diverge, log-based change data capture with snapshots and at-least-once delivery, an outbox, shadow reads, lag, replication-slot disk growth, and decommissioning. Method only."
---

# system-migration-cutover-pitfalls

A defensive block for the project where the old system keeps running until the day the new one takes over. The
failures are repeatable: a field nobody mapped is silently lost, the load runs in a test and not in the time window
available, emails go to every imported customer, two systems each believe they are the master, the new system is
live and nobody can say whether its totals match, the rollback needs data that only exists in the new system. The
change-data-capture facts below come from the Debezium documentation (Apache-2.0); the rest is our craft guidance
and is flagged. It is stack-neutral method.

Neighbours, not repeated: schema changes with old code still running (expand, backfill, contract) are in
`skills/devops-conventions` §6 and `skills/deprecation-migration`; one pair of engines is in
`skills/laravel-mysql-to-postgres-pitfalls`; a spreadsheet or file import is in
`skills/csv-xlsx-import-export-pitfalls` and `business/spreadsheet-data-cleaning-pitfalls`; the outbox and inbox
pattern is in `skills/nestjs-reliability` §3; keeping a search index in step is in
`skills/search-index-sync-pitfalls`; progressive delivery and the rollback of code are in
`skills/release-strategy-and-progressive-delivery-pitfalls`; replaying a data command safely is in
`skills/laravel-idempotent-data-commands`. This block is the generic plan and cutover around those.

## When
- A system, vendor, database engine or data model is replaced and data has to follow.
- Two systems are merged, or one tenant or customer is moved to another instance.
- Old and new run side by side for a while and must stay consistent.
- A cutover date is being planned, or a rollback is being designed.

## Steps

**Read the part for the phase you are in; the cutover plan needs both.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Inventory, mapping, profiling, the loader, side effects, dry runs, reconciliation, the rollback plan | before the first load, and before every rehearsal | [`01-plan-mapping-and-rehearsal.md`](./references/01-plan-mapping-and-rehearsal.md) |
| 2 | Cutover strategies, dual writes, change data capture, snapshots, ordering, outbox, shadow reads, lag, decommissioning | the old and the new system must stay in step, or the switch is being scheduled | [`02-cutover-dual-write-and-cdc.md`](./references/02-cutover-dual-write-and-cdc.md) |

## Output / checkpoint
Before the first load: the inventory (what moves, what is archived, who consumes it), a field mapping with an owner
for every source field including the ones deliberately dropped, and the identity rule (how a source key maps to
a target key). Before cutover: the measured duration of the last dry run, the reconciliation report with its
thresholds and sign-off, the rollback plan with its point of no return, and a runbook with owners and go or no-go
criteria. Evidence is a rerun of the loader that changes nothing, a quarantine table with reasons, a reconciliation
that matches counts, money sums and sampled rows, and a rollback rehearsal. Nothing here was run by us.

## Guardrails
- Give every source field a decision (mapped, transformed, dropped with a reason). Never discover an unmapped field
  after cutover (part 1, rule 2).
- Make the loader idempotent and resumable, and put rejects in a table with a reason. Never skip a bad row without
  a record (part 1, rule 4).
- Switch off emails, webhooks, notifications and indexing for the load, then switch them on deliberately. Never
  let an import contact real customers (part 1, rule 5).
- Rehearse on a copy with the real procedure and time it. Never plan the window from the size of the data alone
  (part 1, rule 6).
- Reconcile with counts, money sums and sampled rows, and have the data owner sign. Never call a migration done
  because the loader exited zero (part 1, rules 7 and 9).
- Design the rollback before the cutover and keep the source read-only and intact. Never decommission the old
  system on the day of the switch (part 1, rule 8; part 2, rule 13).
- Name one system of record at every moment. Never keep two writable systems that both replicate to each other
  without a decided conflict rule (part 2, rules 2 and 3).
- Do not copy a window, lag threshold or batch size from a source; measure them on your data.
- Do not load production personal data into a rehearsal environment with weaker protection than production.

## Origin
Rewritten from the Debezium documentation (`debezium/debezium`, Apache-2.0, LICENSE file read), read 2026-10-20:
the features, architecture, outbox-router and PostgreSQL connector pages. Everything else is our own craft
guidance, flagged in the text. Provenance, removals and what is not verified are in
[`references/origin.md`](./references/origin.md). 🟡: never run by us.
