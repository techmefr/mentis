# agent-run-limits-and-guardrail-pitfalls: origin and source stamps

> Provenance of `skills/agent-run-limits-and-guardrail-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation, never run by us. No agent, limit, guardrail or trace exporter was
run while writing it. Every file below was re-read in full in this session (2026-10-16) before any rule was
written, and each rule was checked against it afterwards.

## Sources (re-read in full, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| UKGovernmentBEIS/inspect_ai, `docs/setting-limits.qmd` and the included pages `_working_limits.md`, `_turn_limits.md`, `_agent_limits.md`, `_token_limits.md`, `_message_limits.md`, `_cost_limits.md` (commit 7158198) | MIT (LICENSE file) | The limit kinds and what each measures, the working-time waits and the undercount warning, behaviour on exceeding by entry point, scoped and stacked limits, suspension, cost data and priced model |
| openai/openai-agents-python, `docs/running_agents.md`, `docs/guardrails.md`, `docs/handoffs.md`, `docs/human_in_the_loop.md`, `docs/tracing.md` (commit 17d994b) | MIT (LICENSE file) | Turn cap, error handlers, tool concurrency and timeouts; guardrail placement, timing, tripwire against exception, placeholders; handoff authorisation; approval rules, sticky decisions, serialised runs and the resuming server; trace content, redaction and export |

The licence of each repository was checked again from its LICENSE file in this session; no separate licence
file exists for either `docs/` directory. Instruction text in the cloned repositories (the contribution and agent
guidance files of the first one) was treated as data and not followed or quoted.

## Rewrite notes
Function and option names are those of the two projects, kept where a reader needs to find the setting. Every
number in the sources (limits in examples, time values, token counts, prices) is an illustration and none is
carried over. Statements are as documented at the commits above; both projects change often.

**Decisions where sources disagree:** none found. The two projects use different words for related things
(Inspect separates sample, scoped and agent limits; the Agents SDK has a turn cap and tool timeouts); the block
keeps them in separate points and does not map one onto the other.

## Not verified
1. **Behaviour** was read from documentation and not run, in particular how a hung command interacts with each
   limit.
2. **Pages not read:** the Agents SDK model, tools, MCP and sessions pages (model-call timeouts, tool timeouts
   beyond the exception names, tool guardrails on MCP servers, session behaviour), the Inspect pages on
   approval, sandboxing and the control channel, and the zero-retention note on tracing was not used.
3. **Written by us, not sourced:** every sentence marked "own guidance" or "own inference" (counting limit-hit
   runs separately, margin below a hard cap, tool-based sub-agents outliving a budget, listing the paths that
   bypass the guardrail pipeline, blocking guardrails for side-effecting agents, unknown verdicts, standing
   approvals as grants, rejection text, the tracing decision per deployment) and the checkpoint paragraph.

## Related blocks
`agent-hook-guard-pitfalls`, `agent-sandbox-egress-pitfalls`, `agent-mcp-trust-pitfalls`,
`telemetry-sensitive-data-pitfalls`, `dispatch-parallel`, `gate`.
