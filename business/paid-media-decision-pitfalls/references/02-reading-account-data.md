# paid-media-decision-pitfalls §2 — Reading account data without false conclusions

Ad reports are partial by design and plausible by accident. Default views leave data out without saying so,
names suggest contents they do not have, and a small account produces numbers that look like findings. Most
wrong conclusions come from not knowing this, not from poor reasoning. The mechanics below come from a
practitioner repository's account of one search platform's reporting; they are the kind of fact to confirm
against the platform's current help pages (`re-read before relying`), and none was checked here.

## 2.1 A search-terms report is a sample
1. **Platforms may withhold queries searched by too few people**, so the terms you can see are a skewed
   subset of what triggered the ads. Before any sentence about what a campaign "buys", write the ratio:
   disclosed clicks (the sum of clicks in the report) against total clicks for the same window, and the
   difference as withheld.
2. **Pull the report unfiltered first.** Filtering to rows with clicks hides every term that only had
   impressions, and a low row limit hides more.
3. **Nothing recovers the withheld queries.** Analytics or a CRM joined on the click identifier can show what
   each visit did afterwards, never what was typed.
4. **No negative keyword without the report.** Without it you have no evidence of what is matching. With it,
   check each candidate before excluding: would this negative also block a query that converts or one that
   starts a later conversion? Keep brand-adjacent and research-stage terms for a human decision. Never write a
   list of candidate negatives from imagination.

## 2.2 "Conversions" is several things in one column
1. **The headline conversion column counts the actions marked as the ones to optimise on**, plus others a
   campaign's own goal setting pulls in; a second column counts everything. Check each campaign's goal as well
   as each action's setting. One campaign's figure can mix a page-view proxy, a trial and a booked demo.
2. **Segment by conversion action before calling anything a lead or a demo.** Read each action's counting
   rule (every occurrence or one per click) and its click window on the same pass.
3. **A model that assigns credit by data is soft on small volume.** With few conversions, do not read much
   into one campaign's share (`business/ad-measurement-pitfalls` §4.2).
4. **Names describe intentions, not contents.** A group called "competitor" may hold informational terms; a
   campaign named for one theme may target another. Read the keyword list and the terms.
5. **One ad group can send traffic to several pages**, and stale ads linger in rotation. Before a conclusion
   about a landing page, check which destinations are serving and how the clicks split, and open the page; a
   static fetch misses what loads through scripts, so absence there is not evidence.
6. **Identical campaign names are often experiment arms.** An expired arm can keep an enabled status while
   serving nothing. Check the experiment type and serving status before believing a duplicate exists.

## 2.3 Dates, lag and the last few days
1. **Conversions are booked to the click date.** A conversion recorded today can appear dated a week earlier,
   so "we got one today" and "the pull says the 11th" can both be true. Say "clicked on the 11th".
2. **The most recent days undercount** wherever conversion lag exists. Read them as incomplete and never call
   a trend from them alone.
3. **Recent ranges grow after you read them.** If you quote a figure, quote the date you pulled it, because
   it will be larger later without anything having improved.

## 2.4 The window is not the picture
1. **Establish how long something has run before quoting efficiency.** A thirty-day pull on a campaign that
   has run for months is a slice; quote recent and lifetime when they diverge.
2. **Never pool across a configuration change.** If bids, keywords, budget, ads or targeting changed inside
   the window, the period is several experiments averaged. A change to bids alone invalidates cost and volume
   comparisons but leaves intent and audience questions readable.
3. **Do not judge a bid strategy the platform marks as still learning.** Fixing a verified break (tracking
   down, wrong URL) still comes first; restructuring a learning campaign as a reflex often costs more than the
   dip it was meant to cure.
4. **History is short.** The change log of the platform covers a limited period with detail and a longer one
   without it (confirm the periods). Past that, a shift may have no recoverable explanation, and the right
   sentence is that it cannot be explained, not a guess.
5. **Other actors change the account**: client staff, automated rules, scripts, agents. Report which client
   made a change and not a guess about who or why; some editors do not appear in the log at all, so a missing
   change is not proof nobody made one. A repeating weekday and time under one user is a scheduled job.

## 2.5 Brand against non-brand
1. **Split brand and non-brand before judging either.** People who already know the name convert cheaply, and
   that is existing demand unless a holdout (`skills/experiment-design-pitfalls`) shows the ad created it.
2. **A cheap brand cost per result is not evidence about prospecting.** Brand terms inside a general campaign
   prop up its figures and hide the non-brand cost.
3. **Report the blended figure at business level and set targets on non-brand**, with brand held to its own
   target.

## 2.6 What a finding is called
Know which of three states each claim is in: **verified** (pulled live this session, unfiltered, reconciled
to a total), **inferred** (reasoned from verified data, could be wrong), **stale** (from a document, an
earlier session or the client, with its date). When a client or owner shows a finding is wrong, concede it
plainly; a string of retractions costs more trust than the first error did.
