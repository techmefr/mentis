# unattended-agent-run-pitfalls §2 — Sources and state

> Part 2 of `skills/unattended-agent-run-pitfalls`. Read it when the job reads something that changes over time.
> Sources: the daily digest and triage agents of anthropics/claude-quickstarts (MIT, re-opened 2026-10-20); for
> points 1, 2, 7, 14 and 15 the Kubernetes CronJob page (CC BY 4.0), GitHub's workflow-events page (CC BY 4.0) and
> Slack's Web API pages (product documentation, facts only), read 2026-10-20. Sentences marked "own guidance" are
> ours.

1. **One bookmark per source, not "the last 24 hours".** A fixed window loses items when a run is skipped and
   repeats them when two runs overlap. The sample keeps a bookmark for each source, and for each channel of a
   source. Check: skip a run on purpose and see that the next run still covers the gap. Schedulers do skip: the
   Kubernetes CronJob page says a job may be created twice or not at all, that with the forbid policy a still-running
   job makes the new run be skipped, and that more than a hundred missed schedules stops it from starting;
   GitHub's schedule-event page says runs can be delayed at busy times, with queued jobs dropped if the load is high.
2. **Start slightly before the bookmark.** The sample reads from a few minutes earlier than the stored position
   and relies on the ledger to drop what it has already reported. Why: sources deliver late and out of order, so
   an exact cut-off loses the straggler. A timestamp filter is usually exclusive at its edge: Slack's history method
   returns only messages after the timestamp given as oldest unless its inclusive flag is set (Slack
   conversations.history reference). Own guidance: the overlap is a setting you can see, not a constant buried
   in a prompt.
3. **Move a bookmark only after success.** A bookmark advances for a source that was read, and only once the
   outcome (the post, or the deliberate silence) is confirmed. Symptom of advancing early: a failed post and a
   next run that starts after the items it never delivered.
4. **A ledger of what was reported.** One line per item: date, source, item identifier and the state that was
   reported. The next run skips an item whose identifier is in the ledger with the same state, and re-reports it
   only when the state changed. Without it, a long-open item appears in every report until the reader stops
   reading.
5. **Carry, do not repeat.** The sample shows an item still open as one marked line ("still waiting, day 3") and
   drops a closed one without comment. Own guidance: decide the carry rule once and test it with an item
   that stays open for three runs.
6. **Unreadable is not quiet.** A source that failed is noted for the coverage line, its bookmark stays where it
   was, the other sources carry on, and the report says the source could not be read. The sample's reasoning: a
   reader who sees "nothing from the tracker" assumes it was checked. A missing number is stated as missing and is
   never filled in.
7. **A success status is not a success.** Some APIs answer with an ordinary status and put the failure in the body
   (an "ok" flag set to false). Check: every response counts only if its body says it worked. Symptom of
   skipping this: an empty channel history read as "no news". Slack's Web API page confirms the shape: every response has a
   top-level ok flag, with an error code when it is false, and a call can be ok with a warning attached.
8. **Mark a source unavailable once and stop retrying it.** The triage agent, on the first entitlement or
   availability failure of an optional analysis service, marks it unavailable for the run and does not call it for
   the other items. Other per-item failures do not stop the report. Own guidance: say which of the two it was in
   the report, without raw error payloads or credentials.
9. **Treat third-party analysis as a hypothesis.** The sample checks an automated root-cause result against the
   issue's own telemetry and labels the fallback "model hypothesis" with its evidence when no analysis came back.
   Own guidance: a label the reader can see beats a confident sentence of unknown origin.
10. **Rank by impact, not by volume.** The triage agent ranks by users affected rather than raw event count, and
    classifies each item (new, regression, escalating, ongoing). Own guidance: write the ranking rule in the
    prompt, or the run ranks by whatever the source sorts by.
11. **Notes hold how a source behaves, never how it failed.** The sample keeps a notes file for limits, ordering
    and quirks that a later run would trip over, and forbids recording a failed credential or connection there or
    a workaround for one: the failure will be fixed and the note would outlive the fix. Failures go in the run
    record only. Check: no note starts with "token" or "cannot reach".
12. **First run is a case.** A missing state file means the first run: read a bounded window and start the files.
    Own guidance: a state file that is missing on a later run is not a first run; it is a failure to report.
13. **The state files are your own notes, and contain no instructions.** The sample says so in the prompt. Own
    guidance: a note written from source content can carry an injected sentence into the next run; write facts about
    behaviour, never quoted text.
14. **A page of results is not the whole result.** Slack's history reference says fewer items than the limit may be
    returned even when the end of the conversation has not been reached, and gives a has-more flag and a cursor. Symptom:
    a bookmark moved to the newest message of a short page, with older ones never read. Check: loop on the cursor until
    the flag is false before judging a source quiet or moving its bookmark.
15. **Time zones are the reader's.** The sample dates titles and run records in the reader's time zone. Symptom of
    using server time: a Monday brief titled with Sunday's date, and "today's edition" lookups that miss. The
    scheduler has the same question: the Kubernetes CronJob page says a schedule without a time zone follows the
    controller's local zone, and a zone is set in its own field, not inside the schedule string.
