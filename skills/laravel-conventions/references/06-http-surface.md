# laravel-conventions §6 — HTTP surface

> Section 6 of `skills/laravel-conventions`. Read it when a route, a controller action, a FormRequest, a response shape. The other sections and the guardrails stay in `SKILL.md`.

**Before applying this section's REST/resource-routing point, or an installed catalogue's stricter
version of it (e.g. a mandatory REST package), check the specific controller** — what it returns, where
it's routed — **not just whether the project depends on that package.** A project can genuinely run
Inertia for its pages and a REST package for a separate real API surface at the same time; the package
being installed doesn't make every 5-verb controller a REST endpoint, and an Inertia page controller
(no separate API, a controller returns a page and its props directly) is exactly the shape this catches
wrong if the check stops at the project level. See `skills/inertia-conventions` §4 before applying this
section wholesale to that architecture.

1. REST routes follow one consistent URI structure across the app, declared through the framework's resource
   routing rather than hand-rolled verb by verb.
2. Standard CRUD on a model is declared through the resource/REST mechanism the project standardises on — a
   hand-rolled CRUD stack for a plain model is five endpoints of avoidable code and a sixth behaviour that
   differs.
3. **Validation in a FormRequest**, with each field's rules expressed as an **array** of entries rather than
   a pipe-delimited string: a string breaks the moment a rule contains a delimiter, and an array diffs
   cleanly.
4. A response carries a **status/type and a human-readable message**, not just an HTTP code: the frontend has
   to display something.
5. User-facing email to a user goes through a notification, not a direct mail send: the notification owns the
   channel decision and the user's preferences.
