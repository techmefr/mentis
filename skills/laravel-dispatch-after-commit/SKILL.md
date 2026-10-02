---
name: laravel-dispatch-after-commit
description: "Use when an event, queued job, notification or mailable is dispatched while a database transaction is open in Laravel: defer it until the commit, drop it on rollback, and assert the right delivery mode in tests."
---

# laravel-dispatch-after-commit

Step 6 of the pipeline (`WORKFLOW.md`). Anything that can run elsewhere or later than the transaction that
caused it can run before the data it needs is visible, or run for data that was rolled back. Narrower than
`skills/laravel-conventions` §8 (jobs and notifications in general) and sits with
`skills/laravel-idempotent-jobs`.

**Special status.** New block, 🟡: written from the rule files the Laravel team ships for its tooling and a
static-analysis rule set, never run on real work in house. Class and method names move between framework
versions: confirm them against the installed one.

## When
A dispatch, `notify`, `Mail::send` or `event()` inside `DB::transaction(...)` or inside code a transaction
wraps (an action called from a transactional controller), or a job that "sometimes can't find the row".

## Steps
1. **The failure is a race with the commit.** A queued job pushed while a transaction is still open may be taken by
   a fast worker before the commit and load rows that are not visible yet, or work on half-written state. A rollback does not
   cancel the job: it runs anyway, against rows that were never kept.
2. **Jobs.** Defer with `->afterCommit()` on the dispatch, `public bool $afterCommit = true` on the job, or
   the after-commit queueing contract on the job; or enable the queue connection's `after_commit` option for
   the whole app. The last `afterCommit()`/`beforeCommit()` call in a dispatch chain wins over the property.
   The outermost transaction decides, and a rollback drops the dispatch.
3. **Events.** An event dispatched inside a transaction implements the after-commit dispatch contract
   (`ShouldDispatchAfterCommit`): dispatch waits for every open transaction to commit and is discarded on
   rollback. This covers synchronous and queued listeners alike, so it is not only about queue timing.
4. **Notifications and mail.** Queue anything that calls an outside service (mail, SMS, chat) unless the
   caller needs the outcome now. A queued notification or mailable sent in a transaction takes
   `->afterCommit()` (or the connection option). The setting has no effect on a synchronous send.
5. **Per-channel queues.** Notification channels with different latency needs implement `viaQueues()` to use
   separate queues. A recipient's locale is carried to queued delivery when the notifiable implements the
   locale-preference contract.
6. **Non-user recipients use on-demand notifications**, not a dummy model made to receive one.
7. **Tests assert the delivery mode.** A mailable that implements `ShouldQueue` is asserted with
   `Mail::assertQueued`, not `assertSent`, which would fail or pass for the wrong reason. Test rendered
   content on the mailable itself and delivery separately, so a failure names which broke.
8. **Test the rollback.** One test that throws inside the transaction and asserts nothing was dispatched is
   worth more than five that assert it was.

## Output / checkpoint
Every dispatch reachable from a transaction is deferred by one of the mechanisms above, with a test that
shows a rolled-back transaction dispatches nothing. Checked at `gate` (7) and `review` (8).

## Guardrails
No comments in the code produced. New and changed code only (`skills/code-baseline` §0). Do not remove a
transaction to dodge the problem. Enabling `after_commit` globally is a configuration decision for the owner
of the queue setup, flagged rather than applied unprompted.

## Origin
Rewritten from the `events-notifications` and `mail` rule files of Laravel Boost (`laravel/boost`, MIT,
cloned 2026-10-02) and from the `JobDispatchedInTransactionUsesAfterCommitRule` entry of the Larastan rules
documentation (`larastan/larastan`, MIT, cloned 2026-10-02, 3.x docs). Mechanisms only, rewritten in our
words.
