---
name: writing-agents
description: "Use when creating or revising an agent for this framework: the 7-pillar template, the check that no existing agent already covers the role, and the model choice."
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
   - **4. TOOLS & SCOPE**: what is allowed and forbidden, stated plainly — and **say which half
     the frontmatter enforces**. Every prohibition that names a tool goes in `disallowedTools`;
     what stays prose is only what the field cannot express, which in practice is the path-scoped
     half ("writes, but only inside the scratch directory").
   - **5. GUARDRAILS**: what checkpoints a human before an action that's hard to undo
     (destructive migration, merge, pushing to Ready).
   - **6. FRESH-CONTEXT REVIEW**: who re-reads this work, with a fresh context: an agent never
     certifies itself "ready".
   - **7. TRACE**: what the end-of-task output always contains (files touched, test evidence,
     status).
4. **Choose the model and the effort level** via `choose-model`, documented in the `model:` and
   (where the verdict is hard to walk back) `effort:` frontmatter.
5. **Fill in the rest of the frontmatter the contract implies.** The seven pillars are prose; four
   of them have a mechanical counterpart, and writing only the prose half is how a guarantee ends
   up unenforced — pillar 4 is `disallowedTools`/`tools`, pillar 3's bounded exit is `maxTurns`,
   pillar 2 is `memory:` (declared only if something genuinely persists — the default here is
   amnesia, and for a reader or the gate it has to stay that way), and an agent that writes code
   without touching the operator's tree is `isolation: worktree`. The field list is in
   `references/claude-code-platform.md` §3.
6. **Update `CATALOG.md`** (registry + traceability) and the agents table in `README.md` in the
   same move.

## Output / checkpoint
A complete `agents/<name>.md` file with the 7 pillars, referenced in `CATALOG.md` and the
`README.md` table, `model:` filled in and justified, and every tool-shaped prohibition from pillar
4 present in the frontmatter.

## Guardrails
- Never an agent without an explicit pillar 6 (FRESH-CONTEXT REVIEW): even a read-only audit
  agent must say clearly how its results go back through the normal pipeline.
- Never grant Write/Edit to a review/audit agent (`aragorn`, `gimli`, `keymaker`,
  `seraph`, etc.), its scope is to report, never to fix things itself — and **"never grant" means
  the frontmatter, not a sentence in pillar 5.** A guarantee the runtime doesn't hold is the exact
  failure this repo's default-FAIL rule exists to refuse; applying it to our own agents is not
  optional.
- An agent that duplicates an existing role is a regression, not an addition: check step 1 before
  writing.

## Origin
Internal synthesis: formalises the 7-pillar template already in use on every agent in this
framework (`doc/HOW-WE-WRITE-OUR-AGENTS.md` §4), packaged as an invocable skill for symmetry with
`writing-skills`.

Step 5 and the pillar-4 amendment added 2026-09-07. The trigger was not an idea: all 25 agents
carried `name`/`description`/`model` and nothing else, while twelve of them stated *"Never
Write/Edit"* in prose and inherited every tool at runtime. The frontmatter fields that close that
gap are stamped in `references/claude-code-platform.md` §3.
