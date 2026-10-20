# client-portal-app-build-pitfalls §1 — Model and pitfalls

> Part 1 of `skills/client-portal-app-build-pitfalls`. Read it when a schema or an access rule is designed.
> Craft knowledge, no external source read. Each point gives the symptom, the check and the fix. Not legal advice.

1. **An invitation is a short-lived, single-use, address-bound token.** Symptom: a forwarded invitation lets a
   stranger claim the account, or an old link still works after the user was re-invited. Check: use the link
   twice, use it after expiry, use it after a newer invitation was sent, and use it while signed in as someone
   else. Fix: store a hash of a random token (never the token), the target email normalised, the client
   organisation and role granted, an expiry, a used-at time and the inviter; on use, require the sign-in or
   sign-up to match the invited address or confirm it by a code, mark it used in the same transaction as the
   account creation, make a new invitation revoke the previous one, and show the inviter the state (sent,
   opened, accepted, expired, revoked). A resend creates a new token, it never extends the old one.
2. **Client organisation, client user and staff user are different entities.** Symptom: a client user is a row
   in the staff table with a flag, so a staff query leaks clients or a client query leaks staff notes. Fix: a
   client organisation (the unit of isolation), client users belonging to it through a membership with a role,
   staff users in their own space, and a staff-to-client assignment (who serves which client). A person who
   works for two clients has two memberships under one login, and the session says which one is active. Keep
   internal notes in a separate entity or a visibility field that is internal by default.
3. **Isolation is a rule on the query, not on the screen.** Symptom: changing an id in the address shows another
   client's document, or the search, the export, the download link and the API return rows the list hides.
   Check: sign in as client A and request client B's record by id on every path: detail, list, search, download,
   export, API, websocket channel. Fix: one scoping function (organisation id from the session, never from the
   request) used by every read and write path (see `skills/laravel-scope-dont-check-after-fetch` and
   `skills/laravel-tenant-context-by-default`), the organisation id on every table including join tables and
   files, the same boundary in the search index and in file storage paths, and a test per path. Answer a
   forbidden record with the same response as a missing one so ids cannot be probed.
4. **Authentication fits clients, not staff.** Symptom: shared client logins, password resets that reveal whether
   an address exists, or clients locked out with no recovery. Fix: one login per person, sign-in methods chosen
   for the audience (email link, password plus second factor, passkey, or single sign-on for larger clients; see
   `skills/auth-session-conventions`, `skills/oauth-oidc-client-pitfalls` and `skills/webauthn-passkey-pitfalls`),
   neutral reset responses, session lifetime and device list shown to the user, and a documented recovery path
   handled by staff with identity checks. Client single sign-on maps external identities to memberships by a
   stable subject, not by email alone.
5. **Shared documents are versioned, scoped and delivered through short links.** Symptom: staff replace a file
   after the client viewed or approved it, a public link is forwarded, or a file is reachable by guessing its
   storage path. Fix: a document record with versions (each immutable: file, checksum, uploader, time), a
   current-version pointer, a visibility field (internal, shared with client), storage that is private with
   downloads through an authorised, expiring link issued after the scope check (see `skills/file-upload-ui-pitfalls`
   for the upload side and `skills/document-file-management-pitfalls` for the internal side), file type and size
   checks and malware scanning on upload from clients, and a record of who viewed or downloaded which version.
   Check: upload, share, replace, then confirm the earlier version and any approval on it are unchanged.
6. **Folders and shares inherit one rule.** Symptom: a sub-folder is shared more widely than its parent, or
   moving a document exposes it. Fix: access is decided by the organisation and the document's visibility, not
   by folder position alone; a move re-checks visibility; sharing with a single client user inside an
   organisation is an explicit grant, not an inheritance accident.
7. **Messaging is a thread bound to a client and, where useful, an object.** Symptom: a message is posted to the
   wrong client, a staff member reads a thread they should not, or a reply by email lands nowhere. Fix: threads
   belong to one client organisation and optionally to a document, order or request; participants are
   explicit; staff internal notes live in a separate visibility class that is never rendered to clients; messages
   are append-only with an edited flag (see `skills/comments-and-activity-feed-pitfalls`); inbound email replies
   are matched by a per-thread address or token, not by subject; attachments follow point 5; and read state is
   per user. Response-time promises belong to the support process (see
   `skills/support-queue-design-pitfalls`).
8. **Staff access to a client account is an audited, visible act.** Symptom: "log in as the client" is used to
   debug and nobody can say who saw what. Fix: impersonation needs an ability and a stated reason, shows a
   banner in the session, blocks sensitive actions (password change, approvals, payments) unless explicitly
   allowed, writes an audit entry with staff user, client, start, end and actions, and optionally notifies the
   client. Read-only view-as is safer than act-as.
9. **Approvals and acknowledgements are recorded events.** Symptom: a client "approved" a quote and cannot prove
   or dispute what they approved. Fix: an approval record with the document version id and checksum, the user,
   the membership, the time, the exact wording shown, the choice (approved, rejected, changes requested) and
   the network context the policy keeps; an approval is never edited, a change is a new document version and a
   new request. Whether this is a binding electronic signature is a legal question; use a dedicated signature
   provider where the contract requires one, and store its reference.
10. **Offboarding is a defined job.** Symptom: a user who left the client company still has access, or a former
    client's data stays reachable with no decision. Fix: deactivate a client user instead of deleting (history
    keeps its author), revoke sessions and tokens at once, let a client admin remove their own users, an
    inactivity review for dormant accounts, and, when the relationship ends, an organisation state (active,
    suspended, closed) with a scheduled export for the client and a retention and erasure routine that is audited
    (see `skills/laravel-no-cascade-delete` and `business/data-protection`). Retention periods are for the
    contract and a qualified person.
11. **Every list shows only what the client can act on.** Symptom: the client sees internal statuses, staff
    names, costs or draft items. Fix: a client-facing view model separate from the staff model, with its own
    status vocabulary mapped from internal states and fields exposed by an allow-list, not by hiding columns.
12. **Time zones and language belong to the user.** UTC storage, display in the user's zone, locale stored per
    user, and message templates translated (see `skills/i18n-message-format-pitfalls`). Symptom: a due date shown
    as "yesterday" to a client in another zone.
