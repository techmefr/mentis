---
name: data-pipeline-conventions
description: Use when writing or reviewing a data pipeline (ETL/ELT), an analytical schema model, or a data quality validation. Distinct from transactional application code.
---

# data-pipeline-conventions

Step 6 of the pipeline (`WORKFLOW.md`), for code that moves/transforms data between systems (ETL/ELT,
analytical warehouse): distinct from the transactional application code (business CRUD) covered by the
Laravel/NestJS conventions. Every rule below holds in a repo with **nothing installed**
(`CONVENTIONS.md`, rule A).

**Applying an override is silent.** Where a company's own data-engineering conventions or governance
policy govern a rule here, write what they require and move on — never report "a conflict between
mentis and the house rules" to whoever's watching. Surface it as a specific, named question only when
no rule anywhere resolves the case. What the *landscape* itself looks like before a query is safe to
trust belongs to `business/data-analytics`.

## When
As soon as a data pipeline, an analytical transformation, or a data schema definition meant for
analysis is written or modified (not the app's own transactional database).

## Steps

**Read only the sections the task actually touches.** The rules live one file per section under
`references/`; §1 applies to every run and to any ad-hoc job on somebody's file, §2 is the
validations, §3 is the shape of the tables, §4 is what it costs to run.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Idempotence and reproducibility | any run, and any ad-hoc job on a supplied file | [`01-idempotence.md`](./references/01-idempotence.md) |
| 2 | Data quality: verified, not assumed | writing validations, or facing a source you don't control | [`02-data-quality.md`](./references/02-data-quality.md) |
| 3 | Analytical schema modelling | shaping tables meant for analysis | [`03-modelling.md`](./references/03-modelling.md) |
| 4 | Performance and cost | before a full reprocessing, or choosing a table's layout | [`04-performance-cost.md`](./references/04-performance-cost.md) |

## Output / checkpoint
Pipeline compliant with the four sections above; the data quality validations run and are green before
the result is considered usable downstream, with the row counts in, out and rejected recorded (§2.7).

## Guardrails
- **Never write back over a supplied source file** (§1.4), and never apply a destructive
  transformation to someone's data without saying first what it changes and on how many rows (§1.5).
- Never run a destructive pipeline (full replacement of a production table) without explicit human
  confirmation, and never treat a green sample as clearance for a full run (§1.12).
- **Never let a validation failure pass silently** (§2.1); where blocking is genuinely unacceptable,
  quarantine the rows and publish the count rather than skipping them (§2.4).
- **Never overwrite the raw layer** (§3.1), and never lose a previous state with an in-place `UPDATE`
  where the history matters (§3.3).
- This block has no dedicated in-house production experience yet: to be confronted with the
  first real data pipeline, not to be treated as proven doctrine.

## Origin
Established dbt conventions, the DAMA-DMBOK quality dimensions and the classic SCD patterns, plus §1.4
and §1.5 from an org BI skill read for its handling discipline. The full provenance and the refresh log
are in [`references/origin.md`](./references/origin.md).
