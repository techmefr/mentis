# api-contract-and-schema-fuzz-pitfalls §2 — Provider verification (Pact JS, HTTP)

The provider takes the contract and replays each recorded request against a running instance of itself. Facts are from
the pact-js documentation at version 17.1.4.

## 2.1 Verify against a running provider with its dependencies stubbed
1. **Start the provider locally and point the verifier at it** with its base URL, plus the contract files or a broker.
2. **Stub out the provider's own dependencies during verification,** so tests are fast and more deterministic. The README
   adds: stub any external dependencies before verifying.
3. **Run the verification as part of the unit test suite** where possible, so stubbing and other tooling are at hand; the
   README says this is best.
4. **Make it fail once on purpose.** Own guidance: change one contract expectation and confirm the verification goes red,
   so a green run means the provider was actually checked.

## 2.2 Provider states
1. **A state in the contract names data the provider must have.** The verifier calls the state handler for it before the
   request, and the handler puts the provider in the right state, for example by seeding a repository.
2. **Handlers are a map from state name to function** (`stateHandlers`).
3. **If the handlers are not configured, the verifier ignores the states in the contract and only logs a warning.** An
   interaction that needs data then runs against whatever is there, and fails or passes for the wrong reason, so treat
   that warning as an error. The last part is our reading.
4. **A handler can return a map of values** that the consumer's `fromProviderState` expressions use (§1.5), which is how
   database-generated identifiers reach the request.
5. **A state may be an object with `setup` and `teardown`.** Setup runs before the test and teardown after the request
   has been sent, for cleaning data that belongs to the state.
6. **Handlers receive parameters from the interaction** (for example an identifier), as the documentation's example shows.

## 2.3 The lifecycle
1. **For each interaction the order is:** the `beforeEach` hook, the state handler, the request filter on the request, the
   provider call, the request filter on the response, then the `afterEach` hook.
2. **If any hook or filter fails, the test fails.** Own guidance: keep hooks small and free of logic that can itself fail,
   since a failing hook is reported as a failing interaction.

## 2.4 Request filters
1. **Use a request filter only for what cannot be stored in the contract,** such as a short-lived bearer token.
2. **Modifying the request modifies what the consumer test recorded.** The documentation's warning: by changing the
   request you may be changing the contract from the consumer tests.
3. **Pair it with state handlers** that set or expire the token for the different cases, as the documentation shows
   ("is authenticated" and "is not authenticated").

## 2.5 Publishing results
1. **Publish verification results to the broker only from CI.** The documentation says to enable the flag only during CI
   builds, for example by testing the CI environment variable.
2. **Record the provider version** (the documentation recommends the commit hash) **and the branch** (recommended to set),
   so the broker can say which provider versions satisfy which consumer versions.

## 2.6 Re-running one failing interaction
1. **Version-bound (17.1.4 documentation):** set `PACT_DESCRIPTION` to select tests whose description contains the string,
   `PACT_PROVIDER_STATE` for those whose provider state contains it, and `PACT_PROVIDER_NO_STATE` to `TRUE` to select
   those with no state (documented for V3 only).
2. **Read the description and state from the failure list:** the failure output names an interaction as its description
   followed by "given" and the state, and the two parts go into the two variables.
3. **Diagnose with debug logging first.** On the verifier the `logLevel` option is documented as not used: the level is
   set by an environment variable, and the troubleshooting page shows `LOG_LEVEL=debug` for this.
