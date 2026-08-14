# flutter-conventions §8 — Data, storage, permissions

> Section 8 of `skills/flutter-conventions`. Read it when persistence, a secret, a platform permission. The other sections and the guardrails stay in `SKILL.md`.

1. **Sensitive data on device goes in secure storage**: auth and refresh tokens, passwords, API secrets,
   biometric-gated secrets, personal data. Plain preferences storage is not encrypted — anything in it should
   be safe to read.
2. Ordinary preferences (flags, last-selected filter) go in the preferences API, keys centralised as
   constants rather than typed as literals at three call sites.
3. On-device SQL: migrations handled explicitly on version upgrade, writes batched or wrapped in a
   transaction, conflict behaviour stated rather than defaulted.
4. **Runtime permissions handle every branch**: granted, denied, permanently denied (which needs a route to
   the system settings), and restricted. Requesting a permission at app start, before the feature needing it
   is visible, is how a user learns to deny it.
5. Remote images go through a caching image widget with a placeholder and an error widget, and a decode size
   bounded to what's displayed — a full-resolution image decoded into a thumbnail is the classic memory
   spike.
6. Where the backend is a known REST convention, generate or centralise the client once; each screen calling
   the HTTP layer by hand is where the contract drifts.
