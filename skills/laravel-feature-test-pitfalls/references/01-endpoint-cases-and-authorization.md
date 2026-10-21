# laravel-feature-test-pitfalls §1 — Endpoint cases and authorization

> Part 1 of `skills/laravel-feature-test-pitfalls`. Read it when an endpoint's tests are planned or reviewed.
> Sourced from `.ai/laravel/skill/testing-best-practices/rules/endpoint-tests.blade.php` and
> `security.blade.php` in `laravel/boost` (commit `f1411f9`), read 2026-10-16, the variant for PHPUnit.
> Sentences marked "own guidance" are ours.

1. **Cover the six cases an endpoint has.** The source's list, each a separate test where it applies: the
   request has missing or invalid authentication; it comes from another tenant, team or organisation; the user
   has an insufficient role or permission; the request does not satisfy a route or scope constraint; the
   request fails validation; and the request is valid, asserting both the response and the persisted state.
   Own guidance: write the list in the pull request with the test name next to each case, and the reason next
   to any case that does not apply.
2. **Assert what the application actually does, not a generic code.** The source's example: an API answers `401`
   for a missing or invalid token, while a browser endpoint redirects to the sign-in route. It also says to
   choose an assertion by the subject of the check (status, header, redirect, JSON body, session, validation
   error, view) and to use the named assertion Laravel provides for it, confirming the name in the HTTP
   testing documentation rather than guessing. Own guidance: a named assertion reports what differed; a
   status-only check cannot tell a redirect to sign-in from a redirect to the home page.
3. **Another tenant's record is a "not found".** The source says to assert the status returned for a
   cross-tenant request, and to use `404` rather than `403` when a tenant must not learn that another tenant's
   record exists, since `403` confirms its existence. Own guidance: assert the same status for a record that
   does not exist and for one that belongs to someone else, so the two cannot be told apart. The framework
   documents the same pattern for authorisation: a gate or policy can answer with an alternative status, and
   `denyAsNotFound` is offered for the 404 case (Authorization, Customizing the HTTP Response Status).
4. **Test the permission matrix at the policy, and one refusal over HTTP.** An HTTP test shows that the endpoint
   performs authorisation but cannot say which mechanism refused: middleware, a policy and an explicit abort
   can all answer `403`. The source's rules: assert the complete matrix against the policy or the gate, so a
   failure names the rule that is wrong; write one HTTP test for one refused role to show the endpoint calls
   the authorisation; and use the project's helper that asserts the ability and arguments of the gate if one
   exists. Own guidance: a matrix repeated across endpoint tests is the first thing to delete from a
   review, as its failure never says which rule broke.
5. **Test each security boundary where user input has an effect.** The source says a defect at such a
   boundary is hard to see, because the feature keeps working, and lists the cases: another tenant's record; each
   unprivileged role (data provider over the roles the endpoint must refuse); escaping of user-provided content
   in HTML and mail, using names and every free-text field the template prints, asserting that dangerous
   characters are escaped and the raw value is absent, without asserting an exact entity for a quote (Markdown
   and mail CSS inliners can decode it); injection into dynamic query parts such as sort columns, filter fields
   and sort directions; and an unexpected key in a payload or configuration array, since a merge that
   accepts every key can set an attribute the user must not control.
6. **A browser test is for behaviour a request cannot reach.** The source reserves real-browser tests for
   JavaScript behaviour such as modals, drag and drop, live search and client-side validation, because they are
   slower and fail for unrelated reasons; they should assert what the user sees and what was saved, and wait
   for a state rather than a fixed number of seconds, which fails on a slower machine. The plugin-specific
   advice in the source (a console-error assertion in every browser test, the wait default, screenshots
   directory, key-code and frame details) belongs to the source's Pest browser plugin and is not restated.
