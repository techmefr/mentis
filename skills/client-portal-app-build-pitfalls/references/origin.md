# client-portal-app-build-pitfalls: origin and source stamps

> Provenance of `skills/client-portal-app-build-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge, then checked on 2026-10-20 against an open-source commerce framework's documentation, an identity specification and one vendor page. Never run by us: no application was built and no test was executed.

## Sources (read date 2026-10-20, restated in our own words, no text copied)

| # | Source | Licence | What it gave |
|---|---|---|---|
| 1 | Medusa documentation (`medusajs/medusa`, commit `829a622`): `www/apps/resources/app/commerce-modules/user/user-creation-flows/page.mdx` and `user/module-options/page.mdx` (invitations) | MIT: file `LICENSE` read (its enterprise carve-out lists role-based access and single sign-on files only) | Invitation bound to an email, signed token, validity duration, accepted flag, refresh issuing a new token |
| 2 | Medusa documentation, `www/apps/resources/app/commerce-modules/order/secure-order-retrieval/page.mdx` | MIT: same file | Order read by random id without sign-in for guests, list of orders requiring authentication |
| 3 | OpenID Connect Core 1.0 (OpenID Foundation), section 5.7 "Claim Stability and Uniqueness" (`openid.net/specs/openid-connect-core-1_0.html`) | Specification text, read for facts only and restated; no sentence copied | Issuer plus subject as the only stable identifier, email reuse and change |
| 4 | Stripe documentation, page "Provide a customer portal to your customers" (`docs.stripe.com/customer-management`) | Vendor documentation, no open licence stated: facts only, rewritten | Ephemeral portal sessions |

Neighbouring blocks of this repository were read to avoid duplication: `skills/crm-app-build-pitfalls` and
`skills/helpdesk-ticketing-app-build-pitfalls` (shape and depth; the helpdesk block covers the staff side of
tickets, not an invited-client portal), `skills/document-file-management-pitfalls` (internal documents),
`skills/file-upload-ui-pitfalls`, `skills/comments-and-activity-feed-pitfalls`, `skills/in-app-notifications-pitfalls`,
`skills/auth-session-conventions`, `skills/laravel-tenant-context-by-default` and
`skills/field-and-row-permission-ui-api-pitfalls`. No block covered the portal as a whole (invitations,
per-client isolation, shared documents, impersonation, offboarding), so a new block was justified; it links to the
others instead of repeating them.

## Verified
1. §1 points 1, 3, 4 and 5 (partly) and §2 point 5: backed by sources 1 to 4, as the points now say.

## Corrected
1. §1 point 1 now says that the reference framework signs its invitation token rather than hashing a stored one.
2. §1 point 3 states the guest-order trade-off of the reference framework and why a portal should not copy it.

## Removed
1. **Every numeric threshold, token lifetime, link expiry and retention period.** None is stated; set them by policy.
2. **Any statement of electronic-signature, contract, retention or privacy law.** Not read; method only.
3. **Named portal products and identity providers:** not used.

## Not verified
1. **Still our own guidance:** the entity split of organisation, client user and staff (§1 point 2), folders and shares
   (point 6), messaging (point 7), impersonation (point 8), approvals as recorded events (point 9), offboarding (point 10),
   client view models and time zones (points 11 and 12), and in §2 roles, requests, notifications, integrations, imports,
   branding, audit, build order and v2 regrets. No permissive client-portal documentation was identified (searched: the
   Medusa documentation tree and the pages above).
2. **Legal questions** (binding approvals, retention, erasure, privacy duties) belong to a qualified person; this
   is not legal advice.
3. **Nothing was run.** The tests named in the checkpoint were not written or executed.
4. **Identity-provider flows beyond the one claim above and framework pointers** (Laravel, Nuxt) were not checked against current
   documentation; re-read before relying.

## Related blocks
`skills/crm-app-build-pitfalls`, `skills/helpdesk-ticketing-app-build-pitfalls`, `skills/document-file-management-pitfalls`,
`skills/laravel-tenant-context-by-default`, `skills/laravel-no-cascade-delete`, `business/data-protection`.
