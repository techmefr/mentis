# hooks

The only enforcement in this repo. Everything else is markdown that an agent reads; these scripts exist
because some guarantees **cannot** be written instructions: a rule holds right up to the moment it is
inconvenient, and the moment it is inconvenient is exactly the moment it matters.

Three guarantees, five scripts (nine more hooks, all opt-in, are described at the end of this file, with an environment-variable table and a wiring snippet):

| Guarantee | Script(s) | Event |
|---|---|---|
| No pass without evidence read (step 7 of `WORKFLOW.md`) | `verify-gate.sh` + `record-read.sh` | `PreToolUse` on `Edit`/`Write`, `PostToolUse` on `Read` |
| **No agent installs anything, ever** | `block-installs.sh` | `PreToolUse` on `Bash` |
| **No pre-existing test assertion disappears silently** (`skills/debug` §3.4) | `guard-test-changes.sh` + `guard-test-changes.py` | `PreToolUse` on `Edit`/`Write`, and on `Bash` for the shell routes |

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

## `block-installs.sh`: no agent installs anything

**What it refuses**, on every `Bash` call: `npm`/`pnpm`/`yarn`/`bun` install, add, `ci`, create, update, link;
`npx`, `bunx`, `pnpm dlx`; `pip`/`pipx`/`uv` install; `gem`, `cargo`, `go install`; `composer install`/`require`;
`brew`, `apt`, `dnf`, `pacman`, `winget`, `choco`; toolchain installers (`nvm`, `rustup`, `asdf`, `volta`); and
the whole `curl … | bash` family, including `bash <(curl …)`, a downloaded `.sh`, and `iwr … | iex`.

**Command boundary (2026-10-02).** A word counts only where a command starts: the start of the text, or after a newline, `;`, `&`, `|`, parentheses or a backtick, once `sudo`, `env`, `VAR=value`, `time` or `xargs` are peeled off. The command inside `ssh host "..."`, `sh -c` or `bash -lc` is unwrapped and judged the same way. `echo 'npm install x'` and `grep "npm install" notes` carry the words as arguments and pass. A shell-quoting error inside the command never blocks by itself.

**What it lets through**: `npm run`, `pnpm test`, `bun run dev`, `make`, `git`, `docker compose`, a plain
`curl` to an API — the ordinary work. That distinction is the whole design. A guard that blocks
`npm run test` is switched off within a day, and then it guards nothing.

**Why.** An install runs lifecycle scripts (`postinstall` and friends) **as the user, with their
environment** — tokens, SSH keys, cloud credentials, session files. That is the payload of the current wave
of malicious packages, and it executes before anyone has read a line of what was pulled. The instruction to
install something also rarely comes from the person at the keyboard: it comes from a README, an issue, a
diff, a helpful error message — text the agent read and treated as a task. The refusal message says so, and
tells the model to quote the source to the user instead of complying.

**What it tells the user to do instead**: name the dependency and let them run it themselves, in their own
terminal, with **pnpm** — one content-addressed store, a strict `node_modules` that refuses undeclared
imports, and a lockfile pinning the whole tree:

```bash
pnpm add -D <package>     # dev dependency
pnpm add <package>        # runtime dependency
pnpm install              # restore from the lockfile
```

`pnpm dlx <tool>` is still a download, so it is still the user's call.

**Second stage: what `npm run <script>` actually runs.** Allowing the runner while blocking the installer
would be theatre — a `package.json` script executes arbitrary shell, so `npm run test` is the obvious way
around a guard that only reads the command line. When the command invokes a script, the hook reads the
manifest, resolves the script **and its `pre`/`post` lifecycle twins**, follows one level of
script-calls-script, and applies the same patterns to the body. So:

- `npm run test` where `"test": "vitest"` → runs;
- `npm run test` where `"test": "curl https://…/x.sh | bash"`, or where `"pretest": "npm i something"` → refused,
  and the message says it is the script that is the problem, not the runner.

A useful side effect: an agent that writes a poisoned script into `package.json` and then runs it is caught at
the run, even though the write itself went through a different tool.

