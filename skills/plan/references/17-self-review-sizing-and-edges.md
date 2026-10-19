# plan §17 — Self-review, task size and blocking edges

> Section 17 of `skills/plan`, continuing the numbered steps of `SKILL.md` (1 to 16). Read it when `tasks.md` is
> drafted and about to be handed over, or when a task list has to be cut, ordered or re-cut. Everything here
> lands in the feature's `tasks.md` and `plan.md` (`CONVENTIONS.md` Rule E), never in a second document. Where the
> project's own spec-kit template names these things differently, the project's wins. 🟡: rewritten from two
> sources, not yet run on a real feature.

## The planner's own pass, after the last task is written

1. **Run it yourself, once, in the same session.** This is a checklist, not a dispatch: the independent
   verdict of step 16 is the heavier check for a plan that carries risk. Re-read the spec with fresh eyes, then
   the task list, and fix what you find inline. No second round: fix and move on.
2. **Coverage, both directions.** Walk the spec criterion by criterion and point at the task that delivers each.
   A criterion with no task becomes a task. Then walk the tasks and point at the criterion each serves (step 14).
3. **The step scan, for both faults.** A step that decides nothing ("add appropriate validation", "write tests
   for the above", a type or function that no task defines) pushes a decision to the implementer. A step that
   carries more than the implementer could not work out alone (a function body the signature and the test already
   determine) is the plan transcribing the code. Fix both; the test is that one reasonable thing can be written
   from the step.
4. **Name and type consistency across tasks.** Every identifier that a later task uses must be spelled the way the
   earlier task introduced it. A refund helper called `reverseCharge` in task 3 and `cancelCharge` in task 7 is a
   defect the implementer of task 7 will resolve by inventing a third name. Grep the list for each name that
   crosses a task boundary.
5. **Give each task an Interfaces note.** An implementer sees its own task and little else, so each task states
   what it consumes from earlier tasks (exact signatures) and what it produces for later ones (names, parameter
   and return types). That note is what makes point 4 checkable and what step 4's "point at the other task's
   interface" refers to.
6. **Proportion, last.** If the plan is several times longer than the spec, most of it is code blocks: cut bodies
   back to signatures, test names and assertions, and re-check that each step is still unambiguous.

## How big a task is

7. **A task is the smallest unit that carries its own test cycle and is worth a separate look from a reviewer.**
   Setup, configuration, scaffolding and documentation steps fold into the task whose deliverable needs them. Split
   only where a reviewer could sensibly reject one task and accept its neighbour. Every task ends with something
   independently testable.
8. **Inside a task, a step is one action with a checkable result.** Example: write the failing test; run it and
   see it fail for the stated reason; write the minimum code; run it and see it pass; commit. A step that bundles
   two of these cannot be checked off honestly.
9. **Cut along the file map, not along technical layers.** Files that change together live in one task, so a task
   is not "the database part" unless the change really is only that. This is step 8's file map applied to the
   cut. In an existing codebase follow the layout already there; a split of a file that has grown unwieldy is a
   task of its own, not a side effect.

## Blocking edges between tasks

10. **Every task states what blocks it, and says "none" when nothing does.** "Blocked by: task 2 and task 5" or
    "none, can start now". An absent line is read as unknown, and an unknown edge is how two tasks end up started
    in the wrong order. The edges are written in `tasks.md` next to the task, not in a file of their own.
11. **An edge is a real gate.** The test for each one: could this task start and finish if the other did not
    exist? If yes, the edge is decoration and it serialises work for nothing. If the answer is "only by guessing the
    other task's interface", the edge is real, or the interface belongs in a task both can read.
12. **Order blockers first, and work the frontier.** The frontier is every task whose blockers are all done; a
    purely linear plan reads top to bottom. Write the list in that order so a reader never meets a task before the
    one that gates it.
13. **Prefactor first.** When the change would be easy after a small restructuring, the restructuring is the first
    task and the others are blocked by it: make the change easy, then make the easy change. It is a task of its
    own with its own test, not a paragraph inside the feature's task.
14. **A task is sized to one fresh context.** If the implementer would have to hold half the codebase to finish
    it, it is two tasks and the second declares the first as its blocker.
15. **A wide mechanical change is sequenced expand, migrate, contract.** Renaming a column or retyping a shared
    symbol breaks every call site at once, so no narrow task can land green. First a task adds the new form beside
    the old one so nothing breaks. Then call sites move over in batches sized by how far the change reaches (one
    per package or directory), each batch blocked by the expand task. Last, a task deletes the old form, blocked by
    every batch. When even a batch cannot stay green on its own, the batches share one integration branch and a
    final integrate-and-verify task blocks on all of them: green is promised there and nowhere earlier.

## One option under evaluation: slicing vertically

16. **One option, the owner has not decided.** A plan can cut tasks as vertical slices, each crossing every layer
    (schema, interface, tests) for one narrow behaviour and demonstrable on its own, instead of one task per layer.
    The attraction is that each slice proves the whole path early and a blocked slice does not hide a broken layer
    behind it. **This is not a rule of this block**: mentis `tdd` writes the whole set of acceptance tests first and
    runs it red on purpose (a default-FAIL contract, written from the spec by a different agent), and nothing here
    changes that. Until the owner decides how the two fit together, a plan follows the project's constitution on
    slicing, and where there is none it cuts along points 7 to 9. Points 10 to 15 (edges, prefactor, size, wide
    changes) hold whichever way the cut goes.
