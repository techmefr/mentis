# § 6 — Injection, privileges, row-level security

> Section 6 of `skills/sql-conventions`. Read it when SQL is built from input, a role or a grant is created,
> or row-level security is used. It states the database half; the application half (validation, session,
> secrets) is `skills/security-hardening`.

1. **Pass values as parameters, always.** A statement text that contains no input, with the values bound
   separately, lets the database tell code from data whatever the value says. That holds in every language and
   through most abstraction layers, which have their own string-built escape hatches (a raw fragment, a
   "where raw"): a value going into one of those is the same defect. Quoting and escaping is the
   strongly discouraged fallback, since it depends on knowing the engine's and the connection's exact rules.
   PostgreSQL's parameter-passing call also refuses a string that holds more than one statement, which is a
   useful second line.
2. **Identifiers and keywords cannot be parameters; allow-list them.** A table name, a column to sort by, a
   sort direction or an operator that comes from input is selected from a fixed list in the code, and the list
   entry (not the input) is what reaches the statement. Never pass input through an identifier-quoting
   function and call it safe.
3. **A stored routine is not safe by being stored.** It is safe if it takes parameters and does not build a
   statement from strings inside. A routine that concatenates its arguments into dynamic SQL is the same
   defect, now harder to find.
4. **Give each role only what it needs, and keep the roles apart.** The application connects as a role that
   can read and write its own tables and nothing else: no ability to create or alter objects, no superuser, no
   access to other schemas. A separate role runs migrations (it needs the object-changing rights and the
   timeouts of `05`), a read-only role serves reporting, and a break-glass administrative role is not in any
   application's configuration. A leaked application credential then costs one application's data, not the
   server.
5. **On PostgreSQL, the catch-all role matters.** `PUBLIC` is an implicit group that contains every role,
   including those created later; a privilege granted to it is granted to everyone, and new functions are
   executable by it by default. Revoke what you do not mean to share and grant to named roles.
6. **A privileged routine is a public entry point unless you close it.** A function declared to run with its
   owner's rights (security definer) runs with the owner's privileges, bypassing the caller's restrictions,
   including row-level security if the owner bypasses it. Never make a function privileged to get past a
   permission error; if one is needed, fix its search path to trusted schemas (so a hostile object in a
   writable schema cannot shadow the ones it calls), revoke execution from the catch-all role, grant it to
   named roles only, and keep it out of any schema reachable through an auto-generated API.
7. **Row-level security is a second lock, not the first.** Enable it on a table and, with no policy defined,
   nothing is visible or updatable (default deny). Superusers and roles with the bypass attribute skip it, and
   so does the table's owner unless the table is set to apply it to the owner, so the application must not
   connect as the owner or a bypass role. Policies are written per command (an update also needs to see the row,
   so it needs a select policy as well), target roles explicitly, and are indexed like any predicate: a policy
   expression evaluated per row is a query cost, so wrap a stable function in a sub-select so it is evaluated
   once, and index the column the policy filters on.
8. **A view reads with its owner's rights unless told otherwise.** A view over a protected table can expose
   rows the caller could not read directly. From PostgreSQL 15 a view can be created to check the permissions of
   the user running the query; on older versions, withhold access to the view or keep it in a schema the
   callers cannot reach. Application-level multi-tenancy (`skills/laravel-tenant-context-by-default`) and
   row-level security are complementary: the first states the tenant, the second is the net behind it.
9. **Authentication is never "trust" over the network.** The access-control file's trust method lets any
   connecting client claim to be any user, including the superuser; allow it at most for a local test, and
   use a password method with a modern hash (scram) or a certificate for anything reachable over TCP. Require
   TLS for remote connections. Credentials come from the secret manager, not from the repository
   (`skills/security-hardening` §4).
10. **Audit what you cannot prevent.** Log connections, privilege changes and failed authentications, keep the
    statement log free of bound values that are personal data (`skills/observability-instrumentation` §2.4),
    and use the engine's audit extension where a regulation requires a record of access.

**Sources:** the PostgreSQL manual (libpq parameter passing, GRANT and the PUBLIC pseudo-role, CREATE
FUNCTION security-definer notes, CREATE VIEW security-invoker option, row security policies and bypass rules)
and the PostgreSQL community "don't do this" list (trust authentication), read 2026-10-02; the OWASP SQL
injection prevention cheat sheet (CC-BY-SA, idea only: parameterisation first, allow-listing for what cannot be
parameterised, stored routines not inherently safe, escaping discouraged); a platform vendor's published
row-security guidance (MIT) for the owner/bypass, view, update-needs-select and per-row evaluation traps.
Version-bound: the security-invoker view option from PostgreSQL 15. Point 10 is reasoning of ours.
