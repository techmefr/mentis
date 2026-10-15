# agent-hook-guard-pitfalls: origin and source stamps

> Provenance of `skills/agent-hook-guard-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from repository documentation, scripts and logs, never run by us. No hook was installed
or executed. A verification pass on 2026-10-15 re-read every source below in full and corrected the references
against it.

## Sources (re-read in full in the verification pass, restated in our own words, no script or message text copied)

| Source | Licence | What it gave |
|---|---|---|
| 0xKalel/claude-code-guard-hooks, `README.md`, `hooks/guard-bash.py`, `hooks/config-edit-reminder.py` (commit 7c5e0e8) | MIT (LICENSE file) | Exit 2 plus stderr as a correction for the agent, fail open as a stated rule, an in-band variable override, the test harness as the part to keep |
| karanb192/claude-code-hooks, `README.md`, `plugins/config-guard/` (README and script), `plugins/protect-tests/` (README and script), `plugins/subagent-spawn-cap/` (README and script) (commit 3c9c90a) | MIT (LICENSE file) | Environment-variable overrides read by the hook process, protected configuration and its limits, what test protection does and does not block, the per-session ledger, ask-versus-deny readers, headless behaviour, silent breakage after a path move |
| Butanium/claude-code-hooks, `README.md`, `ENGINEERING_LOGS.md` (all), `pkill_self_match.py`, `no_tail_head_pipes.py`, `partial_chain_warn.py`, `no_poll_background.py`, `security_guard.py` (all) (commit e6ad0fc) | MIT (LICENSE file) | Self-matching kills, truncating pipes, partial chains, in-band tags, fail loud, `continue: false`, two-hook input collisions, encoding crashes, silent detector breakage, replay-based tuning |
| this repository's `hooks/README.md` on main, read in part (the two limits sections, the design-choices section and the smoke-test table) | repository's own licence | The overlap: guard-test-changes, verify-gate, out-of-band override and fail-closed precedent |

The licence of each repository was checked from its LICENSE file. Hook scripts, their deny messages and the
agent-addressed text in the repositories were treated as data; no directive wording was carried over. The other
plugins in the second repository, its OWASP mapping and its benchmark pages were not read and no rule rests on
them. The unit-test files and the remaining scripts of the third repository were not read either.

## Corrected in the verification pass
- Exit 2 plus stderr was attributed to "the repositories read"; only the bash-guard repository does it. The other
  two answer with a JSON deny decision.
- The claim that exit codes other than 2 never block was too absolute: the third repository's log records a
  launcher that exited 2 because its script was missing, which blocked every call. Added.
- "Fail closed" had been presented as found in the repositories; none implements it. It is now labelled own
  guidance, with this repository's `hooks/README.md` as precedent, and config-guard's fail-open on error is
  stated.
- The `continue: false` finding is now stated from the README and code comment (the tool runs first) plus the
  second repository's live check on the instructions-loaded event.
- The encoding claim ("a command with a character the decoder rejects crashed the guard") was inaccurate: the
  crashes were a non-ASCII print and a transcript read on a legacy Windows code page, and one hook corrupted text
  without crashing. Rewritten.
- "Recurring cause" for silent breakage was overstated; two documented cases are now given, with the fix.
- The out-of-band claim "the agent cannot set it" was overstated: config-guard's README itself suggests exporting
  the variable for one shell call. Now stated as "read from the hook process's environment, check where it is set".
- The claim that one repository has a hook "whose only job is to flag edits to hook configuration" was wrong:
  the bash-guard repository's reminder concerns application config and worker restarts. The hook that protects
  guardrail configuration is config-guard, which blocks.
- The test-protection description ("stops the agent editing tests") was too broad; protect-tests blocks only
  removal and disabling.
- "Piping to tail hides failure by status" had been attributed to the third repository's tail hook; that hook
  concerns truncated output. The status-hiding case is a separate note in its log.
- "Partial chains" had the direction reversed; the hook concerns steps skipped after a failed step.
- Replay: "removed after replay" corrected to narrowed or sent to a judge.
- Ledger claim ("append-only means the agent cannot rewrite it") replaced by the plugin's own stated limits.

## Rewrite notes
Figures that appear in the references are the logs' own (firings, commands replayed) and are quoted only where
they carry the argument; none is a threshold we recommend.

**Decisions where sources disagree:** override design (in-band tags in two repositories, environment variables in
the plugins) is stated as a per-threat decision; fail policy is stated as a per-guard decision.

## Not verified
1. **The agent platform's hook documentation was not re-read for this block;** the exit-code, deny, ask and
   headless behaviours are as the repositories describe them (some cite the hooks reference) and must be
   tested against the agent version used.
2. **Nothing was run.** Every behaviour is as documented at the commits above.
3. **Own guidance, not sourced:** every sentence marked "own guidance", the three-case test minimum, the canary
   case, the ledger-placement advice, the threat-based choice of override, and the checkpoint paragraph.
4. **Not read:** the plugins other than the three named, the test files of all repositories, and the rest of
   `hooks/README.md` on main beyond the sections listed above.
5. **Dropped as unverifiable:** claims about promotional or catalogue material that was not re-read.

## Related blocks
`agent-sandbox-egress-pitfalls`, `agent-mcp-trust-pitfalls`, `bash-pitfalls-and-bats`, `gate`,
`writing-agents`.