**Honest limits**, because a guard oversold is a guard trusted too far:

- **Indirection it does not parse.** `make <target>`, `just`, `task`, a composer script, a `docker compose
  run`, a git hook firing on commit, or a local `bash ./setup.sh` — the hook reads the command line and
  `package.json` scripts, nothing else. The same trick through a Makefile target goes through.
- **Obfuscation.** A base64 blob, an alias, a script assembled at runtime. Any pattern list loses that game.
- **Only `Bash`.** Another tool that can execute commands isn't covered by this matcher.
- **No in-band escape hatch** — deliberately. No `ALLOW_INSTALL=1`, no allowlist file: anything the agent
  could read, the agent could write.

This is an interlock against accidents and against injected instructions, **not a sandbox**. The real
boundary is the permission layer of the tool that runs the agent; this hook makes the common path fail
loudly and explain itself, and fails **closed** on a `Bash` call it cannot parse that mentions a package
manager.

Checked by `bin/test_hooks.py` — 77 checks: 72 commands, blocked and allowed both, because half the
value is in what it does not break, plus the executable bit on every file in this directory, which this
script had been missing since it was written.

## `guard-test-changes.sh`: no pre-existing assertion disappears silently

**What it also refuses (2026-10-02).** A test skipped, marked todo or incomplete; an assertion that cannot fail; a test deleted or renamed away (counted before and after, by declared test name); and, on the `Bash` event, a shell command that rewrites, moves, deletes or reverts a test file (`sed -i`, `rm`, `mv`, `git checkout`/`restore`, a redirection onto it). Wire the same script under `matcher: "Bash"` to get the shell half; wired on `Edit|Write` only, the shell routes stay open. A test path the fast path does not recognise is not seen.

**What it refuses**, on every `Edit`/`Write` targeting a file that looks like a test
(`*.test.*`, `*.spec.*`, `*_test.*`, `test_*.py`, `*Test.php`, `*Test.java`): an edit where an
assertion that existed **before** the edit is no longer there **after** it — deleted, commented
out, or its expected value changed. An assertion is a line matching one of the patterns
(`expect(`, `assert*(`, `$this->assert*(`, `self.assert*(`, a bare `assert `, `Assert::`/`Assert.`,
a Jest/Vitest matcher, `t.Error`/`t.Fatal`, `require.*`) **plus every line it spans until its
brackets balance**, compared with whitespace collapsed and a comma before a closing bracket
dropped.

**Why a statement and not a line, which is what it compared until 2026-09-09.** A formatter puts
the expected value on its own line:

```ts
expect(resolvePruneRule('BlogPost')).toEqual({
  retentionDays: 30,
  lock: false,
});
```

Changing `30` to `60` there touches no line matching an assertion pattern, so the line-level
comparison allowed exactly the edit this hook exists to refuse — in the dominant formatting style
of a TypeScript repo. Two consequences beyond the comparison itself: the whole file is
reconstructed from disk and the replacement applied to it, because an `Edit` hunk that changes
only the value carries no assertion at all; and collapsing whitespace is what keeps a reformat or
a re-indent from reading as a removal. Found by wiring the hook into a real repo.

**What it lets through**: extending a test file with a new case (the old assertion line is
still there, a new one joins it), touching a non-test file, and creating a brand-new test file
(nothing on disk yet to tamper with).

**Why.** `skills/debug` §3.4 states the rule: a pre-existing test that fails is a verdict on the
implementation, not on the test, and the easy way out — editing the test's expectation to match
the broken output instead of fixing the code — ships a regression behind a green suite. Written
as an instruction alone it holds until it's inconvenient; this hook makes the common shape of
that mistake mechanical, the same reasoning as `verify-gate.sh` for evidence.

**The deliberate escape hatch, and why it's not in-band.** Unlike `block-installs.sh`, there's a
real, legitimate reason for a test to change: the spec genuinely moved. `MENTIS_ALLOW_TEST_CHANGES=1`
lets a specific push through — but it's an environment variable the human sets in their own shell
before the session or the task, not a comment or a marker the agent could quietly add to its own
diff. That's the difference between an honest escape hatch and a hole: nothing in the diff itself
can unlock this guard.

