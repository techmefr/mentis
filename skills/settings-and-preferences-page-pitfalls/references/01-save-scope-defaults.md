# settings-and-preferences-page-pitfalls §1 — Save model, scope, defaults and danger

Source: own craft knowledge, with the facts credited inline taken from WCAG 2.2 (SC 3.2.2, 3.3.4) and CSS Media Queries Level 5 (read 2026-10-20, see origin.md).

## 1.1 Autosave against explicit save
1. **Symptom: the user toggles a switch, leaves, and the change is gone, or the reverse: a half-typed value was saved.** Cause: no clear save model. Choose per page: autosave for independent, cheap, reversible controls (toggles, selects); explicit Save for grouped or interdependent fields, text that is validated as a whole, and anything with a cost on change.
2. **Never mix the two on one screen.** A page where toggles save instantly and a text field needs a button teaches nobody what is saved. Split into sections with separate models if both are needed, and say so in each section.
3. **Autosave shows its state per control**: saving, saved, failed with retry. A global "all changes saved" is only true if every request settled; keep a count of pending requests.
4. **Autosave on text commits on blur or after a pause, never on every keystroke**, and never on a value that has not passed validation.
5. **A failed autosave reverts the control or marks it as unsaved with the reason.** Symptom: the toggle stays on and the server says off. Revert to the last confirmed value, or keep the edit and mark it clearly.
6. **Order the requests**: two quick changes to one setting must arrive in order. Send the full value with a version token, or serialise per setting (`long-and-multistep-form-pitfalls` for the token pattern).
7. **Explicit save needs a dirty indicator, a Cancel that restores the stored values, and a warning when leaving with unsaved changes.** Disable Save only when nothing changed, not while validating, or the user cannot tell why it is dead. If one page carries an explicit-Save group and instant-save toggles, label each group with its model (§1.1.2).
8. **A change with a side effect (re-index, email to all members, billing change) is never autosaved.** Put it behind explicit save and a sentence naming the effect.
9. **A control must not change the context on its own.** A language or region select that navigates or reloads the page as soon as the value changes breaks WCAG 2.2 SC 3.2.2 (On Input, level A) unless the user was told beforehand; if the change must apply at once, say so next to the control, or add an Apply button.

## 1.2 Defaults
1. **Symptom: a new account behaves differently from an old one, or a changed default alters existing users.** Cause: defaults stored only as the absence of a row, or copied into rows at creation. Decide once: store nothing and resolve the default at read time (a changed default reaches everyone who never chose), or store the value at creation (a changed default reaches only new accounts). Name the choice per setting.
2. **Distinguish "not set" from "set to the default value".** Without that, reset cannot work and a default change cannot tell who chose. The platform shows why for appearance settings: the prefers-color-scheme media feature has only light and dark, and light also covers a user who expressed no preference (CSS Media Queries Level 5), so a page cannot tell "light" from "unset" from the media query alone. Offer "Match my system" as its own stored choice beside Light and Dark, and resolve it at read time.
3. **Defaults are code or a versioned file, not UI constants**, and the interface reads them from the same place as the server (§1.3).
4. **Safe, private and quiet defaults**: notifications limited to what matters, sharing off, telemetry per policy. A default that exposes data is a defect, not a convenience (`security-hardening`).
5. **Check for the default resolved in more than one layer.** Symptom: changing a default means editing the client, the API and a query. Check: search the code for the fallback idiom of the stack (a nullish-coalescing default, a coalesce in SQL, a default argument) on setting reads; each setting's default has exactly one source and every other layer reads it.
6. **A default change is a release note item** when it affects existing users who never chose (`release-notes-writing-pitfalls`).

