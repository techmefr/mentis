---
name: prisma-ops-and-test-hygiene
description: "Use when a Node service uses Prisma in production or its tests are being written or hardened: connection pool size and poolers, query logging and latency, replacing client middleware with extensions, reading generated migration SQL before it runs (renames, new required columns, enum changes, risky statements, expand and contract), and test hygiene for Node services (assert the five outcomes, port 0 for servers, event listener order and error events, no sleeping, realistic data, property-based and mutation testing)."
---

# prisma-ops-and-test-hygiene

Step 6 and step 7 of the pipeline (`WORKFLOW.md`), for two things that fail quietly: an ORM that runs in
production with defaults nobody chose, and tests that pass without proving anything. The sections are
independent. The Prisma section is **version-aware**: Prisma changed its pool defaults, removed client
middleware and moved datasource configuration between major versions, and a rule is stated with the
version it holds for. The principle for both: **look at what actually runs (the SQL, the pool, the
assertion) and not at the line that was written**.

## When
- A Prisma-backed service goes to production, is moved to serverless, or opens too many connections.
- A migration was generated and is about to be applied to data that matters.
- Writing a test for a Node server, an event emitter, or a handler with several effects.
- Coverage is high and bugs still ship.

## Steps

**Read only the section the task meets.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Prisma operations: pool, logging, extensions, migration review by version | the client is configured, queried slowly, or a migration is applied | [`01-prisma-operations.md`](./references/01-prisma-operations.md) |
| 2 | Test hygiene for Node services | a test is written or reviewed | [`02-test-hygiene.md`](./references/02-test-hygiene.md) |
| 3 | Property-based and mutation testing | the suite's strength, not its size, is in question | [`03-property-and-mutation-testing.md`](./references/03-property-and-mutation-testing.md) |

## Output / checkpoint
Prisma: the SQL of each migration was read and its risky statements named before applying (§1.4), and the
number of connections was observed under load (§1.1). Tests: each new test was seen failing against a
deliberately broken implementation (§2.1). A migration applied from the generator's output unread, or a
test that never failed, is not verified.

## Guardrails
- Never apply a generated migration to shared or production data without reading its SQL (§1.4).
- Never read a rename as a rename: the generator may drop and add (§1.4.1).
- Never run a migration, reset or seed against a non-local database on your own: a human decision.
- Never assert on a mock's call count as the only evidence an effect happened (§2.1).
- Never fix a flaky test with a sleep (§2.4).
- The Prisma claims are tied to the major version named in each rule; the newest major documents a
  different migration workflow, and the pre-existing SQL-file workflow was checked against a skill
  catalogue, not the version-matching official page. Verify against the version the project is on.
- Nothing was run while writing this block.

## Origin
Rewritten from the Prisma documentation (pool, logging, upgrade guide), one MIT agent-skill on Prisma
migration review, one MIT JavaScript testing-practices repository, the fast-check and Stryker
documentation, and the Node.js API documentation (events, net). 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
