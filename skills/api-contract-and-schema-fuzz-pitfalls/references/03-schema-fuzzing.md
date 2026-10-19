# api-contract-and-schema-fuzz-pitfalls §3 — Schema fuzzing (Schemathesis 4.31.1)

A schema fuzzer derives requests from the OpenAPI document and checks the responses against it. Facts are from the
Schemathesis documentation at version 4.31.1; configuration keys are version-bound, so check the version you run.

## 3.1 What it sends
1. **Three kinds of data:** examples from the schema, valid data that follows its constraints, and invalid data that
   deliberately breaks them. Some generated data may be rejected by your API if its validation rules are not expressed in
   the schema.
2. **Four phases contribute requests:** examples, coverage, fuzzing and stateful. An operation receives the sum of what the
   phases add, and all phases except examples send valid and invalid data by default.
3. **A failure triggers extra requests,** because each attempt to shrink the case to a minimal one is another request.
4. **A server that is stricter than the schema shows up as rejected valid-looking data.** The documentation's check for
   this is `positive_data_acceptance`; our reading is that the fix is to express the rule in the schema rather than to
   loosen the server.
5. **Invalid data that the API accepts is also a finding.** The `negative_data_rejection` check reports an API that took a
   schema-violating request.

## 3.2 Stop the destructive requests before the first run
1. **The coverage phase probes each documented path with the methods the path does not declare,** to confirm the API
   answers 405. A path documented only for GET also receives DELETE, PATCH, PUT, POST, TRACE, OPTIONS and QUERY.
2. **Disabling the `unsupported_method` check does not stop the requests.** It only decides whether the response is
   reported. If the framework routes an undeclared method to a real handler, through a catch-all route or a permissive
   router, a DELETE deletes, and the documentation says the run can still report that no issues were found.
3. **Disable the probing itself, with the version 4.31.1 setting:**

```toml
[phases.coverage]
unexpected-methods = []
```

4. **To keep the 405 coverage without the destructive methods, list only safe ones:**

```toml
[phases.coverage]
unexpected-methods = ["OPTIONS", "TRACE"]
```

5. **The default lists every method:** get, put, post, delete, options, patch, trace and query. An empty list disables
   unsupported-method testing entirely; the `allow_header_conformance` check reads the coverage phase's OPTIONS response
   and goes with it.
6. **Make it a precondition of the job, not a convention,** when the target is a shared environment. The documentation says
   so for CI; a check that fails the job when the setting is absent is our suggestion.
7. **Documented operations are exercised as well.** Own guidance, from the purpose of the tool rather than a quoted rule:
   a documented DELETE, PUT or POST receives requests too, so run the fuzzer only against an environment whose data is
   disposable or reset.
8. **The coverage phase also sends malformed multipart bodies and undeclared media types;** only server errors from these
   probes are reported.

## 3.3 Authentication probes are security tests
1. **The tool removes or alters credentials on purpose.** The documentation: it tests with no credentials and with wrong
   ones to catch APIs that accept requests they should reject, and some coverage cases omit required headers including
   authorization. This is not a bug in the tool.
2. **The `ignored_auth` check sends extra requests:** per operation, one without credentials and one with invalid
   credentials per security scheme, until the operation rejects them once. A `401`, a `403` or a redirect to a sign-in page
   counts as enforcement.
3. **If those requests trip a rate limit or a login lockout, exclude that check** (`--exclude-checks ignored_auth`).
4. **An explicit authorization header with credentials the schema's schemes do not declare gives no verdict.** The probes
   cannot remove them, so a successful response proves nothing, and an API that ignores the declared scheme is not reported
   for that operation while such a header is configured.
5. **Supply real credentials, then stop generating security parameters.** With the schema declaring a security scheme and no
   token supplied, the tool generates values and every protected operation answers `401`, hiding everything behind the
   auth wall. The setting is `generation.with-security-parameters = false`, and the flag alone with no real credentials
   makes every operation fail on `401` faster.
6. **Secrets may not reach the job.** In GitHub Actions, secrets are not passed to workflows triggered from forks, and in
   GitLab a protected variable is available only on protected branches; either shows as `401` everywhere.

## 3.4 Narrowing a first run, and what it costs
1. **A first run surfaces everything at once:** schema gaps, setup you have not supplied, and deliberate probes. Decide what
   is in scope.
2. **Four settings silence a whole class of finding everywhere,** including instances you have not seen:
   - `checks.response_schema_conformance.validate-formats = false` stops asserting `format` everywhere, so a malformed
     `uuid` or `email` passes too, and a `oneOf` that relies on `format` may resolve differently;
   - `generation.with-security-parameters = false` (§3.3);
   - `generation.allow-x00 = false` stops testing null-byte handling, which matters for anything that stores or forwards
     the string;
   - `phases.coverage.unexpected-methods = []` (§3.2) costs the 405 check and `allow_header_conformance`.
