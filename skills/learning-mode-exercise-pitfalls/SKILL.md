---
name: learning-mode-exercise-pitfalls
description: "Use when a short learning exercise is offered to a developer after AI-assisted work (a new module, a schema change, a refactor, a design decision) or when someone asks to understand code better: offering without imposing, one short question that ends the message, no hints or example answers after the question, honest feedback that credits only what the learner said, exercise shapes (predict then observe, generate then compare, trace, debug, teach back, retrieval check), directing the learner to the file, and fading the question setup."
---

# learning-mode-exercise-pitfalls

Not a step of the pipeline: an **opt-in mode**, never entered on its own. The premise: **code that was
generated fluently feels understood, and the developer can ship what they cannot explain**; a short exercise
where the learner produces the answer first is the cure, and a "quiz" that leaks its own answer is not one.
This block is about how to run the exercise; whether to offer one at all is the learner's decision.

## When
- A feature, new module, schema change or refactor has just been completed and the user wants to understand
  the design, or has asked "why" during the work.
- The user asks for a quiz, an exercise or a way to check their understanding of the code.
- A returning session on a long project, where a short recall check would help.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Offering, declining, the hard stop after a question, feedback | an exercise is about to be offered or a question is about to be asked | [`01-offer-and-pause.md`](./references/01-offer-and-pause.md) |
| 2 | Exercise shapes, pointing at files, fading the setup, rationale | an exercise is being designed or the learner is stuck | [`02-exercises-and-scaffolding.md`](./references/02-exercises-and-scaffolding.md) |

## Output / checkpoint
Read the message that contains the question and check that it ends right after the question, with at most a
content-free reassurance and an escape hatch: no hint, no example answer, no second question. After the
learner's answer, check that the feedback says plainly what was wrong and credits no insight they did not
state. Nothing here was run with learners.

## Guardrails
- Never start an exercise without asking, and never keep offering after a decline or after two exercises in
  a session (§1.1).
- Never add a hint, a model answer, an italic clue or a second question after the pause point (§1.2).
- Never say the learner understood something they did not express (§1.3).
- Never respond to a struggling learner with a hint; make the question more specific (§2.3).
- Study results behind the method are the author's, summarised from headings only; this block quotes no
  figures (§2.4).
- Ten to fifteen minutes and two exercises per session are one author's defaults, shown as examples.

## Origin
Rewritten from "learning-opportunities" by Dr. Cat Hicks (CC-BY-4.0, https://github.com/DrCatHicks/learning-opportunities),
its SKILL.md read in full and the headings of its PRINCIPLES.md, 2026-10-16. Changes were made: the text is
reworded and shortened, and none of it is the author's endorsement of this block. 🟡: never run by us; open
points are in [`references/origin.md`](./references/origin.md).
