# money-arithmetic-and-rounding-pitfalls §1 — Representation and arithmetic

> Part 1 of `skills/money-arithmetic-and-rounding-pitfalls`. Read it when an amount is stored, computed, split,
> converted or sent. Sourced from payments-platform (`pkg/money/money.go` and
> `docs/adr/ADR-018-money-as-integer-minor-units.md`, commit `576d6da`), TigerBeetle
> (`docs/coding/data-modeling.md`, commit `0450c32`), the pgledger README (commit `54ccb62`) and the ISO 4217
> list one from SIX (`list-one.xml`, published 2026-09-17), all read 2026-10-16. payments-platform is a
> reference implementation its README says has not processed real money: its choices are one author's design.
> Sentences marked "own guidance" are ours.

1. **Store integer minor units plus an explicit currency, or an exact decimal; never a binary float.** The
   decision record's reasons: a float cannot represent a value like 0.10, sums drift, and comparisons then need
   an epsilon, which is a statement of how much money you are willing to lose. Amount and currency are written
   together and stay adjacent (in the source's storage, an integer column and a three-letter currency column).
   Both representations are exact; pick one per system and do not mix them at boundaries.
2. **The exponent comes from the currency; it is not always two.** Zero-decimal and three-decimal currencies
   exist, and the ISO list read today shows JPY with 0 minor-unit digits, USD and EUR with 2, KWD with 3 and CLF
   with 4. A schema that says "cents" is wrong for them, and the error shows up in display and in 100x or 1000x
   amount mistakes. TigerBeetle's page gives the same examples for the asset scale (USD 2, JPY 0, KWD 3).
3. **Read the exponent from the maintained list; do not copy a table.** The ISO 4217 list is published by SIX as
   maintenance agency, and the copy read today carries a publication date of 2026-09-17; lists like this are
   amended over time, so re-read the current one when adding a currency or reviewing the data, and keep the
   source and date next to whatever you load. Own guidance: load it as data you can refresh, not as a literal in
   code. The same file marks some entries as funds and some as having no minor unit (written "N.A." rather than
   0); the file does not define that marker, and our reading is "no minor-unit concept", so decide per such entry
   whether you support it at all. An unlisted or unsupported currency is a validation error at the boundary, never
   a guessed exponent: the source's money package deliberately supports a curated subset for exactly that
   reason. (The same package keeps a default of two decimals for formatting an unknown currency in a log line;
   own guidance: that fallback must never be reachable from a money path.)
4. **Choose the scale once, with future precision in mind.** TigerBeetle: accounts and transfers are immutable,
   so changing a ledger's asset scale means a new ledger and copying every account over. Think about whether you
   will ever need finer fractions before fixing the scale; if so, use the finer scale from the start. Map the
   smallest useful unit to 1 and treat every amount as a multiple of it.
5. **Calculate on integers; rescale only to display or to talk to another system.** The sources agree: scale up
   or down at the edges (rendering, an external interface), never inside the arithmetic. Display is where a wrong
   exponent is least tested (the decision record's example is a yen amount shown with two decimals), so test
   formatting for a zero-, a two- and a three-decimal currency.
6. **Reject invalid amounts at the door, and take direction from the accounts.** pgledger's transfer amount must
   be a positive finite number: zero, negative, null, not-a-number and infinities are all refused, and a rejected
   transfer changes nothing; the direction of a movement comes from the from and to accounts, not the sign. The
   payments-platform design instead allows negative values only for ledger credit entries and rejects non-positive
   amounts on payment, capture and refund requests. These are two designs for one aim: decide which you use, and
   state it where the amount type is defined.
7. **Split by largest-remainder allocation, so the parts sum exactly to the whole.** Dividing ten units three
   ways and rounding each share loses or creates a unit. The source's method: give each part its integer share,
   then hand the leftover units one at a time to the parts with the largest remainders, ties going to the lowest
   index so the result is deterministic and reproducible on both sides of a reconciliation. Reject an empty list,
   a negative ratio and a zero total. Test it as a property over random amounts, part counts and currencies
   including zero- and three-decimal ones, asserting the parts sum to the whole.
8. **Multiply by a rate in integers, and name the rounding mode once.** The source's package multiplies by a rate
   expressed in basis points using integer arithmetic and rounds half away from zero; fees, interchange and
   spreads quoted in basis points then reproduce exactly on both sides of a reconciliation. The mode is that
   author's choice, not a rule. Own guidance, consistent with `business/fintech-compliance` part 2: write the
   rounding mode as a named policy, apply it at one named point, and use the same function everywhere a rate
   meets an amount, because two modes for one computation is how a ledger stops balancing. Quantity
   multiplication by an integer needs no rounding.
9. **The legally required rounding is not covered here.** Which mode, at which point (per line or per total) and
   to which unit is required for tax or invoice amounts depends on the jurisdiction and the date. It was not
   read and is not stated; route it to an accountant or tax adviser and record their answer as the policy of
   rule 8.
10. **Mixing currencies is an error, not a conversion.** Add, subtract and compare check the currencies first and
    return an error (not a crash, not a silent conversion, which would invent a rate). The source's package has
    no exchange rate on purpose: a conversion has a rate source, a spread and an audit trail and belongs in the
    business layer, not in the arithmetic type.
11. **Model an exchange as two paired transfers through a liquidity account per currency.** pgledger: each account
    holds one currency; an exchange touches four accounts, two of them system accounts, so debits and credits
    still net to zero within each currency. Create both transfers in one atomic call. The rate itself is stored
    as business data with its source and time (own guidance).
12. **Overflow is an error.** The source uses checked addition, subtraction and multiplication that return an
    overflow error, and the API refuses amounts above a configured maximum long before the integer limit.
    Own guidance: a hostile or buggy amount should fail validation, not wrap.
13. **Keep the wire format integer-or-string, never a float.** The decision record's wire shape is integer minor
    units plus a currency code, because JSON numbers become binary floats in some parsers (it also notes the safe
    integer limit of such parsers). It rejects a decimal string on the grounds that parsers disagree about forms
    such as "10.5", while noting that several well-known payment APIs use decimal strings. Either is workable if
    the contract fixes one form and rejects the other; a float number is not. Also expect integrators to send
    major units by mistake, so the contract should refuse a non-integer with an error that names minor units.
14. **Sub-unit precision needs a separate type with an explicit boundary.** Interest accrual, per-unit prices
    below one minor unit and intermediate exchange values do not fit in minor units. The decision record's
    suggested direction is a separate higher-precision type for such computations with an explicit, tested
    rounding boundary into the money type, not a change to the money type. Own guidance: that boundary is where
    the rounding policy of rule 8 is applied.
