# graphql-conventions — origin and source stamps

> Provenance of `skills/graphql-conventions`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

Block created 2026-10-02, every rule from a document **read that day** (rule B: mechanisms rewritten in the
house voice, no prose copied). A fact not found in a read source was left out rather than recited.

| Source (public repository, read 2026-10-02) | Licence | Used for |
|---|---|---|
| GraphQL website learning guides (`graphql/graphql.github.io`, `src/pages/learn/`, main branch): naming and design standards, schema design, pagination, global object identification, schema change management, error handling, authorization, performance, security, serving over HTTP | MIT (repository `LICENSE`, read) | §1 and §2. Rewrite with credit. |

**Read but not used for rules:** the GraphQL specification text itself, the GraphQL-over-HTTP specification
(cited by the guides, still a draft, not read), the federation, subscriptions, caching, file-upload and
validation guides, the schema-review and governance pages beyond the change-management one, and the
GraphQL-ESLint rule documentation (a clone exists but no rule was read, so the lint tool is named only
generically in §1.12). Left out: federation and gateways, subscriptions transport, client-side caching, any
server library specifics.

**Version stamp.** The guides were read on their main branch and carry no version. They state that naming
patterns are conventions and that nullability tooling (semantic non-null, client error handling) is still
evolving; the HTTP media type for responses was in a draft specification, which makes §2.5 the point most
likely to move. Expiry: when the GraphQL-over-HTTP specification is published as final, or at the project's
next reread (`skills/source-freshness` §2.1), re-read §2.5 and §2.6 first.

**Status.** 🟡, "base to confront with the real thing", like `go-conventions`. Nothing here was run against a
GraphQL service.
