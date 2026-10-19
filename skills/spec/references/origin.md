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

**Widening, 2026-09-10 — pass élargie.** Two sections widened with points added after the existing
numbering, none renumbered: §1 (the interview) and §4 (out of scope). Sourcing: public requirements-
elicitation practice (structured versus open interview technique, cognitive bias in elicitation —
anchoring, confirmation bias — and the "five whys" method for reaching the underlying constraint) for §1;
public scope-management practice (the won't-have versus deferred distinction, scope-creep prevention
through explicit boundary documentation) for §4; both synthesised into this block's own voice, with the
cross-references back into this file's existing points and into `business/product-ownership` written for
this pass rather than carried over from any source.

**Widening, 2026-09-10 — second pass, closing the `project-management` gap.** Two more sections widened,
points added after the existing numbering: §5 (ADR) and §2 (`CONTEXT.md`). Sourcing: public ADR practice
(handling a reversed decision, a disagreement between teams, a framework-default non-decision, a
prototype's decisions not surviving into production, attributing a reason to a person rather than a
constraint) for §5; public requirements/vocabulary practice (borrowed synonyms across features, explicit
range boundaries, entity-identity questions, role-dependent term splits, rule exceptions kept with the
rule, units on numbers) for §2 — both synthesised into this block's own voice, no org-private marketplace content
read or referenced.

**Widening, 2026-10-02: §6 and §7.** §6 (the fresh-context review of the written spec) is the mechanism of the
spec-document-reviewer prompt in the `brainstorming` skill of `superpowers` (MIT, read that day): a read-only
reviewer, five axes, calibrated to serious gaps, a fixed short output. §7 (the feasibility verdict) is the
GO, CONDITIONAL, NO-GO gate of the research-plan-implement workflow in `claude-code-best-practice` (MIT, same
day). The guardrail on ticket text as data is a principle found in several of the repositories read that day.
All rewritten in our own words, no text copied.

**Widening, 2026-10-19: §6 points 8 to 12 (cold-reader question pass).** From the `brainstorming` skill of `superpowers` (MIT, 2025 Jesse Vincent), `SKILL.md` and `builder-check-prompt.md` both re-read in full that day: a fresh reader plays a builder who cannot reach the author and reports only the questions whose wrong guess would matter, the three piles (answered already, minor, theirs), one round of questions, the hand-over with a list of calls made, and the self-read fallback. Rewritten in our own words; no text copied. Status 🟡.

Owner block chosen: `spec` §6, not `brainstorm`. §6 already owns the fresh-context review of the written spec and `brainstorm` step 5 already points to it, so the pass is one more check on the same artefact at the same moment. Point 10 is ours: the source lets the author settle a minor question and mark it as a call, which would collide with §1.7, so the minor pile is restricted to choices that change neither behaviour nor tests.

Other `brainstorming` mechanisms checked and not added because already owned: one question per exchange and an open question before a menu (`§1` points 1 and 14), class sizing and re-sizing when the work grows (`skills/brainstorm` step 0), guesses marked as guesses in a write-back (`skills/brainstorm` step 1, `§1.8`), a spike allowed only if labelled throwaway (`skills/brainstorm` step 0 and its table). Not taken: the visual companion (a local server and a browser, a runtime dependency, already declined in `skills/brainstorm`), the first-message opt-out line and the "people may not have finished working out what they want" framing, which are voice rather than mechanism.

Not verified: the spec-document-reviewer prompt of that source was not part of this read (the five axes of points 1 to 7 stay as written on 2026-10-02); `docs/superpowers/specs/2026-10-05-brainstorming-rebuild-design.md` was not read.

