# testing-blocks §6 — Test the routing text on its own

> Section 6 of `skills/testing-blocks`. Read it when a block's description is written or changed, or a block loads on the wrong tasks. The other sections and the guardrails stay in `SKILL.md`.

1. **Read the description alone.** A block's description exists to make the right block load at the right
   time. Give an agent only the description and the task: it should pick the block, and it must **not** be
   able to carry out the block's steps from the description alone. A description that summarises the
   process invites the agent to follow the summary and skip the body.
2. **Check both failure directions**: a scenario the block should trigger on and a near-miss it should not.
   A block that loads on everything costs context on every task; one that never loads is untested content.
