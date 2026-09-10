# § 5 — ADRs: the decisions and what was ruled out

> Section 5 of `skills/spec`. Read it when a structural decision is taken during the spec. How an ADR is
> written and where it lives is `skills/documentation-adr`; this section is about which decisions earn
> one and what has to be in it.

1. **Write an ADR for every structural decision: the choice, the alternatives ruled out, and why.** The
   third part is the one that has value later — a record of what was chosen without what was rejected
   tells the next reader nothing they could not read from the code, and it is precisely the rejected
   options they are about to propose.
2. **Structural means expensive to reverse.** A data model, a boundary between two systems, a
   third-party dependency, an authentication mechanism, a storage format, a decision about what is
   canonical. A library choice that could be swapped in an afternoon does not need one; a column that
   will hold two years of data does.
3. **Record the constraint that decided it, not the preference.** "Chosen because the export has to be
   readable by the finance team's existing tooling" survives; "chosen because it is cleaner" does not
   survive its author, and it is indistinguishable from taste when somebody wants to change it.
4. **An alternative is ruled out with the reason it lost, in one line each.** Two or three is usually
   enough, and the ones worth listing are the ones a competent person would suggest. An ADR that rules
   out only strawmen reads as a justification written after the fact.
5. **A decision taken under a constraint that might lift says so.** "While there is one currency" or
   "until the second tenant exists" tells the next reader what to re-check, which converts a stale
   decision into a scheduled one. Without it the constraint is forgotten and the decision looks
   permanent.
6. **A decision nobody in the room owns is escalated, not recorded.** Writing an ADR for a business rule
   the business has not chosen makes it look decided (§1.7's mechanism, one level up). The ADR records a
   decision that was taken; it is not the instrument for taking one.
7. **Where a rule from a governing catalogue or a house style settles the case, apply it and say so
   briefly.** That is a one-line ADR — "we follow the house convention here" — and it is worth writing
   because it stops the question being reopened. It is not a conflict, and it is never reported as one.
8. **A decision that was deliberately *not* taken is worth an ADR too.** Choosing not to introduce a
   Repository, not to add a queue, not to split a service: the absence is invisible in the code, so the
   reasoning has nowhere else to live, and the next reader's first instinct will be to add the thing
   (`skills/design-patterns` §5.3).
9. **One decision per ADR.** Two bundled means one of them gets superseded and the record becomes
   half-true, with no way to tell which half. It also makes them unfindable: an ADR is looked up by the
   decision somebody is questioning.
10. **A superseded ADR is marked superseded, never edited.** The old reasoning is the evidence of what
    was known at the time, which is what makes the new decision judgeable. Editing it produces a document
    that has always agreed with the present, which is worth nothing.
11. **The ADR is written at the moment of the decision, not at the end of the feature.** Written later
    it records the outcome and loses the alternatives, because by then they no longer feel like real
    options — which removes exactly the part point 1 says is the value.
12. **A spec whose ADRs are all trivial has either an easy feature or an unexamined one.** Worth a
    second look: a feature with no expensive-to-reverse decision anywhere is usually a feature whose
    data model was inherited without being checked.
13. **A decision reversed later gets a new ADR, not a deleted one.** The old ADR is superseded (point
    10), and the new one records what changed since — the constraint that lifted, the scale that was
    reached, the dependency that was deprecated. Deleting the old one erases the exact history a reader
    needs to judge whether the same mistake is being made twice.
14. **Two teams disagreeing on a structural choice write one ADR, not one each.** A per-team record lets
    each side keep believing its own version was adopted, and the next reader finds two documents that
    contradict each other with no way to tell which one shipped. The disagreement itself, and how it was
    resolved, is part of what the single ADR has to say.
15. **An ADR that only restates the framework's own default is not a decision.** Choosing not to
    override what the framework already does is worth a line only when a competent reader would expect
    an override here — otherwise it is noise competing with the ADRs that carry real alternatives
    (`skills/design-patterns` §2, framework-already-does-it).
16. **A prototype's ADRs do not survive into the production spec by default.** A decision taken to get a
    demo working under a deadline was usually taken under different constraints — real data volume, real
    concurrency, real security requirements — than the ones the shipped feature will face, so it is
    reopened, not inherited silently.
17. **An ADR referencing a person by name outlives that person's tenure on the project.** "Because
    Sophie needed it this way" is a decision with no traceable reason once Sophie has moved on; the
    reason has to survive independently of who was in the room, per point 3's constraint-not-preference
    rule.
18. **A decision an ADR describes as reversible is checked against what actually reverses it.** "We can
    always change the storage format later" is only true if nothing downstream has come to depend on the
    format's specifics — an ADR that claims reversibility without checking for that dependency is really
    an unrecorded structural decision, mislabeled to avoid point 2's bar.
