# llm-eval-regression-pitfalls §3 — Errors and retries

## 3.1 Error tolerance
1. **Decide how many sample errors a run tolerates.** Inspect's `fail_on_error` takes true (fail on the first),
   false (never fail), a proportion or a count. Failed samples are not scored.
2. **Use a strict setting where the run gates something,** and a lenient one while developing. Inspect lets
   the run-time call override the task's setting for this.
3. **`false` hides infrastructure failure** (own guidance). A run that never fails on errors can report a pass
   rate over a small surviving subset; read the count of errored samples in every report.

## 3.2 Retries and distribution shift
1. **Retries recover transient failures** and the original errors stay recorded with the sample.
2. **A retry can bias the result.** If an error depends on the input, such as a bug triggered by one class
   of cases, retried cases get more tries than others. Inspect's documentation warns of this distribution
   shift.
3. **Compare retried and unretried samples** before trusting a pass rate that includes retries, and report the
   number retried.

## 3.3 Errored samples
1. **An error can be a meaningful outcome,** for example an agent that crashes after producing partial state.
   Inspect can score an errored sample from the state reached, after retries are exhausted, and still counts it
   toward the tolerance for the run status.
2. **The scorer must cope with partial state.** If it raises on a missing output, the sample ends with an error
   and no score as before.
3. **State which choice you made** in the report (own guidance); scoring errors as failures and dropping them
   give different rates.
4. **A model refusal is not an error by default.** The sample continues and is scored on what the agent
   produced. A generation option makes refusals fail the sample, so they appear as sample errors and count
   toward the tolerance; the detail is on a page not read here.

## 3.4 Coverage and crashes
1. **Report coverage** (own guidance): scored, unscored, errored and retried samples next to the rate. The
   model-grading page says unscored results carry an undefined value that metrics exclude, and points to a
   scoring-policy page for how reduction over several epochs affects coverage counts; that page was not read.
2. **A crashed run is not a finished run.** After a crash the log is incomplete and unflushed samples are
   missing; Inspect can recover them from its sample buffer for a limited time after the process exits, so
   recover soon after.
3. **Do not let a retry loop run forever on hanging samples.** Inspect has an option to resolve in-progress
   samples as terminated rather than retry them, with a guard on how many may be treated that way, so a
   provider outage is not recorded as success. Own guidance: apply the same limit in any harness you write.
4. **Resolving stalled samples freezes every errored sample.** The documentation says finalisation records all
   samples that had already errored, within the tolerance, as errors instead of re-running them, and that it
   happens only when every expected sample is final and the metrics can be recomputed; otherwise the log stays
   retryable and the recovery command prints the reason.
