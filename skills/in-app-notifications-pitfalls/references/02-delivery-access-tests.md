# in-app-notifications-pitfalls §2 — Delivery, access and tests

Sources: Lexical documentation on live-region announcements (MIT, read 2026-10-20), WCAG 2.2 (full Recommendation and understanding pages for SC 4.1.3 and SC 2.2.1, read 2026-10-20), WAI-ARIA 1.2 and the HTML Standard (server-sent events, online status; full pages, read 2026-10-20), facts only, for the points marked as such; the rest is own craft.

## 2.1 Realtime against polling
1. **Push is an optimisation over a truth you can always re-read.** The inbox endpoint returns the real state; a push only says "something changed, refetch" or carries one item. Symptom of the opposite: a missed push leaves the badge wrong until reload.
2. **Refetch on the events that prove staleness**: tab becomes visible, window focus, network back online, socket reconnect. This one rule removes most "it only shows after reload" reports. The HTML Standard says navigator.onLine returns false only when the browser is definitely offline and true when it merely might be online, and calls the attribute inherently unreliable; so use the online event as a trigger to refetch, never as proof that the server is reachable, and keep the error state of §2.2.1.
3. **Polling is a valid choice** for a business application with a few notifications per hour. Pick an interval from the product need, back off when the tab is hidden, and send a conditional request (an etag or a "since" id) so an unchanged answer is small: with an etag the client lists the tags it holds in If-None-Match and the server may answer 304 Not Modified when one matches (RFC 9110 section 13.1.2, read 2026-10-20). Do not poll from every open tab at full rate.
4. **Realtime transports differ in cost.** A socket needs authentication at connect, reauthentication when the session ends, and a fallback when proxies drop it; server-sent events are one-way and enough for a bell (the HTML Standard defines the browser object that reconnects on its own and reports the last event id it saw in a Last-Event-ID request header, so the server can resume; replaying missed items is the server's job). Choose the simplest that meets the need (`laravel-conventions` for broadcasting in the Laravel back end).
5. **Authorise the channel per user.** A private channel name derived from the user id is not access control; the server must check that the subscriber is that user (`security-hardening`).
6. **Sequence the items.** Give each row a monotonic id or time and ask "after id N" on reconnect (with server-sent events, the Last-Event-ID header carries that id back, HTML Standard), so a gap is detected and filled instead of assumed absent. Reorder by created time, not arrival time.
7. **Deduplicate on the client by notification id**, since a push and a refetch can deliver the same item.
8. **A logged-out user stops receiving.** Close the connection on sign-out and on a tenant switch; otherwise the next person on a shared machine hears the previous user's inbox.

## 2.2 States of the inbox
1. **A failed load is not an empty inbox.** Symptom: the fetch's error handler sets the list to empty and the count to zero, so a network error clears the badge and shows the "all read" state. Check: grep the loader's catch branch; it must keep the previous data or show an error with retry, and never write zero. Render separately: loading, empty (nothing yet), empty-filtered (nothing unread), error with retry, offline, and partial (older page failed). Never show "no notifications" for a failed request (`data-table-ui-pitfalls` §2.1).
2. **Paginate with a cursor** on created time and id, since new items arrive at the top while the user reads; offset would repeat rows (`data-table-ui-pitfalls` §1.2).
3. **Do not reorder under the pointer.** New items during reading show as a "2 new" control, not a jump.
4. **Filter by unread, by type category and by target**, and keep the count of each honest (§1.3).
5. **A toast is a different object from an inbox item.** It auto-dismisses, so anything that needs action must also exist in the inbox; never make a toast the only place a decision is shown.
6. **Relative times ("5 min ago") are built with the platform's relative-time formatter and re-rendered on a timer** (`locale-value-formatting-pitfalls` §3.2); a label computed once at render goes stale while the page stays open.

## 2.3 Accessibility
1. **The badge needs text.** Give the bell button an accessible name that includes the count ("Notifications, 3 unread"); a bare number inside an icon has no name (WCAG 2.2 SC 4.1.2, level A: user interface components expose a name and role to assistive technology). Do not rely on colour alone for unread (`accessibility`).
2. **Announce through one polite live region** that exists in the page at load, then change its text. A region inserted together with its message is often not announced (recalled practice: WAI-ARIA 1.2 defines what counts as a relevant change inside a live region, additions and text by default, and says nothing on a region created together with its content). Lexical's accessibility documentation describes the same pattern: a visually hidden status region, polite by default, created once and reused (read 2026-10-20).
3. **Do not announce every item.** Batch ("3 new notifications"), rate-limit, and do not announce the user's own actions. Use assertive only for what needs immediate action; a ticking inbox is not that. In WAI-ARIA 1.2 the status role is implicitly polite and atomic, the log role is implicitly polite and fits sequential additions at the end, and the alert role is assertive, for important and time-sensitive messages. WCAG 2.2 SC 4.1.3 (understanding page read 2026-10-20) asks that status messages be programmatically identifiable so assistive technology announces them without moving focus; it suggests the status role for the outcome of an action or the state of an application, the alert role (or a live region) for a suggestion or a warning about an error, and the log role (or a progress live region) for progress and sequential updates, and lists alert or assertive on unimportant content as a common failure.
4. **Do not move focus** to a new notification or a toast. Focus stays where the user is working.
5. **Toasts stay long enough to read and can be paused or dismissed by keyboard**; Escape closes them and the timer stops while they are hovered or focused. A toast with an action button needs to remain reachable. An auto-dismissing toast is a time limit set by the content, so check it against WCAG 2.2 SC 2.2.1 (re-read in the full Recommendation 2026-10-20: turn off, adjust to at least ten times the default, or warn and allow at least 20 seconds to extend, at least ten times; exceptions for real-time and essential limits); applying that criterion to toasts is our reading, not a quote.
6. **The inbox is a list of links or buttons with names**, the unread state stated in text for screen readers, a heading for each group, and a keyboard path from the bell to the first item and back to the bell on close.
7. **The panel is a popover or a page, not a trap.** If it opens as a dialog, trap and restore focus (the modal dialog pattern keeps Tab inside, closes on Escape and returns focus to the opener); if it is a disclosure, note that the ARIA Authoring Practices disclosure pattern defines only Enter and Space on the button and aria-expanded, so Escape and outside-click closing are your own additions and need your own test. Check both with the keyboard only.
8. **Respect reduced motion** for badge pulses and slide-in toasts.

## 2.4 Permissions at open time
1. **Access is checked when the item is opened**, not when it was sent. Symptom: a notification leads to a record the user lost access to, or leaks its title in the list after the permission was removed.
2. **The list shows only what the user may still see.** Hide or redact the text of rows whose target is no longer authorised, and show "no longer available" on open.
3. **Check tenant scope on the target**: a notification id from another tenant must return not found, not a different tenant's record (`laravel-tenant-context-by-default`).
4. **Enforce per row on the server**; the client hiding a link is not a control (`field-and-row-permission-ui-api-pitfalls`).

## 2.5 Mistakes of delivery
1. **Mail and in-app for the same event must agree**: one notification, several channels, one preference check (`laravel-mail-via-notifications`). Two code paths drift.
2. **A failing channel must not block the others**: a mail error does not stop the inbox row.
3. **Do not notify during a bulk import or a migration** unless it is the point; add a suppress flag on the job.
4. **Rate-limit per recipient** so a runaway loop cannot send a thousand messages; log the suppressed count.
5. **Send a test notification to yourself** from the settings page; it is the cheapest end-to-end check a user can run.

## 2.6 Tests
1. **Per-recipient state**: create one event for two users; read it as one; assert the other is unread.
2. **Count parity**: for a mix of read, unread, deleted and expired rows, assert the badge equals the unread rows the list returns.
3. **Grouping**: fire three events on one target in the window; assert one group row with count 3, and a new event after read re-opens it.
4. **Preferences**: muted category sends nothing on any channel; a mandatory type ignores the mute; assert each channel.
5. **Idempotent fan-out**: run the fan-out job twice; assert no duplicate rows.
6. **Gap recovery**: drop a push in a test, reconnect, assert the refetch brings the missing item.
7. **Access at open**: remove the user's permission after the send and assert the open returns not available and the list redacts it.
8. **Accessibility**: assert the bell name with count, a live-region update that does not move focus, and a keyboard-only pass over the panel; run an automated check.

## 2.7 Framework pointers (reference only)
1. **Laravel** has a notifications layer with database and broadcast channels; keep the channel list and preference check in one place and route mail through it (`laravel-mail-via-notifications`, `laravel-permissions-not-roles`).
2. **React or Nuxt query layers**: key the inbox query by user and filter, invalidate it on push, focus and reconnect, keep previous data while loading (`data-fetching-state-conventions` §2).
3. **Vuetify or similar kits** offer badge, snackbar and menu components; check their default live-region and focus behaviour against §2.3 instead of assuming it (`vue-nuxt-vuetify-conventions`).
4. **Phone push** is a separate channel with its own permission prompt and token lifecycle (`flutter-notifications-background`).
