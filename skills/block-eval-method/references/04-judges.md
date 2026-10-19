# block-eval-method §4 — Judges and their gates

> Section 4 of `skills/block-eval-method`. Read it when a model scores what no script can. The general biases and
> panel rules of judges are in `skills/llm-eval-regression-pitfalls` §2; this section is the machinery of this
> method. Every judge here has a gate, and no real scoring runs before its gate passes.

## The completeness judge
1. **Fewer lines only counts if the code still does the job.** On open tasks nothing deterministic checks that
   the feature was built, so an arm could win on size by delivering a stub. A judge scores how fully each
   delivery implements its task.
2. **Rubric, four levels:** 0 stub or placeholder, 1 partial (the core behaviour is missing or broken), 2 mostly
   complete (a stated requirement is missing), 3 fully implements the task. Completeness only: over-building,
   style, speed and security are explicitly out of its remit. It names the single most important missing piece,
   or "none".
3. **The judge sees what the agent delivered:** the diff against the seeded base on repository tasks, the
   files on fresh-file tasks, the chat reply when the agent wrote nothing. State the consequence: on repository
   tasks it does not see the rest of the repository, so a flagged "missing import" has to be checked against
   the real file before it is held against an arm.
4. **Keep the judge blind.** Replace any word that reveals the arm (a marker the rule set asks the agent to
   write, an arm's name) before the text reaches the judge.
5. **Gate:** a known-complete answer must score strictly above a stub for the same task, or nothing is scored.
   The gate logic itself has an offline test: a well-ordered pair must pass and a pair where the stub wins must
   be flagged, so the gate cannot be weakened into a no-op unnoticed.
6. **List the cells at or below partial,** with the missing piece named, and count timeouts apart (§3.4).

## The over-building judge
7. **Over-building is the axis that resists a script,** so a model scores it on the delivered source files only,
   tests excluded (a test is not over-building), against a published rubric of four levels from minimal to
   clearly over-engineered.
8. **Every score names the construct it considers unnecessary, or "none".** A score without a named construct
   is dropped: it is the guard against a judge that scores on impression.
9. **Gate:** a deliberately over-built reference must score strictly above the minimal one for the same task.
10. **Fixed judge model, lowest temperature where the runtime allows it.** When the judge runs through a
   login-based command line with no temperature setting, say so, and rely on the gate to catch the drift.

## The reply judge, in two stages
11. **Score what a reader takes away, not what a grader can dig out.** Stage one: a reader who has not seen the
   code reads only the agent's final reply and writes down what it now believes (what changed, what was left
   out, what to do now, what to watch for). Stage two: a grader sees the task, the reply, the reader's notes
   and the real diff, and scores accuracy (are the notes true), coverage (did the reader learn everything a
   reviewer must know before merging) and clarity (the reply itself, easy to read in one pass).
12. **Length is reported and never scored,** and the grader is told not to reward length or brevity as such.
13. **Gate:** against one fixed diff and four replies about it (a good one, a terse one, a long padded one, one
   that claims work not in the diff), the good reply must beat the terse one on coverage, the false one on
   accuracy and the padded one on clarity. Offline version of the gate as in §4.5.

## Pairwise reply comparison
14. **Pair run i of arm A with run i of arm B on the same task,** and shuffle which one is shown first, with a
   per-pair seed, so position cannot favour one arm and the shuffle is repeatable.
15. **Gate in both slots:** the good reply must beat the terse, the padded and the false one with the good reply
   shown first and with it shown second. A judge that only wins in one slot has a position bias and is not used.
16. **Ties count for neither side,** and the result goes through the sign test of §3.8, over pairs.
17. **The judge sees reply and diff for both candidates,** and is told to judge the reply, not the code.

## When a judge fails its gate
Stop. Do not score "just a few cells" to see. Fix the rubric or the judge model, rerun the gate, and only then
score. A judge is validated by ranking known answers, not by agreeing with the author's opinion of the real ones.
