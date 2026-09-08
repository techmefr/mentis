# § 4 — Say when a trade-off is permanent

> Section 4 of `skills/documentation-adr`. Read it when the decision holds a tension rather than
> resolving one. This section is cited by number from `skills/design-patterns` §5 and
> `business/interface-design` §6.

1. Some decisions don't resolve a tension, they **hold it**: two things that both matter and pull in
   opposite directions (a boundary that costs indirection but keeps two teams independent, duplication
   kept deliberately because merging it would couple two lifecycles).
2. When that's the case, say so in **Consequences**: this tension is deliberate and stays. Otherwise the
   next reader sees only the cost, "simplifies" it, and rediscovers the reason the hard way — usually
   during `simplify`, which is exactly the step that trusts an ADR.
3. This is one sentence, not a section. An ADR that philosophises about tensions is worse than one that
   names the one it's keeping.
4. **The cost is what is visible; the benefit is what is not.** Indirection, duplication and an extra
   boundary are all readable in the code, and the independence, the isolation or the lifecycle they buy
   is readable nowhere. That asymmetry is the whole mechanism: without the sentence, a reader comparing
   what they can see against nothing concludes correctly from the evidence available and removes it.
5. **Name what would break, concretely.** "Keeps the two teams independent" is a claim; "merging these
   two schemas means a change in either service requires a coordinated release" is a consequence
   somebody can check against their own change. The concrete form is what survives being argued with.
6. **Say what would end the tension.** A permanent trade-off is rarely permanent forever — one team
   absorbing the other, one lifecycle disappearing, a volume dropping below the threshold that
   justified the split. Naming the condition turns a rule with no exit into one that can be retired
   deliberately (§3.5).
7. **A tension held without being named is indistinguishable from an accident.** Duplicated code that
   is deliberate looks exactly like duplicated code that nobody noticed, and every review, every
   `simplify` pass and every new reader will treat it as the second. The sentence is what changes the
   default reading, and it belongs where the reader will be standing: in the record, and where it
   matters most, in a comment at the duplication itself (§1.6).
8. **Never use this section to protect a decision from being questioned.** A trade-off named as
   permanent is still open to a reader who shows the constraint is gone, and a record that says "do not
   change this" without saying what it buys is a claim of authority rather than a reason. The
   distinction is whether the sentence can be checked.
9. **A pattern, a boundary or a duplication kept for a reason is kept by a *named* reason.** Where the
   reason lives only in the head of whoever chose it, the structure survives exactly as long as they
   are around to defend it in review — and the reimplementation that follows its removal costs more
   than the record would have (`skills/design-patterns` §6).
