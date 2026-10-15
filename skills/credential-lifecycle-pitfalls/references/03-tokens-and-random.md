# credential-lifecycle-pitfalls §3 — Tokens and random values

> Section 3 of `skills/credential-lifecycle-pitfalls`. Read it when any value is generated or stored to
> prove an identity or an action: a session ID, a reset or verification token, an API key issued to a user.
> Sourced from the Copenhagen Book at commit `fb7eb3a`, read 2026-10-15.

1. **Generate tokens from a cryptographically secure generator, with at least 112 bits of entropy.** The
   source calls 120 to 256 bits a good range and gives the example of 15 random bytes encoded as base32,
   a 24-character token. A fast, pseudo-random generator such as the one in a standard math package must
   not be used. If you build the token by choosing characters one at a time, the total entropy has to
   reach the same level. This is the generation rule `skills/oauth-oidc-client-pitfalls` §3.2 points to.
2. **A "server-side token" is validated by finding it.** It is a long random string kept in a database or an
   in-memory store, with an expiry and an owner; it is valid if it exists, is unexpired and belongs to the
   user. Session IDs, verification tokens and access tokens are all of this kind.
3. **Single-use means the read deletes.** The source says retrieving a single-use token must also guarantee
   its deletion, and that an atomic operation such as a transaction should do it in SQL. A check followed
   by a separate delete lets two concurrent requests both succeed.
4. **Store sensitive tokens hashed with SHA-256.** For tokens that need extra protection, such as reset
   tokens, the source says to hash them with SHA-256 before storage and to validate an incoming token by
   hashing it before the query. A slow password hash is not needed here because the token is long and
   random (§1.4 of this block is for human-chosen secrets). A database leak then exposes no usable link. The
   source names two real incidents where tokens leaked from storage.
5. **Case and alphabet follow the store.** Tokens are case-sensitive, but if the store is case-insensitive
   (the source names MySQL), constrain the alphabet to one case so two tokens cannot collide.
6. **UUIDv4 is not a safe default.** The source says a version-4 UUID may meet the requirements (122 bits)
   but is space-inefficient and the specification does not guarantee a cryptographically secure generator.
   Use it only if you have checked the library's source of randomness.
7. **Make random strings from random bytes, encoded.** The source's easiest safe method is secure random
   bytes encoded as hex, base32 or base64, with a custom alphabet allowed when its size matches an encoding
   (a 32-character custom alphabet works with base32). For an alphabet of another size, choose each
   character with a uniformly random integer (§3.8).
8. **Random integers: mask, reject, never modulo a small sample.** For a range that is a power of two, mask
   bits. For another range, the source's safest approach is rejection sampling: generate only as many bits
   as the maximum needs and retry while the value is out of range. Taking a random value modulo the
   maximum introduces bias (some values appear more often); a very large input makes the bias small (the
   source's example: 32 random bits for a maximum of 10 gives about 1 in 250 million). Multiplying the
   maximum by a random float also biases, unless the float has far more resolution than the range.
9. **Use the same rules for every secret code, however short.** Own guidance: verification codes, recovery
   codes and OTPs (`credential-lifecycle-pitfalls` §2) come from the same generator and the same unbiased
   selection. The shorter the secret, the more the throttle matters, because the generator cannot make a
   6-digit code hard to guess.
10. **An old token must not outlive a change of who the user is.** When the password, the email or the
    permissions change, the tokens issued earlier (sessions especially) are invalidated, per the sessions
    guidance in `skills/oauth-oidc-client-pitfalls` §3.8 and `skills/auth-session-conventions` §1.5. Reset
    and email-verification tokens are deleted when used or superseded (§2.1, §2.7).
