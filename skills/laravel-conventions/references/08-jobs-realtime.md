# laravel-conventions §8 — Jobs, notifications and realtime

> Section 8 of `skills/laravel-conventions`. Read it when a queued job, a notification, a broadcast. The other sections and the guardrails stay in `SKILL.md`.

1. **Order queued work explicitly** — chain the jobs, or make the later step verify its precondition. Never
   a fixed delay, `sleep`, or debounce window chosen so earlier work "should have settled": that's a race
   with a comment. The reason it passes review is that it passes locally, where one worker drains the queue
   in order; the race appears the first time two workers run, which is usually production.
2. **A job is idempotent where it can be, because a queue retries.** Assume every job may run twice: on a
   timeout that already succeeded, on a redeploy mid-run, on a manual retry after a fixed bug. So a job
   asserts the end state rather than applying a delta — set the flag, don't increment the counter; upsert,
   don't insert — and where a side effect genuinely cannot be repeated (a payment, an email), the guard is
   a persisted marker written in the same transaction as the effect, not a check at the top of `handle()`.
3. **A job's payload is a serialised reference, not a snapshot.** A queued model is re-fetched by key when
   the job runs, so the row may have changed or be gone — a job that must act on the state it was created
   with has to carry that state as scalars, and a job whose subject can be deleted has to tolerate the
   missing model instead of throwing on every retry until the queue gives up.
4. **Dispatch after commit.** A job dispatched inside a transaction can start before the commit, or after a
   rollback, and then reads state that never existed. This is the same rule as `skills/design-patterns` §4.7
   and it is the one that gets forgotten, because the failure is intermittent and looks like a queue
   problem.
5. **Failure is part of the design, not the operator's problem.** Every job declares what happens when it
   exhausts its attempts — a `failed()` that leaves the record in a state a human can act on, retries
   bounded rather than infinite, and a backoff where the cause is a rate limit or an unavailable
   dependency. A job that fails silently and leaves a row half-updated is worse than one that never ran,
   because nothing distinguishes it from success. And §11's rule applies here too: swallowing the
   exception to keep the queue green removes the only signal anyone had.
6. **Queue what is slow or fragile, not what is convenient.** A third-party call, an export, a large
   recalculation belong on a queue; a two-row update does not, and moving it there buys nothing while
   making the request's result eventually-consistent — which the interface then has to explain. The
   question is *would the user rather wait, or rather be told it is in progress?*
7. **User-facing messages go through notifications, not hand-built mail.** One channel-agnostic
   notification per event, with the channels chosen per recipient, is what makes adding an in-app or push
   channel a configuration change instead of a second copy of the message. Hand-rolled mail also tends to
   skip what the notification layer already handles: queueing, locale, and the recipient's own preferences.
8. **Realtime broadcasting goes through the project's broadcaster** (a Pusher-protocol-compatible server,
   or the framework's own), with channel authorisation declared alongside the channel — a public channel is
   a decision, not a default. Private channels authorise per subscriber, and that check is the same
   authorisation question as §2: a channel named after a record id is only private if something compares
   the subscriber to that record.
9. **A broadcast payload is a contract with the frontend**: it carries what the client needs, not the whole
   model with its hidden attributes. Broadcasting a model serialises whatever the model serialises, which
   is how a hidden column reaches a browser. Name the fields.
10. **A broadcast is a hint, not a source of truth.** Delivery is best-effort and ordering across channels
    is not guaranteed, so the client refreshes from the API on the event rather than treating the payload
    as the new state — otherwise a dropped frame leaves the interface permanently wrong, and only a reload
    fixes it.
11. **Scheduled work is a queued job with a clock, and it inherits every rule above** plus one of its own:
    it must not assume it ran last time. A task that processes "since the last run" needs the last run
    persisted, because a missed window is normal — a deploy, a stopped worker, a host reboot.
12. **Job middleware (`WithoutOverlapping`, `RateLimited`, `ThrottlesExceptions`) is the framework's answer
    to point 1's ordering problem for the specific case of "not two of these at once" or "not too many of
    these per minute"** — declared on the job's `middleware()` method rather than reinvented as a database
    lock or a cache flag read at the top of `handle()`. `WithoutOverlapping` releases a job back onto the
    queue rather than dropping it, which still needs point 2's idempotence if the release happens after
    partial work.
13. **`Bus::batch()` coordinates jobs that must be reported on together, not jobs that must run together.**
    Its `then`/`catch`/`finally` callbacks fire once for the whole batch, so a batch is the answer to "tell
    me when all forty exports are done" — point 4's dispatch-after-commit rule still applies to the batch
    itself, and a job inside it that needs another job's *result*, not just its completion, is a chain
    (point 1), because a batch does not pass data between its members.
14. **`ShouldBeUnique` and `WithoutOverlapping` answer different questions, and a job can need both.**
    `ShouldBeUnique` stops a duplicate from ever reaching the queue while one instance is already queued or
    running — the second `dispatch()` call is simply dropped. `WithoutOverlapping` lets the duplicate onto
    the queue and only keeps two copies from *processing* at once, releasing the later one back for a retry
    instead of discarding it. A job that must never pile up (the nightly export somebody re-triggers by
    hand) wants the first; a job that tolerates being re-queued but not run twice in parallel wants the
    second — and either way the uniqueness lock is a cache entry with its own TTL, so a lock that outlives
    the job it was guarding silently blocks every legitimate retry after it.
15. **A presence channel is a private channel plus a roster, not a separate authorisation model.** Its
    `join()` callback still returns the same yes/no this record's owner may see this channel that point 8
    asks for private channels; what it adds on top is a payload describing *who else is here*, which is why
    it exists — a shared document, a chat room, anywhere the interface itself shows "3 people viewing".
    Reaching for a presence channel because it "sounds more real-time" without ever rendering that roster
    is a private channel with an unused feature and a heavier handshake.
16. **A notification meant for someone who isn't a `User` — an email captured in a form, a webhook target
    with no account — is routed on demand**, not by inventing a throwaway model to hang a
    `Notifiable` trait on. The routing (address, channel) travels with the `send()` call instead of living
    on a record, which is the right shape precisely when there is no record: the recipient's identity is the
    notification's problem to carry, not the domain's problem to model.
17. **A job payload that carries something sensitive — a token, a document, PII — is encrypted at rest with
    `ShouldBeEncrypted`,** because the default queue payload is a plain serialised string sitting in
    whatever store backs the connection (a database row, a Redis key), readable by anything with access to
    that store. Encrypting the payload is the same reasoning as point 3 pushed one step further: a
    reference is safer than a snapshot, and a snapshot that must exist is safer encrypted than in the clear.
