# firebase-rules-and-client-trust-pitfalls §2 — Keys, admin credentials, claims and functions

Source: own guidance throughout (no source was read; see origin). Names and defaults are the platform's; re-read before relying on them.

## 2.1 Public configuration and abuse
1. **The client configuration (project identifier, web key, sender identifier) is public by design;** it identifies the project, it does not grant access. Do not spend effort hiding it, and do not store a secret in the same file.
2. **What protects the project is the rules (§1) plus an attestation service and key restrictions.** Restrict the web key to the app's own referrers or bundle identifiers, and turn on the platform's app attestation for the products that support it so that requests from copied clients are rejected.
3. **Attestation is a brake, not a lock.** It reduces abuse by scripts; it does not replace rules.
4. **Set quotas and budget alerts** on the project, because an open endpoint is paid for by you (own guidance).

## 2.2 Administrator credentials
1. **The administrator SDK and service account keys bypass the rules entirely.** Anyone holding such a key has full access to the project.
2. **They live on servers only,** in a secret store, never in a client bundle, a repository, a mobile package or a function's public source. Search the repository history too.
3. **Prefer the platform's ambient identity** (the identity of the function or server runtime) to a downloaded key file, so there is no file to leak (own guidance).
4. **Rotate a key found in the wrong place at once,** because removing the file from the repository does not make it private again.
5. **Do not use administrator credentials in code that serves user requests unless you re-check the user's rights in that code.** The rules are not there to help you any more.

## 2.3 Claims, roles and token freshness
1. **Put authorization data (roles, plan, tenant) in custom claims set by a server, or in a document the rules read that clients cannot write.** Never in a profile field the user can edit.
2. **A change of claims reaches the user's token only after the token refreshes.** Force a refresh in the client after the change, or tolerate the delay (an hour is the typical lifetime; re-read it).
3. **Deleting or disabling a user does not invalidate tokens already issued** until they expire. Revoke refresh tokens, keep sensitive actions behind a recent-sign-in check, and for strict cases check in the rule or function that the account is still enabled.
4. **Claims have a size limit;** keep them to identifiers and flags, not profiles.
5. **Tenant isolation is a rule on every path,** with the tenant taken from the trusted claim; a missed path is a cross-tenant leak.

## 2.4 Callable and triggered functions
1. **A callable function that does not check the caller is a public endpoint.** Check authentication and authorization inside it, on every call.
2. **Validate every input in the function** as in §1.5, since the platform's call wrapper does not.
3. **Do not trust the data a trigger delivers as clean** when it came from a client-writable path.
4. **Make functions idempotent;** triggers can run more than once (`skills/serverless-edge-worker-pitfalls`, `skills/laravel-post-may-run-twice` for the same idea on another stack).
5. **Limit the cost an anonymous caller can cause:** concurrency caps, rate limits per user, and no unbounded fan-out from one request.
6. **Keep secrets for third-party services in the platform's secret store,** not in the function's configuration or source.

## 2.5 Authentication settings
1. **Turn on only the sign-in methods you use,** and know that anonymous sign-in widens who counts as signed in (§1.2.2).
2. **Check how email sign-in behaves for existing accounts:** the platform may reveal whether an email exists. Decide whether that is acceptable for the product (own guidance, re-read the current setting).
3. **Require email verification before treating an address as owned,** especially if rules or functions use the email for access (own guidance).
4. **Restrict the authorized domains** for redirects and, for multi-tenant products, restrict who may create accounts.
5. **Account linking and provider changes can merge identities;** test sign-in with two providers on the same email.

## 2.6 Checks (own guidance)
1. Search the repository, its history and the shipped client bundle for service account keys and administrator credentials.
2. Read each callable function and confirm the first lines check the caller and the input.
3. Change a user's role in the server, then confirm what a signed-in client can do before and after a token refresh.
4. Confirm quotas, budget alerts and key restrictions exist for the project.
