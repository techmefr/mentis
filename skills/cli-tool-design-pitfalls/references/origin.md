# cli-tool-design-pitfalls: origin and source stamps

> Provenance of `skills/cli-tool-design-pitfalls`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from our own knowledge of command-line tool design, with the points listed under sources checked against specifications and official documentation on 2026-10-20, never run: no tool was built or
tested while writing it.

## Sources (read 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| no-color.org convention page | web page, facts only, nothing copied | Trigger is a non-empty variable, scope is tools that colour by default, flag and config override it (§1.4.2, §1.4.6) |
| freedesktop base-directory specification | specification, facts only, nothing copied | Four variable names, defaults, absolute-path requirement (§2.2.4) |
| POSIX specification (Open Group, 2024 edition): shell command language 2.8.2 exit status; base definitions chapter 12 utility conventions | specification, facts only, nothing copied, read 2026-10-20 | Exit status ranges and reserved values (§1.2.2), double dash and single dash, option ordering (§2.1.6) |
| POSIX specification (Open Group, 2024 edition): utility syntax guidelines 12.2 (guidelines 3, 5, 6, 9, 10, 13) | specification, facts only, read again 2026-10-20 | Double dash is guideline 10, lone dash is guideline 13, options before operands is 9 (§2.1.6) |
| freedesktop base-directory specification, version 0.8 (8 May 2021) | specification, facts only, read again 2026-10-20 | Four variables, defaults, unset-or-empty fallback, absolute paths (§2.2.4) |
| GNU grep manual, exit status section; GNU coding standards, command-line interfaces | official manuals, facts only, rewritten, read 2026-10-20 | Non-failure non-zero codes (§1.2.3); version and help options, long option for every short one, output option (§2.1) |
| Node.js documentation: process (exit and exitCode, signal defaults, process I/O note, exit codes) | official documentation, facts only, rewritten, read 2026-10-20 | Forced exit truncating pipe output, signal exit codes (§1.1.5, §1.5.1) |
| Python documentation: argparse | official documentation, facts only, rewritten, read 2026-10-20 | Prefix matching default, status 2 and stderr for invalid arguments (§2.1.7, §1.2.2) |
| spf13/cobra: `LICENSE.txt`, `site/content/user_guide.md`, `site/content/completions/_index.md` | Apache-2.0 (`LICENSE.txt` read 2026-10-20, no holder named in the text) | Unknown-command suggestions, unknown flag error, completions generated from the command tree (§2.1, §2.6) |
| docker/cli: `LICENSE`, `docs/reference/commandline/login.md` | Apache-2.0, Copyright 2013-2017 Docker, Inc. (read 2026-10-20) | Password from standard input keeps it out of shell history and logs (§2.3.1) |
| cli-guidelines/cli-guidelines (published command-line guide) | CC BY-SA 4.0 (`LICENSE` read 2026-10-20) | Not opened: share-alike |

## Removed
- Nothing from the guide. The two convention pages were rewritten, no sentence copied.

## Not verified
1. **Sourced on 2026-10-20:** the colour variable, base-directory defaults, POSIX exit-status and syntax guidelines, grep's three-code model, Node's pipe and signal behaviour, prefix matching, unknown-command suggestions, completion generation, and the shell-history half of the secret-argument point. **Still unsourced:** the stream split in general, exit-code classes beyond the POSIX reservations, structured-output rules, prompts on non-terminals, dry-run and confirmation rules, error-message shape, secrets in process lists, configuration precedence and unknown-key policy, resumability, every "Checks" section.
2. **Directory conventions** other than Linux's (macOS, Windows) were not read; re-read the platform's rules before fixing names.
3. **Guide.** No permissive command-line design guide found, searched: the guide's repository (CC BY-SA), convention pages, POSIX and GNU pages, two library documentations (Cobra, argparse), Docker's CLI reference. A clean-room reading of the share-alike guide was not done.
4. **No command, flag or code was executed.**

Dogfood 2026-10-20: one static read on a real project, nothing run; fixes: a skip-when line for internal build scripts, a swallowed environment error reported as success (§1.2.6), a path relative to the working directory and a missing prerequisite (§1.1.6), an unknown flag falling through to write mode (§2.1.8), the dry-run rule exempted for regenerated directories (§2.4.6), and the deprecation rule scoped to published interfaces. The status stays 🟡.

## Related blocks
`shell-scripting-conventions`, `bash-pitfalls-and-bats`, `mcp-server-design-pitfalls`, `api-design`,
`deprecation-migration`, `credential-lifecycle-pitfalls`.
