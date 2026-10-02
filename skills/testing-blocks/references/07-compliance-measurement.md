# testing-blocks §7 — Measure compliance across prompt strictness

> Section 7 of `skills/testing-blocks`. Read it when a block has to be measured across runs, or a rule or an agent definition has to be checked for compliance. The other sections and the guardrails stay in `SKILL.md`.

1. **Turn the block into an expected sequence of observable actions**: an ordered list in which each item can
   be seen in a trace of what the agent did (a test file written before the implementation file; a failing run
   whose output was read; a verification command run before "done"). An item that cannot be observed cannot be
   measured, and a block made only of such items is a block to rewrite as a hook.
2. **Run each scenario at three levels of prompt support.** *Supportive*: the prompt names the practice the
   block asks for. *Neutral*: the task alone, with no mention of it. *Competing*: the prompt pulls the other
   way (a deadline, "skip the tests this once"). The gap between supportive and neutral shows how much the block
   depends on being asked; the competing level is the pressure of step 2 made repeatable.
3. **Classify each recorded action against the sequence by its meaning and its result**, not by a keyword: a
   command that runs the suite and prints failures is the red step, one that prints passes is the green step.
   Check the order mechanically from the trace. The classifier is a different context from the one that wrote
   the block and from the one that was run.
4. **Report the rate per level and per step**, with the trace beside it. A step that is followed at the
   supportive level and dropped at the neutral one is not a step the block guarantees. A step with low
   compliance at every level is a candidate for mechanical enforcement (a hook, a check in `gate`), because
   a longer paragraph does not change what a block cannot make an agent do (`skills/writing-skills`, step 9).
5. **The same measurement applies to a rule or an agent definition**, not only to a workflow block: the
   expected sequence is derived from the document, and for an agent definition the first observable is whether
   it was invoked when the task called for it.
