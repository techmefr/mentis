# § 1 — Recognise, don't apply

> Section 1 of `skills/design-patterns`. Read it before introducing any named pattern, and when a design
> discussion has produced a pattern name as its answer.

1. **A pattern earns its name after the structure exists**, not before. If the code already has three
   interchangeable behaviours behind one call site, that's a Strategy — naming it helps everyone read it.
   The name is doing one job at that point: telling the next reader that the shape they are looking at is
   a known one, so they stop looking for the special reason it exists.
2. **If it doesn't exist yet, you're predicting.** That's `yagni` (`over-engineering-review`), and the
   pattern name is the disguise. The prediction is usually wrong in a specific way: the axis you guessed
   is not the axis the second case actually varies on, so the interface has to be reshaped anyway — and
   now there is an interface, a factory and three call sites to reshape rather than one function.
3. **The threshold is the second real case**, in the code, today. Not a plausible one. Same rule as
   `when-stuck`'s three-occurrence threshold for extracting an abstraction. "Real" means a case someone
   has asked for and someone will read: a ticket, a customer, a second provider that is already being
   integrated. A case in a roadmap slide is not in the code.
4. **The order of operations is duplicate, then observe, then name.** Write the second case as its own
   code, even where that means two similar functions living side by side for a week. The duplication
   shows you which parts actually differ, which is the information the abstraction needs and the
   information you do not have before writing it. An abstraction extracted from one example encodes
   that example's accidents as if they were the rule.
5. **Naming a pattern in a review is a claim about the code, and it has to be checkable.** "This should
   be a Strategy" is not reviewable; "these three branches on `channel` are already a Strategy, and
   naming it lets each one own its tests" is. If the remark cannot point at the existing structure, it is
   a preference, and it should not block the diff.
6. **A pattern is harder to delete than the code it replaced**, which is the asymmetry that makes the
   threshold worth defending. Unstructured code that turns out to be wrong gets rewritten by whoever is
   annoyed by it; a named pattern looks like a decision somebody made deliberately, so the next reader
   assumes there was a reason and works around it. That is how a one-caller interface survives three
   years.
7. **The pattern has to make the code smaller today, not merely more extensible.** Extensibility is a
   claim about the future; line count and reading path are observable now. If adding the pattern adds a
   file, an interface and a registration and removes nothing, it has bought a possibility and paid in
   certainty (`over-engineering-review`'s net-line test).
8. **Reaching for a pattern when the problem is a bad name is the common misdiagnosis.** A function
   nobody can follow is often not missing a structure — it is missing three well-named local functions
   and one honest parameter name. Try the rename first: it costs minutes, it cannot be wrong in a way
   that outlives the diff, and it frequently makes the pattern unnecessary.
9. **Two patterns arriving in the same diff is a signal to stop.** A Factory that builds a Strategy that
   feeds a Pipeline is three indirections introduced before any of them has a second case, and the
   review can no longer judge them separately — each is justified by the presence of the others. Land
   one, live with it, and let the next real case decide the next.
10. **A pattern from a language you are not writing in is usually already solved by the one you are.**
    Half the classic catalogue exists because C++ and early Java had no first-class functions, no
    closures and no sum types. Before reaching for a class hierarchy, ask what the language itself
    offers — §2 is that pass in full.
11. **The catalogue's own framing is a trap worth naming.** Each pattern page describes the problem the
    pattern solves and the benefits of using it; almost none says "and here is when this is the wrong
    call". Read a catalogue and you will find a pattern that fits, because the pages are written to be
    findable. That is why the entry conditions in §4 are stated as triggers rather than as descriptions.
12. **Where an installed house catalogue owns a pattern's shape, this section still owns whether.** The
    two questions are separable: how the Strategy is wired in this house style is theirs, and whether
    there is a second real case is the one nobody else is asking. Apply both, and never turn the
    division into a reported conflict — write what the governing rule requires and move on.
13. **The rule for a lifecycle you are extending is not the rule for one you are writing.** Everything
    above is about introducing a pattern; most work arrives on code that already has the shape without
    the name — a status column with a `switch` in four places, a constructor that grew, a sequence of
    steps in one method. Two rules then, and they are the opposite of each other: do not introduce the
    pattern in the same change as the behaviour, because a reviewer cannot see which of the two broke
    the tests; and do not add the fifth branch to the `switch` either, on the grounds that refactoring
    was out of scope. What fits in a normal change is the behaviour, plus a named place for the next
    person to land in — and the refactor as its own change, with the tests written against the existing
    behaviour first (`skills/tdd`), because a pattern extracted from code nobody pinned is a rewrite
    wearing a refactor's name.
