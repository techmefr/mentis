# jest-vitest-assertion-pitfalls §3 — Matchers, snapshots and mocks

A matcher that is too loose, a snapshot nobody reads and a mock that does not behave as written all give a
test that passes for the wrong reason. Rules from the two plugins are marked by runner.

## 3.1 Strict equality
1. **`toEqual` ignores keys whose value is `undefined`.** The plugin's example: `{ a: 'a', b: undefined }` equals
   `{ a: 'a' }` under `toEqual` and does not under `toStrictEqual`, which also checks the structure, so
   two objects with different keys no longer compare equal (`prefer-strict-equal`, eslint-plugin-jest).
2. **Decision:** use `toStrictEqual` where the presence of a key matters (a payload sent to another system, a
   stored record), and `toEqual` where it does not. The plugin pushes `toStrictEqual` everywhere; the blanket rule
   is a preference.
3. **For errors, neither is enough**: both compare only the message (§1.5).

## 3.2 Asserting a call
1. **A bare `toHaveBeenCalled()` does not check the arguments**, and the assertion is stronger with
   `toHaveBeenCalledWith(...)`. When some arguments are hard to check, `expect.anything()` or `expect.any(Date)`
   still enforces their number and position (`prefer-called-with`, eslint-plugin-jest).
2. **The exceptions the rule allows**: `.not.toHaveBeenCalled()` to assert a call never happened, and
   `toHaveBeenCalledTimes(n)` when the count is the point (`prefer-called-with`).
3. **A call assertion is still not a behaviour assertion.** Whether a mock was called as the point of the test is
   covered in `testing-anti-patterns` §1; this rule only strengthens a call check you have decided is needed.

## 3.3 Snapshots
1. **Keep snapshots short and inline.** Goldberg's guide (section 1.8) suggests 3 to 7 lines included in the test,
   not large external files, because a long document that the writer never read couples the test to thousands of
   values, and the title says nothing about why it failed. It allows long external snapshots for a schema rather
   than data, or for a document that rarely changes.
2. **A snapshot is only as good as its review**, so size is limited: the Jest rule flags a stored snapshot longer
   than 50 lines by default, with separate `maxSize` and `inlineMaxSize` options (`no-large-snapshots`,
   eslint-plugin-jest). The numbers are the plugin's defaults and a project example, not a measured threshold.
3. **No string interpolation inside an inline snapshot.** Interpolation prevents the snapshot from being updated;
   put a property matcher on the variable property instead (`no-interpolation-in-snapshots`, eslint-plugin-jest).
4. **Concurrent Vitest tests that take snapshots use the `expect` from the test context**, not the global one
   (`require-local-test-context-for-concurrent-snapshots`, eslint-plugin-vitest).
5. **Never snapshot inside a `waitFor` loop**: one snapshot is generated per loop. The reason and the Testing
   Library form are in `testing-library-query-pitfalls` §2.1.
6. **Verify** by reading the diff of the last snapshot update as if it were code; if it cannot be reviewed, shorten it.

## 3.4 Vitest: hoisting and typed mocks
1. **Vitest hoists `vi.mock`, `vi.unmock` and `vi.hoisted`**, and the plugin flags them wherever they look like
   runtime code: inside an `if`, or inside a test body (`hoisted-apis-on-top`, eslint-plugin-vitest). Own inference:
   the position in a block is misleading because the call is moved to the top of the file; write it at the top
   level of the file.
2. **`vi.fn()` without a type parameter has the type `(...args: any[]) => any`**, so a wrong call signature compiles.
   Give the signature as a type parameter (`require-mock-type-parameters`, eslint-plugin-vitest). The same rule can
   check `vi.importActual` and `vi.importMock` through `checkImportFunctions`.
3. **Use `vi.mocked(fn)` rather than casting `fn as Mock`**, which the plugin lists for `Mock`, `MockedFunction`,
   `MockedClass` and `MockedObject` (`prefer-vi-mocked`, eslint-plugin-vitest).
4. **Do not hand-import from `__mocks__`** (§2.4).

## 3.5 Jest versions
1. **Jest v30 removed the alias matcher names.** The `no-alias-methods` page notes that these aliases have been
   removed in Jest v30 and links the Jest issue; `toThrowError` is the alias of `toThrow`, and the called and
   returned matchers have `toHave...` canonical names (`no-alias-methods`, eslint-plugin-jest 29.17.0 docs). Use the
   canonical names; the rule's fix does it automatically.
2. **`jest.genMockFromModule` was renamed `createMockFromModule` in Jest 26 and removed in Jest 30**
   (`no-deprecated-functions`, eslint-plugin-jest). The rule reads the installed Jest version to decide what is
   deprecated.
3. **Check the project's Jest version before applying either rule**: both depend on it, and the Jest release
   notes themselves were not read.
