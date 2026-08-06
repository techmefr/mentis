# hooks

The only executable code in this repo. Everything else is markdown that an agent reads; these two
scripts exist because step 7 of `WORKFLOW.md` needs a guarantee that **cannot** be a written
instruction.

## Why a hook and not a rule

`gate` says: never declare a criterion passing without evidence you have read. Written as an
instruction, that holds right up until the moment it's inconvenient. The hook makes it mechanical:
the edit that flips `passes: true` is refused by the tool layer, before the model's intent matters.

This is the one place where "default = failure" stops being a doctrine and becomes an interlock.

## The two scripts

| Script | Event | Job |
|---|---|---|
| `verify-gate.sh` | `PreToolUse` on `Edit`/`Write` | Blocks a `test-results.json` edit that claims `passes: true` without read evidence |
| `record-read.sh` | `PostToolUse` on `Read` | Logs which evidence files were actually read |

They're split because the guarantee needs both halves: `verify-gate.sh` alone could only check that
a file *exists*, and evidence produced but never looked at is exactly the failure mode we're
guarding against. A test run whose output nobody opened is a green tick, not a verification.

## Wiring, per repo

Copy both into the target repo's `.claude/hooks/`, make them executable, then in
`.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/verify-gate.sh" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Read",
        "hooks": [
          { "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/record-read.sh" }
        ]
      }
    ]
  }
}
```

Then, in the repo: `mkdir -p .claude/evidence` and add `.claude/evidence/` to `.gitignore` —
evidence is per-run, it isn't versioned.

Requires `bash` and `python3` (stdlib only). Both scripts are read-only on your project: they touch
nothing but the read log.

## Conventions the scripts assume

- **Contract file**: `test-results.json`, one entry per acceptance criterion, `{"passes": false}`
  initially (written at step 5 by `tdd`/`dozer`).
- **Evidence**: any file under `.claude/evidence/` whose **filename contains the criterion id**.
  Test output, a screenshot, a log: the form doesn't matter, the naming does.
- Override the paths with `MENTIS_EVIDENCE_DIR` / `MENTIS_READ_LOG` if a repo needs different ones.

## Deliberate design choices

**A malfunctioning hook blocks, but only on the guarded path.** If the payload can't be parsed, or
no `python3` is available, we exit non-zero rather than 0 — a guard that fails open is worse than no
guard, because it reports a safety that isn't there while everyone stops checking manually. The
subtlety is *where* that applies: the script first decides, with no parser at all, whether this tool
call touches the contract file. If it doesn't, exit 0. So a repo with nothing installed still works
normally, and only edits to `test-results.json` can be refused for being unverifiable.

The first version of this script got that wrong: it parsed the payload up front, and with the parser
missing it silently allowed everything, while this README claimed it failed closed. It was caught by
the smoke test below, which is the entire argument for having one.

**It guards one file, not your whole repo.** The matcher fires on every `Edit`/`Write`, but the
script exits 0 immediately unless the target is `test-results.json`. Guarding more would make it a
nuisance, and a nuisance gets disabled.

**It doesn't judge the evidence.** Whether the evidence actually proves the criterion is
`galadriel`'s job (fresh context, reads the diff and the evidence, returns `PASS`/`NEEDS_WORK`). The
hook only enforces that something was produced and read. Two different mechanisms, deliberately: the
hook can be fooled by a deliberately misnamed file, and it's not trying not to be. It closes the
honest-mistake path, not the adversarial one.

## Smoke test

Six cases, and they're the specification. Run them after any change to either script:

| Case | Expected |
|---|---|
| claims `passes: true`, no evidence file | **block** (exit 2) |
| evidence file exists but was never read | **block** (exit 2) |
| evidence exists and is in the read log | allow (exit 0) |
| edit sets `passes: false` | allow |
| edit targets any other file | allow |
| payload unparseable but names the contract file | **block** (exit 2) |

Point `MENTIS_EVIDENCE_DIR` and `MENTIS_READ_LOG` at a throwaway directory, feed each payload to the
script on stdin, and compare the exit code. Case 2 is the one that matters most: it's the difference
between "evidence was produced" and "someone looked at it".

## Status

Written and **unit-tested against the six cases above**, but **not yet dogfooded**: not wired into a
real repo at the time of writing. The mechanism is
rewritten from market long-running-agent patterns (a default-FAIL `PreToolUse` hook plus a
fresh-context evaluator); the read-log half, the fail-closed choice and the single-file scope are
ours.