3. **Expect the remaining failures to differ, not only shrink,** because `401` responses mask everything behind them.
4. **After a clean run, switch each setting back on one at a time.** The documentation: each was suppressing a class of bug.
5. **To accept a known set of failures while keeping the check live, use a baseline** (§3.5) rather than disabling the check.
6. **Undeclared status codes dominate most first runs.** Add them in one pass where a pattern shows, in the framework's
   response annotations rather than in a generated schema file; the alternative to defer them is excluding
   `status_code_conformance`.

## 3.5 A baseline for known failures
1. **A baseline records accepted failures so CI fails only on new ones.** Capture it with `--baseline <file>`; if the file
   does not exist the run writes it. Put the path in the configuration file and commit the file.
2. **Once it exists, it changes only when you ask.** A plain run reads it and exits `0` for the recorded failures and `1`
   for anything else, so a regression has to be accepted deliberately.
3. **Generation is random, so each run may find new failures.** Fold them in with `--baseline-update`, using
   `--continue-on-failure` to find more per run, and repeat until a run records nothing new.
4. **Annotate entries, and give them an expiry.** Entries are yours to edit; the tool preserves what you write and acts only
   on `expires`: past that date the entry stops suppressing and the run fails with the entry named. An entry without one
   suppresses indefinitely. The documentation's example has a ticket field; this repository has no tracker, so use a
   reason and an expiry date.

```json
{
  "id": "2a5e5b",
  "operation": "POST /orders",
  "check": "not_a_server_error",
  "failure": "ServerError",
  "signature": "500",
  "reason": "division by zero when quantity is 0, fix planned",
  "expires": "2026-12-01"
}
```
The entry follows the documented fields with our own values; the `id` shown is the documentation's example.

5. **Do not edit `operation`, `check`, `failure` or `signature`:** they identify the failure, `id` is derived from them, and an
   entry with a changed value stops suppressing it.
6. **`--baseline-prune` removes an entry only when the run tested its operation and did not reproduce it.** Entries for
   operations the run never reached are kept, so a filtered or smaller run cannot delete the baseline. An entry that was
   not reproduced is reported as unobserved, which usually means the run did not reach it, not that it is fixed.
7. **What a baseline cannot hold:** for some failure classes one entry covers every failure of that class on that operation
   and status, so a different bug of the same shape there is suppressed too; and response-time failures are never recorded.

## 3.6 Reproduce, replay, seed
1. **Every failure ends with a block to reproduce it:** a `curl` command and a replay command with the case identifier.
2. **Replay re-sends the recorded cases and reports each as fixed, failed, flaky or error.** A case counts as fixed only after
   three consecutive clean replays; one that fails stops after the first, so checking a known-broken case costs no extra
   requests. After a fix, replay instead of re-running the whole suite.
3. **Run replay from the directory where you ran the fuzzer, with the same configuration.** The recorded cases live in a cache
   directory relative to the working directory, and from elsewhere replay finds nothing.
4. **Keep the cache directory out of version control.** The documentation: sensitive header, query and cookie values are
   replaced by default, but request and response bodies are stored as they were.
5. **A case that cannot be fully authenticated is never reported fixed.** If a masked credential is not supplied, or the API
   rejects the replay's credentials where the recorded request was accepted, the case is an error and the file is kept.
6. **For identical runs, fix the randomness.** The command line does not apply the `ci` Hypothesis profile that is loaded
   when a CI environment variable is set, so a run behaves the same locally and in CI. Use `--seed` with an integer, or
   `--generation-deterministic`, when two runs must match.

## 3.7 CI gating
1. **Exit codes:** `0` all checks passed, `1` at least one check failed or a bug was reported, `2` the tool could not run
   (configuration, schema or internal error) or nothing was tested, `130` interrupted.
2. **A run that tests nothing exits `2`,** for example when the schema has no operations or the filters match none. To
   distinguish it from a configuration error in a pipeline, write the JSON report and gate on the number of operations
   tested, and on the failure types for specific findings.
3. **Wait for the schema.** The `--wait-for-schema` option waits up to the given number of seconds for the API to start; inside
   containers the host name is the service alias, not `localhost`.
4. **Split a long run by resource, not through one.** A job given `GET /orders/{id}` without the operation that creates an
   order spends its budget on `404` responses and warns about missing test data. Keep create-and-read chains in one job and
   split on resource boundaries; give jobs on the same machine separate report directories.
