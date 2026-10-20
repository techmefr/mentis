# ad-measurement-pitfalls §2 — What counts as a conversion

Most arguments about ad numbers are really arguments about what is being counted and who keeps the count.
Settle those before any tool or report. Platform mechanics below come from one repository's account of them
and were not checked on the platforms' own pages (`re-read before relying`).

## 2.1 One business conversion, one system of record
1. **Write the business conversion in one sentence**: what happened, to whom, how confirmed. A click on a
   submit button is not a confirmed submission, and starting checkout is not a purchase; counting an attempt
   teaches the bidder and the report the wrong lesson (`skills/event-tracking-plan-pitfalls` §1 holds the
   rule for the event itself).
2. **Name the system that holds the count**: normally the back end or the CRM, where the sale or the lead is
   a record. Platform numbers explain where those conversions came from; they do not get to redefine how many
   there were.
3. **When a platform and the system of record disagree about how many, the system of record is the count.**
   Reconcile monthly and write down the cause of each gap (§3).
4. **Ask whether the conversion that matters sits further down.** A form fill that never becomes a customer
   can be the wrong conversion. Decide which stage the business actually pays for.

## 2.2 Two claimants, one sale
1. **Every platform reports a conversion under its own window and its own rules, so the same sale can appear in
   several reports.** One sale claimed by two platforms is one conversion with two claimants, not two
   conversions.
2. **Never sum platform figures to get a total.** De-duplicate against the system of record, show each
   platform's claim beside it, and state the gap as over-claiming plus view-through plus untracked, with the
   best allocation you can defend and how sure you are.
3. **Read direction, not match.** If every source says one channel rose and another fell this quarter, that
   direction is more trustworthy than any single figure.

## 2.3 Outcomes behind a form fill
1. **Bidding systems optimise towards what you call a conversion.** Fed raw form fills, they find cheap form
   fills, and the cost per lead can improve while the pipeline does not. This is the usual explanation of
   "plenty of leads, no customers".
2. **Send the CRM outcome back where the platform supports it**, as a lead stage or as a value on the lead, so
   the system learns from outcomes. The click identifier has to be stored with the lead when it arrives,
   because by the time a deal closes the browser session is long gone.
3. **There are volume and time-window conditions on whether a platform can use a late-stage outcome**: a
   platform with a short click window will never credit a deal that closes after it, and a stage with few
   events cannot be optimised on. Those conditions vary by platform and change; read the platform's current
   page for the one in use (`re-read before relying`) and do not carry a number from here.
4. **If outcomes cannot be sent back, report them anyway.** Import or join them as observation only, so the
   report shows which campaigns produced customers rather than forms. Until then, have a person read lead
   quality (titles, companies, whether sales calls the lead a lead) next to the cost per lead.
5. **A conversion action that counts something cheap and sits among the ones to optimise on trains the bidder
   to buy it.** Keep soft signals as observation only, and count a lead once per person rather than once per
   submission where a person can submit more than once.

## 2.4 Double counts by design
1. **Two senders for one action count it twice.** A native tag and an imported analytics event both set to be
   optimised on; a tag in two containers or hard-coded and in a container; a browser sender and a server
   sender with no shared identifier. Inventory every sender before adding one, including those that leave
   nothing in the page (a server integration, an import job, a connector), because a second sender is how
   double counting starts.
2. **Where both browser and server send the same event, they need one shared event identifier and the same
   event name**, and the platforms' keys for removing the duplicate differ and change. Read each platform's
   current documentation for the one in use (`re-read before relying`; the Meta documentation was not read for
   this block). A difference as small as case or a separator in an identifier can defeat de-duplication while
   both senders look correctly set up.
3. **A page that can be reloaded or bookmarked counts again unless guarded.** A confirmation page trigger needs
   a guard against refreshes and direct visits.
4. **Bots and test submissions fire real conversions.** If conversions are well above real leads in the inbox
   or CRM, look at spam, test entries and delivery failures before blaming the tag, and exclude tests from the
   count.

## 2.5 Refunds (ecommerce)
Platforms differ on whether a refunded order stops counting: one source reports that one platform supports
adjusting or retracting a conversion, analytics has a refund event, and another platform documents no refund
mechanism, so a sent purchase stays counted. If true, a store that adjusts on one side will show structurally
different return figures on the two sides, and a store that adjusts nowhere overstates every platform by about
its return rate. **The primary sources for this point were not read.** Treat "are refunds adjusted anywhere?"
as an audit question to put to the owner, and do not state the platform mechanics as fact without reading each
platform's current page (`re-read before relying`).
