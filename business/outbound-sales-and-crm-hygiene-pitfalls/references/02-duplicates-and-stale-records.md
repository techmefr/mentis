# outbound-sales-and-crm-hygiene-pitfalls §2 — Duplicates and stale records

Duplicates split a history across two records; stale records pad a total. Both make the next report wrong and the
next message embarrassing (two reps, one person).

## 2.1 Matching before merging
1. **Pick the match keys and write them down**: a verified email, a company domain, a normalised company name.
   Symptom: two people at one company merged because they share a surname. Check: a name alone never merges.
   Fix: keep a "possible duplicate" state for human review.
2. **Normalise before comparing**: case, trailing spaces, legal suffixes, a domain written with and without a
   prefix. Compare on the normalised value; keep the original.
3. **Separate people from accounts.** A person who moves company is one person with two roles, not two people.
   Merging them loses the job-change signal.

## 2.2 Survivorship
1. **Decide which record survives and which field wins before the first merge.** Common rule: the system of
   record wins; for a contested field, the most recently verified value wins. Write the rule.
2. **Keep the losing record's activity and opt-out status** on the survivor. Symptom: a merge silently clears a
   suppression flag and the person is contacted again.
3. **Log every merge** (which records, which rule, who or what ran it) so one can be undone.

## 2.3 Stale records
1. **Define stale by last real touch**, not last system edit: a bulk update touches every record. State the window
   and who chose it.
2. **Stale records leave the pipeline total and the active lists.** Archive, do not delete, so the history stays
   and the opt-out stays.
3. **Re-verify an address before mailing a dormant contact.** A bounce on a stale list damages the sending
   reputation (deliverability: `business/email-deliverability-and-sender-requirements-pitfalls`).

## 2.4 A repeatable audit
1. **Run the same checks each period and compare**: duplicates found, records without an owner, records without
   a source, records missing a stage-required field, stale share of the pipeline.
2. **State each check as a query someone else can rerun.** A one-off cleanup decays; a repeated one shows the
   trend.
