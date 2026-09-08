# § 3 — Access control on every new route

> Section 3 of `skills/security-hardening`. Read it whenever a diff adds or changes an endpoint, a
> consumer or any other entry point. `business/data-protection` cites this section by number.

1. **Every endpoint declares its authorisation**, and new endpoints are the ones that get forgotten:
   a route added to an already-protected controller inherits nothing automatically in some frameworks.
   The failure is silent in the direction that matters — the endpoint works, returns the right data to
   the developer who wrote it, and the missing declaration is visible only to someone who reads the
   route table looking for absences.
2. **Check ownership, not just authentication.** A logged-in user requesting record 42 must be shown
   to be entitled to record 42. Enumerable identifiers make this the most commonly exploited flaw in
   an otherwise well-authenticated app.
3. **Scope in the query.** Detail in `auth-session-conventions` §3.3: filtering after fetching means
   the data was already read, and one branch that forgets to filter leaks it.
4. **Authorise before the work, not after it.** A handler that loads the record, computes a response
   and then checks entitlement has already spent the read, and any early return, log line, cache write
   or timing difference in between is an oracle. It is also the shape that leaks through an error: the
   exception thrown while building the response arrives before the check.
5. **The default has to be deny.** An entry point with no declaration should fail, which is a
   framework-level decision — a fallback policy, a default-protected router, a test that enumerates
   routes — rather than a habit. Without it, "every endpoint declares its authorisation" is
   aspirational: nothing detects the one that does not.
6. **A permission is not a role, and the check names the permission.** Checking for a role scatters the
   policy across every handler that mentions it, so adding a role means finding every such handler;
   checking a named capability keeps the mapping in one place. The observable failure of the role form
   is a new role that silently has less access than intended, or more.
7. **Authorise the write on the row, not only the collection.** Permission to update *some* records is
   the common shape, and a handler that checks the verb and not the target lets a caller update
   somebody else's row with their own valid credentials — the same flaw as point 2, on the path where
   it does damage rather than disclosing.
8. **Every field of a response is subject to the same decision as the endpoint.** A serialiser that
   returns the whole record hands over the columns the caller is not entitled to — an internal note, a
   cost price, another user's email — and the interface not showing them is not a control. What the
   endpoint returns is an allow-list, chosen per caller where the entitlement differs.
9. **Filters, sorts and includes are part of the attack surface.** A caller-supplied relation to
   include, or a filter on a related table, can reach data the endpoint's own check never considered,
   and the whitelist for those (§1.3) is an authorisation decision rather than a validation detail.
10. **Not every entry point is an HTTP route.** A queue consumer, a scheduled job, a webhook receiver,
    a websocket message and a server-side action are not reached by the HTTP middleware at all, so each
    carries its own check. The webhook is the sharpest case: its authorisation is signature
    verification, and a receiver that trusts the payload's own claim of who it is has none.
11. **An identifier that can be guessed is a reason for stronger checks, not for hiding it.** Replacing
    a sequential id with a random one raises the cost of enumeration and changes nothing about
    entitlement; treating the opaque id as the control is how point 2 comes back in a form that looks
    solved.
12. **The negative test is the proof.** A positive test passes identically with no authorisation at
    all, so the only test that shows a policy is wired is the one asserting the wrong user is refused —
    and that the refusal is a clean status, not a crash or an empty success (§5.2). This is also the
    evidence this block owes at its checkpoint.
