# spend-guard-fail-closed §1 — A budget guard that closes by default

> Part 1 of `skills/spend-guard-fail-closed`. Read it when any spend limit is designed, built or reviewed.
> Sources, read 2026-10-19: a cloud provider's budgets documentation
> (https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html) and an AI
> vendor's API error reference (https://platform.claude.com/docs/en/api/errors). Sentences marked "own
> guidance" are ours, and several rest on one gateway project's documentation, not independently verified.

1. **The limit is a gate in the call path, evaluated before the request is sent.** Own guidance. A check after
   the response only measures what was already spent. The cloud provider's page says the same in its own
   terms: a notification can arrive after usage has already passed the threshold, and costs keep moving after
   the alert, because billing lags use.
2. **Billing data is late: a limit built only on it is a smoke alarm.** The provider states its budget
   figures update a few times a day, with hours between updates. Own guidance: for a loop that spends in
   minutes, enforce on your own counter of calls and tokens in the path (a cap you control) and use the
   provider's figures to reconcile, not to stop.
3. **Fail closed: an unreadable or stale reading means "unknown", and unknown blocks.** Own guidance. If the
   usage lookup fails, times out or is older than a freshness limit you chose, refuse or ask a person. Never
   map a missing number to zero. Give the reading an age and refuse past it.
4. **New or unclassified options start excluded.** Own guidance, from the gateway's strict free-only mode: a
   model, provider or plan the guard has no entry for is treated as paid until someone classifies it. The
   allow-list grows by decision, not by discovery.
5. **"Free" is a dated catalogue fact, not headroom.** Own guidance. A listed free tier says nothing about
   what is left of it, and the plan may bill silently past its allowance. Allow a candidate only if
   (a) the provider's own published terms say overage cannot be billed, with the page and read date recorded;
   (b) a current usage reading exists; and (c) the reading shows headroom. Terms change, so the record is
   dated and re-read on a schedule (`skills/source-freshness`).
6. **Verify per credential, not per pool.** Own guidance. If several accounts or keys can serve a candidate,
   check each; restrict the usable set to those that passed. A pool that is "mostly fine" still bills on the
   one account that is not. Hand the dispatcher only the verified subset so it cannot pick another.
7. **Invalidate the reading when a credential fails.** Own guidance: after any failure on a credential,
   drop its cached usage so the next decision re-reads instead of trusting a stale "safe".
8. **Scope limits to the thing that spends.** A per-agent, per-key or per-task cap contains a runaway loop; a
   single organisation-wide cap only stops everyone together. The vendor describes limits you set at
   organisation and workspace level; add a tighter one where an autonomous loop runs.
9. **Know how the wall presents itself.** The vendor reports a user-set spend limit as a plain invalid-request
   error and a tier-level cap as the rate-limit status without a wait hint that keeps failing. An agent that
   retries these wastes its budget and time. Route both to the budget path in
   `skills/failure-classification-before-retry` §1 point 4 and stop.
10. **Report why a candidate was excluded, in distinct reasons.** Own guidance. At least separate: not
    classified, not free, no hard-stop guarantee, allowance exhausted (resolves itself), reading missing or
    stale (the lookup is broken), and no credential to check. "Exhausted" and "lookup broken" look identical
    from outside when the candidate just vanishes, and they need different people.
11. **Say where the guard is blind.** Own guidance: a second exclusion rule that removes candidates before
    the reporting list is built (for example a terms-of-service filter) hides its own reasons. Write such
    gaps down in the block's docs; an honest known gap is better than an implied full coverage.
12. **A cost figure on a dashboard is an estimate unless it comes from the invoice.** Usage times a price
    table is a model: the table can be stale or missing a model (priced at zero), and a subscription or free
    tier has no per-request price at all, so its figure is "what it would have cost at list price". Label the
    figure with its basis, and never use an estimate as the stopping rule. Own guidance, supported by the
    provider's own statement that budget figures lag actual billing.
13. **Decide who is told at each stage, in advance.** An alert at a fraction of the limit goes to the owner of
    the spend, the block at the limit goes to the owner and the requester, and a guard that cannot read its
    own data goes to the person who maintains it. The provider's page offers notifications to email and
    messaging topics and optional automatic actions at a threshold, such as applying a restrictive policy;
    an automatic action is a design decision with a named approver, not a default.
14. **Test the closed path.** Remove the usage reading, mark a credential as unknown, make the lookup slow, and
    assert that the request is refused with a reason. A guard tested only on the happy path has not been
    tested.
