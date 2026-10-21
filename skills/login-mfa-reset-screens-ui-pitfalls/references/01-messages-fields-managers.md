# login-mfa-reset-screens-ui-pitfalls §1 — Messages, fields and password managers

Points credited "HTML autofill", "HTML inputmode" or "GOV.UK" were checked on 2026-10-20 (facts only, own words; see origin.md). The rest is own craft or recalled.

## 1.1 No account enumeration in the interface
1. **Symptom: "No account with this email" or "wrong password" on the sign-in screen.** Anyone can now test which emails are registered. Fix: one message for every failed sign-in ("Email or password is incorrect"), the same wording, the same layout and the same status (GOV.UK passwords: do not reveal which credential was wrong).
2. **The reset request answers the same for known and unknown emails**: "If an account exists for this address, we sent a link." The screen never says "email not found".
3. **The visible equality is not enough**: if the response is faster for unknown emails, or a different redirect, or the page differs by one element, it still leaks. The server side of this (equal work, queued mail) is in `security-hardening`; check the screen against the network response too. Concrete cause to look for: the code path for a known account does extra work the unknown one skips (a database write, a hash, an inline mail send while the unknown case returns at once). Check: time both cases several times, and read whether the mail is sent inline or queued and whether the unknown case waits for the same duration; a sign-in handler may be careful while the reset or emailed-link request next to it is not.
4. **Sign-up has the hardest case**: "this email is already used" reveals an account. Prefer the same neutral confirmation ("check your inbox") and send the real message to the address, with a sign-in or reset hint when the account exists. If the product must say it, accept that the screen leaks and rate limit it (§2.5). Check the network response as well as the screen: a client that hides the conflict behind a generic message still lets anyone read the status and body of the response, so the leak is only hidden from people who do not open the network panel; and the same generic message then fails the user who simply mistyped (§1.2.4).
5. **Do not leak through the shape of the flow**: a two-step login that asks for the email first and then shows "enter password" or "create account" tells the same thing. Use a neutral second step, or accept it knowingly for an SSO-routing screen.
6. **Do not leak in the account state**: a locked, disabled or unverified account looks like a failed sign-in on the screen; the real reason goes to the email or to support, not the form (`admin-back-office-pitfalls` for the support side).
7. **Keep the user helpful without leaking**: "Email or password is incorrect. You can reset your password." with the reset link next to it.
8. **Check**: submit a known email with a bad password, an unknown email, and a locked account; the text, status and timing look the same.

## 1.2 Error placement and wording
1. **Symptom: a red banner far from the field, a message that vanishes, or an error only in colour.** Place field errors next to the field, connect them to it (`aria-describedby`), mark the field invalid, and do not rely on colour (`accessibility` §4).
2. **On a failed submit, move focus to the first invalid field or to a summary at the top**, and announce it.
3. **Keep what the user typed, except the password**: GOV.UK says to clear the password field after a failed sign-in and not keep the failed value (GOV.UK password input and passwords). This corrects the earlier advice to keep it hidden in the field.
4. **Say what to do**: "Enter a valid email address", not "invalid input".
5. **Validation that reveals rules is for new passwords only** (sign-up, change, reset), never for sign-in, which accepts whatever the user remembers.
6. **Do not validate email format harshly on sign-in**; a legacy account may have an odd but valid address. Block only what cannot be an address.
7. **Network errors are not credential errors**: "We could not reach the server, try again" is a different message and state from a failed login. The same holds on the reset-request and sign-up screens: map a rate-limit response, a network failure and a validation failure to their own messages, not one generic failure for every non-success.

