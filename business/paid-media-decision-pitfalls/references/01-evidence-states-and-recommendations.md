# paid-media-decision-pitfalls §1 — Evidence states and what a recommendation owes

An account review fails in a predictable way: the writer grades what they could not see, and a recommendation
reads as certain because the data behind it was thin. This section gives every finding an honest state and
every recommendation an honest ending.

## 1.1 Four results per check
1. **Every check ends in one of four results.** Pass: you saw the evidence and it is right. Fail: you saw the
   evidence and it is wrong. Unknown: the evidence needed to judge was not available to you. Not applicable:
   the check does not concern this account (a check about one campaign type, on an account that runs none).
2. **Unknown is a finding about you, not about the account.** "I could not open the report" and "the report
   shows a problem" are different sentences. An unknown lowers how much of the account you covered; it never
   lowers how healthy the account looks.
3. **Not applicable affects neither number.** A feature the account cannot use, or does not yet use, is an
   opportunity to look at, not a deduction. Judge outcomes, not whether the account adopted something new.
4. **A source you could not read is left out of a rollup, not entered as zero.** If one platform or export
   failed, say "audited these, not audited that, no access" and label the result partial. Never call it a
   complete audit.
5. **Score a root cause once.** A tracking fault that makes five reports look wrong is one finding with five
   observations, not five failures (idea from the audit scoring contract of one source; own wording).

## 1.2 Coverage apart from health
1. **Report two things and keep them apart.** Health is the share of the checks you could verify that pass.
   Coverage is the share of the applicable checks you could verify at all. Blending them hides exactly what
   the reader needs: how much was never looked at.
2. **Say what coverage means before showing a grade.** One source grades above one cutoff, calls the middle
   band provisional and refuses a grade below a second cutoff. The cutoffs it uses (80 and 60 percent) are
   that tool's own choice and nothing here checks them. If you adopt bands, write them down as a house choice
   and say it is a choice. Own guidance: where a large part of the account was not seen, report findings and
   the list of unknowns and decline to give a single number.
3. **List every unknown with the exact evidence that would resolve it** (which report, which access, which
   setting), so the next reader can close it instead of re-deriving it.

## 1.3 Facts, hypotheses, missing data
Paid-media numbers make guesses sound certain: small samples, delayed conversions, an average order that
dropped and looks like a cost problem, a platform suggestion presented as strategy. So every recommendation,
diagnosis or readout that could lead to a decision ends with three labelled lists.

1. **Facts**: what the data you saw shows, each with its source and the window it covers.
2. **Hypotheses**: what you infer from the facts, each with how sure you are and what would settle it.
3. **Missing data**: what you did not have, and how it could change the answer.
4. **A missing input is written MISSING and left out of the calculation.** Do not estimate it, do not back it
   out of other figures, do not fill it from a benchmark. A recommendation that cannot name what is missing has
   not been checked against it, so present it as a hypothesis.
5. **Carry the date with a claim.** A figure from a status document, an earlier session or the client is
   stale until pulled again; say "as of" and the date, and keep stale claims out of a sentence the client will
   read unless they are labelled stale. Own guidance: before a statement reaches the client, ask whether they
   could disprove it in a minute with their own access, and give the limits (what share was disclosed, how
   few clicks) first.

## 1.4 Benchmarks are comparisons, not thresholds
A cross-industry median is a question to investigate, never a pass or fail line. When one is quoted:
1. **Label where it came from**, strongest to weakest: the account's own data; an independent study; a figure
   a platform published; a vendor case study. Anything from a vendor or platform marketing page is
   vendor-supplied and is called that.
2. **Check the cohort fits**: platform, objective, industry, geography, price point and attribution window. A
   median for one kind of business says nothing about a different one.
3. **Use the narrowest comparison available**, in this order: the same account, objective and window in an
   earlier comparable period; the account's own experiment or holdout (`skills/experiment-design-pitfalls`);
   the CRM or revenue cohort joined to spend; a peer cohort whose method is disclosed; and last a broad
   industry figure, which is direction only.
4. **Never blend figures with different windows, conversion definitions or currencies** into one number
   without normalising them and saying you did. Two conversion counts built on different windows are shown
   side by side, each with its window (`business/ad-measurement-pitfalls` §3).
