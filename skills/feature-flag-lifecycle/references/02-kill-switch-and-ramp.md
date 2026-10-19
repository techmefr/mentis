# feature-flag-lifecycle §2 — Kill switch before the ramp, and the ramp itself

> Part 2 of `skills/feature-flag-lifecycle`. Read it before a flag reaches real users.
> Source, read 2026-10-19: Martin Fowler, "Feature Toggles (aka Feature Flags)"
> (https://martinfowler.com/articles/feature-toggles.html), for operational toggles and kill switches as a manual
> circuit breaker. The staged-ramp and abort-criteria points are own guidance, restated from one MIT skill
> collection's flag workflow and not independently verified.

1. **Exercise the off switch before any user is exposed.** Ship the flag off in production, then flip it on
   and off in a safe environment and watch the system return to the old behaviour. A switch nobody has pulled
   is a hypothesis; the first real pull should not be during an incident.
2. **The off state is the old behaviour, and it must keep working.** The article's convention is that "off"
   means legacy behaviour and "on" means the new one. A flag whose off state was never maintained, or cannot be
   reached because data has already moved forward, is not a kill switch.
3. **Decide before the ramp which signal trips the switch and who pulls it.** The signal is something a user
   would feel (errors, latency, a business outcome), not an internal resource figure (`skills/observability-instrumentation`
   §4). The article calls an operator-facing kill switch a manual circuit breaker; the record from §1 names the
   person and the route.
4. **An operational switch must be quick to change.** It is flipped by an operator under pressure, so it cannot
   need a new release. The article makes this the difference between an operational toggle and a release one.
5. **Ramp in stages, each with an abort criterion written first.** Own guidance: start with a small exposed
   share or an internal cohort, widen only when the previous stage held, and write for each stage what result
   means "hold", "go back" or "advance". The number of stages and their sizes depend on traffic and risk, so
   they are chosen per flag, not copied.
6. **Abort criteria are measurable in the time you can afford.** A criterion that needs a day of data does not
   protect a stage that lasts an hour. Where an error budget exists, the burn-rate signals of
   `skills/slo-design` §3 are the natural criteria.
7. **A user stays on one side of the flag.** For an experiment flag the article stresses a consistent cohort per
   user for the duration of the test; the same holds for a ramp, where a user flipping between old and new on
   each request is a bug of its own. Own guidance: say how the share is assigned (by a stable identifier).
8. **Dependent flags are listed.** If one flag only makes sense when another is on, write the dependency in the
   record; otherwise the combination nobody tested ships by accident.
9. **Failure to read the flag has a defined default.** Own guidance: when the flag source is unreachable, the
   code takes the safe state named in the record, which for new behaviour is normally off. This is the same
   "unknown is not safe" stance as `skills/spend-guard-fail-closed` §1, applied to a different gate.
10. **Record every change.** Each flip or stage change is noted with who, when and why, so that the ramp can be
    reconstructed and the removal in §3 knows when the quiet period started.
