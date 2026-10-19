# agent-run-limits-and-guardrail-pitfalls §2 — Guardrail boundaries

## 2.1 Where each kind runs
1. **Input guardrails run only for the first agent in the chain.** The OpenAI Agents SDK documentation says they
   are meant for user input, so an agent's input guardrails run only when that agent is first.
2. **Output guardrails run only for the agent that produces the final output.**
3. **Tool guardrails run on every guarded function-tool call,** before and after execution, including local MCP
   tools when their server is configured with guardrails.
4. **A flow with handoffs or a manager therefore has gaps.** The specialist's input and any intermediate output
   are not seen by the agent-level checks; the documentation tells you to use tool guardrails for checks around
   each custom function-tool call in such flows.
5. **Some paths do not use the tool pipeline at all.** At the documented commit: handoffs run through their own
   pipeline, so tool guardrails do not apply to the handoff call; hosted tools and the built-in execution tools
   (computer, shell, patch application, local shell) do not use it; and converting an agent into a tool did not
   expose tool-guardrail options directly. List these in the design (own guidance), because the unguarded
   paths are often the powerful ones.

## 2.2 Timing: blocking and parallel
1. **A parallel input guardrail runs beside the agent,** which is the default. If its tripwire fires, the agent
   may already have consumed tokens and executed tools before it was cancelled.
2. **A blocking input guardrail finishes before the agent starts.** A tripwire then means the agent never runs, so
   no tokens are spent and no tools execute. Use blocking where tool calls have side effects (own guidance);
   the documentation presents it as the choice for cost and for avoiding side effects.
3. **Output guardrails always run after the agent completes** and have no parallel option. For a tool whose
   result becomes the final output, the tool has already run when the output check sees the value.
4. **A guardrail need not be an agent.** The documentation notes it can call an external classifier directly,
   which is cheaper and easier to make deterministic (own guidance on the second part).

## 2.3 Tripwires, exceptions and what is kept
1. **A tripwire raises an exception and halts the run.** The exception identifies the guardrail that fired; for
   the input and output kinds it also carries the results of every guardrail completed before the stop. Tool
   tripwire exceptions expose the triggering guardrail and its output.
2. **A tripwire and an exception inside the guardrail are different outcomes.** A tripwire rejects the candidate
   final output; the session keeps the tool calls and outputs already completed, without the rejected text. When
   the guardrail function itself raises, the verdict is unknown, and the completed final-turn items are
   persisted before the exception surfaces. If that session write also fails, the write error wins.
3. **Decide what an unknown verdict means** (own guidance). A guardrail that crashes is neither a pass nor a block;
   see `agent-hook-guard-pitfalls` §2 for the per-guard choice between open, closed and loud.
4. **A rejected terminal tool output is replaced in the stored state,** with a placeholder text; the original is
   not retained in the session, the run state, the streamed result state or the sandbox memory input.
5. **The call arguments are kept for replay and can contain the same data.** The documentation states that the
   retained function-call metadata includes the arguments, which may hold what also appeared in the rejected
   output. If the response contains something that cannot be sanitised safely, the SDK discards the whole
   current-response suffix.
6. **The placeholder is replayed, so keep it free of sensitive data.** Its text can be set globally; the
   formatter receives the guardrail name, the agent and the run context but never the rejected output. A
   formatter that raises, returns nothing or returns an awaitable falls back to the default text, and an async
   formatter is rejected when the run configuration is built.

## 2.4 Handoff arguments and approval ordering
1. **A flag that enables a handoff cannot authorise values in its arguments.** It is evaluated while the SDK
   prepares the available handoffs, before the model has produced any arguments.
2. **Authorise inside the handoff callback, before any side effect,** and raise on failure. The transfer
   continues once the callback returns successfully, so returning a refusal does not stop it. Tool input
   guardrails apply to function tools, not handoffs.
3. **The handoff input schema is validated locally** and passed to the callback, but it does not replace the next
   agent's input and does not choose a destination; the receiving agent still sees the history unless a filter or
   the history settings say otherwise. One handoff per destination is how a destination is chosen.
4. **Input checks on a tool that needs approval normally run after the approval,** just before execution. An
   option runs them before the approval pause is raised, and a call that passes is checked again after
   approval, so a time-sensitive check is revalidated. Without the option, a human may be asked to approve a call
   that a guardrail would have rejected (own inference from the order of steps).
