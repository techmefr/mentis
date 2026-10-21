# dispatch-parallel §2 — File ownership and finding merge

> Section 2 of `skills/dispatch-parallel`. Read it when work is split among several writers, when several reviewers
> will cover one change, or when their reports have to be merged. Source, read 2026-10-20: the agent-teams plugin of
> wshobson/agents (MIT, root licence); its tool names and team lifecycle are not carried over. Sentences marked "own
> guidance" are ours. 🟡: not yet run on a real fan-out.

## 2.1 Ownership of files among writers
1. **Give every file exactly one owner before anything starts.** The source's cardinal rule: no file is assigned to
   two implementers. Write the ownership map into each worker's brief as a list of paths or directories, and
   say that anything outside the list is read-only for that worker.
2. **Pick the cut that matches the code's own seams.** By directory where folders are cleanly organised, by module
   where the code is organised by feature, by layer where it is layered. Own guidance: the cut that produces the
   fewest imports across the boundary is the right one; a map with many cross-imports is a sign to run the
   work in sequence (`SKILL.md` Guardrails).
3. **Map the files first, then cluster, then assign.** The source's order: list every file the feature will create
   or change, group them by proximity, by who imports whom and by layer, give each cluster to one worker, and
   check that no file is in two clusters. A file nobody listed is a file two workers will both edit.
4. **A shared file has one owner and the others send requests.** Preferred, in the source's order: split the file so
   the shared concern has its own file; failing that, one worker owns it and the others send change requests that
   the owner applies one at a time; as a last resort, let one worker finish and the next take over. Never let two
   edit it at once. Typical shared files: the service registration list, the shared exception type, the routes
   table, the types file.
5. **Agree the boundaries in writing before work begins.** The shared types, function signatures, request and
   response shapes and event names are written first, in a file the lead owns and the workers only read. Symptom
   of skipping this: every worker passes its own tests against its own idea of the other side, and the join fails.
6. **Tests and fixtures are files too.** Own guidance: give the test directory to one worker or to the same worker
   as the code it covers; two workers who both extend one shared fixture file is the commonest collision.
7. **Verify ownership afterwards.** Own guidance: after each worker returns, compare the changed paths with its
   map (`git status --short`, as in `SKILL.md` step 5); a path outside the map is an escape to deal with before merge.
8. **Keep the group small.** The source starts with the smallest team that covers the dimensions and says each extra
   member adds coordination cost; overlapping workers produce duplicate findings. Own guidance: if two roles
   keep needing the same files, they are one role.

## 2.2 Several reviewers on one change
9. **One dimension per reviewer.** Security, performance, architecture, testing, accessibility: each reviewer takes one
   and says so in its report. The source's picks by change type (a database migration: performance and
   architecture; an authentication change: security and tests) are examples to adapt, not a rule.
10. **Use one fixed finding shape.** Location, dimension, what was found, impact, fix, and the evidence. Own guidance:
    add "what I did not check" so a clean report is distinguishable from a shallow one.
11. **A reviewer reports no findings plainly when there are none.** Padding a report to look useful is the failure
    this prevents (own guidance, in the spirit of the source's honest-reporting rule).
12. **Merge findings by location and by issue.** The source's rules: the same place and the same issue become one
    finding that credits every reviewer; the same place with a different issue stays separate and is tagged as
    sharing a location; the same issue in different places stays separate with a cross-reference; conflicting
    recommendations are both kept, each attributed.
13. **When severities conflict, keep the higher.** The source takes the higher rating of the merged findings. Own
    guidance: record the lower one and who gave it, so the choice can be reviewed.
14. **Calibrate severity on impact and likelihood together,** with a few fixed floors the team writes down, such as
    "a flaw exploitable by an outside user is at least high". The source keeps such floors; the levels and examples
    in it are its own and not carried over.
15. **Keep attribution in the merged report** (`SKILL.md` step 8): a merged finding still says which reviewers raised
    it, so a reader can see agreement without it being counted as proof (`multi-agent-design-pitfalls` §2).

## 2.3 Messages among workers
16. **Status goes in the shared task record, not in free-form messages.** The source forbids structured status
    messages and uses task updates instead; direct messages are for a question to one worker, and a broadcast is
    for something that changes everyone's work.
17. **Address a worker by the name it was started with.** If a name had to be changed to avoid a collision, use the
    changed name everywhere. Own guidance: a message to an alias that no longer resolves is the "enqueued is not
    acknowledged" case (`SKILL.md`, Supervising).
18. **A worker starts with no memory of the conversation.** The source's troubleshooting note: workers need the
    context in their first prompt. Put the goal, the ownership map, the contract file and the report shape there.
