---
name: rails-jobs-migrations-pitfalls
description: "Use when writing or reviewing Rails background jobs, schema migrations or RSpec doubles: what happens to a failed or killed Active Job under Solid Queue and GoodJob (retry_on, mail jobs, error reporting), queue and timeout settings, the strong_migrations patterns for PostgreSQL, and verifying doubles in RSpec."
---

# rails-jobs-migrations-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the narrow Rails traps that generic rules miss. The premise: **the
generic rule (retry safely, migrate without locking, mock honestly) is already written; what hurts is the
framework detail** that makes the generic rule not apply the way you assumed. Generic job rules are
`background-jobs-conventions` §1 to §5; generic test anti-patterns are `testing-anti-patterns` §1 and §2; the
deprecation path of a changed interface is `deprecation-migration`.

## When
- A job class, queue, retry policy or error reporter is added or changed in a Rails app.
- A migration touches a table that is in use.
- An RSpec spec uses a double, a stub or a constant.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Failure semantics: `retry_on`, mail jobs, killed workers, error reporting | a job can fail, be retried or be killed | [`01-job-failures.md`](./references/01-job-failures.md) |
| 2 | Job settings: timeouts, queues, concurrency limits, shutdown | a job calls out, a queue is named, or a limit is set | [`02-job-settings.md`](./references/02-job-settings.md) |
| 3 | Migrations on PostgreSQL: the strong_migrations patterns, timeouts | a column, constraint, reference or default changes on a live table | [`03-migrations.md`](./references/03-migrations.md) |
| 4 | RSpec doubles, partial doubles and constants | a spec stubs, doubles or declares a constant | [`04-rspec-doubles.md`](./references/04-rspec-doubles.md) |

## Output / checkpoint
For each job, the answer to "what happens when this process is killed mid-run, and who is told" is written in
the review; for each migration, the lock it takes and the deploy in which each step runs; for each double, the
interface it is checked against.

## Guardrails
- Never assume `retry_on` covers a killed process (§1.1).
- Never wrap work in Ruby's `Timeout` (§2.1).
- Never ship a column drop, `NOT NULL` or foreign key on a live PostgreSQL table in a single step (§3).
- Versions: each rule names its gem or framework version. Nothing here was run.

## Origin
Rewritten from the Rails 8.1 Active Job sources, the Solid Queue README (1.7.0), the GoodJob README (4.21.1),
the strong_migrations README (2.8.0) and a community RSpec style guide (CC BY 3.0), read 2026-10-08. Meant to be
folded into `rails-conventions` when the extended version of that block lands. 🟡: never run by us; open points
are in [`references/origin.md`](./references/origin.md).
