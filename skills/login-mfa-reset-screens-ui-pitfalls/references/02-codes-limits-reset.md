# login-mfa-reset-screens-ui-pitfalls §2 — Codes, limits and reset

Applicability: §2.1 to §2.3 apply only when the product has a typed one-time code or a second factor. §2.4 and §2.5 apply to any reset or emailed-link flow and any limit message.

Own craft knowledge, except points credited "HTML autofill", "HTML inputmode" or "GOV.UK" (checked 2026-10-20, facts only; see origin.md). The server rules are in other blocks.

## 2.1 One-time-code entry
1. **Symptom: the code arrives by SMS or email and the user types it by hand, or cannot paste it.** Fix: one input (or boxes that accept a pasted full code and distribute it), the one-time-code autocomplete token so the phone can offer it (HTML autofill), numeric input mode for numeric codes on a text-type input (HTML inputmode: a numeric keyboard suited to PIN entry; GOV.UK security code does exactly this), and no change of case or spaces by the field.
2. **Accept spaces and dashes** the user pastes ("123 456") and strip them before sending (GOV.UK security code). Give too few digits, too many digits and non-digit characters their own messages.
3. **Box-per-digit inputs** need paste handling, back-space across boxes, a single accessible name for the group, and a screen reader that does not read six unlabeled fields. A single field is simpler and safer.
4. **Do not auto-submit without a visible state**: if the code auto-submits on the last digit, show it is checking, keep the digits visible and allow correction after a failure.
5. **A wrong code keeps the field, selects the text and says "that code is not right or has expired"**, never which one, and never "wrong code, 2 attempts left" unless the policy wants it (§2.5).
6. **Authenticator-app, email, SMS and security-key paths each have their own copy**; do not show "check your SMS" to an app user. Name the method used and offer another method as an explicit choice (`webauthn-passkey-pitfalls` for keys).
7. **On sign-in the resend screen must not reveal the number or address the code went to** (GOV.UK security code); where the product shows a masked contact, decide that knowingly. The code screen says where the code went without revealing the full contact ("sent to a•••@example.com") and offers "use another method" and "I do not have access".

## 2.2 Resend, timers and expiry
1. **Symptom: users press resend five times, get five codes, and enter an old one.** Show a resend control that is disabled with a visible countdown after each send, and say a new code replaces the old one (or say all are valid, whichever the server does; the screen must match).
2. **The timer uses the server's time, not the browser's clock**; a drifting clock lies about the deadline.
3. **A countdown is also text for a screen reader**, updated at a sane rate, not every second.
4. **An expired code says so and offers resend in place**, keeping the user's context; it does not drop them back to the first screen. GOV.UK shows a distinct expired message with a new code sent, and treats a very old code as simply incorrect (GOV.UK security code). Example only: that service uses fifteen minutes and keeps an earlier code valid until its own expiry; the product's own policy decides both.
5. **A resend failure is its own message** ("could not send, try again"), and it does not reset the countdown.
6. **Do not show more resends than the limit allows**; when the limit is reached say what to do (§2.5).
7. **Email codes arrive late; say it** ("it can take a minute, check your spam folder") without blaming the user.

## 2.3 Recovery codes and backup methods
1. **Symptom: users enrol in MFA and lose the phone with no way back.** Offer backup methods at enrolment and show recovery codes once, with a download or copy action, a confirmation that they were saved, and a plain warning that each works once.
2. **Never show recovery codes again on a later screen**; offer to generate a new set and say that it invalidates the old.
3. **The "I lost my device" path exists and is real** (support, recovery codes, an alternate method); hiding it creates support tickets and insecure workarounds. GOV.UK also tells the user on the code screen what to do without the phone (GOV.UK security code).
4. **Enrolment completes only after the user proves the second factor works**: show the first code check before the factor is turned on.
5. **A change to MFA settings asks for re-authentication** (§3.2) and tells the user by email (`security-hardening`).
6. **Remembered devices say how long and can be listed and revoked** on a settings page.

## 2.4 Reset flow screens
1. **Request screen**: one field, the neutral confirmation of §1.1, and no hint whether the address exists.
2. **The link screen reads the token from the URL, then shows the new-password form**; if the token is bad or expired, say "this link is no longer valid" with a way to request a new one, and do not say why more than that. If the product has an emailed sign-in link (single use), a distinct "already used" message is a deliberate trade: it helps a user who clicked twice and tells only someone who holds the token; decide it once and write it down, and do not apply the same distinction to a reset or code screen where the extra information has a cost.
3. **Do not leave the token in the address bar or history after use**: redirect to a clean URL when the page loads, and keep it out of third-party requests (`security-hardening` §6 on referrer). Check: the page reads the token from the query and never replaces the address (grep for the query read with no history replace), and the responses carry a restrictive referrer policy; this applies to emailed sign-in links as much as to reset links.
4. **The new-password form has the new-password token and rules shown in advance (§1.4)**, and a confirmation field only if the product wants one; a show-password button often replaces it.
5. **On success, say so and go to sign-in (or sign in directly if the product decided)**, and state that other sessions were ended when that is true. Email the owner that the reset happened (GOV.UK passwords). Send a link or code, never the password itself, and time-limit it; the duration is not given by the source.
6. **A reset while signed in is a different screen** (change password) and asks for the current password or a fresh login (§3.2).
7. **The email is part of the interface**: subject, preview and button text name the product and the action, with a sentence for "I did not request this" (`lifecycle-email-program-design-pitfalls` for transactional mail).
8. **Deep links from email must survive login**: a user who is not signed in lands on the right screen after authentication (§3.3).

## 2.5 Rate limit and lockout feedback
1. **Symptom: "too many attempts" with no time, or a shaking form and nothing else.** A user cannot tell if it is broken or blocked.
2. **Say that attempts are limited and when to retry**: "Too many attempts. Try again in a few minutes." A precise countdown is allowed only when it does not depend on whether the account exists.
3. **The limit message appears for known and unknown accounts alike**, otherwise it enumerates (§1.1). Rate limits keyed by address or session, not only by account, make that possible (`security-hardening` §7).
4. **Do not show remaining-attempt counts on sign-in**; they confirm the account and help an attacker plan. For orientation only, GOV.UK allows five to ten wrong attempts before a lock or extra checks, and a time delay after ten wrong codes (GOV.UK passwords, security code); the product sets its own numbers.
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
