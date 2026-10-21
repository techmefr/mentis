# quality-bar-and-ratchets-pitfalls §3 — Guarding the bar

Source: the constraint-driven-development skill and its floor-guard reference in addyosmani/agent-skills (MIT), read 2026-10-21; the contract in 3.6 is rewritten, no code taken.

An agent that meets a red check takes the cheapest road to green; it does not need to be clever. The guard looks
for five moves in the diff and reports only the ones that lower the bar: tightening is silent, loosening is loud.
Existing hooks already cover tests and runner or linter configuration (`guard-test-changes`, `config-protection`);
this section adds what they do not read.

## 3.1 The five moves
1. **A threshold moved.** A limit loosened, a severity dropped, a check removed from the fast stage, a rule
   deleted from the bar file. **Check:** compare the bar file at the branch point with now. A number has a
   direction (a minimum is loosened by going down, a maximum by going up); a number whose direction cannot be
   read is reported on any change, because staying quiet is the wrong default.
2. **A test got easier.** A skip marker added, a test file deleted, assertions removed from a test that stayed.
3. **A checker was silenced.** A new suppression comment. The ones that hide what a check is relied on for:
   coverage exclusions (code dropped from the denominator instead of tested), mutation-testing disables (a
   surviving mutant hidden), static-analysis ignores and secret-scanner allow markers (a security finding
   hidden), beyond the usual type and lint suppressions.
4. **Work is unfinished.** A stub that throws "not implemented", an empty catch that turns a failure into
   silence, a to-do standing where the code should be.
5. **An exception appeared.** A new row in the exceptions table that nobody discussed.

## 3.2 Why the existing guards miss them
1. Test guards read test files; runner guards read configuration. A threshold lives in the bar file, an
   exception in its table, and a suppression in ordinary source: none of them a test or a runner config.
   **Symptom:** a green pipeline after a change that moved the limit it measures against.

## 3.3 Landing a change to the bar
1. **The bar is changed alone.** A commit that edits the bar and the feature that was failing it is the warning
   sign (`skills/gate`, guardrails). **Fix:** two changes, the bar change first with its reason, read by a human.
2. **An agent that proposes relaxing a threshold instead of fixing the code** has found the cheapest road; hand
   the decision to the owner of the file.
3. Tightening needs no review; reporting it would train people to ignore the report.

## 3.4 Where the guard runs
1. At review time, against the merge base, over the diff plus untracked files: a guard that reads only the
   tracked diff misses new files and uncommitted work.
2. In CI, so a local skip of a hook is not the only barrier.
3. Alongside the hooks, not instead of them: a hook stops the edit, the guard reads the whole change.

## 3.5 Exit states
1. Clean, violation found and could not run are three states. **Symptom:** the guard cannot find a merge base
   (shallow or rootless clone) and exits as if clean. **Fix:** a distinct failure code that no caller reads as
   success.

## 3.6 Contract for a guard script
1. Input: the merge-base diff, added and removed lines, plus untracked files, read from the top of the work tree
   whatever the current directory.
2. Output: rule and location, never the matched content when it may be a secret; at most a truncated line.
3. Patterns per ecosystem live in a list the team edits; the stack-neutral part is the five moves.
4. The guard is deterministic text matching on the diff. It does not judge whether a suppression is justified;
   it makes a human or the evaluator look at it (`skills/gate`, step 3).
5. A hook version, if wired, belongs beside `guard-test-changes` and follows its wiring in `hooks/README.md`;
   this block ships none, because the rules above stand without it (rule A).

## Checks
1. The diff was read for each of the five moves, by a guard or by hand, and the result is written down.
2. Any loosening found is reverted or recorded as an exception with owner and expiry.
3. The guard distinguishes "could not run" from "clean".
