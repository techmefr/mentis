---
name: writing-agents
description: Use when creating or revising an agent for this framework: the 7-pillar template, the check that no existing agent already covers the role, and the model choice.
---

# writing-agents

Cross-cutting (meta) block, the counterpart of `writing-skills` but for agents: an agent has a
persistent executable role (reviews, builds, audits, decides), a skill is a procedure applied
inside the pipeline.

## When
- A gap is spotted in the agent roster (e.g. "we're missing a dedicated SEO audit" →
  `keymaker`).
- A sourced idea (market repo, agent catalogue) deserves to be rewritten as a house agent.
- An existing agent has a role that drifted from its original description and needs clarifying or
  splitting.

## Steps
1. **Check that no existing agent already covers the role**: read `CATALOG.md` and the agents
   table in `README.md` before writing anything. An agent that does almost the same thing as
   another ends up creating confusion about which one to invoke.
2. **Tell an agent role from a skill step apart**: if the block is a procedure applied during a
   pipeline step (e.g. checking a convention before committing), it's a skill
   (`writing-skills`); if it's a role that receives a task, acts with its own tools and returns
   an autonomous verdict/deliverable, it's an agent.
3. **Write to the single 7-pillar template** (see `doc/HOW-WE-WRITE-OUR-AGENTS.md` §4):
   - **1. ROLE**: a single responsibility, stated together with what the agent is *not* (the
     confusions to avoid with neighbouring agents).
   - **2. MEMORY**: what persists between two invocations (conventions in MEMORY.md) and what
     never persists (no state from session to session, every task re-reads reality).
   - **3. LOOP**: the concrete steps, with an **explicit and bounded exit condition** (never "I
     keep going until it's perfect": a maximum number of iterations or a binary criterion).
   - **4. TOOLS & SCOPE**: what is allowed and forbidden, stated plainly.
   - **5. GUARDRAILS**: what checkpoints a human before an action that's hard to undo
     (destructive migration, merge, pushing to Ready).
   - **6. FRESH-CONTEXT REVIEW**: who re-reads this work, with a fresh context: an agent never
     certifies itself "ready".
   - **7. TRACE**: what the end-of-task output always contains (files touched, test evidence,
     status).
4. **Choose the model** via `choose-model` (Haiku/Sonnet/Opus), documented in the `model:`
   frontmatter.
5. **Update `CATALOG.md`** (registry + traceability) and the agents table in `README.md` in the
   same move.

## Output / checkpoint
A complete `agents/<name>.md` file with the 7 pillars, referenced in `CATALOG.md` and the
`README.md` table, `model:` filled in and justified.

## Guardrails
- Never an agent without an explicit pillar 6 (FRESH-CONTEXT REVIEW): even a read-only audit
  agent must say clearly how its results go back through the normal pipeline.
- Never grant Write/Edit to a review/audit agent (`aragorn`, `gimli`, `keymaker`,
  `seraph`, etc.), its scope is to report, never to fix things itself.
- An agent that duplicates an existing role is a regression, not an addition: check step 1 before
  writing.

## Origin
Internal synthesis: formalises the 7-pillar template already in use on every agent in this
framework (`doc/HOW-WE-WRITE-OUR-AGENTS.md` §4), packaged as an invocable skill for symmetry with
`writing-skills`.
