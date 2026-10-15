# agent-hook-guard-pitfalls §4 — Matcher traps and testing

## 4.1 Traps in command matching
1. **Self-matching process kills.** The third repository's log explains that the shell tool runs each command
   inside a wrapper shell whose own command line contains the whole command, so a kill-by-full-pattern
   whose pattern matches the command text kills that wrapper: exit 143 or 144, empty output, nothing after
   it runs. Its hook denies a pattern that matches the command's own text and names two fixes: the option
   that makes the tool spare its ancestors where the installed version has it, or bracketing one character of
   the pattern so the pattern stops matching its own text (not for a one-character pattern).
2. **The same trap breaks waits.** A listing by full pattern that matches its own shell makes a loop that waits
   for the process to disappear never end, makes a test for presence always true, and makes counts off by one
   or two; the hook adds a note for those cases instead of denying.
3. **Truncating a pipe loses output.** The same repository's hook denies a tail or head pipe on a background
   command, because the output goes to a file that is read afterwards and the pipe throws away all but a few
   lines, stack traces included. It exempts pipes after reader and short-output tools, inside quotes,
   here-documents, command substitutions and wait-loop conditions, and offers a documented opt-out.
4. **A pipe can also hide a failure.** The log of the same repository says a failed push piped to tail exits with
   success, so a guard that reads the exit status cannot see it. Own guidance: write scripts with a pipefail
   option and read the real status.
5. **Partial chains.** In a chain joined by the and-operator, a failure skips every later step. The repository's
   post-failure hook adds a note naming the file- or remote-changing steps after such an operator that may not
   have run, because agents carried on as if a commit or an edit had happened. It cannot tell which step failed,
   so it names candidates, and it is blind to failures a pipe hides.
6. **A pattern list is not a parser.** The config-guard README calls itself deliberately not a full shell parser,
   and a log entry says a pattern made of everyday tokens cannot be made precise by regular expression without
   parsing shell. Quoting, variables, interpreters and a shell inside a shell defeat text matching: a guard
   that blocks one spelling blocks one spelling.

## 4.2 Measure false positives from history
1. **Replay the pattern over archived real commands before release.** The log records this repeatedly: a
   tail-and-head guard audited over its last hundred firings found 35 harmless ones and was narrowed to
   match by producer; a failed-chain note had a third of its first firings wrong over 546 failed calls and was
   narrowed before wiring; a kill-pattern hook was replayed over 702 archived commands, and a subagent review
   of the flagged ones found no false deny and one missed deny, which was then fixed.
2. **A noisy detector can move from deny to review.** A download-into-shell pattern fired on text that was data
   in six of its first twelve firings and none was harmful, so the repository sent it to a judge instead of
   denying. Own guidance: count blocked-by-mistake, not only blocked-correctly; a guard that blocks real
   work gets disabled.
3. **Re-probe after upgrades.** The log says to re-probe a hook's assumptions after CLI updates, and keeps the
   probe list as test fixtures.

## 4.3 A test harness per guard
1. **One test file per guard,** feeding the hook its real input format on standard input and checking the
   exit code or the decision and the text. The bash-guard repository ships eighteen cases: every rule's block,
   every exemption and the fail-open plumbing, and says that if you adapt the patterns the harness is the part to
   keep. The plugins run unit tests and standard-input tests in CI.
2. **Three cases at least** (own guidance): a blocked input, an allowed look-alike, and a broken input such as
   malformed JSON or non-ASCII text, asserting the policy chosen in §2.
3. **Run the real hook the way the agent does.** The third repository keeps a smoke test that starts a real
   agent session for one of its hooks and calls it the only check that matters after an agent update.
   Own guidance: a test that imports the function does not catch a wrong path or a missing executable bit.
4. **Run it in CI** and when the agent's version changes, since the input format is the agent's, not yours.
