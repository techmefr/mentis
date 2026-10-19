# chaos-experiment §2 — Running, stopping and learning

> Part 2 of `skills/chaos-experiment`. Read it when an experiment is about to run or has just run.
> Source, read 2026-10-19: Principles of Chaos Engineering (https://principlesofchaos.org/), for the
> automate-continuously and contain-the-fallout ideas. Everything else is own guidance, restated from one MIT
> skill collection's workflow and not independently verified.

1. **Measure the baseline just before, not from last week.** Own guidance: the steady-state signal is read
   under the same conditions for long enough to see its normal wobble, so a breach means something.
2. **A person who can stop it watches the signal for the whole run.** Unwatched fault injection is an
   unplanned change to production.
3. **When an abort criterion is met, stop first and investigate after.** Own guidance: the stop is the first
   action, scripted where possible, and it is not delayed to understand what is happening.
4. **After stopping, confirm recovery with the same signal.** If the signal does not return to normal in the
   time the plan allows, the experiment has become an incident and is handled as one
   (`skills/incident-comms-pitfalls`).
5. **Keep a timestamped note as it happens.** Memory of the sequence is wrong within a day; record what was
   injected, what the signal did and which actions were taken.
6. **Declare the result against the hypothesis.** Confirmed, refuted, or inconclusive (and why). Own guidance:
   an inconclusive result because the signal was too noisy is itself a finding about the measurement.
7. **A refuted hypothesis is the product.** The experiment found a gap before a customer did. Record the
   mechanism as far as it is known, and keep the language about causes and conditions, not people
   (`skills/blameless-incident-review-pitfalls`).
8. **Every finding gets an owner and a date, or it is not a finding.** Own guidance: an experiment that yields
   no action either confirmed something worth writing down or was too gentle to teach anything.
9. **Adjust the size by what happened.** Always passing means the fault may be too small to teach; always
   breaking means it is too large to read. Change one thing, and record why.
10. **Repeat what mattered.** The principles say manual experiments are labour-heavy and do not scale, and that
    automating orchestration and analysis allows continuous running. Own guidance: automate a run only after it
    has gone cleanly by hand, with the same abort criteria wired in, and keep the budget check in the loop.
11. **A fix is checked by running the experiment again.** The same plan, after the change, is the regression
    test for the weakness it found.
12. **Share the write-up.** A result known to one person is lost when they move; the plan and the write-up live
    where the team that owns the system can find them.