## 1.3 Fields that let browsers and password managers work
1. **Symptom: the password manager does not offer to fill or save, or offers the wrong entry.** Fix: real form with real inputs, a username or email field and a password field in the same form, correct `type`, names that make sense, and autocomplete tokens.
2. **Tokens**: username or email field with the username token, current password with the current-password token, new password (sign-up, change, reset) with the new-password token, one-time code with the one-time-code token (HTML autofill; the token is the last in the attribute value, comparison is case-insensitive). An optional final token asks the browser to offer saved passkeys on the field (`current-password` followed by `webauthn`, HTML autofill); pair it with `webauthn-passkey-pitfalls`.
3. **One form, one purpose**: sign-in and sign-up are separate forms, or the tokens are clear, otherwise the manager saves the wrong thing.
4. **A two-step login keeps the username field present** (hidden but filled, or visible) on the password step, or managers lose the pairing.
5. **Do not disable autocomplete on credential fields** and do not use random field names to defeat autofill.
6. **A single-page app must submit the form** (or call the credential API) so the manager notices the sign-in; a success without a form submit saves nothing.
7. **Email fields use the email type and a suitable input mode** (the email keyword shows extra keys such as the at sign, HTML inputmode); do not force lower-casing or trimming without telling, but trim whitespace on submit.
8. **Label every field** with a visible label (`accessibility` §4); a placeholder alone disappears and is not read as a label.

## 1.4 Paste, show password and strength
1. **Never block paste** on a password or code field; it breaks password managers and pushes users to short passwords (GOV.UK password input). WCAG 2.2 SC 3.3.8 (Level AA, Understanding page read 2026-10-20) treats blocked paste or blocked password-manager fill on a login or verification code field as a failure unless another way in is offered. Do not set a maximum length attribute on a password field: pasted or autofilled text is truncated silently; show an error if a limit is truly needed. Turn off spellcheck and automatic capitalisation on the field.
2. **A show-password control is a real button with a name and a pressed state**, reachable by keyboard, defaulting to hidden; announce the state change. With two password fields, each button gets a distinct name. Browsers and password managers can reveal the text without the button, so the label may disagree with the field; do not rely on the button as the single source of state. On submit, switch the field back to the password type so the browser does not store the value as general autofill. (GOV.UK password input)
3. **Do not split the password or the code into hidden multi-field tricks that break paste** (§2.1 treats code boxes).
4. **Do not impose composition rules the product cannot justify** (forced symbols, expiry every month); follow your security policy and show it before the user types, not after the failure (`security-hardening` §9 for storage).
5. **A strength meter is advice, not the rule**; if used, it has a text alternative, never colour alone, and the server's rule is the authority.
6. **Offer the passkey or password-manager path where the product supports it** (`webauthn-passkey-pitfalls`), without removing the password path unless the product decided so.
7. **Caps lock and keyboard-layout hints** help on mobile; keep them quiet and accessible.
8. **Show the minimum rules as text beside the new-password field**, linked to it, and update as the user types without announcing every keystroke.

## 1.5 Layout, submit and double press
1. **Symptom: double sign-in, two reset mails, or a spinner forever.** Disable the submit while pending, show progress, and handle the response once.
2. **Enter submits; the button is a real submit.**
3. **Do not auto-submit on a complete code without a way to correct it** (§2.1), and never on a password.
4. **A "remember me" or "keep me signed in" option says what it does** and where it is safe to use (a personal device).
5. **A sign-in screen shown in a dialog follows the dialog rules** (`modal-drawer-dialog-ui-pitfalls`), including returning focus after the session is re-established (§3.2).
6. **Do not hide the reset link or the support route** on error; those are the way out.
7. **Language and timezone**: messages and email subjects follow the user's language; times in "try again at 14:05" use the user's zone (`locale-value-formatting-pitfalls`).

## 1.6 Custom keypads (PIN, device code)
1. **A numeric keypad drawn by the app is an authentication screen too.** Symptom: buttons with no accessible name, a group that a screen reader reads as bare digits, no keyboard digit entry, a code that can be shoulder-surfed in the clear, or a lockout with no message.
2. **Give the group a name and each key a name**, accept typed digits and Backspace from a physical keyboard, show entered digits as masked dots with a text equivalent of the count, and offer a way to clear.
3. **Lockout and failure feedback follow §2.5**: a distinct announced state with the time to retry and a way out, never remaining-attempt counts.
4. **Do not shuffle keys without telling the user**; if it is a deliberate defence, say so in the product's help.
5. **Check**: complete the keypad flow with a keyboard only and with a screen reader, and trip the lockout.

## Checks
```
Sign in with a known email and bad password, an unknown email, and a locked account: same text, same layout, similar timing.
Open the form with a password manager and a screen reader: fields are labelled, offered for fill, pasteable, and errors are announced.
Press submit twice: one request leaves.
```
