---
name: extract-conventions
description: Use when starting on a project or when the reference docs need refreshing, generates from the REAL CODE a draft of the observed conventions, instead of writing them by hand.
---

# extract-conventions

**Setup / maintenance** block (not a pipeline step). Makes the agents stronger by giving them
references **anchored in the real code**, and automates the recovery of a project's *internal*
knowledge. Complements `SOURCING-INBOX` (which collects *external* knowledge).

## When
When starting on a project, or to refresh the references before `review`/`code`/`archi` rely on
them. Always at a human's request.

## Steps
1. Read the real code via **graphify** + targeted reading: structure, recurring patterns, naming,
   backend responses, frontend components, design tokens actually used, test patterns.
2. Extract the **observed conventions** by domain (frontend / backend / tests / design).
3. Emit a **draft** `references/observed/<project>.md`, marked **INTERNAL** (it contains project
   specifics).
4. **Human ratification**: the dev validates / corrects. What is validated **and generic** is
   distilled (by hand) into the publishable conventions (`references/conventions-*.md`); the rest
   stays internal.
5. Replayable: running it again produces a diff against the previous version (drift becomes
   visible).

## Output / checkpoint
`references/observed/<project>.md` (internal) + a possible update of the generic conventions after
ratification. No pipeline checkpoint.

## Guardrails
- **The automation proposes, the human ratifies**: the output has no authority until it's
  validated. We extract what the code *does* (good AND bad habits) ≠ what it *should* do.
- **Internal by default** (rule C): generated from a real project → the publishable version is a
  human distillation, with no project/colleague name.
- **Read-only** on the project: we read, we never edit the code.
- **On demand**, never an automatic hook (the auto "doc-freshness" was removed on purpose).

## Origin
Internal `graphify` + a recognised market skill author (improve-codebase-architecture) + a market
generalist dev skill catalogue (source-driven-development / context-engineering), rewritten our
way.