**Honest limits**, same spirit as `block-installs.sh`:
- **A refactor that moves an assertion into a helper** (`expect(x).toBe(1)` becomes
  `assertFoo(x)`) looks like a removal to this heuristic, because the literal line is gone. This is
  the false-positive case `MENTIS_ALLOW_TEST_CHANGES` exists for.
- **Renaming the symbol under test blocks too**, for the same reason: the assertion text changed,
  and nothing here can tell a rename from a retargeting. It is the most common legitimate block,
  and the escape hatch is task-scoped rather than edit-scoped — so an agent that learns to set it
  for a rename has turned the guard off for the rest of the task. Wire it knowing that.
- **An over-specified assertion is a test defect, and widening it looks identical to bending it.** An
  assertion pinning an exact list where the behaviour legitimately produces more entries fails on
  correct code; the fix is on the test's side and the guard cannot tell it from the dishonest edit. The
  discipline that keeps the two apart: **widen and pin** — narrow the original assertion to the fact it
  was really about, and *add* the test that states the newly understood behaviour, so the suite grows
  rather than loosens. Found by dogfooding 2026-09-08 (43 tests became 44).
- **No AST, no real per-language parser.** A regex over lines, deliberately — the same tradeoff
  `verify-gate.sh` makes for the contract file, for the same reason: exhaustive parsing for five
  ecosystems isn't worth the maintenance for a guard whose job is catching the honest-mistake
  shape, not every possible obfuscation.
- **The shell half is a segment heuristic.** On `Bash` the command is split on `&&`, `||`, `;`, `|` and
  newlines. A redirection (`>`, `>>`) onto a test path is refused; so is a mutator (`rm`, `mv`, `truncate`,
  `tee`, `shred`, `sed -i`, `perl -i`, `git rm`/`checkout`/`restore`/`stash`/`reset`/`clean`) in a segment
  that also names a test path. Allowed: `git checkout .`, `cp x a.test.ts`, `cat`, `npx vitest run a.test.ts`,
  `npx prettier --write a.test.ts`, and `rm -rf node_modules && npm test -- a.test.ts` (the paths sit in
  different segments). A mutator word after a quote (a commit message that says "rm ...") is not seen. A
  mutator word inside an unquoted word of a segment that names a test path can be a false positive.
  A payload that cannot be parsed but names a test path is refused (exit 2). Test paths recognised:
  `.test.`, `.spec.`, `_test.`, `test_*.py`, `*Test.php`, `*Test.java`. A generated file, a script that
  edits tests behind a `make` target, or a path outside those patterns is not seen.
- **Without the `Bash` matcher in the wiring, the shell routes stay open.**

Checked by `bin/test_guard_test_changes.py` — 39 cases across five ecosystems, six of them the
formatted shape above, the rest the shell routes.

## Coexisting with the `test-casebook` gate

A project that installs any of the `test-casebook` siblings (`test-casebook`, `test-casebook-back-js`,
`test-casebook-back-php`) already has a `PreToolUse` hook of its own, which refuses a test file with no
`task-test.md` plan above it. **That is not a duplicate of this pair and both should be
wired**: it guards *plan before tests*, this pair guards *evidence before passing*. They fire on the same
event and chain in either order — a blocked write is a blocked write.

The only thing to check when wiring both: `settings.json` holds an **array** of `PreToolUse` matchers, so
add ours alongside theirs rather than replacing the block.

## Wiring, per repo

