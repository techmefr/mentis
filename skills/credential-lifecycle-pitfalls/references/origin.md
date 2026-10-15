# credential-lifecycle-pitfalls: origin and source stamps

> Provenance of `skills/credential-lifecycle-pitfalls`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation, never run by us. Every file below was re-read in full on
2026-10-15 before a rule was taken from it, and each repository's LICENSE file was read again. The numbers
in the table are the ones the sources state at the commits shown; they are version-bound and meant to be
re-read, not copied.

## Sources (all read 2026-10-15, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Copenhagen Book (`pilcrowonpaper/copenhagen`, commit `fb7eb3a`), pages `password-authentication.md`, `password-reset.md`, `email-verification.md`, `mfa.md`, `server-side-tokens.md`, `random-values.md` | MIT (LICENSE file, copyright 2024 pilcrow) | Password validation, hashing order and minimum parameters (Argon2id 19456 KiB / 2 / 1, scrypt 16384 / 16 / 1 / 64, bcrypt at least 10), throttling, enumeration, reset and verification token rules and lifetimes, TOTP and recovery codes, token entropy, hashed storage, random integers |
| libsodium documentation (`jedisct1/libsodium-doc`, commit `edebe69`), `password_hashing/default_phf.md` and `password_hashing/README.md` | ISC (LICENSE file, copyright 2014-2026 Frank Denis) | The string API, stored parameters, `crypto_pwhash_str_needs_rehash` return values, the parameter-choosing method (opslimit 3, measure), the 64 MiB interactive figure, passwords as encryption keys, plaintext in memory |

## Removed in the verification pass
1. **A single "recommended parameters" table with one hash at one figure.** The two sources give different
   methods and different numbers; §1.6 states both and says they answer different questions instead of
   picking one.
2. **"Equal timing against enumeration" as a flat rule.** The source says protection against timing
   attacks is hard and to attempt it only when strictly required; §1.12 keeps that qualification.
3. **UUIDv4 as a token** is not recommended and kept only with the source's caveat (§3.6).
4. **The Copenhagen WebAuthn page** (item 11 of the review) was not used here; the review notes its Go
   sample has an inverted `rpIdHash` check, and WebAuthn is out of scope for this block.
5. **The OWASP Password Storage Cheat Sheet,** which the Copenhagen Book links for details, is CC-BY-SA and
   was neither read nor used.

## Not verified
1. **Own guidance, flagged as such in the text:** the choice of a hashing parameter set on our hardware
   (§1.6, the method is libsodium's, the instruction to record it is ours), upgrading a hash inside the
   login request (§1.8, the mechanism is libsodium's), the lightweight handling of managed-language
   plaintext (§1.13), the TOTP library and constant-time compare (§2.13), the same-rules-for-short-codes
   point (§3.9), and the deduction that a hash needs no slow function because a token is random (§3.4,
   which the source states).
2. **Parameter values and lifetimes** (hash parameters, 15 minutes to 24 hours, 10 attempts an hour,
   40-bit recovery codes, 160-bit TOTP secret, 112-bit tokens) are as stated by the sources at the commits
   above. They are minimums that age and were not checked against any current standard.
3. **The `zxcvbn` and haveibeenpwned services** were not run or read; only the Copenhagen Book's description
   of them is used. Whether sending a five-character hash prefix to a third party is acceptable for your
   data policy is a decision for the project.
4. **The libsodium AEAD pages and the scrypt page** were not read; §1.14 relies only on the sentence in
   the password-hashing page.
5. **RFC 4226 and RFC 6238** (HOTP, TOTP) were not read.

## Related blocks
`skills/auth-session-conventions`, `skills/jwt-verification`, `skills/oauth-oidc-client-pitfalls`,
`skills/security-hardening`.
