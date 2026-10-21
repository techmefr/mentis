# agent-data-gap-honesty-pitfalls §1 — Absent is not zero

> Part 1 of `skills/agent-data-gap-honesty-pitfalls`. Read it before a figure, a list or a "nothing found" is
> reported from a connector. Source: the shared "absent is not zero" rules of a small-business plugin set
> (Apache-2.0), rewritten in our own words; points marked own guidance are ours.

The shape of every failure here: a field comes back empty, zero, truncated or untracked, and the agent reads
that as a fact about the business instead of a fact about the data. The answer is clean, confident and wrong in
the direction that hides the problem, so nothing prompts a check.

## 1.1 The question to ask first
1. **Before reporting a figure, ask what would produce this value if the business were fine, and what would
   produce it if the data were broken.** If the two cannot be told apart, say so instead of picking one.

## 1.2 Slices and summaries
1. **A paginated or top-N call describes its own slice.** Symptom: a receivables total that omits the oldest
   debts because the report returned only the largest ten lines. Check: compare against a count or a balance
   line from an unconstrained source. Fix: total from that source, or label the number partial and give the
   size of the slice.
2. **A summary object is a convenience, not a source.** When a payload carries both a summary and the rows it
   was computed from, add up the rows. Symptom: a profit-and-loss summary that shows no expenses while the rows
   below it hold large ones. Fix: report the rows' total and note that the summary disagreed.
3. **A partial pull is not a full pull.** A scrape or export that stopped early (rate limit, timeout, a page
   cap) must be reported as stopping early, with how far it got. Own guidance.

## 1.3 Zero, empty and unknown
1. **Zero and absent are different facts that many interfaces conflate.** A revenue of `0.0`, an empty date, a
   null count: decide which reading is plausible. A company with no revenue is rare; a data provider with no
   figure is common. When zero is implausible, report unknown.
2. **Empty is not fresh.** A record with no activity date has not been touched, which is the worst case, not the
   healthiest. Date comparisons silently leave out empty fields, so the neglected records drop out of the very
   list built to find them. Fix: rank "no date" above the oldest date and label it separately.
3. **A date later than today is corrupt.** A recency score reads it as the newest event and floats a bad record
   to the top. Fix: compare every date with today before scoring and treat a future date as missing.
4. **A switched-off tracker looks like no demand.** A product whose stock tracking is disabled reports no sales
   from the stock endpoint. Fix: when two endpoints disagree about the same thing, find which one measures what
   you need and say which you used (§1.5).
5. **A balance field can hide pending money.** An `available` of zero beside a `pending` amount is not "no
   money here". Read the sibling fields before concluding. Own guidance.

## 1.4 Empty versus failed
1. **An empty result and a failed query look the same.** Symptom: a label or filter search returns nothing,
   while the label itself reports hundreds of items. Check: ask for a count by a second route before writing
   "no results". Fix: if the second route disagrees, the query is wrong, not the mailbox.
2. **"No results" is a claim about the business** and gets the same scrutiny as any figure. When a connector
   returned nothing at all, name the connector and say it returned nothing; do not drop it from the answer.

## 1.5 Counts that disagree
1. **Two counts for the same thing that differ by a large factor mean one of them measures something else.**
   Treat it as a finding. Say which count was used and why. Do not pick silently and do not call it rounding.

## 1.6 Saying it well
1. **Give the person the numbers to trust, not the mechanism.** One sentence naming the figure, its scope and
   the one exception is enough: the total across all customers and the single overdue account, not the total of
   the slice.
2. **State the gap where it matters.** "Tracking looks off on most variants, so velocity uses sales figures and
   the inventory report is used only for stock on hand" tells the reader how much to trust the number.
3. **A named gap is useful; an invented zero is worse than silence**, because the person acts on it and forwards
   it to a bank, a board or an accountant.
4. **Say plainly when something cannot be determined, then stop.** Do not fill the hole with a plausible value.
