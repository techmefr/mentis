---
name: data-pipeline-conventions
description: Use when writing/reviewing a data pipeline (ETL/ELT), an analytical schema model, or a data quality validation, conventions for data reliability and traceability, distinct from transactional application code. No dedicated Xefi production experience at this stage, sourced from established practice (dbt, data quality dimensions).
---

# data-pipeline-conventions

Step 6 of the pipeline (`WORKFLOW.md`), for code that moves/transforms data between systems (ETL/ELT,
analytical warehouse): distinct from the transactional application code (business CRUD) covered by the
Laravel/NestJS conventions.

## When
As soon as a data pipeline, an analytical transformation, or a data schema definition meant for
analysis is written or modified (not the app's own transactional database).

## Steps

### 1. Idempotence and reproducibility: the non-negotiable base
1. A pipeline replayed twice on the same source produces the same result (idempotent): never an
   `INSERT` that duplicates on every run with no deduplication or `UPSERT`.
2. Every run is traceable: source, version of the transformation code, timestamp: so you can trace
   back "which version of the pipeline produced this row".
3. Transformations tested on a sample before a full run on production data, especially for a
   destructive transformation (full replacement of a table).

### 2. Data quality: verified, not assumed
1. Explicit validation of the expected constraints (non-null on required fields, key uniqueness,
   plausible value ranges) at the pipeline's input and output: a validation failure blocks the
   pipeline, it doesn't pass silently while producing wrong data.
2. The four quality dimensions verified explicitly where relevant: completeness (nothing missing),
   accuracy (correct value), consistency (same fact, same value across systems), timeliness (data up
   to date at the moment of use).
3. An external source (third-party API, partner file) is treated as unreliable by default: schema
   checked on every ingestion, not assumed stable over time.

### 3. Analytical schema modelling
1. Clear separation between the raw layer (data as received, never modified) and the transformed layer
   (cleaned/aggregated data): never a transformation that overwrites the original raw data without
   keeping it.
2. Consistent and documented column/table naming (explicit table grain: one row = what exactly); a
   table with no defined grain invites wrong joins.
3. Explicit historisation (SCD - slowly changing dimension) when a value changes over time and the
   history matters for the analysis, rather than a plain `UPDATE` that loses the previous state.

### 4. Performance and cost
1. Incremental processing (only the new/modified data) rather than a full reprocessing by default,
   unless the volume genuinely allows it at no significant cost.
2. Table partitioning/clustering aligned with the real query patterns (the most frequent filter), not
   chosen arbitrarily.

## Output / checkpoint
Pipeline compliant with the four sections above; the data quality validations run and are green before
the result is considered usable downstream.

## Guardrails
Never run a destructive pipeline (full replacement of a production table) without explicit human
confirmation. This block has no dedicated Xefi production experience yet: to be confronted with the
first real data pipeline, not to be treated as proven doctrine.

## Origin
Sourced from established dbt conventions (staging/intermediate/marts layers, schema tests), the DAMA-
DMBOK data quality dimensions (completeness/accuracy/consistency/timeliness), and the classic SCD
patterns in dimensional modelling (Kimball). Mechanisms rewritten, no copied text. Market research, no
internal production feedback at this stage.
