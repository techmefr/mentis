# § 3 — Actuator, security filters and tests

> Section 3 of `skills/spring-boot-conventions`. Read it when an operational endpoint is exposed, a request
> matcher, CSRF or CORS rule is written, or a test annotation is chosen. Read 2026-10-02 from the Spring Boot
> reference (4.2.0-SNAPSHOT: actuator endpoints, testing) and the Spring Security reference (authorize HTTP
> requests, CSRF, CORS).

1. **Expose actuator endpoints by allow-list.** By default just the health endpoint answers over HTTP, and
   the documentation warns that endpoints may carry sensitive information. List the ones you need in the
   include property, not a wildcard; before exposing one, check what it returns, and secure or firewall it.
   The values of `env` and `configprops` are masked by default; a setting that unmasks them is a decision to
   record. The shutdown endpoint is disabled by default and stays so.
2. **Access and exposure are two switches.** An endpoint answers only when access is permitted and it is
   exposed. To make access opt-in, set the default access to none and grant it per endpoint.
3. **When you define your own security filter chain, the framework's default actuator protection backs off
   completely.** Add the actuator rules to your chain; do not assume the defaults still apply.
4. **Requests are matched in the order written and the first match wins.** Put specific matchers before general
   ones and end with a single catch-all rule (`authenticated` at least); the authorization filter is last in
   the chain by default, so it decides after authentication has run.
5. **CSRF protection is on by default for unsafe methods and stays on for browser sessions.** Turn it off only
   for an API that carries no ambient credential (a bearer token in a header, no cookie), and say why beside
   the line. Where the page does not need to read the token cookie from JavaScript, keep it HTTP-only (the
   documentation recommends the default cookie repository over the JavaScript-readable one for that case).
   Actuator endpoints that use POST, PUT or DELETE answer 403 under the default CSRF setting.
6. **CORS is processed before security.** A preflight request carries no cookie, so if security runs first it
   rejects it as unauthenticated. Provide the CORS configuration source bean so the filter is integrated, and
   list explicit origins and methods.
7. **A full application context is the exception.** Use the slice annotation for the layer: a web-layer slice
   for mappings, validation and error handling; a data slice for repositories. Each slice scans only its own
   component types and loads a restricted set of auto-configurations; combining two slice annotations in one
   test is unsupported, so add the other slice's auto-configure annotation by hand.
8. **Configuration specific to one layer does not go on the application class.** Slices start from it, so
   enabling auditing or a scan there loads it into every slice; put it in a dedicated configuration class
   imported where needed. An explicit component-scan directive on the application class disables the filters
   that make slicing work.
9. **A mock web environment does not start a server;** it is faster and covers mappings, validation and
   advice. Use a random port only for what depends on the container. With a random port the client and the
   server run in separate threads, so a test-level transaction does not roll back the server's writes: clean
   data explicitly.
10. **Data slices are transactional and roll back by default,** and replace the database with an embedded one
    unless told otherwise. Run persistence tests against the production engine (the replacement annotation
    switches the swap off), since dialect and locking differ.
11. **Test configuration classes marked as such are not picked up by scanning** and are imported where
    needed. The application context is cached across tests that share a configuration, so keep the number of
    distinct configurations low.
12. **Mock beans with the framework's bean-override annotations at the boundary (a remote client),** not a
    repository in a service test that is meant to exercise the query.
