# agent-hook-guard-pitfalls §2 — Failure policy

## 2.1 Outcomes when a guard breaks
1. **Fail open: the action goes ahead.** The bash-guard repository lists it as a design rule (a malformed payload
   returns 0, and its tests pin that). The config-guard and protect-tests plugins also print an empty result on
   any error, including config-guard, which protects the agent's own guardrail configuration.
2. **Fail loud: the action goes ahead and the failure is visible.** One repository's convention is that a guard
   which cannot parse its input crashes with a traceback, a non-blocking error shown to the user, rather than
   approving silently. Its background-poll guard documents the same choice, and says that a loud guard
   never strands a call it cannot reason about.
3. **Fail closed: the action is refused.** None of the three repositories implements this on purpose. Own
   guidance: use it for a security guard, where "I could not check" must not mean "allowed"; the repository's
   own `hooks/README.md` makes that choice for its gate and says why, and also limits it to the guarded path
   so an unrelated call still works.
4. **It is a per-guard decision, written down.** The repositories differ: the bash-guard repository states
   fail open as a rule, the plugins print an empty result on error, and the third repository's convention is
   fail loud. Even there the log describes three of its hooks as failing open on an exception, meaning a
   traceback on stderr and a non-blocking exit 1. Do not inherit a policy from a template.

## 2.2 Crashes that read as allowed
1. **An uncaught exception in a script exits non-zero but not blocking,** so the guard allows everything it
   meant to judge. Catch at the top and map the failure to the policy chosen in §2.1.
2. **Text encoding crashes hooks, and can corrupt instead of crash.** One repository's log records, on a
   Windows machine with a legacy code page, a hook that died printing a non-ASCII warning and so lost the
   rest of its output, and a guard that died reading a transcript containing a byte the code page leaves
   undefined. A fourth hook did not crash but printed corrupted text, because the CLI decodes hook output as
   UTF-8. The fixes were explicit UTF-8 on every text read and write, a reconfigured standard output, and a
   global environment variable that makes UTF-8 the default. Test with non-ASCII input.
3. **A platform call that does not exist is a crash too.** The same log records a hook that called a Unix-only
   function and died on every call of its class on Windows.
4. **A missing script or interpreter is a crash.** If the hook runs through a launcher, test the case where
   the launcher or the script is absent (§1.1 shows that this can block instead of allow).
5. **Find the cause where it is kept.** The log says the full standard error of a failed hook is stored in the
   session transcript as a non-blocking hook error with the command and exit code; the terminal shows only the
   first line.

## 2.3 Silent breakage
1. **A detector can stop matching without any error.** One repository's log records a detector anchored on a
   literal string that a CLI release deleted: every patched binary then read as unpatched for a month, and
   nothing reported it, because "not found" looked the same as "genuinely absent". Another repository's README
   says that after it moved its hook scripts, a settings entry pointing at the old path became a failing hook,
   which Claude Code treats as a non-blocking error: the guard stopped enforcing with no visible sign.
2. **Let a detector answer "I do not know".** The log's fix was a three-state result (applied, not applied,
   unknown) instead of yes or no, plus a test that runs every detector against the real binary and requires
   one of the two known answers, so a moved anchor fails a test instead of degrading quietly. It also
   anchored on the property the code is for rather than on an identifier a minifier can rename.
3. **Count firings** (own guidance): keep a counter or a ledger line per decision (§3.4), and look for a guard
   that has been silent for longer than its history suggests.
4. **Keep a canary case** (own guidance): a known-bad input that a periodic check runs against the real hook
   and expects to be blocked.
