# settings-and-preferences-page-pitfalls §2 — Structure, states, accessibility and tests

Source: own craft knowledge, except the accessibility points marked with a citation, checked on 2026-10-20 and re-checked against the full WCAG 2.2 and WAI-ARIA 1.2 texts the same day (see origin.md). Unmarked points have no source.

## 2.1 Structure and search
1. **Symptom: users cannot find an option and ask support.** Group by the user's task or object (Profile, Notifications, Security, Workspace, Billing), not by the code module that owns the setting. Keep a group to a handful of items before it needs sub-sections.
2. **Separate personal from shared.** "My preferences" and "Workspace settings" are different pages or clearly labelled tabs, with the permission to see each (§1.4).
3. **Each setting has a label that says what changes**, a one-line help text that says the effect and the scope, and the current effective value. Avoid labels that need the help text to be understood.
4. **Use positive wording for toggles.** "Send me weekly summaries" is clear; "Disable no-summary mode" is a double negative. The label and the state ("On"/"Off") agree.
5. **Search the settings when there are more than a screen or two.** Index label, help text and synonyms from the registry (§1.3), match across groups, show the group of each hit, and open the control with focus on it. The `filters-search-and-saved-views-pitfalls` rules on debounce and empty results apply.
6. **No-result search offers a way out**: clear the query, and a link to contact support or the docs, not a blank panel.
7. **Deep links to a setting** (a hash or route per group and setting) so help articles and notifications can open the exact control; the link survives a rename through the registry key, not the label.
8. **Do not bury essentials**: sign-out, language, notification mute and data export are reachable in two steps from anywhere.

## 2.2 States of the page
1. **Render separately**: loading (skeleton with the page shape), loaded, saving, saved, error with retry, offline, and no-permission. Never show defaults while the stored values are still loading; the control then flips under the user's finger. Symptom: a reader that returns a default (all switches on) until the first response arrives. Check the reader's not-loaded branch and show a skeleton or a disabled neutral state instead.
2. **Disabled controls say why**: "Managed by your organisation", "Requires the Pro plan", with the link to act. A silent grey control reads as a bug.
3. **A failed load blocks editing.** Saving over values that never loaded would overwrite them with defaults.
4. **Concurrent edit**: a stale tab saving old values over newer ones needs a version token and a refresh prompt (`long-and-multistep-form-pitfalls`).
5. **Changes that need a reload or restart** say so at the control and offer the action, instead of appearing to work and not taking effect.
6. **Apply preview settings immediately where they are visual** (theme, density, language) so the user sees the result, and keep the saved state separate from the preview until committed, if explicit save is used.
7. **Empty sections do not exist**: a group with no visible setting for this user is hidden from navigation, not shown empty.

## 2.3 Accessibility
1. **Every control has a programmatic label** tied to the visible text, the help text linked as a description, and an error message linked to the field (`accessibility`, `04-forms`). WCAG 2.2 requires labels or instructions for input (SC 3.3.2, level A) and that the visible label text be contained in the accessible name (SC 2.5.3, level A); the help text link is the aria-describedby relation.
2. **A switch is a switch**: the role and the on/off state are exposed, it works with Space (Enter is optional), and the state is not only a colour or a position. A native checkbox styled as a switch is the safest base (ARIA Authoring Practices, switch pattern: role, checked state, keys).
3. **Announce the save result politely.** Use one live region that exists at load; "Saved" or "Could not save, retry" for autosave, without moving focus (WCAG 2.2 SC 4.1.3: a result or an error shown without a focus move must be exposed by role; `in-app-notifications-pitfalls` §2.3 for the pattern).
4. **Keep focus where the user is** after a save, a reset or a dialog close; return it to the control that opened the dialog.
5. **Groups are real groups**: fieldset and legend, or a group element labelled by a visible heading, so a screen-reader user can jump between sections (switch pattern, grouping note).
6. **Confirmation dialogs trap Tab inside, close on Escape and return focus to the opener** (modal dialog pattern). For a dangerous setting, put the initial focus on the least destructive action, not on the confirm button (same pattern, destructive note; corrected: this block first said tab order). `a11y-hiding-and-tables-pitfalls` for hiding rules.
7. **Settings search is a search landmark** (the native search element, or the search role on a form; the APG search landmark page, read 2026-10-20, asks for a search landmark rather than a form landmark and a unique label only when a page has more than one), with results announced as a count and keyboard navigation through hits (`filters-search-and-saved-views-pitfalls`).
8. **Language and locale settings use the native name of each option** and set the language attribute on it, so a speaker of that language can read it (WCAG 2.2 SC 3.1.2, Level AA, read 2026-10-20: the language of each passage must be determinable, with exceptions for proper names, technical terms and words absorbed into the surrounding language; `locale-negotiation-and-switcher-pitfalls`).
9. **Respect reduced motion** for toggle transitions and the saved indicator: WCAG 2.2 SC 2.3.3 (Level AAA, read 2026-10-20) asks that interaction-triggered motion can be turned off unless essential, and names the reduced-motion media query as a technique.
10. **A switch keeps one label whatever its state.** Symptom: the label flips between "Enable alerts" and "Disable alerts" while the state is also announced, so the reader hears a contradiction. Check: the accessible name is identical when on and off (switch pattern, label note).
11. **Reserve the assertive alert role for urgent failures.** Symptom: every successful autosave interrupts the screen reader. Use a polite status for "Saved", the alert role only for a failed save or a blocked dangerous action; assertive output on non-urgent content is a listed failure (WCAG 2.2 Understanding 4.1.3).

