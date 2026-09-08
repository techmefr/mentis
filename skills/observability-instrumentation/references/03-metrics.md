# § 3 — Metrics: anti-cardinality

> Section 3 of `skills/observability-instrumentation`. Read it when a metric, a label or a trace span
> is added.

1. RED metrics (Rate/Errors/Duration) for services, USE (Utilization/Saturation/Errors) for
   resources: a starting grid, not the only possible one, but a healthy default. The value of a default
   is that it is comparable: the same three series for every service means an on-call reads an
   unfamiliar one at a glance, which is exactly the situation the metrics exist for.
2. **Bounded** metric labels: never a user ID, a raw URL or any other unlimited-cardinality
   identifier as a label: a cardinality explosion makes the metrics system unusable or
   prohibitively expensive.
3. Distributed traces (OpenTelemetry or an equivalent already in place) placed at service
   boundaries, not on every internal function. A span per function produces a trace nobody can read
   and a cost proportional to the call count; the boundaries are where the time actually goes and where
   the responsibility changes.
4. **Cardinality is multiplicative, which is why it surprises people.** Three labels of ten values each
   is a thousand series, and the fourth one added "just for this dashboard" multiplies it again. The
   failure is not a warning: it is an ingestion limit reached, a query timing out, or an invoice — and
   it usually lands during the incident that made someone add the label.
5. **A route template is bounded, a raw path is not.** The same distinction applies to a status code
   versus a status message, a plan name versus a customer name, and an error class versus an error
   string. Each pair looks equivalent and one member of it is unbounded, which is the check to run on
   every label before it ships.
6. **A high-cardinality dimension belongs in logs or traces, not in a metric.** That is the actual
   answer to "but I need to know which user": metrics count, logs and traces identify, and the
   correlation between them is the correlation ID (§2.2). Deciding this per question (§1.4) is what
   keeps both systems usable.
7. **A counter answers "how many", a histogram answers "how slow", and an average answers neither.**
   The mean latency of a request path hides the tail entirely, so the reader concludes the system is
   healthy while a share of users cannot use it. If duration matters, the distribution is what is
   recorded.
8. **A metric's name and unit are permanent.** Dashboards, alerts and saved queries are all written
   against them, so renaming one silently empties every panel that used it, and changing a unit — from
   seconds to milliseconds, from bytes to kilobytes — makes every historical comparison and every
   threshold wrong with no error anywhere.
9. **A counter that resets is read as a drop.** Process restarts, deployments and scaling events all
   reset in-process state, which is why a rate over a counter is the readable form and a raw total is
   not — and why a gauge sampled per instance says nothing without knowing how many instances there
   were.
10. **Instrument the failure paths, not only the successes.** An error counter that is only incremented
    on the branch somebody remembered is a metric that reports zero during an outage, which is worse
    than having none: the dashboard actively says the system is fine. Count at the boundary, where every
    outcome passes.
11. **Never let a metric be the only record of something you will need to explain.** A count with no
    example is a number an operator cannot act on, and the example is a log line or a trace — so a
    metric worth alerting on comes with a way to reach the underlying events.
12. **Sampling is a decision with a consequence.** A sampled trace is absent for the request somebody
    asks about, and a sampled error count is an estimate; both are usually the right trade, and both
    have to be known by whoever reads the number, because a rate derived from a sample and a rate
    derived from everything look identical on a chart.
