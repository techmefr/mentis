# § 7 — Reviewing a story

> Section 7 of `business/product-ownership`. Read it when reviewing a story someone else wrote — and
> §9.2 when the story's author is also the person who will build it.

1. **Set the criticality first**, because it decides how deep the review goes: low (UI comfort), medium
   (standard business workflow), high (security, permissions, synchronisation, billing, anything with a data
   or money consequence). Reviewing everything at maximum depth means nothing gets reviewed at all — the
   reviews take too long, the queue backs up, and the next one is skipped entirely rather than shortened.
2. **Read along fixed axes** rather than freehand, so two reviewers find the same gaps: clarity of the
   business intent; quality of the scope; the domain model; the calculation rules; the acceptance criteria;
   whether a developer can act on it as written; testability and QA; delivery risk; consistency with the other
   projects; the story's place in the backlog; functional-debt and maintainability risk; whether it is really
   a foundation/system story; and the cost of framing it properly. Freehand review finds whatever the
   reviewer happens to care about, which is why two reviewers of the same story usually produce two
   disjoint lists and neither notices what both missed.
3. **Read them in priority order, and stop escalating if the foundations are weak.** Structure first, then the
   business need, then whether a developer can pick it up without three rounds of clarification, then the
   implementation risks — and only then criteria and testability, splitting, debt, wording, backlog coherence.
   **Analysing functional debt on a story whose business need is unclear is wasted effort**: fix the first
   four, say out loud that the framing needs rework, and never bury a structural problem under prose about
   acceptance criteria.
4. **Never invent to fill a gap.** Not a business rule, not a dependency, not a status, not a role, not a data
   source. If you need one for the story to make sense, that need **is** the finding. A plausible-sounding
   guess in a story becomes a requirement nobody decided — and it is indistinguishable, three weeks later,
   from one that was decided, so it gets built and defended.
5. **Ask, in conversation, one question at a time** — the exchange *is* the gap-resolution mechanism. Do not
   dump a list of twenty questions for someone to take away: ask the blocking one, wait, then ask what depends
   on the answer. Be specific — "the context says monthly, calendar month or rolling 30 days?" beats "clarify
   the context". Only when the person asking genuinely does not know does it become a written question for the
   business owner. A list of twenty comes back with eight answered, and the eight are the easy ones.
6. **A hypothesis stays labelled as one**, never repackaged as fact in the next draft. The mechanism is
   quiet: a reviewer's "presumably this only applies to active contracts" becomes a sentence in the
   revision, and by the third draft nobody remembers it was a guess.
7. **The output is structured and the same every time**: what's missing, what's ambiguous, what's
   contradictory, what's out of scope, the questions that block a start, and — where it helps — a rewritten
   version. A verdict with no rewrite forces the writer to guess what would satisfy it, which produces a
   second draft that fails for a new reason.
8. Separate a **blocking** gap (can't start) from an **improvement** (can start). Not doing so makes every
   review read as a refusal — and **do not balance artificially**: a weak story is weak, say so; a strong one
   is strong, say that too. A forced "on the other hand" dilutes the only signal the reader needs.
9. **Do not refuse a story outright.** Name which sections are missing and which of them actually matter
   here. "Incomplete" is not actionable; "the exclusions and the permission edge cases are missing, and
   for a billing story both are blocking" is.
10. **Review the story against the code where the code is available.** A rule that contradicts what the
    system already does, a status that does not exist, an entity named differently in the schema: these
    are findings a reading of the story alone cannot produce, and they are the ones that cost most when
    missed — the developer discovers them after starting.
11. **A story that is really two is the most common structural finding, and the sizing test settles it**
    (§8.2). Say which two, and which one goes first — a review that says "this is too big" without
    proposing the split leaves the writer to guess a seam, and the seam they pick is usually a phase
    rather than a deliverable.
12. **Say what you checked, not only what you found.** A review that lists three findings does not tell
    the reader whether the criteria were examined at all. Naming the axes actually read (point 2) is what
    lets the writer trust an empty finding on an axis rather than assume it was skipped.
13. **The review ends with a decision, not with a discussion.** Ready, or blocked on these named
    questions. A review that trails off leaves the story in the state that causes §5.3: picked up
    hopefully, with the questions answered by whoever gets stuck.
