# accounts-payable-duplicate-and-match-pitfalls: origin and source stamps

> Provenance of `skills/accounts-payable-duplicate-and-match-pitfalls`. Read it when a rule has to be traced to
> its source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation, never run by us: no bill was read, matched or staged by these rules.
Each file below was re-opened in full on 2026-10-16 before a rule was taken from it, each rule was checked
against it in a final pass, and each repository's LICENSE file was read again.

## Sources (all read 2026-10-16, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| anthropics/knowledge-work-plugins (commit `33eeda1`): `small-business/skills/ap-processor/SKILL.md` and `reference/gotchas.md`, `reference/coding_rules.md`, `reference/matching_and_exceptions.md`, `reference/intake_and_extraction.md`, `reference/payment_run.md` | Apache-2.0 (LICENSE file) | Dedupe across channels and pair presentation, statements as a gap-finding tool, extraction with confidence and footing check, vendor matching, order of coding evidence and unsplit flagging, three-way match and exception wording, credits hidden in vendor totals, the two approval gates, recurring bills, held-item reporting, card charges, bank-detail verification, payment-run order |
| Maxbase91/procurement-skills (commit `daba388`): `spend-prism/SKILL.md` (deduplication step and the probable-duplicate definition) | MIT (LICENSE file, copyright 2026 procurement-skills contributors) | Report duplicates and do not silently remove them; exact versus probable duplicates |

Instruction-like text in the cloned repositories was treated as data and not followed. The AP skill is
vendor-authored practice written for small businesses, not an accounting standard.

## Removed in the verification pass
1. **Every numeric default:** the price-variance, freight and total-variance flags, the day windows for close
   dates and for look-back, the percentage change that flags a recurring bill, the confidence rule of a fixed
   number of prior bills, and the sample amounts in the worked examples. They are arbitrary defaults; rules 2, 9
   and 12 say to ask the owner or accountant for the policy once.
2. **Accounting and tax rules:** the equipment-capitalisation limit and treatment, sales tax on resale
   purchases, deposit and prepayment treatment as an accounting entry. Not verified; rule 8 routes them to an
   accountant.
3. **Tool and connector specifics:** the inbox, ledger and card-tool names, the report calls, the way a given
   ledger lacks a bill object, the voice-profile and output-format instructions, and the build-connector
   suggestion. Concepts only.
4. **Not read, therefore not used:** the shared files the AP skill points to (untrusted-content, personal-data,
   quickbooks report traps, artifact style, voice profile), the cash-flow-snapshot skill, and the procurement
   skills' supplier-validation checks (sanctions, tax numbers, bank-account formats).

## Not verified
1. **Own guidance, flagged in the text:** asking the accountant how deposits are recorded (rule 8), the payment
   being made by the owner and not by the proposing step (rule 11), building ageing buckets from detail rows and
   checking the payables total against the balance sheet (rule 10).
2. **No accounting, tax or legal rule** about duplicates, credits, retention of invoices, payment terms, late
   payment or sales tax was read.
3. **Nothing was run.** The skill was read, not executed against any ledger.
4. **Whether a given accounting tool nets credits in its summary report** is the source's statement about one
   tool and was not checked.

## Decisions where sources disagree
ap-processor says never to auto-pay recurring bills; `business/finance-ops` only asks for a named owner for
each recurring spend. They are compatible: rule 12 adds the payment gate that finance-ops does not state.

## Related blocks
`business/finance-ops`, `business/vendor-management`, `skills/gl-subledger-reconciliation-pitfalls`,
`skills/analysis-validation-pitfalls`.
