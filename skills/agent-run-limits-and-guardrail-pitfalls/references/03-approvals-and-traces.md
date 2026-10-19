# agent-run-limits-and-guardrail-pitfalls §3 — Approvals and traces

## 3.1 Approval rules and sticky decisions
1. **A tool can require approval always or by a per-call function.** The function receives the run context, the
   parsed parameters and the call identifier.
2. **A per-call approval rule fails closed on arguments it cannot safely inspect.** In the OpenAI Agents SDK, when
   the arguments are missing, empty, whitespace, malformed JSON, valid JSON that is not an object, or contain
   non-standard constants such as NaN or Infinity, the function is not invoked and the call needs manual
   approval. The same holds for realtime tool calls.
3. **Approval for the local shell and patch-application tools is opt-in.** It defaults to off, and a callback
   that decides approvals does not switch it on; the callback runs only for calls that require approval and
   have no decision yet.
4. **Per-call approvals are scoped to the call identifier.** An always-approve or always-reject decision is a
   standing decision for later calls to the same tool identity for the rest of the run, and it is stored in the
   run state, so it survives serialisation and a later resume.
5. **A hosted MCP tool's identity is the server label plus the tool name,** and a standing decision is stored only
   when both are non-empty. A standing approval for a tool name on one server does not cover the same name on
   another.
6. **Treat a standing approval as a permission grant** (own guidance): reserve it for narrow, read-only tools and
   do not carry it into a run that has other tools attached.
7. **The approval surface is run-wide.** It covers tools of the current agent, of an agent reached by handoff and
   of a nested agent used as a tool; the interruption surfaces on the outer run, and that run is the one to
   resume.
8. **A rejection returns text to the model.** A run-wide formatter sets the default and a per-call message takes
   precedence. Keep the text free of data you would not show the model elsewhere (own guidance).

## 3.2 Paused runs and the resuming endpoint
1. **Loading a serialised run state does not authenticate it.** The documentation says the loaders authenticate
   neither the snapshot nor the person submitting it; only load snapshots from trusted storage, or ones whose
   integrity and ownership the application has verified. A schema check or a tool-call fingerprint does not
   authenticate a snapshot.
2. **Keep the whole snapshot on the server.** Send the reviewer only the tool details they are allowed to see and
   opaque identifiers for the pending decisions. Tool names and arguments are untrusted display content: escape
   them when rendering HTML.
3. **When a decision arrives, the server must do four things.** Authenticate the reviewer from its own session and
   not from the request body. Authorise that reviewer for the stored run and the chosen calls; holding a run or
   decision identifier is not authorisation. Check the submitted identifiers and booleans against the pending
   requests it stored, taking the items from the server-owned snapshot and accepting no replacement tool calls,
   arguments, approval records or serialised state from the client. Apply the approve or reject to those
   items, then resume.
4. **Make the consumption of a pending request atomic.** Concurrent or replayed submissions must not resume the
   same snapshot twice; in shared storage the documentation calls for an atomic, owner-checked transition before
   the resumed execution starts.
5. **Neutralising parts of a snapshot does not make it safe.** Replacing the context, requiring a mapping
   context, or deleting only the approval records still leaves other fields controlling the resumed run. If
   the whole snapshot travels through a client, verify its integrity, bind it to the authorised user and run, and
   prevent replay before loading it. That verification does not encrypt or hide the contents.
6. **A serialised run holds more than the conversation:** the application context, approvals, usage, tool input,
   nested agent resumptions and trace metadata. Treat the context as persisted data and keep secrets out of it,
   unless you mean them to travel. The key for exporting traces is excluded unless an option includes it.
7. **Store a version marker with a paused run that may wait.** The documentation advises recording the agent
   definition or SDK version so resuming can route to matching code when models, prompts or tool definitions
   change.
8. **The documentation's own server example is not a deployable service.** It consumes a request before loading
   and resuming, so failures and cancellations also consume it, and its store lives in one process. A real
   application supplies authentication, request protection, retention and recovery that reconciles tool side
   effects before any retry.

## 3.3 What traces record
1. **Tracing is on by default,** and can be turned off globally by an environment variable or in code, or for one
   run.
2. **Model-generation spans store the model's inputs and outputs and tool spans store tool inputs and outputs.**
   The setting that includes sensitive data defaults to on, and a default can also be set from the environment.
   Turn it off for anything that touches personal or secret data (own guidance: decide it per deployment, not by
   default).
3. **With the setting off,** model spans omit the request and response. For calls to an official OpenAI endpoint
   the span still carries a response identifier as correlation metadata; for custom endpoints that identifier
   is omitted too.
4. **A span for an approval-gated tool stores a custom rejection message only when the setting is on;** otherwise
   it records a generic error text. A paused approval does not store the internal wrapper as tool output.
5. **Audio spans carry base64-encoded audio by default,** controlled by a separate setting.
6. **Trace processors are independent observers.** The default provider catches a processor's exception and
   keeps calling the others, so a redaction processor registered before an exporter does not stop that exporter
   from receiving the data if redaction fails. Adding a processor leaves the default exporter registered.
7. **When export depends on redaction, do both in one exporter.** Replace the default processors with a batch
   processor configured with an application-owned exporter that copies the serialised payloads, redacts the
   copies and sends only the redacted result; if serialising, copying or redacting fails, drop the batch before
   calling the destination, and log a fixed failure message with no payload, exception text or traceback.
8. **Limits of that replacement:** a failed batch is dropped while later ones can still go out; replacing the
   processors does not erase data an earlier processor already buffered, so configure it before any trace is
   created; the redactor and destination are trusted code and must not log or send the original data.
9. **An allowlist beats a blocklist for what leaves.** The documentation's example allows only event categories and
   linkage identifiers, and notes that caller-supplied identifiers must carry nothing sensitive or be mapped to
   safe values.
10. **Export is batched.** Traces leave in the background every few seconds, or earlier when the queue fills, with a
    final flush at exit; a worker that needs delivery at the end of a job flushes after the trace context closes.
    Disabling tracing does not discard what the processors already buffered.
