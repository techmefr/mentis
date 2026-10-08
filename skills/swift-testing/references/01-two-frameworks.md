# swift-testing §1 — Two frameworks in one target

The Apple documentation page "Migrating a test from XCTest", read 2026-10-08, with one MIT-licensed iOS testing
skill for the failure modes. The interoperability modes and their defaults need a Swift 6.4 toolchain; below that
the behaviour described in 1.1 point 2 applies.

## 1.1 Cross-library issues
1. **A cross-library issue is an XCTest assertion running inside a Swift Testing test, or a Swift Testing
   expectation running inside an XCTest case.** A shared helper that wraps `XCTAssertEqual` and is called from a
   `@Test` function is the usual way to create one.
2. **What happens to it depends on the interoperability mode, and the mode depends on the toolchain.** The page
   defines four modes: `none` (both sides ignore cross-library issues), `limited` (issues from Swift Testing keep
   their severity, issues from XCTest become warnings with a hint to modernise), `complete` (all keep their
   severity) and `strict` (XCTest issues are fatal errors). The defaults: a toolchain below 6.4 uses `none`; a 6.4
   toolchain with a package tools version below 6.4 uses `limited`; a 6.4 toolchain with a package tools version of
   6.4 or later uses `complete`. So on an older toolchain a failed assertion of the other framework is silently
   dropped and the test is green.
3. **Choose the mode on purpose.** The environment variable `SWIFT_TESTING_XCTEST_INTEROP_MODE`, set to the mode's
   name before the tests run, selects it. Use `complete` to make XCTest failures inside Swift Testing tests count as
   failures. Read the toolchain and the tools version before trusting a green run of a mixed suite.
4. **Do not rely on a third-party assertion helper that calls `XCTAssert` underneath** from a Swift Testing test
   until you know the mode: keep those tests in an `XCTestCase`, or wrap the helper's result in a native
   expectation. The MIT skill adds that a TCA test store needs a release that reports failures through the new
   framework; that version was not checked.
5. **A test method should have one framework's markers.** A method that carries both the `test` name prefix of
   XCTest and `@Test` can run twice, once under each framework (the MIT skill; not confirmed on the page).

## 1.2 Migrating a class
1. **A file may contain both kinds of tests;** import both modules when it does. Migrate one file at a time and keep
   test-support changes out of the production change.
2. **Remove the `XCTestCase` conformance to make a suite.** The page recommends a struct or an actor over a class,
   because the compiler can then enforce concurrency safety.
3. **A test function is any function marked `@Test`;** its name no longer has to start with `test`. Free functions
   and static members can be tests, so a suite is only a way to group them. The `@Suite` attribute is optional on
   a type.
4. **Replace `setUp` and `tearDown` with `init` and `deinit`.** `init` may be `async` and `throws`. If teardown is
   needed, make the suite a class or an actor and write `deinit`.
5. **Map assertions mechanically,** from the page's table: `XCTAssertEqual(x, y)` to `#expect(x == y)`,
   `XCTAssertNil(x)` to `#expect(x == nil)`, `XCTAssertThrowsError(try f())` to
   `#expect(throws: (any Error).self) { try f() }`, `XCTAssertNoThrow` to `#expect(throws: Never.self) { try f() }`,
   `try XCTUnwrap(x)` to `try #require(x)`, `XCTFail("…")` to `Issue.record("…")`. There is no equivalent of
   `XCTAssertEqual(_:_:accuracy:)`; compare numbers within a tolerance with `isApproximatelyEqual()`.
6. **Keep UI automation and performance measurement on XCTest.** The MIT skill's decision tree keeps XCUITest and
   `measure {}` there; the page read does not discuss them.
