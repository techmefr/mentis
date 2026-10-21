# graphql-conventions — origin and source stamps

> Provenance of `skills/graphql-conventions`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

Block created 2026-10-02, every rule from a document **read that day** (rule B: mechanisms rewritten in the
house voice, no prose copied). A fact not found in a read source was left out rather than recited.

| Source (public repository, read 2026-10-02) | Licence | Used for |
|---|---|---|
| GraphQL website learning guides (`graphql/graphql.github.io`, `src/pages/learn/`, main branch): naming and design standards, schema design, pagination, global object identification, governance and versioning, error handling, authorization, performance, security, serving over HTTP | MIT (repository `LICENSE`, read) | §1 and §2. Rewrite with credit. |

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

## Verification pass 2026-10-20
Pages re-opened one by one (same repository, source branch `src/pages/learn/`, MIT licence unchanged). Note that there is no
`schema-change-management` page: the change rules come from `governance-versioning.mdx`, and the section name in the header of
section 1 should read as that page. Confirmed: naming table (casing, `is`/`has`, plural lists, no `get` prefix, `Input` suffix, mutation
naming patterns and the consistency remark), domain over database tables, custom scalar when and when not, cursor connections with
edges, `PageInfo`, opaque cursors, `Node` and root `node` field, two error channels with the business-error examples (the page says
inventory where we say stock), authorization in the business layer with a fully hydrated user, directives for generalised rules,
batching loader, trusted documents for first-party only, all demand limits (list size, depth, a separate smaller nested-list limit,
top-level fields and aliases, batch size), rate limiting and cost analysis with weights and budgets, input sanitising, error masking,
introspection as obscurity, OpenTelemetry, GZIP, POST body, GET for queries only, 4xx without a Content-Type, the Accept media type, URL
length limits with persisted documents.
Corrected: 2.3 (the guide puts field-level decisions after execution begins, not "none until execution"); 1.9 now carries only the
guide's two safe and three breaking changes, the rest marked as our extension; 1.10 offset wording.
Relabelled as ours: `[Item!]!` shape, input three-state advice, descriptions, small-list exception, per-request cache, removal date in the
deprecation reason. HTTPS, timeouts and private caching come from the security page, not the HTTP page.
Draft status: the HTTP page still carries a callout saying the over-HTTP specification is in development and not finalised on 2026-10-20,
so 2.5 stays the point most likely to move. The GraphQL-over-HTTP specification and the GraphQL specification were not opened.

Independent verification 2026-10-21: 17 checked, 17 matched, 0 corrected, 0 unverified
