# crypto-usage-pitfalls §1 — Keys and calls

> Section 1 of `skills/crypto-usage-pitfalls`. Read it when a key is created or a cryptographic call is
> written. Sourced from the libsodium documentation (commit `edebe69`), pages `quickstart/README.md`,
> `password_hashing/README.md`, `secret-key_cryptography/aead.md`, `secret-key_cryptography/encrypted-messages.md`
> and `usage/README.md`, read 2026-10-16. Function names are libsodium's; a binding may rename them. Sentences
> marked "own guidance" are ours.

1. **Use the high-level API and an authenticated construction.** The documentation says to always use the
   high-level API when one is available. It describes the bare stream-cipher call as completely insecure on its own: an attacker can flip
   chosen bits without knowing the key, or replace the ciphertext with null bytes and make the original keystream
   come out. For real encryption it names `crypto_secretbox`, `crypto_aead` and `crypto_secretstream`, each of
   which adds and verifies an authentication tag. For one message that fits in memory: make a key with
   `crypto_secretbox_keygen()`, a nonce with `randombytes_buf()`, encrypt with `crypto_secretbox_easy()`, and
   store the nonce with the ciphertext (a nonce is not secret).
2. **A password is not a key; turn it into one with a password hash.** A password has a small, skewed space and a
   key does not. The documentation says that if an application must use a password as a secret key it should call
   `crypto_pwhash()` first, a deliberately CPU-intensive and memory-hard function, and that native keys from a
   `*_keygen()` function should always be preferred. Never pass password bytes, or a plain hash of them, to a
   cipher.
3. **Keep what you need to derive the key again.** The password-hashing page says the same password with the same
   parameters always gives the same output and the same password with a different salt gives a different one. Own
   guidance: so the salt and the cost parameters travel with the ciphertext (they are not secret), and a file
   encrypted with a password is "derive key, then secretstream" with both stored in the header. Choosing the
   parameters and storing a login password are in `credential-lifecycle-pitfalls` §1.
4. **Initialise the library and check every return value.** `sodium_init()` returns `0`, `1` if already
   initialised and `-1` on failure, and the library is not safe to use after a failure. Functions returning an
   `int` return `0` on success and `-1` on error; functions returning a pointer return `NULL` on error. Some
   outcomes must be read, such as the result of verifying an authentication token, and those functions carry the
   `warn_unused_result` attribute: a compiler warning about them is not to be ignored. The documentation says to
   check unconditionally even where a variant cannot fail in practice (AES-GCM can fail on message size limits,
   XChaCha20 cannot, in theory), because it is cheap and the function may be swapped later.
5. **A failed decryption means discard.** The documentation says decryption functions return an error code when
   a tag does not match (corrupted, tampered with or made without the key) and that the application must discard
   the data. Own guidance: use none of the partial plaintext, and do not tell the caller which check failed.
6. **Do not add a signature to detect tampering with an encrypted message.** The FAQ says no: the tag in
   `crypto_box`, `crypto_secretbox`, `crypto_seal`, `crypto_secretstream` and `crypto_aead` already makes a
   modified message fail, and a signature is for letting many parties verify non-secret data with a public key.
   If you truly need both, it prefers distinct key pairs for signing and encryption over converting one into the
   other, noting that the two keys often have different lifetimes (encryption keys rotate often, signing keys are
   long-term).
7. **Use one key per direction.** If two parties share one key and each increments its own counter from the same
   starting value, two different messages can get the same nonce. The documentation's answer is separate keys
   for each direction, and the key-exchange API (`crypto_kx`) yields exactly two.
8. **Put what matters about the message in the authenticated additional data.** The additional-data parameter is
   authenticated but not stored in the ciphertext. The documentation's uses: a version number, a timestamp or a
   counter so that old messages are discarded and replay is prevented. For files, secret metadata belongs
   inside the encrypted data and non-secret metadata can be additional data.
9. **Decide whether the recipient can be forced onto another key.** With AES-GCM and ChaCha20-Poly1305 several
   keys that make the same (ciphertext, tag) pair verify can be computed efficiently. Decrypting with the wrong
   key still yields a different message and does not break the original, but it matters if an attacker can make
   the recipient choose the key. The documentation's options: use AEGIS, or prepend `H(key, nonce ||
   ciphertext_tag)` (it suggests `crypto_auth`) and verify it before decrypting, including the additional data
   in the hash when the attacker controls it.
10. **Decision for choosing a construction.** The documentation says that with hardware AES acceleration AEGIS-256
    is the safest choice (it needs libsodium 1.0.19 or later) and otherwise XChaCha20-Poly1305-IETF, and that the
    rest exist for interoperability with other libraries. AES256-GCM needs hardware support and has no software
    fallback. Own guidance: default to XChaCha20-Poly1305-IETF, or `crypto_secretstream` for files and ordered
    streams (§2.9), and pick another only for interoperability, with the limits in §2 in hand.
