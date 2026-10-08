# dotnet-container-runtime §3 — Globalization and time zones

Slim images leave out the libraries and data that culture and time zone calls need. This section follows
the official .NET Docker samples.

## 3.1 ICU
1. **Some official images include ICU and some do not.** Included: Alpine `sdk`, Debian, Ubuntu, and every
   `extra` variant. Not included: Alpine `aspnet`, `monitor`, `runtime` and `runtime-deps`, and Ubuntu
   chiseled images. Images without ICU run in globalization invariant mode.
2. **Add ICU in the final stage when the app needs culture-aware sorting or formatting** and the image has
   none. On Alpine the sample installs the ICU data package and sets
   `DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=false`.
3. **Do not remove ICU from an image that has it to save space:** it lives in an earlier layer and the
   image does not shrink.

## 3.2 Invariant mode
1. **`Microsoft.Data.SqlClient` and EF Core need ICU.** Without it, connecting to a database can throw
   `CultureNotFoundException` ("only the invariant culture is supported in globalization-invariant mode");
   the sample says this is by design. Install ICU rather than switching the mode back.
2. **Invariant mode gives only basic globalization behaviour,** so sorting and formatting stop following
   culture. Use it only for an app that does not depend on them, and prove it with a test.

## 3.3 Time zones
1. **The .NET images do not install `tzdata`;** the Debian images contain it at the time of the sample.
   Applications that only record time with `DateTime.UtcNow` do not need it.
2. **Without `tzdata`,** `DateTime.Now` equals `DateTime.UtcNow`, `TimeZoneInfo.Local` is UTC, and
   `TimeZoneInfo.FindSystemTimeZoneById` fails with an exception.
3. **Install `tzdata` in the final stage when code uses named zones,** and set the zone with the `TZ`
   environment variable or `/etc/timezone`. Store and convert in UTC and keep named zones at the edge of
   the system (our own guidance).

## Verification
- Start the final image and run a culture lookup and a named time zone lookup the code uses; both succeed.
- A formatted number and date match the expected culture in a test run inside the image.
