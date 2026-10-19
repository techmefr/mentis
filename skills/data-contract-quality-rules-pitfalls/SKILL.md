---
name: data-contract-quality-rules-pitfalls
description: "Use when quality rules, service levels or lifecycle fields are written or reviewed in an Open Data Contract Standard file (version 3.2.0): the four rule types text, library, sql and custom, unit rows against percent, nullValues against missingValues, dialect-bound SQL and its placeholders, opaque custom rules, stable ids, severity, dimension, scheduler, SLA properties with latency preferred to freshness, status values, deprecated fields."
---

# data-contract-quality-rules-pitfalls

**Version-bound: Open Data Contract Standard (ODCS) v3.2.0**, the `apiVersion` default in the documentation
read. A later version may rename or remove what is described here; check the standard before applying any
rule below to another version. Not a step of the pipeline: a craft block for the quality, service-level and
lifecycle parts of a data contract file. The three parts share one premise: **a contract rule is only as
strong as what executes it**, so each pitfall is a way a rule reads as enforced while nothing checks it, or
checks something other than what the author meant. The generic stance (a contract is a promise checked at the
producer and consumer boundary) is in `data-pipeline-conventions`, part 2; schema and model versioning
for dbt is in `dbt-cli-and-model-versioning-pitfalls`.

## When
- A quality section is added to a contract, or a contract is reviewed before consumers rely on it.
- A rule passes yet bad data got through, or a rule fails and nobody can say what it measures.
- SLA properties, status or ownership fields are filled in.
- A contract written for an older version is moved to 3.2.0.

## Steps

**Read only the part the task meets.**

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Rule types, library metrics, units, operators, null against missing | a rule is chosen or its numbers are questioned | [`01-rule-types-metrics-and-units.md`](./references/01-rule-types-metrics-and-units.md) |
| 2 | SQL and custom rules, rule metadata, severity, dimension, scheduling | a rule must run, be routed or be referenced | [`02-sql-custom-and-metadata.md`](./references/02-sql-custom-and-metadata.md) |
| 3 | SLA properties, contract header, status, deprecated fields, roles | service levels or lifecycle fields are written | [`03-sla-lifecycle-and-roles.md`](./references/03-sla-lifecycle-and-roles.md) |

## Output / checkpoint
A quality section is done when every rule says its type, its metric or query, its operator with an explicit
unit, and an id, and when for each rule a reader can name what executes it and what happens on failure
(severity, business impact). Read it once looking for a text rule counted as a control, a number with no unit,
and a custom rule nobody on the team can read. Nothing was run against a validator or an engine: the check is
a read of the text. No pipeline checkpoint.

## Guardrails
- Never count a `text` rule as a control; nothing executes it until it is translated (part 1).
- Never leave the unit implicit on a threshold; rows is the default and percent is not (part 1).
- Never write a null check and assume it covers empty strings or placeholder values (part 1).
- Never write SQL for another dialect than the contract's server, and use the placeholders the standard names
  (part 2).
- Never rely on the contract tooling to validate a custom rule; the block is passed to the engine as it is
  (part 2).
- Never depend on `severity`, `status` or `unit` values being checked: the schema leaves them open (parts 2, 3).
- Never use a deprecated field in a new contract (part 3).
- Version-bound: say "ODCS v3.2.0" wherever these rules are quoted, and re-read the standard for any other.

## Origin
Rewritten from four documentation pages and the v3.2.0 JSON schema of the Open Data Contract Standard
repository (Apache-2.0), read 2026-10-16. 🟡: never run by us against a validator or a quality engine; open
points are in [`references/origin.md`](./references/origin.md).
