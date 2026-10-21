# android-security-hardening: origin and source stamps

> Provenance of `skills/android-security-hardening`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation, never run by us. No app was built and no device was used.

**Overlap note.** Overlaps with `skills/security-hardening` (2026-10-19); cross-referenced, not merged.

## Sources (read 2026-10-08, rewritten, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| developer.android.com: android:exported, intent redirection, pending intents, Play Integrity verdicts, Android Keystore | Android docs: CC BY 4.0 for text, code Apache 2.0 (facts only, rewritten) | §1, §2, §3 |

No third-party repository was used. The pages were downloaded and read as page text, and every rule was compared with
that text in a second pass.

## Re-verified against page text in the second pass
Exported attribute meaning and default drift; the intent redirection mitigations, the two named mistakes, the
Android 16 default protection and opt-out method, the StrictMode condition; PendingIntent mutability and one-shot
rules; Play Integrity request-details check, field names, label meanings and opt-in conditions; Keystore extraction
protection, StrongBox requirements and algorithm list, the unavailable-exception fallback, authentication modes and
biometric invalidation.

## Removed or corrected in the second pass
- **Removed:** "from Android 12 a component with an intent filter is exported and the manifest must say true or false" and
  "protect an exported component with a signature-level permission": neither is on the exported page; the fetch summary
  had added them.
- **Removed:** "the verdict must be decrypted and verified on the server because only that prevents forgery": the page
  only says the server can use a decrypted, verified verdict; the reasons were not on it.
- **Corrected:** the label field is `deviceRecognitionVerdict`; `MEETS_VIRTUAL_INTEGRITY` is for Play Games for PC, not
  an opt-in label; the optional labels are withheld for unlicensed apps on Android 13 and later.
- **Corrected:** the attestation sentence (the page's recommendation concerns a wrap-key example only).
- **Removed earlier:** broadcast receiver and provider URI-grant rules (those two pages returned 404), root and
  emulator detection recipes, pinning, obfuscation.

## Re-read 2026-10-20
The activity-element manifest page (CC BY 4.0 text) was re-read: default false when there are no intent filters; true needed for other apps to start an activity that has filters; permissions are named as a further way to limit callers. The first 100000 characters were read; the Android 12 explicit-declaration rule was not seen.

## Second pass, 2026-10-20
Read as page text, facts only: activity, provider, service and receiver manifest element pages; Android 12 and Android 16 behaviour-changes pages; defining-permissions page; platform security-tips page; Play Integrity standard-request page. Confirmed or added: defaults per component type, the Android 12 explicit-export install failure, permission attributes on components, signature protection level, strict intent matching on Android 16 (separate from the redirection protection), Play Integrity server decoding, request-hash binding and replay behaviour.

## Not verified (updated 2026-10-20)
1. (Resolved 2026-10-20: defaults per component type and the Android 12 rule are on the element and behaviour-changes pages, see §1.1. The activity page itself gives no default for the with-filters case.)
2. (Resolved 2026-10-20: component permission attributes and signature protection are on the element and permissions pages.)
3. (Resolved 2026-10-20 for standard requests: decoding is a call to the platform from your backend. Classic requests and any local-decryption option were not read.)
4. **How an app proves the caller's identity** is touched only by the security-tips page (calling-permission check, signature comparison of the calling package); no page was read that details the procedure, so no recipe is written.
5. **Android 16 default redirection protection** is still one paragraph on the redirection page; its scope was not read. The Android 16 behaviour-changes page describes a different, opt-in feature (strict intent matching).

## Related blocks
`security-hardening` (server-side input, output and access control), `auth-session-conventions` (sessions and
tokens).

Independent verification 2026-10-21: 26 checked, 26 matched, 0 corrected, 0 unverified
