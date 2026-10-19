# troubleshooting-kb-article-pitfalls §1 — Evidence and the gate

The failure this section prevents is a help centre of pages for failures nobody hits, one page per ticket, and
pages that exist only because a message or a flow is bad.

## 1.1 Write only from failure evidence
1. **Take at least one reported source and one unreported source.** Reported: tickets, issues, community
   threads. Unreported: error telemetry, docs search logs. Tickets alone show what people complain about;
   telemetry alone shows what breaks; the gap is where readers give up without writing in.
2. **Each source over-represents something.** Tickets: paying customers and failures worth complaining about.
   Issue trackers: vocal technical users. Docs search: people who already trust the docs. Telemetry: everything,
   including what nobody reports. Sales and solutions engineers' private lists: evaluation-time blockers.
   Reviews of past incidents: rare but expensive failures.
3. **No source at all means stop.** Say so and start the capture habit in §4.1 first.
4. **Audiences differ in where the signal is.** For self-serve users the loudest failures are public; for
   contract customers they sit in private tickets and may never reach the public tracker, so mining public
   sources alone under-serves the accounts that pay. Check whether a fix may be published at all.

## 1.2 Cluster
1. **One failure is one cluster and one page.** Ten tickets about one cause are not ten pages.
2. **Merge clusters that are one failure worded two ways; split a cluster whose members have different
   causes**, since one string can come from two places.
3. **Records with no error text still matter.** Read them for failures with symptoms and no code; they become
   how-to pages.
4. **By hand it is a pass over the top fifty records**: strip the variable parts (paths, identifiers, numbers),
   tally, keep one raw example per cluster.
5. **Stop when the next cluster has only a handful of occurrences**; the source's view is that ten good entries
   beat sixty stubs, since every stub costs a maintenance pass at every release. That is its opinion, not a
   measured threshold.

## 1.3 A cluster that starts after a release is a regression
1. **Report it, do not write a page.** A page would document a bug into permanence.

## 1.4 Gate each cluster: document or fix
1. **A page is legitimate while a fix is scheduled**, and never the permanent answer for a failure the product
   could stop emitting; documenting around a defect makes it permanent, and the page outlives the memory of why
   it exists.
2. **Route the cluster away from a page when**: the error text does not say what to do (rewrite the message;
   a page cannot be pasted into a terminal), the fix is "edit three files in order" (a product change or a
   command that does it), the cause is account state such as quota, plan or suspension (a product surface or a
   support macro), the same failure class recurs across several postmortems (a scheduled product fix, the page
   being the interim measure), or the fix needs credentials the reader lacks (an escalation path, documented as
   such).
3. **When a page is the interim measure, say so in the queue and name the owner of the real fix.**
4. **Deciding not to document a failure is a legitimate result.** Some failures deserve no page.
5. **A support macro and a public entry must not disagree.** When one exists the other is a link to it or a
   superset of it.

## 1.5 Rank
1. **A default order from the source**: frequent and reproducible clusters first, since they take an afternoon
   and empty the queue fastest; first-use blockers (anything on the path from sign-up to first success) next;
   rare and expensive after; volatile ones last.
2. **That order starves the rare, expensive failure.** Promote it by hand when it hits a contract customer in
   production or appears in an incident review.
3. **Agree the queue with the owner of the docs before writing**, since a queue built from the wrong clusters
   wastes the whole pass.

## 1.6 Verify
Check that every queued cluster has a record of its sources (one reported, one unreported) and a decision
from §1.4. A queue with no decision per cluster has not been gated.
