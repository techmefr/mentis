# agent-hook-guard-pitfalls §3 — Overrides and self-protection

## 3.1 In-band and out-of-band overrides
1. **In-band: the bypass is a marker in the agent's own command or message.** The bash-guard repository lets a
   destructive migration through when the command itself carries an explicit variable, and says the point is that
   typing it turns an accident into a decision. The third repository gives each blocking hook a string opt-out
   named in its deny message, written as a comment in the command or in the message text, so that a false
   positive costs one retry.
2. **The cost of in-band is visible in the sources.** The third repository records the poll guard's tag being
   typed as a shell argument three times, so its deny text now says where the tag goes. Own guidance: an
   agent can write the marker as easily as a person can, including after reading an injected instruction,
   so an in-band marker is a convenience for a cooperative agent, not an authorisation.
3. **Out-of-band: the bypass is read from the hook process's own environment,** not from the tool input. The
   config-guard plugin allows a protected change when its allow variable is the literal string true, and the
   spawn-cap plugin does the same with its own variable. The spawn-cap README says hook processes inherit the
   environment Claude Code was launched with, so the variable is set in the settings environment block and
   needs a restart. config-guard's README also suggests exporting it for one shell call, so whether the agent
   can set it depends on where you set it; check that.
4. **Repository precedent for out-of-band:** `hooks/README.md` documents its test-change guard's override as an
   environment variable the human sets before the session, and says nothing in the diff can unlock it; it also
   gives the limit that a task-scoped override stays on for the whole task.
5. **Choose by threat** (own guidance). In-band suits a guard that is a reminder for a cooperative agent.
   Out-of-band is required where the agent must not be able to switch the guard off.
6. **Log every override.** Both plugins write an entry marked as an override to their log directory, and the
   spawn-cap plugin still records the spawn in its ledger while the bypass is set.

## 3.2 Guarding the guard
1. **A guard's configuration is a thing to protect.** The config-guard plugin exists for this: it denies
   writes, in-place edits, moves, copies onto, symlink swaps and deletes of the settings files that register
   hooks and permissions, the hook scripts, hook manifests, the MCP configuration and plugin manifests, and
   at its strictest level the instruction files. Reads always pass.
2. **Creating a protected file counts as a mutation.** Its README says a file that does not exist yet can be
   created to register a hook, and cites an advisory on that persistence route; it also resolves symlinks
   before checking file paths.
3. **Its listed limits apply to you too:** interpreter one-liners, restoring a path through git, permission
   changes, variable-built paths, and a redirect through a symlinked directory are not caught, and it sees only
   the agent's own tool calls. Its README points to a sibling hook on the configuration-change event for
   changes made by anything else.
4. **Also deny those paths in isolation** (own guidance): see `agent-sandbox-egress-pitfalls`.
5. **A reminder is not a block** (own guidance). A message that asks the agent to be careful is a request; the
   edit is stopped by a deny or an out-of-band lock. The config-guard plugin offers a per-level ask mode that
   prompts instead of denying, which suits intentional edits.
6. **A guard that blocks its own installer surprises people.** The same README warns that once active it also
   blocks the plugin install and disable commands, because the plugin manager rewrites configuration: install
   the others first or set the allow variable for that one call.

## 3.3 Guarding tests
1. **A test-protection plugin is narrower than "the agent cannot edit tests".** The protect-tests plugin blocks
   deleting test files or directories, renaming a test file to a disabled name, adding a skip, expected-failure or
   ignore marker to an existing test, and at its strictest level writing a new test file that is already
   skipped. It does not block new tests, renames to another test name or editing test bodies, and it fails open on
   malformed input.
2. **The repository's own version is different:** the guard-test-changes hook in
   [`hooks/README.md`](../../../hooks/README.md) refuses an edit that makes a pre-existing assertion disappear
   or change, and lists its limits. Compare the two designs and do not stack both (own guidance).

## 3.4 Ledgers and counters
1. **Keep a per-session append-only ledger.** The spawn-cap plugin appends one line per allowed or asked spawn
   to a file per session and uses the line count as the budget. Its README gives the reason: parallel tool
   calls fire parallel hook processes, appended lines survive that, and a read-modify-write counter does not.
2. **A ledger the agent can reach is not tamper-proof.** The same README lists as limits that the file is plain,
   an agent with a shell could delete it, and the config-guard plugin does not cover that directory yet. Own
   guidance: if the ledger is evidence, keep it where the agent's file isolation forbids writes.
3. **A counter has a reset policy.** That plugin resets by deleting the session's file, prunes ledgers untouched
   for seven days, continues the count when a session is resumed, and can overshoot a threshold by a
   parallel batch. A declined "ask" still consumed one unit. Write down the equivalent for yours.
4. **A budget has two thresholds and blind spots.** The plugin asks from a first threshold and repeatedly after
   it, then denies at a hard one, each set by an environment variable; its README says only spawns made
   through the tool are seen, so a script that starts agents another way is invisible to it.
