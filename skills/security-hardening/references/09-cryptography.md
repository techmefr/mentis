# § 9 — Applied cryptography

Using cryptography inside an application, not designing it. The rule that frames the section: **the
agent selects from what the platform or a maintained library already provides, and never composes
primitives by hand.** Figures below are as read on 2026-10-02 and are cited; where none is given, the
rule has none.

1. **No home-made primitive, mode or protocol.** Use the platform's or a maintained library's vetted
   algorithms through their highest-level interface (an authenticated-encryption call, a signature call, a
   password-hash call), not through raw block operations that leave the assembly to you.
2. **Randomness for anything secret comes from the platform's cryptographic generator.** Tokens, session
   identifiers, keys, salts, nonces and reset codes never come from the language's general-purpose random
   function, which is predictable: an attacker who sees some output can reproduce the rest.
3. **Secrets are compared in constant time.** A byte-by-byte early-exit comparison of a token, a signature or
   a MAC leaks how many leading bytes matched; use the library's constant-time comparison.
4. **Encrypt with an authenticated mode, and never reuse a nonce under the same key.** An authenticated
   encryption scheme must be given a distinct nonce for every call under a given key (RFC 5116, §2.1), and
   the key must itself be uniformly random. For the widely used Galois/counter mode, reusing a nonce
   exposes plaintext and breaks the integrity guarantee entirely (to confirm against RFC 5116, security
   considerations: the exact wording was not re-read). Never hard-code a nonce, never derive it from a constant, and where
   several writers share a key, have them partition the nonce space or let the library generate it.
5. **Passwords are hashed with a memory-hard password hash, salted per password, never with a plain fast
   hash and never encrypted.** For Argon2id the standard gives two parameter sets (RFC 9106, §4): one with
   one pass, four lanes and 2 GiB of memory, and one with three passes, four lanes and 64 MiB of memory for
   memory-limited hosts, both with a 128-bit salt and a 256-bit tag; it also gives a procedure for tuning
   memory and passes to the time you can afford. Take the parameters from the current standard or the
   library's documented defaults and record them next to the code; do not invent a cost. Length and
   composition policy belong to `auth-session-conventions`: the digital identity guideline (NIST SP 800-63B,
   rev. 4, §3.1.1.2) requires verifiers to accept at least 64 characters, forbids composition rules, and
   requires comparison with a blocklist of compromised passwords.
6. **Keys never live in source, in the repository, in a client bundle or in a log.** They come from the
   platform key store or the secret manager of the deployment (§4), are scoped to one purpose each, and have
   a documented rotation path before the first release. Where the platform offers hardware-backed storage,
   ask it to keep the key and perform the operation, rather than reading the key bytes into the app.
7. **A decryption or signature failure fails closed and says nothing about why.** Return one generic error to
   the caller, log the cause server-side, and never fall back to an unauthenticated or weaker path. Do not
   accept the algorithm named by the incoming message as the algorithm to verify with: the verifier fixes
   it.
8. **Deprecated primitives are replaced when the code is touched.** Read the library's deprecation notices
   for the version in use (`skills/source-freshness`); legacy files stay as they are unless asked
   (`code-baseline`).

**To confirm:** points 1 to 3 and 6 to 8 are common practice, with no primary source read in this pass; point 6's
scoping and rotation clauses belong to key-management guidance (NIST SP 800-57) that was not read.

**Checks, by command:** search for the general-purpose random function near tokens, identifiers and keys;
for equality operators on secrets and signatures; for fixed byte arrays or string literals assigned to
nonces, IVs and keys; for hash calls on passwords; for algorithm names read from request headers.

**Sources:** RFC 9106 (Argon2); RFC 5116 (authenticated encryption interface); NIST SP 800-63B-4;
language standard-library security guides for the stacks in use. Key separation and key lifecycle rules
from NIST SP 800-57 were not read (the PDF could not be extracted) and carry no figure here.
