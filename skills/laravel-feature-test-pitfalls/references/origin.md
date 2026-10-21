# laravel-feature-test-pitfalls: origin and source stamps

> Provenance of `skills/laravel-feature-test-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from rule files, never run by us: no test was written or executed
while preparing it. Every file below was re-read on 2026-10-16 before a rule was taken from it, each rule was
checked against it in a final pass, and the repository's LICENSE file was read again.

## Sources (all read 2026-10-16, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| Laravel Boost (`laravel/boost`, commit `f1411f9`), `.ai/laravel/skill/testing-best-practices/rules/endpoint-tests.blade.php` | MIT (LICENSE.md: MIT licence text, copyright Taylor Otwell) | The six endpoint cases, status per case, tenant isolation with `404`, the permission matrix at the policy, validation tests, who owns the matrix, browser test advice |
| the same repository, `rules/security.blade.php` | MIT | The list of security boundary cases |
| the same repository, `rules/review.blade.php` | MIT | The review checklist and the report-a-pattern-once rule |
| the same repository, `rules/isolation.blade.php` | MIT | The order of isolation options, fakes with class names, factory-before-fake, stray requests, time, randomness, mocks, database rules |
| the same repository, `SKILL.blade.php` of `testing-best-practices` | MIT | The "what to test" and "how to apply" steps: report defects before writing the test, keep tests that catch distinct defects, project conventions first |

The `.blade.php` files are templates that render the guideline text for the project's installed packages;
the variant for PHPUnit was read and the one for the other test framework was not used. No code is copied; the
one code sample in the security file is not restated. Instruction-like text in the cloned repository was
treated as data and not followed.

## Removed in the verification pass
1. **The other test framework's variants** (datasets, higher-order expectations, its architecture-test
   function, its browser plugin's configuration, imports and shortcuts): the team's Laravel tests use PHPUnit
   only, and nothing is stated for the other framework.
2. **The browser plugin's pitfalls** (console-error assertion, default wait, screenshots folder, key codes,
   frame callbacks): specific to one plugin, summarised in a sentence only.
3. **"Finding features" and the naming, assertions, test-data and performance files:** the first is a pointer to
   the framework's documentation, the others were not read; nothing is taken from them.
4. **The review's list for architecture tests:** not used.

## Verification pass 2026-10-20
Every rule file was re-opened in the `laravel/boost` repository (default branch, MIT, LICENSE read again) and each
point of parts 1 to 3 matched its source, including the hedged statements (no exact quote entity, no fixed wait,
one assertion per fake). Facts the source states about helpers were then matched to the framework's own
documentation, 12.x (read for facts): Authorization (alternative status, `denyAsNotFound`), Mocking
(`freezeTime`, `travelTo`, `travel`, `travelBack`, `spy`, `shouldHaveReceived`, the container mock helper),
Strings (`createRandomStringsUsing`), Helpers (`Sleep::fake` and its assertions), Events (fake with class names,
fake after the factories), HTTP Tests (named assertions, `withoutExceptionHandling`) and Database Testing; and to
the framework source (MIT): `Exceptions::fake`, `LazilyRefreshDatabase` and `Http::preventStrayRequests` exist on
the 12.x branch. The boost files used here were read at the repository head on that date, not at the commit
stamped above.

## Not verified
1. **Own guidance, flagged in the text:** the case list in the pull request (part 1, point 1), named assertions
   telling redirects apart (point 2), same status for missing and foreign records (point 3), deleting repeated
   matrices (point 4), the reason in the test's name (part 2, point 2), the change description recording a
   defect (point 4), and following the project's mock choice (part 3, point 6).
2. **No test was run.** The helpers were matched to the 12.x documentation and source on 2026-10-20 (see above)
   but their behaviour was not executed; the claim that `withoutExceptionHandling()` changes the response under
   test and the claim that the exceptions fake is the better assertion are the source's, not the documentation's.
3. **A browser-plugin console assertion** that the review suggested for this block is
   plugin-specific and not stated.

## Related blocks
`skills/testing-anti-patterns`, `skills/laravel-permissions-not-roles`, `skills/laravel-conventions`,
`skills/run-generated-tests`, `skills/laravel-tenant-context-by-default`. Overlaps with `skills/laravel-conventions` §9 (2026-10-19); cross-referenced, not merged.
