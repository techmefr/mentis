# python-testing-strictness §3 — Fixtures and event loops

Two fixture failures hide until they cost something: a fixture whose setup fails halfway and leaves its
earlier work behind, and an async fixture that lives on a different event loop than the tests using it.

## 3.1 Safe teardown
1. **A fixture that makes several state changes loses its teardown if a later one fails.** The pytest
   documentation's example creates two users and sends a message in one `yield` fixture: if any setup line
   raises, the code after the `yield` never runs, and the earlier users stay in the system.
2. **One state-changing action per fixture, bundled with its own teardown.** Make each resource its own
   fixture (a user, a browser session) and compose them by requesting one from another. The documentation
   states that a successful action is then always torn down, because a failing step lives in a different
   fixture.
3. **Keep fixtures that fetch or build without changing state out of this rule:** the rule is about
   changes to something that outlives the test (a row, a container, a file, a remote account).
4. **The alternative is a finalizer registered right after each step** (`request.addfinalizer`), but the
   documentation calls it harder to maintain than splitting fixtures; use it when the steps cannot be split.
5. **After a test run, check that nothing was left behind:** leaked rows, containers and temporary
   directories are how this shows up, and they make the next run depend on the last.

## 3.2 pytest-asyncio: one loop per collector level
1. **The plugin provides one event loop per pytest collector.** By default each test runs in the loop of
   its function, the narrowest scope, which gives the highest isolation. A test can be put on a wider
   loop with the `loop_scope` argument of the `asyncio` marker.
2. **Neighbouring tests use the same loop scope.** The documentation recommends all tests in a class or
   module share one, and discourages mixing, because mixed scopes are hard to follow.
3. **The mode is decided once:** `strict` (the default) only handles tests carrying the marker and fixtures
   decorated with the plugin's fixture decorator; `auto` takes ownership of every async test and fixture and
   is recommended when asyncio is the only async library (`python-conventions` §8.20).

## 3.3 Async fixtures and the loop they run on
1. **A fixture created on one loop and used by a test on another fails at use**, typically with an error
   that a task or future is attached to a different loop. It happens when a `session`- or `module`-scoped
   async fixture (a client, a connection pool) is requested by function-scoped tests that run on their own
   loops.
2. **Give the fixture the loop scope its tests use:** `loop_scope` on the plugin's fixture decorator, or the
   default for all async fixtures with `asyncio_default_fixture_loop_scope` in the configuration. The
   test-side default is `asyncio_default_test_loop_scope`, which is function scope when unset.
3. **Set both defaults explicitly.** The documentation says the fixture default currently follows the
   fixture's own scope when unset and will change to function scope in a future version, so an unset value
   is a setting that will move under you. Valid values are `function`, `class`, `module`, `package` and
   `session`.
4. **A wide loop for a wide fixture is a deliberate trade:** tests sharing one loop share its pending tasks
   and state. Use it for expensive shared resources (a pool, a container client) and keep per-test state in
   function-scoped fixtures.
5. **Tests are run one after another on their loop,** not concurrently; sharing a loop does not make them
   parallel, so it does not need locking between tests.

## Verification
- A fixture was made to fail in its second setup step and the first step's resource was gone afterwards.
- A session-scoped async fixture is used by a function-scoped test with the configured loop scopes and the
  run has no different-loop error.
- Both loop scope defaults appear in the configuration block.
