# quality-bar-and-ratchets-pitfalls §1 — Writing the bar

Source: the constraint-driven-development skill of addyosmani/agent-skills (MIT), read 2026-10-20.

## 1.1 One file, a reason and a command per number
1. **Symptom:** the standards live in a wiki, three READMEs and somebody's head, and two agents on the same
   repository apply different ones. **Check:** one file at the repository root holds the bar and the agent
   instructions point at it. **Fix:** write it once; a change to it appears in review where a human reads it.
2. **Every number has a reason and a command.** A table row is rule, the command that produces the verdict, and
   where it runs (every edit, end of task, CI, preview deployment). A number with no command is an aspiration:
   remove it or give it its command. A number with no reason is deleted by the next person who hits it.
3. **Detect before asking.** The language, test runner, linters, coverage output and CI already hold most of the
   answers; read them, report in two lines, and ask only what is left. A long intake produces a bar nobody can
   explain, so every question carries a default and "I do not know" is a complete answer.

## 1.2 A small floor with no setup
1. The floor is the set of rules that need no tool: no new suppression comment, no unfinished stub, no skipped
   or deleted test without a reason, no secret in source, and the bar file is not weakened to pass a change.
2. A floor can be enforced from day one with nothing installed, because it reads the diff, so the numbered
   dimensions can be added one tool at a time instead of blocking the first protected commit.

## 1.3 Pick the checker the ecosystem already uses
1. **Symptom:** a hand-written checker for type errors, secrets or dependency risk; two agents, two
   implementations, two results. **Fix:** use the de facto tool for the dimension and keep the team's existing
   configuration. Write a checker from scratch only for the floor, which has none (§3).
2. Re-read a tool's current options and licence before relying on it (`skills/source-freshness`); a rule registry
   may carry its own terms.

## 1.4 At least one external check
Rank checks by one question: can the agent make this pass by writing code that does not work?
1. **External:** a standards-based accessibility scanner, a vulnerability database lookup, a real-browser
   measurement. The agent cannot argue with them.
2. **Project:** the team's lint rules and layer boundaries. A human owns the file.
3. **Suite:** the project's own tests. The most useful and the only circular one: the author wrote both sides.
4. **Check:** a bar made only of the third kind has no outside opinion. **Fix:** add at least one of the first
   kind, or write down that none applies (a command-line tool has no page to measure).

## 1.5 Place each check by cost
1. **Symptom:** a slow check sits in the edit loop, the agent stalls, someone passes the skip flag, and the bar
   still looks alive and is not. **Fix:** cheap checks on the edit (types, lint, secrets, the floor), related
   tests and changed-line coverage at the end of a task, everything else in CI or on a deployed preview.
2. **Scope expensive checks to the diff.** Changed lines for coverage and mutation testing, a path list for a
   static analyser. Read the coverage report the suite already writes and intersect it with the diff instead of
   running the suite twice.
3. Tools that need a running page (performance, accessibility scan) belong to the stage that has one; when the
   project has no page, drop the dimension rather than invent a check that cannot run.
4. The commands exist in two places, the bar file and the project's scripts. The bar file is the source (it
   carries the reason); the scripts mirror it and the file wins when they differ.

## 1.6 Scan output and secrets
1. A secret scanner runs in its redacting mode; without it the matched value lands in the transcript, then in a
   log or a commit message. **Fix:** report rule and location, never the value.

## 1.7 Where it is not worth it
A bar is not for a two-week prototype or a one-off script. The floor alone is still cheap; the numbered
dimensions are not.

## Checks
1. Every number has a reason and a command that runs today.
2. At least one check is external, or the absence is written down.
3. Each check names where it runs, and the edit-loop stage is fast.
4. The agent instructions point at the file.