## 2.4 Performance
1. **Load the page's settings in one request**, with the effective values and their sources, not one request per control.
2. **Do not refetch the whole page after each autosave.** Update the one control from the response; refetch only on conflict.
3. **Debounce text autosave** and cancel the pending request when a newer value supersedes it, keeping order (§1.1).
4. **Lazy-load heavy sections** (billing, API keys, integrations) when opened, but keep their deep links working (§2.1).
5. **Cache read-only registry data** (options lists, locales) and invalidate on release; a cached effective value must be dropped after any change in a higher layer.
6. **Measure with the web-performance block**: layout shift when stored values replace skeletons is the usual defect here (`webperf`).

## 2.5 Privacy and logs
1. **Do not log setting values that are personal or secret**: log the key and that it changed, not an address or a token (`telemetry-sensitive-data-pitfalls`).
2. **Privacy choices are first-class**: consent and tracking preferences are stored with time and version of the text they answered, withdrawable as easily as given, and not pre-ticked where the rule you operate under forbids it. Which rule applies is a question for your adviser, not this block, and not legal advice.
3. **Export and delete my data live in settings** or link from it (`dsar-handling-pitfalls`).

## 2.6 Tests
1. **Save model**: toggle a control, reload, assert the value persisted; for explicit save, assert Cancel restores and leaving warns.
2. **Failure path**: make the save fail, assert the control reverts or shows unsaved, and the live region says so.
3. **Ordering**: send two quick changes, delay the first response, assert the final stored value is the second.
4. **Precedence**: for each layer combination, assert the effective value and the reported source; assert a locked setting cannot be overridden by a direct API call.
5. **Default change**: change a default, assert users who never chose follow it and users who chose do not.
6. **Reset**: assert it removes only the named section's overrides and the value falls back to the inherited layer.
7. **Dangerous setting**: assert a request without permission or fresh confirmation is rejected server-side and that an audit entry is written.
8. **Tenant isolation**: a key from another tenant returns not found.
9. **Accessibility**: assert names, descriptions, switch state, focus after save and dialog, and a keyboard-only pass; run an automated check (`playwright-e2e-pitfalls`, `testing-library-query-pitfalls`).
10. **Registry parity**: a test fails when a stored key, an API field or a UI control has no registry entry.

## 2.7 Framework pointers (reference only)
1. **Laravel**: a settings table keyed by scope, owner and key, resolved through one service; form requests validate against the registry (`laravel-conventions`, `laravel-tenant-context-by-default`).
2. **React or Nuxt query layers**: one query for the page, a mutation per control with optimistic update and rollback, keyed by scope (`data-fetching-state-conventions`, `react-nextjs-conventions`).
3. **Vuetify or similar kits**: switch, text field and dialog components carry their own label and focus behaviour; check them against §2.3 rather than assuming (`vue-nuxt-vuetify-conventions`).
4. **Mobile**: per-device settings may live in local storage and per-account ones on the server; keep the two visibly apart (`flutter-conventions`).
5. **Flags are not settings.** A product flag with rollout rules belongs to `feature-flag-lifecycle`; a user-facing setting that happens to be backed by a flag keeps its registry entry.
