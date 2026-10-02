# react-nextjs-conventions §11 — Testing components and hooks

> Section 11 of `skills/react-nextjs-conventions`. Read it when a component, a hook, a form or a data-fetching
> screen gets a test. What to test and the default-fail contract are `skills/tdd`; the ways a green suite lies
> are `skills/testing-anti-patterns`; end-to-end journeys are a browser tool's job (`skills/qa-exploratory-testing`
> for the manual pass). The other sections and the guardrails stay in `SKILL.md`.

1. **Test what the user sees and does.** A component test renders the component, acts on it as a person would
   (click, type, tab) and asserts on what a person perceives. It does not read state, count renders, check
   which hook ran or inspect props passed to a child. The measure of a good test is that a refactor which keeps
   the behaviour leaves it green; a test that breaks on a rename was testing the structure.
2. **Query by role and accessible name first.** The order of preference follows what assistive technology
   uses: role with its name, then label text for form fields, then visible text for non-interactive content,
   then alt text for images; the project's test-id attribute is the last resort for what has no accessible
   handle, and then it is a sign the element is missing a role or label. A test that finds a button by role and
   name also fails when the name is wrong, which a test id never does. Use the "query" variant to assert
   absence and the "find" variant for what appears later; the plain "get" variant throws when missing.
3. **Drive with the user-event library, awaited.** It simulates the sequence a browser produces (focus,
   key down, input, key up, click) where a bare dispatched event fires one synthetic event and skips behaviour
   such as focus moves and pointer-down side effects. Create the user object once per test and await every
   call, since each is asynchronous.
4. **Async content is awaited, never slept for.** Content that appears after a request or a transition is
   found with the asynchronous finder or a wait-for assertion, which retry until a timeout; an assertion
   written right after the action races the render. A fixed delay is the bet `skills/testing-anti-patterns`
   forbids. A warning that a state update happened outside the test's wrapper is a real finding (a state
   change nobody awaited), not noise to silence.
5. **The network is faked at the network layer.** A request-interception library installed once for the
   suite answers the component's real fetch code, with per-test overrides for the failing cases (a 500, an
   empty list, a slow response, a malformed body), reset after each test. Mocking the fetching hook or the
   client module skips the code that decides what the screen shows on failure, which is the code most likely
   to be wrong. Unhandled requests fail the test, so a new call is noticed.
6. **Server-state libraries get a fresh client per test.** The cache is shared state: create the query
   client inside the render helper with retries off, otherwise a cached answer from the previous test hides a
   missing request and a retry turns a quick failure into a timeout.
7. **One render helper wraps the providers.** The theme, the router, the query client and the i18n provider
   are composed once in a shared helper (with options to override a provider) and every test renders through
   it. Wrapping them by hand in each file is how two tests of the same component disagree about the locale.
8. **Hooks are tested through their public contract.** A hook with no rendering concern is exercised with the
   hook-rendering helper: call it, run state-changing calls inside the act wrapper, assert the returned
   values. A hook that depends on context gets a wrapper supplying it. If the hook is hard to test without
   half the application, it does too much.
9. **Do not mock the library you are testing against.** Mocking the framework's own hooks, or replacing
   child components by default, turns the test into one about the mock; render the real children and stub
   only the boundary (network, clock, storage, a heavy third-party widget with its own tests).
10. **Time is faked in the test, and restored.** Debounces, timeouts and polling are driven by the runner's
    fake timers, advanced by an exact amount inside the act wrapper, with real timers restored in teardown so a
    failing test does not leave the next one on a fake clock (`skills/testing-anti-patterns` §3.6).
11. **A snapshot is not the assertion for a component.** It records the whole tree, so reviewers approve it
    unread and it fails on any class rename. Use it for the output of a pure serialiser. For a component,
    assert the specific fact the test is named for; for appearance, use a visual comparison in a real browser
    on stable fixtures.
12. **Each screen state has a test: loading, empty, error, and the denied variant.** The happy path alone
    passes while the error branch renders a blank page (`skills/qa-exploratory-testing` §5 for the control
    inventory). Include the form's validation messages, the disabled state during submission, and the retry
    after failure.
13. **Accessibility is asserted at component level where a rule engine can.** An automated check on the
    rendered container reports missing names, invalid roles and label mismatches; it cannot judge contrast
    in an emulated DOM or the quality of focus order, which stay in the browser pass (`skills/accessibility`).
    Keyboard-only operation of the component is itself a test: tab to the control, activate it, assert the
    outcome.
14. **Server components and server actions are tested at their seams.** A server component that only
    fetches and composes is tested as an async function whose returned tree is rendered, with its data
    boundary faked; its client children are tested as ordinary components. A server action is a function with
    inputs, an authorisation check and a return value: call it directly with and without a session, assert the
    refusal and the validation errors, and leave the framework's wiring to an end-to-end test (§7).
15. **Pick one component-test environment and one runner.** Components run in an emulated DOM under the
    project's runner; anything needing real layout, scrolling, drag, clipboard or animation is moved to a
    real-browser test and not forced to pass in the emulator. Two runners in one repository means two
    configurations of timers, modules and globals to keep aligned.
16. **Coverage is a map of what no test touched.** Read it for the error branch and the state never rendered.
    This block sets no percentage, and a target is met by tests that execute lines without asserting
    (`skills/testing-anti-patterns`).
