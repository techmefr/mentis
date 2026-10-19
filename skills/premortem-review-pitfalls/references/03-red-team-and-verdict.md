# premortem-review-pitfalls §3 — Attack the assumptions and give the verdict

The cards of §2 say how the plan fails. This section attacks what the plan takes for granted, finds the
cheapest way to learn it is wrong, and ends on one verdict that the reader sees first.

## 3.1 Attack the load-bearing claims
1. **List what the plan asserts as true**, about users, market, constraint, mechanism and timeline, and keep
   only the **load-bearing** claims: the ones whose falsity would kill the plan (phuryn strategy-red-team).
2. **Steelman, then attack.** State the strongest version of why the claim may be true and attack that. An
   attack on a strawman is worthless (same source).
3. **Write each failure as "Fails if ___"**: concrete and falsifiable. "Fails if activation is not actually
   the constraint" beats "execution risk".
4. **Rank by impact if wrong, times likelihood of being wrong, times cheapness to test.** The top of the list
   is what to test first; show the ranking at the top of the report.
5. **For each surviving kill-assumption give four things**: the condition that breaks the plan, the evidence
   to get soon (a query, a conversation), the kill criterion (the threshold at which to stop or change
   course) and the cheapest test (the smallest experiment that moves the belief).
6. **Few and specific**: three to five at most; five real ones with tests beat twenty generic risks (phuryn).

## 3.2 Do not fabricate and do not rubber-stamp
1. **Do not invent a weakness.** If a claim is well-reasoned, say so plainly: an attack that manufactures doubt
   is as useless as one that rubber-stamps (phuryn).
2. **Say what holds.** kharmanskyi ends the report with the parts of the decision that survived, so they are
   not churned while the rest is fixed. Good news belongs there, never as a cushion around a finding.
3. **"The plan is sound" is a legitimate verdict, once the attack has run.** It is never a substitute for
   running one (kharmanskyi).
4. **Say what could not be assessed**, where the plan gave too little to judge (phuryn).

## 3.3 Findings that cut across the cards
1. **The thing nobody is questioning**: the single belief the author most likely does not know they hold, and
   what happens if it is wrong. One, not a list (kharmanskyi).
2. **The cheapest way to find out you are wrong**: the least expensive thing that could disprove the most
   load-bearing untested belief before the money is spent, with what counts as passing and failing.
3. **A flaw no fix can cure**: yes or no. If yes, say why patching does not work.
4. **When to pull the plug**: for a staged decision, one to three stop conditions ("if X has not happened by
   day N, stop") with why that number. For a single act that cannot be taken back, say there is no after and
   every safeguard has to fire before it (kharmanskyi).
5. **A kill criterion and a decision date** belong to every surviving kill-assumption (§3.1, point 5) and to
   every launch-blocking risk (§2.3).

## 3.4 The verdict and the report
1. **One verdict from five** (kharmanskyi): go ahead; go but fix these first; try it small first; think again;
   do not do this. "Try it small first" is not a soft no: the unknowns are testable and worth testing before
   money moves.
2. **Decide the verdict last and print it first**, so the reader does not assemble it from the risks.
3. **Part one fits on one screen**: the verdict, one line of why, the worst case in money, time or trust, the
   biggest risks (at most three, one line each), the thing nobody questions, and what to fix before
   committing. The detail follows for whoever wants it.
4. **Write for someone who must act and may not know the field** (kharmanskyi's prompt): plain words, numbers a
   person can use (money, days, counts) rather than "materially degraded", and bad news never softened or
   moved to the middle of a sentence.
5. **Offer to turn the fixes into work** (edits to the plan, tickets, an owner and a date each, a reminder for
   each early warning). A pre-mortem nobody acts on is entertainment (kharmanskyi, reasons file).
6. **If the author goes ahead against the findings**, note it once, set the tripwires if they want them, and
   do not re-argue (kharmanskyi).
