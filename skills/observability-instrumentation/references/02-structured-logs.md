# § 2 — Structured logs

> Section 2 of `skills/observability-instrumentation`. Read it when a log line is added or changed.
> `skills/security-hardening` §5 cites this section as what to check after a hostile-value replay.

1. Structured format (JSON), never free text for an event that has to be queryable during an
   incident. Free text is queryable by substring only, so the question "all failures for this
   customer" becomes a guess about how the sentence was worded — and the wording changes with every
   edit, silently invalidating whatever query somebody saved.
2. Correlation ID mandatory on any call chain crossing several services/layers: without it, it's
   impossible to tie together the logs of a single request. It has to be *propagated*, which is the
   half that gets missed: generated at the edge, carried on every outbound call, and re-attached on the
   other side of a queue, where the chain is otherwise broken by design.
3. Redaction of personal/sensitive data (PII) before writing: never an email, a password or a
   client's data in clear text in a log.
4. **Credentials are redacted by field name, not by call-site discipline**: `authorization`,
   `cookie`, `set-cookie`, `access_token`, `refresh_token`, API keys. The leak is rarely a
   deliberate log line, it's logging a whole object that carries them, an HTTP client's error
   (which holds the request headers) being the classic one. See `auth-session-conventions` §2.4 for
   the paths to watch.
5. **A log is a copy that leaves its source's access controls behind.** Whatever is written lands in a
   system with different retention, a different audience and often a third-party operator, which is why
   redaction is not a tidiness rule: the same row that was protected in the database is readable by
   everyone with log access (`business/data-protection`).
6. **Log the request's own values as data, never interpolated into the message.** The message is the
   stable identity of the event, and a value spliced into it makes every occurrence a distinct string —
   which defeats grouping, defeats counting, and turns an error tracker into a list. Fields for the
   values, a constant for the message.
7. **Say what the level means and use it.** Levels are the only filter an on-call has before they know
   what they are looking for, so a warning used for an expected case teaches them to ignore warnings,
   and an error logged for a handled condition puts a permanent count in a dashboard nobody can drive
   to zero. Something has to be genuinely wrong at error level, or the level is decoration.
8. **A caught exception is logged once, with its cause, at the boundary that decides what to do.**
   Logging it at every level on the way up produces several entries for one failure, so the on-call
   counts occurrences that never happened and the stack is missing from the entry that did get read.
9. **A log line has to say what happened to the work.** Retried, dropped, queued, partially applied:
   the operator's next action depends on it, and "failed to process order" leaves them unable to tell
   whether the order exists.
10. **Never log inside a hot loop, and never make a log line expensive.** Serialising a large object,
    resolving a relation for a message, or writing per item in a batch turns instrumentation into the
    performance problem it was added to investigate — and it does so precisely under load, when the
    logs are most wanted.
11. **Logging has to survive its own failure.** An unreachable log backend must not take the request
    with it, and a full disk must not stop the process; equally, a log write that blocks the request
    path makes the observability system a dependency of the feature. Asynchronous, bounded, and
    dropping rather than failing.
12. **A log the format of which nothing reads is unstructured after all.** Fields renamed per service,
    a timestamp in a local format, a level as a number in one place and a word in another: each breaks
    the cross-service query that was the point of structuring. One vocabulary, declared once.
