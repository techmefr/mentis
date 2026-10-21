# cli-tool-design-pitfalls §2 — Surface, configuration and safety

Source: own guidance, except the directory defaults in §2.2.4 checked 2026-10-20 against the freedesktop base-directory specification (facts only, rewritten). See origin.

## 2.1 Commands and flags
1. **Use a noun-verb or verb-noun grammar consistently across subcommands,** and choose once. Mixed grammars are the commonest sign of a tool that grew by accretion.
2. **One word per concept everywhere:** if one command says "remove", none says "delete" or "rm". Flags with the same meaning have the same name in every subcommand.
3. **Every flag has a long form; frequent flags also get a short one,** and short ones keep the usual meanings (help, version, verbose, quiet, output, force). Do not reuse a conventional short flag for something else.
4. **Prefer flags to positional arguments past the first one or two,** because positions are unreadable in a script and impossible to extend.
5. **Always support the help flag and the version flag at every level,** and print the same version that the package manager reports. Help goes to standard output with a zero exit code when asked for.
6. **Accept a single dash for standard input or output where a file is expected,** and the double dash to end option parsing, so file names that start with a dash are safe (POSIX utility syntax guidelines, read 2026-10-20: the first double dash that is not an option argument ends the options and everything after is an operand; a lone dash means standard input, or standard output where output is clearly meant; options come before operands and their order should not matter).
7. **Do not guess ambiguous abbreviations or typos silently;** suggest the likely command and exit non-zero.
8. **An unknown flag is an error, never a fall-through to the default mode.** When the default mode writes or deletes and a flag selects the safe mode (a check, a dry run), a mistyped flag must stop the program, not run the default. Symptom: a check flag misspelled in a pipeline rewrites the tracked file and the step goes green. Check: pass a misspelled flag and read the exit code and the working tree. Fix: parse arguments against a list of known flags and reject the rest, with the usage on standard error (own guidance).

## 2.2 Configuration precedence
1. **One order, documented: flag, then environment variable, then project file, then user file, then system default.** Show the effective value and its source with a "show configuration" command.
2. **Environment variables use one prefix** for the tool and map to flag names mechanically.
3. **Do not read configuration from the current directory without saying so,** since running the tool in an untrusted checkout then runs its settings (own guidance).
4. **Follow the platform's directory conventions for user files** (config, cache, data), not a dot-folder per tool where the platform has a standard place. On Linux the base-directory specification names four variables (config, cache, data, state) with defaults under the home directory (`.config`, `.cache`, `.local/share`, `.local/state`), used when the variable is unset or empty, and requires an absolute path: ignore a relative one (basedir specification, checked 2026-10-20).
5. **An unknown key in a config file is an error with the key's name,** not a silent ignore: a typo otherwise passes for months.

## 2.3 Secrets
1. **Never accept a secret as an argument value.** Arguments appear in the process list and in shell history for every user of the machine. Offer a file path, an environment variable, standard input, or an interactive no-echo prompt (terminal only).
2. **Never print a secret,** including in verbose mode and in error messages that echo the command line or a request.
3. **Redact tokens in debug output** and say in the help that the debug option is safe to paste, or that it is not.
4. **Do not write credentials in the tool's config file in plain text** when the platform has a credential store (own guidance); if you must, set the file's permissions to the owner only and check them when reading.

## 2.4 Destructive and costly actions
1. **A command that deletes, overwrites, sends or spends has a dry-run option** that prints exactly what would happen and changes nothing. The exception is point 6.
2. **Confirm on a terminal and offer a flag that skips the confirmation** for scripts; never make the interactive path the only one.
3. **Scale the confirmation to the damage:** a yes/no for a small change; typing the name of the resource for a deletion that cannot be undone.
4. **Make the common case safe by default** (do not overwrite an existing file without a force flag; refuse an operation that matches everything unless an explicit all flag is given).
5. **Print what was changed, as a count and the identifiers,** on standard error after the action.
6. **A directory the tool itself regenerates needs no dry-run or confirmation.** Removing a build-output directory that is ignored by version control and rebuilt by the same tool destroys nothing a user owns. Check before applying it: the directory is ignored by version control, nothing else writes there, and the tool recreates it in full. Otherwise points 1 and 2 apply (own guidance).

## 2.5 Help and error messages
1. **Help starts with a one-line summary and an example,** then the options. People read the examples first.
2. **An error message says what failed, why when known, and what to do next,** in that order, with the offending value quoted.
3. **Point to the exact flag, file or setting** involved; "invalid input" alone is a defect.
4. **Keep error wording stable enough to search for,** and put a short code in it when you have a documentation page per error.
5. **No emoji or decoration needed to find the error:** it begins with a fixed word on standard error (own guidance).

## 2.6 Completions and compatibility
1. **Provide shell completions generated from the same definition as the parser,** not written by hand; a second list drifts.
2. **Subcommands, flags and exit codes published in a release are an interface.** A script that only the repository's own pipeline calls, with no release and no outside users, is changed together with its callers in one commit and needs no deprecation period. Deprecate with a warning on standard error for at least one release, keep the old spelling working, and say in the message what replaces it.
3. **Structured output fields are an interface too** (§1.3). Version the format when you must break it.
4. **Check the tool on the shells and platforms you support,** including quoting and path separators (own guidance).

## 2.7 Checks (own guidance)
1. List every flag and subcommand and look for synonyms, inconsistent names and a reused short flag.
2. Search the code for a secret read from an argument vector.
3. For each destructive command, run the dry-run, then the real command with the skip flag, and read both outputs.
4. Run each error path and check the message names the cause and the remedy.
