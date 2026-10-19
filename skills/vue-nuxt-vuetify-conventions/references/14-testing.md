# vue-nuxt-vuetify-conventions §14 — Testing components, composables, stores and Nuxt

> Section 14 of `skills/vue-nuxt-vuetify-conventions`. Read it when a component, a composable, a store, a
> route or a server handler gets a test. What to test and the default-fail contract are `skills/tdd`; the
> ways a green suite lies are `skills/testing-anti-patterns`; this section is the Vue and Nuxt mechanics.
> The other sections and the guardrails stay in `SKILL.md`.

1. **A component is tested through its public interface and nothing else**: the props it receives, the
   events it emits, the slots it renders, and the DOM a user would perceive. Reaching into a component's
   internal refs or calling its methods couples the test to a structure the next refactor will change, and
   the test then fails for a reason that is not a bug. If the behaviour cannot be observed from outside, the
   component is hiding logic that belongs in a composable.
2. **Mount fully by default; stub on purpose.** A full mount exercises the contract between parent and
   child, which is where most component bugs live. A shallow mount replaces every child with an empty stub
   and so cannot see a prop renamed on one side only. Stub the child that is expensive, that talks to the
   network, or that is itself covered by its own test, and say which one in the test, so the reader knows
   what was not exercised.
3. **Every interaction and every prop change is awaited.** Triggering an event, setting a value or changing
   a prop returns a promise because the DOM updates on the next tick, not synchronously; an assertion
   written before the await reads the old DOM and passes or fails by accident. When the code under test
   resolves a promise chain (a mocked request, a store action), flush the pending promises before
   asserting. Waiting a fixed time instead is the bet `skills/testing-anti-patterns` forbids.
4. **Locate the way the project's selector contract says.** Where the project uses stable test attributes
   (`skills/tdd`), use them for anything that has no accessible role; where an element has a role and a
   name, query by those, because that query also fails when the accessible name is wrong, which a test id
   never does. One mechanism per project, not a mix chosen per author.
5. **Fake timers are installed per test and restored per test.** A debounce, a polling interval or an
   auto-dismiss is tested by advancing a simulated clock, never by waiting. A fake clock left installed
   leaks into the next test and into the framework's own scheduling, so the restore belongs in the shared
   teardown, not in each test's last line where a failing assertion skips it.
6. **State holders are isolated.** A component test that needs a store gets a test store from the store
   library's testing helper, which stubs actions by default so the component is tested against the store's
   interface; switch the stubbing off only for the test whose subject *is* the action. A store tested on its
   own gets a fresh instance activated before each test, because the default instance is process-wide and
   makes the second test depend on the first. Under a test runner without global spies the spy factory is
   passed explicitly.
7. **A composable that uses only reactivity is a plain function call**: call it, change the ref it took,
   assert the ref it returned. A composable that registers a lifecycle hook or reads an injected value is
   tested inside a minimal host component mounted for the purpose, and the test **unmounts** the host and
   asserts the cleanup (listener removed, timer cleared, subscription closed), because a leak is invisible
   until the component has been mounted a hundred times.
8. **Provide what the component injects, with the real key.** The mount option for provided values takes the
   same typed key the application uses (§15), so a renamed key breaks the test instead of silently
   injecting nothing. A component that injects a value and renders something sensible when the value is
   absent has two behaviours and gets two tests.
9. **The router is real or stubbed, never half-faked.** For a component that only renders links, stub the
   link component. For one that reads the route or navigates, create a router with in-memory history, push
   the starting location, await the router's readiness, then mount with it installed; a hand-made `$route`
   object omits the parts the code reads next month.
10. **The component library is installed in the mount, once.** A library component mounted without its
    plugin renders nothing useful or throws in a way that looks like a bug in the code. Install it (and the
    i18n plugin with the real locale messages, so the assertion reads the text a user reads) in the shared
    mount helper. The DOM emulator lacks some browser APIs the library uses (resize observation, media-query
    matching, a visual viewport); stub them once in the setup file, not in each test. Overlays, menus and
    dialogs teleport out of the mounted tree: attach the wrapper to the document and query the document, not
    the wrapper.
11. **Transitions are stubbed, and that is fine.** The test utilities stub the transition wrappers by default
    so assertions run without waiting for an animation. A behaviour that depends on the transition really
    running (a focus moved after it ends) is a browser test, not a component test.
12. **A snapshot is not an assertion about a component.** It records everything, so a reviewer approves it
    without reading, and it fails on a harmless class rename. Use it for the output of a pure serialiser;
    for a component, assert the specific fact the test is named for.
13. **Assert the states the screen ships**: loading, empty, error, and the permission-denied variant, each
    from its own test. The happy path alone is the test that passes while the error branch renders
    nothing.
14. **One DOM emulator per project, chosen once.** The two common ones differ on layout, CSS support and
    some events, so a test that passes under one and fails under the other is information about the
    emulator. Anything that needs real layout (a sticky header, a virtual list's measured heights, a
    container query) is checked in a real browser, not forced to pass in the emulator.
15. **Accessibility is asserted where it can be**: an automated rule engine run on the mounted component
    catches missing names and invalid ARIA, and says nothing about contrast or focus order; those stay in
    the browser pass (`skills/accessibility`).

## Nuxt

16. **Two environments, kept apart.** A function with no Nuxt dependency runs in the plain test environment,
    which starts in milliseconds. Code that uses auto-imports, runtime config, state or the app context
    needs the Nuxt test environment, which boots the framework per file. Use one runner configuration with
    separate projects (unit, Nuxt, end-to-end) so the cheap tests stay cheap, and opt a file into the Nuxt
    environment explicitly rather than turning it on globally.
17. **Mount components that need the app through the suspense-aware helper.** A component with an async
    `setup`, a plugin-provided value or a route dependency must be mounted with the framework's helper for
    that, which resolves the async setup and injects the plugins; the plain mount renders a pending
    boundary and the assertion runs against nothing.
18. **Mock an auto-imported composable with the framework's import mock, not by module path.** The import is
    transformed at build time, so a module mock of the file misses the call site. The mock is hoisted: define
    the replacement inside the hoisting helper, and expect one mock per imported name per file. A component
    mocked by name replaces it for every mount in the file.
19. **Stub the backend at the endpoint.** The test utilities register a handler for a path (and method) that
    answers the framework's own fetch composables, so the component runs its real data path against a
    controlled response, including the failing ones (500, timeout, malformed body). A mock of the fetch
    composable itself skips the code that decides what the screen shows on failure.
20. **Shared state is cleared between tests.** `useState`, cookies and fetched payloads live in the app
    instance, which persists for the file. Clear the state in the shared teardown, or the test that runs
    second inherits the first one's login.
21. **Server handlers are tested twice, cheaply.** The decision logic is extracted into a plain function and
    unit tested; the route itself (input validation, status codes, the error shape, headers) is tested by
    booting the server through the end-to-end helper and calling it. A handler tested only by calling its
    function never runs the validator the router wires in front of it.
22. **The end-to-end helper is where SSR is proven.** The raw HTML response must contain the content a
    crawler and a first paint need, and a browser run over the same page must not log a hydration-mismatch
    warning (§9). Collect the console messages in the test and fail on that warning; it is a bug that every
    manual run scrolls past.
23. **Middleware is tested by navigating.** Route middleware runs during navigation, so the test navigates
    to the guarded path and asserts the resulting location, not by calling the middleware function with a
    fabricated route pair.
