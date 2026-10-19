# block-eval-method §1 — Isolation

> Section 1 of `skills/block-eval-method`. Read it when a run is designed or when a result looks contaminated.
> A measured difference is only the block's if nothing else differed between arms.

1. **Each run gets a fresh workspace, outside any version-controlled folder.** Created empty (or seeded from a
   pinned snapshot, `skills/testing-blocks` §8.1), used once, moved to the results folder afterwards. Some agent
   runtimes show the model the branch and recent commit messages of the repository the run starts in; a run
   started inside the repository under study leaks its own history into every task. That leak was found in the
   source's own earlier runs, and it is the reason this point comes first.
2. **Switch off every ambient instruction source for every arm, identically.** Project-level instruction
   files, the operator's persistent memory, and any globally enabled plugins or skills. Otherwise the "no
   block" arm secretly runs the block (the source discarded an earlier safety result for exactly this: its
   baseline had been running the rule set it was supposed to lack).
3. **Load the block under test the way a user gets it,** through the runtime's normal loading path, not by
   pasting its text into a prompt, unless pasting is the arm under test (`skills/testing-blocks` §8.3, the
   forced arm). A pasted copy approximates the loaded one; it does not equal it.
4. **Prove what was injected, from a finished run.** Open the transcript of one completed cell per arm and
   read what the model was actually given. Do this before trusting any number, and again whenever the runtime
   is updated.
5. **Give every arm the same extra instruction and the same tool restrictions.** If the agents are told to
   write the implementation and stop, all of them are told, in the same words. If a tool is denied (for
   instance a shell, so that nobody runs a server or installs a package), it is denied for all arms. The
   measurement is then "what the agent writes", and the report says so: it does not measure what the agent can
   debug.
6. **Allow tests in every arm, not just one.** Allow tests for every arm; the point of a
   rule that asks for a test is not hidden by forbidding the others to write one.
7. **Warm the shared cache once before running cells in parallel.** The first parallel cells otherwise each pay
   to write the shared prompt prefix and look several times dearer than the later ones: an ordering effect that
   lands on whichever arm ran first.
8. **Bound every cell with a timeout and stop only that cell's own process tree.** A hung run must not freeze
   the pool, and a blanket kill must not take down the session driving the evaluation. A cell killed at the
   timeout is recorded as killed, not as an empty success (§3.4).
9. **Run the arms of one task together, in the same run.** Time of day, load and model drift then hit every
   arm alike. Comparing today's run of one arm with last week's run of another measures the week.
10. **Keep every workspace.** With the transcripts and files kept, a measurement tweak is reapplied offline
    (§2.5); without them each tweak is paid for with new runs.
