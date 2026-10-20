# client-portal-app-build-pitfalls §2 — Roles, notifications, integrations and v2

> Part 2 of `skills/client-portal-app-build-pitfalls`. Read it when permissions, notifications, an integration or
> the first release are planned. Craft knowledge, no external source read. Not legal advice.

1. **Roles are abilities inside a client organisation.** Typical shape: client admin (invites and removes users,
   sees everything of the organisation), client member (works with documents and messages), client viewer
   (read only), and on the staff side an account manager, a support agent and an administrator. Symptom: any
   client user can invite new users or see invoices. Fix: named abilities (view documents, upload, approve,
   invite, see billing, export) checked in one place (see `skills/laravel-permissions-not-roles`), a rule that
   a client admin cannot grant more than they hold, at least one admin per organisation, and an audit trail of
   invitations, role changes and removals (see `skills/field-and-row-permission-ui-api-pitfalls`).
2. **Approvals and requests have owners and deadlines.** A request to a client (provide a file, approve a
   quote) has a due date, a reminder rule, an owner on both sides and a state (open, answered, overdue,
   cancelled). Symptom: staff chase by email and nobody knows what is outstanding. Fix: one request object that
   the dashboard on both sides reads.
3. **Notifications carry a pointer, not the content.** Symptom: an email shows the text of a private message or
   an attachment name that is itself confidential, or a forwarded email gives the content to a third party.
   Fix: the email says that something new exists for the client with a link that requires sign-in, never the
   message body or the document; per-user preferences with a digest option; no sensitive data in push or SMS;
   sent after the transaction commits, once per event (see `skills/in-app-notifications-pitfalls` and
   `skills/laravel-mail-via-notifications`). Inbound reply-by-email is a convenience with its own risk: accept
   it only from the verified address of a participant and strip quoted history.
4. **Integrations map external ids, never open the isolation.** Billing, accounting, storage or project tools
   feed the portal: store the external id per record and per organisation, make retries idempotent, and treat
   an outage as a state shown to staff. An invoice or order list for clients is a client-facing view over the
   source data with the same scope rule (see `skills/invoicing-app-build-pitfalls`); payment links follow
   `skills/unknown-payment-outcome-pitfalls`.
5. **Single sign-on and provisioning are per client.** A larger client may bring its own identity provider:
   verify the issuer and subject, map groups to portal roles by a visible rule, handle a user removed at the
   provider (deactivate here too), and keep a break-glass admin. Check the provider flow against the library's
   current documentation; it was not read here.
6. **Imports and exports follow the same scope and are logged.** Bulk client or user creation is staged,
   previewed and idempotent (see `skills/csv-xlsx-import-export-pitfalls`); sending many invitations at once is
   rate-limited and reviewed. A client exporting their own data gets the same scope as the screens, an async job
   and an expiring link; a staff export of many clients requires an ability and an audit entry.
7. **Branding and white labelling stay presentation.** A custom domain, logo and colours per client must not
   change the isolation boundary; the tenant is decided from the session and the membership, not from the host
   name alone (see `skills/laravel-tenant-context-by-default`). Verify domain ownership before serving a client's
   domain and issue certificates through the platform's own mechanism.
8. **Audit and activity are separate views.** The client sees their own activity (who opened, approved,
   uploaded); staff and administrators see the audit trail of access and changes, including impersonation. Both
   are append-only (see `skills/comments-and-activity-feed-pitfalls`).
9. **What to split first.** Build in this order and keep each independent: organisations, users, memberships and
   the scoping function with its tests; invitations and sign-in; documents with versions and expiring links;
   messaging; requests and approvals; notifications; then single sign-on, integrations, branding and exports.
   Ship the first three before any integration: isolation is the data every later feature depends on.
10. **What is regretted at v2.** Isolation checked in the screen only; invitations as permanent links; clients
    and staff in one table; documents overwritten in place; approvals that point at "the current file"; email
    notifications with the content inside; impersonation with no trace; no client admin so staff manage every
    user; no offboarding; internal notes one flag away from the client. Each is cheap at the first migration and
    expensive once clients are using it.
11. **Laravel and Nuxt pointers, short.** In Laravel: a global scope keyed on the session's organisation, a
    policy per ability, hashed invitation tokens with an expiry column and a unique constraint on the pending
    address per organisation, private disk storage with temporary signed URLs after the policy check, an
    approval table that references a version id, and a queued notification sent after commit. In Nuxt: never
    trust the front to hide another client's data, keep the active membership in the session and send it with
    nothing the user can edit, show the impersonation banner from server state, and request downloads from the
    API for a fresh signed link each time.
