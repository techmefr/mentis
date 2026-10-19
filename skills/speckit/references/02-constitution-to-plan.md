# speckit §2 — Constitution, specify, clarify, plan

The first half of the cycle, in order. For each step: what it produces, and what is checked before the next.
Sources: spec-kit `templates/commands/{constitution,specify,clarify,plan}.md`, `templates/{constitution,spec,plan}-template.md`,
`spec-driven.md`.

## 2.1 Constitution
1. **Produces** `.specify/memory/constitution.md`: named principles, further constraint sections, a governance
   section (how it is amended, how it is versioned, how compliance is reviewed). It is the project's own
   rulebook, written once and amended deliberately.
2. **Versioning**: semantic. A removed or redefined principle is major, a new or materially widened one is
   minor, wording fixes are patch. The amendment carries a short report of what changed (a scratch comment to
   remove before commit).
3. **Check before moving on**: no placeholder left unexplained, principles written as testable MUST or SHOULD
   with a reason, dates in ISO form.
4. Run it once per project, then only to amend. Do not rewrite it to make a feature pass (reference 04).

## 2.2 Specify
1. **Produces** `specs/<prefix>-<name>/spec.md` from the template: prioritised user stories (P1 first, each
   independently testable and demonstrable), acceptance scenarios in given/when/then form, edge cases,
   numbered functional requirements (FR-001...), key entities, measurable and technology-agnostic success
   criteria, and an assumptions list.
2. **The what and the why only.** No stack, no library, no API shape, no file layout. The template exists to
   keep the spec readable by a non-technical stakeholder and to stop premature design.
3. **Unclear points**: make a reasonable default and record it as an assumption; mark a point as needing
   clarification only if it changes scope or user experience materially and has no sensible default; at most
   three markers, ranked scope, then security and privacy, then experience, then technical detail.
4. **It also writes `checklists/requirements.md`**, a quality checklist on the spec itself (no implementation
   detail, testable requirements, measurable criteria, bounded scope, assumptions listed), and loops on it up
   to three times.
5. **Check before moving on**: every requirement is testable, every story has its independent test, every
   criterion is measurable with no technology named.
6. Our complement (own guidance): number the acceptance criteria and never renumber them afterwards; tests,
   review and gate evidence cite them (`skills/spec` keeps that rule).

## 2.3 Clarify
1. **Produces** answers written back into `spec.md`, one at a time, from a scan of the spec by category:
   functional scope, data model, user flows, non-functional attributes, integrations, edge cases, constraints,
   terminology, completion signals, leftover placeholders and vague adjectives.
2. **At most five questions per session**, one at a time, each answerable by a short choice or a few words, each
   with a recommended answer and the reason. A question that only concerns implementation method or task
   breakdown is not asked here.
3. **The record**: after each accepted answer the spec is updated at once, in the place the answer belongs, and
   the answers are kept in a clarifications section.
4. **Skipping is allowed only for an explicit exploratory spike**, with a warning that downstream rework goes
   up. The tool states this itself.
5. **Check before moving on**: no clarification marker remains, vague adjectives are quantified or removed,
   and the operator has read the clarified spec. This is where mentis's `spec_done` is earned.

## 2.4 Plan
1. **Produces** `plan.md` plus design artifacts. A technical context (language, dependencies, storage, tests,
   platform, performance and scale targets) with unknowns marked, then a **constitution check**, then:
   - research (`research.md`): each unknown resolved as decision, rationale, alternatives considered;
   - `data-model.md`: entities, fields, relationships, validation rules, state transitions;
   - `contracts/`: the interfaces the feature exposes, in the format that fits the project type;
   - `quickstart.md`: runnable validation scenarios, not implementation code.
2. **The constitution check is a gate twice**: before research, and again after the design. An unjustified
   violation stops the plan.
3. **Check before moving on**: every unknown from the technical context is resolved, every entity in the spec
   is in the data model, the constitution check passes after design, and the plan does not copy code bodies.
4. Our complement (own guidance): `archi` still runs here (reuse versus create), and `skills/plan` step 0
   (documentation discovery: list the interfaces that really exist) fills the research file. The plan names no
   call that is not on that list.
