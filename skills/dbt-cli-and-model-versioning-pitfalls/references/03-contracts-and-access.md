# dbt-cli-and-model-versioning-pitfalls §3 — Contracts, constraints, access and groups

Sources: `skills/dbt/skills/working-with-dbt-mesh/references/model-contracts.md` and `groups-and-access.md` (dbt-labs/dbt-agent-skills at 7c7b5fa), read in full 2026-10-15. The generic point that a contract is checked before the data lands is in `data-pipeline-conventions` §2 and is not repeated; this section holds the dbt specifics. Fusion points are marked (Fusion).

## 3.1 Where a contract applies
1. **Use one when** the model is public, feeds an exposure, or is queried directly by external consumers, and you need build-time schema guarantees.
2. **Do not add one to** staging models (use data tests), models still being iterated on, models with no external consumers, models with pivoted or dynamic columns, or ephemeral models. The source says to ask who depends on the schema first.
3. **Supported materializations:** `table`, `view` (names and types enforced, constraints not) and `incremental`. Not supported: `ephemeral`, `materialized_view`, Python models.
4. **Every column must be declared with a `data_type`.** A partial list is not a contract.
5. **An incremental model with a contract needs `on_schema_change: append_new_columns` or `fail`.** Without it the source warns of silent drift between the YAML and the table.
6. **Give numeric types precision and scale,** for example `numeric(38, 6)`. Generic types are aliased per platform unless `alias_types: false`.

## 3.2 Constraints
1. **A constraint is checked at build time and the model is not materialised on failure;** a test runs after the build and the model exists when it fails.
2. **Warehouse enforcement varies.** The source's table shows `not_null` enforced on PostgreSQL, Snowflake, BigQuery, Redshift and Databricks, and `unique`, `primary_key` and `check` enforced on PostgreSQL only or not supported elsewhere. Unenforced constraints still serve as documentation and metadata.

## 3.3 Breaking changes
1. **The source lists as breaking:** removing a column, changing a data type, removing or modifying a constraint, removing a contracted model (dbt 1.9 and later). The way out is a new version (§2).

## 3.4 Groups and access
1. **Access levels:** `private` (same group only), `protected` (same project or installed package, the default), `public` (any group, package or project). Only public models are visible to other projects through cross-project `ref`.
2. **A private model referenced from outside its group raises `DbtReferenceError`;** the source says private access requires a `group`, and an ephemeral model cannot be public.
3. **A group is a team boundary with an owner** (at least `name` or `email`), not a per-model label.
4. **Access is a dbt concept and does not control database permissions;** manage those separately.
5. **The source's advice:** start new models as `private` and widen only for a real consumer, and pair `public` with a contract.

## 3.5 Placement in YAML
1. **(Fusion) `contract`, `access` and `group` belong under `config:` in a property file.** The source says top-level placement breaks the Fusion engine. In `dbt_project.yml` use the `+` prefix, and in SQL `{{ config(...) }}`.

## 3.6 Checks (own guidance)
1. Every public model has a contract and a group with a reachable owner.
2. No property file has `access`, `group` or `contract` outside `config:`.
3. No incremental model with a contract lacks `on_schema_change`.
