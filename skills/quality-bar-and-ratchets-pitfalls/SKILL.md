---
name: quality-bar-and-ratchets-pitfalls
description: "Use when a project has no written quality bar, when coverage, performance, accessibility or security numbers are argued per merge request instead of decided once, when an agent keeps silencing checks or editing a threshold to reach green, or when a bar exists but nothing watches the file that holds it: the written bar with a reason and a command per number, ratchets for metrics with no target, exceptions with an owner and an expiry, at least one external check, and diff guards for a lowered threshold, a new exception and suppression comments."
---

# quality-bar-and-ratchets-pitfalls

Step 7 of the pipeline (`WORKFLOW.md`), around `gate`. The premise: **an agent writes more than anyone reads, so
quality has to live in checks that run around the loop, and the checks only mean something if the bar they
enforce cannot be quietly lowered.** `guard-test-changes` and `config-protection` already watch tests and
linter or runner configuration; nothing watches a threshold file, an exception list, or a suppression comment
that switches a check off. That gap is this block.

## When
- A project or a large feature starts and no quality bar is written down.
- A number (coverage, a performance budget, an accessibility level) is discussed in every review.
- A diff lowers a limit, adds a suppression comment, skips a check or adds an exception.
- A bar exists but is made only of the project's own tests.

**Skip when** the code is a throwaway script or a spike; say so and write nothing.

## Steps

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | The written bar: one file, a reason and a command for every number, external checks, placement by cost | a bar is created or reviewed | [`01-writing-the-bar.md`](./references/01-writing-the-bar.md) |
| 2 | Ratchets for metrics with no target, exceptions with owner and expiry | a number is chosen, or a rule cannot be met today | [`02-ratchets-and-exceptions.md`](./references/02-ratchets-and-exceptions.md) |
| 3 | Diff guards: lowered threshold, new exception, suppression comments, unfinished stubs | a diff is reviewed or a guard is written | [`03-guarding-the-bar.md`](./references/03-guarding-the-bar.md) |

## Output / checkpoint
The bar file exists, every number has a reason and a command that runs today, at least one check is external,
metrics with no target are recorded as a ratchet, every exception has an owner and an expiry, and the diff was
read for the five moves of §3. A review of a diff that touches the bar names each loosening found, or says none.

## Guardrails
- Never invent a target a codebase fails today; record where it stands and forbid getting worse (§2.1).
  Positive form: choose a number the current code meets, or a ratchet.
- Never accept a number with no command that produces its verdict; it is an aspiration (§1.1).
  Positive form: write the command beside the number or remove the number.
- Never change the bar in the same commit as the feature that was failing it (§3.3).
  Positive form: land the change to the bar alone, with its reason, and let a human read it.
- Never leave an exception without an owner and an expiry (§2.3). Positive form: an exception unblocks one path
  for a stated time; deleting the rule unblocks everyone for ever.
- Never print a matched secret value from a scan; report the rule and the location (§1, scan output).
  Positive form: run the scanner in its redacting mode.
- Numbers in these files are examples of shape, not recommendations; every default is chosen per project and
  written with its reason.

## Origin
Rewritten from the constraint-driven-development skill of addyosmani/agent-skills (MIT), read 2026-10-20 and
2026-10-21. Details, what was left out and what is unverified: [`references/origin.md`](./references/origin.md).
