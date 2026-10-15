# analysis-validation-pitfalls §4 — Delivery and reproducibility

A correct analysis can still fail at delivery: the finding buried, the assumptions invisible, the work
impossible to redo. This section is what the reader needs beyond the number.

## 4.1 Lead with the finding
1. **Burying the lede**: the key finding on slide 8 after five slides of method. State the headline in the
   first paragraph and let the detail follow (nimrodfisher).
2. **Missing the "so what"**: pair every finding with a recommended action, or with an explicit statement
   that no action is needed (nimrodfisher).
3. **Titles state the insight, not only the metric**, and give the date range (anthropics).
4. **Conclusions stay inside the data**: alternative explanations are acknowledged, uncertainty is
   communicated, and the confidence level matches the strength of the evidence (anthropics validate-data).
5. **Unexpected findings are flagged, not suppressed** (nimrodfisher).

## 4.2 Assumptions and caveats
1. **Undocumented assumptions are invisible** to reviewers and stakeholders (nimrodfisher). List each one in
   its own section and mark the ones to which the result is most sensitive.
2. **Verify each assumption has a source** and, where it is uncertain, that the output was tested against
   a different value (nimrodfisher's process).
3. **Caveats are written for the reader**: limitations that change what they should do come before the
   chart, not in a footnote (own guidance, built on the "required caveats" of the verdict in §1.4).

## 4.3 Make it reproducible
1. **Someone else can recreate it from what is written.** The anthropics documentation standard asks for:

   ```
   Question:               the specific question answered
   Data sources:           table (as of date) | file (where from)
   Definitions:            each metric | each segment | period and timezone
   Methodology:            numbered steps
   Assumptions / limits:   each, with its likely impact
   Key findings:           each with its evidence
   Queries:                all of them
   Caveats:                what to know before acting
   ```
2. **Keep the queries, in version control or a shared document system**, with the date of the data snapshot
   (anthropics). `business/data-analytics` §4 point 5 makes the same point for figures quoted in messages.
3. **When an analysis is re-run on newer data, record what changed and why**, and link earlier versions of a
   recurring analysis so trends stay comparable (anthropics).
4. **For reusable code, a header states** the purpose, the assumptions (what "active" means, which accounts
   are excluded, the timezone), the output, and when it was last validated against what (anthropics' example
   header).

## 4.4 Charts, briefly
1. **Bars start at zero**, axes are labelled, scales are consistent across panels, and the title describes
   what is shown (anthropics, nimrodfisher).
2. **Distortions to look for**: truncated axes, inconsistent intervals, 3D effects (anthropics).
3. **Chart type should match the data story** (nimrodfisher's checklist). Encoding and chart choice are not
   covered further here.
