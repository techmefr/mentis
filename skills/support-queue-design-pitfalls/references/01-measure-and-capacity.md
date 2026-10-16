# support-queue-design-pitfalls §1 — Measure and capacity

The failure this section prevents is a promise or a process designed for an imaginary queue. Everything
that follows refers to numbers measured here.

## 1.1 Measure first
1. **Export the queue and compute a baseline before proposing anything.** The source's list: open count, age
   median and 90th percentile, share of items with no triage state, count with no recent activity, median and
   90th percentile time to first human response, items created versus closed over the window, and how often
   each label is used (including labels used once).
2. **No script available? Sample about fifty open items by hand** and estimate the same figures. An estimate
   beats designing blind, and without a baseline you cannot tell later whether the redesign helped.
3. **Read the numbers back in plain language before acting.** A queue that is mostly usage questions needs a
   different fix from one that is mostly unanswered bug reports.
4. **Ask whether the items cluster.** On a large old backlog, grouping items under a shared cause and pointing
   the rest at one parent may clear more than triaging item by item. Decide this before building per-item
   machinery.
5. **Keep the export and the figures with the policy.** Own guidance: the monthly rerun in the verify step needs
   the first numbers to compare against.

## 1.2 Do the capacity arithmetic
1. **Weekly capacity in items** is triagers times sessions per week times minutes per session, divided by
   minutes per item. Compare it with inflow from the baseline.
2. **Time a pilot session to get the minutes per item** instead of importing a constant. The source offers
   three minutes only as a planning placeholder of its own; do not treat it as a measured figure.
3. **Subtract the time spent on items that can never be actionable** before comparing. A queue full of invalid
   submissions fails the arithmetic even when nominal capacity looks fine.
4. **Deep investigation is not triage**; it is work that triage schedules.

## 1.3 When capacity is below inflow, no label helps
1. **Three levers close the gap**: cut intake, shorten the promise, add triagers. Pick by queue relieved per
   hour of effort, say which one you chose, and write it into the policy.
2. **Cutting intake is the only lever that lowers the demand permanently**; adding triagers is the only one
   that raises capacity, and it is slow (a new triager is net negative for a while). A team that only ever cuts
   intake shrinks itself to fit its worst month.
3. **Shortening the promise changes nothing about the queue**; it only stops the promise being broken.
4. **Paid desk**: where a response target is contractual, the third lever is a contract conversation, and a
   separate intake path for contracted customers keeps their obligation from setting the target for everyone
   else. Own guidance, extending the source's volunteer-versus-company remark.

## 1.4 Set the first-response target from capacity
1. **The target comes from the capacity number, not from ambition.** An aspirational target from two people is
   a promise that will be broken in the first bad week.
2. **Set it for a bad month, not a good one.**
3. **Define what counts**: a human reply, not a fix and not a greeting from a bot.
4. **Publish the number the baseline supports.** A published target converts silence from "abandoned" into
   "known queue"; one nobody can meet is worse than none.

## 1.5 Decide the volume-gating trigger in calm
1. **Name the trigger now**: the inflow rate or valid-report share at which you will restrict who can open
   items, cap open items per author, switch a submission type off, or remove an incentive being farmed.
2. **Projects that gated volume usually did it after burnout was acute**; deciding the trigger at design time
   makes it a policy rather than a crisis improvisation.
3. **Gate on reputation and volume, not on a guess that content was machine-written.** The source reports no
   reliable detector, and an accusation without proof opens a conduct problem on top of the original one.
4. **Paid desk**: you cannot restrict paying customers from contacting you; the equivalent levers are
   entitlement checks, a required minimum of information, and a separate path for out-of-scope requests
   (§2.5). Own guidance.

## 1.6 Verify
Recompute the arithmetic with the pilot figure and check that the published target survives it. Then rerun the
baseline monthly for the first quarter; a redesign with no second measurement is a guess.
