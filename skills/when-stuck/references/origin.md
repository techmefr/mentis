# when-stuck references: origin of §5 and §6

> Provenance of `references/05-repeated-failure.md` and `references/06-unblock-card.md`. Read it to trace a rule to
> its source, never to apply one. The origin of the inline techniques stays in `SKILL.md`.

**Status: 🟡.** Rewritten from two sources, read in full on 2026-10-19 (the MIT licence file of each clone read again). No text copied, own wording, examples replaced.

| Source | Licence | What it gave |
|---|---|---|
| `OthmanAdi/planning-with-files`, `skills/planning-with-files/SKILL.md` (all 514 lines; commit d363544) | MIT, 2026 Ahmad Adi | §5: never repeat a failed action and mutate the approach (point 1), log every error (point 2), the three-attempt protocol of diagnose, alternative approach, broader rethink, then escalate with what was tried, the exact error and a request for guidance (points 3 to 5), write findings the moment an image, PDF or browser result is viewed (point 6), external content kept in the findings file and out of the file read at every step (point 8), read before deciding and do not re-read what was just written (point 9), the reboot test and the next-step line (points 10 and 11) |
| `michalparkola/tapestry-skills-for-claude-code`, `unblock-action/SKILL.md` (whole file; commit 80e1dc5) | MIT, 2025 Tapestry Skills Contributors | §6: the output as a noun, the day-sized slice, the first action as verb and object, the best-use question, the four-line card, the short exchange |

## Decisions that are ours, not the sources'

1. **The number three.** The source gives it (its protocol stops after three failures), so it is not invented here. `debug` §4 and the systematic-debugging source it rests on already stop at three. Stated as the block's default that an operator may change (point 4).
2. **The count is per goal and restarts when the goal changes.** The source does not say what a "same failure" is. Ours.
3. **The two-operation rhythm is not taken.** The source writes findings to disk after every two view, browser or search operations and gives no reason for two. The trigger here is the moment of discovery and the start of the next phase (point 6).
4. **The notes file is never a plan.** The source keeps a plan file, a findings file and a progress file as its process. Here the plan and tasks are the spec-kit artefacts (Rule E), so only the notes (findings and failures) are taken (point 7); its plan, progress and phase files, its hooks, scripts, attestation and gating modes are not taken.
5. **The six questions are mapped to the artefacts of the cycle** (point 10). The source's table names its own files.
6. **The surviving hypothesis and the redaction** in the escalation message (point 5) come from the discarded-attempts rubric of `handoff` and from `debug` §5.8, not from the source.
7. **The unblock card is kept short and separated from the spec** (point 7 of §6), and the emoji of the source's card are dropped.

## Not taken

1. Everything in `planning-with-files` that is a runtime: lifecycle hooks, `session-catchup`, plan resolution scripts, parallel plan directories, attestation hashes, the stop gate, the `/plan-goal` and `/plan-loop` commands, templates. Rule B and Rule D.
2. The source's "create a plan first" rule: the plan is `plan.md` and `tasks.md`.
3. In `unblock-action`: the persona framing ("action-unblocking facilitator") and the style list; the card's checkmark line was rewritten as plain text.

## Not verified

1. The source titles its checkpoint the "5-question" reboot test but lists six questions, and the sixth (what am I about to do) is the one its next-step rule serves. Six are written here, as listed.
2. `reference.md` and `examples.md` of `planning-with-files` and the other skills of the `tapestry` repository were not read: nothing here relies on them.
3. Nothing in §5 or §6 was run on a real stall. The claim that three attempts differing in kind beat three variations is the source's rule of thumb, not measured here.
