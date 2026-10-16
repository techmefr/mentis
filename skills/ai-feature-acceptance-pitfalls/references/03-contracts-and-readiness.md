# ai-feature-acceptance-pitfalls §3 — Contracts and readiness

A spec that says "the AI fills in the fields" hides the decisions that make a feature buildable. This section
covers the interface the feature exposes and the verdict on the spec itself.

## 3.1 Interface and data contracts
1. **One table per endpoint** for input and for output: field, type, required, notes on format and allowed
   values, plus a realistic example payload (source). Tables force every field to be named.
2. **Null has a meaning, and the meaning is written down.** The source's example distinction is "not
   applicable" versus "could not be determined"; ambiguous nulls are, in its words, a top cause of
   integration bugs.
3. **Field ownership**: for each field, which side produces it (the model service or the host system). The
   source says one column removes weeks of "I thought you were setting that".
4. **Identifiers, formats and versioning**: which id ties a request to its response and whether it is echoed
   back; dates, currencies, units and encodings stated once; how the contract changes without breaking callers
   (source).

## 3.2 Two kinds of failure
1. **System-level error**: the service cannot complete the call. Return a non-success status and an error
   code and no business fields; the caller falls back (retry, queue for a person, alert).
2. **Business-level warning**: the call succeeds, the usable fields come back, and a review flag with
   machine-readable reasons marks what needs a person. The caller routes to a human and keeps the partial
   result.
3. **A table for each**: code, trigger, service behaviour, handling downstream (source).
4. **Why the split matters**: merged, the system either hard-fails on recoverable problems or files bad data
   silently (source). The source calls this the most-skipped part of a spec.
5. **Edge inputs get a decided behaviour before build** (source): oversized or empty input, encrypted or
   corrupted files, wrong format, a missing upstream value the rule depends on, duplicate or retried requests,
   partial success.

## 3.3 Non-functional needs as numbers
1. **"Fast", "reliable", "secure" are not requirements.** Convert each into something a tester can check
   (source): a latency at a percentile and not an average, which hides the tail; a size limit and the error
   for anything larger; a timeout and the code it returns; an availability figure and what the client does in
   the remainder; for compliance, the named regime and the observable check.
2. **Write them as acceptance criteria**, so they are verified and not assumed. A requirement without a number
   is a deferred argument (source).
3. **The numbers are the team's.** The source's example values (a 500 ms p95, 100 MB, 30 s, 99.5 percent) are
   illustrations and are not carried here.

## 3.4 Readiness is not an average
1. **Two separate results**: how complete the spec is, and whether it can go to build (source).
2. **The second is a gate over the blocker items, not an average.** The source's gate: all blockers adequate,
   ready; all at least present but thin, ready with conditions to close first; any blocker missing, not ready.
   A spec can be mostly complete and still not ready.
3. **The blockers the source lists**: no one-sentence problem or no stated scope boundary; acceptance criteria
   that are missing, untestable or successful-path only; for an interface, no contract or no error taxonomy;
   for a model feature, no eval bar, no human fallback or an unlisted data dependency; a key risk or a
   blocking open question with no owner.
4. **Grade by severity and give a fix with each gap** (source): a blocker is separated from polish, and "the
   metrics are weak" becomes a named missing guardrail and the line that would add it.
5. **Say what the spec does well** (source). A review that only lists gaps does not calibrate the bar.
6. **Judge the latest version** of a spec with a history; deleted or struck-through requirements are not
   findings (source).
