# saas-metric-definition-pitfalls §2 — Unit economics, engagement and growth

> Part 2 of `skills/saas-metric-definition-pitfalls`. Read it when a per-customer, per-user or growth figure is
> defined or checked. Formulas are the source's (nimrodfisher); points marked own guidance are ours.

## 2.1 LTV, CAC and payback
1. **LTV is ARPU times gross margin, divided by monthly churn rate.** ARPU is average revenue per user per
   month, gross margin is revenue minus cost of goods sold over revenue, and churn is a monthly decimal. The
   source reads the result as the average total gross profit expected over a customer's lifetime, so it is a
   profit figure, not a revenue figure.
2. **State which churn went into LTV.** The source allows monthly logo or revenue churn in the same formula;
   they give different LTVs for the same business (see part 1, churn). Write the choice next to the number.
3. **Keep the periods consistent** (own guidance, a consequence of the formula): a monthly ARPU needs a monthly
   churn. Mixing an annual figure with a monthly one is an error of twelve before any judgement is applied.
4. **CAC is total sales and marketing spend divided by new customers acquired**, usually over the same period
   (quarter or month). A fully loaded CAC includes the salaries, tools and overhead attributable to sales and
   marketing. Say whether the quoted CAC is fully loaded; the two differ by exactly the overhead.
5. **Match the spend period to the acquisition period** (source: same period). Spend in one month and
   customers acquired in the next quarter is a different ratio; if a lag is deliberate, write it down (own
   guidance on the lag).
6. **LTV to CAC is the ratio of the two** and inherits every choice above. Quote the LTV and CAC inputs, not
   only the ratio.
7. **Payback period is CAC divided by ARPU times gross margin**, in months: how long a new customer takes to
   repay its acquisition cost.
8. **No interpretation bands are carried.** The source attaches bands to the ratio and payback targets; none is
   sourced, so they are dropped. The team writes its own threshold and the reason before the number is read.

## 2.2 Active users and engagement
1. **"Active" is defined by the product and must be specified**: the source's examples are a login, any event
   or a core action. DAU and MAU mean nothing until one is chosen, and a count under "any event" can be many
   times a count under "core action".
2. **Use one definition on both sides of the ratio.** The source describes DAU to MAU as the proportion of
   monthly actives who return daily; a daily count under one definition over a monthly count under another is
   not that proportion (own guidance, a consequence).
3. **Name the session metric.** Session length (average time per session), sessions per user per week
   (frequency) and depth (pages or actions per session) answer different questions; a bare "engagement" is
   none of them.
4. **No stickiness benchmark is carried.** The source's "strong" and "typical" cut-offs are unsourced.

## 2.3 Growth rates
1. **Month-over-month growth** is the current month minus the prior month, over the prior month. Week-over-week
   and year-over-year use the same formula over a different period; the source notes that the year-over-year
   comparison removes seasonality effects.
2. **Say which period** is compared. A month-over-month figure and a year-over-year figure for the same metric
   are both correct and answer different questions.
3. **The quick ratio is new plus expansion MRR, over contraction plus churned MRR.** It measures how much of
   the gross additions is offset by losses. The source's cut-off for "high efficiency" is unsourced and
   dropped; read the ratio against the team's own history.
