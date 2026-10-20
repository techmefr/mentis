# cli-tool-design-pitfalls §1 — Streams, exit codes and scripting

Source: own guidance throughout (no external guide was read; see origin). Where a point rests on a widely documented convention, it says so.

## 1.1 Two streams, two jobs
1. **Standard output carries the result and nothing else.** What another program would want to read goes there. Symptom of a violation: piping the tool into another breaks because a "Done!" line is in the data.
2. **Standard error carries everything meant for a human:** progress, warnings, prompts, hints, and error messages. It is also where a script's log goes.
3. **Print nothing on success when there is nothing to report,** for commands whose job is an action. Silence plus a zero exit code is a result.
4. **Do not print a stack trace for an expected failure** (bad input, missing file, no network). Print one line that says what failed and what to do, and keep the trace behind a debug option.
5. **Flush before exit and handle a closed pipe quietly.** A reader that stops early (a head-style filter) must not make the tool print an error or hang.

## 1.2 Exit codes
1. **Zero means success, non-zero means failure, always.** Test it: break the input and read the code that the shell reports.
2. **Use distinct codes for distinct classes a caller would branch on** (usage error, not found, permission, conflict, network, internal error) and publish the table. Do not use more than a handful, and never use codes above the portable range.
3. **Commands that compare or search can use a non-failure non-zero code** (found nothing, differences found); document it, since a script run in strict mode treats it as an error.
4. **A command that does several things reports the worst outcome,** and says which parts succeeded on standard error. A batch that fails half-way must not exit zero.
5. **Usage errors exit non-zero and print the short usage on standard error,** not on standard output.

## 1.3 Machine-readable output
1. **Offer a structured format flag (a JSON output option, or one record per line) for any command that prints data,** and keep the default for humans. The structured form is a contract (§2.6).
2. **Never make scripts parse the human table.** Column widths, colours and wording change.
3. **Emit one JSON document, or one per line, never a mix of text and JSON.** Put errors in the same structure on the error stream when the structured option is on.
4. **Stable ordering and stable field names;** a script that reads the output depends on both. Add fields freely, remove or rename only with a deprecation.
5. **Use ISO 8601 for times and plain numbers for sizes in the structured form;** leave humanized "3 hours ago" to the human form.

## 1.4 Terminal or not
1. **Check whether the output stream is a terminal before using colour, spinners, progress bars or cursor movement.** Off a terminal, print plain lines.
2. **Honour the conventions for turning colour off:** a no-colour environment variable, a colour flag, and a dumb-terminal setting.
3. **Never prompt when input is not a terminal.** Fail with a message that names the flag that supplies the missing value. A hung CI job is the worst failure mode of a command-line tool.
4. **Provide a flag for every prompt's answer** and a "yes to all" for confirmations (§2.4), so that the interactive path and the scripted path reach the same code.
5. **A progress display must not be the only record.** Log the same events as lines on standard error when not on a terminal.

## 1.5 Signals, interruption and long runs
1. **Handle interruption (the usual terminal interrupt and terminate signals) by cleaning up and exiting with the conventional code,** not by leaving partial files, locks or half-written output.
2. **Write to a temporary file and rename it** when the output file must never be half-written.
3. **Make long commands resumable or idempotent** where you can, and print a count of what was done and what remains.
4. **Time out network calls with a flag to change the limit,** and say which step timed out.

## 1.6 Checks (own guidance)
1. Run the tool with output redirected to a file and error to another: the first has only the result, the second only the messages.
2. Run it under a shell in strict mode with each failure class and read the exit codes against the published table.
3. Run it with input closed and with no terminal: it never waits.
4. Run the structured output through a JSON parser.
