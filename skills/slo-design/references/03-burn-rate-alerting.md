# slo-design §3 — Alerting on burn rate

> Part 3 of `skills/slo-design`. Read it when an alert on an objective is written, tuned or complained about.
> Source, read 2026-10-19: Google SRE Workbook, "Alerting on SLOs"
> (https://sre.google/workbook/alerting-on-slos/). Sentences marked "own guidance" are ours. The chapter
> publishes exact windows and burn rates for a worked objective; none is repeated here. Re-read the chapter's
> tables before relying on any figure, and recompute them for your own target and window.

1. **Judge an alert on four properties.** Precision: how many alerts were about something significant. Recall:
   how many significant events alerted. Detection time: how long until the notification, since a slow
   detection spends budget. Reset time: how long the alert keeps firing after the problem is fixed, since a
   long tail breeds confusion and learned dismissal.
2. **A raw error-rate threshold at the objective's level is precise about nothing.** The Workbook shows it fires
   on rates that spend a trivial share of the budget, so a service can page many times a day and still meet its
   objective. It detects fast and recalls well, and it trains people to ignore it.
3. **Lengthening the window fixes precision and breaks reset.** A long window makes the alert mean something,
   but after an outage it keeps firing for as long as the window, and long-range calculations are costly.
4. **A "for" duration does not scale with severity.** A total outage waits as long as a mild one, and a flapping
   failure that keeps resetting the timer may never fire while spending a large share of the budget. The
   Workbook does not recommend durations for objective-based alerts.
5. **Burn rate is the common currency.** It is how fast the budget is being used relative to the objective: a
   rate of one would spend exactly the whole budget by the end of the window. It scales with the target, so a
   strict and a loose objective can use the same reasoning, and "time to exhaustion" follows from it.
6. **A single burn-rate alert still misses slow burns.** A condition set to catch fast burns lets a steady
   moderate burn run, which can still empty the budget well before the window ends, with no page.
7. **Use several burn rates, each with a long and a short window.** A fast burn pages; a slower sustained burn
   pages at a lower urgency; a slow leak opens a ticket and does not page. The short window (the Workbook uses
   a small fraction of the long one) means the alert stops soon after the errors stop, which cures the reset
   problem; the long window keeps a blip from paging. Both must be over their limit for the alert to fire.
8. **Suppress duplicates.** Several conditions will fire for one incident; group or suppress the lower ones
   while the higher one is firing (`skills/observability-instrumentation` §4 point 10).
9. **Low traffic needs its own thought.** With very few requests a single failure is a huge rate and pages at
   once, while spending a large slice of the budget. The Workbook's options: generate synthetic traffic (it can
   hide real-user errors and cannot cover every request type), group services that share a failure domain,
   change the service so one failure matters less (retries with backoff and jitter, a fallback path,
   `skills/failure-classification-before-retry` §2), or accept a looser target or a longer window, which are
   product decisions (§2).
10. **Extreme targets break the arithmetic.** With a loose target a total outage may never reach the page
    condition; with a very strict one a total outage can exhaust the budget faster than any alert pipeline
    reacts, so the defence is design (limiting how much of the traffic a change can touch, canarying), not a
    quicker pager.
11. **Use one parameter set across services where you can.** The Workbook warns that per-service tuning does not
    scale and proposes a handful of request classes with their own targets; fewer variants means fewer
    surprises for the responder.
12. **Test the alert.** Replay or simulate a burn and see the right alert fire and reset
    (`skills/observability-instrumentation` §4 point 2). An alert on an objective that has never fired is
    untested, not quiet.
