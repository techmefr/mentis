# flutter-conventions §8 — Data, storage, permissions

> Section 8 of `skills/flutter-conventions`. Read it when persistence, a secret, a platform permission. The other sections and the guardrails stay in `SKILL.md`.

1. **Sensitive data on device goes in secure storage**: auth and refresh tokens, passwords, API secrets,
   biometric-gated secrets, personal data. Plain preferences storage is not encrypted — anything in it should
   be safe to read. On a rooted or jailbroken device, and in a device backup, the preferences file is a plain
   file; the threat model that matters here is a lost phone and a second-hand one.
2. **A secure read can fail, and failing is not crashing.** The platform keystore is cleared by events the
   app does not control — a biometric re-enrolment, a restore onto different hardware, an OS upgrade gone
   sideways — so a token that was written successfully can be unreadable later. Treat the failure as
   "not signed in" and re-authenticate; treating it as impossible produces a crash loop on launch that no
   reinstall message explains.
3. **Logging out clears the device.** A token, a cached profile, a downloaded document or a rendered
   thumbnail left behind is available to whoever holds the phone next, and on a shared or company device
   that is a different person. Enumerate what the session wrote and remove it in one place, so the next
   feature that caches something has somewhere obvious to register it.
4. **Anything cached to disk is a copy outside the deletion path.** An API response, an image, an exported
   file — the app promises that deleting a record deletes it, and the cache quietly disagrees. Decide each
   cache's lifetime and bound its size, or the app grows until the OS evicts it at the least convenient
   moment.
5. Ordinary preferences (flags, last-selected filter) go in the preferences API, keys centralised as
   constants rather than typed as literals at three call sites. A mistyped key does not fail — it reads as
   absent, so the setting silently reverts to its default and the bug report is "it forgets my choice".
6. **A renamed key orphans its value.** Renaming or retyping a stored preference leaves the old entry on
   every existing installation, so returning users get the default while new ones get the intended
   behaviour — a difference that never reproduces on a fresh install. Version the stored shape and migrate
   it, or accept the reset deliberately.
7. On-device SQL: migrations handled explicitly on version upgrade, writes batched or wrapped in a
   transaction, conflict behaviour stated rather than defaulted. An unstated conflict policy resolves
   differently under a retry than it did in the happy path, which is how a sync ends up with duplicates.
8. **A migration is tested from a real old database.** The fresh-install path always passes, so testing only
   that proves nothing about the users who already have data — and a failed migration on a released version
   is unrecoverable from the app's side, because the data it needed is what broke.
9. **A heavy read blocks the frame.** A large query, a JSON parse of a big response or an image encode on
   the main isolate drops frames for as long as it runs, and the user reads that as the app freezing. Move
   the work off the main isolate; that is also where §2.4's "keep `build` free of work" ends up leading.
10. **Storage failures are real failures.** The disk can be full, the file can be locked, the database can be
    corrupt. A `catch` that swallows the write leaves the user believing something was saved, which is worse
    than the error dialog — and a `catch` that reports it (§9.12) is how you find out it happens at all.
11. **Runtime permissions handle every branch**: granted, denied, permanently denied (which needs a route to
    the system settings), and restricted. Requesting a permission at app start, before the feature needing it
    is visible, is how a user learns to deny it.
12. **The system prompt is often a one-time chance.** Several permissions can only be asked once per install,
    so a prompt fired before the user understands why is a permanent no, recoverable only by a trip to the
    settings app that most people will not make. Explain in the app first, then ask — and ask at the moment
    the feature is used.
13. **Check at the point of use, not once at startup.** A permission can be revoked from the settings app
    while the app is in the background, and some platforms downgrade a grant to "only this time". Code that
    checked at launch and cached the answer then calls into a platform API that refuses, which surfaces as
    an unexplained failure inside an unrelated feature.
14. **Ask for the narrowest thing that works.** Coarse location rather than precise, a single-photo picker
    rather than the whole library, the foreground variant rather than the background one — the narrow
    request is more likely to be granted, cheaper in battery, and materially easier to justify in a store
    review. A broad permission requested for a small feature is refused by both the user and the reviewer.
15. Remote images go through a caching image widget with a placeholder and an error widget, and a decode size
    bounded to what's displayed — a full-resolution image decoded into a thumbnail is the classic memory
    spike. In a scrolling list it is the classic crash: a dozen of them decoded at once exhausts the memory
    the OS was willing to give the process.
16. Where the backend is a known REST convention, generate or centralise the client once; each screen calling
    the HTTP layer by hand is where the contract drifts. The centralised client is also the only place a
    token refresh can be done once: five parallel requests meeting an expired token each trigger a refresh,
    and four of the five new tokens are invalidated by the fifth, logging the user out in the middle of
    using the app.
17. **Never log a credential, and never attach one to a report.** A token in a debug print reaches the
    device log, which other tooling can read, and a header captured into a crash report leaves the device
    entirely (§9.14). This is the one that gets added while debugging and stays.
18. **A parse moved off the main isolate becomes invisible to a widget test.** Point 9 is right and it
    moves the work outside the test's clock: a result coming back from another isolate is delivered
    outside the zone the widget-test harness runs in, so the future the widget is awaiting never completes
    and the test sits there until the suite's timeout — a hang rather than a failure, naming nothing. The
    seam a widget test fakes therefore has to sit *above* the hop, at the repository rather than at the
    file or the asset bundle; where the hop itself is what needs exercising, that is a plain unit test's
    job, or it needs the harness's real-async escape hatch for that one await (§10.7).
