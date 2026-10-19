# dotnet-container-runtime: origin and source stamps

> Provenance of `skills/dotnet-container-runtime`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation and reading, never run by us. No image was built and no process
was started while writing it. mentis `devops-conventions` has no .NET section; this block is new.

## Sources (all read 2026-10-08, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| The .NET Docker repository: README, globalization sample, platform build sample, distroless and image documents | MIT, read 2026-10-08 | Port 8080 from .NET 8, `$APP_UID`, `ASPNETCORE_HTTP_PORTS` in the base image, ICU per image list, SqlClient and invariant mode, tzdata effects, `$BUILDPLATFORM` pattern |
| The .NET runtime configuration for garbage collection | CC-BY-4.0, read 2026-10-08 | 75% heap hard limit percent default under a container limit, workstation default, `System.GC.Server`, DATAS default from .NET 9, decimal and hexadecimal syntax, per-process advice |
| The ASP.NET Core HTTPS documentation | CC-BY-4.0, read 2026-10-08 | Development certificate in images and the environment switch |

## Corrections to the earlier review
The DATAS default is stated per version from the GC page (enabled by default from .NET 9).

## Removed in the verification pass (no page supporting them)
The `-a $TARGETARCH` argument and the SDK container publish target, the thread pool minimum advice, the
concurrent GC advice, the claim that a non-root user cannot bind a low port, and the `TimeZoneNotFoundException`
type name (the sample says only "an exception").

## Not verified
1. **Own guidance, flagged as such in the text:** SDK-then-runtime stages, restore layer ordering, pinned
   base tag, writable data directory, limits on every container, measure before tuning, no secrets in `ARG`
   or `ENV`, UTC at the edge.
2. **ICU image list and tzdata contents** are as of the sample text read; image variants change.
3. **Whether the 75% default applies to every GC mode** is not stated in the part read; §2.1 words it as the
   page does.

## Related blocks
`node-container-runtime` (same layer for Node), `devops-conventions`, `dotnet-conventions` §9,
`dotnet-aspnet-efcore-pitfalls`.
