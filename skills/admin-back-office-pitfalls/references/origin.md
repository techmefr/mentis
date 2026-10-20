# admin-back-office-pitfalls: origin and source stamps

> Provenance of `skills/admin-back-office-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge, then checked on 2026-10-20 against one admin framework's documentation. Never run by us: no application was built and no test was executed.

## Sources (read date 2026-10-20, restated in our own words, no text copied)

| # | Source | Licence | What it gave |
|---|---|---|---|
| 1 | Django documentation (`django/django`, commit `45ce894`): `docs/ref/contrib/admin/index.txt` (the log entry model, per-model permission methods), `docs/ref/contrib/admin/actions.txt` (bulk actions, the delete action, action permissions), `docs/ref/contrib/auth.txt` (the active flag) | BSD-3-Clause: file `LICENSE` read; the documentation sits in the same repository and states no other licence | Admin log row shape, bulk delete skipping the model's delete method, confirmation page on delete, permission per action, deactivating accounts instead of deleting them, a separate staff flag |

Neighbouring blocks of this repository were read to avoid duplication: `skills/feature-flag-lifecycle`
(flag creation, ramp and removal), `skills/field-and-row-permission-ui-api-pitfalls`,
`skills/laravel-permissions-not-roles`, `skills/data-table-ui-pitfalls`, `skills/csv-xlsx-import-export-pitfalls`,
`skills/crm-app-build-pitfalls` and `business/data-protection`. The overlap check found no block that covers
building an admin back office (audit log, impersonation, dangerous and bulk actions); flag lifecycle is already
covered, so this block only cross-links it.

## Verified
1. §1 points 1, 2, 3, 8 and 9 and §2 point 1: backed by source 1, as the points now say.

## Corrected
1. §1 point 3 now states what the reference log does not hold (before and after values, effective actor, reason), so
   the extra columns are clearly our own requirement.
2. §1 point 1 now separates what the framework does from what is ours (second factor, separate host).

## Removed
1. **Every numeric threshold, cap, expiry and retention period.** None is stated; set them by policy.
2. **Any statement of law on access logging, retention or notification.** Not read; method only.
3. **Named admin frameworks and impersonation packages:** not used.

## Not verified
1. **Still our own guidance:** impersonation (§1 points 5 and 6; the framework read has none), flags in admin (point 7),
   previews, caps and select-all semantics (points 9 and 10, beyond the bypass fact), shared validation (point 11),
   production query safety (point 12), and in §2 the two-person rule, customer notification, internal notes, search,
   accessibility, dashboards, build order and v2 regrets. No other permissive source was identified (searched:
   Django admin documentation only; other admin frameworks were not read).
2. **Legal questions** (logging of staff access, retention, notification duties) belong to the data-protection
   owner; this is not legal advice.
3. **Nothing was run.** The tests named in the checkpoint were not written or executed.
4. **Framework pointers** (Laravel, Nuxt) are short and were not checked against a current release; re-read
   before relying.

## Related blocks
`skills/feature-flag-lifecycle`, `skills/field-and-row-permission-ui-api-pitfalls`, `skills/laravel-no-cascade-delete`,
`skills/laravel-idempotent-jobs`, `business/data-protection`.
