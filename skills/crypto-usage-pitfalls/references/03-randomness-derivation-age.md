# crypto-usage-pitfalls §3 — Randomness, derivation, length and age recipients

> Section 3 of `skills/crypto-usage-pitfalls`. Read it when a random value, a subkey, a ciphertext length or an
> age recipient matters. Sourced from the libsodium documentation at commit `edebe69` (`generating_random_data/
> README.md`, `key_derivation/README.md`, `helpers/padding.md`, `usage/README.md`) and from the age repository
> at commit `b74dce4` (`README.md`, `tag/tag.go`), read 2026-10-16. Limits and flags are version-bound.
> Sentences marked "own guidance" are ours.

1. **Take a random integer with the library's uniform function.** `randombytes_uniform(upper_bound)` returns a
   value in `[0, upper_bound)` with a uniform distribution even when the bound is not a power of two, which the
   documentation contrasts with `randombytes_random() % upper_bound`; a bound below 2 leaves only `0`. The
   masking and rejection method for languages without such a function is in
   `credential-lifecycle-pitfalls` §3.8.
2. **Keys, nonces and tokens come from `randombytes_buf`.** It fills a buffer from the operating system
   source (the documentation lists `getrandom`, `arc4random`, `RtlGenRandom` and `/dev/urandom` by platform).
   `randombytes_buf_deterministic` gives the same output for the same seed and the documentation says it is
   mainly useful for writing tests. Own guidance: it never makes a production key.
3. **Do not generate secrets in an image that is copied or snapshotted afterwards.** The documentation says that
   if the random functions are used inside a virtual machine that is snapshotted and restored they may produce
   the same output again. It also says the default generator needs no reseeding after `fork()`, but with a
   non-default implementation the child must call `randombytes_stir()`. Own guidance: generate long-lived keys
   and nonce state after the instance starts in its final form, and do not bake them into a template image.
4. **A stalled `sodium_init()` after boot is an entropy problem, not a reason to relax anything.** The usage page
   says that on some Linux systems, right after a reboot (it names virtual machines from several providers and a
   confidential-compute enclave), initialisation can take a long time; it suggests checking
   `/proc/sys/kernel/random/entropy_avail` (a very low value, under 160, confirms it), enabling `virtio-rng`,
   or using a kernel from version 5.4 on, which includes the relevant algorithm, before installing a
   daemon such as `haveged`. This is version-bound advice.
5. **Derive subkeys from one high-entropy key with a context.** `crypto_kdf` derives subkeys of 16 to 64 bytes
   from a master key, a numeric subkey id and an 8-character context. The context describes what the key is for
   and separates domains to mitigate accidental bugs: the same key and id under two contexts give different
   outputs. Contexts need not be secret or high-entropy, and one application-wide context is acceptable. The id can
   reach 2^64 - 1, but with 128-bit subkeys deriving more than 2^48 of them is not safe; at 160 bits or more it
   is. A password is not a master key (§1.2). Own guidance: one subkey per purpose (encryption, authentication,
   each tenant) rather than one key reused for several.
6. **Ciphertext length is visible; pad before encrypting when length matters.** Most modern constructions disclose
   message lengths. `sodium_pad` rounds a buffer up to a multiple of a block size (ISO/IEC 7816-4 padding,
   libsodium 1.0.14 or later) and `sodium_unpad` recovers the length; padding is applied before encryption and
   removed after decryption. The function returns `-1` if the padded size would exceed the buffer maximum or the
   block size is `0`. The documentation advises against padding to hide the length of a password: hash it instead.
7. **age SSH recipients embed a public-key tag.** The README says encrypting to an SSH key uses more complex
   cryptography and embeds a public key tag in the file, making it possible to track files encrypted to a specific
   public key. The package for hardware-backed "tagged" recipients says in its source comment that its tag
   reduces privacy by letting an observer correlate files with a recipient, but not files among themselves
   without knowing the recipient. Own guidance: if recipient anonymity matters, use native `age1...` recipients
   and check a sample with `age-inspect` rather than assuming; accept a tag only on purpose.
8. **Think before encrypting to someone's published SSH keys.** The README shows combining SSH-key support with
   `-R` to encrypt to the keys on a code-hosting profile, and warns that people may not protect SSH keys
   long-term, since they are revocable when used only for authentication, and that SSH keys held on YubiKeys
   cannot be used to decrypt files. It also says `ssh-agent` is not supported.
9. **Let age generate the passphrase.** With `-p`, leaving the passphrase empty makes age autogenerate a
   secure one. The README says passphrase-protected identity files are not necessary for most uses, where access
   to the identity file implies access to the whole system, and are useful when the file is stored remotely.
10. **An age file's metadata is readable without the key.** `age-inspect` shows the recipient types, whether the
    file uses post-quantum encryption and a size breakdown (header, overhead, payload) without decrypting. Own
    guidance: treat recipient types and length as public, and use §3.6 style padding at the application layer if
    the length matters.
11. **Post-quantum keys are opt-in.** `age-keygen -pq` makes hybrid keys described as secure against future
    quantum computers, built into age 1.3.0 and later; the recipients are about 2000 characters long and the
    README says this may become the default. Own guidance: choose hybrid keys for archives that must stay
    confidential for many years, and confirm that every tool that must read them supports them.
