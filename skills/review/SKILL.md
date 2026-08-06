---
name: review
description: Use when the GATE is green, before simplification, review along two parallel axes (Standards + Spec) then a pass by the Xefi agents.
---

# review

Step 8 of the pipeline (`WORKFLOW.md`). Two independent viewpoints that don't pollute each
other.

## When
After `gate` (`verified`), before `simplify`.

## Steps
1. Run **two subagents in parallel** (separate contexts, no cross-pollution):
   - **Standards axis**: Xefi conventions + code smells (reuse, simplification, duplicated
     CSS).
   - **Spec axis**: is the diff **faithful to the ticket / the spec**? (which the native
     `/code-review` doesn't cover). Clean skip if there's no spec.
2. Aggregate both side by side.
3. A pass by the **Xefi agents** in the dev's usual style: `aragorn`/`gimli`/`legolas` then
   `valerianus` (triage, rewording, no pointless arguments).
4. For depth: native `/code-review` + `/security-review` (gandalf as the final gate).

## Output / checkpoint
`reviewed`.

## Guardrails
The two axes stay **independent** (no shared context). We invoke the native tooling, we don't
reimplement it. Plain comments, no emojis/arrows, lowercase at the start of a sentence.

## Origin
A recognised market skill author (non-polluting two-axis code review) + Xefi agents + native,
rewritten.
