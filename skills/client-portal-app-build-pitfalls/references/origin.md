# client-portal-app-build-pitfalls: origin and source stamps

> Provenance of `skills/client-portal-app-build-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from craft knowledge on 2026-10-20, never run by us: no application was built and no test
was executed.

## Sources (read date 2026-10-20)

| Source | Licence | What it gave |
|---|---|---|
| None read | not applicable | Written from general craft knowledge of building client-portal-style applications. No open-source portal code, identity-provider documentation or signature-provider documentation was opened; no LICENSE file was read because no source was used. |

Neighbouring blocks of this repository were read to avoid duplication: `skills/crm-app-build-pitfalls` and
`skills/helpdesk-ticketing-app-build-pitfalls` (shape and depth; the helpdesk block covers the staff side of
tickets, not an invited-client portal), `skills/document-file-management-pitfalls` (internal documents),
`skills/file-upload-ui-pitfalls`, `skills/comments-and-activity-feed-pitfalls`, `skills/in-app-notifications-pitfalls`,
`skills/auth-session-conventions`, `skills/laravel-tenant-context-by-default` and
`skills/field-and-row-permission-ui-api-pitfalls`. No block covered the portal as a whole (invitations,
per-client isolation, shared documents, impersonation, offboarding), so a new block was justified; it links to the
others instead of repeating them.

## Removed
1. **Every numeric threshold, token lifetime, link expiry and retention period.** None is stated; set them by policy.
2. **Any statement of electronic-signature, contract, retention or privacy law.** Not read; method only.
3. **Named portal products and identity providers:** not used.

## Not verified
1. **All points are our own guidance** and were not compared with any open-source portal.
2. **Legal questions** (binding approvals, retention, erasure, privacy duties) belong to a qualified person; this
   is not legal advice.
3. **Nothing was run.** The tests named in the checkpoint were not written or executed.
4. **Identity-provider flows and framework pointers** (Laravel, Nuxt) were not checked against current
   documentation; re-read before relying.

## Related blocks
`skills/crm-app-build-pitfalls`, `skills/helpdesk-ticketing-app-build-pitfalls`, `skills/document-file-management-pitfalls`,
`skills/laravel-tenant-context-by-default`, `skills/laravel-no-cascade-delete`, `business/data-protection`.
