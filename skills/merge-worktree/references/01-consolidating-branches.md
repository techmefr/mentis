# merge-worktree §1 — Consolidating neighbouring branches

> Section 1 of `skills/merge-worktree`. Read it when several branches or worktrees have grown close to each other
> (overlapping files, competing implementations of the same thing, work split across sessions) and the decision to
> make is which one becomes the base and in what order the others fold in, before any merge command runs.

1. **Fill the room.** List the candidates: worktrees and branches active in a window you choose (a commit or an
   uncommitted edit within it), plus any open change request you name. Fewer than two is not a consolidation; say
   so and stop. Echo the roster to the operator before starting.
2. **The discussion is read-only.** Nobody commits, merges or checks out anything while the plan is being
   decided. The output is a plan; the git work happens afterwards through the strategies in `SKILL.md` step 2.
3. **One shared plan file, one section per branch.** It holds the goal ("collapse these into one branch: what
   each changed, where they overlap, which is the target, in what order"), then each branch's entry, then the
   open items, then the conclusion. Write to it one at a time (a lock file, or turns), so two writers never
   interleave.
4. **Each branch is read by its own reader.** A fresh agent per branch, given the path to the plan file and that
   branch alone: its log against the base, its diff stat, its uncommitted state. It posts one entry: what the
   branch does, how far along it is, what it touches, and how it should fold in. A reader never speaks for
   a branch it did not read.
5. **List the open items yourself between rounds.** Read the whole file and write down each overlap, each conflict,
   each pair of competing implementations, and the target and order if they are undecided. Zero items means
   straight to the conclusion.
6. **Resolve in rounds, with only the people the item concerns.** Re-ask the readers of the branches an item
   involves, with the specific question, after they have read what was said since their last entry. Cap the
   rounds (about four); a room that has not converged by then goes to the operator with the open items.
7. **Write the conclusion yourself, in plain prose**, not a field dump: which branch is the target and why, the
   merge order in a sentence, what is skipped (an empty branch, a superseded one), and the one or two decisions
   that are the operator's before it is safe. Say what "done" looks like (everything folded into the target and the
   proof green).
8. **Then merge as usual**: one branch at a time, under review (`SKILL.md` step 2, multi-worktree), proof after each,
   `finish` once the leftovers are useless. The plan file is scratch and goes with them.
9. **A reader that fails to report is noted as "did not report", not waited for.** The plan proceeds without its
   entry and the gap is on the conclusion, so the operator knows that branch was not read.
