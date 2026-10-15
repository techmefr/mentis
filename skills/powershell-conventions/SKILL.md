---
name: powershell-conventions
description: "Use when writing or reviewing PowerShell scripts, modules or functions: error semantics (non-terminating versus terminating errors, -ErrorAction versus the preference variable, native exit codes), secrets and dynamic code (SecureString, PSCredential, Invoke-Expression), and function design (ShouldProcess, process blocks, strict mode, scoping)."
---

# powershell-conventions

Step 6 of the pipeline (`WORKFLOW.md`), for PowerShell code. The premise: **PowerShell reports most failures
as errors that do not stop anything**, so a script is only safe when it says, at each step, which failures
must stop it. Generic secret handling is `security-hardening` §4; generic anti-patterns for tests are
`testing-anti-patterns`; shell scripts in Bash are `shell-scripting-conventions`.

## When
- A script automates something that changes state (files, services, accounts, remote machines).
- A function, script or module is added or reviewed.
- A secret, credential or dynamic string reaches a command.
- A script calls a native program and its exit code matters.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Error semantics: three kinds of error, escalation, try, native exit codes | a script has to stop, recover or report on failure | [`01-errors.md`](./references/01-errors.md) |
| 2 | Secrets and dynamic code: SecureString, PSCredential, Invoke-Expression | a password, token or built command string appears | [`02-secrets-and-dynamic-code.md`](./references/02-secrets-and-dynamic-code.md) |
| 3 | Function design: ShouldProcess, pipeline input, strict mode, scope, comparisons | a function is written, or a script runs code in another runspace or session | [`03-functions-and-scripts.md`](./references/03-functions-and-scripts.md) |

## Output / checkpoint
For each state-changing script: the failure it must stop on is named, the way it stops (escalation plus one
`try`, or a checked exit code) is visible in the code, and it has been run once with the step failing and once
with `-WhatIf`.

## Guardrails
- Never leave a `catch` block empty (§1.3).
- Never accept a password as a plain string or build a command from input for `Invoke-Expression` (§2).
- Never assume `-ErrorAction` and `$ErrorActionPreference` behave alike; they differ on which errors they reach (§1.2).
- Versions: each rule names its PowerShell version. Nothing here was run on a PowerShell host.

## Origin
Rewritten from the PowerShell documentation on learn.microsoft.com (about pages and cmdlet pages, 7.5 set) and
the PSScriptAnalyzer rule documentation (MIT), read 2026-10-08. A community style guide under a share-alike
licence was used for ideas only. New block, no PowerShell block exists on the main branch. 🟡: never run by us;
open points are in [`references/origin.md`](./references/origin.md).
