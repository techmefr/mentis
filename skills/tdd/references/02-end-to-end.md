# tdd §2 — End-to-end tests

> Section 2 of `skills/tdd`. Read it when the acceptance criteria describe a journey a user performs through a
> real interface (a browser, a mobile shell, a command line) and a unit or integration test cannot show it. The
> sections here are driver-neutral; Playwright is the house default for browsers, and where a project already
> runs another driver the rules still apply.

Which test layer catches which kind of defect, and how visual tests are kept stable, is `skills/frontend-testing`;
   this section is the journey layer only.

1. **Few, and only the journeys whose failure ends the release.** Sign-in, the main write, payment, the one path
   a business depends on. An end-to-end test is the slowest and most fragile layer; what a unit test can show, a
   unit test shows.
2. **Select elements by what the test owns.** A dedicated test attribute (`data-test-*`), or the element's role
   and accessible name when the page has them. Never by a styling class, a position in the tree or a text that
   marketing may reword. Where the page lacks the hook, add it in the same change; do not write around its absence.
3. **A page object per screen, assertions in the test.** The object knows how to find and use the screen; the test
   says what must be true. When the screen changes, one file changes.
4. **Each test owns its starting state.** It creates the data it needs, through an API or a seed, rather than
   through the interface it is not testing, and it does not depend on another test having run. Reuse a signed-in
   session instead of logging in through the form every time, and keep one test that does log in through the form.
5. **Wait on conditions, never on time.** Wait for the element, the response or the state the next step needs
   (`skills/testing-anti-patterns` §3). A fixed sleep is a flake with a delay.
6. **A flaky test is quarantined with its cause, not retried into silence.** Isolate it, write down the suspected
   cause, an owner and a date by which it is fixed or deleted. Automatic retries hide the nondeterminism that
   a user will meet in production. A quarantine list nobody reads is deletion with extra steps.
7. **Keep the evidence of a failing run and read it before concluding.** The trace, the screenshot, the video,
   the network and console logs the driver can record on failure. A failure is diagnosed from them, not guessed
   from the assertion message (`skills/gate` §8).
8. **Run against a build that looks like production**: the same bundle, the same configuration shape, the same
   kind of data. A journey that passes on the development server only proves the development server.
9. **Mock the world you do not own, not your own application.** A third-party payment or mail provider is
   replaced at its boundary; your own backend is what the test exists to exercise.
10. **Test behaviour under a failing dependency for the journeys that matter**: the request that fails, the slow
    response, the empty list. These are the states a happy-path script never visits (`skills/qa-exploratory-testing`).
11. **Accessibility rides along.** The same journey run by keyboard, and an automated accessibility check on the
    screens it crosses, catch what the visual run cannot (`skills/accessibility`).
