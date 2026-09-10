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
13. **Sort what's out into won't-build and not-yet, and keep the two visibly apart.** A won't-have is a
    boundary this story owns; a not-yet is a future decision parked somewhere else. Filing both under the
    same "out of scope" heading lets a not-yet quietly harden into a won't-have that nobody actually chose,
    just because it sat in the same list long enough.
14. **The out-of-scope list is where a change request gets triaged, not where it dies.** When something
    excluded here later turns out to matter, it re-enters through the same ranking every other request
    goes through (`business/product-ownership` §2) rather than being folded into the current story because
    it is already written down nearby — an exclusion is not a queue-jump for its own reversal.
15. **State the boundary in the unit the reader decides in, not the unit the writer typed in.** "Not
    scaling past 10,000 rows this quarter" tells the next planner something they can act on; "performance
    is out of scope" tells them nothing they can size against, and it gets re-litigated the day the row
    count actually becomes a problem.
16. **An exclusion protects the design only if it is read before the design is chosen, not after.** Written
    into the spec but noticed for the first time during code review, it either forces a rework of a design
    that already assumed the excluded case, or gets quietly ignored because reworking is more expensive
    than the exclusion was worth — either way the document did not do the job it was written for.
17. **The out-of-scope section is a two-way boundary: it also protects the excluded thing from being
    half-built by accident.** A validation rule added "just in case" for a case the story explicitly
    excludes creates a code path nobody asked for, nobody tested, and nobody will remember exists the day
    the excluded feature is actually built properly.
18. **Reviewing the exclusions takes less time than reviewing the criteria, which is exactly why it gets
    skipped.** A five-line list that costs two minutes to check against the criteria is the cheapest review
    step available and the one most often waved through unread — the two minutes are what point 10's
    single-pass check is actually for.
