# bash-pitfalls-and-bats §2 — bats

Source: the bats-core documentation (version 1.14.0, MIT): `writing-tests.md` and the gotchas page, read
2026-10-08.

## 2.1 What `run` does
1. **`run` always succeeds.** It stores the command's exit code in `$status` and its output in `$output` and
   `${lines[@]}`. A test that calls `run` and asserts nothing passes whatever the command did; assert on
   `$status` and on the output, or leave `run` out.
2. **Leave `run` out when you only need success.** Bats sets `set -e` for every test, so the bare command already
   fails the test. `run -0 cmd` is documented as equivalent to `cmd`.
3. **`run` executes in a subshell**, so a variable the command changes is not changed afterwards. To test a
   function's effect on variables, call it without `run`.
4. **Options go before the command.** If the command starts with `-`, put `--` first. `--keep-empty-lines`
   retains blank lines in `${lines[@]}` (they are dropped by default) and `--separate-stderr` fills `$stderr`
   and `${stderr_lines[@]}` apart from `$output`.
5. **A pipe after `run` is not inside it.** `run a | b` parses as `(run a) | b`. Use `run bash -c 'a | b'` or
   `run bats_pipe a \| b` (the escaped bar is required, and `bats_pipe` fails when it finds none). `bats_pipe`
   mimics `pipefail` by default and takes `-N` or `--returned-status N` to choose which command's status is kept.

## 2.2 Negation and failures
1. **A bare negated command only fails the test when it is the last command.** Bash does not trigger `set -e` on
   `!`. Use `run !` (bats 1.5.0 and later) for "must fail"; on older versions append `|| false` to the negated
   command (`! x || false`) or assert on `$status`.
2. **Return 0 for success in helpers.** A helper that returns 1 to mean true works against bash's convention and
   breaks tests under `set -e`.
3. **`teardown` failures fail the test, but only through the last command or an explicit `return`.** Unlike a test
   body, a failing command in the middle of `teardown` does not stop it and does not fail it, because errexit is
   off there. Make the last command the one that must succeed, or `return 1` explicitly.

## 2.3 Hangs and output
1. **A background process started from a test inherits file descriptor 3 and hangs the run.** Bats waits for the
   descriptor to close. Close it when launching anything long-lived: `command 3>&-`.
2. **Print with `>&3`, not stdout, when the text must always show.** Text on standard output or error inside a
   test is shown only when the test fails. Avoid printing outside `@test`, `setup*` and `teardown*`: free code runs
   once per execution context, and stdout there can break the TAP plan line.
3. **A `bats:focus` tag filters the suite to the tagged tests and forces the exit code to 1** so a committed tag
   cannot pass CI silently. `BATS_NO_FAIL_FOCUS_RUN=1` disables that and must not be set in CI.

## 2.4 Helpers and structure
1. **`load` sources a helper from inside a function, so a bare `declare` there is local** and disappears when
   `load` returns. Use `declare -g` or plain assignment in helper files. `load` appends `.bash` to the name; to
   load a `.sh` file use `source`.
2. **A test cannot be registered in a loop.** `@test` is preprocessed into a function, so wrapping it in `for`
   only redefines it. Write the cases out, or loop inside one test and say which case failed.
3. **Bats does not take parameters.** Pass values to a test file through environment variables.
4. **Variables exported in `setup_file` are visible to every later hook and test of the file;** `setup_suite` and
   `teardown_suite` must live in a `setup_suite.bash` file, and `setup_suite` must be defined there.
