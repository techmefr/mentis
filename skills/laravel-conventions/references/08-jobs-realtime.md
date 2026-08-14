# laravel-conventions §8 — Jobs and realtime

> Section 8 of `skills/laravel-conventions`. Read it when a queued job, a notification, a broadcast. The other sections and the guardrails stay in `SKILL.md`.

1. **Order queued work explicitly** — chain the jobs, or make the later step verify its precondition. Never a
   fixed delay, `sleep`, or debounce window chosen so earlier work "should have settled": that's a race with
   a comment.
2. A job is idempotent where it can be: a queue retries.
3. Realtime broadcasting goes through the project's broadcaster (a Pusher-protocol-compatible server, or the
   framework's own), with channel authorisation declared alongside the channel — a public channel is a
   decision, not a default.
4. A broadcast payload is a contract with the frontend: it carries what the client needs, not the whole model
   with its hidden attributes.
