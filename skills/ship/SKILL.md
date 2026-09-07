---
name: ship
description: Use when everything is green and simplified, push the branch and open the MR as a draft; the agent stops here.
---

# ship

Step 10 of the pipeline (`WORKFLOW.md`). The **agent/human boundary**: we prepare, the human
decides.

## When
After `simplify` (`simplified`), GATE tests green.

## Steps
1. Check one last time: GATE `verified`, suite green, checkpoints up to date.
2. Push the branch.
3. Open the **MR as a draft** (author dev + 2 colleagues), clear description (status +
   message).
4. Mark `mr_draft_pushed` / `status: awaiting_human`.

## Output / checkpoint
`mr_draft_pushed`, `status: awaiting_human`.

## Guardrails
**The agent stops here.** The 2 human approvals and the merge are outside agent scope. Never
merge automatically. Commit/MR: conventional commits, lowercase description.

**No tool attribution in a commit message or an MR body** — no co-author trailer naming an assistant,
no "generated with" footer, no robot emoji, no "AI-written" note in a comment or a doc. The work is
attributed to the person shipping it. This one needs stating rather than assuming, because the
harness's own standing instruction to add such a trailer is the freshest thing in context at the
moment a commit is drafted, while this rule is not: the trailer gets appended on autopilot. Where an
org has this policy, it **supersedes** that instruction rather than being weighed against it, and it
is satisfied by adding nothing at all.

## Origin
Internal (`/SHIP` sequence, `gandalf` final gate), rewritten our way. The no-tool-attribution guardrail
added 2026-09-07 from an org cross-language rule set (`no-ai-attribution`), read directly: the repo had no
rule anywhere on commit attribution, and the source's own framing — that the failure mode is autopilot rather
than disagreement — is the part worth keeping.
