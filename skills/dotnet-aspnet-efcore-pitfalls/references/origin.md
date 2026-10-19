# dotnet-aspnet-efcore-pitfalls: origin and source stamps

> Provenance of `skills/dotnet-aspnet-efcore-pitfalls`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us.

This block is meant to be folded into the same-topic sections of `dotnet-conventions` (web and EF
sections) when the branch `feat/antislop-lot` (PR 118) lands.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| ASP.NET Core docs: HttpContext, Kestrel options and security considerations | CC-BY-4.0, read 2026-10-08 | Not thread safe, accessor caution, header rule, `AllowSynchronousIO` default and warning, body buffering |
| ASP.NET Core docs: Data Protection (overview, key management, key encryption at rest, scaling on containers) | CC-BY-4.0, read 2026-10-08 | Application name default isolation, explicit location removes default encryption, key deletion warning, antiforgery failure when scaling out |
| ASP.NET Core docs: CORS, HTTPS enforcement and HSTS, antiforgery and CSRF | CC-BY-4.0, read 2026-10-08 | Any-origin and credentials warning, `RequireHttpsAttribute` on APIs, HSTS browser-only, dev certificate switch |
| ASP.NET Core docs: memory cache, HybridCache | CC-BY-4.0, read 2026-10-08 | Size limit rules, sliding with absolute, single-flight factory, key uniqueness |
| .NET docs: IHttpClientFactory | CC-BY-4.0, read 2026-10-08 | Two-minute default handler lifetime, singleton typed client warning, `PooledConnectionLifetime` |
| .NET docs: System.Text.Json nullability | CC-BY-4.0, read 2026-10-08 | Nullable annotation enforcement from .NET 9, opt-in switch, missing versus null |
| EF Core docs: tracking, migrations apply, efficient querying, simple logging, tags, lazy loading | CC-BY-4.0, read 2026-10-08 | Tracking default, migration trade-offs and locking from EF Core 9, buffering cases, expression indexes, logging levels, tag methods |

The unlicensed async-guidance repository was used for no phrasing.

## Corrections to the earlier review
EF Core 9 locks migrations, so "never run Migrate at startup" became a stated trade-off.

## Removed in the verification pass (no page supporting them)
"Synchronous IO disabled since 3.0" (the page gives only the default), the IIS mention, "do not put HTTPS
redirection middleware in front of an API" (narrowed to `RequireHttpsAttribute`), the antiforgery
"disable only on token endpoints" rule, `RespectRequiredConstructorParameters`, "wrapper-free predicates"
for `.Year`, `ToLower` and leading wildcards (narrowed to expression-over-column), and the default-TTL rule
for `HybridCache`. Earlier also dropped: HttpMethodOverride ordering, `PasswordHasher`, `Expression.Constant`
cache bloat, `nvarchar(max)` from missing length, the response `StreamWriter` flush rule.

## Not verified
1. **`HybridCache` first available version:** the page read does not state it in the part read; §4.3 tells
   the reader to confirm.
2. **Own guidance, flagged as such in the text:** accessor as last resort, list origins per environment,
   do not disable antiforgery, headers per request, explicit discriminator.
3. **`ReadFormAsync` rationale:** the page links to a reason that was not followed.

## Related blocks
`dotnet-conventions` §2, §3, §4 and §6, `security-hardening`, `api-design`.
