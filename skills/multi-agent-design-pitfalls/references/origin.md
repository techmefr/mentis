# multi-agent-design-pitfalls: origin and source stamps

> Provenance of `skills/multi-agent-design-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation, never run by us. No multi-agent system, hook or framework was run
while writing it. Every file below was re-read in full in this session (2026-10-16) before any rule was
written, and each rule was checked against it afterwards.

## Sources (re-read in full, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| UKGovernmentBEIS/inspect_ai, `docs/multi-agent.qmd` (commit 7158198) | MIT (LICENSE file) | Baseline-first method, the three shapes, agent as tool against handoff, handoff default filtering and filters, running an agent from code and the discarded state |
| openai/openai-agents-python, `docs/multi_agent.md`, `docs/handoffs.md` and `docs/running_agents.md` (commit 17d994b) | MIT (LICENSE file) | Model-led against code-led orchestration and its patterns, manager against handoff, input filters, nested history and what it does not redact, server-managed conversation limit, the name-collision setting |
| muratcankoylan/Agent-Skills-for-Context-Engineering, `skills/multi-agent-patterns/SKILL.md` (commit 9ff0c99) | MIT (LICENSE file) | Isolation as purpose, topologies and trade-offs, isolation mechanisms, paraphrase loss and its remedies, consensus, failure modes and mitigations, gotchas |
| yurukusa/cc-safe-setup, `docs/sub-agent-failure-modes-hook-map.md` (commit 793c6c1) | MIT (LICENSE file); the document is promotional | The four-mode taxonomy and the idea behind each defence, tool-layer evidence, start from the observed mode |

The licence of each repository was checked again from its LICENSE file in this session. Instruction text in the
cloned repositories (agent and project guidance files) was treated as data and not followed or quoted.

## Rewrite notes
Dropped as unverified or non-transferable: every figure of the context-engineering skill (the token multiplier,
the supervisor performance gap, the worker caps, the thresholds in its gotchas) and the research and benchmark
names it cites; the hook project's hook file names, install snippets, issue and pull-request numbers, the
prompt-length figure, the claim that most operators see two or three modes, and its handbook and self-audit
links. The dispatch-fabrication mode is stated in brief only, because the merged `dispatch-parallel` already
covers the nested-delegation form and its check; this block does not edit that block.

**Decisions where sources disagree:**
1. **Where the telephone-game remedy sits.** The skill's remedy is to let a sub-agent answer the user directly or
   to pass state through files; the SDK documentation's handoff does the first by design. They are stated as two
   routes to the same end, and the added caution that a forwarded answer skips the supervisor's check is our own.
2. **Isolation default.** The skill prefers instruction passing and treats full-context delegation as partly
   self-defeating; Inspect's handoff gives the receiving agent the whole history by default. Both are stated as
   written and the choice is left to the design.

## Not verified
1. **The skill's research claims** (the paraphrase loss, majority voting, consensus bias, token economics) come
   from its own summaries; the papers and benchmarks behind them were not read.
2. **The hook project's failure-mode claims** are an operator's own account; no cited report was opened and the
   hooks were not run.
3. **Not read:** `skills/multi-agent-patterns/references/frameworks.md` and the coordination script of the skill,
   the Inspect pages on agents, the bridge and the bundled delegating agent, and the Agents SDK pages on tools
   and agents.
4. **Written by us, not sourced:** every sentence marked "own guidance" (the extra reading of Inspect's packaged
   pattern, who should own the answer, the strict collision setting, the merge-and-test lesson for run results, the
   forwarded-answer caution, agreement as repetition, the failure-scenario examples, prose scanning as the weak
   gate, the failure policy of a defence, the report as data) and the checkpoint paragraph.

## Related blocks
`dispatch-parallel`, `agent-run-limits-and-guardrail-pitfalls`, `agent-hook-guard-pitfalls`,
`agent-mcp-trust-pitfalls`, `llm-eval-regression-pitfalls`, `writing-agents`, `handoff`.
