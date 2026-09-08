---
name: observability-instrumentation
description: "Use when adding logs, metrics, traces or alerts in application code: define the questions the on-call will ask before instrumenting anything. devops-conventions covers the pipeline and infra."
---

# observability-instrumentation

Step 6 of the pipeline (`WORKFLOW.md`), complementing `devops-conventions` (which covers
CI/CD/infra/monitoring at platform level): here, instrumentation at application-code level: where
to log, which metric, which label. Every rule below holds in a repo with **nothing installed**
(`CONVENTIONS.md`, rule A).

**Applying an override is silent.** Where a platform's own observability conventions govern a rule
here, write what they require and move on — never report "a conflict between mentis and the house
rules" to whoever's watching. Surface it as a specific, named question only when no rule anywhere
resolves the case.

## When
As soon as logging, a metric, a trace or an alert is added or modified in application code: never
by adding instrumentation "just in case" with no precise question behind it.

## Steps

**Read §1 first, every time, then the section for what you are adding.** The rules live one file per
section under `references/`. §1 is what makes the rest judgeable: without the questions written down,
nothing decides whether a log line or a metric belongs.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Define the questions before instrumenting | always, before the first log line or metric | [`01-questions-first.md`](./references/01-questions-first.md) |
| 2 | Structured logs | a log line is added or changed | [`02-structured-logs.md`](./references/02-structured-logs.md) |
| 3 | Metrics and traces: anti-cardinality | a metric, a label or a trace span is added | [`03-metrics.md`](./references/03-metrics.md) |
| 4 | Alerting: symptom-based | an alert is added or changed | [`04-alerting.md`](./references/04-alerting.md) |

## Output / checkpoint
The instrumentation added explicitly answers one of the on-call questions stated at step 1; no
unbounded-cardinality label introduced; the alert tested under simulated conditions before being
considered reliable (§4.2); and the output looked at once with real traffic (§1.10).

## Guardrails
Never instrument out of reflex ("you never know") with no identified on-call question behind it: the
cost of collection/storage isn't free and the noise drowns the useful signal during a real
incident. Never PII in clear text in a log, even in a test environment — and redact by field name
rather than by call-site discipline (§2.4). **Never interpolate a value into a log message** (§2.6);
fields for the values, a constant for the message. **Never rename a metric or change its unit
casually** (§3.8) — every dashboard, alert and saved query is written against them. **Never leave an
alert untested** (§4.2).

## Origin
A rewrite of a market generalist catalogue's `observability-and-instrumentation` skill. The full
provenance and the refresh log are in [`references/origin.md`](./references/origin.md).
