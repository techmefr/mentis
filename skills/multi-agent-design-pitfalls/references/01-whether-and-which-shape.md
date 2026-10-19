# multi-agent-design-pitfalls §1 — Whether and which shape

## 1.1 Whether
1. **Multi-agent designs often do not beat a simple single agent.** The Inspect documentation says so directly
   and recommends a method: start with a baseline tool-using agent so improvements can be measured, optimise the
   environment, the tool selection and the prompts, and only then try multi-agent designs, benchmarked against
   that work.
2. **The same documentation points at its bundled delegating agent first** when subagent delegation, persistent
   memory and planning are what is wanted; that is specific to that framework, and the general reading is to look
   for an existing packaged pattern before wiring your own.
3. **Cost and coordination can cancel the benefit.** The context-engineering skill says multi-agent runs use far
   more tokens than a single agent and that coordination can negate parallelism, and asks you to measure whether
   the design really saves time against one agent with a longer context. The multiplier it quotes is a claim with
   a figure and is not carried over; measure your own.
4. **That skill also claims model quality often matters more than raw token budget,** so changing the model
   belongs next to the topology in the experiment list. This is the skill's claim and was not verified.
5. **Sub-tasks that share mutable state are not a fan-out.** That case, with the scope and isolation rules, is in
   `dispatch-parallel`.

## 1.2 Who decides the flow
1. **There are two ways to orchestrate,** per the OpenAI Agents SDK documentation: let the model plan and route, or
   decide the flow in code. They can be mixed.
2. **Code gives more predictable speed, cost and results.** The documented patterns are: classify with a
   structured output and pick the next agent from the class, chain agents so one's output is the next's input,
   loop a task agent against an evaluator agent until the evaluator accepts, and run independent agents in
   parallel.
3. **The model route suits open-ended tasks** and the documentation's advice for it is to invest in prompts that
   state tools and constraints, monitor and iterate, let the agent critique itself, prefer specialists over one
   generalist, and invest in evals.
4. **Inspect lists three shapes:** a supervisor that hands off to sub-agents, a workflow that invokes agents in
   explicit stages, and agents offered as ordinary tools. It notes that explicit staging is sometimes
   preferable, as in many deep-research agents built with separate planning, search and writing steps.
5. **The context-engineering skill names three topologies** (supervisor, peer-to-peer and hierarchical) and tells
   you to choose by coordination needs, not by an organisational metaphor. Its trade-offs, as claimed there: a
   supervisor gives strict control and a human checkpoint but becomes a bottleneck and a single failure point; peers
   have no central failure point but diverge without a state keeper; layers separate concerns but add
   coordination and misalignment between layers.

## 1.3 Agent as tool, or handoff
1. **An agent used as a tool keeps the caller in control.** In the Agents SDK the manager owns the final answer,
   combines specialist outputs and keeps shared guardrails in one place. In Inspect the tool agent sees one input
   string and returns the output of its last assistant message.
2. **A handoff transfers the conversation.** In the Agents SDK the specialist becomes the active agent for the rest
   of the turn and responds directly. In Inspect the handed-off agent can see the conversation history and append
   messages to it.
3. **Pick by who should own the answer,** not by habit (own guidance restating the two descriptions). Use the
   tool form for a bounded subtask and the handoff where routing is the workflow and the specialist should
   speak for itself. The two combine: a specialist reached by handoff can use other agents as tools.
4. **A handoff is a tool to the model,** named with a transfer prefix and the agent's name. Give each agent a
   name and a description the model can choose by; Inspect requires them for an agent used in a handoff.
5. **Names can collide.** In the Agents SDK, when an unnamespaced function tool and a handoff share a name, the
   default only logs a warning and exposes the one that wins dispatch; a stricter setting raises an error before
   the model is called. Use the strict setting in a design with many tools (own guidance).
6. **One handoff per destination.** The SDK's helper always transfers to the agent it wraps, so several possible
   destinations are several handoffs and the model chooses among them.

## 1.4 Running an agent from code
1. **Inspect's `run` copies its input and returns a new state.** It never writes the agent's conversation back into
   what you passed in, which also makes parallel runs safe from conflicting edits to a shared state.
2. **A caller that discards the returned state loses the agent's work.** Called from a solver, the conversation
   and output do not reach the sample's messages, so scorers reading them see nothing, although they remain in the
   transcript. Copy the fields you need back, or convert the agent into a solver, which updates the state
   automatically.
3. **The general lesson** (own guidance): when an orchestrator calls an agent in code, decide explicitly which parts
   of its result are merged into the caller's state, and test that the caller's downstream readers see them.
