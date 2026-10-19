# receiving-review-pitfalls §2 — Implementing and replying

Once the feedback is understood and checked (§1), the work is to apply it in a safe order, to refuse what is wrong
with evidence, and to answer in a way the reviewer can act on.

## 2.1 The order of fixes
1. **Clear up every unclear item first** (§1.2).
2. **Then apply in this order:** blocking issues (breakage, security), then simple fixes (typos, imports), then
   complex ones (refactoring, logic).
3. **Verify there are no regressions after the whole list**, in addition to the test of each item (§2.2).

## 2.2 One item at a time, tested
1. **Apply one item, run the tests that cover it, then take the next.** The source lists "batch without testing"
   as a mistake. Own reasoning: when a batch breaks, you no longer know which item did it.
2. **A fix with no test of its own is not done.** Own guidance: if no existing test covers the point the reviewer
   raised, the fix adds one or says why none fits.

## 2.3 Pushing back
1. **Push back when** the suggestion breaks existing behaviour, the reviewer lacks context, it asks for a feature
   nothing uses (§1.5), it is technically wrong for this stack, legacy or compatibility reasons exist, or it conflicts
   with an architectural decision.
2. **How:** give the technical reason, ask a specific question, and point at working code or a passing test. The
   source contrasts this with defensiveness, which is a reaction to the comment rather than to the code.
3. **If the disagreement is architectural, involve the owner of the decision** rather than settling it between
   author and reviewer.
4. **A pushback is a claim you can be wrong about.** Own guidance: state it with the evidence that would change your
   mind (a test, a call site), so the reviewer can answer it in one reply.

## 2.4 Replying
1. **When the feedback is correct, state the fix and where it is**: what changed and in which file or commit. The
   source's reasoning is that the change itself shows the feedback was heard.
2. **Agreeing before verifying gives the reviewer nothing to check.** Own guidance: a reply that says only that the
   reviewer is right, sent before the checks of §1.3, hides whether anything was verified.
3. **If you pushed back and were wrong, state the correction factually and move on.** Say what you checked, what the
   code does, and that you are applying the change. The source lists a long apology, a defence of the earlier
   pushback and over-explaining as the things to leave out.
4. **Tone rules are not carried.** The source also forbids any expression of thanks and lists exact phrases to avoid;
   whether to thank a reviewer is a team norm, and this block does not set one.

## 2.5 Where the reply goes
1. **Reply inside the inline comment's thread, not as a new top-level comment.** On GitHub the source names the
   reply endpoint of the pull request comments API for this. Whatever the host, the answer belongs next to the
   comment it answers, so the reviewer sees the resolution where the question was asked.
2. **Every comment gets an outcome, never silence**; the fix-or-reasoned-pushback rule is in `mr-conventions`
   and this section is how to reach either outcome safely.
