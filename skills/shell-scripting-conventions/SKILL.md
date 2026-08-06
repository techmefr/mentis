---
name: shell-scripting-conventions
description: Use when writing or reviewing a shell script that anything depends on — a hook, a CI step, a make target, a deploy or maintenance script — where the default behaviour of the shell is to continue after a failure and report success.
---

# shell-scripting-conventions

Step 6 (`code`) of the pipeline (`WORKFLOW.md`), for shell specifically, because shell breaks the
assumption the rest of the pipeline rests on: **by default, a shell script that fails still exits 0**,
and a gate that exits 0 is a gate that passed.

This block exists because it happened here. The repo's own gate hook parsed its payload with a tool that
wasn't installed, got an empty value, and allowed everything — while its documentation claimed a
malfunctioning hook blocks. It was written to be fail-closed and shipped fail-open.

## When
When writing or reviewing: a `hooks/` script, a CI step of more than one command, a `make` target with
logic in it, a deploy or migration script, anything run by a scheduler.

## Steps

### 1. Make failure the default
1. **`set -euo pipefail` at the top.** Exit on error, fail on an unset variable, and propagate a failure
   from anywhere in a pipeline instead of only the last command.
2. **Know where `-e` doesn't save you** — inside `if`, `&&`/`||` chains, and command substitution in some
   positions. Check exit codes explicitly there.
3. **Quote every expansion**: `"$var"`, `"$@"`, `"${arr[@]}"`. An unquoted empty variable makes an
   argument disappear, which turns `rm -rf "$dir/"*` into something else entirely.
4. **`cd` is checked**: `cd "$dir" || exit 1`. A failed `cd` followed by a destructive command is the
   classic shell disaster.

### 2. Fail closed, and only on the path you guard
1. **Decide the failure posture explicitly and write it in a comment-free, obvious way**: a gate that
   cannot determine the answer must **block**, not allow.
2. **But guard narrowly.** Blocking on every unexpected input makes the script unusable and it gets
   removed. Fast-path out with a cheap check that needs no parser, and only fail closed once you know the
   protected case is in play.
3. **Never depend on a tool being present without checking.** `command -v` first, and decide what its
   absence means — for a gate it means block, for a convenience it means skip.
4. **Exit codes are the interface.** For hooks, the host's contract defines which code blocks; get it
   from the documentation, not from memory (`source-freshness`).

### 3. Portability and provenance
1. **`#!/usr/bin/env bash`** when you use bash features, `sh` only if the script is genuinely POSIX. A
   bashism under `#!/bin/sh` fails on the machine that has a real `sh`.
2. **Windows/WSL crossing**: a file written from Windows carries CRLF, and `\r` at the end of a shebang
   or a variable breaks in ways the error message won't explain. Strip it, and never assume the editor
   didn't add it.
3. **The executable bit is part of the change.** A tool rewriting the file can drop it; git tracks it
   (`git update-index --chmod=+x`), and a script committed 100644 fails on someone else's clone with
   "Permission denied" and no other clue.
4. **Prefer a real language past ~50 lines of logic.** Shell has no types, no test framework you'll
   actually use, and error handling you have to remember. Parsing structured data is the usual signal.

### 4. Prove it, because shell has no compiler
1. **`shellcheck` before it lands.** It catches the quoting and expansion classes above mechanically.
2. **Run the failure cases, not just the happy one.** Missing tool, unparseable input, absent file, empty
   variable. Confirm each one produces the exit code you intended — a fail-open bug is invisible in the
   happy path by definition.
3. **Write the case table down** next to the script, with what each case must do. It's the only test suite
   a hook is going to get.
4. **A script that guards something gets its guard tested against a real attempt to slip through**, not
   only against a well-formed call.

## Output / checkpoint
For anything gate-like: the failure posture stated, the narrow guard, and the case table run with its
results. `shellcheck` clean. The exec bit recorded in git.

## Guardrails
- **Never let a script exit 0 on a path it didn't handle**, and never let a gate degrade to permissive
  when a dependency is missing.
- **Never `rm -rf` a path built from an unquoted or unvalidated variable.**
- Never parse structured data with regex in shell when a real interpreter is available.
- **Never trust "it worked when I ran it"** — you ran the happy path, and the exec bit was set locally.
- Never put a secret in a script, an argument list or an `echo`; arguments are visible in the process
  list (`auth-session-conventions` §2.4).

## Origin
The defensive baseline (`set -euo pipefail`, quoting, checked `cd`, `shellcheck`) is long-established
public practice and is taken as-is. Everything in §2 and §4 is ours and comes from this repo's own
`verify-gate.sh`: the fail-open bug caused by assuming a parser was installed, the fix's parser-free fast
path so a machine without it still works normally, the exec bit silently dropped when a tool rewrote the
file, and CRLF from the Windows side corrupting scripts copied into WSL. All four were real, all four
were invisible on the happy path.
