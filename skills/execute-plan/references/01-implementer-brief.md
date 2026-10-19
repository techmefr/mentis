# execute-plan §1 — The implementer brief

> Section 1 of `skills/execute-plan`. Read it at step 4.2, each time a worker is dispatched. The template is
> written for any agent runtime: "worker" is whatever executes a delegated task.

1. **The brief is a file the worker reads first**, holding the full task text from the plan, the global
   constraints that bind it (exact values and formats, not process rules), and one paragraph of scene-setting:
   where the task sits, what it depends on, which interfaces it must honour. Nothing from the controller's
   conversation travels with it.
2. **State the model and the working directory in the dispatch itself**, never inherited by default.
3. **The worker asks before it starts.** Requirements, acceptance criteria, approach, dependencies, any
   assumption it would otherwise have to make: all questions go up front, and a question raised mid-task is as
   welcome as one raised at the start. Guessing is the failure; pausing is not.
4. **What the worker does, in order**: implement exactly what the task specifies; write the tests the task
   calls for, test first where the plan says so; run the focused test while iterating and the full suite once
   before committing; commit; read its own diff against the brief; write the report.
5. **Self-review has four questions.** Completeness (is everything in the brief built, are the edge cases
   covered), quality (do names say what things do, is it maintainable), discipline (nothing built that was not
   asked, existing patterns followed), tests (do they check behaviour rather than mocks, is the output free of
   stray warnings). Fix what you find before reporting.
6. **The worker does the task itself and dispatches nothing.** No sub-worker for the implementation, and above
   all no reviewer spawned for its own work: the controller schedules the real review after the report, and a
   review the worker commissions has no standing in the process.
7. **Structure stays as the plan drew it.** A file growing past the plan's intent is reported as a concern, not
   split on the worker's own initiative; an already tangled file it must edit is edited carefully and
   mentioned.
8. **Stopping is allowed and is not penalised.** Blocked or uncertain (an architectural choice the plan did not
   make, code it cannot understand after reading enough of it, a restructuring the plan did not foresee):
   report `BLOCKED` or `NEEDS_CONTEXT` with what it is stuck on, what it tried and what it needs. Bad work is
   worse than no work.
9. **The report is a file, plus a short message.** The file holds: what was built or attempted, what was
   tested and the results, for a test-first task the red output before the change and the green output after,
   the files changed, the self-review findings, concerns. The message, under fifteen lines, holds: the status
   (`DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, `NEEDS_CONTEXT`), the commits (short hash and subject), a one-line
   test summary, the concerns, the report path. Detail stays in the file (`references/terse-reporting.md`).
10. **A worker resumed with review findings** fixes them, re-runs the tests that cover the amended code, and
    appends to its report what changed, which tests ran, the command and the output. Reviewers do not re-run the
    suite for it; its appended evidence is what they read.
