# flutter-notifications-background: origin and source stamps

> Provenance of `skills/flutter-notifications-background`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us. No notification was scheduled, no
push sent and no link opened while writing it. The earlier review proposed this as a new block; it stands
alone on main and cites only `flutter-conventions` §5 and the blocks named in the text.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Local-notifications skill of an MIT-licensed Flutter skills repository (SKILL.md, file) | MIT, read 2026-10-08 | The design rules marked as such: reconcile, port, pure math, DST storage, id derivation, handler discipline |
| `flutter_local_notifications` README on pub.dev (version 22.3.1 at the time) | BSD-3-Clause package, read 2026-10-08 | The 64-notification iOS limit, time-zone setup, background handler requirements, date-component matching, reboot rescheduling |
| Android developer page on scheduling alarms | Site terms not read; facts only, no text copied; read 2026-10-08 | Inexact versus exact, the two exact-alarm permissions, reboot, Doze |
| Android developer page on the notification runtime permission | Site terms not read; facts only; read 2026-10-08 | Default off on Android 13, timing advice, 12L behaviour |
| Firebase Cloud Messaging for Flutter, get-started and receive pages | Site terms not read; facts only, no text copied; read 2026-10-08 | APNs key, swizzling, three delivery states, background handler constraints |
| Flutter deep-linking page and the two cookbook pages (Android app links, iOS universal links) | CC-BY-3.0 text, BSD code (Flutter website repository LICENSE), read 2026-10-08 | Hosting and verification, fingerprints, default handler since 3.27, plugin conflict, testing |
| Android developer page on verifying app links | Site terms not read; facts only; read 2026-10-08 | Host file location, auto-verify, failure states, one app per domain |

## Removed in the verification pass (no page supporting them)
The Apple developer page for the 64 limit was not read (the plugin README states it, so that is the cited
source), and a numeric "about 50" iOS budget was dropped as a platform number (kept only as the unnamed
design margin in 1.5). The earlier review's "restricted exact-alarm permission" wording was replaced by the
Android page's own description. The OEM background-kill matrix and the plugin-specific boot receiver setup
were not sourced and are not in the block.

## Not verified
1. **Own guidance or design rules, flagged in the text:** everything marked "design rule" in §1, the handler
   not writing the database, treating payloads and links as untrusted, a destructive action never running
   from a link callback, idempotent delivery.
2. **The plugin's pending-request type and its schedule-mode names** were not looked up, so the id rule and
   the allow-while-idle remark rest on the Android page and on the skill's description.
3. **Licence terms of the Android and Firebase pages** were not read; only platform facts were taken and
   rewritten, nothing was copied.
4. **The fetch tool summarises pages,** so wording was not compared sentence by sentence; numbers (24 hours,
   30 seconds, 3.27, 7.0) are from those summaries.
5. **Apple documentation** for notification limits and associated domains was not read directly.

## Related blocks
`flutter-conventions` (§5), `flutter-startup-error-hooks`, `security-hardening`, `background-jobs-conventions`,
`flutter-dispose-what-you-create`.
