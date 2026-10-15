---
name: multi-agent-design-pitfalls
description: "Use when a design splits work across several model agents and the open questions are whether it should, in which shape and what crosses the boundary: beating a single-agent baseline first, orchestrating by model or by code, agent-as-tool against handoff, what a handoff forwards and what its filters do not redact, discarded state when an agent is run from code, context isolation and the paraphrase loss of a supervisor, consensus that rewards agreement, error propagation, and the four ways a delegated agent fails quietly (fabricated dispatch, silent stall, scope drift, an unverified completion claim)."
---

# multi-agent-design-pitfalls

A block for the design of a system of several agents, as opposed to the mechanics of launching a few of them.
The three sections share one premise: **adding agents adds boundaries, and every boundary is a place where
context is lost, authority is blurred or a failure is reported as success**. The mechanics of a fan-out
(disjoint scopes, isolated worktrees, one-message launch, aggregation, resuming an agent, the concurrency and depth
ceilings, the check that a report's claimed changes exist) are in `dispatch-parallel` and are not repeated; this
block adds what that one does not. Budgets and checkpoints inside a loop are in `agent-run-limits-and-guardrail-pitfalls`;
guard scripts for the failure modes in §3 are in `agent-hook-guard-pitfalls`; measuring whether the design wins is in
`llm-eval-regression-pitfalls`.

## When
- Deciding whether a task needs more than one agent, and which pattern to use.
- Writing the handoff, the tool conversion or the sub-agent call that carries context between agents.
- Designing how several agents agree on an answer.
- A delegated agent reported success and the result is missing, stale, too large or unverified.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Whether and which shape: baseline first, model or code orchestration, agent-as-tool against handoff, name collisions, running an agent from code | a design is being chosen | [`01-whether-and-which-shape.md`](./references/01-whether-and-which-shape.md) |
| 2 | Context, handoffs and consensus: isolation, paraphrase loss, handoff filters and redaction, voting, error propagation, coordination cost | something crosses an agent boundary | [`02-context-handoffs-and-consensus.md`](./references/02-context-handoffs-and-consensus.md) |
| 3 | Delegated-agent failure modes: silent stall, scope drift, unverified completion, the dispatch case in brief, where evidence lives | a delegated agent's report is trusted | [`03-delegated-agent-failure-modes.md`](./references/03-delegated-agent-failure-modes.md) |

## Output / checkpoint
There is a single-agent baseline and the multi-agent design was measured against it on the same cases (§1).
Each boundary has a written line for what crosses it, what is filtered and what is not redacted (§2). Each
delegated agent has a named artifact it must produce and a check that reads the tool-level record, not its own
summary (§3). A design that was never compared with the single-agent version is not verified.

## Guardrails
- Never start from a multi-agent design; start from one agent and justify each addition by a measured gain (§1).
- Never discard the state an agent run returns when the caller needs its output (§1).
- Never treat a history filter as redaction (§2).
- Never score agreement as evidence; agreement among agents is not verification (§2).
- Never accept a sub-agent's statement that it is done as the evidence that it is done (§3).
- Restates the documentation of two agent projects and the claims of a context-engineering skill collection and
  a hook project, as of the commits in [`references/origin.md`](./references/origin.md). Claims of those two
  collections that cite figures or research were not verified and no figure is carried over. No design was
  built or run while writing this.

## Origin
Rewritten from the UK AI Security Institute Inspect documentation on multi-agent designs (MIT), the OpenAI Agents
SDK documentation on orchestration and handoffs (MIT), the multi-agent skill of a context-engineering collection
(MIT, figures dropped) and the sub-agent failure-mode map of a hook project (MIT, promotional, taxonomy only),
read 2026-10-16. 🟡: never run by us; open points are in [`references/origin.md`](./references/origin.md).
