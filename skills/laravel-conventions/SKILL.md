---
name: laravel-conventions
description: Use when writing or reviewing Laravel: where behaviour lives, authorisation, data model and queries, naming and typing, HTTP surface, config and commands, jobs, tests, architecture. The framework layer above skills/php-patterns.
---

# laravel-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the writing and review of Laravel code. Sits **above**
`skills/php-patterns` (which stays on the language: typing, error handling, OOP) and below the review agent
for the stack. Every rule holds in a repo with **nothing installed** (`CONVENTIONS.md`, rule A).

**Relation to an org skill catalogue.** Where a company ships its own versioned catalogue for this stack, it
is the authority on **its** house style — its approved package list, its architecture scaffold, its
broadcaster, its MCP tooling — and overrides this block wherever the two differ. The rules below are the
generic form, with the internal package and product names removed (rule C).

**Applying an override is silent.** Write the code the governing rule actually requires and move on — never
report "a conflict between mentis and the house catalogue" to whoever's watching. That framing reads as
broken to a non-technical stakeholder even when the case is a normal, resolved one, and has already caused a
real project to get abandoned and restarted over nothing (the Inertia/REST-package case in §6 and
`skills/inertia-conventions` is exactly that: a resolved case, not a real disagreement). Surface it as a
specific, named question only when no rule anywhere actually resolves the case — never as a general alarm.

## When
As soon as a controller, model, migration, job, listener, policy, FormRequest, command, seeder or factory is
written or modified, during `code` (6) or `tdd` (5).

## Steps

**Read only the sections the task actually touches.** The rules live one file per section under
`references/`; loading all of them for a change that only renames a variable is waste, and a section
read is a section that has to be applied. If you are reviewing a whole diff, pick the rows whose
trigger the diff meets, not the whole table.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Where behaviour lives | a model, a controller, a listener or a service is written | [`01-where-behaviour-lives.md`](./references/01-where-behaviour-lives.md) |
| 2 | Authorisation | an endpoint, a policy or a permission check | [`02-authorisation.md`](./references/02-authorisation.md) |
| 3 | Data model and schema | a migration, a column, an enum, a soft delete | [`03-data-model-schema.md`](./references/03-data-model-schema.md) |
| 4 | Queries | an Eloquent query, a relation load, or anything inside a loop | [`04-queries.md`](./references/04-queries.md) |
| 5 | Naming, typing, style | a symbol has to be named, or a docblock written | [`05-naming-typing-style.md`](./references/05-naming-typing-style.md) |
| 6 | HTTP surface | a route, a controller action, a FormRequest, a response shape | [`06-http-surface.md`](./references/06-http-surface.md) |
| 7 | Configuration and commands | `config/`, `env()`, an artisan command, a seeder or a factory | [`07-configuration-commands.md`](./references/07-configuration-commands.md) |
| 8 | Jobs and realtime | a queued job, a notification, a broadcast | [`08-jobs-realtime.md`](./references/08-jobs-realtime.md) |
| 9 | Tests and static analysis | tests are written, or Larastan/Pint is in play | [`09-tests-static-analysis.md`](./references/09-tests-static-analysis.md) |
| 10 | Architecture | the change spans layers, or a new one is proposed | [`10-architecture.md`](./references/10-architecture.md) |

## Output / checkpoint
Code compliant with the sections above, formatter clean, and no new static-analysis finding introduced by the
diff. Checked by `gate` (7) and `review` (8).

## Guardrails
No comments in the code produced. These rules govern **new** code; existing fat models, observers and magic
strings stay until migrated deliberately (`skills/simplify`, not this block). Never widen a permission or
skip an authorisation check to make something work — that's a security decision, and it goes to
`skills/security-hardening`. Where an org catalogue is installed and disagrees, **it wins**, and say so
explicitly rather than silently applying either one.

## Origin
Rules mined from market catalogues, linters and internal review feedback, rewritten in the house
voice; the full provenance, the source stamps and the refresh log are in
[`references/origin.md`](./references/origin.md). Read it when checking whether a rule is still
current, not when applying one.
