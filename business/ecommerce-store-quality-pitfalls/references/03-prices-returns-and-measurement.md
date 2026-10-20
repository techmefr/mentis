# ecommerce-store-quality-pitfalls §3 — Prices, returns and measurement

> Part 3 of `business/ecommerce-store-quality-pitfalls`. Read it when prices, policies or conversion figures are
> set or read.

## 3.1 Price display
1. **Show prices the way the buyer's market expects, and say which it is.** Consumers in some markets expect a
   price with tax included, business buyers often expect it excluded. Symptom: the total is higher than the listing
   and the buyer feels deceived. Fix: a stated treatment per market and customer type, and the same treatment
   from listing to total. The rules differ by country and change; take advice. Computation is
   `skills/vat-handling-in-software-pitfalls`.
2. **Show the final price in the buyer's currency, and the rounding rule.** A converted price that moves every
   day confuses; state when it is fixed.
3. **A reference price ("was") must be a real price that was charged.** Symptom: a permanent "was" price. Fix:
   follow the local rule on prior price statements, and keep a log of the prices you charged; ask a qualified
   person what the rule is.
4. **A discount shows the amount and its conditions**, including exclusions and end date, next to the offer, not
   in a link that nobody reads (`business/price-change-and-billing-pitfalls`).
5. **A code that fails says why**: expired, minimum not met, not combinable.

## 3.2 Returns and delivery promises
1. **State the return window, who pays and the refund timing in one place, and link to it from the product page,
   the cart and the confirmation.** Symptom: three pages, three windows. Check: compare the text on each page.
   Whether a statutory right of withdrawal applies to a sale depends on the country and the goods; this is not
   legal advice, and the policy must not give the buyer less than the law does.
2. **Make the process easy to start**: order number lookup, a reason picker that feeds your product team, a label
   when you pay. A hard return process raises disputes with the card issuer.
3. **Measure returns by product, variant and reason.** Symptom: a good-selling shoe at a high return rate. Fix:
   size guidance, better images, a corrected description; the cause is usually in the listing (§1).
4. **Refund by the method of payment, within the time you stated**, and tell the buyer when it is done.
5. **Keep a clear promise on delivery and a plan when it fails**: the buyer hears of a delay from you first, with a
   new date and a choice.

## 3.3 Confirmation and after
1. **The confirmation repeats the order, the total, the address, the delivery promise and the return terms.** It
   is the first document in a dispute.
2. **Send status messages at the points a buyer wonders**: shipped, delayed, delivered. Keep marketing out of
   transactional messages and respect consent for the rest (`business/email-deliverability-and-sender-requirements-pitfalls`
   covers the sender side).
3. **Keep the invoice and the order record as your tax and accounting need**; retention differs by country.

## 3.4 Measurement
1. **Test over whole weekly cycles.** Symptom: a variant declared a winner after three weekdays. Fix: at least two
   full weeks where buying differs by weekday and by pay-day, and the plan written before it starts
   (`skills/experiment-design-pitfalls`).
2. **Judge on a margin-aware outcome.** Conversion up with returns up is not a win. Include returns, discounts and
   shipping paid.
3. **Compare like with like on traffic.** A promotion, an email or a stock change in the period changes who comes.
   Segment new and returning, device and channel.
4. **Count orders from one source of truth**, the order system, and reconcile with the analytics tool, which
   under-counts when consent is declined (`skills/event-tracking-plan-pitfalls` is the plan; the gap is expected, the
   size is measured, not assumed).
5. **Abandoned-cart reminders follow the consent and marketing rules of the market** and stop once the buyer
   orders or opts out (`business/email-campaign-measurement-and-testing-pitfalls`).
6. **Do not quote a benchmark conversion rate.** Rates differ by sector, price and traffic mix; compare with your
   own history, and re-read any external figure at its date before relying on it.
