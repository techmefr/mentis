---
name: crypto-usage-pitfalls
description: "Use when code calls a cryptography library to encrypt, authenticate, derive keys or generate random values (libsodium or a binding of it, AEAD ciphers, file encryption with age): where a key comes from, return values that must be checked, nonce and message-count limits per construction, ciphertext size caps and chunking, rekeying, unbiased random integers, key-derivation contexts, length hiding and the tags age embeds for some recipients."
---

# crypto-usage-pitfalls

A defensive block for the code that uses cryptography, not the code that invents it. The library does the
mathematics; what goes wrong in application code is where the key came from, whether an error was read, how
many messages one key was asked to protect and what the randomness was. The sources are the libsodium
documentation and the age README, and the figures in this block are theirs, dated, and version-bound: re-read
them before a design depends on a limit. Passwords for login (store and verify) are in
`skills/credential-lifecycle-pitfalls`; signed tokens are in `skills/jwt-verification`; the general rule against
designing your own construction holds throughout. Nothing here is a substitute for a cryptographer's review of a
protocol.

## When
- A diff encrypts or decrypts data, files, messages or backups, or authenticates a message with a key.
- A key is derived from a password, from another key or from a random source.
- A nonce, an initialisation vector, a salt or a random integer is generated.
- A system encrypts many messages under one long-lived key, or a stream, a file or a datagram protocol.
- Files are encrypted to people or devices with age.

## Steps

**Read only the section the diff touches.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Keys and calls: key source, high-level API, return values, signing, key commitment, choosing a construction | a key is made or a cryptographic call is written | [`01-keys-and-calls.md`](./references/01-keys-and-calls.md) |
| 2 | Nonces, limits and rekeying: safe nonce choices, message and size limits, chunking, failure limits, sequences | many messages share a key, a message is large, or messages form a sequence | [`02-nonces-limits-rekeying.md`](./references/02-nonces-limits-rekeying.md) |
| 3 | Randomness, derivation and recipients: random integers, RNG after fork or snapshot, KDF contexts, padding, age | a random value, a subkey, a ciphertext length or an age recipient matters | [`03-randomness-derivation-age.md`](./references/03-randomness-derivation-age.md) |

## Output / checkpoint
For each cryptographic use in the diff: where the key comes from and how it is stored, which construction and
why, how each nonce is chosen and the number of messages and the largest message the key will see, what is
done on a failed decryption, and how the key is rotated. Evidence is a test that corrupts one byte of a
ciphertext and sees the decrypt call refuse it, and a count of the messages one key is expected to protect
compared with the limits in §2.

## Guardrails
- Never derive an encryption key from a password with anything but a password hash, and never feed a password
  to a cipher directly (§1.2).
- Never ignore a return value from a cryptographic call, including the ones that "cannot fail" (§1.4).
- Never use a bare stream cipher or a hash as encryption; use an authenticated construction (§1.1).
- Never encrypt under random nonces beyond the message count for the construction, and never reuse a
  (key, nonce) pair (§2.1, §2.3).
- Never decrypt a ciphertext of unbounded size, and never keep serving a peer that keeps failing
  authentication (§2.5, §2.6).
- Never take a random integer with a modulo on a small random value (§3.1).
- Never generate keys or nonces in an image that is cloned or snapshotted afterwards (§3.3).
- Do not paste a real key, nonce set or ciphertext into a prompt, a fixture or a log.

## Origin
Rewritten from the libsodium documentation (ISC) and the age README and source comments (BSD-3-Clause), read
2026-10-16. The full provenance, library versions, what was removed and what is our own guidance are in
[`references/origin.md`](./references/origin.md). 🟡: never run by us.
