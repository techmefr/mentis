# observability-instrumentation — origin and source stamps

> Provenance of `skills/observability-instrumentation`. Read it when a rule has to be traced back to
> its source or checked for freshness (`skills/source-freshness`), never to apply a rule.

Rewrite of the `observability-and-instrumentation` skill from a market generalist dev skill
catalogue; the "define the questions before instrumenting" rule, the RED/USE metrics, the
anti-cardinality rule and symptom-based alerting are taken as-is, rewritten to the mentis template.

**Sectioned and deepened 2026-09-08.** The four inline sections moved to one file each under
`references/` and the router became a table of triggers, with §1 marked read-every-time because it is
what makes the other three judgeable. No section was added. Every section and point number was
preserved: `skills/api-design` §2 cites §1 as the source of usage data, `skills/security-hardening` §5
cites §2 as what to check after a hostile-value replay, and that block's own OWASP coverage check names
this block as the owner of A09.

**What the depth adds.** The original was 511 rules words — the second-thinnest block counted in the
depth table — and it stated the right rules with no failure attached to any of them. That is a
particular problem here, because instrumentation is written by someone who is not the person who will
read it, at a moment that is not the incident: nothing about a log line's uselessness is visible until
three in the morning, and by then it cannot be changed. The additions that were real absences rather
than elaborations:

- **§1**: why the order matters — instrumentation written first records what the function did, which is
  what you already know during an incident, and not which requests were affected or when it started;
  that the questions have to be written down or the discipline lasts one change; that a question has to
  be answerable *end to end*, and "how many users are affected" is usually the dimension the
  cardinality rules keep out of the metric, so the answer has to be planned into logs or traces; the
  "did the fix work" question, the one nobody states and the on-call needs last; that instrumentation
  can stop earning its place, and a dashboard nobody opened in three incidents is cost with no reader;
  retention as part of the decision rather than something discovered from the bill; and that the output
  has to be looked at once with real traffic, which catches the misspelled label and the always-zero
  metric that both pass code review.
- **§2**: that free text is queryable by substring only, so a saved query is silently invalidated by
  the next wording edit; that the correlation ID has to be *propagated* — the half that gets missed —
  including across a queue, where the chain is broken by design; that a log is a copy which leaves its
  source's access controls behind, which is why redaction is not tidiness; that a value interpolated
  into the message makes every occurrence a distinct string and defeats grouping and counting; that a
  level used loosely teaches the on-call to ignore it; that one failure logged at every level on the
  way up produces several entries and loses the stack from the one that gets read; that a log line has
  to say what happened to the *work* — retried, dropped, partially applied; that logging in a hot loop
  becomes the performance problem it was added to investigate, precisely under load; and that logging
  has to survive its own failure without taking the request with it.
- **§3**: that cardinality is *multiplicative*, which is why it surprises people, and that the failure
  arrives as an ingestion limit, a timing-out query or an invoice rather than a warning; the pairs that
  look equivalent where one member is unbounded — route template versus raw path, status code versus
  status message, error class versus error string; that the real answer to "but I need the user" is
  logs and traces rather than a label, joined by the correlation ID; that an average hides the tail
  entirely, so the reader concludes the system is healthy while a share of users cannot use it; that a
  metric's name and unit are permanent because every dashboard and threshold is written against them;
  that a counter resets on deploy and is read as a drop; that an error counter incremented only on the
  remembered branch reports zero during an outage, which is worse than having none; and that sampling
  is a trade whoever reads the number has to know about.
- **§4**: why symptoms and not causes — causes are plural and symptoms are few, so a page for high CPU
  fires on the harmless case and misses the outage nobody predicted; that every alert names the action
  or a link to it, because the people who wrote it are not the ones being woken; that an unactionable
  alert teaches a rota to dismiss notifications, after which the real one is dismissed too; owner and
  route, since a group with no named responsibility is indistinguishable from nobody; thresholds chosen
  from the observed distribution rather than a round number; **duration as part of the condition**,
  which is what separates a page from a flap; that a low-volume service needs a minimum-volume clause
  or a percentage threshold pages on a single failure at night; **alerting on absence** — a job that
  did not run, a queue that stopped being consumed — which is the class a symptom-based set misses
  unless written deliberately; that one incident should produce one page; and that reviewing what fired
  and what was ignored is the only thing keeping a set of alerts trustworthy.

Router plus sections: 511 → 3,048.

**Status.** The source is unchanged and still stands. The depth is ours, written from what an on-call
cannot do with instrumentation that was written for the code rather than for the incident. The block
still has no real incident behind it in this repo, and `devops-conventions` continues to own the
platform side.
