# § 1 — A request is not a story yet

> Section 1 of `business/product-ownership`. Read it when a request arrives from a customer, a colleague
> or a stakeholder, before anything is written into a tracker.

1. **Find the problem behind the request.** A request phrased as a feature is a solution somebody already
   chose (`business/sales-support` §1.1); the problem behind it often has a cheaper answer we already
   ship. The cost of skipping this is not the wasted build: it is that the feature ships, the problem
   stays, and nobody connects the two — so the next request is for a second feature on top.
2. **Name who has the problem and how often.** "A customer asked" and "every customer hits this weekly"
   produce different decisions, and the difference is usually knowable. It is knowable from support
   tickets, from usage, or from asking three of them — which takes an afternoon and settles an argument
   that otherwise runs for a quarter.
3. **What happens if we don't build it?** If the answer is "nothing much", that's the finding. Write it
   down as the finding rather than leaving the item on the list: an item nobody refuses and nobody builds
   occupies attention every time the backlog is read.
4. **Only then does it become a story** — written to the fixed section set of §6, not invented ad hoc.
5. **A request that arrives with a date is two facts, and they separate.** The need is one; the date
   belongs to something else — a contract, a demo, a regulation, someone's holiday. Ask which, because a
   date backed by a contract is a constraint and a date backed by a preference is a preference, and only
   one of them is allowed to change what ships (§3.4).
6. **The person who asked is often not the person with the problem.** A manager relaying a team's
   complaint, a support agent relaying a customer's, a salesperson relaying a prospect's: each relay
   loses the detail the criteria need. Trace it to whoever actually loses the time, or §4's criteria get
   written for the relay's version of the problem.
7. **An existing workaround is the measurement.** How clumsy it is and how many people run it *is* the
   size of the problem, available without any research. If nobody uses the workaround, that is the
   strongest evidence you will get that nobody has the problem — and if everybody does, the story is
   already specified by what they do.
8. **"The competitor has it" is not a problem statement.** It may still be a reason to build — a deal is
   a reason, a market expectation is a reason — but it has to be said as that reason, because it changes
   what "done" means: matching a competitor's feature list is a different objective from closing a
   problem, and it is satisfied by different work.
9. **Count requests, don't remember them.** Three asks in a month is a pattern and three in two years is
   noise, and memory does not distinguish the two — it distinguishes recent from old, and loud from
   quiet. Log every request somewhere countable, even one line, so the second ask is data rather than a
   feeling that this keeps coming up.
10. **A request that is really a documentation or training gap gets that answer.** Building a feature to
    explain a feature doubles the surface: now there are two things to maintain, and the new one has to be
    explained too. The honest response is a change to the wording, the empty state, or the onboarding —
    and it usually ships the same week.
11. **A request that only one customer can use is a decision about the product, not a story.** It may be
    right to build it, as a paid piece of work or as a deliberate bet, but it has to be decided as that
    rather than absorbed into the roadmap — otherwise the backlog fills with work that serves one account
    and nobody notices until the ordering stops making sense (§2.4).
12. **The discovery has an output even when nothing gets built.** The finding, written down where the next
    person asking will find it: what was asked, what the underlying problem was, and why the answer was
    no. Without that, the same discovery is redone every six months, and the second time it is done by
    someone who doesn't know it was done before.
13. **A story drafted by a tool is still a draft, not a finding.** A triage assistant that turns a raw
    request into acceptance-criteria-shaped text has skipped every question in this section — the problem
    behind the request, who has it, how often, what an existing workaround already measures — because it
    answers from the wording of the ask, not from the person who has the problem. The draft can save the
    typing; it cannot stand in for the interview, and a story that reached the tracker without one is
    exactly the "looks decided" failure §8.3's writing-only-after-a-go rule already exists to prevent,
    arriving from a faster source.
