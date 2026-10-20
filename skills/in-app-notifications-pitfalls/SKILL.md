---
name: in-app-notifications-pitfalls
description: "Use when an in-app notification centre (bell, inbox, toast, unread badge) is designed, written or reviewed in a business application, whatever the framework: one row per recipient against one row per event, read and seen state, unread counts that drift, grouping and digests, per-user preferences and channel routing, delivery by realtime push against polling, retention, and the accessibility of badges, live regions and the inbox list, plus the tests that catch them."
---

# in-app-notifications-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the inbox every business application grows. The premise: **a notification
is a promise that something needs the reader, and every defect breaks that promise one way**: the badge says 3 and the
list shows 2, the same event arrives five times, a message links to a record the user may no longer open, a mute
setting is ignored on one channel, a screen reader never hears the new item. Sending the message itself (mail,
channel-agnostic dispatch) is in `laravel-mail-via-notifications`; the push channel on a phone is in
`flutter-notifications-background`; queue behaviour of the sending jobs is in `background-jobs-conventions`; list
mechanics (paging, states) follow `data-table-ui-pitfalls`, and widget accessibility in general is in `accessibility`.

## When
- A bell, inbox page, toast area or unread badge is built or changed.
- A user reports "the count is wrong", "I get duplicates", "I muted it and still get it", "it only shows after reload".
- A new event type, channel or preference setting is added, or realtime delivery is introduced or removed.

**Skip when** a part is absent: a bell that links straight to a page has no popover, so the seen state of §1.2 is meaningless (say so and drop it); an application with no realtime or digest skips §2.1.4 to §2.1.6 and §1.4.4; a toast-only application skips the data model. Say "not applicable: reason" rather than invent a finding.

## Steps

**Read the section the task meets.** Each ends with checks.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Data model, read and seen state, unread count, grouping, preferences, channel routing, retention | the notification table, counter, grouping or settings are written | [`01-model-state-preferences.md`](./references/01-model-state-preferences.md) |
| 2 | Realtime against polling, ordering and gaps, states, accessibility, permissions at open time, tests, framework pointers | delivery, the inbox UI or its tests are written | [`02-delivery-access-tests.md`](./references/02-delivery-access-tests.md) |

## Output / checkpoint
A change is done when: each recipient has their own row with its own read state; the unread count is computed from
those rows and survives a missed push; preferences are checked at send time on every channel; the target is
re-authorised when opened; and the tests in §2.6 exist. No checkpoint is written: a craft block, 🟡, nothing here was
run in an application.

## Guardrails
- Store one row per recipient and event, and keep read state on that row (§1.1). Never share one read flag between users by accident; a role or shared inbox is allowed only when its read semantics are stated (§1.1.6).
- Derive the badge from the stored unread rows, and refresh it on focus and reconnect (§1.3, §2.1). Never keep it only as a client counter that pushes increment.
- Check the user's preferences when sending, for every channel, with a mandatory class that cannot be muted (§1.6). Never filter only in the interface.
- Re-check access to the target when the notification is opened (§2.4). Never trust that access held when it was sent.
- Announce new items politely and keep focus where the user is (§2.3). Never move focus to a toast or announce every item loudly.
- Facts about a library are for the date stamped in `references/origin.md`; re-read before relying.

## Origin
Own craft knowledge; no permissive source on notification centres was found and read. Details in
[`references/origin.md`](./references/origin.md).
