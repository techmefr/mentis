# login-mfa-reset-screens-ui-pitfalls §3 — Session expiry, redirects and tests

Own craft knowledge; the token and cookie mechanics are in `auth-session-conventions` and are not repeated (see origin.md).

## 3.1 Session expiry in the interface
1. **Symptom: the user clicks Save after twenty minutes and is thrown to a login page, or sees a vague error and a blank table.** Cause: the request got an unauthenticated answer and the client has no plan for it.
2. **One place in the client handles the unauthenticated response**: the HTTP layer, not each screen. It decides between a silent refresh, a re-authentication prompt and a redirect.
3. **Distinguish unauthenticated (session over) from forbidden (signed in but not allowed).** The first asks to sign in; the second shows "you do not have access" and keeps the session (`security-hardening` §3).
4. **Warn before expiry only when the product has a fixed idle timeout**, with a short, accessible notice and a way to stay signed in; do not warn for refresh-token sessions that renew themselves.
5. **A background request that fails because of expiry must not toast an error on a page the user is not looking at**; defer until they act.
6. **Show the signed-out state clearly** once confirmed, so a user does not keep typing into a dead page.

## 3.2 Re-authentication without losing work
1. **Symptom: a long form is lost because the session ended during typing.** Fix: re-authenticate in place (a dialog or a popup) and retry the request, or save a draft before redirecting and restore it after sign-in.
2. **A re-auth dialog follows the dialog rules** (`modal-drawer-dialog-ui-pitfalls`): focus inside, return focus to the control that caused the request, the page behind inert.
3. **After re-auth, repeat the failed request once**; a non-idempotent request needs a safe replay rule (`security-hardening` §7), not a blind retry.
4. **Never keep credentials in the client to re-authenticate silently.** The user types them or uses their manager.
5. **Step-up authentication for sensitive actions** (change email, delete account, export data) asks for the password or a second factor again, says why, and returns to the action when done.
6. **A different user signing in on the same screen** must not see or send the previous user's draft; clear drafts on sign-out and on a user change.
7. **Cookie or storage cleared mid-session** looks like expiry; handle it the same way.

## 3.3 Redirects after login
1. **Symptom: the user opens a deep link, signs in and lands on the home page.** Keep the intended destination through the login (a path stored server side or in a short-lived parameter) and go there after success.
2. **Allow only relative paths of your own application** as the destination; an absolute URL, a protocol-relative URL or a script scheme in the value is an open redirect and a phishing aid.
3. **Do not redirect to the login page for an API call**; a page request redirects, an API request returns an authentication error that the client handles (§3.1).
4. **After sign-out, go to a public page and clear the history entries that show private content**; the back button must not display a cached private page (`security-hardening` §6 on caching).
5. **Already signed in, visiting the login page, redirects onward** instead of showing the form.
6. **MFA in the middle of login keeps the destination** across the extra step and across a provider round trip (`oauth-oidc-client-pitfalls` for state and return).
7. **A new account lands on the right first screen**, not an empty dashboard with no hint.

## 3.4 Multi-tab, sign-out and shared devices
1. **Symptom: the user signs out in one tab and keeps working in another.** Notify the other tabs (a storage or broadcast event) and move them to the signed-out state.
2. **Sign-out is a real action**, not a link that clears local data only; the server ends the session (`auth-session-conventions`).
3. **A "sign out everywhere" option exists and says what it does**; it is offered after a reset or a suspected compromise.
4. **Sensitive screens should not stay readable** after a long idle on a shared device: an idle lock or a shorter session is a product decision stated in the policy.
5. **Sign-in in two tabs at once** must not leave one tab in an error state; the second tab reads the new session.
6. **Login after a long idle starts from a clean state**: no old validation messages, no stale form values, no leftover rate-limit message once the time has passed.

## 3.5 Content and trust
1. **The domain and the product name are visible** on every auth screen, and links from emails go to the same domain.
2. **Do not ask for more than needed**: no phone number, address or consent bundle on the login screen.
3. **Consent and terms at sign-up are a real choice** and recorded; links open in the same app flow, not a dead end.
4. **Show a clear route to help** (support, status page), especially on lockout and code screens.
5. **Third-party scripts on auth pages are minimised** (`security-hardening` §6); a tracker on the password field is a leak.

## 3.6 Tests
1. **Enumeration test**: submit a known and an unknown email to sign-in, sign-up and reset; compare text, status, redirect and a coarse timing.
2. **Password manager test**: with a real manager or the platform's autofill, sign in, sign up and change a password; the right entries are offered and saved.
3. **Paste and keyboard test**: paste a password and a spaced code; complete every screen without a mouse.
4. **Code tests**: wrong, expired, reused, spaced and resent codes; countdown matches the server; resend limit message.
5. **Limit test**: trip the limit for a known and an unknown account; same message and a way forward.
6. **Expiry test**: let the session end during a form submit; the work is kept, re-auth works, the request is replayed once.
7. **Redirect test**: deep link to a protected page, sign in, land there; a crafted external destination is refused.
8. **Multi-tab test**: sign out in one tab, the other reacts.
9. **Accessibility tests on error and challenge states**: errors announced, countdown readable, focus handled (`a11y-lint-wiring-pitfalls`).

## 3.7 Framework pointers
Facts to re-read in the version you use; none was checked here.
1. **Auth kits** for Laravel (Breeze, Fortify, Jetstream), Nuxt and Next ship these screens; check the messages they return for unknown emails and the rate-limit text, which are common enumeration leaks.
2. **Laravel throttling and Fortify** return a rate-limit response that a custom SPA must map to the distinct state of §2.5.
3. **SPA routers** need a guard that stores the intended path (§3.3) and one HTTP interceptor for expiry (§3.1).
4. **Passkey and provider libraries** have their own prompts; place them beside the password form without breaking the manager pairing of §1.3.
