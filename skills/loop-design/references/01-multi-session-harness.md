# loop-design §1 — A loop that spans many sessions

> Section 1 of `skills/loop-design`. Read it when a loop is too long for one context window (a whole application
> built or migrated feature by feature) and each session starts with no memory of the last. It adds the session
> protocol; the goal, the judge and the cap are still `SKILL.md` §2 to §4. 🟡: never run by us. The method comes
> from public descriptions of long-running coding harnesses and our own craft; no source text is taken (see
> `references/origin.md`).

1. **Treat the context reset as the design constraint.** A new session knows only what is in files and in version
   control. Everything a session must hand on is written to one of the two, before it ends. Symptom of keeping
   state "in the conversation": the next session redoes finished work or declares victory early.
2. **Use two kinds of session.** An initializer runs once: it turns the specification into the task list, sets up
   the project, the scripts that start it and the first commit. Worker sessions then run again and again against
   that list. Own guidance: the initializer's output is reviewed by a person before the first worker starts, because
   every later session inherits its mistakes.
3. **Make the task list a decidable file.** One entry per feature, each with a description, the steps that show it
   works, and a pass flag that starts false. Make the list long enough that it covers the specification; a short
   list lets a worker conclude "done" long before the product is. Own guidance: the list lives in the repository,
   in a structured format a script can read.
4. **The list is immutable except for the flag.** Workers may set a flag to pass; they may not delete, reword or
   reorder entries or weaken their steps. This is `SKILL.md` §2.2 and §3 applied to a list: the build side may not
   edit the acceptance conditions. Check: a diff of the list between sessions shows only flag changes, enforced by a
   check that runs on every commit.
5. **Flip a flag only after verifying as a user would.** A unit test passing is not the step list passing. For an
   interface, drive it end to end, in a browser or through its public API, and look at the result. Own guidance:
   a worker that cannot run the application cannot flip a flag; it reports blocked.
6. **One feature per session.** A worker takes the highest-priority failing entry, finishes it, verifies it and ends.
   Symptom of taking several: a half-built second feature at the context limit and a tree that does not run.
7. **Start every worker session the same way.** Read the progress file and the recent commit log, start the
   application with the project's script, and then **re-verify one or two entries already marked passing** before
   touching anything new. A regression found now costs one fix; found ten sessions later it costs a bisection.
   If a previously passing entry fails, fix it first and set its flag back to failing until it is verified.
8. **End every worker session the same way.** Commit with a message that says what changed, update the progress
   file (what was done, what is next, what is known to be broken), leave the working tree clean and the application
   in a state the next session can start. Own guidance: a session that ends with uncommitted work or a broken
   start script has failed regardless of what it built.
9. **Keep the progress file short and current.** It is a handover (`skills/handoff`) written every session: the next
   step, the traps found, the commands that matter. The commit log is the record; the progress file is the briefing.
10. **Stop on the list, a budget, or a human.** The loop ends when every flag is pass and a person has looked at the
    running result, or when the attempt or cost cap of `SKILL.md` §3 is reached, or when a worker reports blocked
    twice on the same entry. Never let the loop end because a worker said it was finished.
11. **Judge from outside.** The verification of point 5 is the worker's own check and can be wrong in the worker's
    favour. Own guidance: run an independent pass over a sample of flags set pass (a fresh session with the
    list and the running application, `skills/sampled-evaluation`), and treat any miss as a reason to distrust the
    batch.
12. **Constrain the worker's commands by an allowlist.** An unattended worker runs shell commands for hours. Allow by
    command name, add an extra check for commands that are dual-use (a file removal, a process kill, a database
    client), and fail closed when a command cannot be parsed (`skills/agent-hook-guard-pitfalls`). Own guidance:
    test the check against command substitution, backticks, redirections and chained commands, which splitting on
    separators alone does not see.
13. **Run it in a disposable environment.** The same reasoning as for any unattended agent: a throwaway machine or
    container, no credentials that matter, a network list as short as the task (`skills/agent-sandbox-egress-pitfalls`,
    `skills/unattended-agent-run-pitfalls`).
14. **Expect drift in the specification's meaning, not only in the code.** Own guidance: re-read the specification
    against the list at the halfway point; a list that was faithful at the start can have been quietly narrowed by
    a worker who found an entry hard and, unable to delete it, weakened its steps in spirit.
