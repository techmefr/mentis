---
name: ai-product-ux-pitfalls
description: "Use when the interface of a model-driven feature (assistant, suggestion, autofill, summary, classification shown to a user) is designed or reviewed: showing uncertainty and sources instead of false confidence, giving the person override, edit and undo, streaming and waiting states, what the screen does when the model is slow, wrong, refuses or is down, collecting feedback that reaches the team, and setting expectations about what the feature can do."
---

# ai-product-ux-pitfalls

A defensive block for the screens around a model's output. The three sections share one premise: **the output is
sometimes wrong, so the interface is the control: it has to show how far to trust an answer, let the person
correct it cheaply, and fail in a way that leaves the task doable**. Whether the feature meets its quality bar
before launch is `ai-feature-acceptance-pitfalls`; general interface review is in
`frontend-ux-antipattern-review-pitfalls` and `persona-ux-audit`; accessibility is in the accessibility blocks;
injection through rendered output is in `llm-app-prompt-injection-and-exfiltration-pitfalls`; disclosure duties
are in `ai-content-disclosure-and-provenance-pitfalls`.

## When
- Designing or reviewing a chat, copilot, suggestion, autofill, summary or automated decision screen.
- Users trust a wrong answer, ignore a good one, or cannot recover from an error.
- The feature is slow, rate-limited or sometimes unavailable and the screen shows a blank or a spinner.
- A team asks "how do we know people are not just accepting everything".

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Trust display: confidence, sources, scope statements, the cost of a wrong accept | an output is shown as an answer or an action | [`01-trust-and-expectations.md`](./references/01-trust-and-expectations.md) |
| 2 | Control and recovery: edit, override, undo, human gate, feedback, streaming, failure states | a person acts on, corrects or waits for an output | [`02-control-and-failure-states.md`](./references/02-control-and-failure-states.md) |
| 3 | Review checklist and measuring over-reliance | a screen is reviewed or usage data is read | [`03-review-and-signals.md`](./references/03-review-and-signals.md) |

## Output / checkpoint
For each model output on screen there is a note of what the person does with it, what a wrong output costs them,
how they see the basis (confidence, source, date), how they correct or undo it, and what appears when no output
arrives (§1, §2). The failure states (slow, refused, wrong, empty, down) each have a designed screen with a way
to continue the task without the model (§2). Over-reliance and ignoring are both measured (§3).

## Guardrails
- Never present a generated answer in the same voice and weight as a verified fact; show its basis, or label it as
  a draft (§1).
- Never show a confidence number that was not calibrated against outcomes; show a coarse, honest label or none (§1).
- Never apply a model's action without a way back; offer undo or a preview before a consequential step (§2).
- Never leave the task blocked when the model fails; keep the manual path usable (§2).
- Never treat acceptance rate as quality; read it with edits, reversals and downstream errors (§3).
- Never promise capabilities in copy that the evaluation did not cover; state what it does and does not do (§1).
- This block is mostly craft guidance; the accessibility and error-prevention points were checked against W3C
  documents. Nothing was tested with users while writing it. See [`references/origin.md`](./references/origin.md).

## Origin
Mostly own craft guidance; accessibility points checked against W3C WCAG 2.2 Understanding pages and the citation, refusal and streaming points against Anthropic and OpenAI documentation (facts only, no text copied). 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
