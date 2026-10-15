# api-contract-and-schema-fuzz-pitfalls §1 — Consumer contract tests (Pact JS, HTTP)

In a consumer-driven contract the API consumer writes a test that states what it needs from the provider, and that
test produces the contract. Facts are from the pact-js documentation at version 17.1.4; only the HTTP path was read.

## 1.1 The process
1. **The consumer unit-tests its own behaviour against a mock server provided by Pact.**
2. **Pact writes the interactions to a contract file,** a JSON document.
3. **The contract is shared with the provider,** through a broker or by another route, and replayed against a locally
   running provider (§2).
4. **Version-bound:** in this documentation `Pact` is the `PactV4` class, supporting up to version 4 of the Pact
   specification. The constructor's `spec` option is documented as a number with a default of 2, and the example sets
   the version explicitly; set it deliberately rather than relying on the default.

## 1.2 Test the real client
1. **Run the function your application uses to call the provider, against the mock server's URL.** The documentation's
   point: test the outbound collaborating function, not raw HTTP requests to the provider.
2. **Why:** it tests your actual running code, and the tests stay up to date with what the consumer really does. A test
   that issues its own requests checks the mock against itself and writes a contract the consumer may not honour.
   The second half is our reading of the documentation's reasoning.
3. **Point the client at the mock dynamically.** The mock server's URL is passed into the test callback and given to the
   client under test; the client is not configured for a fixed address.

```ts
await provider
  .addInteraction()
  .given('dogs exist')
  .uponReceiving('a request for the dogs added today')
  .withRequest('GET', '/dogs', (builder) => {
    builder.query({ from: 'today' });
  })
  .willRespondWith(200, (builder) => {
    builder.jsonBody(eachLike({ dog: 1 }));
  })
  .executeTest(async (mockserver) => {
    const client = new DogService({ url: mockserver.url });
    const response = await client.getMeDogs('today');
    expect(response.data[0]).to.deep.eq({ dog: 1 });
  });
```
The sample follows the documented builder shape; its names and values are ours and it was not run.

## 1.3 Interaction identity
1. **The combination of the state given and the scenario name must be unique in the contract file.** The documentation
   states it for `given` and `uponReceiving`.
2. **Name the state for the data the provider must have,** since the provider uses it to set up (§2.2), and the scenario
   for the request. Own guidance.

## 1.4 Clear the pact directory
1. **Clear the pact output directory before the tests run.** Otherwise outdated interactions stay in the contract.
2. **Pact does not clear it itself because tests may run in parallel,** which makes it hard to know when clearing is safe.
   The documentation says this is usually a problem only when you upload from a development machine, since CI rarely has
   old runs lying around.
3. **Duplicate or extraneous interactions in the contract usually mean this step is missing.**

## 1.5 Matchers instead of literals
1. **Use matching rules, not hard-coded values the provider must reproduce.** The documentation says matching makes tests
   more expressive and less brittle: type matches and regular expressions check the structure of the API.
2. **Matchers by spec.** The set depends on the specification version: the V3 and V4 matchers are the `Matchers`
   export, and the V2 ones are a separate `MatchersV2` export with a different API. This section covers V3 and V4 only.
3. **`like` applies a type match.** Around an object, all values and child object values match by type, unless a more
   specific matcher overrides one.
4. **`eachLike` matches every element of an array against the template** and requires at least one element by default,
   because otherwise the contents would never be matched. `atLeastLike`, `atMostLike` and `constrainedArrayLike` add bounds.
5. **`regex(pattern, example)` for a custom format,** and the typed matchers (`integer`, `string`, `boolean`,
   `timestamp`) where they fit. `equal` resets the matching rules that cascade down an object.
6. **`fromProviderState(expression, example)` for values the provider generates,** such as database identifiers that
   appear in a URL or query: the consumer test uses the example, and at verification the state handler's returned values
   fill the expression.

## 1.6 Return every promise
1. **A test that passes when it should fail almost always has a promise that was not returned.** The documentation's
   diagnosis: the call that returns a promise is not returned from the test block, so the test finishes green before the
   promise rejects.
2. **The same goes for the verification call inside a chain.** An unreturned `verify` suffers the same fate.
3. **Return the promise, or use `async` and `await`.**
4. **Intermittent failures have the same cause.** The documentation answers "test intermittent failures" with a pointer
   to this rule.
5. **Some frameworks report an unhandled rejection,** as the documentation notes; do not rely on it.

## 1.7 Testing error responses
1. **Most HTTP clients throw on a status of 400 or above.** With `await`, the throw happens before the assertion line is
   reached, so an `expect` after it never runs.
2. **Pass the promise to the assertion and return or await the result.** The documentation's forms: Jest's `rejects`
   matcher, or Mocha with chai-as-promised, `eventually.be.rejectedWith`.
3. **Add one interaction per error the consumer handles,** with its status and body, so the contract records what the
   client relies on. Own guidance.

## 1.8 Parallelism and environment
1. **A `Pact` instance is not thread safe,** but tests can run in parallel by creating one instance for each.
2. **Jest runs tests in parallel by default, which the documentation calls problematic because Pact is stateful;** run
   Jest in band, or follow the documentation's parallel-tests section, which was not read. It also asks for the Node test
   environment, because Jest's default browser-like environment may break libraries that make HTTP requests.
3. **A runtime without Node, such as a browser test runner, cannot host the mock server;** use a Node-based test framework.
4. **For diagnosing, set the log level to debug on the `Pact` object** to see the requests and responses as Pact sees them.
5. **Behind a corporate proxy, the mock server may be unreachable.** Pact checks that it can reach the mock service over
   HTTP before the tests run, and a proxy can intercept that call; the symptom is a message that the mock service does not
   appear to be running although it started. The documented fix is to set the proxy variables correctly and exclude the
   local address with the `no_proxy` setting.
