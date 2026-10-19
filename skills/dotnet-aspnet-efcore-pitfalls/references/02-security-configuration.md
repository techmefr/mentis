# dotnet-aspnet-efcore-pitfalls §2 — Security configuration

Configuration that works on one process and breaks, or opens a hole, once the app runs in containers
behind a proxy.

## 2.1 Data Protection keys
Cookies, antiforgery tokens and temporary data are protected with a key ring the framework manages.
1. **Plan the key ring for horizontal scale.** The ASP.NET Core scaling guide shows that a form relying on
   antiforgery fails by default when the app scales out, because the data protection service does not share
   keys between instances. Persist the ring in storage that every replica can reach.
2. **Set the same application name in every app that shares the key ring.** By default the system isolates
   apps by content root path, even with a shared repository; the application name should match across
   deployments of the app.
3. **An explicit key persistence location deregisters the default encryption at rest.** Keys are then not
   encrypted unless you configure a key encryption mechanism (for example a certificate).
4. **Never delete a key from the ring to "reset" it.** Data protected by that key becomes permanently
   undecipherable, and there is no emergency override.

## 2.2 Antiforgery
1. **A failed antiforgery check returns 400.** Check the key ring (§2.1) before suspecting the form.
2. **Do not turn antiforgery off to make a post work.** Find why the token is missing. This is our own
   guidance.

## 2.3 CORS
1. **`AllowAnyOrigin` is insecure:** any website can make cross-origin requests. Combined with
   `AllowCredentials` it can allow cross-site request forgery; the framework returns an invalid CORS
   response for that pair, and bypassing the built-in check defeats the protection.
2. **List the allowed origins explicitly**, from configuration, one set per environment. This is our own
   guidance.

## 2.4 HTTPS, HSTS and certificates
1. **Do not use `RequireHttpsAttribute` on a Web API that receives sensitive data.** It redirects browsers
   with a status code; API clients may not follow redirects and may already have sent data over HTTP. An API
   project should only listen and respond over HTTPS, or disable the redirect.
2. **HSTS is a browser-only instruction.** The default API projects do not include it, and other callers
   ignore it.
3. **Never ship a development certificate in a redistributable image.** Set
   `DOTNET_GENERATE_ASPNET_CERTIFICATE` to `false` before the .NET CLI first runs to skip generating it,
   and supply a real certificate or terminate TLS in front of the container.

## Verification
- Start two replicas against a shared key location; a form rendered by one posts successfully to the other.
- A cross-origin request with credentials from an unlisted origin is rejected.
- The image contains no `.pfx` and the container starts without a development certificate.
