# mcp-server-design-pitfalls §2 — Results and errors

## 2.1 Structured content next to text
1. **A tool that returns structured content should also return its serialised JSON as text.** The protocol
   says so for backwards compatibility. FastMCP always produces text content blocks and adds structured
   content for object-like results or when an output schema exists.
2. **The two must agree** (own guidance): a text that says one thing and a structure that says another makes a
   model and a program act on different facts; build the text from the structure.
3. **Output schemas declared by FastMCP must be object types,** and a primitive result is wrapped under a
   `result` key.
4. **Keep large outputs bounded.** The tool-design skill suggests offering a concise and a detailed response
   format and documenting when to use each. Own guidance: when a list is truncated, say so in the result.
5. **Stateful tools return an explicit handle.** The protocol has no session; its non-normative guidance says
   a handle is a name, not a capability, so the server validates the caller's authorisation on every call
   (an unauthenticated server needs a high-entropy handle with a bounded lifetime), handles should be opaque,
   the retention policy should be stated in the creation tool's description, and an expired or unknown handle
   should return a tool execution error saying so.

## 2.2 Two kinds of error
1. **Protocol errors are for a request the model is unlikely to fix:** an unknown tool, a malformed request,
   a server error. They are returned as JSON-RPC errors.
2. **Tool execution errors carry feedback the model can act on** and are returned in a result with
   `isError: true`: API failures, input validation errors such as a date in the wrong format, business rule
   violations. Clients should pass these to the model so it can retry with adjusted parameters.
3. **Write the error text for the model.** The tool-design skill: say what went wrong and how to correct it,
   include the invalid value, the expected format and a retry hint where it applies.
4. **Do not leak internals.** FastMCP can mask the details of unexpected exceptions with
   `mask_error_details`, while messages raised as its `ToolError` are always sent; its own validation
   warnings leave out argument values because they may contain private client data. Own guidance: never put
   secrets, stack traces or internal addresses in an error.
5. **A failure is never only prose in a success result** (own guidance): a caller that checks the error flag
   would miss it.

## 2.3 Ordering
1. **Return lists in a deterministic order.** The protocol says tools should be listed in the same order across
   requests when the set has not changed, which lets clients cache and improves model prompt-cache hits.
2. **The same applies to your own result lists** (own guidance): sort by a stated key.
3. **Do not leak existence** (own guidance): a different error for "no such item" and "not allowed" tells a
   caller which items exist.

## 2.4 Timeouts and side effects
1. **FastMCP tools opt in to a timeout; there is no server-level default.** The protocol's security section
   says clients should implement timeouts for tool calls.
2. **A timeout does not undo side effects.** FastMCP says async tools are cancelled at their next cancellation
   checkpoint, a synchronous worker cannot be interrupted (the server waits for it before returning the timeout
   error), and the timeout does not undo effects or stop a sync tool that never returns. It also does not
   apply to background tasks.
3. **So a write that timed out may have succeeded.** Own guidance: make a mutating tool safe to repeat with an
   idempotency key or a check of current state (the same idea in one stack is in `laravel-idempotent-jobs`),
   and say in the error that the outcome is unknown.