Copy the scripts into the target repo's `.claude/hooks/`, make them executable, then in
`.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/block-installs.sh" },
          { "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/guard-test-changes.sh" }
        ]
      },
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/verify-gate.sh" },
          { "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/guard-test-changes.sh" }
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

**Two things this wiring does not do, both measured on a real repo on 2026-09-09.** Most repos
already ignore `.claude/` wholesale, so everything above lands untracked: the hooks protect the
machine that wired them and nobody else's, and a colleague cloning the repo gets none of it. That
is a decision to take deliberately — commit the wiring and it applies to the team, leave it
ignored and it applies to you. And copying the scripts in forks them at copy time, which is the
exact failure `bin/install-git-hooks.sh` was rewritten to avoid for this repo's own gate: a stale
copy reports the safety of a script that has since changed. Either re-copy them when mentis moves,
or point the command at a cloned mentis and accept the path dependency.

**`block-installs.sh` is the one to wire first, and it is worth wiring alone.** The gate pair only makes
sense inside the mentis pipeline; the install guard applies to any repo where an agent has a shell, and it
is the only one of the three that protects something other than your process.

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

Written and **unit-tested against the six cases above**. Wired into a real repo on 2026-09-09 (a
NestJS project, `.claude/hooks/` + `.claude/settings.json` per the section above) and found to be
**inert there**: that repo runs no mentis pipeline, so it has no `test-results.json`, and the pair
guards one file that does not exist. Which is what the wiring section already said — wire
`block-installs.sh` first, and the gate pair only inside the pipeline. Still not dogfooded in the
sense that matters: no session has been refused by it. The mechanism is
rewritten from market long-running-agent patterns (a default-FAIL `PreToolUse` hook plus a
fresh-context evaluator); the read-log half, the fail-closed choice and the single-file scope are
ours.

`guard-test-changes.sh`/`.py`: 39 cases (`bin/test_guard_test_changes.py`), the shell routes added 2026-10-02
and covered by those cases only (not yet dogfooded in a real session). **Dogfooded once,
2026-09-09**, wired into a real NestJS repo and run against real edits to one of its spec files:
seven edits an agent would actually make, which is where the line-versus-statement defect above
came from — two of the seven were allowed and should have been blocked, and two were blocked and
should have been allowed. Internal synthesis, named directly by the operator; no external source,
the shape mirrors `verify-gate.sh`'s own fail-closed/single-purpose design rather than copying an
existing mechanism.

`block-installs.sh`: **dogfooded once, 2026-09-09** against every command that repo's own
`package.json` declares plus the dozen an agent types by hand — 52 in all, five blocked. One false
positive, since fixed: `pnpm exec`, which is how a single test file gets run, was refused as an
install, while `pnpm prisma …` — the same thing spelled without `exec` — went through. The two
verdicts contradicted each other, and the message named an install the agent had not attempted.

## Opt-in hooks (2026-10-02)

Two more hooks, **off until wired** and never part of the default set.

| Script | Event | Job |
|---|---|---|
| `gateguard.sh` | `PreToolUse` on `Edit`/`Write`/`MultiEdit` | Refuses the first edit of a file until the agent has produced facts it had to look up (importers, public API touched, data shape, the instruction quoted verbatim), then lets the retry through |
| `guard-secrets.sh` | `PreToolUse` on `Write`/`Edit`/`MultiEdit`/`Bash` | Refuses an obvious secret: a private key block, a token with a well-known prefix, a populated `.env`, a `git add` of a `.env` |

**`gateguard.sh`** also needs `MENTIS_GATEGUARD=1` in the session environment. State is per session in
`MENTIS_GATEGUARD_DIR` (default `~/.mentis-gateguard`), expires after 30 minutes of inactivity and keeps at
most 500 files. `MENTIS_GATEGUARD_EXEMPT` takes comma-separated globs of paths never gated (tests, generated
output). It fails open on any error. The gain its source reports comes from two A/B runs by its author and
has not been re-measured here.

**`guard-secrets.sh`** is a tripwire for the evident, not a scanner; keep a secret scanner in CI. It fails open
on any error.

Wire either exactly like the others (see the settings snippet above).

## Opt-in gate and detector hooks (2026-10-02, third set)

Two more hooks, **off until their variable is set**, never part of the default set.

| Script | Event | Job |
|---|---|---|
| `gate-ui-a11y.sh` + `.py` | `PreToolUse` on `Edit`/`Write`/`MultiEdit` | Refuses an edit to a UI file (`.vue`, `.svelte`, `.tsx`, `.jsx`, `.html`, `.astro`; not a test or a story) until the accessibility review of `skills/accessibility` has left its marker for the session |
| `detect-correction.sh` + `.py` | `UserPromptSubmit` | Notices a prompt that corrects the previous answer, appends one line to a log and returns a short reminder to name the wrong assumption and propose the guardrail that would have prevented it |

**`gate-ui-a11y`** needs `MENTIS_A11Y_GATE=1`. The marker lives in `MENTIS_A11Y_DIR` (default
`~/.mentis-a11y`), one file per session, and expires after `MENTIS_A11Y_TTL_HOURS` (default 12). It fails
closed, but only when the target is a UI file and the payload cannot be read.

**`detect-correction`** needs `MENTIS_CORRECTION_DETECTOR=1`; the log is `MENTIS_CORRECTIONS_LOG` (default
`~/.mentis-corrections.jsonl`). It never blocks and fails open. It is a wording heuristic: it misses
corrections phrased in no way it knows and can fire on a prompt that quotes one.

Wire either exactly like the others (see the settings snippet above), the detector under `UserPromptSubmit`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          { "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/gate-ui-a11y.sh" }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          { "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/detect-correction.sh" }
        ]
      }
    ]
  }
}
```

