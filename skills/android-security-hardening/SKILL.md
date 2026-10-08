---
name: android-security-hardening
description: "Use when writing or reviewing the attack surface of an Android app: a component that other apps can start, android:exported on activities services receivers and providers, intent filters that make a component public, signature permissions, an intent received through an extra and launched again (intent redirection), IntentSanitizer, URI permission flags forwarded by mistake, PendingIntent mutability and implicit intents inside it, FLAG_ONE_SHOT, deciding who the caller is, Play Integrity verdict fields checked on the server, requestHash and nonce binding, device integrity labels, and Android Keystore keys with StrongBox, user authentication and invalidation by biometric enrolment."
---

# android-security-hardening

Step 6 of the pipeline (`WORKFLOW.md`), for what an Android app exposes to other apps on the same device and what it
may believe about the device it runs on. The three sections share one premise: **everything that arrives from outside
the process (an intent, an extra, a URI, a caller, an integrity token) is input from a stranger, so each one is
declared, checked or verified on purpose, and a verdict is evidence about the environment, not a guarantee**. Server-side input, output and access-control rules are in `security-hardening`; session and token handling
is in `auth-session-conventions`.

## When
- Adding or editing an activity, service, receiver or provider, or its intent filter, in the manifest.
- Launching an intent, a URI grant or a `PendingIntent` that carries data a caller supplied.
- Using the device's integrity as input to a decision, or storing a key on the device.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Components and callers: explicit `exported`, intent filters, signature permissions, intent redirection, URI grant flags | a manifest component is added or an intent is forwarded | [`01-components-and-intents.md`](./references/01-components-and-intents.md) |
| 2 | `PendingIntent`: mutability, explicit targets, single use | a notification, alarm or widget hands out a `PendingIntent` | [`02-pending-intents.md`](./references/02-pending-intents.md) |
| 3 | Device integrity and keys: Play Integrity verdicts on the server, Keystore, StrongBox, authentication-bound keys | a decision depends on the device or on a stored secret | [`03-integrity-and-keystore.md`](./references/03-integrity-and-keystore.md) |

## Output / checkpoint
The merged manifest was read (the library manifests included), every component shows an explicit `exported` value
and each exported one names its reason (§1); each forwarded intent is sanitised or resolved against an allow-list (§1);
every `PendingIntent` has an immutability flag and an explicit target (§2); every integrity decision compares the verdict's
request details first (§3). A manifest read only in the source tree, without the merge, is not verified.

## Guardrails
- Never leave `exported` implicit, and never export a component without a stated reason (§1).
- Never launch an intent taken from an extra without sanitising it or checking where it resolves (§1).
- Never use `FLAG_MUTABLE` or an implicit intent in a `PendingIntent` unless the field is meant to be filled in (§2).
- Never act on an integrity verdict whose request details (package, request binding, timestamp) were not compared with
  the original request (§3).
- This block states Android behaviour as of the developer.android.com pages read on the date in
  [`references/origin.md`](./references/origin.md); no code was run while writing it.
- Raising `targetSdk` or changing the signing configuration is the user's step; this block names it and stops.

## Origin
Rewritten from the Android developer pages on `android:exported`, intent redirection, pending intents, Play Integrity
verdicts and the Keystore (read 2026-10-08). 🟡: never run by us; meant to be folded into `security-hardening` when
PR 118 lands; open points are in [`references/origin.md`](./references/origin.md).
