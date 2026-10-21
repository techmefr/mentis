# inventory-stock-app-pitfalls §3 — Replenishment demand method

> Part 3 of `skills/inventory-stock-app-pitfalls`. Read it when a tool or an agent estimates how fast an item
> sells, how long stock lasts and how much to reorder. Source: the inventory-planner gotchas of a small-business
> plugin set (Apache-2.0, read 2026-10-20), rewritten in our own words; points marked own guidance are ours. A
> method note, not a forecasting model: no formula constant, window length or cover target is given, because those
> are set per business. Accounting and write-down questions are the accountant's (`references/origin.md`).

The central error: **sales are not demand**. Sales are what was sold while the item was on the shelf; demand is
what customers wanted. Anything that treats a gap in sales as a gap in wanting understates demand exactly where
stock is short.

## 3.1 Velocity
1. **A day with no stock is not a day with no demand.** Compute the rate as units sold divided by the days the
   item was actually available, not by calendar days. Symptom: a best seller that keeps running out is rated
   slow, so the next order is smaller and it runs out sooner (a loop that feeds itself). Check: the number of
   days at zero stock inside the window. Fix: say how many days were out of stock and plan on the in-stock rate.
2. **Compare a short and a long window and look at the gap.** A short rate far above the long one is either a
   real trend or one big order; far below is either cooling or a stockout in the week. Open the orders before
   believing either. Do not choose one window for every purpose.
3. **Take a single bulk order out of the rate used to size a buy.** Show the rate with and without it and say
   which one the quantity rests on. A one-off job should not become a month of stock.
4. **Name which rate drives which number.** A pessimistic rate for when stock runs out and a sober rate for how
   much to buy can differ; label each so the owner can override one without the other. Own guidance: never use
   one word for both.
5. **Items without enough history are reported as such.** Do not scale a week of sales up to a year. Seasonal
   factors are not computed from a history that does not contain the season; ask the owner how much heavier the
   season is and label the figure as the owner's.
6. **Returns and promotions distort the window.** Net returns against the period they were sold in; mark
   promotion periods or ask, because a discounted fortnight is not a baseline.

## 3.2 Stock and orders
1. **A stock figure carries an as-of date.** A count from two weeks ago divided by the current rate yields a
   run-out date that may already have passed. Either net out the sales since the count or ask for a fresh count
   on the fast items, and say which was done.
2. **Subtract what is already on order.** A buy sized without the inbound quantity doubles the order, often right
   after a stockout scare. If the inbound quantity is unknown, say that the result assumes nothing is coming.
3. **A stored reorder point is a hint from the past.** An item with no sales in the window does not get a
   reorder because an old reorder point says so; report the stale point and the cash tied up in the stock.
4. **Zero sales is not "about to run out".** A division by a zero rate gives an error or an absurd cover. Send
   such items to a slow-mover list with the value held in them. The exception is a season the owner named: put it
   on a dated watch list with the decision date, and never infer a season from a quiet month.
5. **Work at the level where stock is held.** A product that sells in one size and not another looks healthy in
   aggregate while the good size runs out. Compute per variant.
6. **A vendor minimum is on the whole order, not on each line.** Check the total first; when it falls short, give
   the owner the extra units, the extra money and the extra days of stock, and never round up silently.

## 3.3 Reporting
1. **Give units and money together.** A buy list with no cost column is not a decision an owner can make; cost
   each line, subtotal each vendor and state the total before asking for approval.
2. **Show the work per line**: the rate and its window, stock on hand and on order, days of cover, lead time,
   the quantity and what it rests on. A bare quantity gets rebuilt by hand every time.
3. **Report a vendor substitution** (different part, different pack) and the effect on cover if the owner
   declines it; it is the owner's decision, not a shipping detail.
4. **Data gaps are named.** Which items had tracking switched off, which counts are old, which inbound numbers are
   unknown: see `skills/agent-data-gap-honesty-pitfalls` §1.
