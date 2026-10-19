# slo-design §1 — Choosing the SLI

> Part 1 of `skills/slo-design`. Read it when an indicator is chosen or reviewed.
> Source, read 2026-10-19: Google SRE Workbook, "Implementing SLOs"
> (https://sre.google/workbook/implementing-slos/). Sentences marked "own guidance" are ours.

1. **Separate the specification from the implementation.** The specification is the outcome users care about
   ("the share of page requests that loaded fast enough"). The implementation adds how it is measured. The
   Workbook gives three ways to measure one specification (server logs, a prober acting like a browser,
   instrumentation in the client) and shows they differ in quality, coverage and cost: logs miss requests that
   never reached the backend, probers can miss problems affecting only some users, client instrumentation is
   closest to the user but needs code and its own reliable telemetry.
2. **Write the SLI as good events over valid events.** Own guidance, consistent with the Workbook's ratio form:
   higher is better, the numerator says what "good" means, the denominator says what counts at all. A ratio
   that goes up when things get worse invites sign mistakes in every rule built on it.
3. **State what is excluded and where it is measured.** Probe traffic, bots, health checks and internal callers
   change both numbers. Own guidance: a request class that users do not make should not spend their budget, and
   the point of measurement (edge, service, client) belongs in the definition because it changes the answer.
4. **Pick a few indicators per kind of system, and the Workbook's split is a good start.** A request-driven
   service: availability, latency and quality (does it degrade gracefully when a backend is down). A pipeline:
   freshness, correctness and coverage. A storage system: durability. The Workbook advises a small set per
   service rather than many.
5. **Use more than one latency threshold when the tail matters.** A single threshold hides the slow few; the
   Workbook shows two thresholds at different shares of requests to capture the long tail.
6. **A slow success is a failure to the user.** Own guidance: error counting alone says nothing about a reply
   that arrives too late, so a latency indicator belongs next to an availability one wherever speed is part of
   the experience (`skills/failure-classification-before-retry` §1 sorts the errors that count).
7. **One journey, one indicator.** Own guidance: averaging a critical journey with a trivial one produces a
   number that is right for neither; split them when their importance differs.
8. **Start with the cheapest measurement that is honest, then improve it.** The Workbook says a first indicator
   need not be correct, provided it is measured and there is a feedback loop to refine it. Say in the
   definition which limitation the first choice has.
9. **Resource figures are not indicators.** Own guidance: CPU, memory and restart counts help capacity work and
   diagnosis (`skills/observability-instrumentation` §3) but a service can look healthy on them while users
   fail, and fail while they look bad.
10. **Re-read the SLI when the system changes.** A new failure mode, a dependency moving to asynchronous work or
    a new endpoint can make the old definition stop describing what users feel. A stale indicator gives false
    comfort, which is worse than none.
