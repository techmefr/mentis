# product-ownership §10 — The whole-feature edge-case catalog

> Section 10 of `business/product-ownership`. Read it when a feature is specified but nobody has yet listed what
> can go wrong across the whole of it, before the build starts or while a test plan is being drafted. Per-story
> criteria stay in §4; this section is the sweep over the feature that §4 cannot do one story at a time. 🟡:
> rewritten from one public source, not yet run on a real feature.

1. **The catalog is a separate document from the criteria, on purpose.** A story's criteria (§4) check one
   slice from the inside. A failure that belongs to no single slice (two users editing the same record, a
   timeout between step two and step three, a quota reached halfway through an import) appears in none of them
   and is therefore tested by nobody. The catalog covers the feature as a whole and feeds the criteria
   afterwards: a catalogued case that matters becomes a criterion on the story that owns it.
2. **Start by fixing the scope in a sentence.** The same input is fine in one flow and an error in another, so
   an edge case only exists relative to a named feature. If the scope cannot be said in a sentence, the feature
   is not specified enough to be swept (§5 ready), and the gap goes back to the story, not into a catalogue of
   guesses.
3. **Walk the sweep in a fixed order, one pass per family.** Inputs (empty, too long, wrong format, special
   characters, the smallest and largest valid value), boundaries (zero, one, the limit, one past it, page
   edges, time-outs, rate limits), error states (network down, permission refused, resource gone, session
   expired), concurrency (two actors at once, a double submit, data changed between load and save), recovery.
   A fixed order is what makes a gap visible: a family with no entry has been skipped or judged irrelevant, and
   the document says which.
4. **Every case is written as scenario plus intended behaviour.** "Session expires mid-form" is a prompt, not a
   case; the case also says what the user sees, whether what they typed survives, and what they can do next.
   A case with only the failure half is detection without design, and the developer fills in the other half
   with whatever is cheapest.
5. **Recovery is its own pass, not a column added at the end.** For each error state, answer three things: can
   the user retry, is their data kept, and what do they read. An error with no recovery path is a dead end by
   design, and it is much cheaper to learn that from a list than from a support queue.
6. **Rank by likelihood and by impact, separately, then together.** A common and harmful case gets robust
   handling and a test. A rare and harmless one gets a graceful failure and a line in the catalogue. The two
   mixed cases (rare but destructive, frequent but trivial) are where the decision is made, so those are the
   ones the author names and argues, not the corners of a grid. Impact includes data loss and security
   exposure, which outrank inconvenience in the same way as in §2.
7. **A sweep is bounded by the feature, not by imagination.** Stop when each family has been walked once and
   each ranked case has an owner; a catalogue that tries to be exhaustive is never finished and is not read.
   What the sweep missed is expected to be found later, which is point 8.
8. **A defect found after release is added as a case, with its family.** The catalogue is the memory of the
   failure surface; a production bug that has no entry is also a sweep gap, and noting which family it fell
   through teaches the next sweep where to look harder.
9. **Hand-off.** The catalogue goes to whoever builds (so the cases are designed, not discovered) and to
   whoever tests (`skills/qa-exploratory-testing` §2 techniques are the manual counterpart; its charter can
   be one family of this catalogue). Where the author is also the builder (§9), do the sweep as a separate pass
   after the criteria are written, not interleaved with them.
