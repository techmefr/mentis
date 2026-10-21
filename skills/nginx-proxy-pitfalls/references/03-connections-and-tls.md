# nginx-proxy-pitfalls §3 — Connections and TLS

Connection limits and TLS settings are trade-offs between capacity, latency and client compatibility. The
boilerplate states the trade-off next to each value; the points below keep it.

## 3.1 Worker and descriptor limits
1. **The maximum number of connections is `worker_processes` times `worker_connections`** (h5bp's main
   file). The boilerplate sets `worker_processes auto`, so it follows the CPU count.
2. **Keep `worker_connections` below `worker_rlimit_nofile`**, the number of open files per worker. The
   boilerplate sets 8000 connections and 8192 descriptors. A proxy holds a descriptor for each client and each
   upstream connection; own reasoning for why the file limit must leave room.
3. **The boilerplate's comment on the connection count**: needing more than that means tuning the operating
   system next. Treat the numbers as a starting point for your host, not a capacity figure.

## 3.2 Keepalive
1. **`keepalive_timeout` is a pool trade-off.** Longer values are better for each client, particularly over
   TLS, but tie up worker connections for longer. The default is 75 seconds; the main file sets 20 seconds.
2. **The TLS file sets a higher value (300 seconds)** to cut repeated handshakes, with the warning that this
   should only be done when you serve mostly HTTPS.
3. **The two files give different values and the files do not say which one wins.** Own note: if you include
   both, check which value is in effect with `nginx -T`, and state the one you chose.

## 3.3 Sessions and cipher preference
1. **Cache TLS sessions** to cut expensive handshakes (the SSL module page: the default is `none`, a shared
   cache gives about 4000 sessions per megabyte, and the docs recommend the shared cache alone). The boilerplate keeps them for 24 hours in a shared
   cache of 10 megabytes; the file says one megabyte holds about 4000 sessions, so this holds about 40000.
   The `10m` is a size, not a time.
2. **Tickets are on by default** (the directive appeared in 1.5.9). The boilerplate turns them off, with the comment that ticket keys are not rotated automatically (only a reload signal or a restart does it, and a restart loses the previous key and resets earlier sessions), so enable them only with a manual rotation mechanism (h5bp TLS engine file). That comment is older than nginx 1.23.2: the SSL module page (read 2026-10-21) says a shared session cache also generates, stores and periodically rotates ticket keys unless `ssl_session_ticket_key` is set, so on 1.23.2 or later with a shared cache automatic rotation exists, and the manual-rotation duty applies once you set the key file yourself or run several servers that must share keys.
3. **Let the client choose the cipher** (`ssl_prefer_server_ciphers off`) when the TLS 1.2 and 1.3 ciphers
   in the policy are not considered dangerous. The boilerplate's changelog shows this moved to `off` in its
   5.0.1 release (July 2023), so older copies of the boilerplate had a different setting.

## 3.4 Choose a TLS policy and re-read it
1. **TLS settings are version-bound.** The boilerplate points at Mozilla's server-side TLS recommendations;
   use a maintained profile and re-read it when you upgrade, rather than copying a value from an old
   article or from this block.
2. **Two profiles in the boilerplate, as a worked example.** Balanced, for a wide range of clients: TLS 1.2
   only in the boilerplate's version, a cipher list, and the curves `X25519`, `prime256v1`, `secp521r1`,
   `secp384r1`. Strict, for services that do not need backward compatibility: TLS 1.2 and 1.3, the same
   ciphers, and `X25519` only. The strict file warns that old clients may get errors, and that you can add
   the other curves back to support Microsoft Edge and Safari.
3. **The boilerplate calls the NIST curves "known to be weak and potentially vulnerable"** and keeps them in
   the balanced profile only because Microsoft Edge and Safari require them (its comment, relayed here; the
   claim itself was not checked).
