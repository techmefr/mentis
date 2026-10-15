# threat-modeling-lite §1 — The four questions and how to run a lite session

> Section 1 of `skills/threat-modeling-lite`. Read it when you start a model or decide whether a change needs
> one. Restated from the Threat Modeling Manifesto website (read 2026-10-16, commit `009df64`, CC-BY-4.0, see
> `references/origin.md` for credit). Sentences marked "own guidance" are ours, not the Manifesto's.

1. **Threat modeling is analysing a representation of a system for security and privacy concerns, and it
   comes down to four questions.** The Manifesto defines it that way and lists the questions: what are we
   working on, what can go wrong, what are we going to do about it, and did we do a good enough job. It credits
   the frame to Adam Shostack. Every session in this block answers them in that order, in writing.
2. **The fourth question needs evidence you can point at.** The Manifesto asks it and gives no test. Own
   guidance: "good enough" means each threat has a decision, an owner and a follow-up that can be checked (a
   test, a configuration value, a review item), and that someone who did not design the change read the
   result. A session that ends after the second question has found problems and decided nothing.
3. **Model the change, in an iteration, early.** The principles say threat modeling pays most when it is early
   and frequent, and that it should follow design changes in iterations, each scoped to a manageable portion of
   the system and aligned with how the organisation develops. Own guidance: the unit is the change you are
   about to make (one new boundary, one new store, one new integration), not the whole architecture.
4. **Dialog first, then a short record.** The Manifesto says dialog establishes the common understanding that
   gives threat modeling its value, while documents record those understandings and make them measurable, and
   that the outcome matters when it is valuable to stakeholders. Own guidance: hold the session with the people
   who built or will build the change, and keep the record to one page that those people will actually reopen.
5. **Invite different viewpoints, and do not wait for an expert.** One of the Manifesto's patterns is varied
   viewpoints: a diverse team with the right subject-matter experts and cross-functional collaboration. It says
   everyone who cares about the privacy, safety and security of a system should threat model, and names
   dependence on one gifted person as an anti-pattern (§3.9). Own guidance: pair the author of the change with
   someone who runs the system and someone who did not design it.
6. **Keep refining; do not deliver once.** The Manifesto values continuous refinement over a single delivery
   and a journey of understanding over a snapshot. Own guidance: write down the events that reopen the model, for
   example a new trust boundary, a new class of data, a new external caller or a new dependency that runs code
   at build or run time, and check for them when the design changes.
7. **Value finding and fixing design issues over ticking a compliance box, and doing over talking.** Two of the
   Manifesto's values. In practice a model counts when it changed the design or produced a decision, not when
   a template was filled in.
8. **The Manifesto is not a method.** It says it contains ideas, is not a how-to and is methodology-agnostic. The
   process in this block (§2 and §3) is a lite one of our own that stays inside those ideas; a team with a
   method it already uses should keep it and borrow only the questions and the checks above.
