# § 4 — Acceptance criteria are a test, or they're decoration

> Section 4 of `business/product-ownership`. Read it when writing the criteria of a story, and when
> accepting delivered work against them. The technical specification that follows is `skills/spec`.

1. **Each criterion must be checkable by someone who didn't write the code**: given this, when that, then
   this observable result. If nobody can verify it, it isn't a criterion. The test is mechanical: hand it
   to a person who has never seen the feature and ask whether they could say yes or no without asking a
   question.
2. **Criteria are the test cases.** They feed `skills/tdd` and `skills/qa-exploratory-testing` directly,
   which is what makes writing them properly worth the time rather than a formality. It is also the
   cheapest quality lever available to whoever writes the story: a criterion written precisely becomes a
   test, and a criterion written loosely becomes a test of whatever the developer assumed.
3. **Include the unhappy paths** — the invalid input, the missing permission, the empty state. These are
   where the disagreement about "done" actually happens. They are also the paths a demo never shows, so
   if they are not written down they are not built and nobody notices until a real user finds them.
4. **Name what's explicitly out**, so the boundary is a decision rather than an omission discovered at
   review. The sentence that costs nothing to write is the one that prevents the review where somebody
   says "obviously it should also do X".
5. **A criterion containing "correctly", "properly", "as expected" or "user-friendly" is not a
   criterion.** Those words are where the disagreement hides: everyone reads them as their own version
   and the conflict surfaces at acceptance, when the code is written. Replace the word with the
   observable thing it stands for, or discover that nobody knows what it stands for — which is the more
   useful outcome.
6. **Say what is observable and where.** A row written to the database, a line changed on the screen, an
   email received, an event emitted: these are four different claims, they are verified by four different
   people, and a criterion that does not say which one it means will be satisfied by the cheapest of
   them.
7. **A criterion that needs data nobody has is not startable.** "Given a customer with three expired
   contracts" requires that customer to exist somewhere the work can be checked; the fixture, the seed
   or the anonymised extract is part of the story, not a detail for later. Otherwise the criterion is
   verified against a hand-made case that happens to work.
8. **A performance criterion carries the number and the conditions.** "Fast" is not checkable; "the list
   returns in under a second for an account with 10,000 rows" is, and it also tells the developer which
   part of the design is constrained. Without both halves it will be argued about at acceptance, with
   each side having measured something different.
9. **Criteria describe behaviour, never implementation.** "The price is recalculated when the quantity
   changes", not "the recalculate method is called from the change handler". The second one locks the
   design, dates immediately, and turns a legitimate refactor into a failed criterion.
10. **A criterion about a permission has two halves.** The allowed case works, and the refused case is
    refused *visibly* — with the response the product intends, not a blank page or a 500. Written as one
    half only, it is satisfied by code that authorises nobody or by code that authorises everybody,
    depending on which half was written.
11. **Count them.** A story with twenty criteria is usually two stories, and the sizing test in §8.2 will
    say so. It is also a story nobody will read to the end, which means the criteria at the bottom are
    decoration whatever their quality.
12. **Acceptance happens against the criteria as written.** Not against what everyone now remembers
    wanting, and not against what the demo revealed would have been nicer. A criterion that turns out to
    be wrong is fixed as a new item with its own decision — changing it during acceptance destroys the
    only fixed reference the work had.
