# swift-testing §2 — Expectations

The Apple documentation pages for expectations, `#expect`, `#require` and the XCTest migration table, read
2026-10-08, with one MIT-licensed iOS testing skill for the failure-message rule. All of it applies to any Swift
Testing release; none is tied to an OS version.

## 2.1 `#expect` continues, `#require` stops
1. **`#expect` records an issue and the test keeps running; `#require` records an issue and throws.** Use `#require`
   for a precondition whose failure makes the rest of the test meaningless: an optional that must be non-nil before
   it is used, a collection that must have an element before the first is read.
2. **Unwrap with `try #require(optional)`,** which replaces `XCTUnwrap` and returns the value; a force-unwrap in
   test setup crashes the whole run instead of failing one test.
3. **Do not use `continueAfterFailure`.** The page explains that XCTest stops a test by throwing an Objective-C
   exception, which has undefined behaviour through Swift frames and in an async function can end the process and
   stop other tests from running; the testing library stops a test with a thrown Swift error from `#require`.

## 2.2 The expression is the message
1. **Put the expression inside `#expect`.** The macro captures the expression you pass and reports detail about it
   when it fails. Evaluating first (`let isValid = sut.validate(10); #expect(isValid)`) leaves the macro with a
   bare Boolean, and the failure says only that the expectation failed. Write `#expect(sut.validate(10))`, or
   compare directly so both sides are shown.
2. **Fix this independently of the framework-mixing problem.** A pre-evaluated Boolean stays a bad assertion after
   the framework is corrected (the MIT skill reports both findings separately).
3. **One concept per test and a name that states it.** The MIT skill asks for this and for display names that
   name the behaviour (`@Test("rejects an expired token")`); the Apple pages read do not state it.

## 2.3 Errors
1. **Assert that an error is thrown with `#expect(throws:)`,** for example `#expect(throws: (any Error).self) { try f() }`.
   The macro returns the thrown error, which the page's table binds to a constant for further checks
   (`let error = #expect(throws: (any Error).self) { try f() }`).
2. **Assert that nothing is thrown with `#expect(throws: Never.self)`.** A test that simply calls a throwing
   function with `try` fails on a throw too, but this form states the expectation.
3. **Record a failure that no assertion can express with `Issue.record("…")`,** the replacement for `XCTFail`; give it
   a message that names what was expected and what happened.

## 2.4 Known issues and skipped tests
1. **Mark a test that is known to fail with `withKnownIssue()` around the failing part,** so it stays in the suite
   without failing it; the page notes there is no equivalent of the unscoped `XCTExpectFailure` and that an
   intermittent known issue is declared as such.
2. **Skip a whole test or suite with the skipping trait, not by returning early.** The page describes a trait that
   decides before the test starts whether it runs. A test that is already running and cannot complete should end
   without failing through the cancellation function the page names for that case; through interoperability it also
   ends an XCTest function, so a helper can serve both frameworks.
