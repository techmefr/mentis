---
name: nginx-proxy-pitfalls
description: "Use when an nginx configuration or a container reverse proxy (caddy-docker-proxy) is written or reviewed: the version banner, security headers (and whether error responses carry them), HSTS lock-in and preload, X-Frame-Options versus CSP frame-ancestors, denying dotfiles and backup, config, log and sql files, Cache-Control public versus private and shared caches, gzip settings, worker and keepalive limits, TLS policy and session tickets, and for label-driven proxies which Docker networks are served, the ingress network detection, quoting upstreams, directive order and the certificate volume."
---

# nginx-proxy-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the reverse proxy in front of an application. The four sections
share one premise: **the proxy answers for everything behind it, so what it leaks, caches or refuses is a
decision made for every response, and some of those decisions (HSTS, shared caches, a TLS policy) cannot be
taken back from the server side**. Authentication done at a proxy is a different problem, in
`auth-gateway-proxy-pitfalls`; the Docker socket a label-driven proxy needs is covered in
`docker-compose-file-pitfalls` §3.1.

## When
- Writing or reviewing an nginx `server` block, or adopting a boilerplate configuration.
- Adding a security header, HSTS, a cache header, compression or a TLS policy.
- A private page or a user-specific response is cached by a CDN or a shared proxy.
- A site is unreachable after a certificate lapsed, or a `.git`, `.sql` or backup file is served.
- Putting caddy-docker-proxy (Caddy configured from container labels) in front of Compose services, and a
  service is not routed, is routed to the wrong network, or its labels produce an unexpected Caddyfile.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Information leaks and security headers: version banner, `always`, HSTS, framing, MIME sniffing | a header is added or removed, HTTPS is forced, or a banner leaks | [`01-headers.md`](./references/01-headers.md) |
| 2 | Files and responses: dotfiles and sensitive extensions, `Cache-Control`, expiry, descriptor cache, gzip | a tree is exposed, a cache serves the wrong thing, or compression is tuned | [`02-files-cache-compression.md`](./references/02-files-cache-compression.md) |
| 3 | Connections and TLS: worker and descriptor limits, keepalive, session tickets, cipher preference, TLS policy, 0-RTT, stapling | limits are sized or a TLS policy is chosen or changed | [`03-connections-and-tls.md`](./references/03-connections-and-tls.md) |
| 4 | Label-driven container proxy (caddy-docker-proxy): ingress networks, quoting, order, labels placement, certificate volume, image variants | a service behind the proxy is not routed or produces a wrong Caddyfile | [`04-container-proxy.md`](./references/04-container-proxy.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: the response headers of a normal page and of a 404 were
fetched with `curl -I` and compared against the intended list (§1), requests for `/.git/config`, a `.sql` file
and a `/.well-known/` path were made and answered as intended (§2.1), the cache headers of a page, an API
response and an asset were read (§2.2), `nginx -t` passed and the TLS policy was checked with a scanner or a
`openssl s_client` handshake from the oldest client you support (§3), and for the label-driven proxy the
generated Caddyfile was read in the container, not guessed from the labels (§4.3). A configuration that only
loads is not verified.

## Guardrails
- Never turn HSTS on for a long period before certificate renewal is dependable (§1.3).
- Never mark a document or a per-user response `public` (§2.2).
- Never leave a dotfile or a backup, config, log or sql extension served from a web tree (§2.1).
- Never enable TLS 0-RTT without passing the early-data signal to the application (§3.4).
- Never route a container proxy by guessing its networks; set the ingress network (§4.1).
- This block states nginx and Caddy behaviour as of the repositories read on the date in
  [`references/origin.md`](./references/origin.md). The nginx documentation itself was not read; TLS settings,
  HSTS preload requirements and header defaults move, so check a policy against a maintained profile before
  using it. Nothing was run while writing it.

## Origin
Rewritten from the h5bp nginx server-configs boilerplate (MIT: main file, security, TLS, file access, cache,
compression, and its changelog) and the README of caddy-docker-proxy (MIT), read 2026-10-16. 🟡: never run
by us; open points are in [`references/origin.md`](./references/origin.md).
