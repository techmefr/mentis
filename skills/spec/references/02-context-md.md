# § 2 — `CONTEXT.md`, the shared vocabulary

> Section 2 of `skills/spec`. Read it when writing the feature's vocabulary document — the terms,
> entities and business rules the rest of the pipeline will use.

1. **`CONTEXT.md` holds the feature's shared vocabulary: the terms, the entities and the business
   rules.** Its job is that the story, the tests, the code and the review all use one word for one
   thing. Without it each layer invents its own name, and the mismatch is only discovered when somebody
   tries to trace a rule from the story to the query.
2. **One term, one definition, one spelling.** Two words for one concept — customer and client, session
   and lesson, agency and branch — splits every search, every grep and every conversation, and the split
   survives into column names. Pick one, write it down, and use it in the code as well.
3. **Define a term only where the definition is not obvious or not shared.** A glossary that defines
   "user" teaches nobody anything and buries the three terms that actually needed it. The test is whether
   two people on the team would give the same definition unprompted.
4. **The definition says what the term excludes.** "An active contract" is useful when it also says
   whether a contract in its notice period is one; the exclusion is the half that settles arguments,
   and it is the half everybody omits.
5. **Business rules go in as rules, testable, one per line.** "A discount applies above ten seats" is a
   rule; "the pricing should be fair to larger customers" is an intention, and an intention cannot be
   implemented or contradicted. If a rule cannot be written testably, that is a gap for §1's interview.
6. **Say which rules are the domain's and which are this feature's choice.** A rule imposed from outside
   — a regulation, a contract, an accounting convention — cannot be traded away in a scope discussion; a
   rule we chose can. Mixing them means every rule is negotiated at the same weight, and the ones that
   should never move are the ones under most pressure at the end of a sprint.
7. **Name the entities and their relationships as the feature sees them.** Not a schema — the schema is
   the plan's business — but which things exist, which owns which, and what happens to the child when the
   parent goes. That last question is where a spec most often turns out to be silent, and it is a data
   question, so the answer has consequences that outlive the feature.
8. **Where a term already exists in the codebase with a different meaning, say so explicitly.** The
   collision is not resolved by choosing the better name: the code is already full of the old one. Either
   rename deliberately as its own piece of work, or use a different word for the new concept and record
   why.
9. **`CONTEXT.md` is a working document, not a deliverable.** It is written to be read by whoever
   implements, tests and reviews the feature — which means it is short, and it is updated when the
   interview produces a new answer rather than left as a snapshot of the first draft.
10. **Anything in it that turned out to be a decision belongs in an ADR** (§5). The vocabulary document
    records what words mean; it does not record why we chose one option over another, and mixing the two
    makes both harder to find.
11. **A term used in the acceptance criteria and undefined here is the tell that the interview stopped
    early.** The criteria are where vocabulary gets exercised (§3), so reading them against
    `CONTEXT.md` is the cheapest check available on both documents.
12. **Keep it out of the code as comments.** The vocabulary lives in one document; restated in comments
    it becomes several copies with no authoritative one, and the copies drift with every edit. The code
    carries the vocabulary in its names instead.
13. **A synonym borrowed from another feature's `CONTEXT.md` is checked, not assumed.** Two features
    using "member" can mean two different entities with different lifecycles; importing the word without
    importing the definition reintroduces the split point 2 exists to prevent, just across feature
    boundaries instead of within one.
14. **A rule stated as a range needs its boundary named explicitly.** "Above ten seats" leaves the tenth
    seat undecided — inclusive or exclusive is a testable fact, not a stylistic choice, and leaving it
    implicit hands the ambiguity to whichever engineer writes the comparison operator first.
15. **An entity's identity is stated, not implied by its fields.** Two contracts with the same customer
    and the same dates are either the same contract or two — `CONTEXT.md` says which, because the schema
    (§7's plan-level concern) will encode whichever answer it is given, and reversing it later is a
    migration, not an edit.
16. **A term that changes meaning depending on which role is reading it is split into two terms.** "Active"
    meaning one thing to billing and another to support is not one rule with two audiences, it is two
    rules sharing a word — leaving it shared guarantees a query that is correct for one reader and wrong
    for the other.
17. **A business rule with a named exception lists the exception in the same entry, not as a footnote
    elsewhere.** A rule and its carve-out read together or they get implemented separately, by different
    people, at different times, and the carve-out is the one that gets forgotten.
18. **Numbers with units are written with the unit.** "Ten" meaning ten seats, ten days or ten euros is
    resolved by context only until the document is read out of order or quoted in a ticket — the unit
    costs three characters and removes the ambiguity permanently.
