# bug-triage §6 — Before the first hypothesis

> Section 6 of `skills/bug-triage`. Read it between getting a reproduction (§2) and handing over to `debug`
> (§4), when the cause is not obvious: intermittent behaviour, a regression with no suspect, a failure that appears
> only in one environment, or a test that fails only when run with others.

1. **Separate the symptom you saw from the cause you infer.** "The export returns an empty file" is observed.
   "The query times out" is a hypothesis until a log, a trace or a measurement shows it. Write them in two
   columns, and mark each entry with the evidence it rests on.
2. **Compare the case that works with the case that does not.** Before guessing, find a working instance (another
   account, the previous version, the same input in another environment) and list every difference between it and
   the failing one: data, configuration, versions, permissions, ordering, time. The cause is almost always
   in that list. Read the reference implementation completely before using it as the model.
3. **Rank the hypotheses by evidence, then by the cost of disproving them.** Test first the one that is cheapest to
   falsify among the plausible ones, since a cheap negative narrows the field faster than an expensive positive.
   Do not edit product code until one mechanism explains all the evidence.
4. **One change per experiment.** Two changes at once make the result unreadable. Record what each experiment
   was meant to show before running it.
5. **Trace the value back to where it went wrong** instead of fixing where it showed up. The place a failure
   surfaces is the last place it could have been caught, rarely the first.
6. **Stop exploring when the evidence names a cause or an exact blocker.** More reading past that point is
   avoidance. Report the cause and the proof; make no fix unless the task authorises one.
7. **No cause found within the bounds you set is a result.** When the failure is truly environmental, timing
   dependent or external, say so, then leave behind what makes the next occurrence diagnosable: the instrumentation
   or logging that would have caught it, the conditions observed, the note of what was ruled out. Do not ship a
   guessed fix; in most cases "no cause" means the investigation was incomplete, so check the comparison in
   point 2 once more first.
8. **Three failed hypotheses are a signal about the approach, not about the fourth guess.** Stop and question the
   model of the system you are working from, or escalate (`skills/debug`, `skills/when-stuck`).
9. **Hunting a test that pollutes others.** When a test fails or leaves state (a file, a record, a global) only
   when run after another, bisect: run the test files one at a time, or in halves, with the check for the stray
   state after each, until the single file that creates it is isolated. Skip any file when the pollution is
   already present before it runs. Then read that file for the shared resource: a global, a temporary path
   reused, a database row not cleaned up, a timer left running. A small script in the project's own task runner
   is enough; it needs no new tool.
