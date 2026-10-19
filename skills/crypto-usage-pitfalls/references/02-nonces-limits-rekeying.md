# crypto-usage-pitfalls §2 — Nonces, limits and rekeying

> Section 2 of `skills/crypto-usage-pitfalls`. Read it when many messages share a key, a message is large, or
> messages form a sequence. Every figure is from the libsodium documentation at commit `edebe69`, read
> 2026-10-16 (`secret-key_cryptography/aead.md`, `encrypted-messages.md`, `secretstream.md` and
> `key_derivation/README.md`). The limits are version-bound and assume untruncated 128-bit or 256-bit tags; the
> documentation points to an interactive limits calculator for other sizes. Sentences marked "own guidance" are
> ours.

1. **Every message needs a unique (key, nonce) pair.** The FAQ says nonces need not be secret but must not be
   reused, and that reuse destroys the confidentiality of the messages sharing the nonce and lets an attacker
   craft further valid ciphertexts.
2. **How a nonce may be chosen depends on the construction.**

   | Construction | Safe ways to choose the nonce |
   |---|---|
   | XChaCha20-Poly1305-IETF | counter, permutation, random |
   | AEGIS-256 | counter, permutation, random |
   | AEGIS-128L | counter, permutation, random (random is safe up to 2^48 messages, for a collision probability below 2^-32) |
   | AES256-GCM | counter, permutation |
   | ChaCha20-Poly1305 (original, 64-bit nonce) | counter, permutation |
   | ChaCha20-Poly1305-IETF (96-bit nonce) | counter, permutation |
3. **Random nonces cap the number of messages per key.** For random nonces the documented maxima are:

   | Construction | Max messages with random nonces |
   |---|---|
   | AEGIS-256, XChaCha20-Poly1305-IETF | no practical limit |
   | AEGIS-128L | 2^48 |
   | AES256-GCM, ChaCha20-Poly1305-IETF | 2^32 |
   | ChaCha20-Poly1305 (original) | 2^16 |

   Own guidance: 2^16 is about 65 thousand messages and 2^32 about 4.3 billion, numbers a busy service can
   reach, so a design that encrypts under random 96-bit or 64-bit nonces needs a counter, a different
   construction or a rekey schedule written down next to the expected message rate.
4. **There is also a per-(key, nonce) size limit.** Maximum bytes for one message under one nonce: no practical
   limit for AEGIS-256, AEGIS-128L, XChaCha20-Poly1305-IETF and the original ChaCha20-Poly1305 (about 2^64
   bytes); 256 GB for ChaCha20-Poly1305-IETF; about 64 GB for AES256-GCM. The secretstream API caps one message at
   about 256 GB.
5. **Cap the ciphertext size you will decrypt, and split large messages into chunks.** The documentation says
   applications must enforce a maximum ciphertext size despite the limits above, and gives three reasons for
   chunking: it keeps memory use under control, a corrupted chunk is detected before the whole ciphertext
   arrives, and large messages give an attacker more room.
6. **Limit what an attacker can try.** The documentation encourages limiting the number of attempts, for
   example closing a session after many decryption failures. Its tables give the total forgery attempts a key
   should allow (failed decryptions plus one successful forgery), and note that these are single-key limits:
   deployments with several keys or connections must also account for aggregate multi-key limits.
7. **Rekey before the number of encryptions reaches the limit for your message size.** Periodic rekeying
   remains highly recommended. For a 2^-32 attack success probability the documentation lists the encryptions to
   allow under one key:

   | Message size | AES256-GCM | All ChaCha20-Poly1305 variants | AEGIS-256 and AEGIS-128L |
   |---|---|---|---|
   | 16 KB | about 2^38 | 2^48 | no practical limit (256-bit tags) |
   | 1 MB | about 2^32 | 2^48 | no practical limit (256-bit tags) |
   | 1 GB | about 2^22 | 2^48 | no practical limit (256-bit tags) |
   | 64 GB | about 2^16 | 2^48 | no practical limit (256-bit tags) |

   The maximum number of encryptions is the criterion the documentation calls most important when choosing a
   primitive. Protocols that put a timestamp or counter in the additional data to drop old messages have no
   practical limit on total messages.
8. **Short-nonce ciphers need frequent rekeying or nonce extension.** AES and ChaCha20 (not XChaCha20) do not
   have nonces large enough to pick at random. A single nonce must not encrypt different messages under one key,
   though the same nonce under different keys is safe. The documentation's two ways: rotate keys often and make
   a new key per stream, or extend the nonce with a pseudorandom function (a key and the first 128 bits of a
   192-bit nonce make a subkey, the remaining 64 bits are the cipher nonce; `crypto_core_hchacha20` is a
   suitable function). The second reduces security to that of the function and costs a little speed. Unless AES is
   required, it says a cipher with a longer nonce is easier and safer.
9. **Messages that belong together need a construction that knows it.** `crypto_secretbox`, `crypto_box` and
   `crypto_seal` are for independent messages; encrypting each one with its own random nonce does not detect
   messages added, removed, duplicated, truncated or reordered. For files and ordered channels such as TCP the
   documentation recommends `crypto_secretstream` (libsodium 1.0.14 or later): it detects all of those, produces
   different ciphertext for the same stream each time, rekeys automatically before its counter wraps, and its
   final-tag message erases the key. Its file example refuses a stream whose final tag arrives before the end
   of the input and one whose input ends before the final tag. Own guidance: do the same, because the
   no-truncation property only helps a reader that insists on the final tag. The stream header is not secret
   but must be stored first.
10. **Without secretstream, build the sequence from AEAD yourself only with a large nonce.** The documentation's
    pattern is a random initial nonce, incremented after each message with `sodium_increment`, with the
    initialisation vector sent once; a stream that does not match fails the tag check. It requires a nonce
    large enough that reuse is negligible: XChaCha20 and XSalsa20 qualify, AES and plain ChaCha20 do not. On
    unordered transports such as UDP, send the nonce or its offset from the initial value with each message,
    since the tag covers the nonce and a tampered one is detected. Key separation per direction is §1.7.
