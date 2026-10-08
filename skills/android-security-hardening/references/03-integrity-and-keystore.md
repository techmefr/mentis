# android-security-hardening §3 — Device integrity and keys

The Android developer pages "Integrity verdicts" of the Play Integrity API (last updated 2026-10-06) and "Android
Keystore system" (last updated 2026-03-06), read in full as page text on 2026-10-08.

## 3.1 Play Integrity verdicts
1. **The verdict is plain-text JSON** with `requestDetails`, `accountDetails`, `appIntegrity`, `deviceIntegrity` and
   `environmentDetails`; field order is not guaranteed. The page describes your server using the decrypted, verified
   verdict to decide how to proceed with an action.
2. **Check `requestDetails` before any other field.** The page's example compares `requestPackageName` with the expected
   package and the request binding with the one you sent (`requestHash` for standard requests, `nonce` for classic ones),
   and checks that the timestamp is recent. It notes that `requestPackageName` might be spoofed in the middle of the request, which
   is why the binding is compared too.
3. **The device label list is `deviceRecognitionVerdict`.** By default it contains `MEETS_DEVICE_INTEGRITY` (a genuine
   certified Android device; on Android 13 and later with hardware-backed proof of a locked bootloader and a
   certified OS image) or is empty (signs of attack or compromise, or not a physical device that passes the checks).
4. **Optional labels need opt-in:** `MEETS_BASIC_INTEGRITY` (basic checks; the device may be uncertified) and
   `MEETS_STRONG_INTEGRITY` (certified with a recent security update; on Android 12 and lower it proves boot
   integrity only, so the page recommends also reading the SDK version in `deviceAttributes`). On Android 13 and
   later these two are returned only when the app is licensed. `MEETS_VIRTUAL_INTEGRITY` appears for apps released to
   Google Play Games for PC.
5. **`appLicensingVerdict` is `LICENSED`, `UNLICENSED` or `UNEVALUATED`,** and **`appRecognitionVerdict` is
   `PLAY_RECOGNIZED`, `UNRECOGNIZED_VERSION` or `UNEVALUATED`.** `UNEVALUATED` means a necessary requirement was missed
   (an untrustworthy device, an app version unknown to Play, a user not signed in), so it is not a pass.

## 3.2 Keystore keys
1. **Key material never enters the app process,** so a compromised process can use the keys but not extract them. A
   key can also be bound to secure hardware (TEE or secure element), when the hardware supports the algorithm, block
   mode, padding and digest. Check where a key lives with `KeyInfo`: `getSecurityLevel()` for an app that targets
   Android 10 or later, `isInsideSecurityHardware()` for Android 9 and lower.
2. **StrongBox (Android 9, API 28 and later) is a KeyMint backed by a secure element with its own CPU, storage and
   random-number generator.** It supports only a subset: RSA 2048, AES 128 and 256, ECDSA and ECDH P-256, HMAC-SHA256
   and Triple DES. It is slower, more constrained and supports fewer concurrent operations, and the page says most apps do
   not need it.
3. **Check `FEATURE_STRONGBOX_KEYSTORE`, then ask for it with `setIsStrongBoxBacked(true)`** (generation, or the
   key-protection builder for import). If StrongBox does not support the algorithm or size, a
   `StrongBoxUnavailableException` is thrown and the page says to generate or import the key without the call.
4. **Authorisations cannot be changed after generation.** Require user authentication for key use only when a compromise of your
   process after key creation must not bypass it; `setUserAuthenticationParameters()` sets either a validity duration after
   authentication or per-operation authorisation through `BiometricPrompt.authenticate()`, with strong biometrics, the
   lock-screen credential or both. Call `canAuthenticate()` to see whether the user has set the credential up.
5. **A key that supports only biometrics is invalidated by default when a new biometric enrolment is added;**
   `setInvalidatedByBiometricEnrollment(false)` keeps it valid. Design the re-creation path.
6. **StrongBox also supports key attestation** (the page states it; how to verify an attestation is on a page not
   read).
