# premortem-review-pitfalls §1 — The brief and who runs the attack

A pre-mortem assumes the decision already failed and works backwards to find why, while there is still time
to change it. Its quality is decided before the first risk is written: who attacks, from what brief, and for
which date.

## 1.1 Independence
1. **The attack runs in a fresh agent or person who had no part in the decision** (kharmanskyi). Someone who
   helped shape it defends its reasoning and, out of politeness, misses the thing that kills it.
2. **The attacker sees only the brief.** Everything it needs travels in the written brief, because the fresh
   reader cannot see the discussion that led to the decision.
3. **If no fresh reader can be started, run it yourself from the brief alone**, attack your own reasoning
   hardest, and never call the result independent (kharmanskyi).
4. **Pre-mortem and red-team are different tools** (phuryn). A pre-mortem imagines the plan already failed and
   narrates why; a red-team attacks the plan's load-bearing assumptions now (see §3). Use the one the situation
   needs, or both (phuryn's red-team command offers a pre-mortem as a follow-up).
5. **Timing**: phuryn's command notes say the best pre-mortems happen when the plan is mostly done, early
   enough to change course and late enough to have substance.

## 1.2 The brief
1. **It states facts and open questions and never argues for the decision.** kharmanskyi: a brief that argues
   gets a report that agrees.
2. **Fields** (kharmanskyi's list, wording ours):

   ```
   What will be done:       three to seven sentences
   What it is for:          the problem, and what success looks like, measured if possible
   The main moves:          money, people, systems, dates
   What is fixed:           constraints and surrounding facts that matter
   Who it lands on:         who is affected if it goes wrong
   What cannot be undone:   the one-way parts
   When we would know:      the date success or failure is judged
   What we know:            facts, each with where it came from
   What we are assuming:    every gap nobody closed, written as an assumption
   ```
3. **A missing constraint is the usual failure.** The brief is where the work is won or lost: a brief that
   omits the one constraint that made the decision sensible produces a confident attack on a plan nobody
   proposed (kharmanskyi, reasons file).
4. **Close gaps in this order** (kharmanskyi): look it up yourself (documents, data, the repository, past
   incidents); ask only where a wrong guess would change the verdict, a few questions at most; otherwise
   write the guess down as a guess, mark it assumed, and repeat it under assumptions.
5. **A date to be judged by is required.** "It failed" means nothing without "by when"; with no such date there
   is nothing to attack (kharmanskyi). If none was given, pick one that fits the decision and say you picked it.

## 1.3 How deep
1. **Two depths** (kharmanskyi): a full attack when the decision is hard to undo or being wrong costs money,
   trust or data beyond one team; a quick look when it is reversible and cheap to be wrong about.
2. **When in doubt, go full.** A full look costs minutes; a quick look at a one-way door costs the door.
3. **Too cheap for the treatment is itself a finding.** If the brief shows the decision is reversible and cheap,
   say so in one line, answer at quick depth, and name the one thing that would justify a full attack. A full
   report on a two-day experiment teaches the reader to ignore the next one.
4. **Use the same treatment for every kind of decision.** A lease and a database migration get the same sweep;
   the money and people areas are where technical decisions often fail (kharmanskyi).
