# flutter-conventions §13 — Testing state holders, doubles, time and flows

> Section 13 of `skills/flutter-conventions`. Read it when a state holder, a repository, a debounce, a
> golden or a device-level flow gets a test. Widget-level tests, finders, pumping and goldens' inputs are
> §10; this section is the part that §10 does not state. The other sections and the guardrails stay in
> `SKILL.md`.

1. **Pick the layer by what can fail, then the tool.** A pure function and a repository with a faked
   boundary are unit tests. A screen's behaviour per state is a widget test. A goldens test fixes a
   design-critical rendering. A flow across screens, navigation and the real platform is an integration test
   on a device or emulator. Each defect belongs to the cheapest layer that can show it, and a flow test is not
   written for what a widget test could assert.
2. **A hand-written fake beats a configured mock for anything with behaviour.** A fake repository holds its
   data in memory, honours the interface, and exposes a way to make the next call fail. A mock configured to
   return a canned value cannot be wrong in the way the real one can (an empty page, a partial update), and
   the tests that use it end up asserting the configuration. Generate or configure a mock only for a narrow
   outbound boundary where the call itself is the observable.
3. **The fake can fail on demand.** The failure branch is the one that ships untested: give the fake a field
   that makes the next call throw a chosen exception, and write the test that sees the error state, the retry
   and the recovery. A fake that can only succeed tests only the screen's good day.
4. **A state holder is tested as a sequence of states.** For a Cubit-style or event-driven holder, the test
   builds it with the fake, triggers one event, and asserts the list of emitted states in order, including the
   loading state before the result. A test that asserts only the final state misses the flicker, the double
   emission and the missing loading step. The holder is closed in teardown.
5. **A provider-based holder is tested through its container.** Build a container with overrides for the
   boundaries, read the provider (awaiting the future provider's value where it is asynchronous), assert, and
   dispose the container at teardown so subscriptions do not leak into the next test. Overriding a provider
   with a fake is the only substitution; reaching into the holder's internals is not.
6. **Time in a unit test is a simulated clock.** A debounce, a retry delay, a polling loop and a timeout are
   tested with the fake-async zone: schedule, elapse a duration, assert the count before and after the
   threshold. This is the exemption `skills/testing-anti-patterns` §3.6 describes: it cannot flake on machine
   speed, where a real delay can. A test that needs real wall-clock time is testing the platform.
7. **Streams are asserted by their emissions.** Collect the events the stream emits with a matcher that
   states the expected sequence, and complete or cancel the subscription in the test. Asserting on the first
   event and moving on leaves a second wrong event for production.
8. **Goldens are for stable, design-critical widgets only.** Each costs a binary file and a review, platform
   differences make them fragile, and an updated golden is approved by a person who sees an image, so use
   them for a small set of components whose pixels matter. The update command is run on purpose, for an
   intentional change, and the image diff is read in the review before the baseline is accepted.
9. **Integration tests cover the journeys that must not break.** Sign in, the purchase, the offline return:
   a handful, on the real platform, against a fake or staging backend selected by configuration, with
   explicit waits on visible conditions and not on durations. Their cost is why the count is small, and why a
   failing one is investigated, not retried.
10. **Test names state the behaviour and the condition.** "Returns null when the user does not exist" tells
    the reader what broke without opening the file; a name that repeats the method does not. The structure of
    the test directory mirrors the library (§10).
11. **Coverage is read, not targeted.** The report shows which lines no test touched, which is where to look
    for an untested failure branch, a state never reached, a catch never taken. This block sets no percentage.
    A number chosen as the objective is met by tests that execute lines without asserting (§10, point 16), so
    whoever sets a floor in the project states what it excludes, and a falling number in a review is read as
    a question about the diff.
12. **Every state transition has a test.** For a screen with loading, success, error and retry, the
    transitions between them (loading to success, loading to error, error to loading on retry) are each
    asserted, because the broken ones are the transitions, not the states.
