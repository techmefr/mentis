# gate §9 — The verification loop

> Section 9 of `skills/gate`. Read it when the change is about to leave your hands: before the evaluator of
> step 3, before a review, before a commit that claims to be finished. The commands come from the project (its
> task runner, its CI file); this section fixes the order and the report.

1. **Phases run in a fixed order, and a failed phase stops the loop.** Build, then types, then lint, then tests,
   then the sweep of the diff. A later phase run on a failed earlier one reports noise: a type error produces
   a dozen test failures that are one problem.
2. **Take the commands from what the project already runs.** Read the CI definition and the task runner first;
   the phases you run are the phases the pipeline will run, with the same flags. A command you invented can
   pass where the pipeline fails.
3. **Phase 1, build.** Compile or bundle the project the way CI does. For an interpreted project with no build,
   record the phase as not applicable, not as passed.
4. **Phase 2, types.** Run the static type checker or analyser at the level the project configures. Report every
   error with its location; do not lower the level to clear it.
5. **Phase 3, lint and format.** Run the linter and the formatter in check mode, not fix mode: a fix mode
   run edits the code you are about to claim is verified, and a diff of the fixes is itself a finding.
6. **Phase 4, tests.** The project's own suite defines green (`skills/tdd`); a targeted run answers "did my
   change break its neighbours" but not "is the suite green". Report counts: total, passed, failed, skipped. A
   skipped test is listed, not hidden in the total. No coverage figure is quoted without the project's own
   tool and threshold behind it; a number recalled from habit is not a target.
7. **Phase 5, sweep of the diff.** Read the whole diff, file by file, as a reviewer would. Look for what no tool
   flags: files that should not be there (build output, local config, a pasted export), debugging leftovers
   (print statements, a test marked as the only one to run, a disabled assertion), merge-conflict markers,
   pending-work markers, commented-out code, a secret or a token or a private address, an unrelated change that
   rode along, a behaviour change nobody mentioned. Search for the secret patterns and the debug calls
   mechanically, then read what remains.
8. **One report, one line per phase**: the phase, `PASS`, `FAIL` or `N/A`, the count that matters, the first
   failures with their locations. Then the overall verdict, `READY` or `NOT READY`, and the numbered list of what
   to fix. The report is built from output you read, not from memory of earlier runs (§8.1).
9. **After a fix, restart from the first phase that failed**, not from the last. When the fix touched build
   configuration or shared types, restart from the top: a change that can alter an earlier phase invalidates
   what ran after it.
10. **Recipes by stack are the same loop with different commands.** A PHP framework project: validate the
    dependency manifest, run the formatter in check mode, run the static analyser, run the tests, audit the
    dependencies for known advisories, list the pending migrations with a dry run (`--pretend`) and read the SQL,
    check the queue and the scheduled-job declarations still load. The ordered sequence for that stack is spelled out in `skills/laravel-verification`; this section is
    the stack-neutral form. A JavaScript project: install from the
    lockfile as CI does, build, type-check, lint, test, audit. A Python project: format check, linter, type
    checker, tests, dependency audit. Add the stack's own steps where CI has them; never drop one CI has.
11. **Run the loop at natural checkpoints in a long task**: after finishing a function, after a component, before
    starting the next unit. Failures found one unit after they were introduced have one suspect.
12. **The loop does not replace the evaluator.** It is the mechanical half: a clean-context evaluator still
    reads the diff against the spec (step 3). The loop makes sure the evaluator is not spending its attention
    on a build that does not compile.
