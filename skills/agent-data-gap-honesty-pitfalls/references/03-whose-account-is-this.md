# agent-data-gap-honesty-pitfalls §3 — Whose account is this

> Part 3 of `skills/agent-data-gap-honesty-pitfalls`. Read it before the first read of a connected drive,
> mailbox, workspace or CRM that the user did not name. Source: the tenant-scope and single-CRM rules of a
> small-business plugin set (Apache-2.0), rewritten in our own words; points marked own guidance are ours. This is
> about which tenant a legitimate connector is signed into, not about whether a server is trustworthy
> (`skills/agent-mcp-trust-pitfalls`) and not about designing tenant isolation
> (`skills/multi-tenancy-isolation-models-pitfalls`).

The failure: a connector is attached to the session, the agent has no data source for the task, and it reads
whatever the attached store holds. The store belongs to a different company. The agent treats another
organisation's confidential files as the user's own history, and nothing in the connector says whose it is.

## 3.1 Confirm ownership before the first read
1. **A document store or a mailbox is the user's only once it is shown to be.** Compare the connected account's
   domain or display name with the business the user described, or use a file or folder the user named in this
   session.
2. **No business context yet, or a mismatch: stop and ask in one line**, naming the account that is connected
   ("the drive connected here looks like <account>; is it yours, or should I use an upload?"). Read nothing until
   the answer.
3. **Ownership checked once is not ownership for ever**: recheck when the connection changes during a session.
   Own guidance.

## 3.2 Search by name, never browse
1. **Every query to a document store carries the business name, the project name or the exact file name given.**
   Symptom: "recent files" and unscoped folder listings pull in unrelated material.
2. **Recent-files and folder listings are never a discovery path.** Ask for the name instead.

## 3.3 A missing source does not become a document store
1. **If the data connector the task needs is absent (no opportunity feed, no CRM, no ledger), the options are
   public web research where a public source exists, an upload, or a question to the user.** "Look in the drive
   for something similar" is not an option.

## 3.4 Discard what came from the wrong store
1. **Anything read from a mismatched store is dropped, not summarised.** If a read happened before the mismatch
   was noticed, say so, remove it from the working set and carry none of it into a deliverable.

## 3.5 One system of record
1. **A business has one CRM of record.** If two are connected, the user names one, the agent says which it read,
   and only that one feeds the pipeline totals and the lead pool. Two merged give duplicate contacts and a
   double-counted pipeline.
2. **Verify the organisation before any record contributes to an answer.** If the connected organisation's name
   does not match the business, stop and say so rather than reporting another company's pipeline.
3. **An authentication banner is not an outage.** Probe with one cheap read before declaring a system
   unavailable and falling back to a file.
4. **Check how the system stamps its records.** Many imports give every record the same creation time; a bulk
   import date is not the date a relationship started, so do not score age on it. Check whether the timestamps
   are suspiciously identical first.
5. **A system of record is not a replacement for mail or calendar.** A task that needs email context or open
   time still needs those connectors, whichever CRM is connected.