**How `gate-ui-a11y` decides.** It reads `tool_input.file_path` (or `path`) and `session_id`. Exempt: tests,
stories and anything under `__tests__`, `__mocks__`, `node_modules`, `dist`, `build`. The block message gives
the `mkdir -p ... && touch ...` command that creates the marker. *Limits:* the agent can create the marker
itself, so it is a speed bump that forces the review to be named, not proof that it happened; a UI file edited
through `Bash` is not seen; with the gate on and no `python3`, an edit to a UI file is refused, otherwise
allowed.

**How `detect-correction` decides.** It reads `prompt` and `session_id`, looks only at the first 600
characters, with English and French patterns, appends a JSONL line (`at`, `session`, the first 300 characters
of the text) to the log and returns a short reminder as `hookSpecificOutput.additionalContext`. *Limit:* the
log holds prompt text, so treat it as sensitive and keep it out of any repository.

### Environment variables

All are read from the human's environment before the session; nothing in a diff or a command can set them.

| Variable | Hook | Effect | Default |
|---|---|---|---|
| `MENTIS_ALLOW_TEST_CHANGES` | `guard-test-changes` | `1` lifts the guard, for the whole task | unset |
| `MENTIS_ALLOW_CONFIG_CHANGES` | `config-protection` | `1` lifts the guard | unset |
| `MENTIS_ALLOW_DESTRUCTIVE` | `guard-destructive` | `1` lifts the guard | unset |
| `MENTIS_COMMIT_TYPES` | `guard-commit-message` | replaces the allowed type list | built-in list |
| `MENTIS_GATEGUARD` | `gateguard` | `1` turns it on | off |
| `MENTIS_GATEGUARD_DIR` | `gateguard` | state directory | `~/.mentis-gateguard` |
| `MENTIS_GATEGUARD_EXEMPT` | `gateguard` | comma-separated globs never gated | none |
| `MENTIS_A11Y_GATE` | `gate-ui-a11y` | `1` turns it on | off |
| `MENTIS_A11Y_DIR` | `gate-ui-a11y` | marker directory | `~/.mentis-a11y` |
| `MENTIS_A11Y_TTL_HOURS` | `gate-ui-a11y` | marker lifetime | 12 |
| `MENTIS_CORRECTION_DETECTOR` | `detect-correction` | `1` turns it on | off |
| `MENTIS_CORRECTIONS_LOG` | `detect-correction` | log file | `~/.mentis-corrections.jsonl` |
| `MENTIS_SESSION_START_SOURCES` | `session-start-using-mentis` | session sources that print the reminder | `clear`, `compact` |
| `MENTIS_USING_MENTIS` | `session-start-using-mentis` | path of the `using-mentis` block | searched |
| `MENTIS_EVIDENCE_DIR`, `MENTIS_READ_LOG` | `verify-gate`, `record-read` | evidence directory, read log | `.claude/evidence`, per repo |

## Opt-in command and config hooks (2026-10-02, second set)

