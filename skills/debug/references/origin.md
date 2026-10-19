# debug references: origin of §5

> Provenance of `references/05-feedback-loop-first.md`. Read it to trace a rule to its source, never to apply one.
> The origin of sections 1 to 4 stays in `SKILL.md`.

**Status: 🟡.** Rewritten from two sources, re-read in full on 2026-10-19 (MIT licence file of each clone read again). No text copied, own wording.

| Source | Licence | What it gave |
|---|---|---|
| `mattpocock/skills`, `skills/engineering/diagnosing-bugs/SKILL.md` (whole file) | MIT, 2026 Matt Pocock | Points 1 to 10 and 12 to 16: the loop as phase one, the ranked ways to build one, tightening, flaky bugs, the completion criterion, no hypothesis before it, minimising, unique log tag, perf baseline, the correct-seam rule, cleanup and stating the right hypothesis; the redaction rule (point 8); the ranked falsifiable candidates of point 11 |
| `obra/superpowers`, `skills/systematic-debugging/SKILL.md` (whole file) | MIT, 2025 Jesse Vincent | Compared before writing, since it is the origin of the existing native block: one hypothesis, smallest change, one variable at a time, stop after three failed fixes and question the structure. It supports keeping `SKILL.md` §1 and §4 as they are |

## Reconciling the two sources (ours, not the sources')

`diagnosing-bugs` generates 3 to 5 ranked falsifiable hypotheses before testing any. `systematic-debugging` and `SKILL.md` §1 hold one hypothesis at a time. §5 keeps §1 as the rule for a fix attempt and says the loop is its precondition (the intro of the section). The ranking is taken only for ambiguous or intermittent failures, and each candidate is still tested alone under the one-variable rule (point 11). That restriction is our decision; neither source states it.

## Not taken

1. The source's step of showing the ranked list to the user before testing: a checkpoint that depends on a person being present, left to the operator (`SKILL.md` §4 already escalates after repeated failures).
2. The source's reference to a glossary file and to ADRs when exploring: `spec` and `domain-modeling` own them.

## Not verified

1. `scripts/hitl-loop.template.sh` of `diagnosing-bugs` was read. Its mechanism (a script that prints one instruction per step, waits, and prints the captured answers as key and value lines) is described in point 4 in words; the script itself is not copied or shipped.
2. The other files of `systematic-debugging` (`root-cause-tracing.md`, `defense-in-depth.md`, `condition-based-waiting.md`, the pressure tests) were not re-read; `SKILL.md` §2 and §3 stay as written from their earlier reading.
3. Nothing in §5 was run on a real bug. The claim that "the loop is the skill, the rest mechanical" is the source's own and is restated as a rule of thumb in point 1, not measured.
