# nginx-proxy-pitfalls: origin and source stamps

> Provenance of `skills/nginx-proxy-pitfalls`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from a configuration boilerplate and a README, never run by us: no nginx or Caddy
instance was started and no configuration was tested while writing it. Every file below was re-read in full
on 2026-10-16 before a rule was taken from it, and each repository's LICENSE file was read again.

## Sources (all read 2026-10-16, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| h5bp/server-configs-nginx (commit `d2f2c3e`), `nginx.conf`, `h5bp/basic.conf` | MIT (LICENSE.txt: MIT permission text, copyright H5BP, no title line) | Worker and descriptor limits, keepalive, the content-type maps, which headers are included |
| the same repository, `h5bp/security/` (server software information, strict transport security, x-frame-options, x-content-type-options, content-security-policy, referrer-policy) | MIT | Version banner, `always`, HSTS rationale and preload requirements, framing, sniffing, CSP |
| the same repository, `h5bp/location/security_file_access.conf` | MIT | Hidden files, `/.well-known/`, sensitive extensions |
| the same repository, `h5bp/web_performance/` (cache-control, cache_expiration, cache-file-descriptors, compression) | MIT | `public` versus `private`, backend-level cache headers, expiry and cache busting, the open-file cache, gzip settings |
| the same repository, `h5bp/tls/` (policy_balanced, policy_strict, ssl_engine, ocsp_stapling, certificate_files) | MIT | TLS profiles, NIST curve note, 0-RTT warning, session cache and tickets, cipher preference, stapling, default certificate |
| the same repository, `CHANGELOG.md` (opening entries read, down to 4.0.0) | MIT | `ssl_prefer_server_ciphers` set to `off` in 5.0.1 (July 2023) |
| lucaslorentz/caddy-docker-proxy (commit `c2c2b0e`), `README.md` (all 652 lines) | MIT (LICENSE file: MIT licence text, copyright Lucas Lorentz Lara 2018) | Ingress networks and their detection, quoting, directive order, label placement, generated file, certificate volume, image variants, controller and server modes |
| nginx documentation, modules `ngx_http_headers_module`, `ngx_http_proxy_module`, `ngx_http_ssl_module`, `ngx_http_core_module`, `ngx_http_gzip_module`, `ngx_http_upstream_module` (nginx.org) | official docs of the product, read 2026-10-20, facts only in our own words | `add_header` status list and inheritance, `expires epoch`, `proxy_pass` URI and DNS behaviour, `proxy_set_header` inheritance, keepalive recipe, buffering and timeout defaults, SSL defaults, session cache sizing, early-data replay, core defaults and location order, gzip defaults and the BREACH warning, upstream failure accounting |

The nginx documentation pages the boilerplate links to were first not read, then read on 2026-10-20 as the line above says, nor was Mozilla's TLS guidance. The
boilerplate repository is MIT as a whole; its comments were rewritten, not copied. The two code samples for
nginx are small adaptations (the dotfile deny pattern) and own illustrations (the two header lines); the
Compose sample adapts the README's quick start with a variable image tag, placeholder names and no
comments.

## Removed in the verification pass
1. **"Send security headers with `always` so error responses carry them"**: the files use `always` on those
   headers but never say why. The block keeps the observation and labels the reason as own reasoning (§1.2).
2. **"Start with a short HSTS max-age"**: the file does not say short; it says the header is not revocable.
   Kept as own guidance (§1.3).
3. **"Cache headers belong to the backend where it knows more"**: kept, narrowed to the file's wording
   ("highly preferred" at backend level).
4. **"Responses with an empty content type default to no-store"**: kept, with the correct subject: it is
   the boilerplate's `map`, not an nginx default.
5. **Header inheritance between `server` and `location` blocks** (a child's `add_header` replacing its
   parent's) was not in any file read and is not claimed.
6. **Not read, so not used**: `h5bp/cross-origin/`, `h5bp/errors/`, `h5bp/media_types/`, the
   `permissions-policy` and `cross-origin-policy` files, the pre-compressed content files, `conf.d`, the
   README of the boilerplate, and the CHANGELOG below the 4.0.0 entry.

## Verified 2026-10-21
Re-read the six nginx module pages, the h5bp files named in the table and the caddy-docker-proxy README. Corrected three points: §3.3 point 2 (the h5bp comment that ticket keys are never rotated automatically predates nginx 1.23.2, which rotates them with a shared session cache), §3.6 point 4 (from 1.29.7 the upstream keepalive cache and HTTP/1.1 are defaults) and §2.5 (the gzip page only says compressed TLS responses may be subject to BREACH; the finer reading is marked as ours).

## Not verified
1. **nginx behaviour**: `add_header` status list, `expires epoch`, directive defaults and inheritance are now confirmed by the nginx module pages (2026-10-20). Version thresholds quoted from those pages (1.29.3, 1.29.7) were not checked against release notes. That literal upstream names resolve at configuration load is general practice that neither the proxy nor the upstream page states; verify on your version.
2. **TLS values** (protocols, ciphers, curves, the NIST claim) and the **HSTS preload requirements** are as the
   boilerplate and its linked list state them and are version-bound to commit `d2f2c3e`; the TLS 1.3 and 0-RTT
   prerequisites (nginx 1.15.4, OpenSSL 1.1.1) are the strict file's.
3. **The "about 75 percent" gzip figure** is the file's statement, not measured; the 4000 sessions per megabyte figure is confirmed by the SSL module page.
4. **caddy-docker-proxy**: image tags and option defaults are as the README lists them; the ingress detection
   failure is described by the README with a link to an issue that was not followed; why the YAML quoting
   matters is not explained by the README.
5. **Written by us, not sourced:** the verification paragraphs, the `always` reasoning (§1.2), the short
   initial HSTS value (§1.3), the `preload` and `includeSubDomains` reasoning (§1.3), the public default trap
   in the cache map (§2.2), keeping sensitive files out of the tree (§2.1), leaving the descriptor cache off
   for rewritten files (§2.4), checking keepalive with `nginx -T` (§3.2), the descriptor reasoning (§3.1),
   the YAML-quoting explanation and label-placement consequences (§4.2), the alpine advice (§4.4), and the
   global-options remark (§4.2).

## Related blocks
`auth-gateway-proxy-pitfalls`, `docker-compose-file-pitfalls`, `docker-multi-project-dev-environment`,
`security-hardening`, `devops-conventions`.

Independent verification 2026-10-21: 55 checked, 52 matched, 3 corrected, 0 unverified
