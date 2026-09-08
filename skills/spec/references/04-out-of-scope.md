# § 4 — Out of scope, explicitly

> Section 4 of `skills/spec`. Read it when the scope is being locked — the exclusions are part of the
> lock, not a postscript.

1. **List the explicit out-of-scope.** An exclusion written down is a decision; the same thing left
   unsaid is an omission somebody discovers at review, and at review it is a negotiation with code
   already written. This is the cheapest section in the document and the one most often left empty.
2. **Write each exclusion at the moment it comes up in the interview.** The sentence "and of course it
   should also handle X" is where an exclusion is obvious and free; recovered a week later it costs a
   conversation, and recovered at acceptance it costs the feature's reputation.
3. **An exclusion says what is not built, not what does not exist.** "Bulk import is not in this story"
   is useful. "There is no bulk import" is a statement about the product that will be wrong the day
   somebody builds one, and it reads as a refusal rather than as a boundary.
4. **Exclude the adjacent thing, by name.** The exclusions that matter are the ones a reasonable person
   would have assumed: the other role, the second entity type, the export, the notification, the mobile
   case, the historical data. Excluding something nobody imagined is filler; excluding the neighbouring
   feature is the whole point.
5. **An exclusion that is really a dependency is labelled as one.** "Not in scope: the permission model"
   means something different depending on whether the permission model exists, is being built elsewhere,
   or has not been decided. The first is a boundary, the second is a dependency with a state
   (`business/product-ownership` §6.11), and the third blocks the start.
6. **Deferring is not excluding, and the two get different words.** "Later" invites the question "when",
   which nobody in this step can answer; "not in this story" is a boundary this step owns. Where the
   thing genuinely is planned, it belongs in the backlog with its own decision rather than as a promise
   inside a spec.
7. **Exclusions constrain the design, so they are read at plan time.** Excluding multi-currency is a
   licence to store one currency; excluding it *for now* while everyone expects it next quarter is a
   different instruction, and the design that follows is different. Say which one it is, because the
   implementer will act on it.
8. **Non-functional expectations are in or out, explicitly.** Scale, latency, accessibility,
   localisation, audit: each is either a criterion with a number (§3.7) or an exclusion. Silence is read
   as "not required" by whoever is implementing and as "obviously required" by whoever asked, which is
   the most reliable disagreement in software.
9. **An exclusion is not a place to hide an unanswered question.** Excluding the case nobody could
   decide converts a blocking gap into an apparent decision, and the gap resurfaces the first time a
   real user hits it. If the interview could not settle it, escalate (§1.10) rather than excluding it.
10. **The exclusions are stated where the reader will look, once.** Duplicated into the criteria and the
    context they drift; kept in one place they can be checked against the criteria in a single pass,
    which is also the fastest review this document supports.
11. **Anything excluded because it is expensive gets its reason recorded.** Otherwise the next person
    reads the exclusion as arbitrary and reverses it, having not seen the cost — and the cost is usually
    the only thing that made the exclusion right.
12. **A spec with no exclusions is not a small spec, it is an unfinished one.** Every real feature has a
    neighbour somebody would reasonably expect it to cover. If none can be named, the interview stopped
    before the scope was sharp (§1.9 is about redundant questions, not about skipping this one).
