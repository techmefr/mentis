# in-app-notifications-pitfalls §1 — Model, state and preferences

Source: own craft knowledge, no external source (see origin.md).

## 1.1 One row per recipient
1. **Symptom: marking a notification read for one user clears it for the team, or a second user cannot see it at all.** Cause: one event row with one read flag. Store one row per recipient and event, holding recipient id, type, target reference, actor, created time, seen time and read time.
2. **Fan-out has a cost.** Writing a row for each of 10,000 followers inside the request is slow. Create the rows in a queued job in chunks, idempotent per (event, recipient) so a retry does not double-insert (`laravel-idempotent-jobs`, `background-jobs-conventions`).
3. **Dispatch after the transaction commits**, so a notification never points at a record that rolled back (`laravel-dispatch-after-commit`).
4. **Store a reference and a small payload, not rendered text.** The reference (type, id) lets the text follow a rename and a locale change; the payload keeps what is needed when the target is later deleted ("Invoice 2024-0031 was deleted").
5. **Render the message in the reader's locale at read time**, not the sender's at write time (`i18n-message-format-pitfalls`, `locale-value-formatting-pitfalls`).

## 1.2 Seen against read
1. **Two states are not one.** Seen means the user opened the inbox and the badge may clear; read means the user opened the item. Collapsing them either leaves a badge that never clears or hides items that were never looked at.
2. **Opening the inbox marks seen, not read.** Clicking an item, or an explicit control, marks read. A "mark all as read" control exists and applies to what the user can see, with the count in its confirmation.
3. **Mark read on the server when the target is opened**, from the link, not from a separate client request that can be lost.
4. **Allow marking unread**, since people use the inbox as a to-do list.
5. **Do not mark read on a prefetch or a preview.** Symptom: items read that nobody opened, caused by a link-unfurler or a hover prefetch following the notification URL. Use a non-GET call for the state change, or a token the prefetch does not trigger.

## 1.3 The unread count
1. **Symptom: the badge says 3, the list shows 2 (or nothing).** Causes: the counter is a separate field incremented by pushes and decremented by clicks; items were deleted or expired; two tabs disagree.
2. **Compute the count from the rows** (a count over unread rows for the user, backed by an index on recipient and read time). If a cached counter is needed for scale, rebuild it from the rows on a schedule and on any bulk change, and treat it as a hint.
3. **Cap the display and keep the real count honest** ("99+"), and never show a negative or a zero badge as a dot.
4. **Counts exclude what the user can no longer open** or the list must show it as unavailable; pick one and apply it to both.
5. **Several tabs and devices share one truth**: after a read in one tab, the others update on the next push or focus event (§2.1).

## 1.4 Grouping and digests
1. **Symptom: 40 "new comment" rows for one busy thread.** Group by (type, target) within a window, show "Ana and 3 others commented on Invoice 31", and keep the latest actor and count on the group row.
2. **A group is one read state.** Opening it marks the whole group read; a new event after that re-opens the group as unread with the new count.
3. **Update a group in place, do not insert a new row**, and keep the position rule explicit (move to top on new activity, or stay).
4. **Digests are a channel choice, not a different table.** The same rows feed an hourly or daily mail; mark rows as digested so none is sent twice and none is dropped.
5. **Do not group across different recipients' permission scope**: a group naming actors a reader cannot see leaks them (`field-and-row-permission-ui-api-pitfalls`).
6. **Do not notify the actor of their own action**, and collapse duplicates of one action fired twice (double click, job retry) with the idempotency key from §1.1.

## 1.5 Types and links
1. **Keep a registry of notification types**: id, template, default channels, whether it can be muted, which target it opens. A type outside the registry is rejected at send time.
2. **Every item opens something**, a deep link to the record and the exact place (comment, row), with a fallback page when the target is gone.
3. **Links are built from ids and routes, never from stored full URLs**, so a domain change or a tenant move does not break the history.
4. **Do not put sensitive content in the preview text** that also goes to a lock screen, a mail or a push; show a neutral line and the detail after opening (`telemetry-sensitive-data-pitfalls` for what must not be logged either).

## 1.6 Preferences and channels
1. **Preferences are per user, per type (or category), per channel**: in-app, mail, push, digest or off. A single global switch is too coarse; a matrix of fifty types is unusable, so group types into categories.
2. **Resolve preferences at send time on the server**, for every channel from the same function. Symptom: muted in the interface but the mail still arrives, because the mail path reads another setting.
3. **Some classes cannot be muted** (security alerts, billing failures, legal notices). Mark them mandatory in the registry, show them as locked in the settings with the reason.
4. **Defaults are a product decision, not an accident**: new types start with the category default, and a new category announces itself once rather than silently going to everyone.
5. **Respect quiet hours and time zone** for push and mail, not for the in-app inbox, which is passive. Store the zone with the preference (`locale-value-formatting-pitfalls`).
6. **Unsubscribe from the channel itself works in one step** (a mail footer link, a push setting) and writes the same preference row.
7. **Muting a thread or a record** is a separate subscription rule on the target, checked with the type preference.
8. **Deleting a user or an opt-out request** removes or anonymises their rows and preferences (`dsar-handling-pitfalls`).

## 1.7 Retention
1. **Notifications are ephemeral by design**: expire read items after a stated period and unread ones later, by a scheduled prune, not by hand. Say the period in the interface.
2. **Pruning must fire the same events as other deletes** if listeners depend on them (`laravel-pruning-fires-delete-events`).
3. **Keep an audit record elsewhere when the message has business meaning** (an approval request): the inbox is not the system of record.
4. **Check the checks**: the registry (§1.5), the per-recipient row (§1.1), the count query (§1.3), the preference function (§1.6) and the prune job each have a test in §2.6.
