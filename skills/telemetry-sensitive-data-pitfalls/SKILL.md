---
name: telemetry-sensitive-data-pitfalls
description: "Use when spans, metrics, log records or auto-instrumentation are added, configured or reviewed and personal or secret data could reach a telemetry backend: what never goes into telemetry, the fields that need a condition (user id, client address, email, URL, request body, database query text), sanitizing URLs, paths and queries at the source, keyed hashing for correlation, redacting auto-instrumented spans, the Collector as a second layer, prompt and completion capture, and tests that prove the redaction."
---

# telemetry-sensitive-data-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for what an instrumented process lets leave it. The three sections share one
premise: **once telemetry is exported it is hard to remove from the backend, so the only reliable control is the
data never entering a span, metric or log record, and every later layer is a net under that one**. Redacting log
fields by name, and the log rules in general, are in `observability-instrumentation` §2; which attribute may be a
metric label at all is in `observability-instrumentation` §3 and `telemetry-sampling-and-cardinality-pitfalls`;
the Collector's own processor order and configuration are in `otel-collector-config-pitfalls`. Attribute names,
instrumentation-library options and SDK behaviour move with releases, so each such fact below is labelled as the
source states it and must be re-checked against the versions in use.

## When
- Adding a span attribute, a log field or a metric label that carries anything about a user or a request.
- Turning on an auto-instrumentation library, or its capture of headers, URLs or database statements.
- Reviewing a pipeline that exports to a third-party backend.
- Enabling content capture for an AI agent or a model call.
- Writing the tests for a redaction layer.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | What never enters telemetry, and the fields that need a condition | an attribute or field is chosen | [`01-what-never-enters-telemetry.md`](./references/01-what-never-enters-telemetry.md) |
| 2 | Sanitizing at the source: URLs, paths, queries, hashing, logged objects, error messages | a value is attached to a span or a log record | [`02-sanitizing-at-the-source.md`](./references/02-sanitizing-at-the-source.md) |
| 3 | Layers and proof: auto-instrumentation, the Collector, content capture, tests | an instrumentation library is enabled, or redaction must be verified | [`03-layers-capture-and-tests.md`](./references/03-layers-capture-and-tests.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: a request carrying a token in its query string, an email in a body
and a credential header was sent through the instrumented service and the exported spans, logs and metrics were
searched for those values (§3.4), the redaction was checked at the layer that is meant to do it and not only at the
last one (§3.1), and the attribute list of the exporting service was read with the table of §1.2 beside it. A
redaction that was only read in review is not verified.

## Guardrails
- Never attach an authentication credential, a card or bank number, a government identifier, a health record or
  biometric data to any telemetry field (§1.1).
- Never use an email address, a username or a display name as an attribute value, and never `user.id` for anything
  but an opaque identifier (§1.2).
- Never pass a request body, form data or a headers object wholesale to a logger or a span attribute call (§2.4).
- Never keep a database statement with literal values, or a URL with its query string intact (§2.1, §2.2).
- Never rely on Collector-side redaction alone (§3.2).
- Never enable prompt or completion capture outside an isolated development environment (§3.3).
- Never store the hash-to-value mapping in the observability backend (§2.3).
- This block states behaviour as of the repositories read on the date in
  [`references/origin.md`](./references/origin.md). Nothing was run while writing it, and no legal or regulatory
  text was read: which data a regulation covers is for the owner of the compliance requirement to decide.

## Origin
Rewritten from the Dash0 agent skills sensitive-data rule (Apache-2.0) and the o11y-dev OpenTelemetry skill
anti-patterns reference (Apache-2.0), read 2026-10-16. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