## 1.3 A registry of settings
1. **Keep one registry** (on a small page with a handful of settings, a single shared constants file holding keys, allowed values and defaults is enough; do not build more): key, type, allowed values or range, default, scope, who may change it, whether it needs a restart or a reload, whether it is dangerous, whether it is searchable. The page, the API validation and the docs are generated from it or checked against it.
2. **Validate on the server against the registry.** An unknown key is rejected, not stored; a stored key without a registry entry is a migration to write.
3. **Type the values**, with enums for choices and ranges for numbers. Symptom: "yes", "true" and 1 in the same column.
4. **Version the schema.** Renaming or splitting a setting needs a migration of stored values; keep reading the old key until the migration has run, then drop it (`api-change-classification-pitfalls`).
5. **Settings are not a dump for state.** UI state (which panel is open) and feature configuration are different stores; a page-size memory is a per-device convenience, not an account setting.

## 1.4 Scope and precedence
1. **Symptom: "I set it, but the page still behaves the other way" or an admin cannot enforce a rule.** Cause: several layers (platform, organisation, workspace, team, user, device) with an undefined order. Write the precedence once, for example platform default, then organisation, then workspace, then user, and state for each setting which layers may set it.
2. **Some settings are locked by a higher layer.** Show the value as locked with the owner ("set by your organisation") rather than hiding it or letting the user change it and have no effect.
3. **Resolve the effective value on the server** and return it with its source, so the client displays "inherited from the workspace" without recomputing the merge.
4. **Show inheritance in the control**: "Using the workspace default (English)" with a way to override, not a control that looks like the user's own choice.
5. **Per-device against per-account**: theme and density may follow the device, language usually the account. Decide, and say which in the label when it differs from what users expect.
6. **Tenant scope on every read and write.** A setting key from another tenant must return not found (`laravel-tenant-context-by-default`).
7. **Who may change a layer is a permission, not a role name**: a user may edit their own, a manager the team's, an owner the organisation's (`laravel-permissions-not-roles`).

## 1.5 Reset
1. **Symptom: "Reset" wiped choices the user did not expect.** Name the target on the button: "Reset notification settings", not "Reset". A page-wide reset is a separate, confirmed action that lists what it covers.
2. **Reset means delete the user's override**, so the value falls back to the inherited layer, not write the default value into the row (which would pin it and ignore later default changes).
3. **Confirm with a count or a preview of what changes**, and offer undo for a short time where the data allows it.
4. **Never reset what the user cannot see.** A section hidden by permission or by a filter is outside the reset.
5. **Reset to default is not the same as restore previous.** If history matters, keep the last values for a period or an audit entry (§1.6).

## 1.6 Dangerous settings
1. **Define dangerous in the registry**: affects other users, deletes or exposes data, costs money, or cannot be undone. Examples: public sharing, data retention, SSO enforcement, API key creation, account deletion.
2. **Separate them physically**: a distinct section at the end, not interleaved with preferences, in a visual style that signals risk without relying on colour alone.
3. **Confirm in words**: the dialog names the effect and the scope ("All 42 members lose access to the shared links"), and for destructive actions asks for a typed confirmation or a re-authentication (`admin-back-office-pitfalls`, `auth-session-conventions`). WCAG 2.2 SC 3.3.4 (Error Prevention for legal, financial and data, level AA) asks that a submission which modifies or deletes user-controllable data be reversible, or checked for input errors with a chance to correct them, or confirmable after a review step; one of the three is enough, and a review-and-confirm step is the usual choice for settings.
4. **Enforce on the server**: permission, re-authentication freshness and the confirmation token are checked there; a hidden toggle is not a control.
5. **Write an audit entry** with actor, old value, new value, time and scope, readable by the people the change affects.
6. **Notify the affected people** when an organisation-wide setting changes (`in-app-notifications-pitfalls`), and rate-limit repeated changes.
7. **Prefer reversible forms**: a deactivation period before deletion, a dry run showing what a retention change would remove (`admin-back-office-pitfalls` for dry runs).
8. **Secrets in settings** (API keys, webhook secrets) are shown once at creation, stored hashed or encrypted, and masked afterwards with rotate and revoke (`credential-lifecycle-pitfalls`).
