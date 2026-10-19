# execute-plan §2 — The task review

> Section 2 of `skills/execute-plan`. Read it at step 4.4, when a task's implementation is finished. The
> reviewer is a fresh, read-only agent: not the implementer, not the controller.

1. **Inputs, all files**: the task brief, the global constraints, the implementer's report, and a diff file the
   controller wrote for BASE..HEAD (commit list, stat, full diff with context). The reviewer reads the diff file
   once and treats its context lines as the changed files; it opens a file separately only when a hunk it must
   judge is cut off, and says so.
2. **Read-only on the checkout.** It does not change the working tree, the index, HEAD or any branch, and it
   does not rerun version-control commands that the diff file already answers. If the diff file is missing it
   fetches the diff itself, once.
3. **Scope is the task, not the repository.** Code outside the diff is inspected only to evaluate a named risk,
   one focused check per risk, and the report names the risk and what was checked. A changed lock order, a
   changed contract or shared mutable state are legitimate named risks: checking the call sites is the method.
4. **The report is a set of claims.** The reviewer verifies them against the diff. A rationale in the report
   ("kept simple on purpose", "left per YAGNI") is the author grading their own work; it never lowers a
   finding's severity.
5. **Tests are read, not regenerated.** The implementer ran the tests and reported them. The reviewer runs one
   only when reading the code raises a specific doubt no existing run answers, and then a focused one, never a
   whole suite or a repeated loop; if heavy verification seems warranted it recommends it. Warnings in the
   reported output are findings. Evidence that looks truncated is re-read at its path; if it is truly missing,
   that is a gap to report, and rerunning the suite to recreate it is not verification.
6. **Part one, conformity to the brief.** Missing (required and skipped, or claimed and absent), extra (not
   requested, over-built), misunderstood (right feature, wrong way or wrong problem). For a batched brief that
   lists several files, check file by file: a listed file absent from the diff is a missing finding however
   clean the rest looks. Something that cannot be judged from this diff is reported as "cannot verify from the
   diff", with what the controller should check, alongside the verdict for everything that could be judged.
7. **Part two, quality, only after part one.** Separation of concerns, error handling, duplication without
   premature abstraction, edge cases; tests that check behaviour rather than mocks; structure (one responsibility
   per file, a defined interface, the plan's file layout followed, no new file already oversized).
   Pre-existing size is not this change's finding.
8. **Severity is by effect.** Critical: breaks the task or the system. Important: this task cannot be trusted
   until fixed (wrong or fragile behaviour, a missed requirement, damage you would block a merge over: a
   verbatim duplicated logic block, a swallowed error, a test that asserts nothing). Minor: polish, "coverage
   could be broader". If the plan itself mandates something this rubric calls a defect, it is still a finding,
   labelled plan-mandated; the plan does not grade its own work.
9. **Evidence in every finding**: file and line, what is wrong, why it matters, how to fix when not obvious.
   Say what was done well, specifically, before the issues; accurate credit is what makes the rest believable.
10. **The reviewer reviews alone.** It spawns no second reviewer; a diff too large for one pass is read in
    passes and the report says so.
11. **Output**: it opens on the conformity verdict (compliant, issues found with locations, cannot verify), then
    strengths, then issues by severity, then one verdict for task quality (approved or needs fixes) with one or
    two sentences of reasoning. No preamble, no process narration, no closing summary.
