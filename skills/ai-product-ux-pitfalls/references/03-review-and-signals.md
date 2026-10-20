# ai-product-ux-pitfalls §3 — Review and signals

Point 3.1.4 is confirmed against W3C WCAG 2.2 documents (see `origin.md`); the rest is own guidance.

## 3.1 Review in order
1. **Pick one real task and run it end to end** with a wrong model output injected (a fixture, not luck). Watch
   whether the person notices, how long correction takes, and whether anything irreversible happened.
2. **Run the failure states of §2.3 on purpose:** disconnect, return an empty result, return a refusal, delay
   the response. Each must leave the task doable.
3. **Read the screen as a stranger** (`persona-ux-audit`): can they say what the feature is for, what it cannot do,
   and which parts came from where.
4. **Check keyboard, screen reader and focus on streamed content.** Live updates that steal focus or are never
   announced exclude people; use the accessibility block for the checks and §2.2 point 4 here for the status-message criteria.
5. **Check the language of the output against the interface language** and what happens when they differ.

## 3.2 Signals in usage data
1. **Acceptance rate alone rewards over-reliance.** A high rate can mean good outputs or people not
   reading. Read it with edit distance after acceptance, reversals, later corrections and downstream errors.
2. **A low rate has two causes** (bad outputs, or users who do not trust good ones). Sample outputs and read
   them before concluding; measure ignoring, not only rejecting.
3. **Time to accept** shorter than reading time suggests no review for outputs of that length (a signal, not proof).
4. **Segment by stakes and by experience.** New users over-trust, experts under-use; one average hides both.
5. **Feed findings back** into the acceptance set and prompt changes (`ai-feature-acceptance-pitfalls`,
   `llm-eval-regression-pitfalls`).

## 3.3 Checks
1. The wrong-output drill and the failure-state drill were run and written down.
2. Acceptance is reported with at least one quality companion metric.
3. Findings reach the evaluation set, not only a backlog.
