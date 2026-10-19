# credential-lifecycle-pitfalls §2 — Reset, verification and second factors

> Section 2 of `skills/credential-lifecycle-pitfalls`. Read it when a reset link, an email-verification
> step, an email change or an MFA enrolment is written or changed. Numbers are as stated by the Copenhagen
> Book at commit `fb7eb3a`, read 2026-10-15.

1. **A reset needs one token, once.** The reset link carries a token in the URL path. The source says the
   token is valid for around an hour and at most 24 hours, is single-use (deleted when a valid new password
   is submitted), and that sending another token either invalidates the earlier ones or reuses the
   existing valid one. Generation and storage are §3: random, and stored as a SHA-256 hash.
2. **A reset does not need a verified email, and it verifies one.** The source says the address does not
   have to be verified before a reset link is sent, and that a successful reset can mark the address as
   verified, since the person demonstrably reads that mailbox.
3. **A reset ends every existing session.** The source says to invalidate all sessions linked to the user
   when the password is reset, so an attacker who held a session does not keep it. This is the same rule as
   `skills/auth-session-conventions` §1.5.
4. **Keep the token out of the `Referer` header.** For any page whose path carries a token, set the
   Referrer Policy to `strict-origin` or an equivalent. A reset page that loads a third-party image or script
   would otherwise send the full URL, token included, to that third party.
5. **Ask for the second factor before accepting a new password.** If the user enrolled TOTP or WebAuthn,
   the source says to prompt for it before the new password form, so a mailbox compromise alone is not an
   account compromise.
6. **Rate-limit every endpoint that sends mail.** The source says any endpoint that can send emails needs
   strict limiting, with a CAPTCHA if necessary; otherwise the reset form is a mail bomb aimed at a victim
   and a cost for you. The enumeration rules for the response text are `credential-lifecycle-pitfalls`
   §1.12, and the source lets the reset form either say the email is invalid or stay vague, depending on
   whether registration status is public.
7. **Verify an email with a code or a link, tied to one user and one address.** The source says a verification
   code or link token is tied to a single user and a single email (important when the user can change the
   address after the mail was sent), is single-use and invalidated immediately on use, is valid for at least
   15 minutes (1 to 24 hours recommended), and is regenerated whenever another mail is requested. For a
   link, the previous token may be resent while still unexpired.
8. **A code is an enumerable secret: size and attempts.** The source asks for at least 8 digits for a
   numeric code and at least 6 characters for an alphanumeric one, more for a secure process such as
   creating an account or changing contact details, from a cryptographically secure generator, avoiding
   mixed case and lookalike characters. Attempts are throttled by user ID, about 10 an hour; with that in
   place a code can be valid for up to 24 hours, and an expired code is replaced by a fresh one rather than
   extended.
9. **Sessions are replaced when the address is verified.** The source says all of a user's sessions are
   invalidated when an email is verified, with a new one created for the current user so they stay signed
   in. Verification changes what the account is allowed to do, which is why the old sessions go.
10. **Normalise emails and validate them lightly.** The source says addresses are case-insensitive and
    recommends lowercasing, and that a regular expression cannot fully validate an address and may add a
    ReDoS risk. Its minimal checks: at least one `@`, at least one character before it, a domain containing
    a `.` with a character before it, no leading or trailing whitespace, at most 255 characters. Never
    silently strip a `+tag`: it can be a regular address. Blocking `+` stops duplicate accounts only
    against a careless user, since temporary or new addresses are always available.
11. **Changing an email re-authenticates and keeps the new address apart.** The source says to ask for the
    password, or for a second factor when MFA is on, to store the new address separately until it is
    verified (for example with the verification token), and to notify the previous address.
12. **A TOTP secret is 160 bits, random, per user, and proven at enrolment.** The source states that
    standard TOTP uses HMAC SHA-1 with an exactly 160-bit secret from a cryptographically secure
    generator, unique to each user, stored on the server (optionally encrypted at rest, which does not help
    against system-level access), shared as a base32 `secret` in an `otpauth://` key URI, and that you
    verify the user scanned it correctly by asking for a generated code. A request for a new QR code
    generates a new secret and invalidates the old one.
13. **Throttle code checks and tell the user.** For TOTP and for SMS codes, the source says throttling is
    mandatory, with a basic example of blocking attempts for 15 to 60 minutes after the fifth consecutive
    failure and notifying the user to change the password. Validating a TOTP means generating the code
    yourself for the current 30-second window and comparing. Own guidance: use a maintained library rather
    than the source's sample, and compare in constant time (§1.9).
14. **SMS is the weak factor.** The source discourages SMS-based MFA because it can be intercepted and is
    sometimes unreliable, while noting it may be more accessible; its codes follow §2.8 and live for about
    5 minutes.
15. **Issue recovery codes, and store them hashed.** The source recommends one or more single-use recovery
    codes that replace a passkey or OTP when a device is lost, generated by a cryptographically secure
    generator, and says 40 bits (10 hex characters) is enough when throttling is in place. Unless you can
    store them securely, hash them with your password hash; they are then shown only once, at
    enrolment, and the user can regenerate them while holding a second factor.
