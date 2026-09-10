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
18. **`ThrottlesExceptions`' two constructor arguments answer two different questions, and confusing them
    produces a job that either never throttles or throttles forever.** The first is how many exceptions the
    job may throw before it is considered failing; the second is how many minutes the throttle then holds
    before the job is tried again. Pair it with `backoff()` on the middleware itself, not a `sleep()` inside
    `handle()` — the delay belongs to the queue's retry mechanism, which can release the job without tying
    up a worker process for the wait.
19. **A released job (`WithoutOverlapping`, a rate limiter, a manual `$this->release()`) still counts
    against `tries` and `maxExceptions`,** so a job released every time it runs eventually exhausts its
    attempts and lands in `failed()` even though it never actually failed — a release loop needs either a
    generous `tries` or its own escape hatch (a `retryUntil()` far enough out, or an explicit check that
    stops releasing past a point and reports instead).
20. **`retryUntil()` bounds a job by wall-clock time instead of by attempt count**, which is the right
    limit for a job whose usefulness expires — a price-check email, a session-bound export — where trying
    a twentieth time an hour later serves nobody even though the attempt count alone would allow it.
    `tries` and `retryUntil()` combine as whichever limit is hit first, not as alternatives to choose
    between.
21. **A queue connection's `retry_after` must exceed the job's own real runtime, or the queue schedules a
    second worker onto the same job before the first one finishes** — the symptom is a job that appears to
    run twice concurrently, which then needs point 2's idempotence to survive but shouldn't have happened
    in the first place. This is a config value (§7), tuned per queue rather than left at the framework's
    default when a job's workload is known to run long.
22. **A private channel's authorisation callback answers exactly one question — may this authenticated
    user see this channel — and nothing else belongs in it.** Loading unrelated data, dispatching a side
    effect, or writing to the database inside `Broadcast::channel()` turns an authorisation check that runs
    on every subscribe attempt into a place with effects nobody expects a permission check to have; keep it
    to the same yes/no §2 already asks of a policy.
23. **Job batching's `allowFailures()` changes whether one job's failure cancels the batch**, and the
    default — a single failed job cancels the rest — is usually wrong for independent work items (forty
    unrelated exports) and usually right for a pipeline where a later step depends on an earlier one's
    output. Naming the choice explicitly is cheaper than discovering it from which jobs quietly never ran.
24. **`toOthers()` excludes the socket that triggered the broadcast from receiving it back.** Without it, the
    client that just made the change gets a second copy of its own update over the socket connection, on top
    of whatever its own request/response already told it — the interface either double-applies the change or
    has to de-duplicate an event against a response it already has, which is point 10's "the client refreshes
    from the API" made harder for no reason.
25. **`ShouldBroadcastNow` sends the event synchronously, skipping the queue `ShouldBroadcast` uses.** That is
    the right choice for a broadcast whose entire value is the immediacy — a typing indicator, a cursor
    position — where the round trip through a queue worker would make the event visibly stale by the time it
    arrives; it is the wrong choice for anything point 6 already says belongs on a queue; a broadcast carrying
    real work (a recalculation, a large payload) synchronously ties up the request that triggered it.
26. **A queued model relationship loaded before dispatch is serialised into the payload unless
    `withoutRelations()` strips it.** `SerializesModels` re-fetches the model by key (point 3) but keeps any
    relation already loaded in memory at dispatch time, so a job built from a model with `->load('items')`
    still called on it carries every one of those rows into the queue's storage a second time — for a payload
    meant to be a lean reference, that is the accidental snapshot point 3 warns about, arriving through a
    side door.
27. **A job is routed to a queue by priority with `->onQueue()`, and the priority only means something if a
    worker actually listens to that queue name first.** `php artisan queue:work --queue=high,default` drains
    `high` before `default`; a job dispatched `->onQueue('high')` against a worker started with no
    `--queue` flag (the implicit `default` only) never gets the priority it was given — the routing and the
    worker's listen order are one decision split across two places in the deploy config, and only one of them
    failing to match is silent.
