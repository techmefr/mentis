# field-and-row-permission-ui-api-pitfalls §1 — Model and interface

## 1.1 One definition
1. **Separate three questions** and answer each in one place: may this person use this kind of action
   (capability), on this record (row scope: ownership, team, tenant, state), and on this attribute (field
   access: read, write, none). Symptom: a check that mixes them in a view and gets one wrong. Check: for one
   resource, find where each question is answered; more than one place is the defect.
2. **Check capabilities, not role names, in code.** A role is a bundle that changes; a capability is stable.
   (Laravel flavour in `skills/laravel-permissions-not-roles`.)
3. **Row scope is a query condition, not a post-check.** Expressed as "records visible to this person" and
   composed into every query on the resource; a check after fetching has already loaded the data and fails
   open when someone forgets it.
4. **State changes access.** A record in "submitted" may be read-only for its author, editable for a reviewer,
   hidden from others. Put the state in the rule, not in the screens, and test each state.
5. **Field access is data, per resource.** A list of fields with, for each role or capability, the access
   level. Hard-coding "if admin show salary" in templates is how a fifth role gets forgotten.
6. **Defaults deny.** A new field is invisible and read-only to everyone until a rule says otherwise; a new
   endpoint has no access until it declares a rule. Symptom: a field added to the model appears in the API for
   all roles the next release.

## 1.2 Hide, disable, mask or explain
1. **Hide when the existence of the thing is itself restricted** (a menu for a module the person has no right
   to, a field of another department's data). Hidden things reveal nothing and add no noise.
2. **Disable (or make read-only) when the person should know it exists but cannot act now**, and say why
   ("Only a manager can approve"). A disabled control without a reason frustrates and, for screen-reader users,
   is easy to miss (see `skills/frontend-ux-antipattern-review-pitfalls`). The ARIA Authoring Practices explain why: browsers take a disabled native control out of the tab order, and screen-reader users find controls mostly by moving focus, so they are far less likely to discover one they cannot reach; aria-disabled keeps an element focusable while it says it is disabled, and the guide asks for one consistent convention.
3. **Mask when the person may know a value exists but not read it** (last four digits, "restricted"), and have
   the server do the masking: a value masked in the client was sent to the client.
4. **A read-only field shows the value as text, not as a greyed input.** A disabled input is ignored by some
   readers and cannot be selected or copied in some browsers (that part is recalled behaviour, not checked). Checked in the HTML Standard: a disabled control is left out of the submitted form data, so a form that uses disabled for read-only sends no value for that field, and a server that reads a missing field as a clear erases it. Treat an absent field as unchanged, and render the value as text.
5. **Do not mix signals across the app.** Pick the convention (hide for existence-restricted, disable plus
   reason for state-restricted) and use it everywhere, so a missing button always means the same thing.
6. **"Request access" beats a dead end** where the business allows it: a link to the owner or a request flow
   in place of an error page.
7. **Hiding is not security.** A hidden button is a courtesy; the endpoint behind it still refuses (§2). Test
   by calling the endpoint directly as the restricted user.

## 1.3 How the interface learns what is allowed
1. **The server sends what the person can do with each record** (an allowed-actions list, field access levels)
   computed from the same rules as enforcement, and the client renders from it. Symptom of a client-side copy:
   the button appears and the server refuses, or the reverse.
2. **Per-record flags beat per-session flags.** A person may edit their own records and not others; a global
   "canEdit" is wrong for lists. Include flags in each row or in the detail response.
3. **Flags are hints and can be stale.** Permissions or state change after the page loaded. The server's refusal
   is authoritative; handle it by refreshing the flags and explaining, not by showing a generic error.
4. **Do not put secrets in the flag payload.** Sending "all roles and their permissions" to the client to
   decide locally exposes the permission model and rarely stays in sync.
5. **Route guards and menu filtering are navigation aids.** Whatever route a person types in, the data call
   behind it is checked (§2).
6. **Forms render from field access.** A field with no read access is absent; read-only access renders text;
   write access renders an input. The form submits only the fields it rendered as inputs, and the server
   re-checks them (§2.2).
7. **Impersonation and "view as" tools** are privileged features: audit them (§3.1), show a persistent banner,
   and block irreversible actions while impersonating.
