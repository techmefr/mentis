# price-change-and-billing-pitfalls §5 — Billing mechanics

A customer-facing promise ("you only pay the difference") is a claim about what a billing system will do. The
facts below were stated on one vendor's documentation page (read 2026-10-20) and are written vendor-neutral.
Other systems differ: check yours, and treat each line as a question to ask it. `re-read before relying`.

## 5.1 Proration of a mid-cycle change
1. **A change to a charge billed in advance yields two lines**: a credit for the unused time on the old price and
   a debit for the remaining time on the new one. Illustration (own numbers): a monthly plan at 30 changes to a
   plan at 60 exactly halfway through the period; the credit is 15, the debit is 30, the net is 15 more.
2. **The net is not always settled at once.** A negative result is not refunded by default and a positive one is
   not necessarily charged immediately. Find out which happens in your system and tell the customer.
3. **The amount is computed when the change is made**, from the start and end of the current period. It can differ
   between a preview made earlier and the change applied later. Preview with a fixed date and apply the change
   with the same date.
4. **Discounts**: the credit and the debit are computed on the discounted price, and the proration lines are not
   discounted a second time. If the discount changes in the same operation as the change of plan, the new
   discount is the one used.

## 5.2 Unpaid invoices
If a customer changes plan while the invoice for the current period is unpaid, the system may credit unused time
on the dearer plan although that time was never paid. Decide the rule (switch proration off for that case, bill
the new plan separately, void the old invoice) and write it down. Two of the ways of switching it off can bill the
customer twice if the old invoice is paid later: void it.

## 5.3 Usage billing is not prorated
Proration applies to charges billed before the period. Usage charges are billed after the fact and are not
prorated. A plan that mixes a fixed fee and usage has two behaviours on the same invoice: explain both in the
customer's words.

## 5.4 Turning proration off
Where it is switched off per request, it stays on for every other request, and it does not stop recurring or
full-period items from being created. Do not promise "no prorations" to a customer after turning it off for one
operation.

## 5.5 Credit rules differ between modes
Two credit-calculation modes of the same vendor gave different results on a plan that was never paid for: one
credited the amount of the current price, the other credited the last amount actually invoiced. If your system has
modes, pick one on purpose and test the never-paid case.

## 5.6 Before any customer-facing example
Run the example through a preview of the actual invoice, with a fixed date. Never publish a worked example
computed by hand. Usage metering and alerts before a threshold are a billing-vendor reference topic, not part of
this block; vendor parameter names and product recommendations are left out on purpose.
