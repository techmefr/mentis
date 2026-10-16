---
name: php-architecture-test-pitfalls
description: "Use when a PHP project enforces its layering with a dependency checker or architecture tests (Deptrac, PHPat as a PHPStan extension): default-deny rulesets, layers that match more or less than intended, classes that belong to no layer, public versus private layer members, a baseline of known violations that must only shrink, and architecture rules written as tests (registration, selectors, allow-list versus deny-list assertions, built-in classes, ignorable errors, reusable rules per module)."
---

# php-architecture-test-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the tools that turn "the domain must not depend on the
infrastructure" into a failing build. The three sections share one premise: **an architecture rule is only as
good as the set of classes it actually selects and the number of exceptions it quietly tolerates**, so every
rule here is about what the checker sees, what it skips, and what can be waived. Where the layers should be is
a design question and is in `skills/no-catch-all-layer` and `skills/archi`; this block is about keeping the
checker honest once the layers exist.

## When
- Adding Deptrac or PHPat to a PHP project, or reviewing its configuration or a change to a rule.
- A violation is "fixed" by adding it to a baseline or an ignore list.
- A new directory, module or package is added and nothing in the checker changed.
- An architecture rule passes although a forbidden dependency is plainly in the code.

## Steps

**Read only the section the task meets.** They are independent.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Layers and rulesets (Deptrac): default-deny, collectors, anchoring, public and private members, uncovered classes, analysis types, debug commands | layers are defined or a rule does not catch what it should | [`01-layers-and-rulesets.md`](./references/01-layers-and-rulesets.md) |
| 2 | Violations and baselines: skipping known violations, stale entries, regenerating, non-ignorable rules | a violation is waived, a baseline is added or changed, or CI starts failing on stale entries | [`02-violations-and-baselines.md`](./references/02-violations-and-baselines.md) |
| 3 | Rules as tests (PHPat): registration, rule naming, selectors, assertion choice, built-in classes, reusable rules | an architecture test is written, or one never seems to fail | [`03-rules-as-tests.md`](./references/03-rules-as-tests.md) |

## Output / checkpoint
For each rule added or changed: a deliberate violation was introduced in a scratch change and the checker
failed on it (a rule never seen failing is not verified), the list of classes the rule selects was printed
(`debug:layer` for Deptrac, or a deliberately failing assertion for PHPat), the count of unassigned classes is
known, and the baseline diff only removes entries.

## Guardrails
- Never add an entry to a violations baseline to make a new change pass; fix the dependency or change the
  design (part 2, point 1).
- Never match a layer with an unanchored name pattern such as a bare word between wildcards (part 1, point 3).
- Never register an architecture test only in a file the analyser does not scan (part 3, point 1).
- Never write an inner-layer rule as a list of forbidden layers when it can be written as the list of allowed
  ones (part 3, point 4).
- Never treat a green run as proof before the rule has been seen failing once (Output).
- This block states the tools' documentation at the commits in [`references/origin.md`](./references/origin.md).
  Nothing was run while writing it, and the tools' versions were not matched to a project's.

## Origin
Rewritten from the Deptrac documentation (MIT) and the PHPat documentation (MIT), read 2026-10-16. 🟡: never
run by us; open points are in [`references/origin.md`](./references/origin.md).
