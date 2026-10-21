# unattended-agent-run-pitfalls §3 — Verify and post

> Part 3 of `skills/unattended-agent-run-pitfalls`. Read it when the job is about to write to the outside world.
> Sources: the daily digest agent of anthropics/claude-quickstarts (MIT, re-opened 2026-10-20); for points 5 and 12
> the Kubernetes CronJob page (CC BY 4.0), GitHub's workflow-events page (CC BY 4.0) and Slack's search reference
> (product documentation, facts only), read 2026-10-20. Sentences marked "own guidance" are ours.

1. **The world moved while you read.** A run takes minutes; an item read at the start may be resolved by the time
   the report is written. The sample re-checks the live source of every item it will report, just before posting:
   resolved since, drop it; changed, fix the line; cannot confirm, drop it and list it as cut.
2. **Assert it or drop it.** Never hedge an item's status ("probably still open"). The sample's argument: one
   stale "still waiting on you" costs the reader's trust more than ten missing items. Own guidance: a report line
   is either confirmed within this run or absent.
3. **Copy links from the source's own link field.** A permalink or an html address returned by the API, never one
   assembled by hand from an identifier. Symptom of hand-built links: a clean-looking report whose links 404 or
   point at the wrong thing.
4. **Silence is allowed, and it is a decision.** If every source was read and there is nothing to report, the
   report says so in one line, or, when the rules allow silence, posts nothing and records a deliberate quiet day.
   Check: a quiet run and a failed run look different in the run record (§3.8).
5. **One post, found by its title.** Before posting, look in the destination for today's edition by its title and
   do not post again if it is there. Own guidance: use the destination's own history call, not a search
   permission the job does not hold; the sample notes that a bot token cannot search, and Slack's search method lists
   only a user-token scope. This makes a re-run after a crash safe, which matters because the Kubernetes CronJob page
   itself says a job can be started twice and tells you to write jobs that are idempotent.
6. **Write "posting" before you post.** The run record gets a status first, the post follows, and the status is
   updated from the result. States used by the sample: posting, posted, maybe posted, held. If the result is
   unclear, "maybe posted" and nothing else in the state changes; if the destination refuses (not a member,
   bad credential, channel missing), "held", with the report text kept in the record.
7. **Bookkeeping comes after the outcome.** Only once the post is confirmed, or a deliberate silence chosen:
   update the run record, add one ledger line per reported item, move the bookmark of each source that was read.
   Never move a bookmark of a source that failed, nor any bookmark when the post failed.
8. **Write the run record on every run, even silent ones.** What was read, what failed, what was posted, what was
   cut with a one-word reason each, and any choice the run made alone. This is the only trace a person has of a
   job that nobody watched, and the input for the next run's notes.
9. **A dry run when the state store is read-only.** The sample's rule: if it cannot write state, it posts
   nothing and puts the report in its final message. Use it deliberately: the first real run of a new job is a
   dry run, and a person reads the output before any post.
10. **Test the bad days, not the good one.** Own guidance: before trusting the job, run it with each source
    unreadable in turn, with the rules unreadable, with the destination refusing, with an item that resolves
    between read and post, and twice on the same day. Each has an expected record and an expected post (or
    none).
11. **Do not answer replies.** Own guidance: a reader's reply in the destination may suggest a rule change; the run
    adds it to the proposals file for the reader to accept, and never edits the rules or reacts in the channel.
12. **A run that never starts leaves no record.** The scheduler is part of the job's failure surface: GitHub's page says
    scheduled workflows run only on the default branch, can be dropped under load, and are disabled automatically in a
    public repository after sixty days without repository activity; a Kubernetes CronJob does not start after more than
    a hundred missed schedules. Own guidance: something outside the job, which expects a run record by a stated time,
    reports its absence; the job cannot report that it did not run.
13. **Pin the version a schedule runs.** Own guidance: a scheduled job refers to a specific version of the agent
    definition, so an edit made for a test cannot change tomorrow's run without someone re-pinning it.
