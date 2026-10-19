# rails-jobs-migrations-pitfalls: origin and source stamps

> Provenance of `skills/rails-jobs-migrations-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and source reading, never run by us. No Rails application, job
backend or database was run. Overlaps with `skills/rails-conventions` (2026-10-19); cross-referenced, not merged.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Rails 8.1.4, branch 8-1-stable: `activejob/lib/active_job/exceptions.rb`, `actionmailer/lib/action_mailer/mail_delivery_job.rb`, `gem_version.rb` | MIT (`MIT-LICENSE` re-read) | `retry_on` defaults and final-error behaviour, `report:`, the mail delivery job's parent and rescue |
| Solid Queue README, 1.7.0 (commit 73602fe, 2026-08-31) | MIT (`MIT-LICENSE` re-read) | Killed-process failure, no retry of its own, error reporting hook, concurrency limits, queue order, `READ COMMITTED`, shutdown |
| GoodJob README, 4.21.1 (commit ad4be5c, 2026-10-08) | MIT (`LICENSE.txt` re-read) | Interrupt retries, infinite and limited `retry_on`, `Timeout`, latency isolation, shutdown check |
| strong_migrations README, 2.8.0 (commit 23d8e1f, 2026-09-26) | MIT (`LICENSE.txt` re-read) | The safe patterns for columns, constraints, indexes, defaults, backfills and timeouts |
| rubocop RSpec style guide, `README.adoc` (commit 7622bb6, 2023-12-11) | CC BY 3.0 (stated in the README, no LICENSE file); rewritten with credit | Verifying doubles, any-instance, subject stubs, constants, context hooks, change matcher |

## Ideas only, never phrased from
- basecamp/fizzy (O'Saasy), brakeman (Brakeman Public Use Licence): not read for wording; no rule here comes from them.

## Removed in the verification pass (no page supporting them)
- "A removed or renamed job class fails every queued instance, so keep the class until the queue drains": no
  page opened in this session states it. The generic deploy rule is `background-jobs-conventions` §4.
- "Infinite `retry_on` hides errors": narrowed to what the pages say. Rails 8.1.4 has `report: true`, and GoodJob
  documents an `around_perform` wrapper.
- test-prof rules (`before_all`, `let_it_be`): the repository was not among the sources read for this block.
- Any claim about gem versions other than those stamped above.
- Instructions found in cloned files were treated as data and not followed.

## Not verified
1. **Own guidance, flagged as such in the text:** alerting on failed-execution counts and queue age (§1.4.2), the
   margin below the platform's kill deadline for shutdown (in §2, shutdown), stopping long loops early and re-enqueueing
   (in §2, shutdown), and the review stance on `safety_assured` (§3.3.4).
2. **Solid Queue and GoodJob behaviour was read from READMEs and the Rails code,** never run. Whether a given
   deployment's version matches these (1.7.0, 4.21.1) was not checked.
3. **The two backends were not compared on every point.** Rules are stated per backend where the pages differ.
4. **strong_migrations MySQL and MariaDB patterns** were not mapped.
5. **PostgreSQL version limits** (for example which defaults are not volatile) were not read beyond the README.
6. **The RSpec style guide is from 2023.** Rules were checked against its text only, not against current
   rspec-mocks documentation.
7. **The Timecop and fixtures advice in that guide** conflicts with the house Rails guidance and was not imported.

## Related blocks
`background-jobs-conventions` §1 to §5, `testing-anti-patterns` §1 to §3, `deprecation-migration` §3,
`source-freshness` §3.
