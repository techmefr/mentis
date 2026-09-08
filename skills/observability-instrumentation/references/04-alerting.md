# § 4 — Alerting: symptom-based

> Section 4 of `skills/observability-instrumentation`. Read it when an alert is added or changed. Point
> 2 is the verification the block's checkpoint owes.

1. An alert fires on a **symptom observable by the user** (latency, error rate), never directly on
   an infra cause (high CPU) unless that link has already been proven causal. The reason is that causes
   are plural and symptoms are few: a page for high CPU fires on the cause that was harmless this time,
   and misses the outage whose cause nobody predicted.
2. Mandatory final verification: deliberately force the alert condition (or simulate it) to confirm
   it really fires: an alert that was never tested is an alert you don't know works. The failure this
   catches is silent and total — a misspelled label, a threshold no real value can cross, a
   notification route to a channel nobody reads — and it is discovered during the first incident, which
   is the one occasion it cost something.
3. **Every alert names what the responder should do**, or a link to it. An alert that states a
   condition and nothing else spends the responder's first minutes working out what it means, and the
   people who wrote it are not the ones who will be woken by it.
4. **An alert that cannot be acted on is not an alert.** If the answer is always "wait and see" or
   "it clears by itself", it is a dashboard line or a report, and leaving it as a page is how a rota
   learns to dismiss notifications — after which the real one is dismissed too.
5. **Every alert has an owner and a route.** Sent to a group with no named responsibility, it is read
   by everyone as somebody else's, which is indistinguishable from being read by nobody.
6. **Thresholds are chosen from observed data, not from a round number.** A threshold picked by
   intuition fires constantly or never, and both outcomes are discovered slowly; the honest method is to
   look at the distribution first (§3.7) and to say which percentile and which window the number came
   from.
7. **Duration is part of the condition.** A rate crossing a threshold for one scrape is noise, and the
   same rate sustained for several minutes is an incident — so the window is what separates a page from
   a flap, and an alert with no window will find every transient.
8. **A low-volume service needs a different condition.** An error *rate* over five requests is either
   0% or 20%, so a percentage threshold pages on a single failure at night and stays silent under real
   load; a minimum-volume clause, or an absolute count, is what makes the alert mean the same thing at
   both ends of the day.
9. **Alert on the absence of what should be there.** A job that did not run, a queue that stopped being
   consumed, a feed that went quiet: nothing errors, every metric looks healthy, and the only signal is
   that a number stopped moving. This is the class of failure a symptom-based alert set misses unless it
   is written deliberately.
10. **One incident should produce one page.** A cause that trips five conditions wakes the responder
    five times and buries the one that says what is happening, so related alerts are grouped and
    dependent ones are suppressed while the upstream is firing.
11. **An alert that fires and is always ignored is a defect to fix or delete.** Reviewing what fired,
    what was acted on and what was not is the only thing that keeps a set of alerts trustworthy — and
    an untrusted set is worse than none, because it costs the same and is not read
    (`business/incident-communication`).
12. **An alert is instrumentation, so §1 applies to it.** It exists to answer one of the stated
    questions, it is removed when it stops answering one, and it is verified against real output — the
    same three rules as any log line or metric, with the difference that this one wakes somebody up.
