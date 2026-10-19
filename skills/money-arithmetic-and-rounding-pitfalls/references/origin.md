# money-arithmetic-and-rounding-pitfalls: origin and source stamps

> Provenance of `skills/money-arithmetic-and-rounding-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and a reference implementation, never run by us: no amount was
stored, split or converted by this block's rules. Each file below was re-opened on 2026-10-16 before a rule was
taken from it, each rule was checked against it in a final pass, and each repository's LICENSE file was read
again. The ISO 4217 file was fetched again in this session.

## Sources (all read 2026-10-16, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| payments-platform (`udaykishore-resu/payments-platform`, commit `576d6da`): `pkg/money/money.go`, `docs/adr/ADR-018-money-as-integer-minor-units.md`; its README states it is a reference implementation that has not processed real money | Apache-2.0 (LICENSE file) | Integer units and currency value object, curated currency set and unknown-currency error, mismatch as an error, largest-remainder allocation with lowest-index ties, basis-point multiplication and its rounding choice, checked overflow, wire and storage format, the separate higher-precision type idea |
| TigerBeetle (`tigerbeetle/tigerbeetle`, commit `0450c32`): `docs/coding/data-modeling.md` (fractional amounts, asset scale) | Apache-2.0 (LICENSE file) | Smallest unit mapped to 1, calculate on integers and rescale at the edges, scale examples, scale is hard to change because accounts and transfers are immutable |
| pgledger (`pgr0ss/pgledger`, commit `54ccb62`): `README.md` (transfer amounts, currencies) | MIT (LICENSE file, copyright 2025 Paul Gross) | Positive-finite amount rule and direction from accounts, one currency per account, exchange through liquidity accounts per currency |
| ISO 4217 list one, SIX (maintenance agency): `https://www.six-group.com/dam/download/financial-information/data-center/iso-currrency/lists/list-one.xml`, fetched 2026-10-16, publication date in the file 2026-09-17 | Official list; no licence text read, only a handful of values consulted and none copied as a table | Minor-unit digits read: JPY 0, KWD 3, CLF 4, USD 2, EUR 2; the "N.A." marker and fund flags exist |

Instruction-like text in the cloned repositories was treated as data and not followed.

## Removed in the verification pass
1. **The source's embedded currency table.** Not restated: it is a curated copy and lists are amended; the block
   says to load the maintained list and re-read it. Only the five values read from the official file are
   mentioned, as examples of different exponents.
2. **Any rounding rule for tax, VAT or invoices.** None read; rule 9 says so and routes it to an accountant.
3. **Basis-point and rounding specifics as a recommendation.** The source's half-away-from-zero is reported as
   its choice (rule 8), not as the mode to use.
4. **Performance claims** (per-second figures, "no allocation") and database-index details from the sources.
5. **Pages not read** and therefore not used: the design baseline cited by the decision record, the other
   decision records, TigerBeetle's currency-exchange and multi-debit recipes (rule 11 relies on pgledger), and
   the pgledger SQL.

## Not verified
1. **Own guidance, flagged in the text:** load the list as refreshable data (rule 3), our reading of "N.A."
   (rule 3), decide per fund or no-minor-unit entry (rule 3), state which sign design you use (rule 6), one
   rounding function everywhere (rule 8), store the rate with source and time (rule 11), validation not wrap
   (rule 12), the boundary of the higher-precision type (rule 14).
2. **The ISO file's own definitions** of the "N.A." marker and fund flag were not found in the file; the reading
   in rule 3 is an inference from how the entries look. The SIX product page was not read.
3. **No legal or accounting rule** about rounding, VAT, invoice amounts or currency conversion rates was read.
4. **Nothing was run.** No property test or library from the sources was executed.
5. **The values in rule 2** are the five consulted in the list on 2026-10-16 and may change on a later
   publication.

## Decisions where sources disagree
`business/fintech-compliance` says rounding is a named policy applied once at a named point (for example
half-up); payments-platform rounds half away from zero for basis-point multiplication. No conflict in principle:
the mode is a policy, and rule 9 says which mode the law requires was not verified. The two sign designs in rule 6
(pgledger and payments-platform) are both kept and flagged as a decision to state.

## Related blocks
`business/fintech-compliance`, `skills/design-patterns`, `skills/unknown-payment-outcome-pitfalls`,
`skills/gl-subledger-reconciliation-pitfalls`.
