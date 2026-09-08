# § 3 — Acceptance criteria: the contract for `tdd`

> Section 3 of `skills/spec`. Read it when turning a ready story's criteria into the contract the tests
> will be written from. What makes a *business* criterion valid is
> `business/product-ownership` §4 — this section is about what `tdd` needs on top of that.

1. **The criteria listed here become the contract for `tdd`.** That is the whole reason they are written
   at this step rather than assumed: the next step in the pipeline writes failing tests from this list,
   so a criterion missing here is a behaviour nobody tests, and a criterion phrased loosely here becomes
   a test of whatever the implementer assumed.
2. **Every criterion is given/when/then, with the given fully stated.** The "given" is the part that
   gets skipped and the part that decides the test: which user, with which permission, with what already
   in the database. A criterion whose starting state is implicit is satisfied by a test that arranges the
   most convenient one.
3. **Name the fixture each criterion needs.** "Given a customer with three expired contracts" requires
   that arrangement to be buildable — a factory, a seed, an anonymised extract. Deciding it here is
   cheap; discovering at `tdd` that the case cannot be built is a blocked step, and the usual workaround
   is a test of a simpler case wearing the criterion's name.
4. **A criterion states an observable, and says where it is observable.** A row written, a response
   field, a rendered line, an email sent, an event dispatched: five different assertions, at five
   different levels of the system, and the choice determines the test's tier
   (`code-baseline` §8, the stack block's testing section). Left unsaid, the cheapest one wins.
5. **Include the refusal cases as criteria, not as notes.** The invalid input rejected with the intended
   message, the missing permission refused visibly, the concurrent second attempt losing cleanly. These
   are behaviour, they are what a test can pin down, and they are exactly what a demo never shows.
6. **A criterion must not name the implementation.** "The total is recalculated when a line is removed",
   not "the recalculate method is called". The second locks the design, dates immediately, and turns a
   legitimate refactor into a red test — which is how a suite starts getting edited to match the code
   rather than the other way round.
7. **A performance or volume criterion carries its number and its conditions**, because a test needs
   both. "Under a second for 10,000 rows" is testable; "fast" produces either no test or a test whose
   threshold somebody picked silently and everybody later raises.
8. **Criteria are numbered and stable.** The tests will cite them, the review will cite them, and the
   gate's evidence will cite them; renumbering mid-flight breaks all three quietly. Add at the end, and
   mark a withdrawn criterion as withdrawn rather than deleting it.
9. **A criterion that cannot be tested at this level says so, and says what covers it instead.** Some
   things are genuinely only verifiable by a person or by a browser pass — a layout, a printed document,
   a third party's sandbox. Naming the coverage (a `qa-exploratory-testing` case, a manual step) is
   honest; leaving it in the list as if `tdd` will handle it is how it ends up covered by nothing.
10. **Do not restate the story's criteria in different words.** Where the story is already precise, cite
    it; where it is not, the correction goes back to the story (`business/product-ownership` §4) rather
    than being fixed silently here — otherwise two documents state the contract and they disagree by the
    second edit.
11. **The count is a sizing signal.** Twenty criteria for one story usually means two stories, and the
    one-MR test settles it (`business/product-ownership` §8.2). Discovering that here, before `tdd`
    starts, is the last cheap moment to split.
12. **A criterion added after the tests are written is a change, handled as one.** It is normal — the
    interview did not catch everything — but it is recorded as an addition with its own decision, not
    slipped in. The alternative is a spec that always matched the code because it was edited to.
