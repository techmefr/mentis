# agent-run-limits-and-guardrail-pitfalls §1 — Limits

## 1.1 Why and which
1. **An open-ended loop can get stuck or hang.** Inspect's documentation names two cases: a model attempting a
   task with no realistic prospect of completing it, and a command in a sandbox that takes extremely long or
   never returns. It advises limits on some combination of total time, messages, turns, tokens and cost.
2. **Sample-level limits end the run early; they do not raise an error.** In Inspect a sample that hits one is
   still scored, and nearly always as incorrect.
3. **Count limit-hit runs separately in any report** (own guidance). A run cut by a budget looks like an agent
   that failed the task, and the two have different fixes.
4. **The values in the documentation's examples are illustrations,** and it says so. Choose yours from the task.

## 1.2 Clock time and working time
1. **A clock-time limit counts all elapsed time.** Also give each command a timeout of its own, so one wayward
   command does not use the whole run's budget; the documentation sets a per-command timeout inside the run
   limit for this.
2. **A working-time limit counts only time spent working.** Waiting is excluded: waiting for a model connection or
   a concurrency slot, a model request that fails and is retried with its backoff, a batch request waiting to be
   submitted, tool approval or review by a person or a model, waiting for a person to answer, a paused model
   call, and any block explicitly marked as waiting.
3. **Work done while any wait is in progress is not charged.** Inspect warns that while one part of a sample
   waits, other work in the same sample is free: concurrent tasks, parallel tool calls, sub-agents, background
   processes in a sandbox and the work of in-process agent libraries. Working time can undercount and a sample
   can run much longer than its limit.
4. **Always set a clock-time limit next to a working-time limit.** The documentation says so in as many words;
   the clock limit is the backstop.
5. **Some providers report no request time,** or measure the whole call; Inspect then counts retries inside the
   client as working time for those providers.
6. **A scoped clock limit cancels at the first yield point,** such as an await. A scoped working limit is not
   driven by cancellation; Inspect checks it periodically, for instance from a model call and after each
   solver step. A long block that does neither runs past it.

## 1.3 Messages, turns, tokens and cost
1. **A message limit counts every message in the conversation,** not only the new ones an agent added.
   Inspect checks it whenever a model is called, raising when the count equals or exceeds the limit, and when the
   message list is modified, raising there only when the count exceeds it.
2. **A turn is one model generation.** One turn often produces several messages, such as an assistant message and
   the tool messages from its calls, so turn and message limits are different instruments. Generations made to
   compact the conversation do not count as turns.
3. **A token limit covers everything used while it is active,** not one call. To bound a single call, use the
   generation option for maximum tokens. By default all tokens are metered; an output-only variant meters just
   what the model generates, reasoning tokens included, so growth of the input does not eat into it.
4. **A cost limit needs cost data.** Inspect raises an error when a cost limit is set and a model in the run has
   no price configured. A request is priced at the model that served it when the provider reports a different
   one, for example after a fallback or through a router; if that served model has no data, the requested
   model's rates are used with a warning that names the served model.
5. **Token and cost limits are checked when a model is called,** and a turn limit when a turn is recorded.
   A single call can therefore carry a run past a budget (own inference from those rules); leave margin below any
   hard external cap (own guidance).

## 1.4 What happens when a limit is hit
1. **It depends on how the agent was run.** Inspect documents three cases. An agent run as a solver ends the
   sample. An agent run directly with limits has the limit exception caught and returned alongside its state;
   limits that were not passed to it propagate up. An agent used through a handoff or as a tool gets a message
   to that effect returned to the model, and **the sample continues running**.
2. **A tool-based sub-agent can therefore outlive its budget** (own guidance). Treat a limit message as input the
   parent may ignore, and give the parent its own budget as well.
3. **Pass limits where the agent is attached,** to the handoff, the tool conversion, the solver conversion or the
   direct run; the documentation shows each.
4. **Querying usage covers the sample limits only.** Scoped and agent limits are not reported by that call, and a
   limit passed to an agent has to be kept as a reference to read its usage.

## 1.5 Scoped and stacked limits
1. **Wrap the whole use of a scoped limit in the handler.** Some exceptions are raised when the context
   manager closes, so a handler placed inside the block misses them.
2. **A helper that catches limit errors catches only those from the limits passed to it.** Errors from other
   limits, such as the sample's, still propagate, which is what you want.
3. **Token, turn and cost limits stack;** usage counts toward every open limit. A message limit is different:
   only the innermost active one is checked.
4. **Removing a limit is not the same as suspending it.** Setting a scoped token limit to none suppresses only the
   innermost limit's check. The suspend helper disables both recording and checking across all active token
   limits for the block, and a suspended working limit makes the whole sample count as waiting, including work by
   other tasks in it. Use either for a specific step and name why (own guidance).
5. **A custom limit is an exception of the same type with a custom name,** which the sample machinery catches
   like the built-in ones.

## 1.6 Turn caps in another framework
1. **The OpenAI Agents SDK loop** calls the model, then either finishes, hands off or runs tool calls and loops
   again. Exceeding the maximum number of turns raises a dedicated exception, and passing none for the maximum
   removes the limit. An unattended run should not remove it (own guidance).
2. **Handle the exception or register a handler for it.** The error-handler hook returns a controlled final output
   instead of ending with an error; the same hook exists for model refusals and for outputs that fail the
   structured type.
3. **A fallback output is added to history and to the session by default.** The handler result has an option to
   leave it out; set it when the fallback is a message for the caller and not something the agent said (own
   guidance: otherwise the next turn reads it as the agent's own words).
4. **Model calls and tool calls have their own timeouts,** with dedicated exception types; a tool timeout raises
   only when the tool is configured for that behaviour.
5. **Local tool calls are all started by default.** When a model emits several in one turn, the SDK starts them
   all unless a concurrency cap is set. The model setting that allows several calls in one response is separate
   from this cap, which governs how the SDK runs them afterwards.