28. **A batch can grow after it starts: `$batch->add(...)` from inside a job already in that batch appends
    more jobs to the same batch rather than starting a second one.** That is what makes a batch usable for
    work whose full size isn't known up front — a paginated export that discovers page two only after
    reading page one — but it also means `finally` can fire before a job that just added itself has actually
    run, unless the added jobs are counted before the batch is allowed to consider itself finished.
29. **`Concurrency::run()` runs independent closures in parallel without a queue, for work that must finish
    before the request continues** — several unrelated API calls whose results the response needs right now.
    It is not a substitute for a queue: nothing survives a worker restart, there is no retry, and point 5's
    failure design does not apply, because there is no `failed()` to define. Reach for it only when point 6's
    "does the user need to wait" answer is genuinely yes and the wait is for parallel I/O, not serial work.
30. **A job's `$afterCommit` property is point 4's dispatch-after-commit rule made per-job instead of a global
    connection setting.** Setting `queue.connections.*.after_commit` in config applies to every job on that
    connection; a job that must dispatch inside the transaction anyway (rare, but genuine — a step that reads
    uncommitted work on purpose within the same request) overrides it with `public $afterCommit = false;` on
    the job itself. The property exists precisely so one exception to point 4 doesn't force turning the rule
    off connection-wide.
31. **`Bus::chain([...])->catch(function (Throwable $e) {...})` fires once, for the first job in the chain
    that fails, and it is not the same signal as that job's own `failed()`.** The chain stops at the failing
    link — later jobs never run — and the `catch` callback is where a chain-level cleanup or notification
    belongs, separate from whatever the individual job's `failed()` (point 5) already does for that job alone;
    relying on the job's own `failed()` to also cover "the chain as a whole didn't finish" misses the case
    where an *earlier* job in the same chain is what actually broke it.
32. **A job's `displayName()` override is what a queue dashboard (Horizon, `queue:monitor`) shows instead of
    the fully-qualified class name, and it is worth setting once a job class is reused for several distinct
    operations.** `ProcessExport::displayName()` returning `"Export invoices for tenant {$this->tenantId}"`
    turns a dashboard full of identical `ProcessExport` entries into one that says which tenant's export is
    stuck — the default (the class name) is fine for a job that only ever does one thing, and stops being
    enough the moment the same class handles several distinguishable payloads.
33. **`$deleteWhenMissingModels` on a job tells the framework to silently discard the job when
    `SerializesModels` re-fetches its subject (point 3) and finds it gone, instead of throwing a
    `ModelNotFoundException` that then exhausts retries and lands in `failed()`.** It is the right default for
    a job whose subject being deleted before the job runs is an expected, harmless outcome (send a reminder
    about a record someone since removed); leaving it off is right when a missing subject is itself the
    anomaly a `failed()` handler should know about, so the choice is a statement about which case is normal
    for that specific job, not a blanket setting to reach for everywhere.
34. **A notification's `via()` method receives the notifiable and can choose channels per recipient, not just
    per notification class.** `via($notifiable)` returning `['mail']` for a user who opted out of in-app
    alerts and `['mail', 'database', 'broadcast']` for one who didn't is what point 7's "channels chosen per
    recipient" actually means in code — a fixed `protected $channels = ['mail']` on the class can only ever
    express one policy for every recipient, which is the shortcut that quietly reappears the day two
    recipients need to be treated differently.
35. **`Queue::before()` and `Queue::after()` listeners observe every job on every queue from one place, which
    is the right layer for logging or metrics that shouldn't live inside each job's `handle()`.** Registered
    once in a service provider, they fire around every job regardless of class — a duration metric, a
    structured log line with the job name and tenant — without touching the job classes themselves; point 12's
    per-job middleware is the tool when the behaviour is specific to *one* job's concurrency or rate, and these
    listeners are the tool when it's a blanket concern across all of them.
36. **`broadcastAs()` and `broadcastWith()` decouple the event name and payload a frontend listens for from the
    PHP class name and public properties, and skipping them ties the two together by accident.** Without
    `broadcastAs()`, the event name on the wire is the fully-qualified class name, so renaming or moving the
    PHP class (a refactor with no behavioural intent) breaks every listener still bound to the old name; without
    `broadcastWith()`, the payload is every public property serialised as-is, which is the same "broadcast the
    model, not the contract" problem point 9 already names, here for a plain event's own properties instead of
    a model attached to it.
