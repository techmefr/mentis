# chaos-experiment §1 — Designing the experiment

> Part 1 of `skills/chaos-experiment`. Read it when an experiment is designed or reviewed.
> Source, read 2026-10-19: Principles of Chaos Engineering (https://principlesofchaos.org/). Sentences marked
> "own guidance" are ours, several restated from one MIT skill collection and not independently verified.

1. **Start from a steady state you can measure.** The principles define the discipline as experimenting on a
   system to build confidence it withstands turbulence, and begin with a measurable output that signals normal
   behaviour: throughput, error rate, latency percentiles, not internal details. The aim is to check that the
   system works, not to explain how.
2. **State the hypothesis as "this holds under that fault".** The principles predict that steady state is the
   same in a control group and an experimental group, and the experiment tries to disprove it. Own guidance:
   write it as one sentence naming the fault, the signal and the tolerance, so a result can contradict it.
3. **Write the plan before the run.** A hypothesis written afterwards is a post-mortem. The same goes for the
   signal and the tolerance: picking them while the fault is running lets any result look fine.
4. **Inject one realistic event.** The principles say variables should mirror what really happens: hardware
   failures, software faults such as malformed responses, and non-failure events such as traffic spikes or
   scaling, prioritised by likely impact or frequency. Own guidance: one fault at a time, so a change in the
   signal has one cause; a combined scenario comes after the single ones are understood.
5. **Size the fault in numbers.** "Slow" or "a bit" varies by reader; write the amount, the duration and the
   target. The numbers come from the system and its budget, not from another team's plan.
6. **Production is where it counts, and you get there in steps.** The principles hold that behaviour depends
   on real traffic and environment, so production gives the most authentic result. Own guidance: a first run
   of a new fault in a safer environment to prove the injection and the rollback, then a small share of real
   traffic, widening only after a clean run.
7. **Minimise the blast radius.** The principles say production experiments can hurt customers, some
   short-term impact is accepted, and the person running it is responsible for containing it. Own guidance:
   name the scope (which users, which instances, which region) and what is outside it, and check that the
   scope holds before starting.
8. **Check the budget first.** Own guidance: an experiment spends reliability on purpose; compare the worst
   case with what remains of the period's error budget (`skills/slo-design` §2) and do not start when it is
   spent or nearly so.
9. **Write abort criteria before starting.** The principles speak of containment but do not list stop rules;
   this one is own guidance. Each criterion is a measurable signal, a threshold, an action and a person, and
   it can be checked quickly enough to matter. Where a flag or switch is the stop, it is one already proven
   (`skills/feature-flag-lifecycle` §2).
10. **Plan the way back and test it.** The injection tool can fail to undo the fault, and effects such as
    caches or open connections can linger. The plan says how to remove the fault, how to confirm the signal
    recovered and what to do if it does not.
11. **Say what you expect to learn, and what you do not.** Own guidance: predicting the outcome makes a surprise
    visible; a result you predicted raises confidence, one you did not is a finding.
12. **Tell the people who would be woken.** The on-call, the owner of any dependency in scope and anyone who
    has been promised nothing will change are told before, with the start, the scope and how to stop it.
13. **Do not start when the team is already stretched.** Own guidance: during a release freeze, a live
    incident, an unmeasured system or a day the team has no capacity to watch, the answer is later.
