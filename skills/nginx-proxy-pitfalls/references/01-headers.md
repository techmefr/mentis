# nginx-proxy-pitfalls §1 — Information leaks and security headers

Every response that leaves the proxy carries, or lacks, a few headers. The boilerplate read for this block
(h5bp's nginx server configs) sets them from small files, one header each, with the reasoning in the
comments. The points below keep the reasoning, not the file layout.

## 1.1 The version banner
1. **Set `server_tokens off`** so nginx does not send its version number in the `Server` response header
   (h5bp's `server_software_information` file). The boilerplate includes this file at the top of its `http`
   block, so it applies to every server.

## 1.2 Send headers with `always`
1. **The boilerplate attaches HSTS, `X-Frame-Options`, `X-Content-Type-Options`, `Content-Security-Policy`
   and `Referrer-Policy` with the `always` parameter** of `add_header`. Its `Cache-Control` header is the
   exception and is added without it.
2. **Own reasoning, not from the files**: without `always`, nginx adds the header only to successful and
   redirect responses, so an error page would go out without it. The nginx documentation was not read for
   this block; confirm the behaviour for the version in use with `curl -I` against a missing path.
3. **Choose the value by content type where it matters.** The boilerplate computes `X-Frame-Options`, the
   `Content-Security-Policy`, the `Permissions-Policy` and the `Referrer-Policy` from a `map` on the response
   content type, so each header goes mainly to HTML documents, scripts and similar, not to every image.

```nginx
add_header X-Content-Type-Options nosniff always;
add_header Strict-Transport-Security "max-age=300" always;
```

   The `max-age` value in the sample is an illustration for a first rollout (§1.3), not the boilerplate's
   value.

## 1.3 HSTS cannot be revoked by the server
1. **`Strict-Transport-Security` makes a browser connect only over HTTPS**, whatever the user types, which
   closes the window of the first plain HTTP request that an attacker could downgrade or redirect.
2. **The header is not revocable.** You must be able to serve the site over HTTPS for the whole `max-age`
   you sent. When a valid TLS connection is lost, for example because a certificate expired, visitors see an
   error even when they try plain HTTP (h5bp's comment).
3. **Own guidance, not from the file**: start with a short `max-age`, and raise it only after the HTTPS
   setup, including certificate renewal, has run without incident. The boilerplate's own default is
   `max-age=16070400; includeSubDomains` (186 days), which is a decision for a mature setup, not a start.
4. **Preload is a separate, heavier step.** The boilerplate states the requirements for submitting a site to
   the preload list as: `includeSubDomains`, `preload`, and a `max-age` of at least 31536000 seconds (one
   year), with the list's own page as the source (version-bound: re-check the current requirements there).
   The boilerplate ships the preload form commented out. Own reasoning: `includeSubDomains` forces every
   subdomain to HTTPS for the period, so add `preload` only when that is true of all of them.

## 1.4 Framing and content type
1. **`X-Frame-Options` protects against clickjacking.** The boilerplate sends `DENY` for HTML and notes it
   may not suit everyone: `SAMEORIGIN` and `ALLOW-FROM` are the other values, and sending it on every page
   forbids even non-malicious framing.
2. **Send it at least on pages that allow a state-changing operation** (one-click purchase links, checkout
   or transfer confirmation pages, pages that change configuration), says the file.
3. **The `frame-ancestors` directive of `Content-Security-Policy` obsoletes the header for supporting
   browsers.** The boilerplate's policy includes `frame-ancestors 'none'`, so the two agree by default; keep
   them in step when you loosen one.
4. **`X-Content-Type-Options: nosniff` stops some browsers from MIME-sniffing a response.** It reduces drive-by
   download and cross-origin leak exposure and matters most where users upload content or where content could
   be treated as executable (the file's text).
5. **There is no universal CSP.** The file's own comment: no policy fits all websites, adapt the directives
   to your needs and validate the header with a CSP validator.

## 1.5 Verify
Fetch headers with `curl -I` for a normal page, a missing path and an asset, and check the three against the
intended list. Do not raise the HSTS `max-age` in the same change as a certificate or hostname change.
