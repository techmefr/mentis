# postgres-operations-and-exposed-api-pitfalls §3 — Tables reachable through a generated API

Sources: the security checklist of the `supabase` skill and the `security-rls-basics`, `security-rls-performance` and `security-privileges` rules of the `supabase-postgres-best-practices` skill in supabase/agent-skills at c9be0e9, read 2026-10-20. Vendor-specific names (`anon`, `authenticated`, the user-id function) are those of that platform; the principles hold for any API generated from a PostgreSQL schema.

## 3.0 Is a data API exposed at all? (own guidance)
1. **Find the host the application connects to.** Read the connection variable names and the example configuration, never a real secret. A host belonging to a platform that generates a REST or GraphQL layer from the schema is a candidate; a plain database host reached only through the application's own server routes is not.
2. **Look for the exposure setting.** In the platform's configuration file or project settings, find whether the data API is enabled, which schemas it serves, and which keys the clients ship. No API section, or an API switched off, plus no client holding a database key, means no exposed schema.
3. **Check what the browser or app calls.** Grep the client code for direct calls to the data API host or for a client library of the platform used to read tables. Calls only to the application's own routes close the question.
4. **Write the verdict with its evidence:** "exposed: schema, key shipped to clients" (go on with §3.1) or "not exposed: <what you read>" (stop). Absence of policies in the migrations is correct for a database only the server reaches and a finding for an exposed one; the verdict decides which.
5. **Identity-only use does not expose data.** A platform used just for sign-in, with its service key on the server, is not an exposed schema; check that the service key never reaches a client (§3.4, point 4).

## 3.1 Two separate locks: reach and rows
1. **A table can be reachable or not (grants), and rows can be visible or not (row-level security).** They are independent: an inaccessible table is a missing grant, an empty result on an accessible table is usually a policy. Check which one before editing either.
2. **A newly created table may or may not be exposed automatically,** depending on the project's API settings (on older projects new objects in the public schema receive default grants for the API roles, and a project setting can switch that off; the vendor announced a move to opt-in). When a SQL-created table is "not found" by the API, look at the exposure setting and the explicit grants to the API roles before suspecting the code.
3. **When access is granted to the public API roles, enable row-level security on the table in the same migration.** Every table in an exposed schema gets it; for a private schema it is defence in depth. A table with security enabled and no policy returns nothing, which is the safe default (`skills/sql-conventions` §6.7).

## 3.2 Policies that actually restrict
1. **A policy limited to the "authenticated" role checks that someone signed in, not whose row it is.** Combine the role with an ownership test on the row (the user id equals the owner column), or any signed-in user reads every row.
2. **An update policy has two expressions: a filter on the existing row and a check on the new row.** When only the filter is written, the manual says it is reused as the check, so the new row must also pass it; write the check explicitly when the rule for the new row differs (an allowed set of values, a fixed owner), and test an attempted reassignment. A failed filter skips the row silently, a failed check raises an error.
3. **An update or delete that reads columns also needs a select policy to pass,** which in practice means any statement with a filter, a returning clause or a column on the right of an assignment (the manual's per-command table). A row that fails the filter is skipped without an error, so the symptom is zero rows changed; a returning clause that hits a hidden row errors instead.
4. **Name the target role on the policy rather than testing the role inside the expression.** The vendor deprecated the in-expression role test, and it also misbehaves when anonymous sign-ins are on, because anonymous users carry the signed-in role.
5. **Wrap the identity function in a sub-select and index the owner column** (`skills/sql-conventions` §6.7). The source states large speed-ups; none is recited here, measure on your data.
6. **Views read with their owner's rights** (`skills/sql-conventions` §6.8): on a version that supports it, create them to check the caller's permissions, or keep them out of exposed schemas.

## 3.3 Privileged code
1. **A privileged function in an exposed schema is a public endpoint:** functions are executable by everyone by default (manual, and the platform's own hardening guide), so the API roles can call it. Revoking execute inside one schema does not remove that global default; the platform guide changes it through default privileges for the creating role, after which callers that policies rely on need an explicit grant. In the privileged function, pin the search path with the temporary schema last, and create the function and revoke public execution in one transaction. Keep such functions in an unexposed schema, check the caller's identity inside, revoke execution from everyone and grant to named roles (`skills/sql-conventions` §6.6).
2. **Never add the privileged attribute to make a permission error go away.** It removes the access control and leaves the cause in place.
3. **Give the application login role only the grants it needs,** read-only roles separate from writer roles, and revoke the default public access on the schema (`skills/sql-conventions` §6.5).

## 3.4 Claims and sessions
1. **Never authorize from a claim the user can edit.** On the source's platform the user-editable metadata can appear in the token; authorization data belongs in the application-controlled metadata.
2. **A token stays valid after its user is deleted,** until it expires. Revoke sessions first, keep lifetimes short for sensitive actions, and for a strict guarantee check the session still exists on sensitive operations.
3. **Claims are not fresh until the token is refreshed.** A role change made in the database does not reach a signed-in user's token at once; design the change to tolerate the delay, or force a refresh.
4. **Never ship the service key or a secret key to a public client,** and a build-time public variable is shipped (`skills/react-native-expo-pitfalls` §2). Prefer the publishable key in clients and scoped access tokens for tooling and CI.
5. **Storage objects follow the same logic:** the source states that replacing a file (upsert) needs insert, select and update policies together; with insert alone, new uploads work and replacements fail without a clear error.

## 3.5 Checks (own guidance)
1. For each table in an exposed schema, record: grants to the API roles, whether security is on, and the policy per command. A gap is a finding.
2. Test as a second ordinary user: they cannot read, update or reassign the first user's rows, and an update on a row they cannot see returns zero rows.
3. Search the repository and the shipped client bundle for the service key.
