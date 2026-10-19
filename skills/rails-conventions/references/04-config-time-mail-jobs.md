# § 4 — Configuration, time, translations, mail and jobs

> Section 4 of `skills/rails-conventions`. Read it when an environment setting or a secret is read, a date or a
> time is produced or compared, user-facing text is written, an email is sent, or a job is enqueued or
> declared. Pinned to Rails 7.1 to 8.x as read on 2026-10-02; the job points assume Active Job with a queue
> backend, and the transactional ones are the guide's wording for the database-backed default queue.

1. **Three environments, no more.** `development`, `test` and `production` exist; a staging environment is
   production with different environment variables, not a fourth `config/environments` file whose differences
   from production nobody tracks. Settings common to every environment go in `config/application.rb`;
   additional structured configuration goes in a YAML file under `config/` loaded with `config_for`.
2. **Initialisation code lives in `config/initializers`, one file per gem, named after the gem.** The file
   that configures a gem is then the first place to look when it misbehaves.
3. **After an upgrade, move `config.load_defaults` to the new version, deliberately.** An application keeps the
   configuration defaults of the Rails version it started on until told otherwise, so the setting should match
   the framework version in use; change it as its own step, with the test suite as the check, not folded into
   the dependency bump.
4. **Environment variables are read once, at boot, into configuration.** A bare `ENV["X"]` deep in the code
   turns a missing variable into a runtime error on the request that happens to need it; reading it during
   initialisation and copying it into the application's config makes the same mistake fail the deploy.
   Secrets live in encrypted credentials: the encrypted file may be committed, the master key never; use the
   bang reader (`credentials.some_key!`) so a blank value raises instead of producing a `nil` that fails later.
5. **Do not branch on `Rails.env` for behaviour.** A condition on the environment name is a feature flag that
   nobody can switch off without a deploy. The built-in `Rails.env.local?` (development or test, Rails 7.1+)
   is the honest exception: it expresses "this must never run in production", not "this is how production
   is configured".
6. **Time is always zone-aware.** Set `config.time_zone`, and produce times with `Time.current` or
   `Time.zone.now`, parse with `Time.zone.parse`, never with `Time.now`, `Time.parse` or `String#to_time`,
   which use the system zone and ignore the configured one. Do not store a relative date in a constant
   (`EXPIRED_AT = 1.week.since`): it is evaluated once, at load. Write durations as `1.minute.ago` and
   `2.days.from_now` rather than arithmetic on the current time, with positive literals, and prefer
   `date.all_week` and its siblings to `beginning_of_week..end_of_week`.
7. **Every user-facing string is a translation key.** No literal text in views, models or controllers; keys
   are dot-separated, looked up lazily from a template (`t(".title")` inside the view the key is scoped to),
   and model and attribute names are translated under the `activerecord` scope so that form labels and error
   messages follow. Shared formats (dates, currency) sit at the root of the locale files. When locale files
   are split into directories, add the load path in the application config or the nested files are never
   loaded.
8. **A job is enqueued only when the data it needs is committed.** A job enqueued inside a transaction may run
   before the transaction commits, and may be enqueued even if the transaction then rolls back. Turn on
   `enqueue_after_transaction_commit` (globally in the application's base job is the safest default), or
   enqueue from an `after_commit` callback; do not rely on the queue backend happening to behave.
9. **Pass records to jobs, not their ids.** Active Job serialises a record as a global id and locates it when
   the job runs; the job's signature then states what it works on. A record deleted in the meantime raises a
   not-found-on-deserialisation error; a job for which that is normal discards that exact error, never its
   parent class, which would also discard a job that failed on a transient database error.
10. **Retries are declared per job.** On the database-backed queue a job with no `retry_on` goes straight to
    failed; declare which errors retry, with a wait that grows (`:exponentially_longer`) and a bounded number
    of attempts, and which are discarded. A job that can be interrupted and retried must be safe to run again:
    check the state it is about to change, or use the continuation feature to resume from a recorded cursor
    rather than start over.
11. **Mail is sent from a job.** Delivering during the request makes the page wait for the mail server and
    times out when several are sent; use `deliver_later`. Mailers are named `SomethingMailer`, ship an HTML and
    a plain-text template, inline their styles for the mail clients that ignore external ones, and set a
    default host for URL helpers. In development, raise delivery errors (they are off by default) and send to
    a local catcher; in test, the delivery method is `:test`.
12. **Logs never contain credentials.** Add every sensitive parameter name to `filter_parameters` (the defaults
    match partially on `passw`, `secret` and `token`); pass a block to debug-level log calls with an
    interpolated string, so that production's `info` level does not pay to build a message it discards.
13. **Process rules outside the code.** Gems used only in development or test are in their Gemfile groups;
    `Gemfile.lock` is committed; use only established gems and review the source of a small one before taking
    it on.
