# safe-refactor §1 — The surgical patch

> Section 1 of `skills/safe-refactor`. Read it when the change is a bug fix or a small behaviour change, not a
> restructure: the proof protocol is the same, the allowed surface is narrower.

1. **Reproduce first when it is cheap, and say so when it is not.** A failing test or a command that shows the
   defect is the strongest evidence a fix can start from. When reproduction is expensive or impossible (a
   production-only condition), state what evidence you have instead; do not present a guess as a reproduction.
2. **Trace the symptom to the mechanism that owns it.** The line that throws is rarely the line that is wrong.
   Follow the value back to where it became incorrect; a fix at the symptom leaves the cause producing the next one.
3. **Change the narrowest layer that owns the wrong behaviour.** Not the caller that happens to see it, not a
   wrapper that hides it. If five callers each work around the same defect, the defect is the fix.
4. **A fix touches the lines that carry the cause.** Renames, formatting, a tidier loop nearby and an
   abstraction you would prefer all go in a separate change. A reviewer who has to separate the fix from the
   cleanup will do it by approving both or neither.
5. **Remove only what your own change orphaned.** An import or a helper your fix made unused goes with it.
   Dead code that was already there is reported, not deleted.
6. **Add the regression proof the fix needs, no more.** One test that fails without the change and passes with
   it (revert the fix, watch it go red, restore it). Not a new test suite around the neighbourhood.
7. **Run the focused proof, then the nearest gate that could be affected**, and stop when both are green. The
   wider verification belongs to `gate`, not to the patch.
8. **Preserve what was not asked to change**, including behaviour you dislike and uncommitted edits other people
   made in the same files.
