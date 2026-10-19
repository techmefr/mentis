# reuse-before-write §3 — Guards, bug fixes, tests and the closing note

> Section 3 of `skills/reuse-before-write`. Read it when the ladder produced a shorter answer than you expected,
> when the change is a fix, when it moves or merges code, or when it contains logic.

## The never-cut list
1. **The ladder never removes any of these:** validation at a trust boundary (anything that arrives from a
   user, another service or a file), error handling that prevents losing data, security measures, accessibility
   basics, hardware calibration a device needs, and anything the task or the operator explicitly asked for.
2. **A short answer that drops one of them is not shorter, it is incomplete.** The lines a "keep it minimal"
   instruction cuts first are usually the guard clauses; that is the defect the list exists to prevent.

## Moved and merged code
3. **Code you move or merge keeps its error handling and its validation.** Folding two handlers into one is
   the moment a guard disappears without anyone deciding to remove it.
4. **Check the merged result against both originals' callers,** not only against the one you were editing.

## Bug fixes
5. **Before editing, grep every caller of the function you are about to change.** Include tests, fixtures and
   config, not only source.
6. **Fix the cause once, in the shared code.** Patching one caller while the shared function stays wrong
   leaves every other caller broken and teaches the next reader that the function is safe.

## Logic leaves a check behind
7. **New non-trivial logic leaves one small test:** a branch, a loop, a parser, money arithmetic, anything
   security-related, or a whole new script. One test that fails when the logic breaks, not coverage.
8. **A trivial change needs none.** A rename or a copy change is not worth a test of its own.
9. **Short code without its check is unfinished,** which is what makes this a guard and not a style point.
   Where tests and the change are written in separate steps, `tdd` still owns the order; this point is about
   not letting the shortest answer drop the check.

## The closing note
10. **End the reply with one or two lines:** what you skipped on purpose (the unrequested option from rung 1,
   the case you did not handle), what you did not check, and any risk the reviewer must know before merging.
11. **It is a rule inside this block, not a mode for the whole session.** It appears when this block ran, and
   it names facts, not apologies.
12. **Never present it as a saving.** "Skipped the retry logic, no caller needs it today" is a fact a reviewer
   can overrule; "saved 80 lines" is a claim about code that was never written.

## What this block does not carry
A record of deliberate shortcuts inside the code. The team writes no comments in code, so a deferral that
has a limit and an upgrade trigger goes in the merge request description or the decision record
(`skills/documentation-adr`), where a reviewer reads it.
