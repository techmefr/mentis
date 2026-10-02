# execute-plan §4 — The ledger and the decision register

> Section 4 of `skills/execute-plan`. Read it at step 1 when opening the ledger, and at step 5 when a decision
> comes up that is not a stop.

1. **The ledger is one file per plan, outside version control.** Its first line names the plan file. A ledger
   whose first line names a different plan belongs to that plan: leave it and start your own.
2. **What it holds, in order**: the conflict table from the pre-flight scan; per task the BASE commit, the
   completion line (`Task N: complete`, its commits), and each fix round with its number; the decision register;
   the observations the scoped re-reviews set aside.
3. **Resuming**: a task with a completion line is done and is not dispatched again; a task that ends on a
   fix round is mid-loop and resumes at the next round; everything else starts fresh. The commits the ledger
   names exist in the log even when nobody remembers making them.
4. **A register entry has three parts**: what was decided, why, and what it costs if it was wrong. For example:
   "Decision: the retry limit comes from the config key the plan names, not a new constant. Why: one source for the
   value. Cost if wrong: one replace." It is a record, not a question.
5. **What belongs in the register**: a tie between two options the spec allows, an ordering the spec leaves
   open, a name, the resolution of a contradiction inside the plan that the spec settles. The spec is the
   binding authority and the plan is its argument; where the spec is silent, the register records the judgement.
6. **What does not**: a change to behaviour the spec states, to a public contract, to stored data, to a
   security property, or anything the operator reserved. Those are stops (`SKILL.md` step 6), asked before they
   are done, because a wrong register entry is cheap to undo and these are not.
7. **Read the register back at the end**, in the closing message to the operator: every entry, one line each. A
   decision nobody can see is a decision nobody could overrule.
8. **When the run ends**, the ledger stays until the branch is merged; then it is deleted. It is scratch, and
   a stale one is the first thing the next run would mistake for its own progress.
