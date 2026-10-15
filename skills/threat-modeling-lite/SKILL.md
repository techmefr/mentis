---
name: threat-modeling-lite
description: "Use when a feature, integration or architecture change adds a trust boundary, a new data flow, a new store of sensitive data or a new way in, and the design is still open (not after the code review): a one-session threat model built on four questions, a data-flow sketch with trust boundaries, design-risk prompts, and a recorded decision for each threat."
---

# threat-modeling-lite

A small, repeatable way to find design flaws while they are still cheap to change. It follows the Threat Modeling
Manifesto's four questions and borrows the vocabulary of an open-source threat-model toolkit (assets, data flows,
trust boundaries, risk decisions) for the sketch and the prompts. It is deliberately light: one change, one
session, one page. `skills/security-hardening` is what you apply while writing the code that results;
`seraph` audits a repository afterwards; this block is the step before both, when the shape of the change can
still move. Defensive use only.

## When
- A change adds a service, a queue, a store, a third-party integration, a new caller or a new kind of data.
- A change moves data across a boundary it did not cross before (a new network, a new tenant, a new vendor).
- A design review is about to start and nobody has written down what could go wrong.
- A previous model exists and the design it describes has since changed.

## Steps

**Read the section for the phase you are in.** They run in order for a new model.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | The four questions, values and principles as working rules, scope and who takes part | you are starting, or deciding whether a change needs a model | [`01-four-questions.md`](./references/01-four-questions.md) |
| 2 | The sketch: assets, data, flows, trust boundaries, confirming it with the owner | you are drawing what the change touches | [`02-sketch.md`](./references/02-sketch.md) |
| 3 | Threat prompts, decisions and the anti-patterns | you are asking what can go wrong and recording what you will do | [`03-threats-and-decisions.md`](./references/03-threats-and-decisions.md) |

## Output / checkpoint
One page, kept next to the code: the scope of the change, the sketch with its trust boundaries marked, the
list of threats found (each with the boundary it crosses, the decision taken and who owns it), an answer to
each of the four questions, and the event that will reopen the model. Evidence that it was done and not just
written: every decision names a follow-up that can be checked (a test, a configuration value, a review item),
and at least one person who did not design the change took part.

## Guardrails
- Never skip the fourth question; a model with no check that it was good enough is a document, not a result
  (§1.2).
- Never model the whole system when the change is one boundary (§1.3).
- Never present one person's one-time document as the threat model (§1.6, §3.9).
- Never treat a tool's list of risks as the outcome; each needs a human decision recorded (§3.8).
- Never put real secrets, customer data or production hostnames in the model file (§2.5).
- Do not stop at naming the problem; each threat ends in a decision, even if the decision is to accept it
  (§3.9).

## Origin
Rewritten from the Threat Modeling Manifesto website (CC-BY-4.0, credit below and in `references/origin.md`)
and the model and risk-rule documentation of the Threagile toolkit (MIT), read 2026-10-16. The four-question
frame is credited by the Manifesto to Adam Shostack. This is a restatement with additions of our own, not the
Manifesto, and the Manifesto's authors have not endorsed it. The full provenance, what was removed and what is
our own guidance are in [`references/origin.md`](./references/origin.md). 🟡: never run by us.
