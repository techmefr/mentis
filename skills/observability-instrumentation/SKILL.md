---
name: observability-instrumentation
description: Use when adding logs, metrics, traces or alerts in application code, define first the questions the on-call will ask, before instrumenting anything, to avoid collecting useless data. Complements devops-conventions (which covers the pipeline/infra) at the level of the code itself.
---

# observability-instrumentation

Step 6 of the pipeline (`WORKFLOW.md`), complementing `devops-conventions` (which covers
CI/CD/infra/monitoring at platform level): here, instrumentation at application-code level: where
to log, which metric, which label.

## When
As soon as logging, a metric, a trace or an alert is added or modified in application code: never
by adding instrumentation "just in case" with no precise question behind it.

## Steps

### 1. Define the questions before instrumenting
1. State 2 to 4 concrete questions the on-call will ask during an incident ("why is this request
   slow?", "how many users are affected?"), **before** writing the first log or the first metric.
2. Every piece of data collected must answer at least one of those questions: a metric/log that
   answers none of the questions asked is noise, don't add it.

### 2. Structured logs
1. Structured format (JSON), never free text for an event that has to be queryable during an
   incident.
2. Correlation ID mandatory on any call chain crossing several services/layers: without it, it's
   impossible to tie together the logs of a single request.
3. Redaction of personal/sensitive data (PII) before writing: never an email, a password or a
   client's data in clear text in a log.
4. **Credentials are redacted by field name, not by call-site discipline**: `authorization`,
   `cookie`, `set-cookie`, `access_token`, `refresh_token`, API keys. The leak is rarely a
   deliberate log line, it's logging a whole object that carries them, an HTTP client's error
   (which holds the request headers) being the classic one. See `auth-session-conventions` §2.4 for
   the paths to watch.

### 3. Metrics: anti-cardinality
1. RED metrics (Rate/Errors/Duration) for services, USE (Utilization/Saturation/Errors) for
   resources: a starting grid, not the only possible one, but a healthy default.
2. **Bounded** metric labels: never a user ID, a raw URL or any other unlimited-cardinality
   identifier as a label: a cardinality explosion makes the metrics system unusable or
   prohibitively expensive.
3. Distributed traces (OpenTelemetry or an equivalent already in place) placed at service
   boundaries, not on every internal function.

### 4. Alerting: symptom-based
1. An alert fires on a **symptom observable by the user** (latency, error rate), never directly on
   an infra cause (high CPU) unless that link has already been proven causal.
2. Mandatory final verification: deliberately force the alert condition (or simulate it) to confirm
   it really fires: an alert that was never tested is an alert you don't know works.

## Output / checkpoint
The instrumentation added explicitly answers one of the on-call questions stated at step 1; no
unbounded-cardinality label introduced; the alert tested under simulated conditions before being
considered reliable.

## Guardrails
Never instrument out of reflex ("you never know") with no identified on-call question behind it: the
cost of collection/storage isn't free and the noise drowns the useful signal during a real
incident. Never PII in clear text in a log, even in a test environment.

## Origin
Rewrite of the `observability-and-instrumentation` skill from a market generalist dev skill
catalogue; the "define the questions before instrumenting" rule, the RED/USE metrics, the
anti-cardinality rule and symptom-based alerting are taken as-is, rewritten to the mentis template.
