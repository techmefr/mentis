# § 3 — Empty states: the screen someone sees first

> Section 3 of `business/ux-writing`. Read it when a list, table, search result or dashboard region can
> come back with nothing in it.

1. **An empty list is the new user's first impression**, and "No data" wastes it. Say what belongs here
   and how to add the first one. It is also the only screen where the product gets to explain itself
   with the reader's full attention, and the two sentences that do it are cheaper than any amount of
   onboarding built later.
2. **Distinguish "nothing yet" from "nothing matches"**: a filter returning nothing needs a way to
   clear the filter, not an invitation to create something. The two are visually identical and mean
   opposite things, so the wrong one is actively misleading: a reader with an active filter reads
   "create your first item" as their data being gone, and the support ticket that follows is about data
   loss.
3. **Distinguish both from "failed to load"** — showing an empty state when a request errored teaches
   the user their data is gone. This is the failure that costs most, because the reader acts on it: they
   re-enter records that already exist, or they escalate a data-loss incident that never happened.
4. **Say why it is empty when the reason is knowable, and only then.** "No results for *this term*
   with *these two filters*" tells the reader which of the three to change; "No results" makes them
   clear everything and start again. Where the reason genuinely is not knowable, do not invent one — a
   confidently wrong explanation is worse than none.
5. **The way out is the reader's next action, and it belongs in the empty state itself.** Create the
   first item, clear the filters, widen the date range, change the search. An empty state that describes
   the situation and offers nothing sends the reader hunting for the control that fixes it, usually in
   the part of the screen the empty state has replaced.
6. **A zero is not an empty state.** A dashboard tile showing 0 is a real measurement and reads as one;
   a tile with nothing to measure yet is a different message, and presenting it as 0 puts a false
   datapoint into whatever the reader is deciding (`business/data-analytics` §4.2).
7. **A permission-empty list is not an empty list.** A reader whose role scopes them out of every row
   sees the same screen as a reader whose account is genuinely new, and "add your first item" is then an
   instruction they cannot follow. Where the scoping is not itself confidential, say it; where it is,
   the honest form says the list is empty for this account and names who to ask.
8. **Never fill an empty screen with fake content.** Sample rows, illustrative charts and placeholder
   records are read as real: someone reconciles a figure against a demo number, or edits a row that does
   not exist. If an example is genuinely useful, it is labelled as an example and cannot be acted on.
9. **The empty state is written when the list is built, not afterwards.** Its text is the part that
   reaches production untouched, because the developer's fixture data is never empty and the state is
   never seen during the work — which is exactly why "No data" survives to the first real user.
10. **A partially empty screen still owes each region a message.** In an assembled screen, one empty
    region and three populated ones is the case a single page-level empty state cannot express, and the
    silent version is a section the reader does not notice is missing (`business/interface-design`
    §3.7).
11. **Never write an empty state that only makes sense on the first visit.** The same string is read by
    someone who deleted their last item, and "welcome — get started by adding an item" then reads as the
    product having forgotten them. A wording that works in both cases is the requirement, or the two
    cases are two strings.
