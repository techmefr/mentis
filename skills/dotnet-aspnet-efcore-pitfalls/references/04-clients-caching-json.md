# dotnet-aspnet-efcore-pitfalls §4 — Clients, caching, JSON

## 4.1 HttpClient factory
1. **Do not capture a typed client in a singleton.** The factory recycles handlers (default lifetime two
   minutes) so clients react to DNS changes; once a typed client is captured in a singleton, the factory
   has no control over it. Inject `IHttpClientFactory` and create clients when needed, or use
   `SocketsHttpHandler` with `PooledConnectionLifetime` as the primary handler.
2. **Choose one strategy:** short-lived clients from the factory, or long-lived clients with
   `PooledConnectionLifetime`.
3. **Do not derive client names from unbounded input.** The number of registered named clients should be
   bounded.
4. **Do not cache scope-related data (such as `HttpContext` values) in a message handler.** Handlers have
   their own DI scope that can outlive the request scope.
5. **Set headers per request rather than mutating `DefaultRequestHeaders` on a shared client.** This is our
   own guidance; the documentation sets defaults at registration time only.

## 4.2 Memory cache
1. **Without `SizeLimit` the cache grows without bound,** and the runtime does not trim it under memory
   pressure.
2. **When a size limit is set, every entry must specify a size,** in one unit all users of the cache agree
   on. An entry is not cached if its size would exceed the limit.
3. **Use a dedicated cache singleton for size-limited entries.** A shared injected cache with a size limit
   can make other users of it fail.
4. **Do not rely on a sliding expiration alone.** An entry that keeps being read never expires; combine it
   with an absolute expiration.

## 4.3 HybridCache
1. **`HybridCache` lets only one concurrent caller per key run the factory;** the others wait for that
   result. Prefer it to a hand-written check-then-set around `IMemoryCache`. It is registered with
   `AddHybridCache`; confirm the package and framework version your project targets.
2. **The key must uniquely identify the data.** If the value depends on the user or tenant, put that
   identifier in the key; a key without it serves one person's data to another.
3. **Remove entries explicitly when the source data changes** (`RemoveAsync`, or tags) rather than waiting
   for expiry.

## 4.4 System.Text.Json
1. **From .NET 9, `JsonSerializerOptions.RespectNullableAnnotations` enforces non-nullable reference types
   on serialisation and deserialisation,** and an application-wide switch exists
   (`System.Text.Json.Serialization.RespectNullableAnnotationsDefault`). It was added as opt-in to avoid
   breaking existing apps; the documentation recommends enabling it in new apps.
2. **It does not reject a missing property.** The serializer treats required and non-nullable as separate
   concepts, and an explicit `null` is not the same as an absent property; use `required` for presence.
3. **Use an explicit discriminator for polymorphism** mapped to a closed list of types, never a type name
   read from the payload. This is our own guidance.

## Verification
- A test posts null to a non-nullable property and gets a 400.
- Two concurrent requests with different headers each see only their own.
- Filling the cache past its limit leaves the process memory flat.
