---
name: finish
description: Use after the human merge of the MR, cleans up the worktree and updates the integration branch. Closes the pipeline loop.
---

# finish

Step 11 of the pipeline (`WORKFLOW.md`). Post-merge: tidying up behind you.

## When
Once the MR has been **merged by a human** (never before).

## Steps
1. Call `finish_task(project, branch, base?)`: stops the server, removes the git worktree
   (`git worktree remove`), updates the integration branch (`develop` by default,
   fast-forward), deletes the row from the database.
2. Check that the dashboard no longer lists the worktree.

## Output / checkpoint
Row deleted: the task leaves the tracking.

## Guardrails
Don't delete the worktree by hand: `finish_task` does it cleanly. Don't run anything before the
human merge. The integration base is **configurable** (`base`), not hard-coded to `develop` if
the repo uses `main`.

## Origin
Internal starfleet (`finish_task`), rewritten our way.
