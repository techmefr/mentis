# § 2 — Order by consequence, not by volume of asking

> Section 2 of `business/product-ownership`. Read it when a backlog needs ordering, or when two items are
> being argued about.

1. **Rank on the pair (impact, cost)**, where cost comes from an estimate grounded in the code (§8), not
   from a feeling. The two halves fail differently: an impact nobody quantified is optimism, and a cost
   nobody read the code for is optimism twice — and the second one is what turns a two-week plan into a
   quarter.
2. **The loudest request is not the most valuable one.** Who asked is data about who asks, not about
   value. The systematic bias is worth naming: the customers who complain are the ones still engaged
   enough to complain, so an ordering driven by volume of asking serves the people least likely to leave.
3. **Bugs that lose or corrupt data, and anything with a security or privacy consequence, outrank
   features** — that ordering isn't negotiable (`skills/bug-triage` §3). The reason it is stated as
   non-negotiable rather than as a heavy weighting is that these are exactly the items that lose an
   argument against a visible feature, every time, on the grounds that nobody has complained yet.
4. **Leave room for the work nobody requests**: migrations, debt, upgrades. A backlog that is 100%
   features silently borrows against the next quarter, and the interest arrives as an incident. Reserve
   the room as a share of the capacity rather than as items in the list, because as items they lose to
   whatever is more visible that week.
5. **Write down what you decided not to do, and why.** Otherwise it's re-litigated monthly, and the
   person who asked assumes it was forgotten rather than declined. The written version also protects the
   decision from being reversed by whoever asks most recently rather than by new information.
6. **Rank one list, not a series of pairs.** Comparing two items at a time produces an order that is not
   transitive — A beats B, B beats C, and C beats A — because each comparison is made on whichever axis
   is salient at the time. Force a single total order over everything in play; the argument that follows
   is the useful one.
7. **Cost is not build cost.** It is the support load, the migration, the documentation, the training,
   and what it makes harder to change afterwards. An item that is three days to build and permanent to
   maintain is more expensive than one that is two weeks and self-contained, and a ranking that only
   counts build time systematically picks the first.
8. **An order that never moves is a queue, and one that moves weekly has no order at all.** Both are
   failures with the same symptom: nobody trusts the list. Re-rank on a fixed rhythm and on new
   information, and say which of the two caused a change — otherwise a re-rank reads as somebody having
   been lobbied.
9. **The order has to be visible to the people who asked.** An ordering that lives with one person is
   re-explained one conversation at a time, and each explanation is an opportunity to be argued out of
   it. Published, it answers the question before it is asked and makes the trade-off visible rather than
   personal.
10. **Bundling is how a small item waits for a big one.** "Do these three together, they're related" puts
    a two-day change behind a three-week one, and related is not the same as inseparable. Bundle only
    where doing one without the others leaves the product in a state nobody can use — and say which of
    those it is.
11. **Something urgent every week means the intake is broken, not the backlog.** Recurrent emergencies
    are a symptom: no ordering visible to the people who ask (point 9), no way to say not now (§3), or a
    quality problem generating its own interruptions (point 4). Re-ranking faster does not fix any of the
    three.
12. **A backlog nobody prunes is a backlog nobody reads.** An item untouched for a year is a decision
    already taken — close it, with the reason, and let it be re-raised if the need is still real. A list
    long enough to need a search box has stopped being a priority list and become an archive with
    aspirations.
