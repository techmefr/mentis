---
name: flutter-notifications-background
description: "Use when a Flutter app schedules local notifications, receives push messages, runs a handler while the app is in the background or terminated, or is opened from outside by a link or a tapped notification: reminders that must survive DST, reboot and the iOS pending cap; exact-alarm permissions; notification permission timing; FCM foreground, background and terminated delivery; app link and universal link hosting, verification and cold-start delivery."
---

# flutter-notifications-background

Step 6 of the pipeline (`WORKFLOW.md`), for everything that reaches a Flutter app while it is not in the
user's hands: a scheduled reminder, a push message, a link. The premise: **the operating system owns the
clock, the delivery and the verification, and each of them can drop, reorder or repeat what the app thinks it
asked for, so the app keeps its own record and treats what arrives as untrusted**. Routing an entry point
into the route table is `flutter-conventions` §5; reading what a link or payload carries is
`security-hardening`; the launch path that must be ready before any of this arrives is
`flutter-startup-error-hooks`.

## When
- Writing or reviewing code that calls a notification-scheduling or push plugin.
- A reminder fires at the wrong hour after a clock change, is missing after a reboot, or stops after many were
  scheduled.
- A background or terminated-state message handler crashes or never runs.
- A link opens the browser instead of the app in the store build, or works in debug and not in release.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Local notifications: source of truth, reconcile, time zones and DST, exact alarms, the iOS cap, reboot, permission timing, background tap handlers | a reminder or alarm is scheduled or reviewed | [`01-local-notifications.md`](./references/01-local-notifications.md) |
| 2 | Push messages: platform prerequisites, permission, the three delivery states, background handler constraints | FCM or another push channel is wired or a push handler is written | [`02-push-and-background-handlers.md`](./references/02-push-and-background-handlers.md) |
| 3 | Links and tapped notifications: hosting and verifying the association files, signing fingerprints, plugin conflicts, testing, delivery order, link is not authorisation | an app link, universal link or notification route is added or "works in debug only" | [`03-links-and-entry-delivery.md`](./references/03-links-and-entry-delivery.md) |

## Output / checkpoint
Each path was exercised on a device in a build that matches what ships: a reminder across a clock change and
a reboot (§1), a push in each of the foreground, background and terminated states (§2), and an opened link
from the browser on a release-signed build (§3). An emulator run and a green unit test of the scheduling math
are not that evidence.

## Guardrails
- Never treat the operating system's pending set as the record of what is scheduled (§1).
- Never store a recurring schedule as a single UTC instant (§1).
- Never declare the permission that is granted automatically for exact alarms unless the app is an alarm,
  timer or calendar app (§1).
- Never put UI or app-state work in a background handler (§2).
- Never treat an opened link or a notification payload as proof of permission to the resource it names (§3).
- Versions: each rule names the page it comes from and the date it was read. Nothing was run while writing
  this block.

## Origin
Rewritten from a local-notifications skill and a Firebase messaging skill in MIT-licensed agent skill
repositories (design rules only, checked against vendor pages), the notification plugin's README, the Android
alarm, notification-permission and app-link pages, the Firebase Cloud Messaging for Flutter pages and the
Flutter deep-link pages, read 2026-10-08. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
