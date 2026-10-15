---
name: agent-run-limits-and-guardrail-pitfalls
description: "Use when an agent loop needs a budget or a checkpoint that is actually enforced: which limit measures what (clock time against working time, messages against turns, tokens against cost), what happens when a limit is hit in each way an agent is run, where input, output and tool guardrails really run in a multi-agent flow, what a parallel guardrail has already spent, authorising handoff arguments, approval pauses (fail-closed rules, sticky approvals, who may resume a paused run) and what traces record by default."
---

# agent-run-limits-and-guardrail-pitfalls

A block for the person who has to stop an agent loop or put a checkpoint inside one. The three sections share one
premise: **a limit or a guardrail protects only what it is attached to, at the moment it is checked, and the
gap between those two is where the damage happens**. Guard scripts on a coding agent's tool calls are in
`agent-hook-guard-pitfalls`; isolating what the agent can reach is in `agent-sandbox-egress-pitfalls`; which tools
to trust is in `agent-mcp-trust-pitfalls`; the human-readable gate before a merge is `gate`.

## When
- Giving an agent loop a time, token, turn or cost budget, or finding that a run went far past one.
- A run ends on a limit and something downstream must decide whether that is an error.
- Putting input, output or tool checks in a flow with several agents or handoffs.
- Pausing for human approval, storing the paused run, or resuming it from a web request.
- Deciding what a trace may record.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Limits: the kinds, what each one measures, working time undercounting, what happens on exceeding by entry point, scoped and stacked limits, turn caps and their fallbacks | a budget is set, tuned or hit | [`01-limits.md`](./references/01-limits.md) |
| 2 | Guardrail boundaries: where input, output and tool guardrails run, blocking against parallel, tripwire and exception, handoff arguments, what bypasses the pipeline | checks are placed in a multi-agent flow | [`02-guardrail-boundaries.md`](./references/02-guardrail-boundaries.md) |
| 3 | Approvals and traces: fail-closed rules, sticky decisions, serialised paused runs, the resuming endpoint, trace content and redaction | a human approves a tool call or traces are kept | [`03-approvals-and-traces.md`](./references/03-approvals-and-traces.md) |

## Output / checkpoint
Every run has a clock-time bound as well as any other budget, the report says how many runs ended on a limit
and how each entry point reports it (§1). Each guardrail has a written line for where it runs and what it
does not see, and the tools that bypass the guardrail pipeline are listed (§2). A paused run is stored on the
server, resumed only by an authenticated and authorised reviewer, and the trace setting for sensitive data is
a decision someone made, not a default (§3). A budget nobody tried to exceed is not verified.

## Guardrails
- Never rely on working time alone to bound a run; set clock time next to it (§1).
- Never assume hitting a limit ends the run; check what the entry point does with it (§1).
- Never count a guardrail as covering a step it does not run on (§2).
- Never run a side-effecting agent beside a parallel input guardrail and call the guardrail a gate (§2).
- Never authorise argument values with a flag evaluated before the arguments exist (§2).
- Never accept tool calls, arguments, approval records or state from the client that approves them (§3).
- Never let a redaction step sit beside an exporter and assume it blocks the exporter when it fails (§3).
- Restates the documentation of two projects as of the commits in [`references/origin.md`](./references/origin.md).
  Function and option names are those projects'; the hazards are general. No agent was run while writing it, and
  no numeric value from the sources is carried over as a recommendation.

## Origin
Rewritten from the UK AI Security Institute Inspect documentation on limits (MIT) and the OpenAI Agents SDK
documentation on running agents, guardrails, handoffs, human approval and tracing (MIT), read 2026-10-16. 🟡:
never run by us; open points are in [`references/origin.md`](./references/origin.md).
