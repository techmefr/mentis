# § 2 — ADR template: six fields, always the same

> Section 2 of `skills/documentation-adr`. Read it when the six fields are being proposed, or when a
> written ADR is being reviewed.

1. **Status**: proposed / accepted / superseded (never an indefinite "in progress"). An indefinite
   status is the failure mode: a reader cannot tell whether the decision binds them, so half the
   codebase follows it and half does not, and both halves can point at the file.
2. **Date**: the date of the decision, to place the context in time. It is what makes every other field
   readable — a constraint from two years ago is read as history, the same sentence undated is read as
   current, and the reader has no way to tell which they are looking at.
3. **Context**: the situation that made the decision necessary, what won't be obvious any more in
   six months. Write the constraint, not the preference: a constraint can be checked for whether it
   still holds, and a preference does not survive its author (§4 for the case where it is deliberately
   permanent).
4. **Decision**: what was decided, in a sharp formulation. Sharp means a reader can tell whether a
   given piece of code complies — a decision phrased as a direction ("we will favour...") is not a
   decision, it is a mood, and it will be cited by both sides of the next argument.
5. **Alternatives considered**: every option ruled out, with its pros/cons; without that, a future
   reader can't tell whether the alternative was considered or forgotten. This is the field that gets
   dropped for time and the field that does the work: the proposal that comes back in six months is
   almost always one of these, and the note turns a re-litigation into two sentences.
6. **Consequences**: what the decision implies, including the trade-offs accepted. The accepted cost is
   the part a later reader would otherwise mistake for an oversight, and it is where §4's permanent
   tension is named.
7. **Every field is filled, and an unfillable field is a finding.** No alternatives means nothing was
   compared, so the decision was a default; no consequences means the cost was not looked for. Leaving
   one blank "to go faster" converts the missing thinking into a document that looks like it happened.
8. **The decision is dated, not the file.** A record edited to reflect what we do now has lost the
   thing it existed to hold, and it does so silently, since nothing in the file says it was rewritten.
   Corrections of fact are fine; a changed decision is a new record (§3).
9. **Name the decision by what it decides.** A record titled after a technology cannot be found by
   someone looking for the problem, and the problem is what the next reader has. A number plus a
   sentence is enough, and the number is what everything else cites.
10. **Say what the decision does *not* cover.** The neighbouring case a reasonable reader would assume
    was included is where a record gets stretched to justify something it never considered — which is
    how an ADR ends up cited as the reason for a shape nobody chose.
11. **Write it so the person who has to reverse it can.** That reader needs the constraint, the
    alternatives and the cost, in that order, and needs to know which of the three has changed. An ADR
    that only records the outcome makes reversal a fresh investigation, which is the expense the record
    was supposed to remove.
12. **Six fields is the whole template, and short is the target.** A record long enough to need
    skimming gets skimmed at the field the reader needed, and the cost of length is paid by every
    future reader rather than by its author.
