# gate §8 — Claims and the proof each one needs

> Section 8 of `skills/gate`. Read it before saying that anything passes, is fixed or is finished, and before
> accepting a worker's report of the same.

1. **The law: no completion claim without evidence produced in this turn.** If the command that proves the
   claim has not run since the last change, the claim cannot be made. The rule covers exact phrases, paraphrases,
   implications ("that should be it") and satisfaction expressed before verification.
2. **Four steps before the sentence.** Name the command that proves the claim. Run it whole, fresh. Read the
   full output, the exit code, the count of failures. Only then say the claim, with the evidence beside it; if the
   output does not confirm it, state the actual status with the output.
3. **Which command proves which claim**, and what is not enough:

   | Claim | Proof | Not enough |
   |---|---|---|
   | tests pass | the suite's output with zero failures | an earlier run, "should pass" |
   | linter clean | the linter's output with zero findings | a partial run, an extrapolation |
   | build succeeds | the build command exiting cleanly | the linter passing, a quiet log |
   | the bug is fixed | the original reproduction no longer fails | the code was changed |
   | the regression test works | red without the fix, green with it | it passed once |
   | the worker finished | the diff shows the change you asked for | the worker's report says so |
   | the requirements are met | a line-by-line check against the spec | the tests are green |
   | the migration worked | the resulting data inspected | the command returned success |

4. **A regression test earns its keep by failing.** Write it, run it green, revert the fix, run it and see it red,
   restore the fix, run it green. A test you never saw fail may be testing nothing.
5. **Delegated work is a claim until the diff says otherwise.** A worker's "done" is checked against the version
   control diff and the evidence it points to, then restated by you with your own run, not forwarded.
6. **Flag words are a signal to stop**: "should", "probably", "seems", "I believe", "looks right". Each one means
   the verification command has not run. Run it, then write the sentence without the hedge, or write what you
   could not check.
7. **Four proof states, never collapsed into two.** `pass`, `fail`, `unavailable` (the check cannot run here: no
   service, no credentials, no browser) and `blocked` (something prevents running it that someone can lift).
   "Unavailable" is not "passed", and it is reported as unavailable with what would make it available.
8. **Reuse a result only while its input has not changed.** A result produced on the same tree state, with the
   same command, is still evidence; one produced before the last edit is not. Do not re-run a verification whose
   input is unchanged, and do not trust one whose input has moved.
9. **Run focused checks before wide gates**, then the wide gate once. A narrow failure found in seconds beats the
   same failure found at the end of a long suite.
10. **Stop when the proof is complete.** Once every acceptance condition has its evidence, the work of
    verifying is done; do not add polish, cleanup or unrelated tests to a verification task. Report the commands,
    their results and the residual risk, and nothing more.
11. **Before any commit, push or hand-over**, run the proof for what the commit claims. A message that says
    "fixes the failing import" rests on a run that shows the import working.
12. **Requirements are checked against the spec, not the suite.** Re-read the acceptance criteria, make the
    checklist, and tick each from evidence. Tests passing means the tests pass.
