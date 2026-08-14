# flutter-conventions §5 — Navigation

> Section 5 of `skills/flutter-conventions`. Read it when a route, back handling, a deep link. The other sections and the guardrails stay in `SKILL.md`.

1. **Centralised declarative routing**, one place that maps routes to screens, rather than imperative pushes
   scattered across widgets. Arguments are typed, not passed as an untyped map.
2. Guards/redirects (auth, onboarding) declared with the route, not checked in each screen's `initState`.
3. Deep links and notification taps are entry points into the same route table, including the cold-start
   case — the tap that launches the app is the one that's usually forgotten.
4. Back handling is explicit where it matters: confirm before leaving a screen with unsaved changes,
   intercept the system back deliberately, and never trap the user with no way out.
5. Tabbed/bottom navigation **preserves each tab's state and scroll position** across switches — losing a
   half-filled form on a tab switch reads as a broken app.
