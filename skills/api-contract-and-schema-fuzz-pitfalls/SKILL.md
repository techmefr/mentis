---
name: api-contract-and-schema-fuzz-pitfalls
description: "Use when an HTTP API is tested with consumer-driven contracts (Pact JS, HTTP path only) or fuzzed from its OpenAPI schema (Schemathesis 4.31): the consumer test calls the real client, interaction identity, clearing the pact directory, matchers instead of literals, returned promises, error responses, provider states and verification lifecycle, publishing results only from CI, and, for schema fuzzing, the destructive coverage probes that survive disabling a check, auth probes, narrowing a first run, baselines, replay, seeds and CI gating."
---

# api-contract-and-schema-fuzz-pitfalls

Step 5 of the pipeline (`WORKFLOW.md`), for two ways to test an HTTP API against a written contract. The three
sections share one premise: **a contract test proves something only if it exercises the real client and the real
provider, and a schema fuzzer sends every request the schema allows, including the ones that change data**. Where the
contract itself comes from and how it evolves is in `api-design` §1; the doctrine on doubles that test themselves is in
`testing-anti-patterns` §1, and the flake rules for a fuzz run that varies are in `flaky-test-triage-pitfalls`.

Scope: Pact is covered for the **HTTP consumer and provider path only** (pact-js 17.1.4 documentation); messages,
plugins, GraphQL, XML and broker administration were not read. Schemathesis is covered as of **version 4.31.1**; its
configuration keys are version-bound.

## When
- Writing a consumer test that produces a contract, or a provider verification that replays one.
- A contract test passes but should fail, fails intermittently, or the contract file has duplicate or stale interactions.
- Pointing a schema fuzzer at an environment, or adding it to CI.
- A fuzz run reports hundreds of failures on day one, every request answers 401, or data disappeared after a run.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Consumer tests: real client, interaction identity, pact directory, matchers, promises, error responses, parallelism | a consumer contract test is written or misbehaves | [`01-consumer-contracts.md`](./references/01-consumer-contracts.md) |
| 2 | Provider verification: running provider, states, lifecycle, request filter, publishing results, re-running one failure | a provider verifies a contract | [`02-provider-verification.md`](./references/02-provider-verification.md) |
| 3 | Schema fuzzing: what is sent, the destructive probes, auth probes, first-run narrowing, baseline, replay, seeds, CI | a schema fuzzer is pointed at an API or into CI | [`03-schema-fuzzing.md`](./references/03-schema-fuzzing.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: the consumer test was made to fail by changing what the client sends
and went red (§1.2), a deliberately wrong interaction made the provider verification fail (§2.1), and the fuzzer
configuration was checked before the first run against anything with data: the coverage method list was empty or safe
and the environment was disposable (§3.2). A contract test that has never been seen failing is not verified.

## Guardrails
- Never write a consumer test that issues raw HTTP requests instead of calling the real client (§1.2).
- Never leave a promise in a contract test unreturned or unawaited (§1.6).
- Never publish verification results from a developer machine (§2.5).
- Never run a schema fuzzer against data you care about before the unexpected-methods setting is empty or safe (§3.2).
- Never treat disabling the unsupported-method check as stopping the requests (§3.2).
- Never disable a fuzzer check to hide a failure you mean to fix later; use a baseline with an expiry (§3.6).
- This block states what the documentation describes at the commits in [`references/origin.md`](./references/origin.md).
  Version-bound facts name their version. Nothing was run while writing it.

## Origin
Rewritten from the pact-js documentation (consumer, provider, matching and troubleshooting pages, MIT) and the
Schemathesis documentation (FAQ, triage, CI, baseline, replay, coverage, checks and configuration pages, MIT), read
2026-10-16. 🟡: never run by us; open points are in [`references/origin.md`](./references/origin.md).
