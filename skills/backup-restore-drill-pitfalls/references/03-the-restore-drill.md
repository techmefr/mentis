# backup-restore-drill-pitfalls §3 — The restore drill

> Part 3 of `skills/backup-restore-drill-pitfalls`. Read it when a drill is planned, run or reviewed.
> Sources, read 2026-10-20: Azure Architecture Center, "Design a ransomware-resilient backup architecture by
> using Azure Backup" (CC BY 4.0), for the restore-drill, validation and clean-environment points;
> mercari/production-readiness-checklist, pre-production checklist (MIT), for the requirements that a recovery
> procedure be defined, tested, described in the on-call playbook and practised on a schedule. Sentences
> marked "own guidance" are ours.

1. **Run the drill, not a review of the procedure.** The checklist asks that recovery from backup be defined and
   tested, and, for the most critical level, practised on a schedule with the procedure in the on-call
   playbook. Own guidance: someone follows the written steps against a real backup and a real clock. Reading a
   document tests the document's grammar.
2. **Choose the scope of each drill.** Own guidance: a single table or file; one datastore; one service end to
   end; the loss of a whole account or region. Start small and increase; each drill states what it does not
   cover.
3. **Restore into a separate environment.** The Azure guide restores into a clean, isolated environment first.
   Own guidance: for a routine drill the same applies, with no connection to production data or traffic, no
   outbound mail or webhooks that could fire from restored data, and anonymisation where a copy of personal data
   leaves its normal controls (`business/data-protection` §3 point 5).
4. **Write the success criteria first.** Own guidance: the measured recovery time and recovery point meet the
   objectives of `references/01-objectives-and-design.md`, row counts and checksums match expectations, the
   application starts and a listed set of user journeys pass. Do not adjust the criteria after the run.
5. **Start the clock when the failure is declared and stop it when the service is usable.** Own guidance: the
   figure that matters includes finding the right backup, fetching access, waiting for data to copy, replaying
   the log, rebuilding the application and validating. Record each phase; the slowest one is the next thing to
   fix.
6. **Validate the data, not only the restore command's exit code.** The Azure guide validates the restored
   environment with functional testing and integrity checks before promoting it. Own guidance: compare counts and
   a sample of known records, run the database's own consistency check where one exists, and run the
   application's own smoke test against the restore.
7. **Restore with the people and access you would have on a bad day.** Own guidance: the person on call, with
   only the documented credentials, from a machine that is not the usual one. Symptom: the drill needed the one
   engineer who knows a flag. Fix: put it in the runbook.
8. **Test the point-in-time path separately.** Own guidance: choose a target moment inside the retention window,
   including one just before a known change, and confirm the data reflects that moment. A full restore proving
   good does not prove the log replay.
9. **Test restoring a copy from the isolated location.** The guide runs drills from both primary and secondary
   copies on a defined schedule. Own guidance: a copy never used for a restore is a copy of unknown quality;
   rotate which copy each drill uses.
10. **Break the procedure on purpose once.** Own guidance: after a clean drill, make the first choice fail (the
    latest point is bad, a key is missing, the second region must be used) and see whether the runbook says what
    to do. This is the game-day form (`skills/chaos-experiment` §1); have written abort criteria.
11. **Capture what the drill found.** Own guidance: the write-up lists measured recovery point and time against
    the objectives, steps that were wrong or missing, surprises, and fixes each with an owner and a date.
    Blameless: the finding is the procedure, not the person (`skills/blameless-incident-review-pitfalls`).
12. **Fix the runbook the same week.** Own guidance: every wrong step found goes into the runbook before the
    drill is closed (`skills/documentation-craft-pitfalls` §3 point 7); a finding left as a ticket is repeated
    at the next drill.
13. **Schedule the next drill and its trigger.** The checklist ties practice to a recurring interval for the
    most critical systems. Own guidance: set the interval from how fast the system changes and how bad a miss
    would be, and add triggers beyond the calendar: a new datastore, a major version upgrade, a change of
    backup tool, a change of provider, or a restructuring of access.
14. **Report the result in terms the owner uses.** Own guidance: "we recovered the orders data to within a stated
    loss in a stated time, against the agreed objectives; the invoice files were not covered" is a decision
    input; "backups OK" is not.
