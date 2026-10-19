# testing-anti-patterns §6 — Regressions typical of code written by an agent

> Section 6 of `skills/testing-anti-patterns`. Read it when a bug is being fixed, when a diff written in
> one pass (by a model or by a person in a hurry) is reviewed, when a test is added after a defect, or when the
> author of a change is also its only reviewer. The other sections and the guardrails stay in `SKILL.md`.

The common root: the author's assumptions are present in the code **and** in the read-through that follows,
so a review in the same context repeats the mistake with confidence. A failing test needs no assumptions. The
patterns below recur often enough to be searched for on purpose.

1. **Mechanical checks come before the read-through, and the read-through comes from a fresh context.**
   Run the test suite, the type check and the build first; a failure there is a finding that needs no
   judgement. Then the review is done by a reader that did not write the change and has only the diff, the
   specification and the evidence (`skills/review`, and `skills/santa-method` when the stakes warrant two).
2. **Two paths to the same result, and only one got fixed.** Any behaviour with a sibling path is a place
   where the fix lands on one side: the real and the simulated backend, a feature flag on and off, cached and
   uncached, the synchronous and the queued variant, the web and the mobile client, the old and the new API
   version, the tenant-scoped and the global query. After a fix, search for the sibling and open it. The test
   that holds the line asserts the **same contract through both paths** (a parity test), so it fails when
   they diverge.
3. **A test that runs a path production does not.** A test mode that bypasses authentication, a repository
   replaced by a fake that returns more than the real one, a fixture that pre-populates the column the code
   forgot to select, a schema auto-created from the model so the missing migration never shows: each makes
   the test green on a code path that no user takes. For each test ask which lines of production code
   executed, and whether the assertion sits on the boundary the user crosses (the response, the row, the
   screen) rather than on an intermediate.
4. **A partial projection.** A field added to the model but not to the query's column list, the serialiser,
   the mapper, the resource or the form request is `null` or absent at the other end, and the unit tests of
   each layer are all green. A contract test lists every field the consumer needs and asserts each is
   present, not merely that a response arrived.
5. **An error state leaks into the success state, and the reverse.** The error flag is set and the previous
   data stays visible; the loading flag is cleared on success and not on failure; the failure of request A
   shows on the screen for request B; a cached result outlives the filter that produced it. The test runs
   the sequence failure, success, failure and asserts after each step that stale data is gone and the right
   state is shown.
6. **An optimistic update with no way back.** The interface changes first and the request follows; when the
   request fails, nothing restores the previous state, and the user sees something the server refused. The
   code captures the previous value before the change and restores it in the failure path, and the test uses
   a double that fails the request and asserts the restored state.
7. **A type assertion, a default or an empty catch hides the absence.** The cast that makes the compiler
   accept a possibly-null value, the fallback that substitutes `0` or `[]`, the `catch` that logs and
   continues: each turns a visible failure into a plausible wrong answer (`skills/gate` step 6). The test
   gives the code the absent value and asserts a failure, not a quiet result.
8. **A rename or a move that missed the strings.** The compiler follows identifiers; it does not follow a
   configuration key, a route name, a translation key, a queue payload for jobs already in flight, a cache
   key, a serialised record, a documentation reference or a test fixture. Before a rename is done, search the
   old name across every file type, including data that was written under the old name.
9. **The expectation was edited to match the output.** A red test turned green by changing the expected
   value, loosening the matcher or deleting the case is the commonest way a regression is hidden. The change
   to an existing assertion is explained by a change in the specification, not by the output; where the
   project installs a guard that flags edits to existing tests (`hooks/README.md`), it is on for this reason.
10. **One instance fixed, the class left.** The same mistake appears in several handlers, components or
    queries, and the fix lands where the report pointed. After fixing, search for the pattern, fix its other
    occurrences in the same change or list them with the reason they are left, and add the test at the level
    that covers the class.
11. **An API that does not exist in the installed version.** The code calls a method, an option or a flag
    that the version in the lock file lacks or has renamed; it type-checks against loose types or fails only
    at run time on that path. The type check with the strict settings, a run that reaches the line and a read
    of the installed version's documentation (`skills/source-freshness`) are the checks; the model's memory
    of the API is not.
12. **A near-duplicate instead of the existing function.** A new helper that does what an existing one does,
    with slightly different edge behaviour, is a divergence waiting to be fixed in one place only. Search
    before adding, and extend the existing one (`skills/writing-skills` makes the same point for blocks).
13. **The regression test is written where the bug appeared, and shown red.** Each fixed defect gets a test at
    the layer in which it showed, named for the behaviour it keeps; the test is run against the code **before**
    the fix to confirm it fails there, then against the fix. Coverage is not the measure: bugs cluster in the
    same few areas (authorisation, multi-path logic, state transitions), so the tests accumulate where the
    failures are, and the suite grows with what has actually broken.