Five more hooks, **off until wired**, never part of the default set. Four are guards of the same family as
`block-installs.sh`: they exist because the written rule they enforce holds right up to the moment it is
inconvenient.

| Script | Event | Job |
|---|---|---|
| `block-no-verify.sh` | `PreToolUse` on `Bash` | Refuses the ways past a git hook: `--no-verify` (and `-n` on commit/am), `-c core.hooksPath=...`, `git config core.hooksPath <path>`, `HUSKY=0`, `LEFTHOOK=0`, `SKIP=...`, and removing or disabling a script in `.git/hooks` |
| `config-protection.sh` | `PreToolUse` on `Edit`/`Write`/`MultiEdit` | Refuses loosening a check to make code pass it: any edit to an existing linter, formatter or hook-manager config or ignore list; and, for type-checker, analyser and test-runner configs, an edit that turns a strictness flag off, adds an ignore or baseline entry, lowers a level, or drops a "warnings are errors" switch |
| `guard-commit-message.sh` | `PreToolUse` on `Bash` | Refuses a `git commit` whose message is not `type(scope)!: description` with a lowercase description, or whose text credits a tool (a co-author trailer or "generated with" line naming an assistant) |
| `guard-destructive.sh` | `PreToolUse` on `Bash` | Refuses recursive forced deletion, forced or deleting pushes, `reset --hard`, wholesale `checkout`/`restore`/`clean`, `DROP`/`TRUNCATE`/unqualified `DELETE` sent to a database client, framework database-wipe commands, prune/destroy of containers, volumes, clusters and infrastructure, package publishing, `chmod -R 777` |
| `session-start-using-mentis.sh` | `SessionStart` | After a clear or a compaction, prints a condensed `using-mentis` so the entry-point habit survives the lost context |

`command_views.py` is not a hook: the three Bash guards import it so that they agree on what a command is.
**Copy it next to them.** The python halves (`*.py`) sit beside their shell wrappers for the same reason.

**Command boundary, shared by the three Bash guards.** A word counts only where a command starts: the
start of the text, or after an **unquoted** newline, `;`, `&`, `|`, parentheses or a backtick, once `sudo`,
`env`, `VAR=value`, `time` or `xargs` are peeled off. The command inside `ssh host "..."`, `sh -c`,
`bash -lc`, `eval` and `find -exec` is unwrapped and judged the same way. Quoted text is one argument, so
`grep "rm -rf" notes`, `echo 'git commit --no-verify'` and `git commit -m "docs: why --no-verify is refused"`
pass. Heredoc bodies are data, except where the guard reads them on purpose (a commit message, SQL for a
database client). There is no PowerShell detection.

**Fail-open, everywhere.** No `python3`, an unreadable payload or any error in the hook exits 0. These are
tripwires for the honest mistake and for injected instructions, not a sandbox; a guard that breaks the
session gets removed, and then it guards nothing. (The install guard above is the exception, by design: it
fails closed on a command that mentions a package manager.)

