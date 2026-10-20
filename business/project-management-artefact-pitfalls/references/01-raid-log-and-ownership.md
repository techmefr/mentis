# project-management-artefact-pitfalls §1 — RAID log and ownership

> Part 1 of `business/project-management-artefact-pitfalls`. Read it when a log is started or inherited.

A RAID log holds four kinds of line: risks, assumptions, issues and dependencies. Its value is that each line can
be acted on by one person by one date. A log that is only a list of worries is read once and never again.

## 1.1 Four kinds, kept apart
1. **A risk is something that may happen; an issue already has.** Symptom: the "risks" column holds a supplier
   that already missed its delivery. Check: ask of each line "has it occurred?". Fix: move occurred events to
   issues, with an owner and a date to resolve, and keep the risk only if a recurrence is still possible.
2. **An assumption is a fact you are planning on without having checked it.** Symptom: the plan depends on a
   budget, a person's availability or an access that nobody confirmed. Fix: write it as an assumption with who
   will confirm it and by when; an assumption that cannot be checked becomes a risk.
3. **A dependency is something another party must deliver for you, or you for them.** Symptom: a task waits on a
   team that does not know the project exists. Fix: name the supplier, the date needed and the person who agreed.
   Dependencies are tracked in §2.

## 1.2 Make a line actionable
1. **One named owner per line, a person and not a team.** Symptom: nobody acts when the trigger fires. Check:
   scan the owner column for groups and blanks. Fix: the owner is who will be asked, not who will necessarily do
   the work.
2. **Describe a risk as cause, event and effect.** "Delay" is a worry; "the vendor's security review may not
   finish before the pilot, which would push the launch" can be acted on. Fix: rewrite each risk in one such
   sentence.
3. **Give a risk a trigger and a response chosen in advance.** The trigger is an observable sign (a milestone
   missed, a number crossed); the response is one of: avoid, reduce, transfer, accept. Symptom: the log records
   risks and never changes the plan. Fix: for each risk that matters, one action with a date, or an explicit
   decision to accept it, written down by whoever can accept it.
4. **Rate by likelihood and impact, and say what the scale means.** Symptom: everything is "high" or everything
   is "medium". Fix: define each level in a line on the log's first page; rank by the product only to order
   attention, not to claim precision. Any numeric scale is yours to define, not a standard.

## 1.3 Keep it alive
1. **Review on a fixed rhythm, with a date on the line.** Symptom: the last-updated column is months old. Fix: a
   review in the regular project meeting, closed lines struck through with the reason and the date, never deleted.
2. **Separate what the project can do from what it can only escalate.** A risk outside the team's reach is
   escalated with a named recipient, and the log records the escalation and the answer.
3. **Take over a log by reading it as a suspect.** Own guidance: when inheriting one, call every owner and check
   every date; most of an old log is stale and the stale lines hide the live ones.
4. **Never log a person as a risk.** Write the capacity or the knowledge gap instead ("only one person knows the
   import job"), which can be mitigated.
