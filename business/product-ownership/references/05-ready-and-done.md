# § 5 — Ready and done, stated once

> Section 5 of `business/product-ownership`. Read it before a story is picked up, and when delivered work
> is being accepted.

1. **Ready to start**: the problem is stated, criteria are testable, the unknowns are either answered or
   carved out as a spike, and the dependencies are named. Four conditions, all checkable in a couple of
   minutes — which is the point: a ready bar that takes a meeting to apply is a ready bar nobody applies.
2. **Done** means merged with the pipeline's guarantees met — gate passed on cited evidence, review
   findings closed (`WORKFLOW.md` §3). Not "the developer says it works". The reason it is stated this
   way is that a claim of completion is the cheapest thing in the process to produce and the most
   expensive to check later.
3. **A story that can't be made ready is split or sent back**, not started hopefully. Starting it converts
   an unanswered question into rework: the developer answers the question by choosing, the choice becomes
   code, and the correction now costs the implementation plus the undo.
4. **Whoever accepts the work isn't the person who built it.** Same reason the gate uses a fresh-context
   judge. Where the organisation genuinely has one person doing both (§9), the separation has to be
   replaced deliberately rather than quietly dropped.
5. **Ready is a checklist someone applies, not a state someone feels.** The failure is specific: a story
   is called ready because the sprint starts tomorrow, and the four conditions of point 1 are checked
   retrospectively by whoever gets stuck. Apply it at the moment of picking up, out loud, and let a
   failed check cost fifteen minutes instead of two days.
6. **A spike has an output and a bound.** A question carved out as a spike needs a written answer, a
   deadline and a decision that follows it; without those it is work that disappears — time is spent,
   nothing is recorded, and the same unknown blocks the story again next month. "Two days, and the output
   is a paragraph saying which of the two approaches we take."
7. **Merged is not the last mile.** A feature behind a flag that is off, a migration that has not run, a
   permission not granted to the people who need it, a document not updated: each leaves the work
   delivered and unusable. The done bar includes whatever it takes for a real user to reach it.
8. **A done story produces the announcement.** The person who asked should learn from you rather than by
   noticing — and if nobody can be told because nobody remembers who asked, §1.12's record is what was
   missing. This is also the cheapest source of the next request's context.
9. **A story that is done except for one thing is not done.** Carve the remaining thing into its own item
   with its own decision, so the state is honest and the leftover is either scheduled or refused.
   "Done-ish" items are how a backlog accumulates work nobody can total up and nobody will finish.
10. **Reopening beats a duplicate.** When accepted work turns out not to meet a criterion, reopen the
    story — a second story describing the same need loses the history, splits the discussion, and makes
    the delivery record say the work was completed twice.
11. **The definition is written once and applies to every story.** Per-story ready and done bars are
    negotiated per story, which means they are negotiated when the pressure is highest. One definition,
    visible, is what makes point 3 a procedure rather than a confrontation.
12. **A story cancelled after being started is a normal outcome and gets the same write-up as a refusal**
    (§3.11): what was learned, and what would make it worth restarting. That record is the only value
    the abandoned work still has, and it is lost by default.
13. **A ready checklist that only ever grows is solving the wrong problem.** Every incident adds one more
    line, and a year in, applying the bar takes longer than the story it gates — at which point people
    stop applying it and check it retrospectively instead, which is exactly the failure point 5 describes.
    An experienced team's list shrinks as members learn to recognise the missing piece without a line item
    for it; a list that only accumulates is a sign nobody is allowed to remove a check that stopped
    earning its place.
14. **One shared bar across teams needs a floor everyone can meet, not a ceiling everyone negotiates.**
    A board that mixes several teams either drags the strictest team's bar down to what the loosest team
    can hit, or asks the loosest team to defend criteria written for someone else's stack. The fix is a
    short common floor plus whatever each team adds on top, named as theirs — not one list pretending to
    fit all of them.
15. **Vague completion criteria is a leading cause of sprint failure, not a cosmetic complaint.** When
    "done" and "ready" are read differently by the person who wrote the story and the person building it,
    the gap surfaces mid-sprint as a scope argument neither side saw coming, and the sprint slips for a
    reason that was decidable a week earlier at zero cost.
16. **A spike's ready bar is not the story's ready bar.** A spike is ready when the question and the
    timebox are both written down (point 6); demanding testable criteria or a target implementation before
    a spike starts defeats the reason it exists, which is that nobody yet knows enough to write those
    criteria. Applying the wrong bar to a spike is how investigation work quietly turns into unplanned
    delivery work.
17. **Done without a rollback path is done for the version that never needs to be undone.** A migration
    with no down-path, a flag with no kill switch, a release nobody can revert without a full redeploy:
    each converts the next incident into a longer outage than the feature warranted. The rollback question
    belongs in the same bar as the feature, decided before merge, not improvised during the incident.
18. **A story sitting "in progress" with nobody touching it is not blocked, it is abandoned quietly.**
    Blocked has a named blocker and a next check-in; a story that simply stalled has neither, and it stays
    on the board making the team's throughput look worse than it is while teaching nobody anything. Either
    name the blocker or move the story back — a silent stall serves no one.
19. **The definition itself needs an owner, or every dispute becomes a renegotiation.** When ready and
    done are nobody's document, each contested story reopens the definition from scratch, and the person
    with the most time in the room wins. One named owner, and a way to propose a change outside the heat
    of a specific story, is what makes point 11's "written once" durable rather than aspirational.
