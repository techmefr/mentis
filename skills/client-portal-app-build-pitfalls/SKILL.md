---
name: client-portal-app-build-pitfalls
description: "Use when a client or customer portal is designed or built: invitations that expire and bind to one address, client accounts with per-client isolation enforced in every query, shared documents with versions and expiring links, messaging between staff and client, approvals and signatures as recorded events, notifications that leak nothing, staff impersonation with an audit trail, offboarding a client, and what to split first and regret at v2. Method only; contract, signature and privacy law is not legal advice."
---

# client-portal-app-build-pitfalls

A defensive block for building the portal, not for running client relationships. A client portal built in a hurry
fails in familiar ways: an invitation link works for anyone who finds it, one client sees another client's file by
changing an id, a document is replaced and the client signs the old one, a notification email shows the content of a
private message, a staff member "logs in as" a client with no trace, and an ex-client keeps access for years. The content is mostly craft knowledge; some points are checked against an open-source commerce framework's documentation, the OpenID Connect core specification and a payment platform's portal page (see `references/origin.md`). Internal document handling
is `skills/document-file-management-pitfalls`; uploads are `skills/file-upload-ui-pitfalls`; comments and threads are
`skills/comments-and-activity-feed-pitfalls`; notifications are `skills/in-app-notifications-pitfalls`; sign-in is
`skills/auth-session-conventions`, `skills/oauth-oidc-client-pitfalls` and `skills/webauthn-passkey-pitfalls`;
field and row permissions are `skills/field-and-row-permission-ui-api-pitfalls`; tenant boundaries are
`skills/laravel-tenant-context-by-default`; the staff side of a ticket flow is
`skills/helpdesk-ticketing-app-build-pitfalls`; an invoice list for clients builds on `skills/invoicing-app-build-pitfalls`.

## When
- A client area, customer portal, extranet or supplier portal is specified or its schema is drafted.
- A feature touches invitations, document sharing, client messaging, approvals or staff access to a client account.
- An internal tool is being opened to external users.

## Steps

**Read the part you need before the schema or the access rules are written.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Identity and invitations, client and contact model, isolation, shared documents, messaging, approvals, impersonation, offboarding | a schema or an access rule is designed | [`01-model-and-pitfalls.md`](./references/01-model-and-pitfalls.md) |
| 2 | Roles, notifications, integrations, imports, what to split first, v2 regrets, framework pointers | permissions, notifications, an integration or the first release are planned | [`02-roles-integrations-and-v2.md`](./references/02-roles-integrations-and-v2.md) |

## Output / checkpoint
Before building: the entity list (client organisation, client user, staff user, document, message, approval) with a
key and an owner, the invitation lifecycle with expiry and single-use rules, the isolation rule stated as one
scoping function, the document version and link rules, the approval record fields, the impersonation and offboarding
behaviour. Evidence is a test that a client user cannot read another client's record by id, list, search, download
link or export; a test that an expired or reused invitation fails; a test that a replaced document does not change
an earlier approval; and a test that a notification body carries no private content. Nothing here was run by us.

## Guardrails
- This block is not legal advice. What makes an electronic approval or signature binding, retention duties and
  privacy duties towards clients depend on the jurisdiction and the contract; ask a qualified person and state no
  rule here (see `business/data-protection`).
- Never trust an id from the client; scope every read and write by the client the session belongs to, in the query
  (§1, point 3).
- Never make an invitation a long-lived or reusable secret; bind it to one address, make it single-use and let it
  expire (§1, point 1).
- Never overwrite a shared document that was viewed or approved; add a version (§1, point 5).
- Never put private content in a notification email or push; send a pointer and require sign-in (§2, point 3).
- Never impersonate a client without a visible banner, a reason and an audit entry (§1, point 8).
- Never leave a departed client user or organisation with access; offboarding is a defined job (§1, point 9).

## Origin
Written from craft knowledge of building client-portal-style applications, then checked on 2026-10-20 against the
Medusa documentation (MIT), the OpenID Connect core specification and a payment platform's portal page (facts only),
credited in the origin file; no text was taken. See [`references/origin.md`](./references/origin.md). 🟡:
never run by us.
