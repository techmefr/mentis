---
name: dotnet-aspnet-efcore-pitfalls
description: "Use when an ASP.NET Core or EF Core change touches HttpContext or IHttpContextAccessor, background work started from a request, request body IO, Data Protection keys behind several replicas, antiforgery, CORS with credentials, RequireHttps or HSTS, EF Core tracking defaults, running migrations at startup, buffering or non-sargable queries, query logging, IMemoryCache or HybridCache, HttpClient default headers, or System.Text.Json nullable handling."
---

# dotnet-aspnet-efcore-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the ASP.NET Core and EF Core traps that the broad conventions
in `dotnet-conventions` §3, §4 and §6 do not name: request-scoped objects used after the request, keys and
cookies that break when a second replica starts, a query that silently loads the table, a cache that
grows forever. The premise: **a web app runs as many instances, restarts without warning and serves many
requests at once, so anything that works on one laptop process is a hypothesis, not a fact**.

## When
- Reading `HttpContext`, request headers or the body anywhere except the request path itself.
- Adding a cookie, antiforgery, CORS, HTTPS redirect or a certificate to a service that runs in a container.
- Changing how EF Core tracks, migrates, logs or materialises.
- Adding a cache, or changing `HttpClient` or JSON serialisation settings.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Request context: HttpContext lifetime, threads, body IO | code reads the request outside the handler or starts background work | [`01-request-context.md`](./references/01-request-context.md) |
| 2 | Security configuration: Data Protection keys, antiforgery, CORS, HTTPS and HSTS, dev certificates | the service gets a second replica, a cookie, a form post or a cross-origin caller | [`02-security-configuration.md`](./references/02-security-configuration.md) |
| 3 | EF Core: tracking default, startup migrations, buffering, sargable predicates, logging | a query, a DbContext option or a deploy step changes | [`03-efcore.md`](./references/03-efcore.md) |
| 4 | Clients, caching, JSON: shared HttpClient headers, memory cache limits, HybridCache, nullable handling | a cache, a typed client or a serializer option is added | [`04-clients-caching-json.md`](./references/04-clients-caching-json.md) |

## Output / checkpoint
Each rule was exercised: two replicas were started and a cookie issued by one was read by the other (§2),
the migration deploy step ran from a clean database (§3), the query was inspected in its generated SQL
(§3), and the cache was filled past its limit (§4). A rule checked by reading code only is not verified.

## Guardrails
- Never store `HttpContext` in a field or use it after the request ends (§1.1).
- Never enable a global no-tracking default without opting writes back in (§3.1).
- Never apply migrations from several instances at startup without a lock and a rollback plan (§3.2).
- Never combine credentials with an allow-any or always-true origin policy (§2.3).
- Versions: each rule names the .NET or EF Core version it needs. Nothing was run while writing this block.
- Broader authorisation, logging and EF design rules stay in `dotnet-conventions` §3 and §6;
  security review beyond the points here belongs to `security-hardening`.

## Origin
Rewritten from the ASP.NET Core and EF Core documentation (CC-BY-4.0), cross-checked against MIT skill
files (read 2026-10-08). 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md). It is meant to be folded into the same-topic sections of
`dotnet-conventions` when the branch `feat/antislop-lot` (PR 118) lands.
