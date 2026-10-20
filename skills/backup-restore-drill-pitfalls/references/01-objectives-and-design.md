# backup-restore-drill-pitfalls §1 — Objectives and design

> Part 1 of `skills/backup-restore-drill-pitfalls`. Read it when a backup is designed or reviewed.
> Sources, read 2026-10-20: mercari/production-readiness-checklist, "Automatic Datastore Backups" and the
> pre-production checklist's data-storage section (MIT); Azure Architecture Center, "Design a ransomware-resilient
> backup architecture by using Azure Backup" (CC BY 4.0). Sentences marked "own guidance" are ours.

1. **List what must be recoverable, store by store.** Own guidance: databases, object storage, queues that hold
   work, search indexes that cannot be rebuilt, secrets and keys, infrastructure state and configuration, and
   the encryption keys that make the rest readable. Symptom: a restored database that cannot be decrypted, or an
   application whose uploads are gone. Fix: one row per store with its owner and how it is protected.
2. **Say what each backup is for.** The checklist lists the events a backup answers: accidental deletion,
   corrupt data, a bad schema migration, lost credentials, ransomware, a mistake in a manual operation,
   environmental disaster, power or hardware failure and sabotage. Own guidance: a replica protects against
   hardware loss and copies an accidental delete in seconds; only a point-in-time copy answers the delete. Match
   the mechanism to the event.
3. **Set a recovery point objective and a recovery time objective, and have the owner choose them.** Own
   guidance: the first is how much recent data may be lost, the second how long the service may be down while
   restoring. Both are product decisions with a cost, not a technical default. Symptom: "daily backup" with no
   statement of acceptable loss. Fix: write both per data class and have the owner sign.
4. **Back up on a schedule and before risky events.** The notes name both triggers: a schedule, and before
   anything that may damage the datastore such as schema changes, manual operations and releases. Own guidance:
   the pre-event copy is the one you restore after a bad migration, because the nightly one lost the day
   (`skills/devops-conventions` §6 point 13).
5. **Keep the log or journal if you need a point in time.** Own guidance: a periodic full copy gives a recovery
   point at the time of the copy; recovering to a chosen moment needs a continuous stream of changes kept
   alongside it. Check that the stream is archived, complete and retained as long as the oldest copy you rely
   on.
6. **Design retention against how late damage is discovered.** The Azure guide calls for retention long enough
   to recover from an attack found days or weeks after it began, with short-term and longer-term layers. Own
   guidance: a corruption noticed after the oldest copy expired is unrecoverable; set the window from how late
   you realistically notice, and from any legal retention, then check deletion rules do not contradict it
   (`business/data-protection` §3 point 2).
7. **State what a restore does to data that was deleted on purpose.** Own guidance: restoring an old copy
   resurrects records a person asked to erase. Keep a record of erasures to replay after a restore, and say so in
   the procedure (`skills/dsar-handling-pitfalls`).
8. **Cover the application, not only the data.** Own guidance: a database restore without the matching code
   version, configuration, secrets, DNS and certificates is half a recovery. List the rebuild path: the
   infrastructure as code, the images, the order of start-up.
9. **Write down the dependencies of recovery.** Own guidance: the restore needs a login, a network path, a key
   store, a registry and a person; if those live in the system that has failed, the restore cannot start.
   Include a copy of the runbook outside that system.
10. **Define who decides and who acts.** Own guidance: a named person declares a recovery, picks the recovery
    point, and approves cutting traffic over; the procedure names the roles and a way to reach them
    (`skills/incident-comms-pitfalls`).
11. **Know the cost of waiting and of choosing wrongly.** Own guidance: restoring to the latest point loses the
    least data and may restore the corruption; an older point is safer and loses more. The procedure says how to
    choose and how to try a second point if the first fails validation.
12. **Treat a replica or failover as a different tool.** Own guidance: high availability keeps the service up
    through a node failure; it is not a backup, and it copies mistakes. Record both and test both.
