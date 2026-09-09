# spec — origin and source stamps

> Provenance of `skills/spec`. Read it when a rule has to be traced back to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

A recognised market skill author (grill-with-docs → `CONTEXT.md` + ADR) plus an internal
`spec-clarification` skill, rewritten. Mechanisms rewritten, no copied text.

**Sectioned and deepened 2026-09-08.** The block was 140 rules words — five numbered steps and nothing
else — and it is the smaller of the two blocks in `CATALOG.md`'s `project-management` row. The five steps
became five sections under `references/` with a router table in `SKILL.md`, in the same order: the
interview, `CONTEXT.md`, the criteria, the exclusions, the ADRs.

**Why this block was so thin, and what the depth actually adds.** As a pipeline step it was written as a
procedure — do these five things — which is enough for an agent that already knows what each one is for
and useless to one that does not. The five steps name deliverables; what they never said is what makes
each deliverable *correct*, which is the part a reader has to get right under pressure. Nothing was
removed and no step was reordered.

Where the boundary with the neighbouring blocks sits, stated explicitly for the first time in this pass:
`business/product-ownership` owns whether the work should exist and what the story says (its §4 owns what
makes a *business* criterion valid); this block turns a ready story into the technical contract; `tdd`
writes failing tests from §3 here. §3 therefore points at `product-ownership` §4 rather than restating it, and
says so — the previous version of both blocks each described acceptance criteria without saying which of
them was authoritative.

The additions worth citing:

- **§1**: asking about the case that decides rather than about the feature; interviewing the unhappy
  paths first, since the happy path is the part already described and agreed; not asking what the code
  can answer; recording answers in the words that were used, because a paraphrase makes a
  misunderstanding invisible; distinguishing "not decided" from "not said", which is the difference
  between a question and a decision that needs an owner; and stopping when the remaining questions no
  longer change what gets built.
- **§2**: one term, one definition, one spelling, because two words for one concept split every search
  and survive into column names; a definition stating what the term *excludes*, which is the half that
  settles arguments; separating rules imposed from outside from rules we chose, since only the second
  can be traded away in a scope discussion; naming what happens to the child when the parent goes; and a
  term colliding with an existing one in the codebase being recorded rather than silently overruled.
- **§3**: the "given" being the part that gets skipped and the part that decides the test; naming the
  fixture each criterion needs, because discovering at `tdd` that the case cannot be built is a blocked
  step whose usual workaround is a test of a simpler case wearing the criterion's name; saying *where*
  the result is observable, which is what picks the test's tier; criteria being numbered and stable,
  since the tests, the review and the gate's evidence all cite them; and a criterion that genuinely
  cannot be tested at this level naming what covers it instead.
- **§4**: writing each exclusion at the moment it comes up; excluding the *adjacent* thing by name,
  because the exclusions that matter are the ones a reasonable person would have assumed; an exclusion
  that is really a dependency being labelled as one; non-functional expectations being explicitly in or
  out, since silence is read as "not required" by the implementer and "obviously required" by whoever
  asked; and never hiding an undecided question inside the exclusion list.
- **§5**: structural meaning expensive to reverse; recording the constraint that decided it rather than
  the preference, because a preference does not survive its author; a decision taken under a constraint
  that might lift saying so, which converts a stale decision into a scheduled one; a deliberate
  *non*-decision earning an ADR too, since the absence is invisible in the code; and a superseded ADR
  being marked rather than edited.

Router plus sections: 140 → 3,689.

**Status.** The two sources behind the original five steps are unchanged and still stand. The depth is
ours: written from this repo's own pipeline experience — what goes wrong at step 2 and shows up at `tdd`
or at the gate — rather than from a source that can be re-checked.
