---
name: gate
description: "Use when the code is written, before the review, mechanical lock: declaring a criterion \"passing\" without evidence is forbidden, and a clean-context evaluator decides."
---

# gate

Step 7 of the pipeline (`WORKFLOW.md`). **The number one reinforcement from the scouting.**
Turns "tests are green" from a declarative wish into a **proven fact**. "Done" becomes
structural, not a claim.

## When
After `code` (implementation done), before `review`.

## Steps
1. For every `{ passes: false }` line in `test-results.json`, **produce evidence**: test
   output, `verify-flow` screenshot, or a log; then **read** it (`Read`).
2. The native `PreToolUse` hook **refuses** to write `passes: true` until the matching evidence
   has been read. You cannot declare yourself passing without observing. The scripts and the
   per-repo wiring are in [`hooks/`](../../hooks/README.md); "exists" isn't enough, the evidence
   has to appear in the read log.
3. Run the **clean-context evaluator**: a subagent **with no Write/Edit**, which didn't watch
   the build, examines the diff + the evidence and returns `PASS` or `NEEDS_WORK` + findings.
4. `NEEDS_WORK` → the findings become the prompt for the next `code` pass, driven by native
   `/goal`: the exit condition is exactly the evaluator's verdict (`PASS`), so this is a goal-based
   loop, not a manual relaunch. `/goal` re-invokes step 1-3 until `PASS` or the attempt cap.

5. **Gate on the artefact, not the exit code.** For anything that is not a test runner (a migration, a
   build, a deploy, an export, a script that calls an API), `rc=0` is not a success. Open the output: a
   `200` whose body carries an `errors[]` is a failure, a log line saying "0 rows processed" is a finding,
   and a command that printed nothing proves nothing happened as much as nothing went wrong. An instrument
   that reads zero because it was not attached is not a measured zero; say which of the two you have.
6. **Never invent a datum to fill a hole.** A default is not data: `return []` on an error fabricates an
   empty result, `0` for a failed measurement fabricates a measurement. Fail loudly, or return a value that
   carries its own absence. A value shown only as an illustration is labelled as one, and the test is
   whether the reader can see that it was not measured.
7. A journey that can run is driven as an inventory of controls (`skills/qa-exploratory-testing` §5); if
   nothing can run, say so and verify by reading the code, never by writing PASS.

## Output / checkpoint
`verified`: every line `passes: true`, each backed by evidence that was read, evaluator `PASS`.

## Guardrails
- **Exit code 0 and a populated file are claims, not evidence** (step 5), and a fallback value is never evidence (step 6).
The agent **cannot validate itself**: validation comes from the hook (evidence) + the
evaluator (clean context). Stays within native Claude Code (hooks + subagent + `/goal`), no
homemade layer — we invoke the native loop, we don't reimplement it.

## Origin
Market long-running agent patterns (default-FAIL hook + fresh-context evaluator), rewritten
our way. The iteration itself is native `/goal` (Claude Code goal-based loops), not a block.
