# execute-plan §3 — The scoped re-review

> Section 3 of `skills/execute-plan`. Read it at step 4.5, after a fix round. It narrows the first review; it does
> not repeat it.

1. **Why it is scoped.** A full review after every fix invents new findings each round and the loop oscillates.
   Scoping to the previous findings and the fix diff makes the loop converge, and it is cheaper, so a smaller
   model tier is usually enough.
2. **Inputs, all files**: the task brief, the previous findings copied verbatim (Critical, Important and
   conformity gaps; one per line), the implementer's report with the fix report appended, and a diff file for
   FIX_BASE..HEAD, where FIX_BASE is the commit the last review ended on.
3. **Read-only, alone, no second reviewer**, as in `references/02-task-review.md`.
4. **One verdict per previous finding, in order**: addressed or not addressed, with file and line evidence.
   A fix that was only tried counts as not addressed; the defect itself has to be gone.
5. **Look at the fix diff for new breakage**, with severity and location. The fix itself is code and can
   break things; this is the only place the re-reviewer judges anything beyond the list.
6. **Do not re-review what the fix did not touch.** An issue noticed outside the fix diff goes under
   out-of-scope observations: it blocks nothing, does not extend the loop, and the controller keeps it for the
   final whole-branch review.
7. **Tests are read as in the task review**: the fix report must name the covering tests and show their output;
   the reviewer confirms that against the diff and runs a focused test only for a named doubt.
8. **Output**: opens on the first finding's verdict. Sections: finding verdicts, new breakage in the fix diff
   (or "none"), out-of-scope observations (or "none"), and a one-line round verdict: all addressed with no new
   Critical or Important breakage, or the list of findings still open.
9. **Round accounting is the controller's.** It writes the round number in the ledger. From the second fix
   round on, a worker that has not converged is replaced by a fresh one on a more capable model rather than
   resumed again; at the cap the open findings go to the operator (`SKILL.md` step 4.6).
