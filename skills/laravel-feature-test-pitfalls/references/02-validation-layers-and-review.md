# laravel-feature-test-pitfalls §2 — Validation, layers and reviewing

> Part 2 of `skills/laravel-feature-test-pitfalls`. Read it when validation is tested, tests overlap, or a suite
> is reviewed. Sourced from `.ai/laravel/skill/testing-best-practices/SKILL.blade.php` and `rules/endpoint-tests.blade.php`
> and `rules/review.blade.php` in `laravel/boost` (commit `f1411f9`), read 2026-10-16, the variant for
> PHPUnit. Sentences marked "own guidance" are ours.

1. **Write one test per rule when each failure is a separate contract; one empty-payload test for the required
   fields together.** The source's validation rules: test the message the user receives, since a message that
   is present but wrong is a defect, and use a data provider (`#[DataProvider]`, or `#[TestWith]` for a few
   values) for inputs that need the same setup and the same assertions.
2. **Send the invalid value through the application; do not assert the rules array.** The source says an
   assertion that an array of rules contains a string tests the declaration and not the behaviour; keep such an
   assertion for a rule no request can reach, with the reason written in the test (own guidance: in the test's
   name, since comments are not allowed in our code).
3. **The rule class owns the matrix; the endpoint keeps one case.** The source: the test of the rule class owns
   the table of values that pass and fail, and the endpoint test proves that the endpoint applies the rule and
   that the user receives the message. When both hold the matrix, move it to the rule-class test and keep one
   case at the endpoint, and never remove the last one, because the rule-class test still passes if the request
   forgot to apply the rule. The same split applies to policies, scopes and other classes a request calls. The
   source's rule for existing tests: keep every test that can catch a distinct defect, trim a duplicate at the
   higher layer to the one case that proves the wiring, and report the duplication instead of deleting
   anything unasked.
4. **Report the defects in the code before writing the test.** The source's order of work: read the code and
   the neighbouring tests, list every decision in the code (a branch, a validation, a calculation, an
   authorisation), report defects first (its examples: a method with no body, a policy that no action calls, a
   write action with no validation), then test the actual behaviour and tell the user. Own guidance: a test that
   enshrines a defect as expected behaviour makes it expensive to fix later, so the report goes into the
   change description.
5. **A write test asserts three things.** The response, the state in the database and the side effects. The
   source's review list also asks for expected values that are known values and not computed with the
   implementation's own logic.
6. **Read the project's convention before the source's.** The source says a pattern repeated in the project is
   a convention and takes precedence over its rules; follow it for new tests, and do not delete or rewrite an
   existing test merely because it conflicts. If the convention has drawbacks, explain them and let the
   owner decide.
7. **Review checklist, shortened.** Each test covers observable behaviour and still passes after an
   implementation change that keeps the behaviour; none asserts the framework's own behaviour (what this
   project configures, such as a relation with a constraint, a cast, a scope, does belong to it); each catches a
   defect no other test catches; every changed decision and each applicable high-value failure has coverage.
   Names state a result, the condition and, for an API error, the status code; a file is named after the class
   it tests, with the class's relative path. HTTP tests cover authentication, authorisation, role, scope and
   validation where they apply; each validation rule has one test asserting the user-visible message; a
   `setUp` holds configuration only; each factory state and relationship gives the data a meaning; each call
   to `make()` is in a test that does not need the database; time, randomness, sleep and outbound HTTP are
   controlled; each test passes alone and in any order; comparisons use `assertSame()`.
8. **Report a pattern once.** The source's review rule: report each finding, and when a problem appears across
   the suite as a convention, report the pattern once rather than once per file.
