# agent-hook-guard-pitfalls §1 — Signalling

## 1.1 How a hook says no
1. **Two refusal forms appear in the repositories read.** One repository documents exit code 2 with the reason
   on standard error: the call is blocked and the text is shown to the agent. The other two answer with a JSON
   object carrying a permission decision of "deny" and a reason, and exit 0.
2. **Write the message for the agent.** The exit-code repository's README says a good block message is a
   correction, not an error: it names the command to run instead, so the agent fixes itself in the same turn.
   Say what was blocked, why, and what to do instead.
3. **Only the documented refusal path blocks.** One of the repositories states in a script's docstring that
   exit 2 is the only blocking exit code and that a crash, which exits 1, is a non-blocking hook error: the
   error is shown to the user and the call proceeds. The failure policy follows in §2.
4. **A launcher can exit 2 on its own.** One repository's log records a configuration commit that wired a hook
   script which existed only in an unpushed commit; the launcher exited 2 on every call of that tool, and
   exit 2 blocked them. A missing script behind a launcher is therefore a fail-closed accident, not
   always a fail-open one.

## 1.2 Deny versus ask
1. **A decision of "deny" refuses; "ask" hands the choice to a person.** One plugin's README, citing the hooks
   reference, says the reason of an "ask" is shown to the user and the reason of a "deny" to the agent. Write
   each text for its own reader and test what each one receives.
2. **In a run with nobody to answer, "ask" is refused.** The spawn-cap plugin documents that in a headless
   run without a permission host, and in the mode that never prompts, anything that would prompt is denied, so
   its ask threshold becomes the effective stop; it advises setting the ask and deny thresholds equal for
   unattended runs. Another repository maps its "ask" to "deny" in the two permission modes where nobody
   answers. Decide what an unattended run should do and test it.
3. **A field that stops the session does not block the call.** One repository's README and a code comment say
   that a "continue: false" field alone ends the agent loop only after the tool has run, and that blocking needs
   the deny decision; that guard sends both for its destructive patterns. A second repository reports that
   current builds ignore "continue: false" on the instructions-loaded event, verified live by its author.
   Treat any field other than the documented refusal path as unproven until a test shows it blocks.
4. **Two hooks that rewrite one call collide.** The same repository's log records that when two pre-tool hooks
   both return a rewritten input for one call, the CLI keeps the last one it reads, so one hook's rewrite
   silently replaces the other's. It fixed this by making one hook skip the calls that the other one rewrites.
   Own guidance: do not give two hooks the same call to rewrite.

## 1.3 Where the hook fits
1. **A hook is a speed bump with an exit.** The guard-test-changes and verify-gate hooks in
   [`hooks/README.md`](../../../hooks/README.md) state their own limits (indirection it does not parse,
   obfuscation, other tools); a guard written here has the same ones.
2. **The config-guard plugin states the same limits for itself:** interpreter one-liners, restoring a config path
   with git, changing permissions, and paths built from variables are not caught, and its own README calls
   it deliberately not a full shell parser.
3. **Pair a hook with isolation for what must not happen.** Own guidance: network and file limits in
   `agent-sandbox-egress-pitfalls` hold when a pattern misses.
