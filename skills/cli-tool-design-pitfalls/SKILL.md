---
name: cli-tool-design-pitfalls
description: "Use when designing or reviewing a command-line tool that people or scripts will call: command and flag naming, standard output versus standard error, exit codes, machine-readable output, prompts and non-interactive use, configuration precedence, secrets on the command line, destructive actions, help and error messages, and shell completions."
---

# cli-tool-design-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the interface of a command-line program, whatever language it is
written in. The premise: **a command-line tool has two kinds of caller, a person at a terminal and a script with
no terminal, and most defects are one caller's convenience breaking the other**: a progress message on standard
output that corrupts a pipe, a success code after a failure, a prompt that hangs a pipeline, a token in an
argument that every user of the machine can read. Writing the shell scripts that call tools is in
`shell-scripting-conventions` and `bash-pitfalls-and-bats`; a tool exposed to an agent is in `mcp-server-design-pitfalls`.

## When
- A new command, subcommand or flag is added, renamed or removed.
- A tool prints, prompts, reads configuration or exits.
- A tool is called from CI, a hook or another program.
- A command can delete, overwrite, send or spend something.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Output streams, exit codes, machine-readable output, colour and progress, interactive versus non-interactive, signals | a command prints, prompts or exits | [`01-streams-exit-codes-and-scripting.md`](./references/01-streams-exit-codes-and-scripting.md) |
| 2 | Command and flag naming, configuration precedence, secrets, destructive actions, help and errors, completions, compatibility | a command surface, option or message is designed or changed | [`02-surface-config-and-safety.md`](./references/02-surface-config-and-safety.md) |

## Output / checkpoint
Each section ends with its own checks. For a change touching this block: results go to standard output and
everything else to standard error, failure exits non-zero with a message that says what to do, the command runs
with no terminal and no prompt, no secret is accepted as an argument value, and a destructive command has a
dry-run and a non-interactive confirmation flag.

## Guardrails
- Write only the result to standard output; send messages, progress and warnings to standard error (§1.1). Never mix them.
- Exit zero only on success and name each failure class with its own non-zero code (§1.2). Never exit zero after an error.
- Detect a missing terminal and never wait for input there (§1.4). Never block a pipeline on a prompt.
- Take secrets from a file, an environment variable or standard input, not from an argument (§2.3).
- Give every destructive command a preview and an explicit flag to skip confirmation (§2.4).
- Once a flag, output format or exit code is published, change it only with a deprecation period (§2.6).
- Conventions below are general practice from our own knowledge; no external guide was read (🟡, nothing here was run).

## Origin
Own guidance, from the craft of writing command-line tools; no source was read. The published guide
named in the review file has no licence we verified, so it was not opened. See
[`references/origin.md`](./references/origin.md).
