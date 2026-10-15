# rails-jobs-migrations-pitfalls §1 — Job failures

Sources: Rails 8.1.4 (`activejob` `exceptions.rb`, `actionmailer` `mail_delivery_job.rb`, branch 8-1-stable),
the Solid Queue README (1.7.0) and the GoodJob README (4.21.1), read 2026-10-08.

## 1.1 What `retry_on` covers
1. **`retry_on` and `rescue_from` only intercept exceptions raised inside `perform`.** A worker killed by
   `SIGKILL` (an out-of-memory kill, for example) never raises inside the job, so neither runs. Solid Queue says
   so explicitly: after the missing heartbeat is noticed, a different process marks the job failed with
   `SolidQueue::Processes::ProcessPrunedError`, and it deliberately does not retry it, because the job may be what
   killed the worker. Recover from outside: look at the failed executions (a dashboard, or the
   `fail_many_claimed.solid_queue` event, which carries the error and the job ids), and retry only jobs known to be
   idempotent (`background-jobs-conventions` §1).
2. **GoodJob behaves the other way.** It retries a job automatically when the process is interrupted before the job
   finishes, including after `SIGKILL` or power loss; the interrupted execution is recorded as
   `GoodJob::InterruptedError`. To control that, include the `InterruptErrors` extension in the job class and use
   `retry_on` or `discard_on` for `GoodJob::InterruptError`. Know which backend you run before reasoning about a
   killed worker.
3. **Solid Queue marks a job failed when a worker is terminated outside the graceful signals,** with
   `SolidQueue::Processes::ProcessExitError`. A job that causes such a kill (a memory leak) is visible this way.
4. **Solid Queue has no retry of its own.** A failed job stays as a failed execution until discarded or retried by
   hand or by code; only Active Job's `retry_on` retries.

## 1.2 What happens after the last attempt
1. **A limited `retry_on` re-raises the last error** to the backend when attempts run out (Active Job 8.1: it
   calls the stop hook, runs the after-discard callbacks, then raises), unless a block is given: with a block, the
   block handles the final error and nothing is raised. The defaults are `attempts: 5` and `wait: 3.seconds`.
2. **An unlimited `retry_on` never reaches the backend's error hook.** GoodJob documents that with
   `attempts: Float::INFINITY` its `on_thread_error` is never called, and suggests an explicit wrapper in
   `around_perform` that reports the error and re-raises. Rails 8.1 also accepts `report: true`, which sends each
   retried error to `ActiveSupport.error_reporter` before it is retried.
3. **GoodJob does not retry by default.** An error that reaches it is not retried unless `retry_on` is set or
   `retry_on_unhandled_error` is true, in which case it retries immediately and without limit, which the README
   warns can cause high load.

## 1.3 Mail jobs are separate
1. **`ActionMailer::MailDeliveryJob` inherits from `ActiveJob::Base`, not from `ApplicationJob`.** Anything declared
   on `ApplicationJob` (`rescue_from`, `retry_on`, `around_perform`, error reporting) does not apply to
   `deliver_later`. Declare it again on `ActionMailer::MailDeliveryJob`, or in the mailer base class as Solid Queue's
   README does.
2. **The job rescues `StandardError` and hands it to the mailer class** (`handle_exception`), which re-raises
   when no mailer handler is declared. A mail failure is therefore handled by the mailer's own `rescue_from`
   before it is raised again, so declare handling where the failure is meant to be seen.

## 1.4 Reporting
1. **Report from the job class, and re-raise.** Solid Queue's README shows a `rescue_from(Exception)` on the
   application job that calls `Rails.error.report` and then raises again, and says that its own
   `on_thread_error` hook is not used for errors inside a job.
2. **Count something that is not an exception.** A job killed rather than raised, or silently retried forever, only
   shows up as a failed-execution count, a queue age or an attempt count; alert on those, not only on exceptions
   (own guidance).
