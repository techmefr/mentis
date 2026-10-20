# price-change-and-billing-pitfalls §6 — Showing prices

A price shown to a buyer is the first thing that can mislead them. This section covers the total and the
reference price. It is method, not legal advice: the legal reading of a given page belongs to the person who owns
legal.

## 6.1 The total comes first
Show the price the buyer will pay, with the charges that cannot be avoided and the taxes as they will appear,
from the first price displayed, not at the last step of checkout. If the total cannot be computed in advance
(it depends on usage or on a country not yet known), say what it depends on and show the part that is known.
Tax display by country is `skills/vat-handling-in-software-pitfalls`. Whether a particular jurisdiction
requires a total price display, and for which products, is `method only, re-read before relying`; §6.5 records what
two regulators' texts say, as facts, and the legal reading stays with the person who owns legal.

## 6.2 A reduced price needs a reference price
"Was / now", "reduced", "X percent off" and "save" each compare the current price with another price. Before the
comparison is displayed, write: which price is the reference, since when it applied, and where that is recorded.
Keep a price history (date, plan, price, currency, who changed it) as a plain table kept up to date, so that the
reference can be shown on request. A reference that was never charged, or was charged for a short time before a
sale, is the pattern to look for in review.

## 6.3 The EU rule on announced reductions
Text read 2026-10-20 on the legislation.gov.uk copy of Directive 2019/2161 (Article 2 inserts Article 6a into
Directive 98/6/EC), a mirror of the EU text. The Official Journal text on EUR-Lex and data.europa.eu returned an
empty body (HTTP 202) to every fetch tried, so it was **not read** and the Omnibus-amended provisions beyond Article
6a were not read either. Paraphrase, near the text:
1. An announcement of a price reduction must indicate the prior price the trader applied for a determined period
   before the reduction.
2. The prior price is the lowest price the trader applied during a period not shorter than 30 days before the
   reduction.
3. Member states may set different rules for goods liable to deteriorate or expire rapidly.
4. Where a product has been on the market for less than 30 days, member states may provide a shorter period.
5. Member states may provide that, when a reduction is progressively increased, the prior price is the price
   without the reduction before the first application of the reduction.

Not read, so not stated: whether the rule reaches a software subscription or a digital service, the national laws
that transpose it, any exemption, the Commission's guidance, any court decision. A reading of those belongs to the
person who owns legal. The text above is a directive: the obligation sits in each member state's law.

## 6.4 Method for any reduction
1. Keep the price history (§6.2).
2. Before a reduction is announced, take the lowest price applied over the period your jurisdiction's rule uses
   (found by the person who owns legal), and compare.
3. Name the cases that need their own decision: new plans, plans that change price often, progressive reductions,
   renewals.
4. Store the comparison with the announcement, so a complaint can be answered from a record.

## 6.5 What two regulators' texts say (facts read 2026-10-20, own words, not a legal reading)
Sources: the UK CMA guidance "Unfair commercial practices: price transparency" (CMA209, final text, 142k
characters read in part: paragraphs 3.3 to 3.5, 3.25 to 3.26, 4.3 to 4.5, 4.16 to 4.19, 5.30 to 5.36), the CMA open letter on
urgency and price reduction claims (29 March 2023, with its examples of non-compliance 9 and 10), the US FTC
Guides Against Deceptive Pricing (16 CFR Part 233, sections 233.1 and 233.4 of that part) and the FTC Rule on Unfair or Deceptive Fees
(16 CFR Part 464), the last two on the eCFR. CMA documents carry the Open Government Licence; the eCFR text is a
US government work. Each is a text to re-read before a page relies on it.
1. **A mandatory charge belongs in the headline price.** The CMA text says a charge shown apart from the price, or
   labelled an "extra", is still mandatory if the buyer must pay it to get the advertised product, even if it could be
   avoided by buying something else. Its list of mandatory charges includes taxes, fees however named (booking,
   processing, platform) and joining fees paid on top of a first regular payment. Symptom: the total grows at a later
   step. Check: add every charge a buyer cannot avoid and compare with the first price shown. Fix: show the
   inclusive figure from the start; keep only genuinely optional items apart.
2. **When the total depends on choices, say so at every step.** Where a total cannot reasonably be calculated yet,
   the CMA text says the information needed to calculate it should appear in each invitation to purchase, not once on
   a front page, and the total must be shown as soon as it becomes calculable. It lists a full price list or a
   realistic "from" price as ways to cope, and says an indicative price should be realistic, meaningful and
   attainable.
3. **Recurring plans.** For a rolling plan the CMA text treats the total price as what is paid each period, inclusive
   of mandatory charges. For a minimum-term plan it names two ways: the cumulative price over the minimum term, or
   the per-period total beside a prominent statement of the commitment length. A fixed-term plan paid in
   instalments is a different case: the CMA text says the whole price is stated. The same text states that
   subscription-contract provisions of the UK Act add further duties and are outside that guidance.
4. **Monthly versus annual.** The CMA text says that if paying annually is cheaper, the trader risks misleading unless
   the options are made comparable, for example by giving each option's total or the difference in cost. This
   supports §4.2 item 1. Discounts applied later, such as codes or negotiated prices, are not barred by the total
   price duty.
5. **A former price must be a real price.** The FTC guides say a reduction claim from a former price is sound only
   if that price was genuinely offered to the public, openly and in good faith, for a reasonably substantial
   period in the regular course of business, and describe an inflated price set up to make a cut look large as
   fictitious. They add that a former price can be genuine without many sales, but should not be called a selling
   price unless substantial sales occurred. The CMA letter calls a higher comparison price misleading in two
   example situations: it was charged only briefly before a long period at the lower price (its example 9), and it
   sold in very small numbers (its example 10), and says the higher price must be a genuine and realistic
   selling price the business can demonstrate. Symptom: a "was" price nobody remembers. Check: the §6.2 history
   for the period and the units sold. Fix: drop the comparison or use a real reference.
6. **Offers conditional on a purchase.** The FTC guides say such offers (free, two-for-one, percent off) can
   mislead if the regular price, quantity or quality of the required item changes, and that material conditions
   should be stated at the outset.
7. **The FTC fees rule has a stated scope.** Its text defines the covered goods and services as live-event tickets
   and short-term lodging, requires the total price (maximum a buyer must pay including mandatory fees, with
   government charges, shipping and optional add-ons allowed to be left out of that figure) to be shown more
   prominently than other price information, and bars misrepresenting a covered fee. Whether a given page falls
   inside that scope is a question for legal. The effective date and any later change were not read.
8. **Not stated by these texts, so not stated here**: any penalty, any statute number beyond what is named above,
   how either regulator treats a particular software plan, any national law of an EU state.
