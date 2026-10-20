# dashboard-ui-pitfalls §2 — States, roles, access and tests

Sources: own craft, except §2.5, checked against WCAG 2.2 (W3C Recommendation of 12 December 2024, facts only; success criteria cited as SC). Status messages (SC 4.1.3) were not read; point 2.5.5 stays unsourced.

## 2.1 States per widget
1. **Each widget loads, fails and empties on its own.** One slow or failing query marks one card with a retry; the page, the range control and the other cards stay usable. Symptom: a white page or a spinner over everything because one aggregate times out.
2. **Five renderings per widget**: loading (skeleton of the final size), no data yet (what to do to get some), no data in this range (change the range), failed (message plus retry, never a zero), and stale (data shown with its age).
3. **Never show zero for an error or an unknown.** A failed card that renders 0 reads as a business result; show a dash and the failure.
4. **Keep the last good value on a failed refresh**, marked stale, instead of replacing it with an error card.
5. **Reserve space** so cards do not shift when data arrives or when one fails; a dashboard that rearranges itself while being read invites mis-clicks.
6. **Order loading by importance**: render the headline cards first and lazy-load below-the-fold widgets when they near the viewport, so the page is useful early.
7. **Fetch widgets in parallel with bounded concurrency**, and batch where one endpoint can return several small numbers; fifty requests on load is a design failure.
8. **Partial permission is a state**: a widget the viewer may not see is absent, not "access denied" shown to everyone, unless the denied state is part of an upsell by decision.
9. **First-run and empty accounts** get a guided empty dashboard (what the cards will show, how to start), not a wall of zeros.

## 2.2 Layout and customisation
1. **Define the information hierarchy**: three to five headline numbers, then supporting detail; every card must lead to a decision or an action, otherwise remove it.
2. **User-arranged dashboards persist per user and per role template**, with reset to default (`data-table-ui-pitfalls` §2.2 for the same versioning rules when widgets change).
3. **A new widget version must not break a saved layout**: unknown widget ids are dropped, new ones are appended to the end.
4. **Narrow screens re-flow cards in a meaningful order**, not a shrunken desktop (`responsive-layout`).
5. **Print and export**: if the dashboard is exported or emailed, it carries the range, the zone and the as-of time, because the page context is gone.

## 2.3 Role-based views
1. **A role view is a server decision.** The server decides which widgets exist for the viewer and computes every number under the viewer's data scope (own records, team, company). Hiding a card in the client while the endpoint answers anyone is a data leak.
2. **Permissions gate widgets, not roles by name** (`laravel-permissions-not-roles`); new roles then need configuration, not code.
3. **Scope the numbers, not only the widgets.** A "total customers" card must be the viewer's scope or the company's by a stated rule; two roles with the same card and different numbers need a label ("Your team").
4. **Aggregates can leak**: a count over a filter the viewer cannot read reveals presence; a small group count can identify a person. Apply minimum group sizes where privacy matters, and decide it with the data owner.
5. **Impersonation and "view as"** show the target's scope and a visible banner, and are logged.
6. **Per-role default ranges and layouts** are templates; the user can still change the range, within scope.
7. **Cache keys carry the scope** (§1.5) and invalidation covers permission changes.
8. **Drill-down targets enforce the same scope** (§1.4); a card and its list never use two different rules.

## 2.4 Refresh and cost
1. **Budget the page**: queries per load, worst-case query time, and what a tab left open all day costs; measure on realistic data.
2. **Precompute heavy aggregates** (summary tables, scheduled jobs) and show the as-of time; do not run a full-table aggregate per page view.
3. **Cap and index the drill-down filters** the dashboard offers; a range control that allows five years on a large table is a denial of service by a click.
4. **Debounce range and filter changes** and cancel the superseded requests (`filters-search-and-saved-views-pitfalls` §2.2).
5. **Deduplicate identical requests** across widgets that share a query.

## 2.5 Accessibility
1. **A card has a heading and its value in text**, with the unit, the range and the delta read as words ("Overdue invoices, 120, up 8 from the previous 30 days"), not a number floating beside a coloured arrow.
2. **Charts need a text alternative** (SC 1.1.1: non-text content needs an equivalent text; SC 1.3.1: information shown visually must also be available as text or structure): a short description of what it shows and the main reading, plus a data table or the underlying list reachable by keyboard; hover-only tooltips are not accessible, so show values on focus too.
3. **Colour is never the only encoding** (SC 1.4.1): patterns, labels or direct values (`accessibility`); graphical parts needed to understand the chart, such as series lines and bars, need at least 3:1 contrast against their neighbours (SC 1.4.11, level AA).
4. **Interactive points and cards are keyboard-operable** (SC 2.1.1) in a sensible order, with a visible focus.
5. **Live updates are announced sparingly**: a polite live region for meaningful changes, never for every tick.
6. **Respect reduced-motion** for count-up animations and chart transitions (SC 2.3.3, level AAA, asks that interaction-triggered motion can be switched off).
7. **Range and comparison controls are labelled**, and their result is announced once settled.
8. **Auto-updating widgets can be paused.** Information that starts by itself and refreshes alongside other content needs a way to pause, stop, hide or slow it (SC 2.2.2, level A), unless the updating is essential. Check: a polling widget has a pause control or a visible interval setting.

## 2.6 Mistakes of presentation
1. **Too many cards**: users stop reading; cut until each remaining card answers a question someone asks weekly.
2. **Vanity numbers without a threshold or target** leave the user unable to say if it is good; show the target or the previous value.
3. **Rounded numbers that do not add up**: totals computed from rounded parts differ from the shown total; round at display, keep exact values in calculation.
4. **Mixed scopes on one row of cards** (my tasks, company revenue) with no label.
5. **Dark patterns**: a red badge for something unactionable trains people to ignore alerts; alert only on what someone can and should act on.

## 2.7 Tests
1. **Number against list**: seed known rows, assert each card equals the drill-down count under the same filter, zone and user.
2. **Boundaries**: rows at midnight, month end and daylight-saving changes in two zones; assert the range edges.
3. **Role scope**: for each role and a seeded dataset, assert the numbers equal the scoped counts and that calling the endpoint directly as a lower role is refused or scoped.
4. **Cache scope**: warm the cache as one role, request as another, assert different numbers.
5. **Failure isolation**: make one widget endpoint fail or time out; assert the others render and the failed one shows a retry, not zero.
6. **Freshness**: freeze the pipeline time; assert the as-of text and the stale mark past the threshold.
7. **States**: loading skeleton size, no data, no data in range, error, stale for one widget.
8. **Accessibility**: heading and text for a card, chart text alternative, keyboard path to a drill-down, reduced-motion.
9. **Definition parity**: a test that the card query and the export query come from the same function.

## 2.8 Framework pointers (reference only)
1. **Laravel**: one class or query object per metric returning value, unit and as-of; grouped queries for aggregates; scope queries by permission in that class; cache with a key that holds scope and range (`laravel-cache`, `laravel-aggregate-in-database`, `laravel-tenant-context-by-default`).
2. **Nuxt or Vue**: one composable per widget with its own loading and error state, fetched in parallel, with the range held in the router query (`vue-nuxt-vuetify-conventions`, `data-fetching-state-conventions`).
3. **Vuetify**: cards, skeleton loaders and tooltips exist, but keyboard access and text alternatives are yours to add.
4. **Charts**: choose the type by the question (`chart-choice-pitfalls`) and check palette and contrast before shipping.
