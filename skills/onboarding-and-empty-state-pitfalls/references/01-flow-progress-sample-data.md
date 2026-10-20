# onboarding-and-empty-state-pitfalls §1 — Flow, progress and sample data

Source: own craft knowledge, no external source (see origin.md).

## 1.1 First-run routing
1. **Symptom: the welcome flow shows again on a new browser, or never shows for an invited user.** Cause: first-run kept in a cookie or local storage. Store an onboarding state on the user (and on the workspace for shared setup) and decide the route from it on each entry.
2. **Keep user onboarding and workspace setup apart.** The first person creating a workspace configures it; an invited member only learns the product. Ask a second user to redo the workspace steps and the page punishes them.
3. **Route by role and by what is already true.** A user invited to an existing workspace with data skips "create your first project". An existing user after a migration is never treated as new.
4. **Never block the product behind onboarding** unless a legal or technical prerequisite demands it (accepting terms, verifying an address). Everything else is skippable (§1.4).
5. **Preserve the intended destination.** An invitation or a deep link lands on its target after the minimum necessary step, not on the welcome screen.
6. **Do not rely on "account created less than N days ago"** as the rule. Use explicit completion and dismissal state; age is a nudge condition, not a state.
7. **Treat sign-in, sign-up and invite-accept as one funnel** for state purposes; a person arriving by social sign-in or passkey gets the same stored state (`auth-session-conventions`, `webauthn-passkey-pitfalls`).

## 1.2 Checklist model
1. **A checklist is a list of steps with a stored status each**: id, status (open, done, skipped, dismissed), time and, where it applies, the evidence. Keep ids stable across releases; renaming a step must not reset it.
2. **Derive done from data when the data exists**: "Add a teammate" is done when a second member exists, whoever added them and however. A manually ticked step is for things the system cannot see.
3. **Symptom: a step stays done after the user deleted the thing.** Recompute derived steps on read; keep an "ever done" marker if the history matters for messaging only.
4. **Order is a suggestion, not a lock**, unless one step truly depends on another; then say which and why in the step text.
5. **Keep the list short and about value**: the steps that lead to the first real result, not a tour of the menu. A step the user cannot do without a permission is hidden or marked "ask an admin".
6. **New steps added later** appear as new items, with a one-time notice, without reopening a checklist the user completed or dismissed.
7. **Show progress honestly**: count of derived done over visible steps, not a bar that jumps when a step is added or hidden.
8. **One completion event**: when the last step is done, record it once and stop prompting. Idempotent, since two tabs can finish the same step (`laravel-idempotent-jobs` for the pattern).

## 1.3 Persistence and devices
1. **Progress lives on the server**, keyed by user (and workspace where relevant). Local storage may cache it for speed, never own it.
2. **Resume exactly**: store the current step and any draft input (`long-and-multistep-form-pitfalls` for draft handling), so closing the tab mid-flow loses nothing.
3. **Handle two tabs and two devices**: a step done in one shows in the other on focus or reconnect; last write does not undo a done status.
4. **Resolve the user's locale and timezone at the start of the flow**, since the first screens set the tone (`locale-negotiation-and-switcher-pitfalls`).
5. **Do not persist secrets in the progress object** (invite tokens, generated keys); store the fact that the step happened.
6. **A reset for support and for testing**: an admin or a debug path can reset onboarding state for a user, audited, otherwise testers create accounts forever.

## 1.4 Skip, dismiss and resume
1. **Symptom: users feel trapped, or lose the checklist by closing it once.** Every step and the whole flow have a visible skip or dismiss, with the consequence stated ("You can finish this later in Settings").
2. **Dismiss is not complete.** Record them as separate states; a dismissed checklist stays reachable from a persistent entry (a help menu, a settings item) and can be reopened.
3. **Skipping a step may leave the product in a state that needs a safe default** (no team, no currency chosen). Define it per step and test it (`settings-and-preferences-page-pitfalls` §1.2 for defaults).
4. **A reminder after skipping is a nudge with a limit**: show at most once per session or per event, never a modal on every page, and stop after an explicit dismissal.
5. **Respect "do not show again"** per surface and per user, stored on the server, not per browser.
6. **Back and forward work.** The browser back button inside a multi-step flow goes to the previous step, not out of the flow; the step is in the URL or the history state.

## 1.5 Tours and in-context hints
1. **A tour is a feature with state**: seen, skipped, completed, with a version. A tour that replays after each release teaches users to ignore it; version it and show it only when its content changed meaningfully.
2. **Anchor to elements that exist.** Symptom: a tooltip points to nothing because the target is behind a permission, a collapsed menu or a different viewport. Skip steps whose target is absent, and never throw.
3. **Do not cover what the step asks the user to click.** A spotlight that blocks the control, a tooltip off the viewport on mobile, a step that needs a hover on a touch device are the usual faults.
4. **Offer contextual hints at the moment of need** (an inline hint on first empty state, a tip on first use of a feature) rather than one front-loaded tour.
5. **Never auto-start a tour in front of a task.** A user arriving via a deep link to do work does not want a tour first.
6. **Keep copy short, in the product's voice, translated** (`i18n-message-format-pitfalls`), and verify the translated text still fits the anchor.

## 1.6 Sample data
1. **Symptom: the dashboard shows 12 invoices and 3 are demo; or the sample customer received an email.** Flag every sample record at creation (a boolean or a source field), never infer it from the name.
2. **Exclude samples from real aggregates by default**: totals, exports, billing counts, usage limits, search facets and reports, or show them with a visible "Sample" marker everywhere they appear. Pick one and apply it to every query path.
3. **Never send anything outward from sample data**: mail, webhooks, payments and integrations are suppressed for flagged records (`laravel-mail-via-notifications`).
4. **Remove in one action**, reachable from the empty-state area and from settings, that deletes exactly the flagged records and nothing else, with a count in the confirmation. Deleting the first real record must not delete samples and vice versa.
5. **The first real record replaces the empty or sample state** gracefully: offer to clear the samples, do not clear them silently.
6. **Samples are seeded per workspace, idempotently**, in a job, localised, with plausible but obviously fake values; use the project's seeder conventions (`laravel-idempotent-seeders`) and never real personal data.
7. **Sample data obeys the same permissions and tenant scope** as real data (`laravel-tenant-context-by-default`).
8. **A guided demo is not a sample**: a read-only sandbox or video tour needs no records in the user's workspace and no cleanup.

## 1.7 Invitations and first contact
1. **An invitation is a state machine**: pending, accepted, expired, revoked. Opening an expired or revoked link explains and offers a request, not a generic error.
2. **Accepting while signed in as another account** is a defined case: say which account is signed in, and offer to switch.
3. **Invitation tokens are single-use, expire and are not logged** (`credential-lifecycle-pitfalls`, `telemetry-sensitive-data-pitfalls`).
4. **The first screen after accepting shows what the inviter shared**, not an empty product.
5. **Resend and revoke are available to the inviter**, with an audit entry for workspace-level invitations (`admin-back-office-pitfalls`).
