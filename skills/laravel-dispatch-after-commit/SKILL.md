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
   Precedence in the framework: a job implementing the contract defers unless its property is explicitly
   `false`; otherwise a non-null property decides; otherwise the connection option. A nested transaction's
   commit runs nothing: the outermost commit decides, and a rollback drops the dispatch. A unique job's lock
   is released on that rollback.
3. **Events.** An event dispatched inside a transaction implements the after-commit dispatch contract
   (`ShouldDispatchAfterCommit`): dispatch waits for every open transaction to commit and is discarded on
   rollback. In the framework's dispatcher the whole dispatch is deferred, so synchronous listeners and
   broadcasting wait too: it is not only about queue timing. A queued listener has its own contract
   (`ShouldQueueAfterCommit`), and a synchronous listener can defer itself with
   `ShouldHandleEventsAfterCommit`; model lifecycle hooks (creating, updating, saving, deleting, restoring,
   force-deleting) are exempt from the latter.
4. **Notifications and mail.** Queue anything that calls an outside service (mail, SMS, chat) unless the
   caller needs the outcome now. A queued notification or mailable sent in a transaction takes
   `->afterCommit()` (or the connection option); the manual does not say what the call does when the
   connection option is already on, so do not rely on mixing them. A notification is one job per recipient and
   channel, each deferred. A synchronous send is not queued, so the setting is moot there (🟡: our reading).
5. **Per-channel queues.** Notification channels with different latency needs implement `viaQueues()` to use
   separate queues. A recipient's locale is carried to queued delivery when the notifiable implements the
   locale-preference contract.
6. **Non-user recipients use on-demand notifications**, not a dummy model made to receive one.
7. **Tests assert the delivery mode.** A mailable that implements `ShouldQueue` is asserted with
   `Mail::assertQueued`, not `assertSent`, which would fail or pass for the wrong reason. Test rendered
   content on the mailable itself and delivery separately, so a failure names which broke.
8. **Test the rollback.** One test that throws inside the transaction and asserts nothing was dispatched is
   worth more than five that assert it was.
9. **Do not trust the static check to find every case.** The Larastan rule is off by default and inspects only
   `Job::dispatch()` and the global `dispatch()` helper inside a `DB::transaction` closure: dispatches through
   the bus or queue facades, and manual begin/commit blocks, are not seen. Review those by hand.
10. **Rule out the event-fake trap.** With the event fake active no listener runs; a test of an after-commit
    listener therefore needs the real dispatcher, or it proves nothing about the deferral.

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
