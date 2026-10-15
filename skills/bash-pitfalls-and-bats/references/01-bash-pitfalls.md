# bash-pitfalls-and-bats §1 — Bash pitfalls

Sources: the Bash reference manual (version 5.3), the Google shell style guide (CC BY 3.0, tree of
2026-10-08) and a community Bash style guide (MIT). Each rule marked "run" was also run once on Bash 5.2.21.

## 1.1 State that disappears
1. **Every command of a pipeline runs in a subshell** by default, so `cmd | while read line; do n=$((n+1)); done`
   leaves `n` unchanged afterwards (run). Feed the loop with process substitution (`done < <(cmd)`) or read the
   output into an array with `readarray -t lines < <(cmd)` (Bash 4 and later); the style guide recommends both.
   A process substitution hides the status of `cmd`, so check it separately when it matters.
2. **A command substitution is a subshell too**, so an assignment inside `$( )` does not persist.
3. **`declare` inside a function makes a local variable**, including when the file is sourced from a function;
   add `-g` for a global (run). This is the cause of "the variable is set but empty" in sourced helper files.

## 1.2 Statuses that lie
1. **`local v=$(cmd)` returns the status of `local`, not of `cmd`**, so a failure of `cmd` is lost even under
   `set -e` (run). Declare first and assign on the next line: `local v` then `v=$(cmd)`. The style guide gives
   the same advice.
2. **An arithmetic command `(( expr ))` exits 1 when the expression evaluates to zero.** `(( i++ ))` with `i`
   at 0 returns the old value, 0, so it fails and aborts a script under `set -e` (run). Use `i=$((i+1))` or the
   pre-increment `(( ++i ))`, whose value is never zero when counting up from zero.
3. **`set -e` does not fire in several places the manual lists:** a command in a `&&` or `||` list other than the
   last, a command whose status is negated with `!`, any command in the condition of an `if`, `while` or
   `until`, and, when a function or subshell is itself called in such a context, everything inside it. A function
   called as `if f; then` therefore runs its whole body with `set -e` ignored. Check the status explicitly
   for any step that must not fail silently (the failure default is `shell-scripting-conventions` §1, the guard
   rules are §2).

## 1.3 Comparison and tests
1. **Inside `[[ ]]`, `<` and `>` compare strings lexicographically**, so `[[ 10 > 9 ]]` is false (run). Compare
   numbers with `(( a > b ))` or `-gt`.
2. **The right-hand side of `==` and `=~` inside `[[ ]]` is a pattern or a regular expression** unless quoted.
   Quote it when a literal match is meant.

## 1.4 Lists, globs and argument vectors
1. **Build argument lists in arrays and expand them as `"${args[@]}"`.** A list held in a string needs `eval` or
   unquoted splitting to be used, and both break on spaces and metacharacters; the style guide says `eval`
   should be avoided because it munges its input. Forward arguments with `"$@"`, never `$*` or an unquoted
   `$@` (run).
2. **Prefix a wildcard with `./`** (`rm -v ./*`, not `rm -v *`) so a file whose name starts with `-` is not read
   as an option (run). Use `--` before names where the command accepts it.
3. **Never iterate over `$(ls)` or over any unquoted command substitution.** The output is split on whitespace
   and globbed. Iterate over a glob directly, or read delimited output with `while IFS= read -r` from a process
   substitution. Both style guides tell you not to parse `ls`.
4. **Send error messages to standard error** (`>&2`) so they survive when standard output is piped or captured;
   the Google guide states this rule.

## 1.5 Size, and two contested sources
1. **Past about 100 lines, or with non-trivial control flow, rewrite in a language with real data structures.**
   The Google guide gives the 100 line threshold; the house line in `shell-scripting-conventions` §4 is about
   50 and wins when they differ.
2. **One community guide says never to use `set -e`** and lists situations where it does more harm than good.
   Not adopted: strict mode stays the default in `shell-scripting-conventions` §1. The useful part is §1.2.3
   above, the places where it silently does nothing.
3. **The Google guide asks for file and function header comments.** Not adopted: the house rule is no comments
   in code (rule C of `CONVENTIONS.md`); put the intent in names or in the documentation of the script.
