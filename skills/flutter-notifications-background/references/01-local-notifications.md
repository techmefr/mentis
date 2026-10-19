# flutter-notifications-background §1 — Local notifications

Plugin facts are from the README of `flutter_local_notifications` as shown on its pub.dev page on 2026-10-08
(version 22.3.1 then). Android facts are from the Android developer pages on scheduling alarms and on the
notification runtime permission, read the same day. Design rules (marked) come from an MIT-licensed skill
and are our judgement on top of those facts, not statements of the vendor pages.

## 1.1 The record and the reconcile
1. **Keep the schedule in the app's own database and treat the operating system's pending set as a
   disposable cache.** Two documented facts make the cache unreliable: Android cancels all alarms when the
   device shuts down, and iOS keeps only the 64 notifications that were last set (plugin README, for iOS
   versions newer than 9). The database can always rebuild what the cache lost. (Design rule.)
2. **Every scheduling change goes through one function that computes the desired set from the database and
   makes the cache match it,** cancelling what is stale and scheduling what is missing. Feature code never
   calls the plugin's schedule or cancel directly, because that path cannot be made idempotent. Call it on
   foreground, on every change to a reminder, after a restore from backup, and when the exact-alarm
   permission changes (§1). (Design rule.)
3. **The plugin is imported in exactly one file, behind a small interface** of schedule, cancel, cancel-all
   and list-pending, so the scheduling math and its tests never touch the plugin. (Design rule.)
4. **The scheduling math is pure and takes the current time as a parameter,** never reading the clock itself,
   so a test can put "now" on either side of a clock change. (Design rule.)
5. **The foreground reconcile is the backbone.** The reboot receiver, background ticks and permission toggles
   are best effort; the next foreground pass is the only point where a dropped reminder is guaranteed to be
   noticed. (Design rule.)

## 1.2 Identity of a scheduled item
**Derive the id deterministically from the entity, the occurrence and the resolved fire time.** An id that
ignores the fire time means a reminder moved from 09:00 to 14:00 keeps the same id and is skipped by a
reconcile that compares ids only, so it fires at the old time. The reasoning assumes the pending list exposes
the id but not the fire time; that assumption was not checked against the plugin's pending-request type.
(Design rule.)

## 1.3 Time zones and DST
1. **Store a recurring schedule as a wall-clock time plus a recurrence rule, and resolve it to a zoned
   instant in the local zone when scheduling.** A stored UTC instant sits an hour off the wall clock after
   each daylight-saving change. A true one-off moment may stay a UTC instant. (Design rule.)
2. **The plugin needs the time-zone database initialised before any zoned scheduling,** and the README says
   a local location may optionally be set as the default with `setLocalLocation`. Set it once at startup from
   the device's zone name, before the first scheduling call (README for the call; the "at startup" placement
   is ours and belongs in the launch path of `flutter-startup-error-hooks`).
3. **The plugin's date-component matching parameter schedules a daily or weekly repeat** from a single call
   (README). Use it for a genuinely calendar-fixed repeat; use one-shot items recomputed by the reconcile for
   anything the rule can change.

## 1.4 Exact alarms
1. **Default to inexact scheduling.** The Android page says most apps can use inexact alarms and that exact
   alarms are for apps whose core function depends on a precise time, such as an alarm clock or calendar app,
   because they can significantly affect battery life.
2. **The two exact-alarm permissions differ.** The one the user grants is revocable by the user or the
   system, is not pre-granted to fresh installs that target Android 13, and has a runtime check
   (`canScheduleExactAlarms`). The one granted automatically cannot be revoked and is limited by Google Play
   policy to a narrow set of apps (the Android page). Declare the automatic one only for an alarm, timer or
   calendar app; everything else declares the user-granted one or none.
3. **Exact scheduling is an opt-in with a silent fall back to inexact** when the check fails, and the
   permission state change broadcast is the cue to run the reconcile again (the Android page describes the
   broadcast and says to re-check and reschedule).
4. **Doze defers alarms** unless an exact alarm or an allow-while-idle inexact alarm is used (Android page);
   so "inexact" in the plugin's schedule mode is chosen with the allow-while-idle variant when a reminder must
   still arrive on an idle device. (The mode names were not looked up here.)

## 1.5 The iOS cap
Keep the number of pending items under 64. Sort the future occurrences by time, schedule the nearest ones
only, and refill on every foreground. The README says nothing about an error for the extra items, so an
item beyond the cap is simply not kept; the margin below 64 (an app that wants a spare) is a design choice,
not a documented number.

## 1.6 Reboot
Alarms are cancelled at shutdown (Android page). The page's recipe is a boot-completed receiver that
re-creates them; the plugin states it detects the reboot so that it can reschedule (README). That covers what
the plugin scheduled; it does not make the foreground reconcile of §1 optional.

## 1.7 Permission to show notifications
1. **On Android 13 and later notifications are off by default for a new install** and need the runtime
   permission (the Android permission page).
2. **Ask in a context where the reason is clear,** such as when the user turns on reminders, not at app
   start; and check that notifications are enabled before relying on them (both are the page's own
   best-practice list).
3. **An app targeting Android 12L or lower is asked by the system,** and one "Don't allow" is permanent until
   reinstall (same page); so target the newer level and own the timing.

## 1.8 Tap and action handlers in the background
1. **The background response handler is a top-level or static function marked with the VM entry-point
   pragma,** or tree-shaking can remove it; it runs, except on Linux, in a separate isolate with limited
   plugin access (README).
2. **A handler does not write the app database.** Record a small intent (or nothing) and let the next
   foreground reconcile do the work, so two isolates are not opening the same store. (Design rule, ours.)
3. **A tap carries a typed route payload that is untrusted input like a link;** the screen it opens loads its
   own data from identifiers (`flutter-conventions` §5) and §3 of this block applies.
