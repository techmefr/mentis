# python-testing-strictness §2 — Coverage

Coverage is a gate only if it can fail and only if it measures what ran. Both properties are checked by
doing, not by reading the configuration. The settings are coverage.py's.

## 2.1 Measure branches
1. **Turn branch measurement on (`branch = true`).** Line coverage says a line ran; branch coverage says
   both outcomes of a condition ran. A guard clause whose failing side is never exercised is fully covered by
   lines and untested.
2. **The threshold counts statements and branches together.** A `fail_under` of 90 with branch measurement
   on can pass at a lower branch-only rate, so read the branch column of the report when branches are the
   point, rather than trusting the total.

## 2.2 A threshold that can trip
1. **Set `fail_under` in the 80 to 90 band and ratchet it up, not to 100.** A 100 target pushes people to
   write assertion-free tests or exclude lines to reach it, which is the kind of test that `testing-anti-patterns`
   exists to catch. Lowering it is a project decision (`python-conventions` §8.7).
2. **Prove it trips once.** Run the suite with a threshold the code cannot meet (100 on a partly covered
   project) and confirm a non-zero exit. A gate that has never been seen failing may not be wired: a wrong
   source path or a data file never written both give a number that looks fine.
3. **Gate on non-zero, not on one exit code.** The tools disagree on the code they return for a coverage
   failure, and pytest uses a different one when no tests were collected.

## 2.3 Parallel and subprocess runs
1. **A parallel test run needs `parallel = true` and `relative_files = true`** in the coverage run settings:
   each process writes its own data file, and relative paths let files from different machines or
   directories be combined later.
2. **Subprocesses started by tests are measured only if enabled.** With coverage 7.10 and later this is the
   `patch = ["subprocess"]` run setting; without it, code that only runs in a child process reports as
   unexecuted, or the whole report comes back empty.
3. **Combine, then report once** (`coverage combine`, then `coverage report`) after a parallel run.

## 2.4 Several Python versions
1. **Do not apply the threshold in each version leg.** A branch that only runs on one version drops the
   total on the others, and every leg then fails even though the union passes.
2. **Each leg writes and uploads its own data file; one job combines them and applies the threshold.** The
   workflow side (unique artifact names, hidden files, the combine job) is `ci-workflow-hardening` §2.4.
3. **A version-specific branch is excluded or tested on the version that has it,** not excused by a lower
   global number.

## Verification
- The gate failed once on purpose, with the exit code recorded, and passes at the real threshold.
- The report lists the files you expect and branch columns are present.
- With parallel runs, combining produced one data file and a non-empty report.
