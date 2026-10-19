# block-eval-method §2 — Instruments before spend

> Section 2 of `skills/block-eval-method`. Read it when a task set is written. Every scoring instrument is
> proven on known answers before any run is paid for.

1. **Mix task types, and say which can have a hidden check.** Surgical tasks (implement this function, fix this
   bug, rename a field that must reach every caller) can be scored by running the produced code; open tasks
   ("build me a small tool", "add a picker to the form") cannot. The source's set contained both, in roughly
   equal measure, on purpose.
2. **A hidden check is deterministic and runs the code.** Standard library only, no model in the loop: it
   imports what the agent produced and calls it with normal input (correct?) and with adversarial input (safe?).
   Example for a Laravel-style task: an endpoint that lists a user's orders, checked by calling it as user A and
   asserting that user B's rows never appear.
3. **Keep the requirement implicit, the way a real ticket reads.** The task says "untrusted filename", not
   "guard against path traversal". An arm that forgets the guard is then caught; spelling the requirement out
   tests reading comprehension.
4. **Ship a good and a bad reference answer with every check, and run a self-test first.** The good one must
   pass, the bad one (correct on the happy path, unsafe on the adversarial input, which is what a hurried author
   actually writes) must be caught on its declared axis. A run is refused if the self-test fails.
5. **Reapply measurement changes offline.** With the workspaces kept (§1.10), a changed metric or scorer is
   recomputed over the stored results with no new runs.
6. **A crashed cell counts as failed,** in both the correct and the safe columns, rather than crashing the
   summary or vanishing from it.
7. **Only the tasks with a hidden check count as a quality result.** On the others "pass" means only that
   something was delivered. Report size and completeness (§4) for them and make no pass-rate claim; the
   source states this itself and keeps the two groups apart in its tables.
8. **Tests the agent writes are a positive signal, never size.** Count them separately from delivered code. A
   self-check inside the same file (a demo block, a `main` guard) is split off and counted as test, so that
   following a rule that asks for a check is not scored as bloat against the arm that follows it.
