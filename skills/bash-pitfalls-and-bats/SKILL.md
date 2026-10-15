---
name: bash-pitfalls-and-bats
description: "Use when writing or reviewing Bash scripts beyond the failure-default basics, or tests for them with bats: the shell traps that lose a variable or an exit status silently (pipes into loops, local with a command substitution, arithmetic exit status, string comparison, globs, word splitting, argument lists) and the bats-core behaviours that make a test green while asserting nothing."
---

# bash-pitfalls-and-bats

Step 6 of the pipeline (`WORKFLOW.md`), for Bash code and its tests. The premise: **most silent shell bugs are
the shell doing exactly what its manual says**, and a shell test that cannot fail is worse than none.
Strict mode, quoting, checked `cd` and fail-closed guards are `shell-scripting-conventions` §1 to §4; this
block holds only the traps those sections do not name. Generic test anti-patterns are `testing-anti-patterns`.

## When
- A Bash script builds argument lists, loops over command output or globs, or compares values.
- A Bash function is changed that sets variables, returns a status or runs under `set -e`.
- A bats test file is written or reviewed, or a bats run hangs or passes suspiciously.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Bash traps: subshells, statuses, comparison, globs, splitting, arguments | any non-trivial Bash is written or reviewed | [`01-bash-pitfalls.md`](./references/01-bash-pitfalls.md) |
| 2 | bats-core: what `run` does, negation, pipes, hangs, helpers, teardown | a bats test is written, reviewed, or hangs | [`02-bats.md`](./references/02-bats.md) |

## Output / checkpoint
Each trap rule applied has been run once in the target Bash on a three-line reproduction, and each bats test
has been seen failing (by breaking the code under test or inverting the assertion) before it is trusted.

## Guardrails
- Never assume a variable set inside a pipeline, a `run` or a command substitution is visible afterwards
  (§1.1, §2.1).
- Never write a negated command and expect the test to fail on it unless it is the last command (§2.2).
- Versions: each rule names its Bash or bats version. Nothing here was run against your environment.

## Origin
Rewritten from the Bash reference manual (5.3), the bats-core documentation (1.14.0, MIT), the Google shell
style guide (CC BY 3.0) and a contested community guide (MIT), read 2026-10-08, plus a few one-line runs on
Bash 5.2.21. Meant to be folded into `shell-scripting-conventions`. 🟡: open points are in
[`references/origin.md`](./references/origin.md).
