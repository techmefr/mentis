# onboarding-and-empty-state-pitfalls §2 — Empty states, accessibility, performance and tests

Source: own craft knowledge, no external source (see origin.md). Accessibility points are recalled public practice (see origin.md, Not verified).

## 2.1 Kinds of empty
1. **Symptom: "No results" shown while the request failed or is still running.** Render separately: loading, first-use empty (nothing created yet), filtered empty (data exists, filters hide it), permission empty (data exists, the user cannot see it), error with retry, offline. Each has its own copy and action (`data-table-ui-pitfalls` §2.1). Check: a length-is-zero test with no separate loaded flag renders the empty state before the first response; a catch block that sets the list to empty renders it after a failure. Grep for both, and note which screens guard and which do not.
2. **First-use empty teaches and offers one primary action**: what this area is for, the single next step, and a secondary link to import or learn. Three equal buttons are a menu, not guidance.
3. **Filtered empty says what is filtered and how to clear it**: "No invoices match 'overdue' and 'Berlin'" with a clear-filters action, and keeps the filter controls visible (`filters-search-and-saved-views-pitfalls`).
4. **Permission empty must not leak**: "Nothing to show" and a request-access path, not "3 items hidden", which reveals that data exists (`field-and-row-permission-ui-api-pitfalls`).
5. **Error is never styled as empty.** A failed request keeps the last good data where there is some and shows the reason and a retry, not a friendly illustration of nothing.
6. **Empty after deletion differs from empty at start**: after the last item is removed, say so and offer undo or create, not the welcome copy.
7. **Empty states of derived screens** (dashboards, charts, reports) say why no value exists (no data in range, no source connected) and do not draw a zero line that looks like a measurement (`dashboard-ui-pitfalls`, `chart-choice-pitfalls`).
8. **Empty search results suggest recovery**: check spelling, widen the range, remove a filter; do not just state absence.
9. **An empty state in a component that appears many times** (a card in a grid) stays small and consistent; do not render a full illustration per card.

## 2.2 Copy and visuals
1. **Say what the user can do, in the product's own terms**, in one or two short sentences and a labelled button that names the action ("Create the first invoice", not "Get started").
2. **Illustrations are decoration**: mark them as such, keep them light, never carry the meaning in the image alone.
3. **Do not blame**: "No data yet" over "You have not added anything".
4. **Localise and test the longest translation**; empty states are often the first thing a new locale sees (`i18n-message-format-pitfalls`).
5. **Do not promise what is not built**: a "coming soon" empty state with no date or action is noise; link to the request channel or hide the area.
6. **Keep tone consistent with the rest of the product** and with the UX-writing rules of the team's design system where they exist.

## 2.3 Accessibility
1. **The empty state is real content in the reading order**, in the region the list would occupy, with a heading at the right level (a styled paragraph is not a heading), not a pseudo-element or a background image.
2. **Announce the change to empty** after a filter or search: one polite live region with the result ("No invoices match your filters"), without moving focus (`in-app-notifications-pitfalls` §2.3 for the pattern).
3. **The primary action is a native button or link** with an accessible name that stands alone; the illustration has empty alt text if decorative (`accessibility`, `01-semantics-keyboard`).
4. **A checklist is a list**: each step has a name, a status stated in text (not only a tick colour), and the progress is exposed as text ("3 of 5 done"), with a progress element only if it carries the same value.
5. **Tours and coach marks are keyboard-operable**: next, back, skip and close by keyboard, focus moves into the step and returns on close, Escape closes, and the underlying page is inert only while a modal step is open (`a11y-hiding-and-tables-pitfalls`).
6. **Do not time out guidance**: hints that vanish after a few seconds fail users who read slowly or use a screen reader.
7. **Do not rely on colour, position or hover** to indicate the highlighted target; describe it in text ("the Share button in the toolbar").
8. **Respect reduced motion** for spotlight animations, confetti and progress bars (`web-animation-pitfalls`).
9. **Check touch targets and viewport on a phone**: tours are the most common overlay to break small screens (`responsive-layout`).

## 2.4 Performance
1. **Do not load the tour or checklist library on the critical path.** Load it after the first meaningful render, and only for users whose state needs it.
2. **One request for onboarding state**, returned with the session or the first page data, not a separate round trip per widget.
3. **Seed sample data in a queued job** and show progress; a request that creates hundreds of rows will time out (`background-jobs-conventions`).
4. **Avoid layout shift** when the checklist or banner loads after content; reserve space or render it from the initial data (`webperf`).
5. **Empty states are cheap**: no heavy illustration files for a state shown once; prefer inline SVG or a small reused asset.

## 2.5 Measurement
1. **Track steps by stable id** with start, done, skipped and dismissed events, so a funnel can say where people stop (`event-tracking-plan-pitfalls`, `funnel-and-cohort-definition-pitfalls`).
2. **Do not count sample data activity as activation.** A user who only touched samples has not reached value; exclude flagged records from the metric (§1.6).
3. **Do not put personal data in event properties**, and respect consent for analytics before sending (`telemetry-sensitive-data-pitfalls`).
4. **Judge changes with an experiment, not a feeling**, and beware that onboarding cohorts are small (`experiment-design-pitfalls`).

## 2.6 Tests
1. **First-run routing**: a new user, an invited user and a migrated user each land on the intended page; a second device does not replay the flow.
2. **Derived step**: create the data, assert done; delete it, assert open again; assert two tabs finishing together record one completion.
3. **Skip and resume**: skip each step, reload, assert state and the safe default; dismiss the checklist, assert it is reachable and reopens.
4. **Versioned tour**: a release without content change does not replay; one with change shows once; a missing anchor skips the step without error.
5. **Sample data**: assert flagged records are excluded from totals, exports, limits and outbound mail, and that one action removes exactly them with the right count.
6. **Empty kinds**: assert distinct output for loading, first-use, filtered, permission, error and offline; assert the error case never renders the empty copy.
7. **Invitation states**: pending, expired, revoked and wrong-account each render the right screen.
8. **Accessibility**: assert heading, button name, status text for steps, live-region announcement, focus return after a tour and a keyboard-only pass; run an automated check (`playwright-e2e-pitfalls`, `testing-library-query-pitfalls`).
9. **Locale**: render the empty states and checklist in the longest supported locale and a right-to-left one (`rtl-and-bidi-layout-pitfalls`).

## 2.7 Framework pointers (reference only)
1. **Laravel**: onboarding state as a small table or JSON column on user and workspace, steps derived in one service, sample seeding as an idempotent queued job (`laravel-conventions`, `laravel-idempotent-seeders`, `background-jobs-conventions`).
2. **React or Nuxt query layers**: onboarding state in the session query, steps derived from it; a tour library is a lazy import, and its focus and keyboard behaviour is checked against §2.3 (`data-fetching-state-conventions`, `react-nextjs-conventions`).
3. **Vuetify or similar kits**: stepper, progress and dialog components have their own accessibility defaults; verify, do not assume (`vue-nuxt-vuetify-conventions`).
4. **Mobile**: first-run permission prompts (notifications, location) are asked in context, after the user sees why, not on first launch (`flutter-conventions`, `flutter-notifications-background`).
5. **AI features** start with an empty prompt: see `ai-product-ux-pitfalls` for what that screen must teach.
