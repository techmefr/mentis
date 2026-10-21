# architecture-fitness-functions-pitfalls §3 — Keeping the rules honest

> Part 3 of `skills/architecture-fitness-functions-pitfalls`. Read it when a rule passes suspiciously or the
> suite is reviewed. Source, read 2026-10-20: ArchUnit user guide, "JUnit Support", "Advanced Configuration"
> mentions and "Freezing Arch Rules" (Apache-2.0). Sentences marked "own guidance" are ours and rest on no
> source read.

1. **See the rule fail once.** Own guidance: after writing a rule, introduce a deliberate violation in a scratch
   change and confirm the build goes red with a readable message; then revert. A rule that never failed is a
   hypothesis. Symptom: a forbidden import exists in the code and the suite is green.
2. **Confirm it selects something.** Own guidance: a rule of the form "all classes that match P should satisfy
   Q" is true when P matches nothing. A renamed package, a wrong root or a moved module turns the rule into a
   vacuous pass without any error. Count the selected classes in the rule or in a companion check, and fail
   when the count is zero. The tool's current user guide (read 2026-10-20) says it fails a rule whose should-part meets an empty set of classes, with a global property to switch that off and a per-rule override to allow it; the guide does not say which version introduced it, so on an older pinned version test it and keep the count check.
3. **Say which code is analysed.** The JUnit support lets a test class declare the packages, classes or
   locations to import, and options to leave out test code and archives, and can cache the imported classes
   across tests. Own guidance: a rule applied to the wrong root, or to a cached import taken before a module
   was added, ignores new code. Declare the roots in one place and review them when a module is added.
4. **Give CI stricter store permissions than a laptop.** The guide notes that a CI build should probably never
   create a new violation store but work on the existing one, and shows how to forbid creation and updates by
   configuration or by a system property. Own guidance: otherwise a missing file turns into a fresh store that
   records every violation as known, and the build is green for the wrong reason.
5. **Run the rules where the code changes, early.** Own guidance: architecture tests belong in the ordinary
   unit-test phase so a violation appears in the same run as the change, not a night later. Keep them fast by
   limiting the analysed set to the project's own classes.
6. **One owner for the suite, and a review trigger.** Own guidance: name who edits the rules and when they are
   revisited: a new module, a split service, a change to the decision record. A decision revised in the record
   but not in the rule makes the build enforce a stale policy. Review the rule list when an ADR is superseded.
7. **Keep the rules independent of the framework.** The guide's rules are plain test code, which is why they can
   be refactored, unit-tested and run in any environment that runs tests. Own guidance: do not bury a rule in a
   build plugin configuration nobody reads; a failing rule should be a test someone can open and read.
8. **Report the trend.** Own guidance: the number of known violations, the number of rules and the number of
   waivers (ignore patterns) are three figures worth a line in each architecture review. A rising waiver count
   with a flat rule count means the rules are being worn down.
9. **Do the same for non-Java code with the tool at hand.** Own guidance: every ecosystem has a dependency-rule
   or import-lint tool; the pitfalls above (empty selection, rule never red, store growth, blanket ignore, CI
   creating the baseline) recur unchanged, so carry the checks over rather than inventing new ones.

## Checks (own guidance)
1. Each rule has been seen red in a scratch change, and the selected set is non-empty and counted.
2. The CI configuration forbids creating the store and re-recording violations.
3. The rule list is revisited whenever the matching decision record changes.
