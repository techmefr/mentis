# api-contract-and-schema-fuzz-pitfalls: origin and source stamps

> Provenance of `skills/api-contract-and-schema-fuzz-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from repository documentation, never run by us. No contract was written, no fuzzer was run
and nothing was installed while writing it. Open points are listed under "Not verified".

## Sources (re-read 2026-10-16, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| pact-foundation/pact-js (commit 9e07fea, 2026-10-13, version 17.1.4 in `package.json`): `docs/consumer.md`, `docs/provider.md`, `docs/matching.md`, `docs/troubleshooting.md`, `README.md` (each read in full; only the HTTP consumer and provider path was used) | MIT (repository LICENSE file, re-checked: "The MIT License (MIT)", original work DiUS) | The process, real client under test, interaction identity, clearing the pact directory, the V3 and V4 matchers, unreturned promises, error-response tests, parallelism, provider states, request filters, the lifecycle, CI-only publishing, re-running one interaction, the proxy symptom |
| schemathesis/schemathesis (commit 290178c, 2026-10-15, version 4.31.1 in `pyproject.toml`): `docs/faq.md`, `guides/triage.md`, `guides/cicd.md`, `guides/baseline.md`, `guides/crash-reproduction.md`, `guides/coverage.md`, `reference/checks.md`, `explanations/data-generation.md` (each read in full), and the `seed`, `continue-on-failure`, `baseline`, `phases.coverage.unexpected-methods`, `validate-formats`, `generation.deterministic`, `generation.allow-x00` and `generation.with-security-parameters` sections of `reference/configuration.md` plus `--seed` and `--generation-deterministic` in `reference/cli.md` | MIT (repository LICENSE file, re-checked: "MIT License", Kiwi.com) | What is generated, the destructive coverage probes and the setting that stops them, the auth probes, the first-run settings and their costs, baselines and their expiry, replay outcomes and credentials, seeds, exit codes, the JSON report gate, splitting runs |

Both documentation sets contain no agent directives. The Schemathesis pages were re-read in full for the files
named above; the rest of its documentation (stateful testing, hooks, extending, auth guide, Python apps and others)
was not read, and no rule depends on it.

## Rewrite notes
The three code blocks are small illustrations of documented shapes: the consumer builder sample (§1.2) follows the
documented builder API with our own names, the two configuration snippets (§3.2) are the documented key with our
choice of values, and the baseline entry (§3.5) uses the documented fields with our own reason and date. None was run.

**Version-bound facts, with their version:** Pact: `Pact` as `PactV4` supporting up to specification version 4, the
`spec` option documented with a default of 2, the V3 and V4 `Matchers` against the V2 `MatchersV2` export, the
`PACT_DESCRIPTION`, `PACT_PROVIDER_STATE` and `PACT_PROVIDER_NO_STATE` variables (all pact-js 17.1.4 documentation).
Schemathesis (4.31.1): the `phases.coverage.unexpected-methods` key and its default list, the `generation.*` and
`checks.response_schema_conformance.validate-formats` keys, `--baseline`, `--baseline-update`, `--baseline-prune`,
`--seed` and `--generation-deterministic`, the replay outcomes, and the exit codes.

**Decision where this repository differs from a source:** the Schemathesis baseline example carries a `ticket` field;
this repository has no tracker, so §3.5 shows `reason` and `expires` instead. `expires` is the one annotation the tool
acts on.

**Own guidance, not from a source:** the make-it-fail-once checks (§2.1.4), the naming advice for states and scenarios
(§1.3.2), the one-interaction-per-handled-error advice (§1), the small-hooks advice (§2.3.2), the CI check for the
unexpected-methods setting (§3.2.6), the statement that documented destructive operations are exercised and need
disposable data (§3.2.7), and the reading of the stricter-server finding (§3.1.4), plus every cross-link.

## Removed or corrected from the review item
1. **Not carried, as outside the HTTP consumer and provider path or as product operation:** messages, plugins, GraphQL, XML
   and multipart, pending and WIP pacts, consumer version selectors and tags, can-i-deploy, the broker's authentication
   options, the V2 matcher section (including its remark on the regular-expression dialect), and installation and
   platform troubleshooting.
2. **Not carried from Schemathesis:** the Allure and HTML report integrations, TraceCov coverage reporting and its
   reading-the-percentage advice, stateful testing and its checks, hooks, extending, the Docker and GitLab file snippets,
   and the optimisation guide.
3. **Completed:** the review item listed DELETE, PUT, PATCH, POST and TRACE for the undeclared-method probes. The triage
   page also names OPTIONS and QUERY for a path documented only for GET, and the configuration default lists eight methods
   including get; §3.2 uses those lists.
4. **Corrected:** the item gave "records branch and version" for the provider as an unconditional rule; the documentation
   marks the branch as recommended to set and the version as required to publish results (§2.5).
5. **Cross-links not made:** `nestjs-reliability` was checked and does not cover contract tests, so it is not linked.

## Not verified
1. **Pact beyond HTTP**, the broker, and the "parallel tests" section that the troubleshooting page points to.
2. **Whether the mock server stays stateless across tests** in your runner; the not-thread-safe remark is the
   documentation's only statement.
3. **Schemathesis behaviour under versions other than 4.31.1,** including whether the default method list or the
   `unexpected-methods` key persists.
4. **Whether a given framework routes undeclared methods to a real handler.** The documentation says a catch-all or a
   permissive router does; testing your own API for that was not done here.
5. **Stateful-phase requests:** the stateful phase and its DELETE-then-read checks were not read beyond the checks page,
   so the destructive-request advice rests on the coverage-phase page and the generic statement that all documented
   operations are exercised.
6. **Interaction of baselines with pending changes** such as a schema change that renames an operation was not read.

## Related blocks
`api-design`, `testing-anti-patterns`, `flaky-test-triage-pitfalls`, `playwright-e2e-pitfalls`.
