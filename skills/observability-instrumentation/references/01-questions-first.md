# § 1 — Define the questions before instrumenting

> Section 1 of `skills/observability-instrumentation`. Read it before adding the first log line or
> metric. `skills/api-design` §2 cites this section as the source of usage data.

1. State 2 to 4 concrete questions the on-call will ask during an incident ("why is this request
   slow?", "how many users are affected?"), **before** writing the first log or the first metric. The
   order matters because instrumentation written first is written from the point of view of the code:
   it records what the function did, which is what you already know at three in the morning, and not
   which requests were affected or when it started, which is what you do not.
2. Every piece of data collected must answer at least one of those questions: a metric/log that
   answers none of the questions asked is noise, don't add it. Noise is not neutral — it is paid for
   twice, in storage and in the time an on-call spends discarding it while the incident continues.
3. **Write the questions down where the next person will find them**, next to the instrumentation or in
   the merge request. Unrecorded, the questions cannot be used to judge whether a later log line
   belongs, so the discipline lasts exactly one change.
4. **A question has to be answerable from what is collected, end to end.** "How many users are
   affected" needs a user dimension somewhere, and it is often the one thing cardinality rules keep out
   of the metric (§3.2) — so the answer has to come from logs or traces instead. Deciding that when the
   question is written is what stops the answer being discovered to be missing during the incident.
5. **Include the "did the fix work" question.** It is the one nobody states and the one the on-call
   needs last: something has to move visibly when the mitigation lands, or the operator is left
   deciding whether to keep going with no feedback.
6. **The questions are about the failure, not about the feature.** Success paths are what dashboards
   already show and what nobody looks at during an incident; the useful set is what breaks, how it
   breaks partially, and what a partial failure looks like from outside.
7. **Instrumentation earns its place the same way any other structure does, and it can stop earning
   it.** A dashboard nobody opened during the last three incidents, a metric no alert or query reads, a
   log line whose format nothing parses: each is cost with no reader. Remove it, and say so
   (`skills/design-patterns` §6).
8. **Retention is part of the decision.** Data kept for a day answers a live incident and nothing about
   a slow regression; data kept for a year costs accordingly and, where it contains anything personal,
   becomes a retention question with an owner (`business/data-protection`). Decide it when the
   instrumentation is added, not when the bill or the request arrives.
9. **What is collected has to be findable by someone who did not write it.** A metric whose name says
   nothing, a log field whose meaning lives in the code, a trace span named after an internal class:
   each is data that exists and cannot be used by the on-call, which is the only reader this section is
   about.
10. **The instrumentation is verified with real traffic, once.** A log line that renders an object
    unhelpfully, a metric that is always zero because the label was misspelled, a trace that never
    links: all of these look correct in code review and are visible in one look at the actual output.
    That look is the cheapest check in this block and the one most often skipped.
