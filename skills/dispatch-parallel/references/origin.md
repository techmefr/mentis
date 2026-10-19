# dispatch-parallel references: origin of §1

> Provenance of `references/01-worker-status-reports.md`. Read it to trace a rule to its source, never to apply one.
> The origin of `SKILL.md` stays there.

**Status: 🟡.** Rewritten from documentation, not yet run on a real fan-out. Re-read on 2026-10-19; MIT licence file read again.

| Source | Licence | What it gave |
|---|---|---|
| `obra/superpowers`, `skills/subagent-driven-development/SKILL.md` (lines 270 to 330 and the grep of its status words, this session) and its `implementer-prompt.md` (lines 60 to end) | MIT, 2025 Jesse Vincent | The four statuses and what the controller does with each (points 1 to 10): the status line, the short final message with the detail in a report file, escalation being allowed, the handling of `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT` and `BLOCKED`, and "never retry the same worker unchanged" |

Overlap checked: `skills/execute-plan/references/01-implementer-brief.md` already names the four statuses on the
worker side (its lines 29 and 34), without the orchestrator's handling of each; §1 therefore carries the handling and
the generic worker contract, and leaves the implementer brief to that file.

## Not taken

1. The source's model choice per role and the turn-count argument for a mid-tier floor for reviewers, and the rule to use a tier above the implementer after the third fix round: the review lists them (P2.7) with `choose-model`, and none of that text was re-read for this pass.
2. Its continuous-execution and "rulings, not stalls" stance (a running plan never waits on a human, decisions are ledgered) and its no-nested-subagents contract: the first conflicts with the operator's step-by-step validation in `skills/plan` Guardrails; the second is already step 5 of `SKILL.md`.
3. Its review-package scripts and ledger files.

## Not verified

1. The lines of `subagent-driven-development/SKILL.md` outside 270 to 330 (and the first lines seen in a truncated read) were not read in full this session; nothing is claimed about them.
2. Applying the four statuses to non-implementer workers is our extension, stated as such in point 1.
3. Nothing here was run on a real dispatch.
