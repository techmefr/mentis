# debug references: origin of §5

> Provenance of `references/05-feedback-loop-first.md` and `references/06-component-boundaries.md`. Read it to trace a rule to its source, never to apply one.
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

## Section 6 (`06-component-boundaries.md`), added 2026-10-19

**Status: 🟡.** One source, re-read in full on 2026-10-19: `obra/superpowers`, `skills/systematic-debugging/` (MIT, 2025 Jesse Vincent, commit bb92a77): `SKILL.md` (283 lines), `root-cause-tracing.md`, `defense-in-depth.md`, `condition-based-waiting.md` and its example file, `find-polluter.sh`, `CREATION-LOG.md` and the four test files. Own wording, own example.

| Source passage | What it gave |
|---|---|
| `SKILL.md` Phase 1, step 4 (gather evidence in a multi-component system: log what enters and leaves each boundary, verify environment propagation, run once, then analyse which component fails) | Points 1 to 3 |
| Same passage, its worked example (a secret reported as set or unset at each layer, never printed) | Point 5 and the placement in point 1 |

**Ours, not the source's.**
1. The reason for "once" in point 2 (a run is costly), the bounded and tagged probe set (point 4) and the check that the probes change nothing (point 6) are added to reconcile with §5.12, §5.13 and §5.16. The source says to log each boundary and nothing of tags or of the probes' own effect.
2. The statement that this section sits after the loop of §5 and does not breach the single hypothesis of `SKILL.md` §1 is our reconciliation, not the source's.

**Compared and not taken.** `root-cause-tracing.md` (the backward trace, the stack capture, the bisection script for finding the test that pollutes) is the origin of `SKILL.md` §2 and §5.4; `defense-in-depth.md` is `SKILL.md` §3. `condition-based-waiting.md` (replace sleeps with condition polling) belongs to the flaky-test block (`skills/flaky-test-triage-pitfalls`), not here. The pressure tests and `CREATION-LOG.md` describe how the source skill was tested and carry no rule to take. The source's four-phase structure, its red-flags list and its "95 percent of no-root-cause cases are incomplete investigation" figure are not taken: the figure has no measurement behind it in the source.

**Not verified.** Nothing in §6 was run on a real multi-stage failure.
