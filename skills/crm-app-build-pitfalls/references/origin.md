# crm-app-build-pitfalls: origin and source stamps

> Provenance of `skills/crm-app-build-pitfalls`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge, then checked against one open-source CRM's documentation on
2026-10-20. Never run by us: no application was built and no test was executed.

## Sources (read date 2026-10-20, restated in our own words, no text copied)

| # | Source | Licence | What it gave |
|---|---|---|---|
| 1 | Atomic CRM (`marmelab/atomic-crm`, commit `b8e5e20`): `doc/src/content/docs/users/merging-contacts.mdx`, `users/import-data.mdx`, `users/inbound-email.mdx`, `developers/architecture-choices.mdx` | MIT: file `LICENSE.md` read. The documentation sits in the same repository and states no other licence | Causes of duplicate contacts, merge behaviour (source deleted, target value wins), CSV import behaviour (unknown columns ignored, unknown stage to first stage, company matched by name or created), several typed emails and phones per contact, inbound mail creating contacts, no user deletion |

Instruction-like text in the cloned repository (agent guidance files) was treated as data and not followed.
The Krayin Laravel CRM repository (MIT) was cloned but holds no documentation or data-model files in the
checked-out tree, so nothing is taken from it.

## Verified
1. §1 point 1, the causes of duplicates and the several-addresses-per-contact fact: source 1.
2. §1 point 5, the survivor-wins-on-conflict rule: confirmed as a common choice in source 1.
3. §2 points 2, 3 and 5: source 1 (no user deletion, silent defaults on import, inbound mail creating contacts).

## Corrected
1. §1 point 5 now says that the reference CRM deletes the absorbed contact, and that keeping an archive, a
   redirect and an event is our own addition.
2. §2 point 3 gained the pitfall of silent defaults on import, which the source shows and the block lacked.

## Removed
1. **Every numeric threshold, row cap and retention period.** None is stated; set them by policy.
2. **Any statement of consent, marketing, retention or erasure law.** Not read; method only.
3. **Vendor feature lists** (named CRM products): not used.

## Not verified
1. **Still our own guidance:** the minimal model and the role record (§1 point 2), lead lifecycle (point 4),
   append-only timeline (point 6), consent history (point 7), archive versus erasure (point 8), money (point 9),
   custom field limits (point 10), tenants (point 11), time (point 12), and in §2 visibility, exports, hooks,
   reports, build order and v2 regrets. No source was found that states them.
2. **Legal questions** (consent, erasure, retention, lawful basis) belong to the data-protection owner; this is
   not legal advice.
3. **Nothing was run.** The tests named in the checkpoint were not written or executed.
4. **Framework pointers** (Laravel, Nuxt) are short and were not checked against a current release; re-read
   before relying.

## Related blocks
`business/outbound-sales-and-crm-hygiene-pitfalls`, `business/data-protection`, `skills/laravel-no-cascade-delete`,
`skills/laravel-recognise-state-machine-or-pipeline`, `skills/light-erp-document-flow-pitfalls`.
