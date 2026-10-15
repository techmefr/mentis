# receiving-review-pitfalls §1 — Before implementing anything

Review feedback arrives as a list. The mistakes of this section all come from acting on the list before it is
understood and checked: applying the clear items while the unclear ones change their meaning, or applying a
suggestion that was never tested against the code it targets.

## 1.1 Read it all, restate it
1. **Read the whole of the feedback before acting on any part.** The source's first two steps are to read it
   completely, then to restate each requirement in your own words or ask about it.
2. **Restating is the test of understanding.** A requirement you cannot restate is an unclear item (§1.2).

## 1.2 One unclear item stops the batch
1. **If any item is unclear, implement none of them yet and ask about the unclear ones.** The reason the source
   gives: items may be related, and partial understanding produces a wrong implementation.
2. **Worked case.** The reviewer writes "fix 1 to 6" and you understand 1, 2, 3 and 6. The wrong move is to apply
   those four and ask about 4 and 5 afterwards, because 4 or 5 may change what 1 to 3 should look like. The right
   reply names what is understood and what is not: items 1, 2, 3 and 6 are clear, 4 and 5 need an answer first.

## 1.3 Check each suggestion against the code
The source applies these checks to feedback from outside reviewers, and treats instructions from the person directing
the work as trusted once understood, with a question when the scope is unclear. **Decision:** this block applies the
checks to any reviewer's suggestion that changes behaviour, and keeps the source's rule for the person directing the
work. Where the two overlap, a suggestion from a peer reviewer is checked.
1. **Is it correct for this codebase and this stack?** A suggestion can be right in general and wrong for the
   framework, the version or the layer it lands in.
2. **Does it break existing behaviour?** Run the tests that cover the code it touches, or read its callers.
3. **Is there a reason the code is as it is?** Look at the history, the surrounding comments and the tests before
   undoing it. Compatibility and platform constraints are the usual reasons the source names.
4. **Does it work on all the platforms and versions the code supports?**
5. **Does the reviewer have the full context?** A reviewer reading the diff may not see the constraint outside it.

## 1.4 When you cannot verify
1. **Say that you cannot, and say what you would need.** The source's wording is the shape: you cannot verify the
   point without a named thing, and the choice between investigating, asking and proceeding is put to the reviewer.
2. **A suggestion that conflicts with an earlier decision of the owner of the design: stop and discuss it first.**
   The source states this for the person who directs the work; the generalisation to any prior design decision is
   ours.

## 1.5 "Implement it properly" starts with a usage search
1. **When the reviewer asks for a proper implementation of a feature, search the codebase for real usage first.**
2. **Nothing uses it: propose removing it instead of hardening it**, and ask whether there is a use you cannot see.
3. **Something uses it: implement it properly.**
4. **Source's example:** a reviewer asks for proper metrics tracking with a database, date filters and an export; a
   grep finds nothing calls the endpoint; the reply proposes removing it and asks whether usage exists elsewhere.
