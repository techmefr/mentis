# testing-library-query-pitfalls §3 — Structure and lint

How much of the component a test renders, and what it asserts on, decides whether the test survives a
refactor. The lint plugin turns the query and wait rules of §1 and §2 into checks.

## 3.1 Render the component fully
1. **Test the component from outside, as a user does**: render the whole UI, act on it, and assert that the
   rendered result behaves as expected. Avoid mocking, partial rendering and shallow rendering, which can leave
   bugs untrapped and make tests poke at internals (Goldberg's JavaScript testing best-practices guide, section 3.3).
2. **Replace a child with a fake only when it hurts**: a child that slows the test, such as an animation, or one
   that complicates the setup (same section).
3. **The limit is size.** Fully rendering a component with too many children makes a failure hard to trace and
   may be slow; write only a few tests on that large parent and more tests on its children (same section).
4. **Verify** (own guidance) with a break-it check: rename a private method or an internal state field of the component and
   confirm that no test fails.

## 3.2 Separate UI details from logic
1. **When a test is about component logic, UI details are noise.** Extract the wanted data from the markup in a
   way that is not tied to the visual structure, and assert on that data rather than on HTML or CSS details
   (Goldberg's guide, section 3.1).
2. **Disable animations that slow the test down** (same section). The pure result may be ready in 10 ms while
   the whole test lasts half a second because of an animation nobody asserts on.
3. **Do not skip rendering to get there.** The guide warns that testing only the back part of the UI, such as
   services, actions or the store, gives tests that do not resemble reality and miss the case where the right data
   never reaches the UI (same section).

## 3.3 Do not sleep
1. **Do not wait with a fixed delay.** A long sleep makes tests an order of magnitude slower and a short one
   fails when the component answers late, so it is a trade between flakiness and slowness (Goldberg's guide,
   section 3.4). The general rule and its virtual-clock exception are in `testing-anti-patterns` §3.
2. **Use the library's waiting**: `findBy*` and `waitFor` (§1.3, §2.1).
3. **Make the moment deterministic instead**: stub the slow resource so its response arrives at a known point
   and re-render explicitly, or advance a fake clock where the code under test sleeps (Goldberg's guide,
   section 3.4).
4. **When polling cannot be avoided and the framework offers no support**, a small helper that polls with a
   timeout is the fallback the guide mentions (it names a wait-for-expect package); the interval and timeout
   are explicit.

## 3.4 The lint set
The plugin `eslint-plugin-testing-library` ships configurations per flavour: Angular, DOM, Marko, React, Svelte
and Vue (as listed on its rule pages). Enable the rules below because each stands for a silent failure; they
are the rules the sections above rely on.

| Rule | Catches | Section |
|---|---|---|
| `prefer-screen-queries`, `no-container`, `no-node-access` | queries that bypass the user's view | §1.1 |
| `prefer-presence-queries`, `prefer-query-by-disappearance` | `get` and `query` used for the wrong claim | §1.3 |
| `prefer-find-by`, `await-async-queries`, `no-await-sync-queries`, `no-promise-in-fire-event` | async queries handled wrongly | §1.3 |
| `no-global-regexp-flag-in-query` | stateful regexps | §1.4 |
| `no-wait-for-side-effects`, `no-wait-for-multiple-assertions`, `no-wait-for-snapshot` | `waitFor` misuse | §2.1 |
| `await-async-events`, `prefer-user-event-setup`, `prefer-user-event` | unawaited or low-level events | §2.2 |
| `no-unnecessary-act` | silenced warnings | §2.3 |
| `no-manual-cleanup`, `no-render-in-lifecycle` | cleanup and render placement | §2.4 |

Two rules depend on the installed user-event version and must not both be on: `await-async-events` for v14 and
`no-await-sync-events` for earlier versions (§2.2). `no-test-id-queries` is deliberately absent: it is the
decision in §1.2. The plugin's rules about naming a render result and about preferring an explicit or implicit
assertion were not read, so they are left to the project.
