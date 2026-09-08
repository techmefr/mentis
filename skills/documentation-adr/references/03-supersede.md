# § 3 — Never delete, always supersede

> Section 3 of `skills/documentation-adr`. Read it when a recorded decision is being changed, reversed
> or has quietly stopped being true.

1. An ADR is **never deleted** even if the decision becomes obsolete: a new ADR explicitly
   replaces it (`Status: superseded by ADR-0042`). Deleting it removes the only evidence that the
   question was ever settled, so the same option comes back as a fresh idea — with the same appeal it
   had the first time and none of the reasons it lost.
2. The decision history stays readable over time: understanding why we changed our mind matters as
   much as the current decision. A reversal with its reason recorded is what stops the third change
   from being a coin flip between the first two.
3. **The superseding record names the record it replaces, and the old one names its successor.** Only
   one of the two links is usually written, and it is the wrong one: a reader arrives at the old record
   through a citation in the code or in another document, and with no forward pointer they act on a
   decision that was reversed.
4. **Say what changed, not only what was decided.** A reversal is caused by something: a constraint
   lifted, a measurement taken, a dependency dropped, a volume that grew. Naming it is what lets the
   next reader judge whether *their* case is covered by the new record or by the situation the old one
   described.
5. **A decision taken under a constraint that might lift says so when it is written.** That single
   sentence converts a record that will look stale into one that is scheduled: the reader who finds the
   constraint gone knows the decision is due for review rather than wondering whether it was ever
   right.
6. **Superseding is not the same as amending.** A record whose *decision* changes is replaced; a record
   with a wrong date, a missing alternative or an unclear sentence is corrected in place. Treating a
   reversal as an edit destroys the history; treating a typo as a reversal fills the log with noise
   nobody reads.
7. **A decision that was abandoned rather than replaced still gets a status.** Work stopped, the
   problem went away, the feature was cut: without a status the record reads as accepted and binding,
   and someone will implement it. "Superseded by nothing, the case no longer exists" is a complete
   record.
8. **A superseded record stays where it was.** Moving it to an archive folder breaks every citation
   that pointed at it — from the code, from another record, from a merge request — and the reader who
   follows a dead link concludes the decision was never documented.
9. **An ADR contradicted by the code is a live defect, not a stale document.** One of the two is
   wrong: either the code drifted and should be brought back, or the decision was superseded in
   practice and never recorded. Both are findings, and the second is the one that makes the whole log
   untrustworthy — because after one silent drift, no reader can rely on any record without checking.
10. **The record is what `simplify` and a fresh reader trust.** A pass looking for cost to remove finds
    indirection, duplication and a boundary that seems gratuitous, and the ADR is the only thing that
    can say the cost is bought. That is why deleting a record has a consequence beyond history: it
    disarms the mechanism that protects the structure the record chose (§4.2).
