# login-mfa-reset-screens-ui-pitfalls §2 — Codes, limits and reset

Own craft knowledge; the server rules are in other blocks and are linked, not repeated (see origin.md).

## 2.1 One-time-code entry
1. **Symptom: the code arrives by SMS or email and the user types it by hand, or cannot paste it.** Fix: one input (or boxes that accept a pasted full code and distribute it), the one-time-code autocomplete token so the phone can offer it, numeric input mode for numeric codes, and no change of case or spaces by the field.
2. **Accept spaces and dashes** the user pastes ("123 456") and strip them before sending.
3. **Box-per-digit inputs** need paste handling, back-space across boxes, a single accessible name for the group, and a screen reader that does not read six unlabeled fields. A single field is simpler and safer.
4. **Do not auto-submit without a visible state**: if the code auto-submits on the last digit, show it is checking, keep the digits visible and allow correction after a failure.
5. **A wrong code keeps the field, selects the text and says "that code is not right or has expired"**, never which one, and never "wrong code, 2 attempts left" unless the policy wants it (§2.5).
6. **Authenticator-app, email, SMS and security-key paths each have their own copy**; do not show "check your SMS" to an app user. Name the method used and offer another method as an explicit choice (`webauthn-passkey-pitfalls` for keys).
7. **The code screen says where the code went without revealing the full contact** ("sent to a•••@example.com") and offers "use another method" and "I do not have access".

## 2.2 Resend, timers and expiry
1. **Symptom: users press resend five times, get five codes, and enter an old one.** Show a resend control that is disabled with a visible countdown after each send, and say a new code replaces the old one (or say all are valid, whichever the server does; the screen must match).
2. **The timer uses the server's time, not the browser's clock**; a drifting clock lies about the deadline.
3. **A countdown is also text for a screen reader**, updated at a sane rate, not every second.
4. **An expired code says so and offers resend in place**, keeping the user's context; it does not drop them back to the first screen.
5. **A resend failure is its own message** ("could not send, try again"), and it does not reset the countdown.
6. **Do not show more resends than the limit allows**; when the limit is reached say what to do (§2.5).
7. **Email codes arrive late; say it** ("it can take a minute, check your spam folder") without blaming the user.

## 2.3 Recovery codes and backup methods
1. **Symptom: users enrol in MFA and lose the phone with no way back.** Offer backup methods at enrolment and show recovery codes once, with a download or copy action, a confirmation that they were saved, and a plain warning that each works once.
2. **Never show recovery codes again on a later screen**; offer to generate a new set and say that it invalidates the old.
3. **The "I lost my device" path exists and is real** (support, recovery codes, an alternate method); hiding it creates support tickets and insecure workarounds.
4. **Enrolment completes only after the user proves the second factor works**: show the first code check before the factor is turned on.
5. **A change to MFA settings asks for re-authentication** (§3.2) and tells the user by email (`security-hardening`).
6. **Remembered devices say how long and can be listed and revoked** on a settings page.

## 2.4 Reset flow screens
1. **Request screen**: one field, the neutral confirmation of §1.1, and no hint whether the address exists.
2. **The link screen reads the token from the URL, then shows the new-password form**; if the token is bad or expired, say "this link is no longer valid" with a way to request a new one, and do not say why more than that.
3. **Do not leave the token in the address bar or history after use**: redirect to a clean URL when the page loads, and keep it out of third-party requests (`security-hardening` §6 on referrer).
4. **The new-password form has the new-password token and rules shown in advance (§1.4)**, and a confirmation field only if the product wants one; a show-password button often replaces it.
5. **On success, say so and go to sign-in (or sign in directly if the product decided)**, and state that other sessions were ended when that is true.
6. **A reset while signed in is a different screen** (change password) and asks for the current password or a fresh login (§3.2).
7. **The email is part of the interface**: subject, preview and button text name the product and the action, with a sentence for "I did not request this" (`lifecycle-email-program-design-pitfalls` for transactional mail).
8. **Deep links from email must survive login**: a user who is not signed in lands on the right screen after authentication (§3.3).

## 2.5 Rate limit and lockout feedback
1. **Symptom: "too many attempts" with no time, or a shaking form and nothing else.** A user cannot tell if it is broken or blocked.
2. **Say that attempts are limited and when to retry**: "Too many attempts. Try again in a few minutes." A precise countdown is allowed only when it does not depend on whether the account exists.
3. **The limit message appears for known and unknown accounts alike**, otherwise it enumerates (§1.1). Rate limits keyed by address or session, not only by account, make that possible (`security-hardening` §7).
4. **Do not show remaining-attempt counts on sign-in**; they confirm the account and help an attacker plan.
5. **A lockout never reveals its cause on the form**; the account owner learns by email, with a way to unlock or reset.
6. **Offer the way out next to the message**: reset password, use another method, contact support.
7. **A rate-limited response is a distinct, announced state** (live region), the form stays editable where it is safe, and the retry control is disabled until the time passes.
8. **A bot challenge, when used, is accessible** (an alternative to a visual puzzle) and does not appear only after a user error that leaks (`security-hardening` §6).
9. **The same rule applies to the resend and reset-request buttons.**

## Checks
```
Request a reset for a known and an unknown email: same text and same timing; the real mail arrives only for the known one.
Enter a wrong code, an expired code and a code with spaces: three distinct, accurate states; the spaced code works.
Hit the limit: the message gives a way forward and does not change between known and unknown accounts.
```
