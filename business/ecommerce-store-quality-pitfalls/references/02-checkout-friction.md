# ecommerce-store-quality-pitfalls §2 — Checkout friction

> Part 2 of `business/ecommerce-store-quality-pitfalls`. Read it when a cart or checkout is built or abandoned
> carts are studied.

A checkout is a form that takes money. Each field and each surprise gives the buyer a reason to leave.

## 2.1 No surprises
1. **Show shipping, fees and tax before the last step.** The same EU page says the full price including taxes and
   additional charges must be shown before purchase and that delivery costs appearing only at checkout are not
   allowed; this is for the EU, other markets differ, take advice. Symptom: abandonment peaks at the payment page. Check:
   walk the flow as a buyer in each market and write down the step where each cost first appears. Fix: an
   estimate in the cart, the exact figure no later than the delivery step.
2. **Say the delivery date or range** and what it depends on (stock, carrier, cut-off time), not just "fast".
3. **Make the total and the line items visible at every step**, with an easy way back to the cart.
4. **Reserve what is bought** (§1.3) and warn if an item sold out, before payment and not after.

## 2.2 Fewer reasons to stop
1. **Offer guest checkout.** A forced account is an abandonment cause; offer account creation after the order,
   with one click and the email already known.
2. **Ask only what the order needs.** Each field has a use: delivery, payment, contact. A phone number is
   optional unless the carrier needs it, and say why when you ask. Collection of personal data has its limits
   (`business/data-protection`).
3. **Make forms work with browser autofill and the right keyboard on mobile**, one column, labels above fields,
   inline validation that says what to fix (`business/ux-writing` §1 for the wording of errors).
4. **Do not clear the form on an error**, and keep the cart for a returning visitor.
5. **Make address entry tolerant.** Names, postal codes and addresses vary by country (`skills/international-input-pitfalls`);
   a validator that rejects real addresses loses real orders.
6. **Never add anything to the basket the buyer did not choose**, and never preselect paid extras. Besides losing
   trust, it is banned or restricted in many places; check the local rule with a qualified person. The EU consumer
   page read says paid extras need an active choice, a pre-ticked box is not consent, and such payments can be
   refunded; it also says traders generally cannot charge a fee for paying by card, with named exceptions, and that an
   offer to charge in the buyer's currency must disclose the markup over the central bank rate (Your Europe, pricing and payments).

## 2.3 Payment and delivery options
1. **Offer the payment methods your buyers use in each market**, and test each one end to end, with a refund.
2. **Show what is accepted before the buyer fills in anything.** A card icon row that omits the method they came
   with sends them away at the last step.
3. **Give a delivery choice that is real**: a method that is never available for that address should not be
   offered; an unavailable option should say why.
4. **Handle payment failure on purpose.** Symptom: "something went wrong" and an empty cart. Fix: a message that
   says whether the card was charged, how to retry, and keeps the order. Check: simulate decline, timeout and a
   closed window; a double-click must not charge twice.
5. **Send the confirmation at once**, with what was bought, the total, the delivery promise and how to reach you
   (§3.3).

## 2.4 Finding the real leak
1. **Look at the step-by-step drop-off before changing anything** (`skills/funnel-and-cohort-definition-pitfalls`), split by device,
   market and payment method. Symptom: a redesign of the page where nobody leaves.
2. **Watch real sessions and read support messages.** Numbers say where; people say why.
3. **Separate technical failure from decision.** An error rate at payment is a bug, not a conversion problem; log
   and alert on it (`skills/event-tracking-plan-pitfalls`).
4. **Retest after each change on a phone.** Most traffic is there and most layout faults too.
