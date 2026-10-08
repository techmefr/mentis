# android-security-hardening: origin and source stamps

> Provenance of `skills/android-security-hardening`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation, never run by us. No app was built and no device was used.

**Fold-in note.** Meant to be folded into `security-hardening` (an Android reference) when PR 118 lands.

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

## Not verified
1. **Manifest default of `exported` per component type and the Android 12 rule** were not read on any page; do not
   state them.
2. **Permission protection for exported components** (signature level) was not read on a page.
3. **Where to decrypt a Play Integrity token** (on your server or by Google) is on the standard-request pages, which
   were not read.
4. **How an app proves the caller's identity** (package signature checks) was not sourced and is not written.
5. **Android 16 default redirection protection** is one paragraph; its exact scope was not read.

## Related blocks
`security-hardening` (server-side input, output and access control), `auth-session-conventions` (sessions and
tokens).
