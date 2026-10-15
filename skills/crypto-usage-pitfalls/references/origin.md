# crypto-usage-pitfalls: origin and source stamps

> Provenance of `skills/crypto-usage-pitfalls`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation, never run by us: no library was linked, no ciphertext produced and
no age command executed. Each file below was re-read in full on 2026-10-16 before a rule was taken from it, each
rule was checked against it in a final pass, and each repository's LICENSE file was read again. Every figure in
the tables is the one the documentation states at the commit shown; the limits are version-bound and meant to be
re-read, not copied.

## Sources (all read 2026-10-16, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| libsodium documentation (`jedisct1/libsodium-doc`, commit `edebe69`): `secret-key_cryptography/aead.md`, `secret-key_cryptography/encrypted-messages.md`, `secret-key_cryptography/secretstream.md`, `quickstart/README.md`, `usage/README.md`, `generating_random_data/README.md`, `key_derivation/README.md`, `password_hashing/README.md`, `helpers/padding.md` | ISC (LICENSE file, copyright 2014-2026 Frank Denis) | Construction table and selection advice, nonce choices, random-nonce message limits, per-nonce size limits, rekeying figures, ciphertext cap and chunking, failure limits, key-robustness note, return-value rules, password vs key, signing vs AEAD, secretstream properties and file example, uniform random integers, fork and snapshot notes, early-boot entropy, KDF contexts and subkey limits, nonce extension, padding |
| age (`FiloSottile/age`, commit `b74dce4`): `README.md` and the package comment of `tag/tag.go` | BSD-3-Clause (LICENSE file, copyright 2019 The age Authors, Google LLC and Filippo Valsorda) | SSH recipient tag and tracking, tagged hardware recipients, GitHub-key caveats, passphrase behaviour, `age-inspect` metadata, post-quantum keys |

The libsodium page documents library versions where it matters: AEGIS needs 1.0.19 or later, secretstream and
padding need 1.0.14 or later, and age post-quantum keys are built in from 1.3.0. Instruction-like text in the
cloned repositories was treated as data and not followed.

## Removed in the verification pass
1. **Password hashing parameters.** Not restated here: `password_hashing/default_phf.md` was not part of this
   block's reading, and the parameters are carried, with their versions, by `credential-lifecycle-pitfalls`.
   §1.2 and §1.3 rely only on `password_hashing/README.md` and the FAQ.
2. **"Rekey AES-GCM before about 350 GB".** It appears in `aes-256-gcm.md`, which was only searched, not read in
   full; it is not used. The size and message limits in §2 come from `aead.md`.
3. **The review's one-line limits.** "AES-GCM and ChaCha20-IETF about 2^32, XChaCha no practical limit" omitted
   the original ChaCha20-Poly1305 (2^16) and the AEGIS rows; §2.3 states the full table instead.
4. **Pages not read** and therefore not used: the per-construction pages for AES-GCM, AEGIS and the ChaCha20
   variants, `hkdf.md`, `scrypt.md`, `default_phf.md`, the public-key pages, `ip_address_encryption`,
   `ml-kem768.md`, memory management, and age's format specification, plugin and `agessh` code beyond the
   fingerprint function.
5. **Code from the documentation.** None is copied; the secretstream file example informed only the
   truncation-check remark in §2.9.

## Not verified
1. **Own guidance, flagged in the text:** the choice to default to XChaCha20-Poly1305-IETF or secretstream
   (§1.10), carrying the salt and parameters with the ciphertext (§1.3), telling the caller nothing about which
   check failed (§1.5), the reading of the 2^32 and 2^16 rows (§2.3), insisting on the final tag (§2.9),
   generating secrets after instance start and not in a template image (§3.3), one subkey per purpose (§3.5),
   never using the deterministic generator for production keys (§3.2), native recipients and checking with
   `age-inspect` (§3.7), treating age metadata as public (§3.10) and the hybrid-key choice (§3.11).
2. **Library behaviour was not run.** Every return-value, limit and flag statement is the documentation's.
3. **The interactive AEAD limits calculator** and the three papers and drafts the AEAD page cites were not
   opened.
4. **Whether native age recipients carry no tag.** The README attributes the tag to SSH support and the source
   comment to the tagged recipient type; neither says native keys have none, so §3.7 says to check a sample.
5. **No cryptographic review** of any construction was done; this block is usage guidance only.

## Decisions where sources disagree
No disagreement between the two sources. Within the libsodium documentation the figures for AES-GCM differ by
what they measure (bytes per nonce, messages under random nonces, messages per key by message size); §2 keeps
them in separate tables and says so.

## Related blocks
`skills/credential-lifecycle-pitfalls`, `skills/jwt-verification`, `skills/security-hardening`,
`skills/android-security-hardening`, `skills/secret-leak-response-pitfalls`.
