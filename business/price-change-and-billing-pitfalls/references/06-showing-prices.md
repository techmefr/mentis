# price-change-and-billing-pitfalls §6 — Showing prices

A price shown to a buyer is the first thing that can mislead them. This section covers the total and the
reference price. It is method, not legal advice: the legal reading of a given page belongs to the person who owns
legal.

## 6.1 The total comes first
Show the price the buyer will pay, with the charges that cannot be avoided and the taxes as they will appear,
from the first price displayed, not at the last step of checkout. If the total cannot be computed in advance
(it depends on usage or on a country not yet known), say what it depends on and show the part that is known.
Tax display by country is `skills/vat-handling-in-software-pitfalls`. Whether a particular jurisdiction
requires a total price display, and for which products, is `method only, re-read before relying`; no rule of that
kind is stated here because none was read in this session.

## 6.2 A reduced price needs a reference price
"Was / now", "reduced", "X percent off" and "save" each compare the current price with another price. Before the
comparison is displayed, write: which price is the reference, since when it applied, and where that is recorded.
Keep a price history (date, plan, price, currency, who changed it) as a plain table kept up to date, so that the
reference can be shown on request. A reference that was never charged, or was charged for a short time before a
sale, is the pattern to look for in review.

## 6.3 The EU rule on announced reductions
Text read 2026-10-20 on the legislation.gov.uk copy of Directive 2019/2161 (Article 2 inserts Article 6a into
Directive 98/6/EC), a mirror of the EU text; EUR-Lex returned an empty page twice. Paraphrase, near the text:
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

## 6.5 Other jurisdictions
Rules on total price display and on drip pricing exist in other places (the United States, the United Kingdom).
None was read in this session: leave them to the person who owns legal, and re-read their texts before a page for
that market relies on them.
