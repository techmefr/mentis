# multi-agent-design-pitfalls §2 — Context, handoffs and consensus

## 2.1 Isolation as the purpose
1. **The context-engineering skill's central claim is that sub-agents exist mainly to isolate context,** so each
   works in a clean window free of the accumulated noise of other subtasks, and not to act out organisational
   roles. This is the skill's position and its supporting research was not read.
2. **It lists three ways to carry information into a sub-agent.** Full context delegation gives the whole
   planner context, which partly defeats isolation. Instruction passing sends only what the sub-agent needs and
   limits its flexibility. File-system memory uses persistent storage as the coordination medium, avoiding the
   weight of passing shared state through messages, at the cost of latency and consistency problems.
3. **Its default is instruction passing, escalating to files when state must be shared,** and full context only when
   the subtask genuinely needs it. Treat this as a starting point to test, not a rule (own guidance).
4. **A supervisor that paraphrases loses fidelity,** which the skill calls the telephone game. Its remedies are a
   tool through which a sub-agent's final answer goes straight to the user without the supervisor rewriting it,
   and files for state that several agents must read faithfully. The performance figure it gives for the effect
   is not carried over.
5. **A forwarding tool skips the supervisor's check on what it forwards** (own guidance). Use it only for answers
   whose format or content must be preserved, and verify them where they originate.

## 2.2 Handoff filters
1. **By default the target agent sees the global message history,** minus system messages, in Inspect. The
   messages the handoff generates are passed back through a filter that removes system messages and reasoning
   traces and turns tool calls into text, so the parent model is not confused by content it cannot place.
2. **Filters can be swapped.** Inspect has one that removes all tool calls from the history shown to the agent,
   and one on output that appends only the agent's last message to the global conversation; a custom function
   works for either side.
3. **In the Agents SDK the receiving agent sees the previous conversation unless an input filter changes it.**
   A per-handoff filter takes precedence over a run-level one. A run-level option compacts history into summary
   segments and is documented as a beta that is off by default.
4. **Filtering structure is not redacting content.** The documentation says nested history changes how the
   transcript is represented and does not redact sensitive data: tool-call arguments and outputs can remain in the
   generated summary. The helper that removes tool items does not redact arguments or results already copied into
   ordinary messages.
5. **Filter every field the summary is built from.** A custom filter that also calls the nesting helper must
   sanitise the history, the pre-handoff items and the new items first, because the helper builds from those three
   and ignores an existing override of the forwarded items. Clearing only the forwarded items afterwards leaves
   content in the summary.
6. **Server-managed conversations do not support these filters.** When the receiving agent must not inherit that
   history, use a separate run with explicitly selected input and do not reuse the original conversation or
   response identifier.
7. **Treat the receiving agent and its model provider as recipients of everything forwarded** (the documentation's
   wording). Decide what a specialist may see before choosing a handoff; see `agent-mcp-trust-pitfalls` for untrusted
   content in what agents exchange.

## 2.3 Consensus
1. **Simple majority voting treats a weak model's hallucination as equal to a strong model's reasoning,** per the
   skill, and discussions can settle on a false premise because of a bias toward agreement. These are its claims;
   the research behind them was not read.
2. **Its alternatives are weighted votes** (by confidence or expertise), **debate** in which agents critique each
   other over several rounds, and triggers that watch for a stall or for agents repeating each other without
   independent reasoning.
3. **Make disagreement explicit before convergence is allowed** (the skill's gotcha: assign adversarial roles and
   require each agent to state its disagreements first). Own guidance: agreement of agents sharing the same
   inputs and prompt is one reading repeated, not an independent confirmation; where correctness matters,
   verify against something outside the agents.

## 2.4 Error propagation and coordination cost
1. **One agent's wrong output becomes the next agent's fact,** and a downstream agent cannot tell a hallucination
   from information. The skill's mitigations: validate outputs before they pass on, retry with circuit breakers,
   prefer idempotent operations, and consider a checking agent for critical outputs.
2. **A supervisor that receives every worker's output becomes the bottleneck.** The skill suggests constraining
   worker outputs to a distilled schema and checkpointing supervisor state instead of carrying full history. It
   gives a cap on workers per supervisor; the figure is not carried over, so measure where yours saturates.
3. **Splitting too finely costs more than it saves.** The skill warns against over-decomposition and agent
   sprawl: decompose only where separate contexts bring a clear benefit, and start with the fewest agents.
4. **Agents without shared state duplicate work and drift.** The skill asks for a shared persistent store before
   a multi-agent workflow is built, and for objective boundaries, convergence checks and execution time limits to
   stop divergence; the limits are in `agent-run-limits-and-guardrail-pitfalls` §1.
5. **Test the failure scenarios on purpose** (the skill's last guideline). Own examples: kill a worker, make one
   return a wrong answer, make one return nothing, and see what the system reports.
