# § 6 — Tests

> Section 6 of `skills/inertia-conventions`. Read it when a page, a form or a shared prop is covered by a
> test, or when deciding what a feature test can and cannot prove about an Inertia app.

1. **A feature test for an Inertia route asserts the page component name and its props**, not a JSON
   body shape — Laravel's Inertia testing assertions (asserting the component and specific prop values)
   are the equivalent of a JSON-shape assertion on an API endpoint, just aimed at what Inertia actually
   returns.
2. **The two-tier split from `laravel-conventions` §9 still applies**: an Inertia-returning controller
   action is a feature test, the same as any other HTTP endpoint would be.
3. **The component-name assertion is a string comparison against a string, so it cannot catch a rename.**
   Rename the page file and forget the controller, and the test stays green while the browser gets a
   resolver error (§1.4). If page renames are frequent enough to matter, the cheap guard is a test that
   walks the rendered component names and checks a file exists for each — nothing else in the stack does.
4. **A validation failure is asserted as a redirect back plus the session's error keys, not as a JSON
   body.** The 422 becomes an errors prop only on an Inertia request (§3.11), so a test that posts
   without Inertia's own headers exercises the other branch: it can pass on the JSON shape while the page
   shows the reader nothing. Assert the keys the fields actually read, dot notation included (§3.4).
5. **Assert what must *not* be in the props, not only what must.** The props are published to whoever is
   viewing the page (§2.6), so the leak of an internal field, another tenant's row or a soft-deleted
   record is a defect the happy-path assertion cannot see — it only checks that the expected keys are
   present. One negative assertion per sensitive shape is what turns §2.6 from advice into a check.
6. **Shared data is in every page's payload, so one test on `share()` covers all of them.** It is the
   highest-leverage test in the block: a field added to the shared user object leaks to every page at
   once, and a single test asserting the exact shared shape fails the moment someone widens it. Assert
   the shape, not a subset — a subset assertion passes on every addition.
7. **The redirect after a mutation is part of the contract; assert the status and the target.** The
   status matters on its own: a `DELETE` that redirects with 302 instead of 303 deletes the row and then
   errors (§1.6), and a test asserting only "the row is gone" passes on exactly that bug. Assert the
   status code, the location, and the flash the target is supposed to show.
8. **A page-component test needs a props fixture, and the fixture is a copy of the server's shape.** It
   drifts the same way a hand-written interface does (§2.2): derive it from the same source the types
   come from, or keep the component tests deliberately shallow and let the feature test own the shape.
   A component suite green against a fixture the server stopped sending is worse than no suite — it
   reports on a page that no longer exists.
9. **What no feature test can prove is that the swap works in a browser.** An asset-version mismatch
   (§5.6), a component that renders server-side props fine and then throws on an event handler, a
   deferred prop read on first paint (§2.9): all of these return 200 with correct props. One smoke pass
   through a real browser on the critical path is what covers them, and it is a different tier — not a
   reason to widen the feature tests.
10. **A partial reload is testable, and worth testing where the page relies on one.** Request the page
    with a single prop asked for, then assert both halves: that the requested prop came back, and that
    the expensive one was not computed (§2.7). That second assertion is the whole point of the partial
    reload, and it is the one that silently stops holding when someone unwraps a closure.
11. **A prop assertion that only checks the key exists is not an assertion.** It passes when the value is
    null, an empty collection, or the wrong record entirely — which are the three outcomes a scoping or
    authorization mistake actually produces. Assert the value, and where the value is a list, assert what
    it contains for a user who should not see all of it.
