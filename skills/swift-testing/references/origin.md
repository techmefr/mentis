# swift-testing: origin and source stamps

> Provenance of `skills/swift-testing`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run on a real Swift project by us. No test was
compiled, no toolchain was installed and no interoperability mode was exercised while writing it.

**Fold-in note.** This block is meant to be folded into `swift-conventions` (a testing reference) when PR 118
lands and the Swift blocks are consolidated. It is standalone only so that it does not depend on a block that is
not yet on main.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Apple developer documentation pages for Swift Testing: migrating from XCTest, expectations, `#expect` and `#require`, testing asynchronous code, the confirmation function, parallelisation, suites and the time-limit trait | Apple proprietary (facts only, rewritten) | §1.1 points 1 to 3, §1.2, §2, §3.1, §3.2 point 4, §4.1, §4.2, §4.3 |
| Apple developer documentation pages for XCTest `fulfillment(of:timeout:enforceOrder:)` and `wait(for:timeout:enforceOrder:)` | Apple proprietary (facts only, rewritten) | §3.2 points 1 and 3 |
| One MIT-licensed iOS testing skill (its SKILL.md, anti-patterns checklist, Swift Testing framework, async and enterprise testing references) | MIT (LICENSE read, copyright 2026) | §1.1 points 4 and 5, §2.2 point 3, §3.1 point 4 last sentence, §3.2 point 2 mechanism, §3.3, §4.2 point 3, §4.3, §4.4 |

Apple pages were read through the documentation JSON that backs developer.apple.com, so only prose was available;
the names of functions and traits that sit in links inside sentences were lost, which is why the expectations reference describes the
skip and cancel APIs instead of naming them.

## Rewrite notes
The MIT skill is opinionated: it mandates Swift Testing for all new tests, a 90 per cent unit, 8 per cent
integration and 2 per cent UI split, and a severity label on every finding. Those are the author's policy and
were left out. Its claim that an XCTest assertion in a Swift Testing test, or the reverse, is "silently ignored" is
true only on the toolchains whose default interoperability mode is `none`; the Apple page defines newer defaults, so
§1.1 states the rule by mode.

## Not verified
1. **Toolchain thresholds.** "Swift 6.4" and the three default modes are the Apple page's table as of the date above.
   No toolchain was installed, and the page's table may move with later releases.
2. **`@Test` plus a `test`-prefixed method runs twice** (§1.1 point 5), the TCA release floor and the claim that
   UI automation and `measure {}` stay on XCTest (§1.2 point 6) are statements of the MIT skill only.
3. **The deadlock mechanism of `wait(for:)`** in an async method (§3.2 point 2) is the skill's; the Apple pages only
   say to prefer `fulfillment(of:)`.
4. **Clock helpers** named in §3.3 come from a third-party package that was not read or vetted.
5. **Dropped from the source list:** "the confirmation helper fails against any completion handler" stated as a
   universal (kept only as the bridge-with-a-continuation fix), "attachments need XCTest" (the Apple page read
   documents an attachments type in Swift Testing), snapshot, VIPER, TCA and UI-testing recipes, the test pyramid
   ratios, and "test names as `test_<method>_<condition>_<expected>`".
6. **Written by us, not sourced:** the advice to reproduce a flake with parallelism on, repeated, in random order
   (§4.1 point 3), the list of shared-state suspects in §4.1 point 2, and the checkpoint in Output.

## Related blocks
`testing-anti-patterns` (the general rules for tests that prove nothing), `jvm-test-infrastructure` (the same
discipline on the JVM: real dependencies, no sleeps), `swiftui-correctness` (view models that these tests drive).