4. **TLS 1.3 and 0-RTT need nginx 1.15.4 or later and OpenSSL 1.1.1 or later**, per the strict file
   (version-bound to that file). The SSL module page: `ssl_protocols` defaults to TLS 1.2 and 1.3 (1.3 by
   default since 1.23.4, needing OpenSSL 1.1.1), `ssl_prefer_server_ciphers` defaults to `off`.
5. **Do not enable `ssl_early_data` blindly.** Requests sent in early data are subject to replay attacks.
   The boilerplate ships the directive commented out, and says to pass the `$ssl_early_data` variable to the
   application with a request header, which should answer `425 Too Early` for anything that could contain
   user-supplied data. OpenSSL's own replay protection is disabled on nginx because it conflicts with session
   resumption; `ssl_conf_command Options AntiReplay;` re-enables it.

## 3.5 Certificate and stapling
1. **The default certificate is served to clients that do not support SNI** (the boilerplate's
   certificate file). The certificate file may contain the intermediate certificate.
2. **With OCSP stapling on the issuer must be known**: include the intermediate in the certificate file or load it through `ssl_trusted_certificate` if the certificate
   file lacks it (the same file).
3. **Stapling needs a `resolver`.** The boilerplate sets `ssl_stapling` and `ssl_stapling_verify` on, a
   60-second validity and a 2-second resolver timeout, and lists three public DNS operators as alternatives.
   Choose the resolver your network policy allows; do not copy the list by default.

## 3.6 Proxying to an upstream
From the nginx proxy and upstream module pages (facts only).
1. **`proxy_pass` with a URI part replaces the matched location prefix; without one it passes the request URI
   unchanged.** `location /name/ { proxy_pass http://app/remote/; }` turns `/name/x` into `/remote/x`. In a
   regex or named location use no URI, and after a `rewrite ... break` the URI part is ignored. A trailing slash
   on the upstream is therefore a behaviour change, not style.
2. **In practice names are resolved when the configuration loads** (the proxy and upstream pages do not say when; verify on your version). A literal host that does not resolve at start can stop
   nginx from starting, and a container that later gets a new address is not noticed. With a variable in
   `proxy_pass` the name is resolved per request and needs a `resolver`. For a named upstream, `server ... resolve`
   re-resolves at run time, needs a `resolver` and a shared-memory `zone`.
3. **`proxy_set_header` has the same all-or-nothing inheritance as `add_header`**: one such line in a location drops
   the ones set above it. The default `Host` sent upstream is `$proxy_host`, not the client's; pick `$host` or
   `$http_host` on purpose.
4. **Upstream keepalive needs three things together**: a `keepalive` line in the `upstream`, HTTP/1.1 to it and
   an empty `Connection` header. Older versions default to HTTP/1.0 and `Connection: close`, which defeats it;
   from 1.29.7 the pages make all three defaults (`proxy_http_version` 1.1, `keepalive 32 local` in the upstream, and the upstream page's example drops the `Connection` line it keeps for earlier versions), so check your version.
5. **Buffering is on.** For server-sent events or long polling turn `proxy_buffering` off for that location (or
   let the app send `X-Accel-Buffering: no`). `proxy_read_timeout` is 60 seconds between two reads, not for the
   whole response, so a slow steady stream survives and a silent one is cut.
6. **A request body over `client_max_body_size` (1 MB by default) gets 413** before it reaches the app.
7. **An upstream that redirects to its own address leaks it**: use `proxy_redirect` to rewrite `Location`.
8. **A group with one server ignores `max_fails` and `fail_timeout`**; with several, one failure within 10
   seconds takes a server out for 10 seconds by default.
9. **Location matching is not top to bottom for prefixes**: exact `=` wins, then the longest prefix (stopping at
   `^~`), then the first matching regex in file order. `root` appends the URI; `alias` replaces the location part.

## 3.7 Verify
Run `nginx -t` and `nginx -T` and read the effective keepalive, protocols and ciphers. Handshake from the
oldest client you support and from a current one; if the old one is refused on purpose, say so in the
change.
