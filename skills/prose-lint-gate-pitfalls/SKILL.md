---
name: prose-lint-gate-pitfalls
description: "Use when a style guide is turned into automated prose checks that run in CI or an editor: severity levels so the gate fails only on rules you mean to enforce, per-repository overrides in one declared file, scoped disables that are re-enabled, skipping a move-only change, pinning the rule package and the tool, planted-violation tests per rule, vocabulary and filters against false positives, inclusive-language checks, and what a linter cannot judge."
---

# prose-lint-gate-pitfalls

Not a step of the pipeline: a craft block for the **gate** around a prose linter, not for any one linter. The
three parts share one premise: **a gate is trusted only while it fails for the reasons its owners meant and
stays quiet otherwise**, so the pitfalls are the ways a prose check gets ignored (noise, surprises), silently
stops working (a rule that no longer matches), or changes under a pipeline unannounced. The tools named in the
sources (Vale for rules, a Node-based checker for insensitive wording) are examples of the mechanism; nothing
here depends on them. The wording of the style itself is in `business/ux-writing` and `release-notes-writing-pitfalls`.

## When
- A style guide is being turned into checks, or a prose check is added to CI.
- A prose gate is failing pull requests and people want to switch it off.
- A rule package or the linter is upgraded, or a rule seems to have stopped firing.
- Inclusive-language or accessibility wording checks are added.

## Steps

**Read only the part the task meets.**

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Severity levels, overrides in one file, path scoping, scoped disables, skipping a change, changed lines only | the gate's behaviour on a pull request is designed or argued | [`01-severity-and-gate.md`](./references/01-severity-and-gate.md) |
| 2 | Pinning the package and the tool, local against global config, planted-violation tests, vocabulary and filters | the checks must stay trustworthy over time | [`02-keeping-rules-trustworthy.md`](./references/02-keeping-rules-trustworthy.md) |
| 3 | Rule messages, the inclusive-language family, what lint does not judge | a rule is written or a finding is disputed | [`03-rule-content-and-limits.md`](./references/03-rule-content-and-limits.md) |

## Output / checkpoint
A gate is ready when its owner can state from one file: which levels fail the build, where overrides live, what
a scoped disable looks like, which versions are pinned, and which fixture proves each rule still fires. Read
the setup once looking for a rule that has no planted violation, a package referenced by name only, and a
disable that is never re-enabled. Nothing here was run against a linter: the check is a read of the text. No
pipeline checkpoint.

## Guardrails
- Never let a rule fail the build that nobody decided should (part 1).
- Never switch a rule off for a whole file when a section needs it; disable and re-enable around the section
  (part 1).
- Never reference a rule package or a linter by name only in CI; pin the version (part 2).
- Never ship a rule without a planted-violation fixture, and never leave a fixture for a rule that was removed
  (part 2).
- Never treat a clean lint as a reviewed text; a person still reads for meaning (part 3).
- Never police: inclusive-language checks are checks with a replacement, not accusations (part 3).
- Thresholds, level names and file names in this block are the sources' own choices; write the team's own in one
  file.

## Origin
Rewritten from the Elastic Vale rules repository and the Grafana writers' toolkit (both Apache-2.0), the Vale
packages index and the alex checker (both MIT), read 2026-10-16. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
