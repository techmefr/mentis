---
name: laravel-feature-test-pitfalls
description: "Use when writing or reviewing Laravel feature tests for HTTP endpoints (PHPUnit): the cases an endpoint needs (authentication, other tenant, insufficient permission, route constraint, validation, valid request with persisted state), 404 versus 403 for another tenant's record, testing the permission matrix at the policy and one refusal over HTTP, who owns the validation matrix (rule class versus endpoint), reporting defects found in the code before writing the test, framework fakes with class names, stray HTTP requests, time and randomness, and what makes a passing test worthless."
---

# laravel-feature-test-pitfalls

Step 5 of the pipeline (`WORKFLOW.md`), for the tests that exercise a Laravel application through its HTTP
layer. The three sections share one premise: **a feature test earns its place by the defect it would catch**,
so every rule is about which case catches which defect, at which layer it is cheapest to catch it, and what
makes a passing test say nothing. Test doubles in general and test smells are in `skills/testing-anti-patterns`;
which tier a test belongs to in a given project follows the project's own conventions first.

## When
- Writing the tests of a new or changed route, controller, form request, policy or middleware.
- A review has to judge whether an endpoint's tests are enough, or whether two layers test the same thing.
- A test depends on the clock, the queue, mail, an outbound HTTP call or random identifiers.
- A test passes but nobody can say what failure it would detect.

## Steps

**Read only the section the task meets.** They are independent.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Endpoint cases and authorization: the six cases, the real status of each, other tenants, the permission matrix, security boundaries | an endpoint's tests are planned or reviewed | [`01-endpoint-cases-and-authorization.md`](./references/01-endpoint-cases-and-authorization.md) |
| 2 | Validation, layers and reviewing: who owns the matrix, message assertions, reporting defects first, the review checklist | validation is tested, tests overlap, or a suite is reviewed | [`02-validation-layers-and-review.md`](./references/02-validation-layers-and-review.md) |
| 3 | Isolation and determinism: fakes, class names, stray requests, time, randomness, the database | a test fakes something, or fails depending on time or order | [`03-isolation-and-determinism.md`](./references/03-isolation-and-determinism.md) |

## Output / checkpoint
For each endpoint changed: the list of the six cases from part 1 with the test that covers each (or the reason
none applies), the status code each refusal returns, and the defects found in the code before the tests were
written, reported and not hidden by a test. Evidence is that every new test was seen failing once for the right
reason, by breaking the behaviour it covers, and that the tests pass in any order.

## Guardrails
- Never assert only a generic success code for a write; assert the response, the stored state and the side
  effects (part 2, point 5).
- Never answer another tenant's record with a code that confirms it exists (part 1, point 3).
- Never put the complete permission matrix in endpoint tests; keep it at the policy (part 1, point 4).
- Never delete or rewrite an existing test without being asked; report the duplication (part 2, point 3).
- Never create a fake without class names where the code dispatches known classes (part 3, point 2), and never
  let an outbound HTTP call reach the network in a test (part 3, point 3).
- Never use real time or a real sleep in a test (part 3, point 4).
- This block states the Laravel Boost testing rule files at the commit in
  [`references/origin.md`](./references/origin.md); the source also has a variant for another test framework
  that is not covered here. No test was run while writing it.

## Origin
Rewritten from the Laravel Boost testing rule files (MIT), PHPUnit variants only, read 2026-10-16. 🟡: never
run by us; open points are in [`references/origin.md`](./references/origin.md).
