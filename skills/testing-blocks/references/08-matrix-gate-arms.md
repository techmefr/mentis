# testing-blocks §8 — Model matrix, exit gate and the three-arm protocol

> Section 8 of `skills/testing-blocks`. Read it when a block is about to leave 🟡 on the strength of runs, or
> when a result has to be compared across models or against "no block". The other sections and the guardrails
> stay in `SKILL.md`. This section is our own method, built on §1-§7; it has no external source.

## The fixture
1. **Pin everything that is not the variable.** A fixture is a repository snapshot (a commit id), the task
   prompt (exact text, in a file), the scenario's pressures (§2), the grading criteria (below), the model
   identifiers as the runtime reports them, the number of runs per cell, and the date. A result with an
   unpinned element cannot be repeated, so it cannot be compared with the next one.
2. **Grade by criteria, one observable each.** A criterion is a yes/no question about the trace or the
   resulting files ("a failing test was run before the implementation file was edited", "the output names the
   step that was skipped"). Written before the first run; changed afterwards only by starting a new fixture
   version, never to rescue a result.

## The three arms
3. **Run every scenario in three arms on the same fixture.**
   - **A, baseline**: the block is absent. This is the RED run of §1.
   - **B, routed**: the block is installed the way a user installs it, so it loads only if its description
     routes the task to it (§6).
   - **C, forced**: the block's text is placed in the context directly, so it is read whether or not routing
     would have chosen it.
4. **Read the three differences, not the three scores.** C minus A is what the block's content can do. B minus
   C is what routing loses: a large gap means the description, not the body, is the defect (§6). B minus A is
   what a user gets. A block with a large C-minus-A and a small B-minus-A needs its description rewritten; a
   block with a small C-minus-A needs its body rewritten, or a hook (§7.4).

## The model matrix
5. **Run each arm on at least two model tiers**, a small or fast one and a large one, with the same fixture.
   A block that holds on the strongest model and is ignored by a small one is an incomplete block; a block
   that only a small model needs is a block whose value shrinks as models improve, and says so in its
   `Origin`. Never average across models: report the table (criterion by arm by model), because the average
   hides exactly the cell that fails.
6. **Repeat each cell** (at least five runs for a stochastic task) and report the count over the runs, not a
   single pass. One run per cell measures luck.

## The exit gate
7. **A block leaves 🟡 on a measurement only when both of these hold:**
   - **No criterion sits at 0% in every cell.** A criterion nobody satisfies, in any arm, on any model, is
     either not observable, graded wrongly, or asks for something the agent cannot do: fix the criterion or
     the scenario before drawing any conclusion about the block.
   - **No criterion has a negative delta.** If a criterion is met less often with the block (B or C) than
     without (A), on any model, the block makes that behaviour worse. Find why before anything else; a
     positive average does not offset it.
8. **Passing the gate says "tested under pressure", nothing more.** It is not "used on real work" and does not
   prove the content is correct (`SKILL.md` guardrails). Record the fixture version, the matrix and the date
   in the block's `Origin`.

## Mechanical checks

```
grep -rnE "fixture|commit [0-9a-f]{7,}" skills/<block>/references/origin.md
grep -rnE "model[s]? *(:|=)" skills/<block>/references/origin.md
```

- A measured claim in an `Origin` with no fixture version and no model identifiers is an unrepeatable claim.
