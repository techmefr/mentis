# premortem-review-pitfalls §2 — The sweep and the risk cards

From a brief to a short list of risks that each has a chain behind it, three separate scores and a first
warning sign. The aim is a list a reader can act on, not a long one.

## 2.1 Start from the outside
1. **Name the class of decision** ("a multi-year commitment", "moving a live database", "raising prices on
   existing customers") and say what usually kills decisions of that class, including real failures you know
   of (kharmanskyi). Most decisions fail the ordinary way for their class.
2. **Keep it as its own section of the report**, three to six lines, with which of those causes are live
   here. It is the one part a reader can check the risks against; folding it into the cards hides whether the
   ordinary failures were examined.
3. **Check load-bearing facts before speculating** about them: a document, a number, a price, a past incident
   (kharmanskyi).

## 2.2 Sweep every area, then publish what survives
1. **Hunt for a way to fail in each area** (kharmanskyi's nine, wording ours): will people use it, money,
   building it, running it day to day, the people involved, things you depend on, legal and rules, people
   misusing it, what others do about it.
2. **Account for every area in the report**, including the empty ones, one line each. An area nobody mentions
   and an area nobody checked look the same (kharmanskyi).
3. **No quota.** A risk earns a place only when its chain (this leads to that, which kills it) is anchored in
   the brief or in evidence that was checked. Three well-anchored risks beat seven padded ones; fewer than
   three is itself a finding and is said plainly.
4. **Follow the interests**: wherever the plan needs someone to behave a certain way, check whether their own
   interests agree. If not, that is a risk with a mechanism, not a footnote about culture (kharmanskyi).
5. **Say who benefits if it fails**, only where someone does (a competitor, the other side of a contract,
   someone inside whose interests point the other way); otherwise write one line that nobody does.

## 2.3 Tigers, paper tigers, elephants
1. **Three kinds** (phuryn pre-mortem skill):
   - *Tigers*: real problems that could derail the plan, based on evidence, experience or clear logic;
   - *Paper tigers*: worries others raise that you do not believe in, still worth documenting to align people;
   - *Elephants*: something you are not sure is a problem, which the team is not discussing enough.
2. **Urgency of a Tiger**: launch-blocking (solve before launch), fast-follow (soon after), track (monitor, act
   if it becomes a problem). Each launch-blocking Tiger gets a described risk, a concrete mitigation, an owner
   and a decision or completion date (phuryn).
3. **Sources differ**: phuryn's skill says to default to Tiger when unsure; kharmanskyi says to publish only
   what is anchored. **This block follows kharmanskyi**: an unsure item becomes an Elephant with an
   investigation step, and a Tiger needs its anchor (own reconciliation).
4. **phuryn's two files define Elephants differently**: not sure it is a problem, versus known but avoided.
   Both are carried as "unspoken and unchecked" and the report says which it means (own reconciliation).

## 2.4 One card per surviving risk
1. **Fields** (kharmanskyi's card, wording ours):

   ```
   Risk / area:        short name | one of the nine areas
   How it happens:     the chain, and why it kills the decision rather than annoys
   Assumption:         the belief that turns out false
   Based on:           the line of the brief, or the outside evidence checked
   Likelihood:         low | medium | high, and why
   Severity:           small | serious | severe | fatal, and what is lost
   Detectability:      easily | only if you look | not until too late
   How it shows up:    first sign, next sign, damage, rough timing
   Early warning:      what to watch | value that means trouble | how often | what to do then
   What to do:         the change, what gets worse if made, which bucket it lands in
   ```
2. **Three separate answers.** Likelihood, severity and detectability are not collapsed into "risky": the
   scariest risk is often not the likeliest, and the one you would not see coming is often neither
   (kharmanskyi).
3. **Four buckets**: fix before you commit, worth fixing, just watch it, accept on purpose.
4. **Every claim is anchored or labelled**: it quotes the brief, names evidence, or says it is an assumption.
   There is no fourth kind (kharmanskyi).
