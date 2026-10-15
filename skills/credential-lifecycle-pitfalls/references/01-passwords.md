# credential-lifecycle-pitfalls §1 — Passwords

> Section 1 of `skills/credential-lifecycle-pitfalls`. Read it when a password is accepted, stored,
> compared or rate-limited. Numbers are as stated by the Copenhagen Book at commit `fb7eb3a` and the
> libsodium documentation at commit `edebe69`, read 2026-10-15; they are minimums that age.

1. **Validate length and content on a permissive rule.** The Copenhagen Book asks for at least 8
   characters, a maximum that is not set too low (around 64 to 256 is its suggestion), no silent
   modification or truncation of the input, and every valid Unicode character allowed, including
   whitespace. A silent truncation means two different passwords verify as the same one, and a
   maximum of 20 rejects the password manager's output.
2. **Check for weak and leaked passwords.** The source suggests a strength estimator such as `zxcvbn` and
   the haveibeenpwned range API for leaks: hash the candidate with SHA-1, hex-encode it, send only the
   first 5 characters, and compare the returned suffixes locally. The full hash never leaves your server.
   The libsodium documentation agrees on the principle: the best defence against cracking is a strong
   password, and a library such as passwdqc can enforce it.
3. **Do not make password policy hostile.** Per the source: do not block pasting (it discourages password
   managers), do not require periodic changes, and ask for the current password when a user changes it.
4. **Hash with a password hash, salted.** The source ranks Argon2id first, scrypt second and bcrypt for
   legacy systems. With a library string API such as libsodium's `crypto_pwhash_str`, the output already
   contains the algorithm, its version, the salt and the parameters, is ASCII, and can be stored as is;
   no extra column is needed. If you build the record yourself, the salt comes from a cryptographically
   secure generator with at least 120 bits (the source's figure). A pepper (a secret key kept apart from
   the hashes) is only worth adding where the algorithm supports it; the source warns that rolling your own
   mechanism is a bad idea and that HMAC-based peppering with bcrypt must not be attempted.
5. **MD5, SHA-1 and SHA-256 are not password hashes.** The source says not to use them for passwords: they
   are designed to be fast, and a password space is small enough that fast hashes fall to guessing and
   precomputed tables. A slow, memory-hard function makes each guess expensive.
6. **Start from these minimums, then measure.** The Copenhagen Book's minimum parameters: Argon2id with
   memory 19456 KiB (19 MiB), 2 iterations and parallelism 1; scrypt with N 16384, r 16, p 1 and a 64-byte
   output; bcrypt with a work factor of at least 10. The libsodium documentation gives a different method:
   fix the memory you can reserve for hashing given the highest number of simultaneous evaluations, set
   `opslimit` to 3, measure, and lower the memory (keeping 3) if it is too slow or raise the operations
   if it is fast; about one second is the likely acceptable maximum for an online login. Its named
   presets differ again (the interactive memory preset needs 64 MiB). The figures disagree because they
   answer different questions; choose on your hardware, record the choice, and re-read both sources when
   revisiting it.
7. **bcrypt has a length limit and no pre-hash.** The source says input is capped at 72 bytes and some
   implementations at 50, that pre-hashing with SHA-256 or SHA-512 is not recommended because some
   implementations mishandle null bytes, and that a need for longer passwords is a reason to use Argon2id
   or scrypt instead. This is also why §1.1 asks for a maximum no lower than 64.
8. **Store the parameters with each hash and upgrade at login.** The libsodium documentation says not to
   use constants to verify a password and to save the algorithm identifier and parameters alongside the
   hash, so passwords can be rehashed later. `crypto_pwhash_str_needs_rehash` returns 1 when the string is
   valid but does not match the given parameters (rehash at the next login), 0 when it matches, and -1 on
   error (compute a correct hash at the next login). After a successful verification you hold the plaintext,
   which is the only moment an upgrade is possible; do it then, in the same request.
9. **Compare in constant time.** The source says to compare hashes with a constant-time function rather
   than `==`, to avoid timing leaks. A library's `verify` call does this; a hand-written comparison
   usually does not.
10. **Password hashing is a denial-of-service lever.** The source says hashing is resource-intensive and
    vulnerable to DoS. That is the second reason for throttling (§1.11) and for bounding the password
    length (§1.1) before the hash is computed.
11. **Throttle by address, and rely on MFA.** The source calls multi-factor authentication the best defence
    against brute force and credential stuffing and says it should be required for security-critical
    applications. It also says address-based throttling should always exist, for example blocking an
    address for 10 minutes after 10 consecutive failures, with lockout periods that grow or that relax
    gradually. An identifier-based throttle can be layered on top, though it can introduce a DoS of its
    own against a named account (the source points to device cookies as an alternative). Bot detection
    such as a CAPTCHA is another layer the source lists.
12. **Make the error and the timing the same for a wrong password and an unknown user.** The source's
    rule of thumb is a vague message ("Incorrect username or password") and a sign-up and reset that do
    not disclose whether an email is registered: answer "we have sent an email" either way and put the
    "you already have an account" text in the email. It also says response times can still reveal a valid
    account, for example when the password is only checked for existing users, and that defending against
    timing is hard, so go that far only when the account list is truly private. Where usernames are
    public anyway, the source accepts specific messages for usability.
13. **Plaintext passwords do not linger.** libsodium's documentation says a plaintext password should not
    stay in memory longer than needed and recommends locking and zeroing the regions that hold it. In a
    managed language that means not logging, not storing and not passing the value further than the hash
    call; in C it means the documented memory calls.
14. **A password is not an encryption key.** The libsodium documentation says passwords should generally not
    be used for encryption, and sends the reader to its AEAD section before doing so. If a key must be
    derived from a password, use its key-derivation function (`crypto_pwhash`) with a stored random salt and
    stored parameters, not the string API meant for verification.
