---
name: firebase-rules-and-client-trust-pitfalls
description: "Use when an app talks to a backend-as-a-service directly from the client (Firebase first: Firestore, Realtime Database, Storage, Auth, callable functions): security rules that are open or only check sign-in, rules that are not filters, public client keys and App Check, admin credentials, custom claims and sessions, field validation on write, and testing rules in an emulator."
---

# firebase-rules-and-client-trust-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for backends that have no server of yours between the client and the data.
The premise: **when the client talks to the database directly, the rules file is the whole backend**: a rule that
says "allow if signed in" lets every user read every document, a test-mode rule that was never replaced lets the
whole internet do it, and the client's keys are public by design. The same reasoning for a PostgreSQL-based
platform (grants, row-level security, key types, token claims) is already in `postgres-operations-and-exposed-api-pitfalls`
§3; read that one for Supabase and similar. Generic client-side trust rules are in `security-hardening`.

## When
- An app reads or writes a managed database, file store or function directly from a browser or mobile client.
- A rules file, a storage rule, a callable function or an authentication setting is created or changed.
- A project was started in a "test" or "development" mode and is going to real users.
- A key or credential file is found in a client bundle or a repository.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Open and test-mode rules, sign-in versus ownership, rules versus queries, cascade, per-operation rules, field validation, files, testing in an emulator | a rules file or a client query is written or reviewed | [`01-rules-that-actually-restrict.md`](./references/01-rules-that-actually-restrict.md) |
| 2 | Public config and abuse limits, admin credentials, claims and token freshness, callable functions, authentication settings, limits and cost | keys, credentials, roles or server-side functions are involved | [`02-keys-admin-claims-and-functions.md`](./references/02-keys-admin-claims-and-functions.md) |

## Output / checkpoint
Each section ends with its own checks. For a change touching this block: no rule allows everything or only checks
sign-in, each collection and file path has a rule per operation with an ownership or role test, rules were tested
in an emulator with a second user and an anonymous caller, and no administrator credential is reachable by a client.

## Guardrails
- Replace every development-mode rule before real users arrive (§1.1). Never ship an expiry date as the security plan.
- Test ownership, not sign-in: the user id must equal the owner of the data (§1.2). Never treat "signed in" as "allowed".
- Write rules per operation, and validate the shape of what is written (§1.4, §1.5). Never use one catch-all write rule.
- Keep administrator credentials on servers only, and remember they bypass the rules (§2.2). Never bundle them in a client.
- Put authorization data where the user cannot edit it (§2.3).
- Platform limits, defaults and prices change; re-read the current documentation before relying on a name or a number (🟡, nothing here was deployed).

## Origin
Own guidance, from the craft of securing client-direct backends; no source was read. Official platform
documentation was not opened (licence not verified). See [`references/origin.md`](./references/origin.md).