**Activation, one by one.** Add the entry to the `settings.json` array of the event, exactly as in the
wiring snippet above:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/block-no-verify.sh" },
          { "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/guard-commit-message.sh" },
          { "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/guard-destructive.sh" }
        ]
      },
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          { "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/config-protection.sh" }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "clear|compact",
        "hooks": [
          { "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/session-start-using-mentis.sh" }
        ]
      }
    ]
  }
}
```

Wire only the ones you want. `block-no-verify.sh` and `config-protection.sh` are the pair that stop the two
cheapest ways of turning a red check green; `guard-destructive.sh` is the one to wire where an agent runs
unattended; `guard-commit-message.sh` is a house-format decision, so it is the one a team opts into on
purpose.

**What each one lets through, and where its limit is.**

- **`block-no-verify.sh`.** Lets through an ordinary commit and push, `git push -n` (a dry run, not a skip),
  reading `core.hooksPath`, and unsetting it. *Limits:* a hook skipped through a wrapper script or an alias
  is not seen; `HUSKY=0` set in a `.env` the manager loads is not seen.
- **`config-protection.sh`.** The strict tier refuses an edit to an existing file even when it tightens the
  rule, because a tightening is the user's call too and the cost of asking is one line. The loosening tier
  counts strictness tokens before and after, so it is a heuristic: a rewrite that moves a flag around can
  read as neutral, and a loosening phrased in a way no pattern knows passes. `MENTIS_ALLOW_CONFIG_CHANGES=1`,
  set by the human before the task, lifts it (the same shape as `MENTIS_ALLOW_TEST_CHANGES` above, with the
  same task-wide reach). Only the edit tools are seen, not `sed -i`.
- **`guard-commit-message.sh`.** Judges a message it can read: `-m`, `--message`, `-F file`, `-F -` with a
  heredoc, `-m "$(cat <<'EOF' ...)"`. An editor commit, `--amend --no-edit` and a message built by a command
  substitution are not judged. The subject must start with a type from the default list (`feat`, `fix`,
  `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`; replace it with
  `MENTIS_COMMIT_TYPES`), may carry a scope and a breaking `!`, and its description starts lowercase unless
  the first word is an acronym. Git's own `Merge`, `Revert`, `fixup!` and `squash!` subjects pass. Attribution
  is a line that looks like a trailer or a "generated/written/created with|by|using" sentence and names an
  AI assistant by name; a human co-author passes. *Limit:* a name list ages; extend it when a new assistant
  appears.
- **`guard-destructive.sh`.** `rm -rf` of `node_modules`, `dist`, `build`, `coverage` and the other
  plainly rebuildable directories passes, as do `--force-with-lease`, `git reset --soft`, `git clean -n`,
  `branch -d` and a `DELETE` with a `WHERE`. Anything leaving the working tree, a wildcard, or a path that is
  not on that short list is refused. SQL is judged only when a database client is a command of the same line,
  so `grep "DROP TABLE" migrations` passes; `cat dump.sql | mysql` is not seen. `MENTIS_ALLOW_DESTRUCTIVE=1`
  in the human's own environment, set before the session, lifts the guard; the same text inside the command
  does nothing. *Limit:* a destructive action behind a `make` target, a script or an alias is not seen. A
  "freeze" mode that confines writes to one directory is not here: one worktree per task does that job.
- **`session-start-using-mentis.sh`.** Reads the `source` of the session start and acts for `clear` and
  `compact` (override with `MENTIS_SESSION_START_SOURCES`). The text it prints is **derived** from
  `skills/using-mentis/SKILL.md` at run time (frontmatter, `When`, `Output / checkpoint` and `Origin` dropped,
  the rest as written), so editing the block edits the reminder and there is no second copy to forget. The
  file is found through `MENTIS_USING_MENTIS`, then next to the hooks directory, then the project's and the
  user's `.claude/skills`. Not found: prints nothing.

**Using them from another harness.** The behaviour is in markdown and in these scripts, not in one product.
The contract is small: a JSON object on standard input (`tool_name`, `tool_input` with `command` or
`file_path` and the edit strings, `cwd`, `session_id` for the session-scoped hooks, `prompt` for the correction detector, `path` as an alternative
to `file_path`, and `source` for a session start), exit code 2 to refuse with the
reason on standard error, exit 0 to allow, standard output of a session-start hook added to the context. A
harness with a different payload shape adapts the few lines that read it (`load_payload` and the field
names in each `main`); the command reader, the patterns and the messages carry over unchanged. Where a
harness has no pre-execution hook at all, the same checks belong in a git hook or the CI job.

Checked by `bin/test_hooks.py`: each hook with the commands it must refuse and, as importantly, the ones it
must not (quoted text, the safe spelling of the same action, an ordinary neighbour), plus fail-open on a
malformed payload and the executable bit on every file in this directory.

Origin: the five ideas come from the MIT-licensed `affaan-m/ECC` hook set (a no-verify blocker, a config
protector, a commit-quality check, a safety guard) read 2026-10-02, and from the session-start context
re-injection pattern. Rewritten here as readable shell and python that fail open, anchored on the command
boundary instead of a substring match, with the message and config rules of this repository.
