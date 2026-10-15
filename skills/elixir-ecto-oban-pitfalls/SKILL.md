---
name: elixir-ecto-oban-pitfalls
description: "Use when writing or reviewing Elixir persistence, background jobs or configuration: Ecto uniqueness constraints, upserts and aborted transactions, Oban production settings and unique-job limits, and when configuration is read (config.exs, runtime.exs, compile_env, Phoenix force_ssl)."
---

# elixir-ecto-oban-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the narrow Elixir traps that generic rules miss. The premise: **the
database and the build system settle these questions, and the code that looks right asks them too early**. Generic
job rules are `background-jobs-conventions` §1 to §5; secrets handling is `security-hardening` §4; generic test
anti-patterns are `testing-anti-patterns`.

## When
- An Ecto changeset, upsert or transaction is written or reviewed.
- An Oban worker, queue or plugin setting is added or changed.
- A value is read from the application environment, or a release is built.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Ecto: unique constraints, upserts, aborted transactions, raw fragments | a uniqueness rule, an insert-or-update or a transaction is written | [`01-ecto.md`](./references/01-ecto.md) |
| 2 | Oban: args, attempts, uniqueness, pruning, orphans, errors, tests | a worker or Oban config changes | [`02-oban.md`](./references/02-oban.md) |
| 3 | Configuration timing: build time, runtime, `compile_env`, `force_ssl` | a value comes from the environment or a release is built | [`03-config-timing.md`](./references/03-config-timing.md) |

## Output / checkpoint
For each uniqueness rule, the index that enforces it is named; for each transaction, what happens to the next
statement after a failed insert; for each unique job, what it does not prevent; for each configuration value,
whether it is read at build time or at boot.

## Guardrails
- Never rely on `unsafe_validate_unique` alone for a uniqueness guarantee (§1.1).
- Never run a statement after a failed one in the same transaction without a savepoint (§1.3).
- Never read a runtime value in a module attribute (§3.2).
- Versions: each rule names its library or Elixir version. Nothing here was run.

## Origin
Rewritten from the Ecto 3.14.2 and Oban 2.24.1 source documentation and guides (Apache-2.0), the Elixir 1.20.4
`Config`, `Application` and release documentation (Apache-2.0) and the Phoenix SSL guide (MIT), read 2026-10-08.
Meant to be folded into `elixir-phoenix-conventions` when the extended version of that block lands. 🟡: never
run by us; open points are in [`references/origin.md`](./references/origin.md).
